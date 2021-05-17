# Compiler
This code was made using python to learn about formal languages and compilers.

### How to use
The main code is at 'compiler.py' file.

A folder named as 'input/' must be created at the root path, containing the input files, which are named as 'entradaXYZ.txt', where 'XYZ" represents an integer value.

To execute the compiler you should have python 3 instaled at your machine, and run the following command:

```bash
python3 compiler.py
```

or

```bash
python compiler.py
```

The output files are created on 'output/' folder, located at the root.

### Lexical structure table
The analyzer follows the  lexical structure below:

Type | Format
--- | --- |
Reserved words | var, const, typedef, struct, extends, procedure, function, start, return, if, else, then, while, read, print, int, real, boolean, string, true, false, global, local |
Identifiers | letter(letter \| digit \| _ ) *
Numbers | Digit+(.Digit+))?
Digit | [0-9]
Letter | [a-z] \| [A-Z]
Arithmetic operator | + - * / ++ --
Relational operator | == != > >= < <= =
Logical operator | && \|\| !
Comment delimiters | // This is a comment<br />/* This is<br />a comment */
Delimiters | ; , ( ) { } [ ] .
String | " ( letter \| digit \| symbol \| \" )* "
Symbol | ASCII code from 32 to 126 (except ASCII 34)

### Grammar
The grammar is factored on the left, without left recursion, respecting the precedence and associativity of the arithmetic, logical and relational operators, using the GOLD Parser Builder software.

Its code was built by the class and can be found at [Compiler Grammar](https://github.com/diegossl/compiler-grammar).

### About
Developed by [Matheus Teles](https://github.com/matheustdo).