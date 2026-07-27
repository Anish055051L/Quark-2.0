# Quark 3.0

## Overview

Quark 3.0 is a lightweight interpreted scripting language written in
Python. It is designed to be easy to learn while still supporting
variables, math, conditions, loops, functions, file I/O, modules, and
simple game scripting.

## Features

-   Variables (`let`)
-   Printing and string substitution
-   Math evaluation
-   Random numbers
-   User input
-   Conditional execution (`if`)
-   Game loops
-   Custom functions
-   Importable modules
-   File read/write/append
-   Interactive REPL
-   `.qk` script execution

## Installation

1.  Install Python 3.10 or newer.
2.  Download `Quark_3.0.py`.
3.  Run:

``` bash
python Quark_3.0.py
```

## Hello World

``` text
print Hello, World!
```

## Variables

``` text
let name = Quark
print 'name'
```

## Math

``` text
math 5 * (3 + 2)
let x = math 10 / 2
```

## Conditions

``` text
let score = 100
if score == 100 then print Perfect!
```

## Game Loop

``` text
let lives = 3

game loop lives > 0
print Lives:, 'lives'
let lives = math lives - 1
loop end
```

## Functions

``` text
fn greet
print Hello!
fn end

call greet
```

## Files

``` text
write notes.txt Hello
append notes.txt World
read notes.txt
```

## Modules

``` text
import utilities
```

## Running Programs

``` text
run script.qk
game mygame
```

## Built-in Commands

-   help
-   print
-   math
-   let
-   repeat
-   if
-   game loop
-   fn / call
-   input
-   random
-   wait
-   time
-   read
-   write
-   append
-   run
-   game
-   import
-   clear
-   list
-   stop / exit / kill

## Project Goals

-   Simple syntax
-   Educational
-   Open source
-   Easy to extend

## License

MIT License (or your preferred license).

------------------------------------------------------------------------

Created by Professor Heisenberg.
