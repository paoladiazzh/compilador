## Contenido del Proyecto

### 1. **Analizador Léxico (Lexer)**
- Ubicación: `lexer/`
- Reconoce tokens del lenguaje mediante Autómatas Finitos Deterministas (AFD)
- Soporta palabras clave, identificadores, números, operadores y delimitadores
- Maneja comentarios de línea (`//`, `#`) y de bloque (`/* */`)

**Características principales:**
- Implementación basada en AFD para eficiencia
- Validación de lexemas
- Manejo robusto de errores léxicos

**Ver documentación completa:** [lexer/README.md](lexer/README.md)

### 2. **Analizador Sintáctico (Parser)**
- Ubicación: `parser/`
- Implementación de análisis sintáctico descendente recursivo
- Valida la estructura gramatical de expresiones
- Soporta operadores aritméticos, identificadores, números y delimitadores

**Ver documentación completa:** [parser/README.md](parser/README.md)

### 3. **Analizador Semántico**
- Ubicación: `semantic/`
- Realiza un recorrido del AST para validar reglas semánticas del lenguaje
- Utiliza una tabla de símbolos con manejo de ámbitos (scopes)
- Verifica la correcta declaración y uso de variables y funciones
- Comprueba la compatibilidad de tipos en expresiones, asignaciones y retornos
- Valida llamadas a funciones, cantidad de argumentos y tipos esperados

**Características principales:**
- Tabla de símbolos jerárquica que registra variables, parámetros y funciones
- Validación de tipos en operadores aritméticos, lógicos y relacionales
- Detección de errores como variables no declaradas, duplicaciones o tipos incompatibles
- Reporte detallado de errores semánticos
- Representación clara de la tabla de símbolos generada durante el análisis
- Incluye casos de prueba que demuestran funcionamiento correcto y manejo de errores

**Ver documentación completa:** [semantic/semantic_analyzer.py](semantic/semantic_analyzer.py)


### 4. **Especificaciones del Lenguaje**
- Ubicación: `specs/`
- **Gramática formal:** [grammar_spec.md](specs/grammar_spec.md)
- **Definición de tokens:** [tokens_spec.md](specs/tokens_spec.md)

---

## Requisitos

- **Python 3.7+**
- No se requieren dependencias externas