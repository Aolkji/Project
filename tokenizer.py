class Token:
    def __init__(self, kind, value):
        self.kind = kind
        self.value = value


class Tokenizer:
    def __init__(self, text):
        self.text = text
        self.pos = 0

    def tokenize(self):
        tokens = []

        while self.pos < len(self.text):
            c = self.text[self.pos]

            if c.isspace():
                self.pos += 1

            elif c.isalpha() or c == "_":
                word = self.read_identifier()
                if word == "let":
                    tokens.append(Token("LET", word))
                else:
                    tokens.append(Token("ID", word))

            elif c.isdigit():
                num = self.read_number()

                # ❗ Leading zero check
                if len(num) > 1 and num[0] == "0":
                    raise Exception("error")

                tokens.append(Token("NUM", int(num)))

            elif c in "+-*();=":
                tokens.append(Token(c, c))
                self.pos += 1

            else:
                raise Exception("error")

        tokens.append(Token("EOF", "EOF"))
        return tokens

    def read_identifier(self):
        start = self.pos
        while self.pos < len(self.text) and (
            self.text[self.pos].isalnum() or self.text[self.pos] == "_"
        ):
            self.pos += 1
        return self.text[start:self.pos]

    def read_number(self):
        start = self.pos
        while self.pos < len(self.text) and self.text[self.pos].isdigit():
            self.pos += 1
        return self.text[start:self.pos]