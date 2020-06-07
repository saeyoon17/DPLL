class Clause():
    def __init__(self, id, clause):
        self.id = id
        self.clause = clause

    def valuation(self, var_lst):
        value = None
        unassigned_vars = []
        for i in range(len(self.clause)):
            target_var = int(self.clause[i])
            var_instance = var_lst[abs(target_var) - 1]

            # check a variable instance
            if(var_instance.check_assigned()):
                var_instance_value = var_instance.value
                if(target_var > 0):
                    real_value = var_instance_value
                else:
                    real_value = not var_instance.value

                if(real_value == True):
                    value = True
            else:
                unassigned_vars.append(target_var)

        if(value == True):
            return value
        else:
            # there are no unassigned_vars, all of them are evaluated to False
            if(len(unassigned_vars) == 0):
                return False
            else:
                return unassigned_vars


class Var():
    def __init__(self, name):
        self.name = name
        self.value = None
        return

    def assign(self, value):
        self.value = value
        return

    def check_assigned(self):
        return self.value != None
