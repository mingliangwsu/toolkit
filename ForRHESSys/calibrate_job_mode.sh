#!/bin/bash

#pass arguments: $1: veg type  $2: cover_fraction $3: patchID $4:npp/gpp ratio $5:height $6:npp $7:LAI $8: AGBc
#$9:cal0_min $10:cal0_max $11:cal1_min $12:cal1_max $13:cal2_min $14:cal2_max $15:cal3_min $16:cal3_max

#RHESSys="/home/liuming/RHESSys_Ning/RHESSys/build/Qt/gcc/Release/RHESSys"
#py_likelyhood="/home/liuming/dev/toolkit/ForRHESSys/growth_yearly_model_performance_nppratio_height_npp_LAI_AGBc.py"
#droot="/home/liuming/mnt/hydronas2/Projects/FireEarth/Cedar"
#patch_stata_veg="${droot}/patch_stratum_vegid.txt"

mywkdir="$PWD"
cd ${droot}

cal_veg=$1 #evergreen
cal_veg_coverfraction=$2
cal_patch=$3

flowtable=patch_${cal_patch}.flow
worldfile=patch_${cal_patch}.state





if [ "$cal_veg" = "1" ]; then
    source_default=${droot}/defs/stratum_evergreen_mode.def
    target_default=${droot}/defs/stratum_evergreen.def
elif [ "$cal_veg" = "2" ]; then
    source_default=${droot}/defs/stratum_deciduous_mode.def
    target_default=${droot}/defs/stratum_deciduous.def
elif [ "$cal_veg" = "5" ]; then
    source_default=${droot}/defs/stratum_shrub_mode.def
    target_default=${droot}/defs/stratum_shrub.def
fi

outputdir=${outputdir_root}/patch${cal_patch}
if [ ! -d "$outputdir" ]; then
    mkdir -p $outputdir 
fi

outpfile=${outputdir}/mrcoef_likelihood_mcmc.txt
debug_file=${outputdir}/echo_test_likelihood.txt

echo "idx cal0 cal1 cal2 cal3 cal4 cal5 likelyhood" > $outpfile

growth_year=${outputdir}/calib_grow_stratum.yearly
distfile=${outputdir}/dist_npp_gpp_ratio.txt
logfile=${outputdir}/pylog.txt
tempGaussRandom=${outputdir}/testGauseRandom.txt
valid_veg_id=${cal_veg}

#CAL0 mrc.per_N
#CAL1 epc.proj_sla
#CAL2 epc.max_daily_mortality
#CAL3 epc.dickenson_pa
#CAL4 epc.height_to_stem_exp
#CAL5 epc.height_to_stem_coef

#target0: npp/gpp ratio
#target1: height (m)
#target2: npp (kgC/m2/year)
#target3: LAI (m2/m2）
#target4: AGBc (kgC/m2）

declare -a target
declare -a target_stddev
target[0]=$4
target_stddev[0]=0.051
target[1]=$5
target_stddev[1]=`echo "scale=6; 0.3*${target[1]}" | bc`
nppveg=$6
#target[2]=$((nppveg+cal_veg_coverfraction))
target[2]=`echo "scale=6; ${nppveg}/${cal_veg_coverfraction}" | bc`
echo target2:${target[2]}

target_stddev[2]=`echo "scale=6; 0.3*${target[2]}" | bc`
#from MODIS (5%), then double it
#target_stddev[2]=`echo "scale=6; 0.1*${target[2]}" | bc`
laiveg=$7
#target[3]=$((laiveg/cal_veg_coverfraction))
target[3]=`echo "scale=6; ${laiveg}/${cal_veg_coverfraction}" | bc`
target_stddev[3]=`echo "scale=6; 0.3*${target[3]}" | bc`
target[4]=`echo "scale=6; ${8}/${cal_veg_coverfraction}" | bc`
target_stddev[4]=`echo "scale=6; 0.3*${target[4]}" | bc`

#read -p 'Press [Enter] key to continue...'

#1.8-2.2
#CALq10=1.9
#0.1-0.5
#CALper_N=0.25
echo "New" > ${droot}/echo_test_likelihood.txt


#first try
#min_c0=0.05
#max_c0=0.25
#min_c1=10
#max_c1=30
#min_c2=0.001
#max_c2=0.02

#second try
declare -a min_c
declare -a max_c
min_c[0]=${9}    #0.1
max_c[0]=${10}    #0.25
min_c[1]=${11}    #12
max_c[1]=${12}    #50
min_c[2]=${13}    #0.005
max_c[2]=${14}    #0.10
min_c[3]=${15}    #0.4
max_c[3]=${16}    #0.8
min_c[4]=${17}    #0.4
max_c[4]=${18}    #0.8
min_c[5]=${19}    #0.4
max_c[5]=${20}    #0.8

declare -a CAL
declare -a dtrange
for cidx in 0 1 2 3 4 5;do
    test=$(shuf -i0-100 -n1)
    min=${min_c[$cidx]}
    max=${max_c[$cidx]}
    CAL[${cidx}]=`echo "scale=6; $test*0.01*(${max}-${min})+${min}" | bc`
    dtrange[${cidx}]=`echo "scale=6; 0.05*(${max}-${min})" | bc` 
    echo cidx:$cidx min:${min} max:${max}
