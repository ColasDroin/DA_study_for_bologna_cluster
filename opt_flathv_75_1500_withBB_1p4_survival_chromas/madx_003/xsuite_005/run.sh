#!/bin/bash
source /gpfs/gpfs/gpfs_maestro_home_new/hpc/cdroin/DA_study/miniconda/bin/activate
cd /gpfs/gpfs/gpfs_maestro_home_new/hpc/cdroin/DA_study/opt_flathv_75_1500_withBB_1p4_survival_chromas/madx_003/xsuite_005
python 000_track.py > output.txt 2> error.txt
rm -rf final_* modules optics_repository optics_toolkit tools tracking_tools temp mad_collider.log __pycache__ twiss* errors fc* optics_orbit_at*
