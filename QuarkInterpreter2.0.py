# Quark 2.0 Market Version
import random
import time
import sys
import os
import re

variables = {}

print("Welcome To Quark 2.0, The Future Of Programming! ")
time.sleep(1)
print("Initialising Shell... ")
time.sleep(2)
print("Done!")

running = True

def safe_substitute(text):
    """
    Replace ONLY whole variable names.
    Variables inside quotes are ignored.
    """

    for name, value in sorted(variables.items(), key=lambda x: len(x[0]), reverse=True):
        pattern = rf"\b{re.escape(name)}\b"
        text = re.sub(pattern, str(value), text)

    return text

def parse_print_item(item):
    """
    Parses individual items in a print command:
    - Items inside single quotes like 'var' or 'time' print evaluated values.
    - Special tokens like math, random are processed.
    - Regular unquoted text is printed literally.
    """
    item = item.strip()

    if item.startswith("math "):
        expr = safe_substitute(item[5:])
        try:
            return str(eval(expr))
        except Exception:
            return "Error //Found By QuarkSaviour!"

    elif item.startswith("random "):
        try:
            low, high = map(int, safe_substitute(item[7:]).split())
            return str(random.randint(low, high))
        except ValueError:
            return "Error //Found By QuarkSaviour!"

    # Helper function to evaluate single-quoted variables or 'time'
    def replace_quoted_var(match):
        var_name = match.group(1)
        if var_name == "time":
            return time.strftime("%H:%M:%S")
        return str(variables.get(var_name, f"'{var_name}'"))

    # If the item itself is wrapped in single quotes e.g. 'time' or 'score'
    if item.startswith("'") and item.endswith("'") and len(item) > 1:
        inner = item[1:-1]
        if inner == "time":
            return time.strftime("%H:%M:%S")
        return str(variables.get(inner, item))

    # Substitute inline quoted variables inside text e.g. "Current time is 'time'"
    item = re.sub(r"'([a-zA-Z_][a-zA-Z0-9_]*)'", replace_quoted_var, item)

    return item

