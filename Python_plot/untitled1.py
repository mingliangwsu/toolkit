from pyDOE import *
filename = "/home/liuming/mnt/hydronas1/Projects/ForJon/climate_sequence.csv"

start_sim_year = 2075
last_sim_year = 2614
first = 2060
last = 2090

t = lhs(1, (last_sim_year - start_sim_year + 1))

index = 0
with open(filename,"w") as f:
    for y in t:
        f.write(str(index + start_sim_year) + "," + str(first + int((last - first) * y + 0.5)) + "\n")
        index += 1