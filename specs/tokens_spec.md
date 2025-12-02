
# Definición formal de Tokens

## Palabras clave
- `if`, `else`, `while`, `for`, `int`, `float`, `return`, `print`  
> Regla: reconocidas mediante el autómata de `ID` y reclasificadas si el lexema coincide.

## Tabla de tokens principales

| Token        | Expresión Regular                | Ejemplo(s) |
|--------------|----------------------------------|------------|
| IF           | `if`                             | `if` |
| ELSE         | `else`                           | `else` |
| WHILE        | `while`                          | `while` |
| FOR          | `for`                            | `for` |
| INT          | `int`                            | `int` |
| FLOAT        | `float`                          | `float` |
| RETURN       | `return`                         | `return` |
| PRINT        | `print`                          | `print` |
| ID           | `[A-Za-z_][A-Za-z0-9_]*`         | `contador`, `_temp` |
| NUM          | `(?:\d+\.\d+\|\d+)`              | `42`, `3.14` |
| ASIGNACION   | `=`                              | `=` |
| OP_EQ        | `==`                             | `==` |
| OP_NEQ       | `!=`                             | `!=` |
| OP_LE        | `<=`                             | `<=` |
| OP_GE        | `>=`                             | `>=` |
| OP_LT        | `<`                              | `<` |
| OP_GT        | `>`                              | `>` |
| OP_AND       | `&&`                             | `&&` |
| OP_OR        | `\|\|`                           | `\|\|` |
| OP_NOT       | `!`                              | `!` |
| OP_SUMA      | `\+`                             | `+` |
| OP_RESTA     | `-`                              | `-` |
| OP_MUL       | `\*`                             | `*` |
| OP_DIV       | `/`                              | `/` |
| OP_MOD       | `%`                              | `%` |
| LPAREN       | `\(`                             | `(` |
| RPAREN       | `\)`                             | `)` |
| LBRACE       | `\{`                             | `{` |
| RBRACE       | `\}`                             | `}` |
| PUNTOYCOMA   | `;`                              | `;` |
| COMA         | `,`                              | `,` |
| VOID         | `void`                           | `void` |

## Observaciones formales
- **Identificadores (ID)**: AFD con estado inicial `S`, transición por `[A-Za-z_]` a `A` (aceptación), y bucle en `A` por `[A-Za-z0-9_]`.
- **Números (NUM)**: AFD que acepta:
  - Enteros: `\d+`
  - Reales: `\d+\.\d+`
- **Operadores y delimitadores**: literales reconocidos por matching directo. Para multi-caracter se aplica maximal munch para priorizar `==`, `!=`, `<=`, `>=`, `&&`, `||` sobre sus prefijos de 1 carácter.
- **Limpieza**: se eliminan comentarios `//...`, `#...` y `/*...*/` y se normalizan caracteres extraños según la implementación.