done

output_pre=${outputdir}/init_soil
#Step one: initialize the soil (C & N)

echo "${RHESSys} -netcdfgrid -ncgridinterp 10 -t ${tecfile} -w ${worldfile} -whdr ${headfile} -start_from_zero_soilpools -st ${startyear} 01 01 01 -ed ${endyear} 12 31 24 -pre ${output_pre} -s ${s1} ${s2} -sv ${s1} ${s2} -svalt ${po} ${pa} -gw ${gw1} ${gw2} -r ${flowtable} -g -b -p -c -firespread 100 ${patchgrid} ${demgrid} -Ndecayrate 3.0 -firespin ${spyrs} ${soil_spins} 
newworldfile=${worldfile}.Y${stateyear}M1D1H1.state"
${RHESSys} -netcdfgrid -ncgridinterp 10 -t ${tecfile} -w ${worldfile} -whdr ${headfile} -start_from_zero_soilpools -st ${startyear} 01 01 01 -ed ${endyear} 12 31 24 -pre ${output_pre} -s ${s1} ${s2} -sv ${s1} ${s2} -svalt ${po} ${pa} -gw ${gw1} ${gw2} -r ${flowtable} -g -b -p -c -firespread 100 ${patchgrid} ${demgrid} -Ndecayrate 3.0 -firespin ${spyrs} ${soil_spins} 

newworldfile=${worldfile}.Y${stateyear}M1D1H1.state
worldfile=${newworldfile}

#Step two: init veg -
output_pre=${outputdir}/init_veg

echo "${RHESSys} -netcdfgrid -ncgridinterp 10 -t ${tecfile} -w ${worldfile} -whdr ${headfile} -start_from_zero_vegpools -st ${startyear} 01 01 01 -ed ${endyear} 12 31 24 -pre ${output_pre} -s ${s1} ${s2} -sv ${s1} ${s2} -svalt ${po} ${pa} -gw ${gw1} ${gw2} -r ${flowtable} -g -b -p -c -firespread 100 ${patchgrid} ${demgrid} -Ndecayrate 3.0 -firespin ${spyrs} ${veg_spins} 
newworldfile=${worldfile}.Y${stateyear}M1D1H1.state"
${RHESSys} -netcdfgrid -ncgridinterp 10 -t ${tecfile} -w ${worldfile} -whdr ${headfile} -start_from_zero_vegpools -st ${startyear} 01 01 01 -ed ${endyear} 12 31 24 -pre ${output_pre} -s ${s1} ${s2} -sv ${s1} ${s2} -svalt ${po} ${pa} -gw ${gw1} ${gw2} -r ${flowtable} -g -b -p -c -firespread 100 ${patchgrid} ${demgrid} -Ndecayrate 3.0 -firespin ${spyrs} ${veg_spins} 

newworldfile=${worldfile}.Y${stateyear}M1D1H1.state
worldfile=${newworldfile}

output_pre=${outputdir}/calib

