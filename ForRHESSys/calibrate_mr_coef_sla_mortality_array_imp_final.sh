#!/bin/bash
RHESSys="/home/liuming/RHESSys_Ning/RHESSys/build/Qt/gcc/build-RHESSys-Generic_Linux-Debug/RHESSys"
#py_likelyhood="/home/liuming/dev/toolkit/ForRHESSys/growth_yearly_model_performance.py"
py_likelyhood="/home/liuming/dev/toolkit/ForRHESSys/growth_yearly_model_performance_nppratio_height_npp_LAI.py"
droot="/home/liuming/mnt/hydronas2/Projects/FireEarth/Cedar"

source_default=${droot}/stratum_evergreen_mode.def
target_default=${droot}/stratum_evergreen.def

outpfile=${droot}/Outputs/mrcoef_likelihood_mcmc.txt

debug_file=${droot}/echo_test_likelihood.txt

echo "idx cal0 cal1 cal2 likelyhood" > $outpfile

growth_year=${droot}/Outputs/spinup_fire__grow_stratum.yearly
distfile=${droot}/Outputs/dist_npp_gpp_ratio.txt
tempGaussRandom=${droot}/Outputs/testGauseRandom.txt
valid_start_year=1990
valid_end_year=2015
valid_veg_id=1

#target0: npp/gpp ratio
#target1: height (m)
#target2: npp (kgC/m2/year)
#target3: LAI (m2/m2）
declare -a target
declare -a target_stddev
target[0]=0.5
target_stddev[0]=0.051
target[1]=39
target_stddev[1]=`echo "scale=6; 0.3*${target[1]}" | bc`
target[2]=1.4
target_stddev[2]=`echo "scale=6; 0.3*${target[2]}" | bc`
#from MODIS (5%), then double it
#target_stddev[2]=`echo "scale=6; 0.1*${target[2]}" | bc`
target[3]=9.0
target_stddev[3]=`echo "scale=6; 0.3*${target[3]}" | bc`



#1.8-2.2
#CALq10=1.9
#0.1-0.5
#CALper_N=0.25
echo "New" > ${droot}/echo_test_likelihood.txt
#CAL0 mrc.per_N
#CAL1 epc.proj_sla
#CAL2 epc.max_daily_mortality

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
min_c[0]=0.06
max_c[0]=0.14
min_c[1]=3
max_c[1]=20
min_c[2]=0.005
max_c[2]=0.02

declare -a CAL
declare -a dtrange
for cidx in 0 1 2;do
    test=$(shuf -i0-100 -n1)
    min=${min_c[$cidx]}
    max=${max_c[$cidx]}
    CAL[${cidx}]=`echo "scale=6; $test*0.01*(${max}-${min})+${min}" | bc`
    dtrange[${cidx}]=`echo "scale=6; 0.05*(${max}-${min})" | bc` 
    echo cidx:$cidx min:${min} max:${max}
done

declare -a old_CAL
declare -a dt
idx=1
#while [ $idx -le 200 ]
while [ $idx -le 2000 ]
do
    #echo $idx $CALq10 $CALper_N
    
    cp $source_default $target_default
    sed -i "s/CAL0/${CAL[0]}/g" $target_default
    sed -i "s/CAL1/${CAL[1]}/g" $target_default
    sed -i "s/CAL2/${CAL[2]}/g" $target_default
    
    #run RHESSys
    ${RHESSys} -netcdfgrid -ncgridinterp 10 -t calibration.tec -w world_file_patchID_100951_100952.txt -whdr  defFiles.hdr  -st 1979 01 01 01 -ed 2015 12 31 24 -pre ./Outputs/spinup_fire_ -s 5.200298 54.26672 -sv 5.200298 54.26672 -svalt 1.143066 3.829007 -gw 0.604857 0.3806356 -r flowtable_100951_100952.txt -b -g -p -c -h -z -firespread 100 patchGrid.txt DemGrid.txt -firemort 0.71 -9999  -9999 0.52 4.05 -10 1 -firespin 10 50
    
    #-firespin 10 50
    #cal likelihood (squre dist)
    python ${py_likelyhood} ${growth_year} ${valid_start_year} ${valid_end_year} ${valid_veg_id} ${target[0]} ${target_stddev[0]} ${target[1]} ${target_stddev[1]} ${target[2]} ${target_stddev[2]} ${target[3]} ${target_stddev[3]} ${distfile}

    likelihood=$(head -n 1 ${distfile})
    if [ $idx -eq 1 ]; then
        old_likelihood=${likelihood}
        #tv=`echo "scale=4;$idx $CALq10 $CALper_N ${likelihood}" | bc -l`
        printf "%d %.4f %.4f %.4f %.4f\n" $idx ${CAL[0]} ${CAL[1]} ${CAL[2]} ${likelihood} >> $outpfile
        update=1
        for cidx in 0 1 2;do
            old_CAL[$cidx]=${CAL[$cidx]}
        done
    else
        beta=`echo "scale=6; ${likelihood}/${old_likelihood}" | bc`
        u=$(shuf -i0-100 -n1)
        ru=`echo "scale=6; ${u}*0.01" | bc`
        echo idx:$idx beta:${beta} ru:${ru} perf:${likelihood} old_perf:${old_likelihood} cal0:${CAL[0]} cal1:${CAL[1]} cal2:${CAL[2]} >> $debug_file
        if (( $(echo "${ru} <= ${beta}" | bc -l) ))
        then
            #accept
            update=1
            echo accept! >> $debug_file
            printf "%d %.4f %.4f %.4f %.8f\n" $idx ${CAL[0]} ${CAL[1]} ${CAL[2]} ${likelihood} >> $outpfile
            old_likelihood=${likelihood}
            for cidx in 0 1 2;do
                old_CAL[$cidx]=${CAL[$cidx]}
            done
        else
            #not accept
            echo not accept! >> $debug_file
            #CAL0=${old_CAL0}
            #CAL1=${old_CAL1}
            #CAL1=${old_CAL2}
        fi
    fi
    
    #old_CAL0=${CAL0}
    #old_CAL1=${CAL1}
    #old_CAL2=${CAL2}

    #generate proposal
    for cidx in 0 1 2;do
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
    
    echo idx:$idx old_cal0:${old_CAL[0]} proposed_cal0:${CAL[0]} dt0:${dt[0]} old_cal1:${old_CAL[1]} proposed_cal1:${CAL[1]} dt1:${dt[1]} old_cal2:${old_CAL[2]} proposed_cal2:${CAL[2]} dt2:${dt[2]} >> $debug_file
    
    idx=$(( $idx + 1 ))
done
