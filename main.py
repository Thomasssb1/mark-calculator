from typing import Set
from cli_parser import CLIParser
from module import Module
from module_calculator import ModuleCalculator

if __name__ == "__main__":
    parser = CLIParser()
    parser.add_option("target", required=True, value_type=int)
    parser.add_option("load", flag=True, default=True)

    parser.add_command("help", hidden=True)
    parser.add_option("help", command="help", flag=True, hidden=True, default=False)

    parser.add_command("add", description="Add a module")
    parser.add_option("name", command="add", value_type=str, required=True)
    parser.add_option("credits", command="add", required=True, value_type=int)
    parser.add_option("grade", command="add", value_type=int)

    parser.add_command("remove", description="Remove a module")
    parser.add_option("name", command="remove", value_type=str, required=True)

    parser.parse()

    if parser.command == "help":
        print(parser)
    else:
        FILENAME = "data/scores.csv"
        modules: Set[Module] = set()
        if parser.get_option("load"):
            modules = Module.from_csv(FILENAME)
            print(f"Loaded modules from {FILENAME}")

        if parser.command == "add":
            inp = parser.get_option("name", command="add")
            match = next((m for m in modules if m.name.lower() == inp.lower()), None)
            if match is not None:
                modules.discard(match)
                print(f"Module '{inp}' already exists. Replacing it.")
            try:
                credits = int(parser.get_option("credits", command="add"))
                grade = None
                try:
                    grade = int(parser.get_option("grade", command="add"))
                except TypeError:
                    print("No grade provided, setting to ungraded.")

                modules.add(Module(inp, credits, grade))
                print(f"Added module: {inp}")
            except TypeError:
                print("Invalid input for --credits. Please enter a number.")
        elif parser.command == "remove":
            inp = parser.get_option("name", command="remove")
            if inp.lower() in {m.name.lower() for m in modules}:
                modules = {m for m in modules if m.name.lower() != inp.lower()}
                print(f"Removed module: {inp}")
            else:
                print(f"Module '{inp}' not found.")

        if (
            parser.command == "add" or parser.command == "remove"
        ) and parser.get_option("load"):
            Module.save_to_csv(modules, FILENAME)

        else:
            calculator = ModuleCalculator(
                modules,
                target=parser.get_option("target"),
            )
            print(calculator)