declare -a old_CAL
declare -a dt
idx=1
#while [ $idx -le 20 ]
while [ $idx -le ${loops} ]
do
    #echo $idx $CALq10 $CALper_N
    
    cp $source_default $target_default
    sed -i "s/CAL0/${CAL[0]}/g" $target_default
    sed -i "s/CAL1/${CAL[1]}/g" $target_default
    sed -i "s/CAL2/${CAL[2]}/g" $target_default
    sed -i "s/CAL3/${CAL[3]}/g" $target_default
    sed -i "s/CAL4/${CAL[4]}/g" $target_default
    sed -i "s/CAL5/${CAL[5]}/g" $target_default
    
    #run RHESSys




    echo "${RHESSys} -netcdfgrid -ncgridinterp 10 -t ${tecfile} -w ${worldfile} -whdr ${headfile} -start_from_zero_vegpools -st ${startyear} 01 01 01 -ed ${endyear} 12 31 24 -pre ${output_pre} -s ${s1} ${s2} -sv ${s1} ${s2} -svalt ${po} ${pa} -gw ${gw1} ${gw2} -r ${flowtable} -g -b -p -c -firespread 100 ${patchgrid} ${demgrid} -Ndecayrate 3.0 -firespin ${spyrs} ${veg_spins}"
    ${RHESSys} -netcdfgrid -ncgridinterp 10 -t ${tecfile} -w ${worldfile} -whdr ${headfile} -start_from_zero_vegpools -st ${startyear} 01 01 01 -ed ${endyear} 12 31 24 -pre ${output_pre} -s ${s1} ${s2} -sv ${s1} ${s2} -svalt ${po} ${pa} -gw ${gw1} ${gw2} -r ${flowtable} -g -b -p -c -firespread 100 ${patchgrid} ${demgrid} -Ndecayrate 3.0 -firespin ${spyrs} ${veg_spins} 

  
    #-firespin 10 50
    #cal likelihood (squre dist)
    echo "python ${py_likelyhood} ${growth_year} ${valid_start_year} ${valid_end_year} ${valid_veg_id} ${patch_stata_veg} ${target[0]} ${target_stddev[0]} ${target[1]} ${target_stddev[1]} ${target[2]} ${target_stddev[2]} ${target[3]} ${target_stddev[3]} ${target[4]} ${target_stddev[4]} ${distfile} ${logfile}"
    #read -p 'Press [Enter] key to continue...'
    printf "%d %.4f %.4f %.4f %.4f %.4f %.4f %.4e\n" $idx ${CAL[0]} ${CAL[1]} ${CAL[2]} ${CAL[3]} ${CAL[4]} ${CAL[5]} ${likelihood} >> $logfile
    python ${py_likelyhood} ${growth_year} ${valid_start_year} ${valid_end_year} ${valid_veg_id} ${patch_stata_veg} ${target[0]} ${target_stddev[0]} ${target[1]} ${target_stddev[1]} ${target[2]} ${target_stddev[2]} ${target[3]} ${target_stddev[3]} ${target[4]} ${target_stddev[4]} ${distfile} ${logfile}

    likelihood=$(head -n 1 ${distfile})
    if [ $idx -eq 1 ]; then
        old_likelihood=${likelihood}
        #tv=`echo "scale=4;$idx $CALq10 $CALper_N ${likelihood}" | bc -l`
        printf "%d %.4f %.4f %.4f %.4f %.4f %.4f %.4e\n" $idx ${CAL[0]} ${CAL[1]} ${CAL[2]} ${CAL[3]} ${CAL[4]} ${CAL[5]} ${likelihood} >> $outpfile
        update=1
        for cidx in 0 1 2 3 4 5;do
            old_CAL[$cidx]=${CAL[$cidx]}
        done
    else
        #beta=`echo "scale=6; ${likelihood}/${old_likelihood}" | bc`
        beta=`ps -ef | awk -v a=${likelihood} -v b=${old_likelihood} 'BEGIN{print (a / b)}'`
        u=$(shuf -i0-100 -n1)
        ru=`echo "scale=6; ${u}*0.01" | bc`
        echo idx:$idx beta:${beta} ru:${ru} perf:${likelihood} old_perf:${old_likelihood} cal0:${CAL[0]} cal1:${CAL[1]} cal2:${CAL[2]} cal3:${CAL[3]} cal4:${CAL[4]} cal5:${CAL[5]} >> $debug_file
        if (( $(echo "${ru} <= ${beta}" | bc -l) ))
        then
            #accept
            update=1
            echo accept! >> $debug_file
            printf "%d %.4f %.4f %.4f %.4f %.4f %.4f %.4e\n" $idx ${CAL[0]} ${CAL[1]} ${CAL[2]} ${CAL[3]} ${CAL[4]} ${CAL[5]} ${likelihood} >> $outpfile
            old_likelihood=${likelihood}
            for cidx in 0 1 2 3 4 5;do
                old_CAL[$cidx]=${CAL[$cidx]}
            done
        else
            #not accept
            echo not accept! >> $debug_file
            echo not accept! >> ${logfile}
            #CAL0=${old_CAL0}
            #CAL1=${old_CAL1}
            #CAL1=${old_CAL2}
        fi
    fi
    
    #old_CAL0=${CAL0}
    #old_CAL1=${CAL1}
    #old_CAL2=${CAL2}

    #generate proposal
    for cidx in 0 1 2 3 4 5;do
        python /home/liuming/dev/toolkit/ForRHESSys/generate_gauss_random.py 0 ${dtrange[${cidx}]} $tempGaussRandom
        dt[${cidx}]=$(head -n 1 ${tempGaussRandom})
        ldt=${dt[${cidx}]}
        orig=${old_CAL[${cidx}]}
        CAL[${cidx}]=`echo "scale=6; ${orig}+${ldt}" | bc -l`
        min=${min_c[${cidx}]}
        max=${max_c[${cidx}]}
        current=${CAL[${cidx}]}
        if (( $(echo "${current} > ${max}" | bc -l) )); then
            CAL[${cidx}]=${max}
        else
            if (( $(echo "${current} < ${min}" | bc -l) )); then
                CAL[${cidx}]=${min}
            fi
        fi
    done
    
    echo idx:$idx old_cal0:${old_CAL[0]} proposed_cal0:${CAL[0]} dt0:${dt[0]} old_cal1:${old_CAL[1]} proposed_cal1:${CAL[1]} dt1:${dt[1]} old_cal2:${old_CAL[2]} proposed_cal2:${CAL[2]} dt2:${dt[2]} old_cal3:${old_CAL[3]} proposed_cal3:${CAL[3]} dt3:${dt[3]}  old_cal4:${old_CAL[4]} proposed_cal4:${CAL[4]} dt4:${dt[4]}  old_cal5:${old_CAL[5]} proposed_cal5:${CAL[5]} dt5:${dt[5]} >> $debug_file
    
    idx=$(( $idx + 1 ))
done

cd ${mywkdir}
