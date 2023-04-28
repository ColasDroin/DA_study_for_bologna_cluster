# %%
"""
Example of a chronjob
"""

# %%
import tree_maker
import yaml
from tree_maker import NodeJob
import pandas as pd
import awkward as ak
from joblib import Parallel, delayed
import time

start = time.time()


# my_study='opt_flatvh_75_300_1500'
# my_study='opt_flathv_75_1500_withBB_chroma15_octscan'
my_study='opt_flathv_75_1500_withBB_chroma5_filling'
# my_study = "opt_flathv_75_1500_withBB_chroma5_1p4"
# my_study = "opt_flathv_75_1500_withBB_chroma15_1p4"
# my_study='opt_flathv_75_1500_withBB_chroma15_octphi2'
# my_study = "opt_flathv_75_1500_withBB_chroma15_1p4_all_bunches"
# my_study = tree_maker.tree_from_json(
#     "tree_maker_opt_flathv_75_1500_withBB_chroma15_b1891_octscan.json"
# )
problematic = []
try:
    # root=tree_maker.tree_from_json(f'{my_study}/tree_maker.json')
    root = tree_maker.tree_from_json(f"tree_maker_{my_study}.json")
except Exception as e:
    print(e)
    print("Probably you forgot to edit the address of you json file...")

my_list = []

for node in root.generation(2):
    with open(f"{node.get_abs_path()}/config.yaml", "r") as fid:
        config_parent = yaml.safe_load(fid)
    for node_child in node.children:
        with open(f"{node_child.get_abs_path()}/config.yaml", "r") as fid:
            config = yaml.safe_load(fid)
        try:
            particle = pd.read_parquet(f"{node_child.get_abs_path()}/{config['particle_file']}")
            df = pd.read_parquet(f"{node_child.get_abs_path()}/output_particles.parquet")
            df["path 1"] = f"{node.get_abs_path()}"
            df["name 1"] = f"{node.name}"
            df["path 2"] = f"{node_child.get_abs_path()}"
            df["name 2"] = f"{node_child.name}"
            df["q1"] = config_parent["qx0"]
            df["q2"] = config_parent["qy0"]
            df["nb"] = node.parameters["beam_npart"]
            df["oct_current"] = node.parameters["oct_current"]
            df["on_x1"] = node.parameters["knob_settings"]["on_x1"]
            try:
                df["bunch_nb"] = node.parameters["beambeam_config"]["bunch_to_track"]
            except:
                df["bunch_nb"] = config_parent["beambeam_config"]["bunch_to_track"]
            df = pd.merge(df, particle, on=["particle_id"])
            my_list.append(df)
        except Exception as e:
            problematic.append(node_child.get_abs_path())

my_df = pd.concat(my_list)
aux = my_df[my_df["state"] != 1]  # unstable
# df_for_evolution = aux.copy()
print(
    pd.DataFrame(
        [
            aux.groupby("name 1")["normalized amplitude in xy-plane"].min(),
            aux.groupby("name 1")["q1"].mean(),
            aux.groupby("name 1")["q2"].mean(),
        ]
    ).transpose()
)
my_final = pd.DataFrame(
    [
        aux.groupby("name 1")["normalized amplitude in xy-plane"].min(),
        aux.groupby("name 1")["q1"].mean(),
        aux.groupby("name 1")["q2"].mean(),
        aux.groupby("name 1")["nb"].mean(),
        aux.groupby("name 1")["on_x1"].mean(),
        aux.groupby("name 1")["oct_current"].mean(),
        aux.groupby("name 1")["bunch_nb"].mean(),
    ]
).transpose()
my_final.to_parquet(f"{my_study}/da.parquet")
# df_for_evolution.to_parquet(f"{my_study}/da_evolution.parquet")

end = time.time()
print(end - start)
