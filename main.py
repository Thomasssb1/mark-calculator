from typing import Set
from cli_parser import CLIParser
from module import Module
from module_calculator import ModuleCalculator

if __name__ == "__main__":
    parser = CLIParser()
    parser.add_option("target", required=True, value_type=int)
    parser.add_option("load", flag=True, default=False)

    parser.add_command("help", hidden=True)
    parser.add_option("help", command="help", flag=True, hidden=True, default=False)

    parser.parse()

    if parser.command == "help":
        print(parser)
    else:
        FILENAME = "scores.csv"
        modules: Set[Module] = set()
        if parser.was_parsed("load"):
            modules = Module.from_csv(FILENAME)
            print(f"Loaded modules from {FILENAME}")

        while inp := input("Enter a module name (or 'exit' to quit): ").strip():
            if inp.lower() == "exit":
                break

            if inp.lower() in {m.name.lower() for m in modules}:
                print(f"Module '{inp}' already exists. Replacing it.")

            try:
                credits = int(input("How many credits is it worth?: ").strip())
                grade = None
                try:
                    grade = int(input("What is the grade?: ").strip())
                except ValueError:
                    print("No grade provided, setting to None.")
                modules.add(Module(inp, credits, grade))
                print(f"Added module: {inp}")
            except ValueError:
                print("Invalid input. Please enter a number.")
                continue

        if parser.was_parsed("load"):
            Module.save_to_csv(modules, FILENAME)

        calculator = ModuleCalculator(
            modules,
            target=parser.get_option("target"),
        )
        print(calculator)
