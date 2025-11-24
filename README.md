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

### 3. **Especificaciones del Lenguaje**
- Ubicación: `specs/`
- **Gramática formal:** [grammar_spec.md](specs/grammar_spec.md)
- **Definición de tokens:** [tokens_spec.md](specs/tokens_spec.md)

---

## Requisitos

- **Python 3.7+**
- No se requieren dependencias externas