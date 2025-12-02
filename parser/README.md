# Parser - Analizador Sintáctico

## Descripción

Este parser implementa un **analizador sintáctico descendente recursivo predictivo LL(1) estricto** para el lenguaje. El parser valida que la estructura del código fuente cumpla con la gramática formal del lenguaje 

## Características

- **LL(1) Estricto**: Solo usa el token actual
- **Sin backtracking**: Cada decisión se toma de forma determinista
- **Análisis predictivo**: Utiliza los conjuntos FIRST y FOLLOW para determinar qué producción aplicar
- **Descendente recursivo**: Cada no-terminal de la gramática se implementa como un método en Python
- **Integración con el Lexer**: Consume los tokens generados por el analizador léxico
- **Soporte completo del lenguaje**:
  - Declaraciones globales de variables y funciones
  - **Declaraciones locales** dentro de bloques con inicialización opcional
  - Tipos de datos: `int`, `float`, `void`
  - Estructuras de control: `if`, `else`, `while`, `for`
  - Operadores aritméticos, relacionales y lógicos
  - Llamadas a funciones con argumentos
  - Sentencias de retorno e impresión
  - **Asignaciones** integradas en expresiones

## Gramática LL(1) Implementada

El parser implementa la gramática LL(1) actualizada definida en [`specs/grammar_spec.md`](../specs/grammar_spec.md).

## First and Follow

Ver análisis completo en [`specs/first_and_follow_spec.md`](../specs/first_and_follow_spec.md)

### Ejemplos

#### Caso de éxito 1: Función recursiva

Ejecutar:
```bash
python parser_ast.py sample_1.src
```

#### Caso de éxito 2: Programa completo

Ejecutar:
```bash
python parser_ast.py sample_2.src
```

#### Caso de falla 1: Falta punto y coma

Ejecutar:
```bash
python parser_ast.py sample_3.src
```

#### Caso de falla 2: Paréntesis sin cerrar

Ejecutar:
```bash
python parser_ast.py sample_4.src
```


## Manejo de Errores

El parser detecta y reporta errores sintácticos específicos:

- **Tokens inesperados**: Cuando encuentra un token que no es válido en esa posición
- **Tokens faltantes**: Cuando se espera un token específico (paréntesis, punto y coma, etc.)
- **Estructura incorrecta**: Cuando la secuencia de tokens no cumple con la gramática

Los errores se reportan con mensajes descriptivos que indican:
- Qué token se esperaba
- Qué token se encontró
- La ubicación implícita en el flujo de tokens

## Algoritmo de Análisis LL(1)

El parser utiliza el método de **análisis sintáctico descendente recursivo predictivo**:

1. **Inicio**: Comienza desde el símbolo inicial `S`
2. **Decisión determinista**: Para cada no-terminal, usa **solo el token actual** y la tabla predictiva para decidir qué producción aplicar
3. **Sin lookahead adicional**: No necesita ver más allá del token actual (k=1)
4. **Recursión**: Procesa los no-terminales llamando a sus métodos correspondientes
5. **Consumo**: Los terminales se consumen verificando que coincidan con el token actual
6. **Éxito**: Si se consumen todos los tokens y se llega a EOF, el análisis es exitoso
7. **Fallo**: Si en cualquier punto no se puede continuar, se reporta un error inmediatamente

## AST implementacion

### Construcción del AST (Abstract Syntax Tree)

El parser ha sido extendido para construir un árbol de sintaxis abstracta que representa la estructura del programa de manera jerárquica. Cada nodo del AST corresponde a una construcción del lenguaje:

- **Nodos de Programa**: `ProgramNode`
- **Nodos de Declaración**: `VarDeclNode`, `FuncDeclNode`, `ParamNode`
- **Nodos de Sentencias**: `BlockNode`, `IfNode`, `WhileNode`, `ForNode`, `ReturnNode`, `PrintNode`, `ExprStmtNode`
- **Nodos de Expresiones**: `BinaryOpNode`, `UnaryOpNode`, `AssignNode`, `VarNode`, `NumNode`, `FuncCallNode`

## Referencias

- [Especificación de la Gramática LL(1)](../specs/grammar_spec.md)
- [Definición de Tokens](../specs/tokens_spec.md)
- [Conjuntos FIRST y FOLLOW](../specs/first_and_follow_spec.md)
- [Documentación del Lexer](../lexer/README.md)
- [Documentación del Analizador Semántico](../semantic/README.md)
