# Parser - Analizador Sintáctico LL(1)

## Descripción

Este parser implementa un **analizador sintáctico descendente recursivo predictivo LL(1) estricto** para el lenguaje miniC. El parser valida que la estructura del código fuente cumpla con la gramática formal del lenguaje sin requerir lookahead adicional (k>1).

## Características

- **LL(1) Estricto**: No requiere lookahead adicional - solo usa el token actual
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

### Cambios principales respecto a la versión anterior:

1. **DECLLOCAL** - Nueva producción para declaraciones locales:
   ```
   DECLLOCAL → TIPO id DECLLOCAL' puntoycoma
   DECLLOCAL' → asignacion EXPR DECLLOCAL'' | DECLLOCAL''
   DECLLOCAL'' → coma id DECLLOCAL' | ε
   ```
   
   Permite:
   - `int x;`
   - `int x = 5;`
   - `int x = 5, y, z = 10;`

2. **FACTOR'** - Asignación integrada:
   ```
   FACTOR' → asignacion EXPR | lparen ARGLIST rparen | lparen rparen | ε
   ```
   
   Esto elimina la ambigüedad permitiendo distinguir:
   - `x = 5` (asignación)
   - `x + 5` (expresión)
   - `funcion()` (llamada)

3. **SENTENCIA** - Incluye DECLLOCAL:
   ```
   SENTENCIA → DECLLOCAL | SENTENCIAEXPR | SENTENCIASEL | ...
   ```

### Propiedades LL(1)

✓ **Conjuntos FIRST disjuntos** - No hay conflictos al decidir producciones  
✓ **Condiciones ε correctas** - FIRST no se solapa con FOLLOW  
✓ **Tabla predictiva sin conflictos** - Cada celda tiene máximo una producción  
✓ **Determinismo completo** - No requiere backtracking  

Ver análisis completo en [`specs/first_and_follow_spec.md`](../specs/first_and_follow_spec.md)

## Estructura del Código

```
Parser (LL(1) Estricto)
├── __init__()          # Inicializa con tokens
├── advance()           # Avanza al siguiente token
├── match()             # Verifica y consume un token
├── expect()            # Verifica un token esperado (lanza error si falla)
│
├── parse()             # S → bof PROGRAMA eof
├── programa()          # PROGRAMA → LISTADECL
│
├── Declaraciones Globales
│   ├── listadecl()     # LISTADECL → DECL LISTADECL | ε
│   ├── decl()          # DECL → TIPO DECL'
│   ├── tipo()          # TIPO → int | float | void
│   └── parametros()    # Parámetros de funciones
│
├── Declaraciones Locales (NUEVO)
│   ├── decllocal()          # DECLLOCAL → TIPO id DECLLOCAL' puntoycoma
│   ├── decllocal_prima()    # Con/sin inicialización
│   └── decllocal_dobleprima() # Múltiples variables
│
├── Sentencias
│   ├── sentencia()         # Decisión basada en FIRST
│   ├── sentenciaexpr()     # EXPR puntoycoma | puntoycoma
│   ├── sentenciasel()      # if-else
│   ├── sentenciaiter()     # while, for
│   ├── sentenciaret()      # return
│   └── sentenciaprint()    # print
│
└── Expresiones
    ├── expr()              # Expresiones lógicas OR
    ├── exprand()           # Expresiones lógicas AND
    ├── expreq()            # Expresiones de igualdad
    ├── exprrel()           # Expresiones relacionales
    ├── expradit()          # Expresiones aditivas
    ├── term()              # Términos multiplicativos
    ├── factor()            # Factores (números, IDs, llamadas)
    └── factor_prima()      # Asignación, llamadas, o ε (NUEVO)
```

## Uso

### Requisitos previos

El parser requiere el analizador léxico del proyecto:

```
proyecto/
├── lexer/
│   └── lexer.py
└── parser/
    ├── parser.py
    └── README.md
```

### Ejecutar el parser

```bash
python parser.py <archivo_fuente.src>
```

### Ejemplos

#### Caso de éxito 1: Función recursiva

Archivo: `test_success1.src`
```c
int factorial(int n) {
    if (n <= 1) {
        return 1;
    } else {
        return n * factorial(n - 1);
    }
}

int main() {
    int num = 5;
    int resultado;
    resultado = factorial(num);
    print(resultado);
    return 0;
}
```

Ejecutar:
```bash
python parser.py test_success1.src
```

Salida esperada:
```
=== Análisis Léxico Exitoso ===
Tokens generados: 62

=== Iniciando Análisis Sintáctico (LL(1) Estricto) ===
✓ Parsing completed successfully!
```

#### Caso de éxito 2: Programa completo

