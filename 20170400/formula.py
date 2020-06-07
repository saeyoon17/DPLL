import random
from building_block import Clause


class Formula():
    def __init__(self, formula_str, var_lst, clause_lst):
        self.formula_str = formula_str
        self.var_lst = var_lst
        self.clause_lst = clause_lst
        self.assignment = []

        decision_strategy = []
        for i in range(len(var_lst)):
            decision_strategy.append(0)

        self.decision_strategy = decision_strategy

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
            self.decision_strategy[int(target_var)-1
                                   ] = self.decision_strategy[int(target_var)-1] + 1
            del self.assignment[-1]
            self.var_lst[int(target_var)-1].value = None

            valuated = learned_clause.valuation(self.var_lst)

        return

    def decision_dlis(self):

        # DLIS Strategy
        current_state = self.valuation()

        # Find variable with the most positive literal
        max_cnt_cp_var = None
        max_cnt_cp = 0
        for i in range(len(self.var_lst)):
            target_var = int(self.var_lst[i].name)
            cnt = 0
            for j in range(len(current_state)):
                if target_var in current_state[j][0]:
                    cnt = cnt + 1
            if(cnt > max_cnt_cp):
                max_cnt_cp = cnt
                max_cnt_cp_var = self.var_lst[target_var-1]

        max_cnt_cn_var = None
        max_cnt_cn = 0
        for i in range(len(self.var_lst)):
            target_var = int(self.var_lst[i].name) * -1
            cnt = 0
            for j in range(len(current_state)):
                if target_var in current_state[j][0]:
                    cnt = cnt + 1
            if(cnt > max_cnt_cn):
                max_cnt_cn = cnt
                max_cnt_cn_var = self.var_lst[abs(target_var)-1]

        if(max_cnt_cp > max_cnt_cn):
            max_cnt_cp_var.value = True
            self.assignment.append(
                ["decision", max_cnt_cp_var.name, True, None])
        else:
            max_cnt_cn_var.value = False
            self.assignment.append(
                ["decision", max_cnt_cn_var.name, False, None])

    def decision_random(self):
        while(True):
            temp_var = random.choice(self.var_lst)
            if(temp_var.value == None):
                new_value = bool(random.getrandbits(1))
                temp_var.value = new_value
                self.assignment.append(
                    ["decision", temp_var.name, new_value, None])
                break

    def decision_proportional(self):
        # My strategy #1: Doing proportionally
        decision_lst = []
        flag = False
        for i in range(len(self.decision_strategy)):
            if(self.decision_strategy[i] == 0 or self.var_lst[i].value != None):
                decision_lst.append(0)
            else:
                decision_lst.append(1/self.decision_strategy[i])
                flag = True

        while(True):

            if(flag):
                temp = random.choices(
                    self.var_lst, weights=decision_lst, k=1)
                temp_var = temp[0]
            else:
                temp_var = random.choice(self.var_lst)

            if(temp_var.value == None):
                new_value = bool(random.getrandbits(1))
                temp_var.value = new_value
                self.assignment.append(
                    ["decision", temp_var.name, new_value, None])
                break
