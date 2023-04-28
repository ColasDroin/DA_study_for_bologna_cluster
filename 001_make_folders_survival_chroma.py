# %%
import tree_maker
from tree_maker import NodeJob
from tree_maker import initialize
import time
import os
from pathlib import Path
import itertools
import numpy as np
import yaml
from user_defined_functions import generate_run_sh
from user_defined_functions import generate_run_sh_htc

# Import the configuration
config = yaml.safe_load(open("config.yaml"))

# The user defines the variable to scan
# machine parameters scans
qx0 = [62.316]
qy0 = [60.321]
optics_file = ["optics_repository/flatcc/opt_flathv_75_180_1500_thin.madx"]
beam_sigt = [0.0761]
beam_npart = [1.4e11]
oct_current = [60.0]
enable_crabs = [True]
mode = "b1_with_bb"

on_x1 = 250.0
on_x8v = 170
on_x8h = 0.0
on_disp = 1
chroma = [5, 15]
bunch_nb = [
    525,
    1132,
    2272,  # Low difference between chromas
    2622,
    3009,
    2996,  # High difference between chromas
    252,
    438,
    2434,
]  # Moderate difference between chromas

study_name = f"opt_flathv_75_1500_withBB_1p4_survival_chromas"

children = {}
children[study_name] = {}
children[study_name]["children"] = {}

for optics_job, (
    myq1,
    myq2,
    my_optics,
    my_sigt,
    my_npart,
    my_oct,
    my_crabs,
    my_chroma,
    my_bunch_nb,
) in enumerate(
    itertools.product(
        qx0, qy0, optics_file, beam_sigt, beam_npart, oct_current, enable_crabs, chroma, bunch_nb
    )
):
    # # Ignore conditions below the upper diagonal
    # if myq2 < (myq1 - 2 + 0.005):
    #     continue

    optics_children = {}
    children[study_name]["children"][f"madx_{optics_job:03}"] = {
        "qx0": float(myq1),
        "qy0": float(myq2),
        "mode": mode,
        "optics_file": my_optics,
        "beam_sigt": my_sigt,
        "beam_npart": my_npart,
        "oct_current": my_oct,
        "enable_crabs": my_crabs,
        "chromaticity_x": my_chroma,
        "chromaticity_y": my_chroma,
        "knob_settings": {
            "on_x1": on_x1,
            "on_x5": on_x1,
            "on_x8v": on_x8v,
            "on_x8h": on_x8h,
            "on_disp": on_disp,
        },
        "beambeam_config": {"bunch_to_track": my_bunch_nb},
        "log_file": f"{os.getcwd()}/{study_name}/madx_{optics_job:03}/tree_maker.log",
        "children": optics_children,
    }
    for track_job in range(50):
        optics_children[f"xsuite_{track_job:03}"] = {
            "particle_file": f"../../particles/{track_job:03}.parquet",
            "xline_json": "../xsuite_lines/line_bb_for_tracking.json",
            "n_turns": int(1000000),
            "log_file": f"{os.getcwd()}/{study_name}/madx_{optics_job:03}/xsuite_{track_job:03}/tree_maker.log",
        }

# if config["root"]["use_yaml_children"] == False:
config["root"]["children"] = children
config["root"]["setup_env_script"] = os.getcwd() + "/miniconda/bin/activate"

# Create tree object
start_time = time.time()
root = initialize(config)
print("Done with the tree creation.")
print("--- %s seconds ---" % (time.time() - start_time))

# From python objects we move the nodes to the file-system.
start_time = time.time()
# root.make_folders(generate_run_sh)
root.make_folders(generate_run_sh_htc)
print("The tree folders are ready.")
print("--- %s seconds ---" % (time.time() - start_time))

import shutil

shutil.move("tree_maker.json", f"tree_maker_{study_name}.json")
shutil.move("tree_maker.log", f"tree_maker_{study_name}.log")
