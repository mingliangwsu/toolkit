#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Nov 22 10:26:45 2022

@author: liuming
"""
import sys 


if len(sys.argv) <= 1:
    print("Usage:" + sys.argv[0] + "<1world_state_filename> <2out_subset> <3world_id> <4basin_ID> <5hillslope_ID> <6zone_ID> <7patch_ID> <8canopy_strata_ID>\n")
    sys.exit(0)

print(sys.argv[1])
