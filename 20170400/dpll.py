from formula_gen import Formula_Gen
from formula import Formula


class DPLL():
    def __init__(self, target_file):
        self.target_file = target_file

    def dpll(self):
        temp = Formula_Gen(self.target_file)
        temp.gen_formula()
        temp.make_variables()
        temp.make_clauses()
        temp_formula = Formula(temp.formula_str, temp.var_lst, temp.clause_lst)

        while(True):
            # Real DPLL phase
            # While there is a unit clause {L} in F|A, add L -> 1 to A.
            temp_formula.unit_propagation()

            # If F |A contains no clauses, stop & output A.
            if(temp_formula.valuation() == True):
                return ("SATISFIABLE", temp.var_lst)

            elif(temp_formula.valuation() == False):
                learned_clause = temp_formula.learning_procedure()
                if len(learned_clause.clause) == 0:
                    return ("UNSATISFIABLE", temp.var_lst)

                temp_formula.clause_lst.append(learned_clause)
                temp_formula.formula_str.append(learned_clause.clause)

                # Backtrack to the position where learned clause is a unit clause

                temp_formula.backtrack(learned_clause)

            else:
                temp_formula.decision()
