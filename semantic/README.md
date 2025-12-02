# Analizador Semántico para miniC

## Descripción

El analizador semántico es la tercera fase del compilador miniC. Recibe el **Abstract Syntax Tree (AST)** generado por el parser y realiza validaciones semánticas sobre el código fuente, asegurando que cumpla con las reglas del lenguaje más allá de la sintaxis.

## Características Principales

### 1. Tabla de Símbolos

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

### 2. Validaciones Semánticas Implementadas

####  Validación 1: Declaración antes de uso
####  Validación 2: Tipos compatibles en operaciones

Validaciones de tipos en operaciones:
- **Aritméticas** (`+`, `-`, `*`, `/`, `%`): Requieren operandos numéricos
- **Relacionales** (`<`, `>`, `<=`, `>=`, `==`, `!=`): Requieren operandos numéricos, retornan bool
- **Lógicas** (`&&`, `||`, `!`): Retornan bool

####  Validación 3: Número y tipo de parámetros en funciones
####  Validación 4: Ciclos y condicionales con expresiones válidas
####  Validación 5: Tipo de retorno de funciones

### semantic_analyzer.py

Implementa el analizador semántico:
- **SymbolTable**: Maneja la tabla de símbolos con múltiples ámbitos
- **SemanticAnalyzer**: Recorre el AST realizando validaciones

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
