from tokenizer import Tokenizer
from parser import Parser


def run(program):
    tokenizer = Tokenizer(program)
    tokens = tokenizer.tokenize()

    parser = Parser(tokens)
    variables, order = parser.parse_program()

    for name in order:
        print(f"{name} = {variables[name]}")


def main():
    print("Enter your program.")
    print("Type run to execute it.")
    print("Type quit to exit.")

    while True:
        lines = []

        while True:
            line = input()

            if line.strip() == "quit":
                return

            if line.strip() == "run":
                break

            lines.append(line)

        program = "\n".join(lines)

        if program.strip() == "":
            continue

        try:
            run(program)
        except Exception as e:
            print(e)


if __name__ == "__main__":
    main()