#!/bin/bash
source /afs/cern.ch/work/c/cdroin/private/DA_study_for_bologna_cluster/miniconda/bin/activate
cd /afs/cern.ch/work/c/cdroin/private/DA_study_for_bologna_cluster/opt_flathv_75_1500_withBB_1p4_survival_chromas_debug/madx_000/xsuite_068
python 000_track.py > output.txt 2> error.txt
rm -rf final_* modules optics_repository optics_toolkit tools tracking_tools temp mad_collider.log __pycache__ twiss* errors fc* optics_orbit_at*
