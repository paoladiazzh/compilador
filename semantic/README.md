# Analizador Semántico para miniC

## Descripción

El analizador semántico es la tercera fase del compilador miniC. Recibe el **Abstract Syntax Tree (AST)** generado por el parser y realiza validaciones semánticas sobre el código fuente, asegurando que cumpla con las reglas del lenguaje más allá de la sintaxis.

## Características Principales

### 1. Construcción del AST (Abstract Syntax Tree)

El parser ha sido extendido para construir un árbol de sintaxis abstracta que representa la estructura del programa de manera jerárquica. Cada nodo del AST corresponde a una construcción del lenguaje:

- **Nodos de Programa**: `ProgramNode`
- **Nodos de Declaración**: `VarDeclNode`, `FuncDeclNode`, `ParamNode`
- **Nodos de Sentencias**: `BlockNode`, `IfNode`, `WhileNode`, `ForNode`, `ReturnNode`, `PrintNode`, `ExprStmtNode`
- **Nodos de Expresiones**: `BinaryOpNode`, `UnaryOpNode`, `AssignNode`, `VarNode`, `NumNode`, `FuncCallNode`

### 2. Tabla de Símbolos

El analizador mantiene una **tabla de símbolos** con soporte para múltiples ámbitos (scopes):

- **Ámbito global**: Variables y funciones globales
- **Ámbitos locales**: Variables locales dentro de funciones y bloques
- **Stack de ámbitos**: Implementa reglas de alcance léxico (lexical scoping)

La tabla de símbolos almacena:
- Nombre del símbolo
- Tipo de dato (`int`, `float`, `void`)
- Ámbito en el que está declarado

Para funciones, almacena adicionalmente:
- Tipo de retorno
- Lista de tipos de parámetros

### 3. Validaciones Semánticas Implementadas

#### ✓ Validación 1: Declaración antes de uso
```c
// ERROR: variable no declarada
int main() {
    x = 10;  // Error: 'x' no está declarada
}

// CORRECTO
int main() {
    int x;
    x = 10;  // OK
}
```

#### ✓ Validación 2: Tipos compatibles en operaciones
```c
// ERROR: tipos incompatibles
int main() {
    int x = 5;
    int y;
    y = 3.14;  // Error: asignación de float a int sin conversión explícita
}

// CORRECTO: promoción implícita int -> float permitida
float main() {
    int x = 5;
    float y;
    y = x;  // OK: promoción implícita
}
```

Validaciones de tipos en operaciones:
- **Aritméticas** (`+`, `-`, `*`, `/`, `%`): Requieren operandos numéricos
- **Relacionales** (`<`, `>`, `<=`, `>=`, `==`, `!=`): Requieren operandos numéricos, retornan bool
- **Lógicas** (`&&`, `||`, `!`): Retornan bool

#### ✓ Validación 3: Número y tipo de parámetros en funciones
```c
// ERROR: número incorrecto de argumentos
int suma(int a, int b) {
    return a + b;
}

int main() {
    int x = suma(5);  // Error: se esperaban 2 argumentos, se encontró 1
}

// ERROR: tipo de argumento incompatible
float promedio(float a, float b) {
    return (a + b) / 2.0;
}

int main() {
    float x = promedio(5, 10);  // OK: promoción int -> float
    float y = promedio("texto", 10);  // Error: tipo incompatible
}
```

#### ✓ Validación 4: Ciclos y condicionales con expresiones válidas
```c
// Validación de condiciones en if
if (x > 5) {  // OK: expresión relacional
    print(x);
}

// Validación de condiciones en while
while (contador < 10) {  // OK
    contador = contador + 1;
}

// Validación de condiciones en for
for (i = 0; i < 10; i = i + 1) {  // OK
    print(i);
}
```

#### ✓ Validación 5: Tipo de retorno de funciones
```c
// ERROR: tipo de retorno incompatible
int suma(int a, int b) {
    return 3.14;  // Error: se esperaba 'int', se encontró 'float'
}

// CORRECTO
float promedio(int a, int b) {
    return (a + b) / 2.0;  // OK: retorna float
}
```

## Estructura del Código

```
semantic/
├── ast_nodes.py           # Definición de nodos del AST
├── parser_ast.py          # Parser extendido con construcción de AST
├── semantic_analyzer.py   # Analizador semántico
└── README.md             # Esta documentación
```

### ast_nodes.py

Define las clases de nodos del AST:
```python
class ASTNode:              # Clase base
class ProgramNode:          # Programa completo
class VarDeclNode:          # Declaración de variable
class FuncDeclNode:         # Declaración de función
class BinaryOpNode:         # Operación binaria (x + y)
class AssignNode:           # Asignación (x = expr)
# ... más nodos
```

### parser_ast.py

Parser que construye el AST mientras analiza sintácticamente:
- Extiende el parser original (`parser/parser.py`)
- Cada método de parsing retorna un nodo del AST
- Mantiene compatibilidad con la gramática LL(1)

### semantic_analyzer.py

Implementa el analizador semántico:
- **SymbolTable**: Maneja la tabla de símbolos con múltiples ámbitos
- **SemanticAnalyzer**: Recorre el AST realizando validaciones

## Uso

### Análisis completo (Léxico + Sintáctico + Semántico)

```bash
python semantic/semantic_analyzer.py 
```

### Ejemplo de ejecución exitosa

Archivo: `semantic/test_success.src`
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

