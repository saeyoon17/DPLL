import sys
from dpll import DPLL
target_file = sys.argv[1]

dpll_solver = DPLL(target_file)

# Three modes.
# dlis
# prop
# random


(s, v) = dpll_solver.dpll("random")

print("s " + s)

if(s == "SATISFIABLE"):
    output_str = "v"

    for i in range(len(v)):
        if(v[i].value == True):
            output_str = output_str + " " + v[i].name

        elif(v[i].value == False):
            output_str = output_str + " " + "-" + v[i].name

        else:
            continue

        if(i == len(v) - 1):
            output_str = output_str + " 0"
            print(output_str)
        else:
            if(i % 5 == 4):
                print(output_str)
                output_str = "v"
