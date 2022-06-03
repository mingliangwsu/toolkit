#!/bin/bash
RHESSys="/home/liuming/RHESSys_Ning/RHESSys/build/Qt/gcc/build-RHESSys-Generic_Linux-Debug/RHESSys"
droot="/home/liuming/mnt/hydronas2/Projects/FireEarth/Cedar"
outpfile=${droot}/Outputs/mrcoef_likelihood_mcmc.txt

debug_file=${droot}/echo_test_likelihood.txt

echo "idx q10 per_N likelyhood" > $outpfile

growth_year=${droot}/Outputs/spinup_fire__grow_stratum.yearly
distfile=${droot}/Outputs/dist_npp_gpp_ratio.txt
tempGaussRandom=${droot}/Outputs/testGauseRandom.txt
valid_start_year=1990
valid_end_year=2018
valid_veg_id=1
target=0.5
target_stddev=0.051

source_default=${droot}/stratum_evergreen_mode.def
target_default=${droot}/stratum_evergreen.def

#1.8-2.2
#CALq10=1.9
#0.1-0.5
#CALper_N=0.25
echo "New" > ${droot}/echo_test_likelihood.txt

qrmin=1.7
qrmax=2.1

test=$(shuf -i0-100 -n1)
CALq10=`echo "scale=6; $test*0.01*($qrmax-$qrmin)+$qrmin" | bc`
dq10=`echo "scale=6; 0.05*($qrmax-$qrmin)" | bc` 

test2=$(shuf -i0-100 -n1)
nrmin=0.05
nrmax=0.25
CALper_N=`echo "scale=6; ${test2}*0.01*($nrmax-$nrmin)+$nrmin" | bc`
dn=`echo "scale=6; 0.05*($nrmax-$nrmin)" | bc` 

update=0

idx=1
while [ $idx -le 200 ]
do
    #echo $idx $CALq10 $CALper_N
    
    cp $source_default $target_default
    sed -i "s/CALq10/${CALq10}/g" $target_default
    sed -i "s/CALper_N/${CALper_N}/g" $target_default
    
    #run RHESSys
    ${RHESSys} -netcdfgrid -ncgridinterp 10 -t spinup_update_state.tec -w world_file_patchID_100951_100952.txt -whdr  defFiles.hdr  -st 1979 01 01 01 -ed 2018 12 31 24 -pre ./Outputs/spinup_fire_ -s 5.200298 54.26672 -sv 5.200298 54.26672 -svalt 1.143066 3.829007 -gw 0.604857 0.3806356 -r flowtable_100951_100952.txt -b -g -p -c -h -z -firespread 100 patchGrid.txt DemGrid.txt -firemort 0.71 -9999  -9999 0.52 4.05 -10 1 -firespin 5 1

    #cal likelihood (squre dist)
    python /home/liuming/dev/toolkit/ForRHESSys/growth_yearly_model_performance.py ${growth_year} ${valid_start_year} ${valid_end_year} ${valid_veg_id} ${target} ${target_stddev} ${distfile}

    likelihood=$(head -n 1 ${distfile})
    if [ $idx -eq 1 ]
    then
        old_likelihood=${likelihood}
        #tv=`echo "scale=4;$idx $CALq10 $CALper_N ${likelihood}" | bc -l`
        printf "%d %.4f %.4f %.4f\n" $idx ${CALq10} ${CALper_N} ${likelihood} >> $outpfile
        update=1
    else
        beta=`echo "scale=6; ${likelihood}/${old_likelihood}" | bc`
        u=$(shuf -i0-100 -n1)
        ru=`echo "scale=6; ${u}*0.01" | bc`
        echo idx:$idx beta:${beta} ru:${ru} perf:${likelihood} old_perf:${old_likelihood} q10:${CALq10} perN:${CALper_N} >> $debug_file
        if (( $(echo "${ru} <= ${beta}" | bc -l) ))
        then
            #accept
            update=1
            echo accept! >> $debug_file
            printf "%d %.4f %.4f %.4f\n" $idx ${CALq10} ${CALper_N} ${likelihood} >> $outpfile
            old_likelihood=${likelihood}
        else
            #not accept
            echo not accept! >> $debug_file
            CALq10=${old_q10}
            CALper_N=${old_pern}
        fi
    fi
    
    old_q10=${CALq10}
    old_pern=${CALper_N}

    #generate proposal
    python /home/liuming/dev/toolkit/ForRHESSys/generate_gauss_random.py 0 ${dq10} $tempGaussRandom
    dt=$(head -n 1 ${tempGaussRandom})
    CALq10=`echo "scale=6; $CALq10+$dt" | bc -l`
    if (( $(echo "${CALq10} > ${qrmax}" | bc -l) )); then
        CALq10=${qrmax}
    else
        if (( $(echo "${CALq10} < ${qrmin}" | bc -l) )); then
            CALq10=${qrmin}
        fi
    fi
    
    python /home/liuming/dev/toolkit/ForRHESSys/generate_gauss_random.py 0 ${dn} $tempGaussRandom
    dt=$(head -n 1 ${tempGaussRandom})
    CALper_N=`echo "scale=6; $CALper_N+$dt" | bc -l`
    if (( $(echo "${CALper_N} > ${nrmax}" | bc -l) )); then
        CALper_N=${nrmax}
    else
        if (( $(echo "${CALper_N} < ${nrmin}" | bc -l) )); then
            CALper_N=${nrmin}
        fi
    fi
    
    
    echo idx:$idx old_q10:${old_q10} proposed_q10:$CALq10 old_perN:${old_pern} proposed_perN:${CALper_N} >> $debug_file
    
    idx=$(( $idx + 1 ))
done
