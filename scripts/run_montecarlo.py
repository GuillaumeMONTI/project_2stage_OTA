#!/usr/bin/env python3

import argparse
import csv
import math
import os
import re
import subprocess
import tempfile
from concurrent.futures import ThreadPoolExecutor, as_completed
from pathlib import Path
from statistics import mean, stdev


ROOT = Path("/foss/designs/project_2stage_OTA")

BASE_NETLIST = ROOT / "work/tb_ota_2stage_mc.spice"

OUTDIR = ROOT / "work/montecarlo"
TMPDIR = OUTDIR / "tmp"
FAILDIR = OUTDIR / "failed"

RESULTS_CSV = OUTDIR / "mc_results.csv"
SUMMARY_CSV = OUTDIR / "mc_summary.csv"

VDD_VALUES = [1.62, 1.80, 1.98]
TEMP_VALUES = [-40, 27, 125]

VIN_DC = 0.600


RE_VOUT = re.compile(
    r"v\(vout\)\s*=\s*([-+0-9.eE]+)",
    re.IGNORECASE
)

RE_A0 = re.compile(
    r"a0db\[0\]\s*=\s*([-+0-9.eE]+)",
    re.IGNORECASE
)


def make_netlist(base_text, vdd, temp_c):
    text = base_text

    # Replace VDD source.
    text, n = re.subn(
        r"(?mi)^\s*V1\s+VDD\s+0\s+.*$",
        f"V1 VDD 0 {vdd}",
        text,
        count=1
    )

    if n != 1:
        raise RuntimeError("Could not find unique V1 VDD source.")

    # Replace existing .temp, or insert one before .control.
    if re.search(r"(?mi)^\s*\.temp\s+", text):
        text = re.sub(
            r"(?mi)^\s*\.temp\s+.*$",
            f".temp {temp_c}",
            text,
            count=1
        )
    else:
        text = re.sub(
            r"(?mi)^\.control",
            f".temp {temp_c}\n\n.control",
            text,
            count=1
        )

    return text


def run_one(base_text, vdd, temp_c, sample):
    netlist_text = make_netlist(base_text, vdd, temp_c)

    TMPDIR.mkdir(parents=True, exist_ok=True)
    FAILDIR.mkdir(parents=True, exist_ok=True)

    with tempfile.NamedTemporaryFile(
        mode="w",
        suffix=".spice",
        dir=TMPDIR,
        delete=False
    ) as f:
        f.write(netlist_text)
        netlist_path = Path(f.name)

    try:
        proc = subprocess.run(
            ["ngspice", "-b", str(netlist_path)],
            cwd=ROOT,
            text=True,
            stdout=subprocess.PIPE,
            stderr=subprocess.STDOUT
        )

        log = proc.stdout

        mv = RE_VOUT.search(log)
        ma = RE_A0.search(log)

        if proc.returncode != 0 or mv is None or ma is None:
            fail_name = (
                f"VDD{vdd:.2f}_T{temp_c:+d}_"
                f"S{sample:04d}.log"
            )

            (FAILDIR / fail_name).write_text(log)

            return {
                "vdd": vdd,
                "temp_c": temp_c,
                "sample": sample,
                "status": "FAIL",
                "vout_v": "",
                "a0_db": "",
                "vos_uv": ""
            }

        vout = float(mv.group(1))
        a0_db = float(ma.group(1))

        # Open-loop gain in linear V/V.
        a0_lin = 10.0 ** (a0_db / 20.0)

        # Unity-follower finite-gain correction:
        #
        # Vout = A0 * (Vin - Vout + Vos)
        #
        # therefore:
        #
        # Vos = Vout*(1 + 1/A0) - Vin
        #
        vos_v = vout * (1.0 + 1.0 / a0_lin) - VIN_DC

        return {
            "vdd": vdd,
            "temp_c": temp_c,
            "sample": sample,
            "status": "PASS",
            "vout_v": vout,
            "a0_db": a0_db,
            "vos_uv": vos_v * 1e6
        }

    finally:
        try:
            netlist_path.unlink()
        except FileNotFoundError:
            pass


def load_completed():
    done = set()

    if not RESULTS_CSV.exists():
        return done

    with RESULTS_CSV.open() as f:
        reader = csv.DictReader(f)

        for row in reader:
            done.add((
                float(row["vdd"]),
                int(row["temp_c"]),
                int(row["sample"])
            ))

    return done


