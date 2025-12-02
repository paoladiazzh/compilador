# Tabla Predictiva 

**Terminales en columnas:**  
`num`, `id`, `(` (lparen), `)` (rparen), `+` (op_suma), `-` (op_resta), `*` (op_mul), `/` (op_div), `%` (op_mod), `,` (coma), `;` (puntoycoma), `{` (lbrace), `}` (rbrace), `if`, `else`, `while`, `for`, `return`, `print`, `int`, `float`, `void`, `=` (asignacion), `!` (op_not), `==` (op_eq), `!=` (op_neq), `<` (op_lt), `>` (op_gt), `<=` (op_le), `>=` (op_ge), `&&` (op_and), `||` (op_or), `eof`

---

## Tabla Completa

| No-terminal | num | id | ( | ) | op_suma | op_resta | op_mul | op_div | op_mod | coma | ; | { | } | if | else | while | for | return | print | int | float | void | asignacion | op_not | op_eq | op_neq | op_lt | op_gt | op_le | op_ge | op_and | op_or | eof |
|-------------|-----|----|----|---|---------|----------|--------|--------|--------|------|---|---|---|----|----|-------|-----|--------|-------|-----|-------|------|------------|--------|-------|--------|-------|-------|-------|-------|--------|-------|-----|
| **S** | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | S → bof PROGRAMA eof |
| **PROGRAMA** | | | | | | | | | | | | | | | | | | | | PROGRAMA → LISTADECL | PROGRAMA → LISTADECL | PROGRAMA → LISTADECL | | | | | | | | | | | PROGRAMA → LISTADECL |
| **LISTADECL** | | | | | | | | | | | | | | | | | | | | LISTADECL → DECL LISTADECL | LISTADECL → DECL LISTADECL | LISTADECL → DECL LISTADECL | | | | | | | | | | | LISTADECL → ε |
| **DECL** | | | | | | | | | | | | | | | | | | | | DECL → TIPO DECL' | DECL → TIPO DECL' | DECL → TIPO DECL' | | | | | | | | | | | |
| **DECL'** | | DECL' → id DECL'' | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | |
| **DECL''** | | | DECL'' → lparen DECL''' | | | | | | | DECL'' → LISTAID' puntoycoma | DECL'' → LISTAID' puntoycoma | | | | | | | | | | | | | | | | | | | | | | |
| **DECL'''** | | | | DECL''' → PARAMETROS rparen BLOQUE | | | | | | | | | | | | | | | | DECL''' → PARAMETROS rparen BLOQUE | DECL''' → PARAMETROS rparen BLOQUE | DECL''' → PARAMETROS rparen BLOQUE | | | | | | | | | | | |
| **LISTAID'** | | | | | | | | | | LISTAID' → coma LISTAID | LISTAID' → ε | | | | | | | | | | | | | | | | | | | | | | |
| **TIPO** | | | | | | | | | | | | | | | | | | | | TIPO → int | TIPO → float | TIPO → void | | | | | | | | | | | |
| **PARAMETROS** | | | | PARAMETROS → ε | | | | | | | | | | | | | | | | PARAMETROS → PARAMLISTA | PARAMETROS → PARAMLISTA | PARAMETROS → PARAMLISTA | | | | | | | | | | | |
| **PARAMLISTA** | | | | | | | | | | | | | | | | | | | | PARAMLISTA → PARAM PARAMLISTA' | PARAMLISTA → PARAM PARAMLISTA' | PARAMLISTA → PARAM PARAMLISTA' | | | | | | | | | | | |
| **PARAMLISTA'** | | | | PARAMLISTA' → ε | | | | | | PARAMLISTA' → coma PARAM PARAMLISTA' | | | | | | | | | | | | | | | | | | | | | | | |
| **PARAM** | | | | | | | | | | | | | | | | | | | | PARAM → TIPO id | PARAM → TIPO id | PARAM → TIPO id | | | | | | | | | | | |
| **BLOQUE** | | | | | | | | | | | | BLOQUE → lbrace LISTASENTENCIAS rbrace | | | | | | | | | | | | | | | | | | | | | |
| **LISTASENTENCIAS** | LISTASENTENCIAS → SENTENCIA LISTASENTENCIAS | LISTASENTENCIAS → SENTENCIA LISTASENTENCIAS | LISTASENTENCIAS → SENTENCIA LISTASENTENCIAS | | | | | | | | LISTASENTENCIAS → SENTENCIA LISTASENTENCIAS | LISTASENTENCIAS → SENTENCIA LISTASENTENCIAS | LISTASENTENCIAS → ε | LISTASENTENCIAS → SENTENCIA LISTASENTENCIAS | | LISTASENTENCIAS → SENTENCIA LISTASENTENCIAS | LISTASENTENCIAS → SENTENCIA LISTASENTENCIAS | LISTASENTENCIAS → SENTENCIA LISTASENTENCIAS | LISTASENTENCIAS → SENTENCIA LISTASENTENCIAS | LISTASENTENCIAS → SENTENCIA LISTASENTENCIAS | LISTASENTENCIAS → SENTENCIA LISTASENTENCIAS | LISTASENTENCIAS → SENTENCIA LISTASENTENCIAS | | LISTASENTENCIAS → SENTENCIA LISTASENTENCIAS | | | | | | | | | |
| **SENTENCIA** | SENTENCIA → SENTENCIAEXPR | SENTENCIA → SENTENCIAEXPR | SENTENCIA → SENTENCIAEXPR | | | | | | | | SENTENCIA → SENTENCIAEXPR | SENTENCIA → BLOQUE | | SENTENCIA → SENTENCIASEL | | SENTENCIA → SENTENCIAITER | SENTENCIA → SENTENCIAITER | SENTENCIA → SENTENCIARET | SENTENCIA → SENTENCIAPRINT | SENTENCIA → DECLLOCAL | SENTENCIA → DECLLOCAL | SENTENCIA → DECLLOCAL | | SENTENCIA → SENTENCIAEXPR | | | | | | | | | |
| **DECLLOCAL** | | | | | | | | | | | | | | | | | | | | DECLLOCAL → TIPO id DECLLOCAL' puntoycoma | DECLLOCAL → TIPO id DECLLOCAL' puntoycoma | DECLLOCAL → TIPO id DECLLOCAL' puntoycoma | | | | | | | | | | | |
| **DECLLOCAL'** | | | | | | | | | | DECLLOCAL' → DECLLOCAL'' | DECLLOCAL' → DECLLOCAL'' | | | | | | | | | | | | DECLLOCAL' → asignacion EXPR DECLLOCAL'' | | | | | | | | | | |
| **DECLLOCAL''** | | | | | | | | | | DECLLOCAL'' → coma id DECLLOCAL' | DECLLOCAL'' → ε | | | | | | | | | | | | | | | | | | | | | | |
| **SENTENCIAEXPR** | SENTENCIAEXPR → EXPR puntoycoma | SENTENCIAEXPR → EXPR puntoycoma | SENTENCIAEXPR → EXPR puntoycoma | | | | | | | | SENTENCIAEXPR → puntoycoma | | | | | | | | | | | | | SENTENCIAEXPR → EXPR puntoycoma | | | | | | | | | |
| **SENTENCIASEL** | | | | | | | | | | | | | | SENTENCIASEL → if lparen EXPR rparen SENTENCIA SENTENCIASEL' | | | | | | | | | | | | | | | | | | | |
| **SENTENCIASEL'** | SENTENCIASEL' → ε | SENTENCIASEL' → ε | SENTENCIASEL' → ε | | | | | | | | SENTENCIASEL' → ε | SENTENCIASEL' → ε | SENTENCIASEL' → ε | SENTENCIASEL' → ε | SENTENCIASEL' → else SENTENCIA | SENTENCIASEL' → ε | SENTENCIASEL' → ε | SENTENCIASEL' → ε | SENTENCIASEL' → ε | SENTENCIASEL' → ε | SENTENCIASEL' → ε | SENTENCIASEL' → ε | | SENTENCIASEL' → ε | | | | | | | | | |
| **SENTENCIAITER** | | | | | | | | | | | | | | | | SENTENCIAITER → while lparen EXPR rparen SENTENCIA | SENTENCIAITER → for lparen EXPR puntoycoma EXPR puntoycoma EXPR rparen SENTENCIA | | | | | | | | | | | | | | | | |
| **SENTENCIARET** | | | | | | | | | | | | | | | | | | SENTENCIARET → return EXPR puntoycoma | | | | | | | | | | | | | | | |
| **SENTENCIAPRINT** | | | | | | | | | | | | | | | | | | | SENTENCIAPRINT → print lparen EXPR rparen puntoycoma | | | | | | | | | | | | | | |
| **EXPR** | EXPR → EXPRAND EXPR' | EXPR → EXPRAND EXPR' | EXPR → EXPRAND EXPR' | | | | | | | | | | | | | | | | | | | | | EXPR → EXPRAND EXPR' | | | | | | | | | |
| **EXPR'** | | | | EXPR' → ε | | | | | | EXPR' → ε | EXPR' → ε | | | | | | | | | | | | | | | | | | | | EXPR' → op_or EXPRAND EXPR' | | |
| **EXPRAND** | EXPRAND → EXPREQ EXPRAND' | EXPRAND → EXPREQ EXPRAND' | EXPRAND → EXPREQ EXPRAND' | | | | | | | | | | | | | | | | | | | | | EXPRAND → EXPREQ EXPRAND' | | | | | | | | | |
| **EXPRAND'** | | | | EXPRAND' → ε | | | | | | EXPRAND' → ε | EXPRAND' → ε | | | | | | | | | | | | | | | | | | | | EXPRAND' → op_and EXPREQ EXPRAND' | EXPRAND' → ε | |
| **EXPREQ** | EXPREQ → EXPRREL EXPREQ' | EXPREQ → EXPRREL EXPREQ' | EXPREQ → EXPRREL EXPREQ' | | | | | | | | | | | | | | | | | | | | | EXPREQ → EXPRREL EXPREQ' | | | | | | | | | |
| **EXPREQ'** | | | | EXPREQ' → ε | | | | | | EXPREQ' → ε | EXPREQ' → ε | | | | | | | | | | | | | | EXPREQ' → op_eq EXPRREL EXPREQ' | EXPREQ' → op_neq EXPRREL EXPREQ' | | | | | EXPREQ' → ε | EXPREQ' → ε | |
| **EXPRREL** | EXPRREL → EXPRADIT EXPRREL' | EXPRREL → EXPRADIT EXPRREL' | EXPRREL → EXPRADIT EXPRREL' | | | | | | | | | | | | | | | | | | | | | EXPRREL → EXPRADIT EXPRREL' | | | | | | | | | |
| **EXPRREL'** | | | | EXPRREL' → ε | | | | | | EXPRREL' → ε | EXPRREL' → ε | | | | | | | | | | | | | | EXPRREL' → ε | EXPRREL' → ε | EXPRREL' → op_lt EXPRADIT | EXPRREL' → op_gt EXPRADIT | EXPRREL' → op_le EXPRADIT | EXPRREL' → op_ge EXPRADIT | EXPRREL' → ε | EXPRREL' → ε | |
| **EXPRADIT** | EXPRADIT → TERM EXPRADIT' | EXPRADIT → TERM EXPRADIT' | EXPRADIT → TERM EXPRADIT' | | | | | | | | | | | | | | | | | | | | | EXPRADIT → TERM EXPRADIT' | | | | | | | | | |
| **EXPRADIT'** | | | | EXPRADIT' → ε | EXPRADIT' → op_suma TERM EXPRADIT' | EXPRADIT' → op_resta TERM EXPRADIT' | | | | EXPRADIT' → ε | EXPRADIT' → ε | | | | | | | | | | | | | | EXPRADIT' → ε | EXPRADIT' → ε | EXPRADIT' → ε | EXPRADIT' → ε | EXPRADIT' → ε | EXPRADIT' → ε | EXPRADIT' → ε | EXPRADIT' → ε | |
| **TERM** | TERM → FACTOR TERM' | TERM → FACTOR TERM' | TERM → FACTOR TERM' | | | | | | | | | | | | | | | | | | | | | TERM → FACTOR TERM' | | | | | | | | | |
| **TERM'** | | | | TERM' → ε | TERM' → ε | TERM' → ε | TERM' → op_mul FACTOR TERM' | TERM' → op_div FACTOR TERM' | TERM' → op_mod FACTOR TERM' | TERM' → ε | TERM' → ε | | | | | | | | | | | | | | TERM' → ε | TERM' → ε | TERM' → ε | TERM' → ε | TERM' → ε | TERM' → ε | TERM' → ε | TERM' → ε | |
| **FACTOR** | FACTOR → num | FACTOR → id FACTOR' | FACTOR → lparen EXPR rparen | | | | | | | | | | | | | | | | | | | | | FACTOR → op_not FACTOR | | | | | | | | | |
| **FACTOR'** | | | FACTOR' → lparen ARGLIST rparen / FACTOR' → lparen rparen | FACTOR' → ε | FACTOR' → ε | FACTOR' → ε | FACTOR' → ε | FACTOR' → ε | FACTOR' → ε | FACTOR' → ε | FACTOR' → ε | | | | | | | | | | | | FACTOR' → asignacion EXPR | | FACTOR' → ε | FACTOR' → ε | FACTOR' → ε | FACTOR' → ε | FACTOR' → ε | FACTOR' → ε | FACTOR' → ε | FACTOR' → ε | |
| **ARGLIST** | ARGLIST → EXPR ARGLIST' | ARGLIST → EXPR ARGLIST' | ARGLIST → EXPR ARGLIST' | | | | | | | | | | | | | | | | | | | | | ARGLIST → EXPR ARGLIST' | | | | | | | | | |
| **ARGLIST'** | | | | ARGLIST' → ε | | | | | | ARGLIST' → coma ARGLIST | | | | | | | | | | | | | | | | | | | | | | | |
