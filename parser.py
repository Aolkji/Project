class Parser:
    def __init__(self, tokens):
        self.tokens = tokens
        self.pos = 0

        self.variables = {}
        self.let_vars = set()
        self.order = []

    def current(self):
        return self.tokens[self.pos]

    def eat(self, kind):
        if self.current().kind == kind:
            self.pos += 1
        else:
            raise Exception("error")

    def parse_program(self):
        while self.current().kind != "EOF":
            self.parse_assignment()

        return self.variables, self.order

    def parse_assignment(self):
        is_let = False

        if self.current().kind == "LET":
            is_let = True
            self.eat("LET")

        if self.current().kind != "ID":
            raise Exception("error")

        name = self.current().value
        self.eat("ID")

        self.eat("=")

        value, used_normal = self.parse_exp()

        self.eat(";")

        # Let rule
        if is_let and used_normal:
            raise Exception("error, normal variables in let expression")

        # Prevents reassignment of let variable
        if name in self.let_vars:
            raise Exception("error")

        if name not in self.variables:
            self.order.append(name)

        self.variables[name] = value

        if is_let:
            self.let_vars.add(name)

    def parse_exp(self):
        value, used_normal = self.parse_term()

        while self.current().kind in ["+", "-"]:
            op = self.current().kind
            self.eat(op)

            right, right_used = self.parse_term()
            used_normal = used_normal or right_used

            if op == "+":
                value += right
            else:
                value -= right

        return value, used_normal

    def parse_term(self):
        value, used_normal = self.parse_fact()

        while self.current().kind == "*":
            self.eat("*")

            right, right_used = self.parse_fact()
            value *= right
            used_normal = used_normal or right_used

        return value, used_normal

    def parse_fact(self):
        if self.current().kind == "(":
            self.eat("(")
            value, used_normal = self.parse_exp()
            self.eat(")")
            return value, used_normal

        elif self.current().kind == "-":
            self.eat("-")
            value, used_normal = self.parse_fact()
            return -value, used_normal

        elif self.current().kind == "+":
            self.eat("+")
            return self.parse_fact()

        elif self.current().kind == "NUM":
            value = self.current().value
            self.eat("NUM")
            return value, False

        elif self.current().kind == "ID":
            name = self.current().value
            self.eat("ID")

            # Checks for uninitialized variable
            if name not in self.variables:
                raise Exception("error")

            # Checks if for normal variable usage
            if name in self.let_vars:
                return self.variables[name], False
            else:
                return self.variables[name], True

        else:
            raise Exception("error")