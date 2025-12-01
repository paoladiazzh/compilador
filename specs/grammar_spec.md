**S** → ``bof`` **PROGRAMA** ``eof``

**PROGRAMA** → **LISTADECL**

**LISTADECL** → **DECL** **LISTADECL** | ε

**DECL** → **TIPO** **DECL'**

**DECL'** → ``id`` **DECL''**

**DECL''** → **LISTAID'** ``puntoycoma`` | ``lparen`` **DECL'''**

**DECL'''** → **PARAMETROS** ``rparen`` **BLOQUE** | ``rparen`` **BLOQUE**

**LISTAID** → ``id`` **LISTAID'**

**LISTAID'** → ``coma`` **LISTAID** | ε

**TIPO** → ``int`` | ``float`` | ``void``

**PARAMETROS** → **PARAMLISTA** | ε

**PARAMLISTA** → **PARAM** **PARAMLISTA'**

**PARAMLISTA'** → ``coma`` **PARAM** **PARAMLISTA'** | ε

**PARAM** → **TIPO** ``id``

**BLOQUE** → ``lbrace`` **LISTASENTENCIAS** ``rbrace``

**LISTASENTENCIAS** → **SENTENCIA** **LISTASENTENCIAS** | ε

**SENTENCIA** → **SENTENCIAEXPR**
| **SENTENCIASEL**
| **SENTENCIAITER**
| **SENTENCIARET**
| **SENTENCIAPRINT**
| **BLOQUE**
| **DECLLOCAL**

**DECLLOCAL** → **TIPO** ``id`` **DECLLOCAL'** ``puntoycoma``
**DECLLOCAL'** → ``asignacion`` **EXPR** **DECLLOCAL''** | **DECLLOCAL''**
**DECLLOCAL''** → ``coma`` ``id`` **DECLLOCAL'** | ε

**SENTENCIAEXPR** → **ASIGNACION** ``puntoycoma`` | ``puntoycoma``

**ASIGNACION** → ``id`` ``asignacion`` **EXPR** | **EXPR**

**SENTENCIASEL** → ``if`` ``lparen`` **EXPR** ``rparen`` **SENTENCIA** **SENTENCIASEL'**

**SENTENCIASEL'** → ``else`` **SENTENCIA** | ε

**SENTENCIAITER** → ``while`` ``lparen`` **EXPR** ``rparen`` **SENTENCIA**
 | ``for`` ``lparen`` **EXPR** ``puntoycoma`` **EXPR** ``puntoycoma`` **EXPR** ``rparen`` **SENTENCIA**

**SENTENCIARET** → ``return`` **EXPR** ``puntoycoma``

**SENTENCIAPRINT** → ``print`` ``lparen`` **EXPR** ``rparen`` ``puntoycoma``

**EXPR** → **EXPRAND** **EXPR'**

**EXPR'** → ``op_or`` **EXPRAND** **EXPR'** | ε

**EXPRAND** → **EXPREQ** **EXPRAND'**

**EXPRAND'** → ``op_and`` **EXPREQ** **EXPRAND'** | ε

**EXPREQ** → **EXPRREL** **EXPREQ'**

**EXPREQ'** → (``op_eq`` | ``op_neq``) **EXPRREL** **EXPR'** | ε

**EXPRREL** → **EXPRADIT** **EXPRREL'**

**EXPRREL'** → (``op_lt`` | ``op_gt`` | ``op_le`` | ``op_ge``) **EXPRADIT** | ε

**EXPRADIT** → **TERM** **EXPRADIT'**

**EXPRADIT'** → (``op_suma`` | ``op_resta``) **TERM** **EXPRADIT'** | ε

**TERM** → **FACTOR** **TERM'**

**TERM'** → (``op_mul`` | ``op_div`` | ``op_mod``) **FACTOR** **TERM'** | ε

**FACTOR** → ``lparen`` **EXPR** ``rparen``
 | ``num``
 | ``op_not`` **FACTOR**
 | ``id`` **FACTOR'**

**FACTOR'** → ``lparen`` **ARGLIST** ``rparen`` | ``lparen`` ``rparen`` | ε

**ARGLIST** → **EXPR** **ARGLIST'**

**ARGLIST'** → ``coma`` **ARGLIST** | ε