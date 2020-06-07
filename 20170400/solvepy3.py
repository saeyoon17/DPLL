import sys
from dpll import DPLL
target_file = sys.argv[1]

dpll_solver = DPLL(target_file)

(s, v) = dpll_solver.dpll()

print("s " + s)
