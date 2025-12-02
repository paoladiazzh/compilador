import sys
import os

current_dir = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(current_dir, 'lexer'))
sys.path.insert(0, os.path.join(current_dir, 'parser'))
sys.path.insert(0, os.path.join(current_dir, 'semantic'))

from lexer import Lexer, LexerError
from parser_ast import ParserAST
from semantic_analyzer import SemanticAnalyzer, SemanticError


def print_separator(title="", char="-"):
    width = 80
    if title:
        padding = (width - len(title) - 2) // 2
        print(f"\n{char * padding} {title} {char * padding}")
    else:
        print(char * width)


def compile_file(filepath, verbose=False):
    """Ejecuta el proceso de compilación completo"""

    try:
        with open(filepath, "r", encoding="utf-8") as f:
            source_code = f.read()

        print(f"Archivo: {filepath}")
        print(f"Tamaño: {len(source_code)} caracteres\n")

        # --- FASE 1: ANÁLISIS LÉXICO ---
        print_separator("FASE 1: ANÁLISIS LÉXICO")

        lexer = Lexer()
        tokens = lexer.tokenize(source_code)

        print("Análisis léxico completado")
        print(f"Tokens generados: {len(tokens)}")

        if verbose:
            print("\nPrimeros 10 tokens:")
            for i, token in enumerate(tokens[:10]):
                print(f"  {i+1}. <{token[0]}, \"{token[1]}\">")
            if len(tokens) > 10:
                print(f"  ... y {len(tokens) - 10} más")

        # --- FASE 2: ANÁLISIS SINTÁCTICO ---
        print_separator("FASE 2: ANÁLISIS SINTÁCTICO")

        parser = ParserAST(tokens)
        ast = parser.parse()

        if not ast:
            print("Error en el análisis sintáctico")
            return False

        print("Análisis sintáctico completado")
        print("AST generado correctamente")

        if verbose:
            print("\nEstructura del AST:")
            print(f"  {ast}")
            print(f"  Declaraciones: {len(ast.declarations)}")

        # --- FASE 3: ANÁLISIS SEMÁNTICO ---
        print_separator("FASE 3: ANÁLISIS SEMÁNTICO")

        analyzer = SemanticAnalyzer()
        success = analyzer.analyze(ast)

        print("\nTABLA DE SÍMBOLOS\n")
        print(analyzer.symbol_table.get_table_representation())

        if success:
            print("\nAnálisis semántico completado sin errores")
            print_separator("COMPILACIÓN EXITOSA", "-")
            print("El programa pasó todas las fases correctamente")
            return True
        else:
            print("\n" + analyzer.get_errors_report())
            print_separator("COMPILACIÓN FALLIDA", "-")
            print(f"Errores semánticos: {len(analyzer.errors)}")
            return False

    except LexerError as e:
        print_separator("ERROR LÉXICO", "-")
        print(str(e))
        return False

    except FileNotFoundError:
        print_separator("ERROR DE ARCHIVO", "-")
        print(f"No se encontró el archivo: {filepath}")
        return False

    except Exception as e:
        print_separator("ERROR INESPERADO", "-")
        print(str(e))
        import traceback
        traceback.print_exc()
        return False


def main():
    if len(sys.argv) < 2:
        print("Uso: python compile.py <archivo.src> [--verbose]")
        sys.exit(1)

    filepath = sys.argv[1]
    verbose = "--verbose" in sys.argv or "-v" in sys.argv

    success = compile_file(filepath, verbose)
    sys.exit(0 if success else 1)


if __name__ == "__main__":
    main()
