from typing import Dict, List, Optional
import os

class MEPAInterpreter:
    """
    Interpretador para a linguagem MEPA (Máquina de Execução de Programas Acadêmicos)
    """
    def __init__(self):
        # Lista para armazenar valores na memória
        self.memory: List[int] = []
        # Pilha para operações
        self.stack: List[int] = []
        # Dicionário para armazenar o código (número_linha: instrução)
        self.code: Dict[int, str] = {}
        # Nome do arquivo atual
        self.current_file: str = ""
        # Modo de depuração
        self.debug_mode: bool = False
        # Contador de programa
        self.program_counter: int = 0
        # Indicador de modificações não salvas
        self.modified: bool = False
        # Dicionário para armazenar rótulos
        self.labels: Dict[str, int] = {}

    def execute_instruction(self, instruction: str) -> bool:
        """
        Executa uma instrução MEPA individual
        """
        parts = instruction.split()
        op = parts[0].upper()

        try:
            if op == "INPP":  # Iniciar Programa
                self.stack = []
                self.memory = []
            elif op == "AMEM":  # Alocar Memória
                m = int(parts[1])
                self.memory.extend([0] * m)
            elif op == "DMEM":  # Desalocar Memória
                m = int(parts[1])
                self.memory = self.memory[:-m]
            elif op == "CRCT":  # Carregar Constante
                k = int(parts[1])
                self.stack.append(k)
            elif op == "CRVL":  # Carregar Valor
                n = int(parts[1])
                self.stack.append(self.memory[n])
            elif op == "ARMZ":  # Armazenar na Memória
                n = int(parts[1])
                if n >= len(self.memory):
                    self.memory.extend([0] * (n - len(self.memory) + 1))
                self.memory[n] = self.stack.pop()
            # Operações aritméticas
            elif op in ["SOMA", "SUBT", "MULT", "DIVI"]:
                b = self.stack.pop()
                a = self.stack.pop()
                if op == "SOMA": self.stack.append(a + b)      # Soma
                elif op == "SUBT": self.stack.append(a - b)    # Subtração
                elif op == "MULT": self.stack.append(a * b)    # Multiplicação
                elif op == "DIVI": self.stack.append(a // b)   # Divisão
            elif op == "INVR":  # Inverter sinal
                self.stack[-1] = -self.stack[-1]
            elif op == "IMPR":  # Imprimir
                print(self.stack.pop())
            elif op == "PARA":  # Parar programa
                return False
            elif op == "NADA":  # Não fazer nada
                pass
            elif op in ["CMEG", "CMMA", "CMME", "CMAG", "CMIG", "CMDG"]:
                b = self.stack.pop()
                a = self.stack.pop()
                if op == "CMEG": self.stack.append(1 if a <= b else 0)  # Menor o igual
                elif op == "CMMA": self.stack.append(1 if a > b else 0)  # Mayor
                elif op == "CMME": self.stack.append(1 if a < b else 0)  # Menor
                elif op == "CMAG": self.stack.append(1 if a >= b else 0) # Mayor o igual
                elif op == "CMIG": self.stack.append(1 if a == b else 0) # Igual
                elif op == "CMDG": self.stack.append(1 if a != b else 0) # Diferente
            elif op == "DSVF":  # Desvio Se Falso
                target = int(parts[1])
                condition = self.stack.pop()
                if condition == 0:  # Se falso
                    self.program_counter = target - 1
            elif op == "DSVS":  # Desvio Sempre
                target = int(parts[1])
                self.program_counter = target - 1
            else:
                print(f"Instrução não reconhecida: {op}")
                return False
            return True
        except Exception as e:
            print(f"Erro ao executar {instruction}: {str(e)}")
            return False

    def load_file(self, filename: str) -> None:
        """
        Carrega um arquivo MEPA
        """
        # Verifica se há alterações não salvas
        if self.modified:
            resp = input("Há alterações não salvas. Deseja salvar? (S/N): ")
            if resp.upper() == 'S':
                self.save_file()

        try:
            with open(filename, 'r') as file:
                self.code.clear()
                self.labels.clear()
                # Lê cada linha do arquivo
                for line in file:
                    line = line.split('#')[0].strip()  # Remove comentários
                    if line:
                        parts = line.split(maxsplit=1)
                        num = int(parts[0])
                        if len(parts) > 1:
                            instruction = parts[1]
                            # Trata rótulos
                            if instruction.endswith(':'):
                                self.labels[instruction[:-1]] = num
                            self.code[num] = instruction
            self.current_file = filename
            self.modified = False
            print(f"Arquivo '{filename}' carregado com sucesso.")
        except FileNotFoundError:
            print(f"Erro: Arquivo '{filename}' não encontrado")

    def save_file(self) -> None:
        if not self.current_file:
            print("Não há arquivo aberto para salvar")
            return

        try:
            with open(self.current_file, 'w') as file:
                for line_num in sorted(self.code.keys()):
                    file.write(f"{line_num} {self.code[line_num]}\n")
            self.modified = False
            print(f"Arquivo salvo: {self.current_file}")
        except Exception as e:
            print(f"Erro ao salvar: {str(e)}")

    def list_code(self) -> None:
        if not self.code:
            print("Não há código carregado")
            return

        lines = sorted(self.code.keys())
        for i in range(0, len(lines), 20):
            chunk = lines[i:i+20]
            for line_num in chunk:
                print(f"{line_num} {self.code[line_num]}")
            
            if i + 20 < len(lines):
                input("Pressione Enter para continuar...")

    def insert_line(self, line_num: int, instruction: str) -> None:
        if line_num < 0:
            print("O número da linha não pode ser negativo")
            return

        self.code[line_num] = instruction
        self.modified = True
        print(f"Linha inserida: {line_num} {instruction}")

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
            print("Linhas eliminadas:")
            for line in deleted:
                print(line)
        else:
            print("Não foram encontradas linhas para eliminar")

    def run(self) -> None:
        if not self.code:
            print("Não há código para executar")
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
            print("Não está em modo de depuração")
            return

        if self.program_counter in self.code:
            instruction = self.code[self.program_counter]
            print(f"{self.program_counter} {instruction}")
            if self.execute_instruction(instruction):
                self.program_counter = next((k for k in sorted(self.code.keys()) 
                                           if k > self.program_counter), -1)
            self.show_stack()
        else:
            print("Fim do programa")
            self.debug_mode = False

    def show_stack(self) -> None:
        print("Conteúdo da pilha:")
        for i, value in enumerate(self.stack):
            print(f"{i}: {value}")

    def run_repl(self) -> None:
        """
        Ejecuta el loop REPL (Read-Eval-Print Loop)
        """
        print("Interpretador MEPA - Digite 'EXIT' para sair")
        
        while True:
            try:
                command = input("> ").strip().split()
                if not command:
                    continue

                cmd = command[0].upper()
                args = command[1:]

                if cmd == "EXIT":
                    if self.modified:
                        resp = input("Deseja salvar as alterações antes de sair? (S/N): ")
                        if resp.upper() == 'S':
                            self.save_file()
                    break
                elif cmd == "LOAD":
                    if len(args) != 1:
                        print("Uso: LOAD <arquivo>")
                    else:
                        self.load_file(args[0])
                elif cmd == "LIST":
                    self.list_code()
                elif cmd == "RUN":
                    self.run()
                elif cmd == "INS":
                    if len(args) < 2:
                        print("Uso: INS <numero_linha> <instrucao>")
                    else:
                        self.insert_line(int(args[0]), ' '.join(args[1:]))
                elif cmd == "DEL":
                    if len(args) == 1:
                        self.delete_line(int(args[0]))
                    elif len(args) == 2:
                        self.delete_line(int(args[0]), int(args[1]))
                    else:
                        print("Uso: DEL <linha_inicial> [linha_final]")
                elif cmd == "SAVE":
                    self.save_file()
                elif cmd == "DEBUG":
                    self.debug_mode = True
                    self.program_counter = min(self.code.keys())
                    self.stack = []
                    self.memory = []
                    print("Modo de depuração iniciado")
                elif cmd == "NEXT":
                    self.debug_next()
                elif cmd == "STOP":
                    self.debug_mode = False
                    print("Depuração interrompida")
                elif cmd == "STACK":
                    self.show_stack()
                else:
                    print(f"Comando desconhecido: {cmd}")

            except KeyboardInterrupt:
                print("\nPrograma interrompido...")
                break
            except Exception as e:
                print(f"Erro: {str(e)}")

def main():
    interpreter = MEPAInterpreter()
    interpreter.run_repl()

if __name__ == "__main__":
    main()
    
