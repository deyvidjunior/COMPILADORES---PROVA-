from typing import Dict, List, Optional
import os

class MEPAInterpreter:
    def __init__(self):
        self.memory: List[int] = []
        self.stack: List[int] = []
        self.code: Dict[int, str] = {}
        self.current_file: str = ""
        self.debug_mode: bool = False
        self.program_counter: int = 0
        self.modified: bool = False
        self.labels: Dict[str, int] = {}

    def execute_instruction(self, instruction: str) -> bool:
        parts = instruction.split()
        op = parts[0].upper()

        try:
            if op == "INPP":
                self.stack = []
                self.memory = []
            elif op == "AMEM":
                m = int(parts[1])
                self.memory.extend([0] * m)
            elif op == "DMEM":
                m = int(parts[1])
                self.memory = self.memory[:-m]
            elif op == "CRCT":
                k = int(parts[1])
                self.stack.append(k)
            elif op == "CRVL":
                n = int(parts[1])
                self.stack.append(self.memory[n])
            elif op == "ARMZ":
                n = int(parts[1])
                if n >= len(self.memory):
                    self.memory.extend([0] * (n - len(self.memory) + 1))
                self.memory[n] = self.stack.pop()
            elif op in ["SOMA", "SUBT", "MULT", "DIVI"]:
                b = self.stack.pop()
                a = self.stack.pop()
                if op == "SOMA": self.stack.append(a + b)
                elif op == "SUBT": self.stack.append(a - b)
                elif op == "MULT": self.stack.append(a * b)
                elif op == "DIVI": self.stack.append(a // b)
            elif op == "INVR":
                self.stack[-1] = -self.stack[-1]
            elif op == "IMPR":
                print(self.stack.pop())
            elif op == "PARA":
                return False
            elif op == "NADA":
                pass
            else:
                print(f"Instrucción no reconocida: {op}")
                return False
            return True
        except Exception as e:
            print(f"Error ejecutando {instruction}: {str(e)}")
            return False

    def load_file(self, filename: str) -> None:
        if self.modified:
            resp = input("¿Hay cambios sin guardar. ¿Desea guardar? (S/N): ")
            if resp.upper() == 'S':
                self.save_file()

        try:
            with open(filename, 'r') as file:
                self.code.clear()
                self.labels.clear()
                for line in file:
                    line = line.split('#')[0].strip()  # Eliminar comentarios
                    if line:
                        parts = line.split(maxsplit=1)
                        num = int(parts[0])
                        if len(parts) > 1:
                            instruction = parts[1]
                            if instruction.endswith(':'):
                                self.labels[instruction[:-1]] = num
                            self.code[num] = instruction
            self.current_file = filename
            self.modified = False
            print(f"Archivo '{filename}' cargado con éxito.")
        except FileNotFoundError:
            print(f"Error: No se encontró el archivo '{filename}'")

    def save_file(self) -> None:
        if not self.current_file:
            print("No hay archivo abierto para guardar")
            return

        try:
            with open(self.current_file, 'w') as file:
                for line_num in sorted(self.code.keys()):
                    file.write(f"{line_num} {self.code[line_num]}\n")
            self.modified = False
            print(f"Archivo guardado: {self.current_file}")
        except Exception as e:
            print(f"Error al guardar: {str(e)}")

    def list_code(self) -> None:
        if not self.code:
            print("No hay código cargado")
            return

        lines = sorted(self.code.keys())
        for i in range(0, len(lines), 20):
            chunk = lines[i:i+20]
            for line_num in chunk:
                print(f"{line_num} {self.code[line_num]}")
            
            if i + 20 < len(lines):
                input("Presione Enter para continuar...")

    def insert_line(self, line_num: int, instruction: str) -> None:
        if line_num < 0:
            print("El número de línea no puede ser negativo")
            return

        self.code[line_num] = instruction
        self.modified = True
        print(f"Línea insertada: {line_num} {instruction}")

    def delete_line(self, start: int, end: Optional[int] = None) -> None:
        if end is None:
            end = start

        deleted = []
        for line_num in range(start, end + 1):
            if line_num in self.code:
                deleted.append(f"{line_num} {self.code[line_num]}")
                del self.code[line_num]
                self.modified = True

        if deleted:
            print("Líneas eliminadas:")
            for line in deleted:
                print(line)
        else:
            print("No se encontraron líneas para eliminar")

    def run(self) -> None:
        if not self.code:
            print("No hay código para ejecutar")
            return

        self.program_counter = min(self.code.keys())
        self.stack = []
        self.memory = []

        while self.program_counter in self.code:
            instruction = self.code[self.program_counter]
            if not self.execute_instruction(instruction):
                break
            self.program_counter = next((k for k in sorted(self.code.keys()) 
                                       if k > self.program_counter), -1)

    def debug_next(self) -> None:
        if not self.debug_mode:
            print("No está en modo depuración")
            return

        if self.program_counter in self.code:
            instruction = self.code[self.program_counter]
            print(f"{self.program_counter} {instruction}")
            if self.execute_instruction(instruction):
                self.program_counter = next((k for k in sorted(self.code.keys()) 
                                           if k > self.program_counter), -1)
            self.show_stack()
        else:
            print("Fin del programa")
            self.debug_mode = False

    def show_stack(self) -> None:
        print("Contenido de la pila:")
        for i, value in enumerate(self.stack):
            print(f"{i}: {value}")

    def run_repl(self) -> None:
        print("Interpretador MEPA - Digite 'EXIT' para salir")
        
        while True:
            try:
                command = input("> ").strip().split()
                if not command:
                    continue

                cmd = command[0].upper()
                args = command[1:]

                if cmd == "EXIT":
                    if self.modified:
                        resp = input("¿Guardar cambios antes de salir? (S/N): ")
                        if resp.upper() == 'S':
                            self.save_file()
                    break

                elif cmd == "LOAD":
                    if len(args) != 1:
                        print("Uso: LOAD <archivo.mepa>")
                    else:
                        self.load_file(args[0])

                elif cmd == "LIST":
                    self.list_code()

                elif cmd == "RUN":
                    self.run()

                elif cmd == "INS":
                    if len(args) < 2:
                        print("Uso: INS <línea> <instrucción>")
                    else:
                        line_num = int(args[0])
                        instruction = ' '.join(args[1:])
                        self.insert_line(line_num, instruction)

                elif cmd == "DEL":
                    if len(args) == 1:
                        self.delete_line(int(args[0]))
                    elif len(args) == 2:
                        self.delete_line(int(args[0]), int(args[1]))
                    else:
                        print("Uso: DEL <línea> [línea_final]")

                elif cmd == "SAVE":
                    self.save_file()

                elif cmd == "DEBUG":
                    self.debug_mode = True
                    self.program_counter = min(self.code.keys())
                    self.stack = []
                    self.memory = []
                    print("Modo depuración iniciado")

                elif cmd == "NEXT":
                    self.debug_next()

                elif cmd == "STOP":
                    self.debug_mode = False
                    print("Modo depuración terminado")

                elif cmd == "STACK":
                    self.show_stack()

                else:
                    print(f"Comando desconocido: {cmd}")

            except KeyboardInterrupt:
                print("\nPrograma interrumpido. ¿Desea guardar los cambios antes de salir? (S/N): ", end='')
                try:
                    resp = input().upper()
                    if resp == 'S':
                        self.save_file()
                    print("\nSaliendo del programa...")
                    break
                except KeyboardInterrupt:
                    print("\nSaliendo del programa sin guardar...")
                    break

            except EOFError:
                print("\nSaliendo del programa...")
                break

            except Exception as e:
                print(f"Error: {str(e)}")

def main():
    interpreter = MEPAInterpreter()
    interpreter.run_repl()

if __name__ == "__main__":
    main()