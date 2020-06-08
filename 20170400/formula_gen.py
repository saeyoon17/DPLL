from building_block import Clause, Var


class FormulaGen():
    def __init__(self, file):
        self.file = file
        self.num_clause = -1
        self.num_var = -1
        self.formula_str = None
        self.var_lst = []
        self.clause_lst = []

    def get_token(self, target_line):
        ret_str = ""
        for i in range(len(target_line)):
            if(target_line[i] == " "):
                return (ret_str, target_line[i:].strip())
            else:
                ret_str = ret_str + target_line[i]
        return ret_str, ""

    def get_num_clause_var(self, target_line):

        first_tok, rest = self.get_token(target_line)
        assert first_tok == "p"
        second_tok, rest = self.get_token(rest)
        assert second_tok == "cnf"

        num_var, rest = self.get_token(rest)
        num_clause, rest = self.get_token(rest)

        self.num_var = int(num_var)
        self.num_clause = int(num_clause)

    def gen_formula(self):
        with open(self.file, "r") as f:
            altogether = ""
            target_lines = f.readlines()
            formula_str = []
            clause = []

            for i in range(len(target_lines)):
                if(target_lines[i][0] == "c"):
                    continue
                elif(target_lines[i][0] == "p"):
                    self.get_num_clause_var(target_lines[i])
                else:
                    altogether = altogether + target_lines[i]
            altogether = altogether.replace("\n", " ")

            i = 0
            clause = []
            while(i < self.num_clause):
                one_line = altogether.strip()
                token, rest = self.get_token(one_line)
                if(token == "0"):
                    formula_str.append(clause)
                    i = i + 1
                    clause = []
                else:
                    clause.append(token)
                altogether = rest

            self.formula_str = formula_str

    # initialize assignment

    def make_variables(self):
        self.var_lst = []
        for i in range(self.num_var):
            self.var_lst.append(Var(str(i+1)))

    def make_clauses(self):
        for i in range(len(self.formula_str)):

            self.clause_lst.append(Clause(str(i), self.formula_str[i]))
