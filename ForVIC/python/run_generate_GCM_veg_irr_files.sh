#!/bin/bash

orig_veg="/home/liuming/mnt/hydronas1/Projects/Forecast2020/irrigation/pnw_veg_parameter_filledzero.txt"
orig_irr="/home/liuming/mnt/hydronas1/Projects/Forecast2020/irrigation/pnw_irrigation.txt"
data_path="/home/liuming/mnt/hydronas1/Projects/Forecast2020/GCAM_scenario_land_use_newCropSyst_20200525"
outpath="/home/liuming/mnt/hydronas1/Projects/Forecast2020/GCAM_scenario_land_use_newCropSyst_20200525/VIC_CropSyst"
pyscript="/home/liuming/dev/toolkit/ForVIC/python/generate_cropirrigation_parameter_from_original_veg_irigation_parameter_and_updated_fraction_GCM.py"

declare -a scenarios=("baseline" "RCP_4.5_expanded" "RCP_4.5_max_expansion" "RCP_4.5_no_expansion" "RCP_8.5_expanded" "RCP_8.5_max_expansion" "RCP_8.5_no_expansion")
#declare -a scenarios=("1" "2")
echo ${scenarios}

for scenario in "${scenarios[@]}"
do
    echo ${scenario}
    newfraction=${data_path}/GCAMLU_${scenario}.csv
    out_veg=${outpath}/GCAMLU_${scenario}_veg_parameter.txt
    out_irr=${outpath}/GCAMLU_${scenario}_irrigation.txt
    python ${pyscript} ${newfraction} ${orig_veg} ${orig_irr} ${out_veg} ${out_irr}
done