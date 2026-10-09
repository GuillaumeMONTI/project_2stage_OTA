from pathlib import Path
import re

RAW = Path("work/transistor/noise_integrated.raw")

text = RAW.read_text(errors="ignore")


# ------------------------------------------------------------
# Parse ngspice ASCII raw file
# ------------------------------------------------------------

m_var = re.search(
    r"Variables:\s*\n(.*?)\nValues:",
    text,
    re.S,
)

m_val = re.search(
    r"Values:\s*\n(.*)",
    text,
    re.S,
)

if not m_var or not m_val:
    raise SystemExit("Could not parse raw file.")


variables = []

for line in m_var.group(1).splitlines():

    parts = line.split()

    if len(parts) >= 2:

        index = int(parts[0])
        name = parts[1]

        variables.append(
            (index, name)
        )


# noise2 is normally a single integrated-noise point.
# Extract all numerical values from the Values section.

values_text = m_val.group(1)

numbers = []

for token in re.findall(
    r"[+-]?(?:\d+\.\d*|\.\d+|\d+)"
    r"(?:[eE][+-]?\d+)?",
    values_text,
):
    numbers.append(float(token))


# ASCII raw format interleaves point index and vector values.
# For a one-point noise2 plot the final N values correspond
# to the N variables.

nvars = len(variables)

if len(numbers) < nvars:
    raise SystemExit(
        f"Only {len(numbers)} numbers found "
        f"for {nvars} variables."
    )

vals = numbers[-nvars:]


# ------------------------------------------------------------
# Keep useful individual integrated output-noise contributors
# ------------------------------------------------------------

rows = []

for (_, name), value in zip(
    variables,
    vals,
):

    lname = name.lower()

    # Skip frequency and total vectors
    if (
        "frequency" in lname
        or lname in {
            "onoise_total",
            "inoise_total",
        }
    ):
        continue

    # Most contribution vectors contain onoise
    if "onoise" not in lname:
        continue

    rows.append(
        (abs(value), name)
    )


rows.sort(reverse=True)


print()
print("Largest integrated output-noise contributors")
print("1 Hz -> 1 MHz")
print("=" * 78)

for value, name in rows[:25]:

    print(
        f"{value:14.6e}   {name}"
    )