def execute(line):
    line = line.strip()

    # Ignore blank lines and comments starting with '#'
    if not line or line.startswith("#"):
        return

    # Parse command and arguments safely
    parts = line.split(" ", 1)
    cmd = parts[0].strip()
    arg = parts[1].strip() if len(parts) > 1 else ""

    if cmd == "math":
        expression = safe_substitute(arg)
        try:
            print(eval(expression))
        except Exception as e:
            print(f"Math Error: {e} //Found By QuarkSaviour!")

    elif cmd in ("stop", "exit", "kill"):
        print("Shell Stopped Working. Thank You For Using Quark! ")
        sys.exit()

    elif cmd == "let":
        if "=" in arg:
            name, value = arg.split("=", 1)
            name = name.strip()
            value = value.strip()

            if value.startswith("math "):
                expression = safe_substitute(value[5:])
                try:
                    variables[name] = str(eval(expression))
                except Exception as e:
                    print(f"Math Error: {e} //Found By QuarkSaviour!")

            elif value.startswith("random "):
                try:
                    low, high = map(int, safe_substitute(value[7:]).split())
                    variables[name] = str(random.randint(low, high))
                except ValueError:
                    print("Error: Usage 'let var = random <min> <max>' //Found By QuarkSaviour!")

            else:
                variables[name] = safe_substitute(value)

    elif cmd == "print":
        if not arg:
            print()
            return

        items = [item.strip() for item in arg.split(",")]
        output = [parse_print_item(item) for item in items]
        print(*output)

    elif cmd == "repeat":
        if not arg:
            print("Usage: repeat <count> <command> //Found By QuarkSaviour!")
            return

        first_token, _, remaining_cmd = arg.partition(" ")
        first_token_sub = safe_substitute(first_token)

        # Check if the user specified a count or directly passed a command
        if first_token_sub.isdigit():
            count = int(first_token_sub)
            command_to_run = remaining_cmd
        else:
            # Default to 1 repeat if count is omitted
            count = 1
            command_to_run = arg

        if command_to_run:
            for _ in range(count):
                execute(command_to_run)

    elif cmd == "random":
        try:
            low, high = map(int, safe_substitute(arg).split())
            print(random.randint(low, high))
        except ValueError:
            print("Usage: random <min> <max> //Found By QuarkSaviour!")

    elif cmd == "help":
        help()

    elif cmd == "clear":
        os.system("cls" if os.name == "nt" else "clear")

    elif cmd == "time":
        print(time.strftime("%H:%M:%S"))

    elif cmd == "wait":
        try:
            time.sleep(float(safe_substitute(arg)))
        except ValueError:
            print("Usage: wait <seconds> //Found By QuarkSaviour!")

    elif cmd == "run":
        target = safe_substitute(arg.strip())
        try:
            with open(target, "r") as file:
                for file_line in file:
                    execute(file_line)
        except FileNotFoundError:
            print(f"Error: '{target}' does not exist //Found By QuarkSaviour!")

    elif cmd == "game":
        target = safe_substitute(arg.strip())
        try:
            with open(target + ".qk", "r") as file:
                for file_line in file:
                    execute(file_line)
        except FileNotFoundError:
            print(f"Error: '{target}' does not exist //Found By QuarkSaviour!")

    elif cmd == "read":
        target = safe_substitute(arg.strip())
        try:
            with open(target, "r") as file:
                print(file.read().strip())
        except FileNotFoundError:
            print(f"Error: '{target}' does not exist //Found By QuarkSaviour!")

    elif cmd in ("write", "append"):
        mode = "w" if cmd == "write" else "a"
        filename, _, content = arg.partition(" ")
        
        # Substitute variable names in filename dynamically
        filename = safe_substitute(filename.strip())
        content = content.strip()

        # Handle special built-ins like 'time' or 'math'
        if content == "time":
            text_to_save = time.strftime("%H:%M:%S")
        elif content.startswith("math "):
            try:
                text_to_save = str(eval(safe_substitute(content[5:])))
            except Exception:
                text_to_save = "Error"
        else:
            text_to_save = safe_substitute(content)

        try:
            with open(filename, mode) as file:
                file.write(text_to_save + "\n")
        except Exception as e:
            print(f"{cmd.capitalize()} Error: {e} //Found By QuarkSaviour!")

    elif cmd == "input":
    # Syntax:
    # input Prompt -> variable
    # Variables are substituted ONLY if enclosed in single quotes.

        if " -> " in arg:
            prompt_text, var_name = arg.split(" -> ", 1)
            var_name = var_name.strip()

        # Same helper used by print
            def replace_quoted_var(match):
                var = match.group(1)

                if var == "time":
                    return time.strftime("%H:%M:%S")

                return str(variables.get(var, f"'{var}'"))

            prompt_text = prompt_text.strip()

            # Only replace variables inside single quotes
            prompt_text = re.sub(
                r"'([a-zA-Z_][a-zA-Z0-9_]*)'",
                replace_quoted_var,
                prompt_text,
            )

            variables[var_name] = input(prompt_text + " ")

        else:
            var_name = arg.strip()
            variables[var_name] = input(f"Enter {var_name}: ")

    elif cmd == "list":
        for k, v in variables.items():
            print(f"{k} = {v}")

    elif cmd == "if":
        condition, _, command = arg.partition(" then ")
        condition = safe_substitute(condition)

        # Helper function to quote unquoted text words for safe eval()
        def quote_words(expr):
            for op in ("==", "!=", ">=", "<=", ">", "<"):
                if op in expr:
                    left, right = expr.split(op, 1)
                    left = left.strip()
                    right = right.strip()
                    # If side isn't a number or already quoted, quote it
                    if not left.isdigit() and not (left.startswith('"') or left.startswith("'")):
                        left = f"'{left}'"
                    if not right.isdigit() and not (right.startswith('"') or right.startswith("'")):
                        right = f"'{right}'"
                    return f"{left} {op} {right}"
            return expr

        try:
            if eval(condition):
                execute(command)
        except (SyntaxError, NameError):
            try:
                fixed_condition = quote_words(condition)
                if eval(fixed_condition):
                    execute(command)
            except Exception as e:
                print(f"If Condition Error: {e} //Found By QuarkSaviour!")
        except Exception as e:
            print(f"If Condition Error: {e} //Found By QuarkSaviour!")

    elif cmd == "import":
        try:
            with open(arg + ".qk", "r") as file:
                for line in file:
                    execute(line)
        except FileNotFoundError:
            print("Module not found. Found By QuarkSaviour!")

    else:
        print(f"Unknown command: {cmd} //Found By QuarkSaviour!")

def help():
    print("""Commands:
help
print <item1>, <item2>
math <expression>
let var = value / math / random
repeat <count> <command>
if <condition> then <command>
input <prompt> -> <var>  (or input <var>)
list
time
wait <seconds>
random <min> <max>
read <file>
run <file>
game <file>
write <file> <content>
append <file> <content>
clear
import <module>
stop / exit / kill
""")

while running:
    try:
        user_input = input(">>> ")
        execute(user_input)
    except (KeyboardInterrupt, EOFError):
        print("\nShell Stopped Working. Thank You For Using Quark!")
        sys.exit()
