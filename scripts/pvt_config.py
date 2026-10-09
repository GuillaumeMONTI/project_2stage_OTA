PROCESS_CORNERS = [
    ("SS",   "ss"),
    ("SNFP", "sf"),
    ("TT",   "tt"),
    ("FNSP", "fs"),
    ("FF",   "ff"),
]

TEMPERATURES_C = [
    -40,
    27,
    125,
]

SUPPLIES_V = [
    1.62,
    1.80,
    1.98,
]

# PVT is performed at maximum specified capacitive load.
CL_PF = 4.0

# Hard design requirements.
A0_MIN_DB = 80.0
PM_MIN_DEG = 60.0
GM_MIN_DB = 10.0