def generate_summary():
    rows = []

    with RESULTS_CSV.open() as f:
        reader = csv.DictReader(f)

        for row in reader:
            if row["status"] != "PASS":
                continue

            rows.append({
                "vdd": float(row["vdd"]),
                "temp_c": int(row["temp_c"]),
                "sample": int(row["sample"]),
                "a0_db": float(row["a0_db"]),
                "vos_uv": float(row["vos_uv"])
            })

    summary_rows = []

    for temp_c in TEMP_VALUES:
        for vdd in VDD_VALUES:

            subset = [
                r for r in rows
                if r["vdd"] == vdd and r["temp_c"] == temp_c
            ]

            if len(subset) < 2:
                continue

            vos = [r["vos_uv"] for r in subset]
            a0 = [r["a0_db"] for r in subset]

            vos_mu = mean(vos)
            vos_sigma = stdev(vos)

            a0_mu = mean(a0)
            a0_sigma = stdev(a0)

            summary_rows.append({
                "vdd": vdd,
                "temp_c": temp_c,
                "n": len(subset),

                "vos_mean_uv": vos_mu,
                "vos_sigma_uv": vos_sigma,
                "vos_3sigma_uv": 3.0 * vos_sigma,
                "vos_mean_minus_3sigma_uv":
                    vos_mu - 3.0 * vos_sigma,
                "vos_mean_plus_3sigma_uv":
                    vos_mu + 3.0 * vos_sigma,
                "vos_min_uv": min(vos),
                "vos_max_uv": max(vos),

                "a0_mean_db": a0_mu,
                "a0_sigma_db": a0_sigma,
                "a0_3sigma_db": 3.0 * a0_sigma,
                "a0_mean_minus_3sigma_db":
                    a0_mu - 3.0 * a0_sigma,
                "a0_mean_plus_3sigma_db":
                    a0_mu + 3.0 * a0_sigma,
                "a0_min_db": min(a0),
                "a0_max_db": max(a0),
            })

    if not summary_rows:
        return

    with SUMMARY_CSV.open("w", newline="") as f:
        writer = csv.DictWriter(
            f,
            fieldnames=summary_rows[0].keys()
        )
        writer.writeheader()
        writer.writerows(summary_rows)

    print("\nMonte Carlo summary")
    print("=" * 92)

    for r in summary_rows:
        print(
            f"VDD={r['vdd']:.2f} V  "
            f"T={r['temp_c']:+4d} C  "
            f"N={r['n']:3d}  |  "
            f"Vos={r['vos_mean_uv']:+8.1f} uV "
            f"sigma={r['vos_sigma_uv']:7.1f} uV "
            f"3sigma={r['vos_3sigma_uv']:7.1f} uV  |  "
            f"A0={r['a0_mean_db']:6.2f} dB "
            f"sigma={r['a0_sigma_db']:.3f} dB"
        )


def main():
    global VDD_VALUES, TEMP_VALUES
    global OUTDIR, TMPDIR, FAILDIR
    global RESULTS_CSV, SUMMARY_CSV

    parser = argparse.ArgumentParser()

    parser.add_argument(
        "--samples",
        type=int,
        default=300
    )

    parser.add_argument(
        "--jobs",
        type=int,
        default=4
    )

    parser.add_argument(
        "--vdd",
        nargs="+",
        type=float,
        default=None
    )

    parser.add_argument(
        "--temp",
        nargs="+",
        type=int,
        default=None
    )

    parser.add_argument(
        "--tag",
        type=str,
        default=None
    )

    args = parser.parse_args()

    if args.vdd is not None:
        VDD_VALUES = args.vdd

    if args.temp is not None:
        TEMP_VALUES = args.temp

    if args.tag is not None:
        OUTDIR = (
            ROOT /
            "work/montecarlo/iterations" /
            args.tag
        )

        TMPDIR = OUTDIR / "tmp"
        FAILDIR = OUTDIR / "failed"

        RESULTS_CSV = OUTDIR / "mc_results.csv"
        SUMMARY_CSV = OUTDIR / "mc_summary.csv"

    OUTDIR.mkdir(parents=True, exist_ok=True)
    TMPDIR.mkdir(parents=True, exist_ok=True)
    FAILDIR.mkdir(parents=True, exist_ok=True)

    base_text = BASE_NETLIST.read_text()

    completed = load_completed()

    jobs = []

    for temp_c in TEMP_VALUES:
        for vdd in VDD_VALUES:
            for sample in range(1, args.samples + 1):

                key = (vdd, temp_c, sample)

                if key not in completed:
                    jobs.append((vdd, temp_c, sample))

    total_requested = (
        len(VDD_VALUES) *
        len(TEMP_VALUES) *
        args.samples
    )

    print(f"Requested samples : {total_requested}")
    print(f"Already completed : {len(completed)}")
    print(f"Remaining         : {len(jobs)}")
    print(f"Parallel jobs     : {args.jobs}")

    fieldnames = [
        "vdd",
        "temp_c",
        "sample",
        "status",
        "vout_v",
        "a0_db",
        "vos_uv"
    ]

    file_exists = RESULTS_CSV.exists()

    with RESULTS_CSV.open("a", newline="") as f:
        writer = csv.DictWriter(
            f,
            fieldnames=fieldnames
        )

        if not file_exists:
            writer.writeheader()

        finished = 0
        failed = 0

        with ThreadPoolExecutor(
            max_workers=args.jobs
        ) as executor:

            futures = {
                executor.submit(
                    run_one,
                    base_text,
                    vdd,
                    temp_c,
                    sample
                ): (vdd, temp_c, sample)
                for vdd, temp_c, sample in jobs
            }

            for future in as_completed(futures):
                result = future.result()

                writer.writerow(result)
                f.flush()

                finished += 1

                if result["status"] != "PASS":
                    failed += 1

                if (
                    finished % 25 == 0
                    or finished == len(jobs)
                ):
                    print(
                        f"{finished:4d}/{len(jobs)} new runs "
                        f"completed, failures={failed}"
                    )

    generate_summary()

    print()
    print(f"Results : {RESULTS_CSV}")
    print(f"Summary : {SUMMARY_CSV}")


if __name__ == "__main__":
    main()