Archivo: `test_success2.src`
```c
float calcular_promedio(int a, int b, int c) {
    float suma, promedio;
    suma = a + b + c;
    promedio = suma / 3.0;
    return promedio;
}

int main() {
    int x = 10, y = 20, z = 30;  
    float prom;
    int contador = 0;
    
    while (contador < 10 && x != 0) {
        contador = contador + 1;
        x = x - 1;
        if (contador >= 5 || y > 15) {
            print(contador);
        }
    }
    
    for (contador = 0; contador < 5; contador = contador + 1) {
        if (contador % 2 == 0) {
            print(contador);
        } else {
            y = y + contador;
        }
    }
    
    prom = calcular_promedio(x, y, z);
    print(prom);
    
    if ((x >= 0 && y <= 100) || z != 0) {
        print(x + y * z - 10);
    }
    
    return 0;
}
```

#### Caso de falla 1: Falta punto y coma

Archivo: `test_failure1.src`
```c
void main() {
    int x = 10
    int y = 20;
    print(x + y);
}
```

Salida esperada:
```
=== Análisis Léxico Exitoso ===
Tokens generados: 20

=== Iniciando Análisis Sintáctico (LL(1) Estricto) ===
Error de sintaxis: Se esperaba PUNTOYCOMA, se encontró INT
✗ Parsing failed
```

#### Caso de falla 2: Paréntesis sin cerrar

Archivo: `test_failure2.src`
```c
int suma(int a, int b) {
    return a + b;
}

void main() {
    int x = 5;
    int y = 10;
    
    if (x < y {
        print(suma(x, y));
    }
}
```

Salida esperada:
```
=== Análisis Léxico Exitoso ===
Tokens generados: 41

=== Iniciando Análisis Sintáctico (LL(1) Estricto) ===
Error de sintaxis: Se esperaba RPAREN, se encontró LBRACE
✗ Parsing failed
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

### Ejemplo de decisión LL(1) en SENTENCIA:

```python
def sentencia(self):
    token = self.current_type()
    
    if token in ["INT", "FLOAT", "VOID"]:
        self.decllocal()           # FIRST(DECLLOCAL)
    elif token == "IF":
        self.sentenciasel()        # FIRST(SENTENCIASEL)
    elif token in ["WHILE", "FOR"]:
        self.sentenciaiter()       # FIRST(SENTENCIAITER)
    elif token == "RETURN":
        self.sentenciaret()        # FIRST(SENTENCIARET)
    elif token == "PRINT":
        self.sentenciaprint()      # FIRST(SENTENCIAPRINT)
    elif token == "LBRACE":
        self.bloque()              # FIRST(BLOQUE)
    else:
        self.sentenciaexpr()       # FIRST(SENTENCIAEXPR)
```

Cada decisión se toma **únicamente con el token actual**, sin necesidad de lookahead adicional.

## Características de Declaraciones Locales

La gramática ahora soporta:

### Declaración simple:
```c
int x;
float y;
```

### Declaración con inicialización:
```c
int x = 10;
float pi = 3.14;
```

### Declaración múltiple:
```c
int x = 5, y, z = 10;
float a = 1.0, b = 2.0;
```

Todas estas formas se parsean con la regla **DECLLOCAL** sin ambigüedad.

## Características de Asignación

La asignación ahora está integrada en **FACTOR'**:

```c
x = 5;              // Asignación simple
x = y = z = 0;      // Asignación múltiple (anidada)
x = funcion();      // Asignación desde llamada
a = b + c * d;      // Asignación con expresión
```

La decisión es LL(1) porque:
- Si después de `id` viene `asignacion`, es una asignación
- Si viene cualquier otro token, es solo un identificador en una expresión

## Limitaciones Actuales

- El parser realiza **análisis sintáctico puro** (no genera código ni construye árbol de sintaxis)
- No realiza análisis semántico (validación de tipos, alcance de variables, etc.)
- Los errores se reportan en el primer problema encontrado (no hay recuperación de errores)

## Próximos Pasos

Para completar el compilador:
1. **Construcción de AST** (Árbol de Sintaxis Abstracta)
2. **Análisis semántico** (tabla de símbolos, chequeo de tipos)
3. **Generación de código intermedio**
4. **Optimización**
5. **Generación de código objeto**

## Validación LL(1)

La gramática ha sido verificada para cumplir con las condiciones LL(1):

✓ **FIRST(α) ∩ FIRST(β) = ∅** para todas las alternativas  
✓ **Si ε ∈ FIRST(α), entonces FIRST(β) ∩ FOLLOW(A) = ∅**  
✓ **Tabla predictiva sin conflictos**  
✓ **No requiere backtracking**  

Ver análisis completo en la documentación de FIRST y FOLLOW.

## Referencias

- [Especificación de la Gramática LL(1)](../specs/grammar_spec.md)
- [Definición de Tokens](../specs/tokens_spec.md)
- [Conjuntos FIRST y FOLLOW](../specs/first_and_follow_spec.md)
- [Documentación del Lexer](../lexer/README.md)

---

**Nota académica**: Este parser es **LL(1) estricto** y no utiliza lookahead adicional (peek) ni backtracking. Todas las decisiones se toman de forma determinista basándose únicamente en el token actual y los conjuntos FIRST/FOLLOW de la gramática.
