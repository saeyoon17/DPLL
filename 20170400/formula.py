import random
from building_block import Clause


class Formula():
    def __init__(self, formula_str, var_lst, clause_lst):
        self.formula_str = formula_str
        self.var_lst = var_lst
        self.clause_lst = clause_lst
        self.assignment = []

    # return True if valuation under assignment var_lst is True
    # return False if valuation under assignment var_lst is False
    # return Formula if undetermined
    def valuation(self):
        value = None
        unassigned_clauses = []

        for i in range(len(self.formula_str)):
            clause_result = self.clause_lst[i].valuation(self.var_lst)
            if clause_result == False:
                value = False
            elif clause_result == True:
                continue
            else:
                unassigned_clauses.append([clause_result, i])

        if(value == False):
            return value
        else:
            if(len(unassigned_clauses) == 0):
                return True
            else:
                return unassigned_clauses

    # Check whether there is unit clause in the formula.
    # If there is a unit clause, assign value True to the variable
    # Returns true if there is a unit clause that we handled
    def check_unit_clause(self):
        for i in range(len(self.clause_lst)):
            clause_result = self.clause_lst[i].valuation(self.var_lst)
            if(not isinstance(clause_result, bool)):
                if len(clause_result) == 1:
                    target_variable = int(clause_result[0])
                    # Positive Literal
                    if(target_variable > 0):
                        self.var_lst[target_variable-1].value = True
                        # [decision, assigned variable, value, index of clause? -> this may only exist for implied variable]
                        self.assignment.append(
                            ["implied", str(target_variable), True, i])
                    else:
                        self.var_lst[abs(target_variable)-1].value = False
                        self.assignment.append(
                            ["implied", str(abs(target_variable)), False, i])
                    return True
        return False

    def unit_propagation(self):
        i = 0
        while(True):
            check_flag = self.check_unit_clause()
            if(check_flag == False):
                break
            i += 1

    def learning_procedure(self):
        assert self.valuation() == False
        target_clause = None
        for i in range(len(self.clause_lst)):
            temp = self.clause_lst[i]
            if(temp.valuation(self.var_lst) == False):

                # make a new instance with the same information
                target_clause = Clause(len(self.clause_lst), temp.clause)
                break
        # target_clause: clause that is failing according to current assignment
        assert target_clause != None
        self.assignment.reverse()

        for i, target_assignment in enumerate(self.assignment):

            clause_for_checking = []
            for j in range(len(target_clause.clause)):
                if(int(target_clause.clause[j]) < 0):
                    clause_for_checking.append(target_clause.clause[j][1:])
                else:
                    clause_for_checking.append(target_clause.clause[j])

            if((target_assignment[0] == "decision") or (target_assignment[1] not in clause_for_checking)):
                continue

            elif((target_assignment[0] == "implied") and (target_assignment[1] in clause_for_checking)):
                target_clause.clause = self.resolution(
                    self.clause_lst[target_assignment[3]], target_clause, target_assignment[1])

        self.assignment.reverse()
        return target_clause

    def resolution(self, clause1, clause2, target_var):
        new_clause1 = []
        for i in range(len(clause1.clause)):
            clause_var = clause1.clause[i]
            if abs(int(clause_var)) != int(target_var):
                new_clause1.append(clause_var)

        new_clause2 = []
        for i in range(len(clause2.clause)):
            clause_var = clause2.clause[i]
            if abs(int(clause_var)) != int(target_var):
                new_clause2.append(clause_var)

        resolvent = list(dict.fromkeys(new_clause1 + new_clause2))
        return resolvent

    def backtrack(self, learned_clause):
        valuated = learned_clause.valuation(self.var_lst)
        while(isinstance(valuated, bool)):
            # assignement가 비어있을 경우도 고려해야함
            decision, target_var, var_value, clause_idx = self.assignment[-1]
            del self.assignment[-1]
            self.var_lst[int(target_var)-1].value = None

            valuated = learned_clause.valuation(self.var_lst)

        return

    def decision(self):
        i = 0
        temp = random.choice(self.var_lst)
        while(i < len(self.var_lst)):
            temp = random.choice(self.var_lst)
            if(temp.value == None):
                new_value = bool(random.getrandbits(1))
                temp.value = new_value
                self.assignment.append(
                    ["decision", temp.name, new_value, None])
                break
            i = i + 1
