#!/bin/bash
cd /home/liuming/Projects/BioEarth/VIC-CropSyst/Simulation/Scenarios/Liu_Linux_308186_rot_4001
declare -a arr=("DEFAULT_CENTER_PIVOT" "DEFAULT_BIG_GUN" "DEFAULT_SOLID_SET" "DEFAULT_MOVING_WHEEL" "DEFAULT_DRIP" "DEFAULT_FLOOD" "DEFAULT_RILL" "DEFAULT_FURROW" "IrrigTP_CP_impact_14VH_RainBird" "IrrigTP_CP_impact_M20VH_PM_RainBird" "IrrigTP_CP_impact_65PJ_RainBird" "IrrigTP_CP_impact_30FH_30FWH_RainBird" "IrrigTP_CP_impact_L36H_L36AH_RainBird_1" "IrrigTP_CP_impact_L36H_L36AH_RainBird_2" "IrrigTP_CP_impact_85EHD_RainBird_1" "IrrigTP_CP_impact_85EHD_RainBird_2" "IrrigTP_CP_impact_85EHD_RainBird_3" "IrrigTP_CP_impact_85EHD_LA_RainBird_1" "IrrigTP_CP_impact_85EHD_LA_RainBird_2" "IrrigTP_CP_impact_85EHD_LA_RainBird_3" "IrrigTP_CP_spray_S3000_Nelson" "IrrigTP_CP_spray_O3000_Nelson" "IrrigTP_CP_spray_R3000_Nelson_1" "IrrigTP_CP_spray_R3000_Nelson_2" "IrrigTP_CP_spray_A3000_Nelson_1" "IrrigTP_CP_spray_A3000_Nelson_2" "IrrigTP_Big_Gun_75TR_Nelson_1" "IrrigTP_Big_Gun_75TR_Nelson_2" "IrrigTP_Big_Gun_75TR_Nelson_3" "IrrigTP_Big_Gun_150TB_Nelson_1" "IrrigTP_Big_Gun_150TB_Nelson_2" "IrrigTP_Big_Gun_150TB_Nelson_3" "IrrigTP_Big_Gun_200TB_Nelson_1" "IrrigTP_Big_Gun_200TB_Nelson_2" "IrrigTP_Big_Gun_200TB_Nelson_3" "IrrigTP_Solid_set_R5_POP_UP_Nelson" "IrrigTP_Solid_set_R2000WF_6_Nelson_1" "IrrigTP_Solid_set_R2000WF_6_Nelson_2" "IrrigTP_Solid_set_R2000WF_6_Nelson_3" "IrrigTP_Solid_set_R33_Nelson" "IrrigTP_Moving_wheel_R2000WF_6_Nelson_1" "IrrigTP_Moving_wheel_R2000WF_6_Nelson_2" "IrrigTP_Moving_wheel_R2000WF_6_Nelson_3" "IrrigTP_drip_0_0" "IrrigTP_Sub_surf_drip_0_0" "IrrigTP_flood_0_0" "IrrigTP_rill_0_0" "IrrigTP_furrow_0_0");
#declare -a arr=("DEFAULT_CENTER_PIVOT");
for i in "${arr[@]}"
do
   echo "$i"
   cp /home/liuming/Projects/BioEarth/VIC-CropSyst/Simulation/Database/Management/irrigation_308186_replace_mode.txt /home/liuming/Projects/BioEarth/VIC-CropSyst/Simulation/Database/Management/irrigation_308186_test.txt
   replacestring='s/REPLACE_THIS_WITH_REAL_IRRIGATION_TYPE/'${i}'/g'
   sed -i ${replacestring} /home/liuming/Projects/BioEarth/VIC-CropSyst/Simulation/Database/Management/irrigation_308186_test.txt
   #echo ${replacestring}
   
   cp vic_control_replace_mode.txt vic_control.txt
   replacestring='s/REPLACE_THIS_WITH_REAL_CROP_OUTPUT/'CROP_''${i}'/g'
   sed -i ${replacestring} vic_control.txt
   replacestring='s/REPLACE_WITH_REAL_FLUX_OUTPUT_PREFIX/'VICFLUX_''${i}'/g'
   sed -i ${replacestring} vic_control.txt

   /home/liuming/dev/VIC_CropSyst/build/Qt/Linux_gcc/Debug/VIC_CropSyst -g vic_control.txt
done
