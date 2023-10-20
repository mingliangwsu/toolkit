#!/bin/bash
mywkdir="$PWD"
cd ${veg_default_path}
cal_veg=$1 #evergreen
if [ "$cal_veg" = "1" ]; then
    source_default=${veg_default_path}/defs/stratum_evergreen_mode.def
    target_default=${veg_default_path}/defs/stratum_evergreen.def
elif [ "$cal_veg" = "2" ]; then
    source_default=${veg_default_path}/defs/stratum_deciduous_mode.def
    target_default=${veg_default_path}/defs/stratum_deciduous.def
elif [ "$cal_veg" = "5" ]; then
    source_default=${veg_default_path}/defs/stratum_shrub_mode.def
    target_default=${veg_default_path}/defs/stratum_shrub.def
fi


declare -a CAL
for cidx in 0 1 2 3 4 5;do
    value_index=$((cidx + 2))
    CAL[${cidx}]=${cidx}
done


cp $source_default $target_default
sed -i "s/CAL0/${CAL[0]}/g" $target_default
sed -i "s/CAL1/${CAL[1]}/g" $target_default
sed -i "s/CAL2/${CAL[2]}/g" $target_default
sed -i "s/CAL3/${CAL[3]}/g" $target_default
sed -i "s/CAL4/${CAL[4]}/g" $target_default
sed -i "s/CAL5/${CAL[5]}/g" $target_default
    
    #run RHESSys
cd ${mywkdir}
