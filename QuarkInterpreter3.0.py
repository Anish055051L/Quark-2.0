# Quark 3.0 Gaming Version (With Loops & Functions)
import random
import time
import sys
import os
import re

variables = {}
functions = {}  # Stores custom functions: { "func_name": [lines_of_code] }

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
    Parses individual items in a print command.
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

    def replace_quoted_var(match):
        var_name = match.group(1)
        if var_name == "time":
            return time.strftime("%H:%M:%S")
        return str(variables.get(var_name, f"'{var_name}'"))

    if item.startswith("'") and item.endswith("'") and len(item) > 1:
        inner = item[1:-1]
        if inner == "time":
            return time.strftime("%H:%M:%S")
        return str(variables.get(inner, item))

    item = re.sub(r"'([a-zA-Z_][a-zA-Z0-9_]*)'", replace_quoted_var, item)
    return item

def eval_condition(condition_expr):
    """
    Evaluates conditional expressions for 'if' and 'game loop'.
    """
    condition = safe_substitute(condition_expr)

    def quote_words(expr):
        for op in ("==", "!=", ">=", "<=", ">", "<"):
            if op in expr:
                left, right = expr.split(op, 1)
                left, right = left.strip(), right.strip()
                if not left.isdigit() and not (left.startswith('"') or left.startswith("'")):
                    left = f"'{left}'"
                if not right.isdigit() and not (right.startswith('"') or right.startswith("'")):
                    right = f"'{right}'"
                return f"{left} {op} {right}"
        return expr

    try:
        return bool(eval(condition))
    except (SyntaxError, NameError):
        try:
            return bool(eval(quote_words(condition)))
        except Exception as e:
            print(f"Condition Error: {e} //Found By QuarkSaviour!")
            return False
    except Exception as e:
        print(f"Condition Error: {e} //Found By QuarkSaviour!")
        return False

def find_matching_block_end(code_lines, start_idx, start_keyword, end_keyword):
    """Scans forward to find matching block end tags for loops or functions."""
    depth = 0
    for i in range(start_idx, len(code_lines)):
        l = code_lines[i].strip()
        if l.startswith(start_keyword):
            depth += 1
        elif l == end_keyword:
            depth -= 1
            if depth == 0:
                return i
    return len(code_lines)

def run_code(code_lines):
    """
    Executes lines with support for loops and functions.
    """
    line_idx = 0
    total_lines = len(code_lines)
    loop_stack = []

    while line_idx < total_lines:
        line = code_lines[line_idx].strip()

        if not line or line.startswith("#"):
            line_idx += 1
            continue

        # 1. FUNCTION DEFINITION (Store code without executing)
        if line.startswith("fn "):
            func_name = line[3:].strip()
            end_idx = find_matching_block_end(code_lines, line_idx, "fn", "fn end")
            
            # Extract function body lines
            functions[func_name] = code_lines[line_idx + 1 : end_idx]
            
            # Skip past 'fn end'
            line_idx = end_idx + 1
            continue

        # 2. CALL FUNCTION
        elif line.startswith("call "):
            func_name = line[5:].strip()
            if func_name in functions:
                run_code(functions[func_name])
            else:
                print(f"Function Error: '{func_name}' is not defined //Found By QuarkSaviour!")

        # 3. GAME LOOP START
        elif line.startswith("game loop"):
            condition_expr = line[len("game loop"):].strip()
            if eval_condition(condition_expr):
                loop_stack.append(line_idx)
            else:
                line_idx = find_matching_block_end(code_lines, line_idx, "game loop", "loop end")

        # 4. GAME LOOP END
        elif line == "loop end":
            if loop_stack:
                line_idx = loop_stack.pop() - 1

        # 5. ALL OTHER COMMANDS
        else:
            execute(line)

        line_idx += 1

def execute(line):
    line = line.strip()

    if not line or line.startswith("#"):
        return

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
            name, value = name.strip(), value.strip()

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

        if first_token_sub.isdigit():
            count = int(first_token_sub)
            command_to_run = remaining_cmd
        else:
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
        result = os.system("cls" if os.name == "nt" else "clear")
        if result != 0:
            print("\n" * 100)

    elif cmd == "time":
        print(time.strftime("%H:%M:%S"))

    elif cmd == "wait":
        try:
            time.sleep(float(safe_substitute(arg)))
        except ValueError:
            print("Usage: wait <seconds> //Found By QuarkSaviour!")

    elif cmd in ("run", "game"):
        target = safe_substitute(arg.strip())
        ext = ".qk" if cmd == "game" and not target.endswith(".qk") else ""
        try:
            with open(target + ext, "r") as file:
                run_code(file.readlines())
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
        filename = safe_substitute(filename.strip())
        content = content.strip()

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

    elif cmd == "list":
        print("--- VARIABLES ---")
        for k, v in variables.items():
            print(f"{k} = {v}")
        print("--- FUNCTIONS ---")
        for k in functions:
            print(f"fn {k}")

    elif cmd == "input":
        if " -> " in arg:
            prompt_text, var_name = arg.split(" -> ", 1)
            var_name = var_name.strip()

            def replace_quoted_var(match):
                var = match.group(1)
                if var == "time":
                    return time.strftime("%H:%M:%S")
                return str(variables.get(var, f"'{var}'"))

            prompt_text = prompt_text.strip()
            prompt_text = re.sub(r"'([a-zA-Z_][a-zA-Z0-9_]*)'", replace_quoted_var, prompt_text)
            variables[var_name] = input(prompt_text + " ")
        else:
            var_name = arg.strip()
            variables[var_name] = input(f"Enter {var_name}: ")

    elif cmd == "if":
        condition, _, command = arg.partition(" then ")
        if eval_condition(condition):
            execute(command)

    elif cmd == "import":
        try:
            with open(arg + ".qk", "r") as file:
                run_code(file.readlines())
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
game loop <condition> ... loop end
fn <name> ... fn end
call <name>
input <prompt> -> <var>  (or input <var>)
list
time
wait <seconds>
random <min> <max>
read <file>
run / game <file>
write / append <file> <content>
clear
import <module>
stop / exit / kill
""")

while running:
    try:
        user_input = input(">>> ").strip()
        if not user_input:
            continue

        # Multiline block collector for loops and functions in interactive mode
        if user_input.startswith("game loop") or user_input.startswith("fn "):
            buffer = [user_input]
            depth = 1
            start_kw = "game loop" if user_input.startswith("game loop") else "fn"
            end_kw = "loop end" if start_kw == "game loop" else "fn end"

            while depth > 0:
                sub_line = input("... ").strip()
                buffer.append(sub_line)
                if sub_line.startswith(start_kw):
                    depth += 1
                elif sub_line == end_kw:
                    depth -= 1

            run_code(buffer)
        else:
            run_code([user_input])

    except (KeyboardInterrupt, EOFError):
        print("\nShell Stopped Working. Thank You For Using Quark!")
        sys.exit()
