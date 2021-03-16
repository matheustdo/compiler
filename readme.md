# Lexical Analyzer
This code was made using python to learn about lexycal analyzis.

### How to use
The main code is at 'lexical_analyzer.py' file.
To execute, you should have python 3 instaled and run the followed command:

```bash
python lexical_analyzer.py
```

or

```bash
python lexical_analyzer.py
```

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
Comment delimiters | // This is a comment
                   | /* This is
                   | a comment */
Delimiters | ; , ( ) { } [ ] .
String | " ( letter \| digit \| symbol \| \" )* "
Symbol | ASCII code from 32 to 126 (except ASCII 34)

### About
Developed by [Matheus Teles](https://github.com/matheustdo).