Salida:
```
=== Análisis Léxico Exitoso ===
Tokens generados: 62

=== AST Construido Exitosamente ===

=== Iniciando Análisis Semántico ===

================================================================================
TABLA DE SÍMBOLOS
================================================================================

--- Variables Globales ---
(ninguna)

--- Funciones ---
Nombre               Tipo Retorno    Parámetros                    
-----------------------------------------------------------------
factorial            int             int
main                 int             (sin parámetros)

================================================================================

✓ No se encontraron errores semánticos

✓ Análisis semántico completado exitosamente!
```

### Ejemplo con errores semánticos

Archivo: `semantic/test_errors.src`
```c
int main() {
    int x = 10;
    y = x + 5;           // Error: 'y' no declarada
    x = 3.14;            // Error: tipo incompatible
    int z = suma(5, 3);  // Error: función 'suma' no declarada
    return 0;
}
```

Salida:
```
=== Análisis Léxico Exitoso ===
Tokens generados: 28

=== AST Construido Exitosamente ===

=== Iniciando Análisis Semántico ===

================================================================================
TABLA DE SÍMBOLOS
================================================================================

--- Variables Globales ---
(ninguna)

--- Funciones ---
Nombre               Tipo Retorno    Parámetros                    
-----------------------------------------------------------------
main                 int             (sin parámetros)

================================================================================

================================================================================
ERRORES SEMÁNTICOS ENCONTRADOS
================================================================================
1. Variable 'y' no está declarada
2. Asignación de tipo incompatible a 'x': se esperaba 'int', se encontró 'float'
3. Función 'suma' no está declarada
================================================================================

✗ Análisis semántico falló
```

## Casos de Prueba

### Caso 1: Declaración antes de uso ✓
```c
int main() {
    int x;
    x = 10;        // OK
    int y = x + 5; // OK
}
```

### Caso 2: Variable no declarada ✗
```c
int main() {
    x = 10;  // Error: 'x' no declarada
}
```

### Caso 3: Compatibilidad de tipos ✓
```c
int main() {
    int x = 5;
    float y = x;  // OK: promoción int -> float
}
```

### Caso 4: Tipo incompatible ✗
```c
int main() {
    int x;
    x = 3.14;  // Error: float no asignable a int sin conversión explícita
}
```

### Caso 5: Llamada a función correcta ✓
```c
int suma(int a, int b) {
    return a + b;
}

int main() {
    int resultado = suma(5, 10);  // OK
}
```

### Caso 6: Argumentos incorrectos ✗
```c
int suma(int a, int b) {
    return a + b;
}

int main() {
    int x = suma(5);  // Error: número incorrecto de argumentos
}
```

### Caso 7: Expresiones en condicionales ✓
```c
int main() {
    int x = 5;
    if (x > 0) {      // OK: expresión relacional
        print(x);
    }
    while (x < 10) {  // OK
        x = x + 1;
    }
}
```

### Caso 8: Tipo de retorno ✗
```c
int suma(int a, int b) {
    return 3.14;  // Error: tipo de retorno incompatible
}
```

## Algoritmo del Análisis Semántico

1. **Inicialización**: Crear tabla de símbolos con ámbito global
2. **Primera pasada**: Registrar todas las declaraciones globales (funciones)
3. **Segunda pasada**: Para cada función:
   - Crear nuevo ámbito local
   - Registrar parámetros en la tabla
   - Recorrer el cuerpo de la función
   - Validar variables, tipos y expresiones
   - Validar retornos
   - Salir del ámbito local
4. **Validación de expresiones**: Para cada nodo:
   - Verificar que variables estén declaradas
   - Verificar compatibilidad de tipos
   - Inferir tipo resultante
5. **Reporte de errores**: Acumular todos los errores encontrados

## Representación Tabular del AST

El AST se puede visualizar en forma de tabla para depuración:

```
Program
├── FuncDecl: int factorial(int n)
│   └── Block
│       └── If
│           ├── Condition: BinaryOp(n <= 1)
│           ├── Then: Return(1)
│           └── Else: Return(BinaryOp(n * FuncCall(factorial)))
└── FuncDecl: int main()
    └── Block
        ├── VarDecl: int num = 5
        ├── VarDecl: int resultado
        ├── ExprStmt: Assign(resultado = FuncCall(factorial))
        ├── Print(resultado)
        └── Return(0)
```

## Limitaciones Actuales

- No se realiza análisis de flujo de control (código muerto, alcanzabilidad)
- No se detectan variables no utilizadas
- No hay optimización de expresiones constantes
- La conversión de tipos es limitada (solo int -> float implícito)
- No se valida que todas las rutas de una función no-void retornen un valor

## Próximos Pasos

Para completar el compilador:
1. **Generación de código intermedio** (TAC - Three Address Code)
2. **Optimización** (eliminación de subexpresiones comunes, propagación de constantes)
3. **Generación de código objeto** (ensamblador o bytecode)

## Integración con el Pipeline del Compilador

```
Código fuente (.src)
        ↓
    [LEXER]
        ↓
    Tokens
        ↓
    [PARSER]
        ↓
      AST
        ↓
[SEMANTIC ANALYZER]
        ↓
AST validado + Tabla de símbolos
        ↓
(Generación de código)
```

## Referencias

- [Especificación de la Gramática](../specs/grammar_spec.md)
- [Definición de Tokens](../specs/tokens_spec.md)
- [Documentación del Lexer](../lexer/README.md)
- [Documentación del Parser](../parser/README.md)

---

**Nota académica**: Este analizador semántico implementa las validaciones fundamentales requeridas para un compilador básico. Las validaciones cubren los aspectos más críticos del análisis semántico: declaración de variables, compatibilidad de tipos, y correctitud de llamadas a funciones.