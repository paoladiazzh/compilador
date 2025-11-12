# Tabla predictiva 

**Terminales en columnas:**  
`num`, `id`, `(`, `)`, `+`, `-`, `*`, `/`, `,`, `;` (puntoycoma), `{` (lbrace), `}` (rbrace), `if`, `else`, `while`, `for`, `return`, `print`, `int`, `float`, `void`, `asignacion`, `op_not`, `eof`


| No-terminal \ Terminal | num | id | ( | ) | + | - | * | / | , | ; | { | } | if | else | while | for | return | print | int | float | void | asignacion | op_not | eof |
|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| **S** |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  | `S → bof PROGRAMA eof` |
| **PROGRAMA** |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  | `PROGRAMA → LISTADECL` |  |  |  |  |  |
| **LISTADECL** |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  | `LISTADECL → DECL LISTADECL` | `LISTADECL → DECL LISTADECL` | `LISTADECL → DECL LISTADECL` |  |  | `LISTADECL → ε` (en `eof`) |
| **DECL** |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  | `DECL → TIPO DECL'` | `DECL → TIPO DECL'` | `DECL → TIPO DECL'` |  |  |  |
| **DECL'** |  | `DECL' → id DECL''` |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |
| **DECL''** |  | `DECL'' → LISTAID' puntoycoma` (si `,` o `;`) / `DECL'' → lparen DECL'''` (si `(`) | `DECL'' → lparen DECL'''` |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |
| **DECL'''** |  |  | `DECL''' → PARAMETROS rparen BLOQUE` |  |  |  |  |  |  |  | `DECL''' → PARAMETROS rparen BLOQUE` |  |  |  |  |  |  |  |  |  |  |  |  |
| **LISTAID** |  | `LISTAID → id LISTAID'` |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |
| **LISTAID'** |  | `LISTAID' → coma LISTAID` |  |  |  |  |  |  | `LISTAID' → ε` (si `;`) |  |  |  |  |  |  |  |  |  |  |  |  |  |  |
| **TIPO** |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  | `TIPO → int` | `TIPO → float` | `TIPO → void` |  |  |  |
| **PARAMETROS** |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  | `PARAMETROS → PARAMLISTA` | `PARAMETROS → PARAMLISTA` | `PARAMETROS → PARAMLISTA` |  |  | `PARAMETROS → ε` (si `)`) |
| **PARAMLISTA** |  | `PARAMLISTA → PARAM PARAMLISTA'` |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  | `PARAMLISTA → PARAM PARAMLISTA'` | `PARAMLISTA → PARAM PARAMLISTA'` | `PARAMLISTA → PARAM PARAMLISTA'` |  |  |  |
| **PARAMLISTA'** |  | `PARAMLISTA' → coma PARAM PARAMLISTA'` |  |  |  |  |  |  | `PARAMLISTA' → ε` (si `)`) |  |  |  |  |  |  |  |  |  |  |  |  |  |  |
| **PARAM** |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  | `PARAM → TIPO id` | `PARAM → TIPO id` | `PARAM → TIPO id` |  |  |  |
| **BLOQUE** |  |  |  |  |  |  |  |  |  |  | `BLOQUE → lbrace LISTASENTENCIAS rbrace` |  |  |  |  |  |  |  |  |  |  |  |  |
| **LISTASENTENCIAS** |  |  |  |  |  |  |  |  |  |  |  | `LISTASENTENCIAS → ε` (si `}`) |  |  |  |  |  |  |  |  |  |  |  |
| **SENTENCIA** |  | `SENTENCIA → SENTENCIAEXPR` / `SENTENCIA → BLOQUE` | `SENTENCIA → SENTENCIAEXPR` |  |  |  |  |  |  | `SENTENCIA → SENTENCIAEXPR` | `SENTENCIA → BLOQUE` |  | `SENTENCIA → SENTENCIASEL` |  | `SENTENCIA → SENTENCIAITER` | `SENTENCIA → SENTENCIAITER` | `SENTENCIA → SENTENCIARET` | `SENTENCIA → SENTENCIAPRINT` |  |  |  |  | `SENTENCIA → SENTENCIAEXPR` (por op_not) |  |
| **SENTENCIAEXPR** |  | `SENTENCIAEXPR → ASIGNACION puntoycoma` | `SENTENCIAEXPR → ASIGNACION puntoycoma` |  |  |  |  |  |  | `SENTENCIAEXPR → puntoycoma` |  |  |  |  |  |  |  |  |  |  |  | `SENTENCIAEXPR → ASIGNACION puntoycoma` (op_not) |  |
| **ASIGNACION** |  | `ASIGNACION → id asignacion EXPR` (si `id` seguido por `asignacion`) / `ASIGNACION → EXPR` (si id pero not asignacion) | `ASIGNACION → EXPR` |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  | `ASIGNACION → EXPR` (op_not) |  |
| **SENTENCIASEL** |  |  |  |  |  |  |  |  |  |  |  |  | `SENTENCIASEL → if lparen EXPR rparen SENTENCIA SENTENCIASEL'` |  |  |  |  |  |  |  |  |  |  |
| **SENTENCIASEL'** |  |  |  |  |  |  |  |  |  |  |  |  | `SENTENCIASEL' → else SENTENCIA` | `SENTENCIASEL' → ε` (si no `else`) |  |  |  |  |  |  |  |  |  |
| **SENTENCIAITER** |  |  |  |  |  |  |  |  |  |  |  |  |  |  | `SENTENCIAITER → while lparen EXPR rparen SENTENCIA` | `SENTENCIAITER → for lparen EXPR puntoycoma EXPR puntoycoma EXPR rparen SENTENCIA` |  |  |  |  |  |  |  |
| **SENTENCIARET** |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  | `SENTENCIARET → return EXPR puntoycoma` |  |  |  |  |  |  |
| **SENTENCIAPRINT** |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  | `SENTENCIAPRINT → print lparen EXPR rparen puntoycoma` |  |  |  |  |  |
| **EXPR** | `EXPR → Term EXPR'` | `EXPR → Term EXPR'` | `EXPR → Term EXPR'` |  |  |  |  |  |  | `EXPR → Term EXPR'` |  | `EXPR → Term EXPR'` |  |  |  |  |  |  |  |  |  | `EXPR → Term EXPR'` | `EXPR → Term EXPR'` |  |
| **EXPR'** |  |  |  | `EXPR' → ε` | `EXPR' → op_suma Term EXPR'` | `EXPR' → op_resta Term EXPR'` |  |  |  | `EXPR' → ε` |  | `EXPR' → ε` |  |  |  |  |  |  |  |  |  |  |  |  |
| **EXPRAND** | `EXPRAND → EXPREQ EXPRAND'` | `EXPRAND → EXPREQ EXPRAND'` | `EXPRAND → EXPREQ EXPRAND'` |  |  |  |  |  |  | `EXPRAND → EXPREQ EXPRAND'` |  | `EXPRAND → EXPREQ EXPRAND'` |  |  |  |  |  |  |  |  |  |  |  |
| **EXPRAND'** |  |  |  | `EXPRAND' → ε` |  |  |  |  |  | `EXPRAND' → ε` |  | `EXPRAND' → ε` |  |  |  |  |  |  |  |  |  | `EXPRAND' → op_and EXPREQ EXPRAND'` |  |
| **EXPREQ** | `EXPREQ → EXPRREL EXPREQ'` | `EXPREQ → EXPRREL EXPREQ'` | `EXPREQ → EXPRREL EXPREQ'` |  |  |  |  |  |  | `EXPREQ → EXPRREL EXPREQ'` |  | `EXPREQ → EXPRREL EXPREQ'` |  |  |  |  |  |  |  |  |  |  |  |
| **EXPREQ'** |  |  |  | `EXPREQ' → ε` |  |  |  |  |  | `EXPREQ' → ε` |  | `EXPREQ' → ε` |  |  |  |  |  |  |  |  |  | `EXPREQ' → op_eq EXPRREL EXPREQ'` / `op_neq ...` |  |
| **EXPRREL** | `EXPRREL → EXPRADIT EXPRREL'` | `EXPRREL → EXPRADIT EXPRREL'` | `EXPRREL → EXPRADIT EXPRREL'` |  |  |  |  |  |  | `EXPRREL → EXPRADIT EXPRREL'` |  | `EXPRREL → EXPRADIT EXPRREL'` |  |  |  |  |  |  |  |  |  |  |  |
| **EXPRREL'** |  |  |  | `EXPRREL' → ε` |  |  |  |  |  | `EXPRREL' → ε` |  | `EXPRREL' → ε` |  |  |  |  |  |  |  |  |  | `EXPRREL' → op_lt EXPRADIT EXPRREL'` / (op_gt/op_le/op_ge) |  |
| **EXPRADIT** | `EXPRADIT → TERM EXPRADIT'` | `EXPRADIT → TERM EXPRADIT'` | `EXPRADIT → TERM EXPRADIT'` |  |  |  |  |  |  | `EXPRADIT → TERM EXPRADIT'` |  | `EXPRADIT → TERM EXPRADIT'` |  |  |  |  |  |  |  |  |  |  |  |
| **EXPRADIT'** |  |  |  | `EXPRADIT' → ε` | `EXPRADIT' → op_suma TERM EXPRADIT'` | `EXPRADIT' → op_resta TERM EXPRADIT'` |  |  |  | `EXPRADIT' → ε` |  | `EXPRADIT' → ε` |  |  |  |  |  |  |  |  |  |  |  |
| **TERM** | `TERM → FACTOR TERM'` | `TERM → FACTOR TERM'` | `TERM → FACTOR TERM'` |  |  |  |  |  |  | `TERM → FACTOR TERM'` |  | `TERM → FACTOR TERM'` |  |  |  |  |  |  |  |  |  |  |  |
| **TERM'** |  |  |  | `TERM' → ε` |  |  | `TERM' → op_mul FACTOR TERM'` | `TERM' → op_div FACTOR TERM'` |  | `TERM' → ε` |  | `TERM' → ε` |  |  |  |  |  |  |  |  |  |  |  |
| **FACTOR** | `FACTOR → num` | `FACTOR → id FACTOR'` | `FACTOR → lparen EXPR rparen` |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  | `FACTOR → op_not FACTOR` |  |
| **FACTOR'** |  | `FACTOR' → ( ARGLIST )` (si `(`) / `FACTOR' → ( )` (si `(` y `)`) / `FACTOR' → ε` (si siguiente en FOLLOW es operador/; , )` |  | `FACTOR' → ε` |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |
| **ARGLIST** | `ARGLIST → EXPR ARGLIST'` | `ARGLIST → EXPR ARGLIST'` | `ARGLIST → EXPR ARGLIST'` |  |  |  |  |  |  | `ARGLIST → EXPR ARGLIST'` |  | `ARGLIST → EXPR ARGLIST'` |  |  |  |  |  |  |  |  |  |  |  |
| **ARGLIST'** |  | `ARGLIST' → coma ARGLIST` |  | `ARGLIST' → ε` |  |  |  |  | `ARGLIST' → comma ...` |  |  |  |  |  |  |  |  |  |  |  |  |  |  |
