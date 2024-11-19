# 🖥️ Interpretador MEPA

## ✒️ Autor
**Guilherme Henrique Pires Lopes** - [GuilhermePiresLopes](https://github.com/GuilhermePiresLopes)

## 📋 Sobre o Projeto
Um interpretador para a linguagem MEPA (Máquina de Execução de Português Algorítmico) desenvolvido em Python. Este projeto implementa um ambiente REPL (Read-Eval-Print-Loop) completo para execução e depuração de códigos MEPA.

## 📋 Pré-requisitos
- Python 3.6 ou superior

## 🎮 Guia Completo de Comandos

### Comandos Básicos de Execução
# 1. Iniciar o interpretador
python mepa.py

# 2. Carregar um arquivo
> LOAD factorial.mepa

# 3. Executar o programa
> RUN

# 4. Sair do programa
> EXIT

### Comandos de Visualização e Edição
# Listar o código atual
> LIST

# Inserir uma nova linha
> INS 10 INPP
> INS 20 AMEM 3
> INS 30 CRCT 5

# Deletar uma linha específica
> DEL 30

# Deletar um intervalo de linhas
> DEL 20 40

### Comandos de Depuração
# Iniciar modo de depuração
> DEBUG

# Executar próxima instrução
> NEXT

# Ver conteúdo da pilha
> STACK

# Sair do modo de depuração
> STOP

### Comandos de Arquivo
# Salvar alterações
> SAVE

# Carregar outro arquivo
> LOAD outro_exemplo.mepa

### Exemplo de Sessão Completa
# Iniciar o programa
python mepa.py

# Carregar arquivo de fatorial
> LOAD factorial.mepa

# Verificar o código
> LIST

# Executar o programa
> RUN

# Testar depuração
> DEBUG
> NEXT
> STACK
> STOP

# Fazer alterações
> INS 35 CRCT 6
> LIST
> DEL 35
> LIST

# Salvar e sair
> SAVE
> EXIT

### Dicas Importantes

1. **Carregamento de Arquivos**
   - Use o caminho completo se o arquivo não estiver na pasta atual
   - Exemplo: LOAD C:\Users\Usuario\factorial.mepa

2. **Edição de Código**
   - Números de linha devem ser positivos
   - Mantenha espaço entre número e instrução
   - Use LIST após edições para confirmar mudanças

3. **Depuração**
   - DEBUG deve ser usado antes de NEXT
   - STACK mostra estado atual da pilha
   - STOP pode ser usado a qualquer momento

4. **Salvamento**
   - SAVE antes de EXIT para não perder alterações
   - Sistema perguntará sobre alterações não salvas

### Sequência Recomendada para Testes

1. Carregar arquivo:
> LOAD factorial.mepa

2. Verificar conteúdo:
> LIST

3. Executar normalmente:
> RUN

4. Testar depuração:
> DEBUG
> NEXT
> STACK
> STOP

5. Testar edição:
> INS 35 CRCT 6
> LIST
> DEL 35
> LIST

6. Finalizar:
> SAVE
> EXIT

### Observações Finais
- Todos os comandos são case-insensitive (LOAD = load)
- Use Ctrl+C para interromper execução
- Comentários em arquivos MEPA começam com #
- Sistema pergunta sobre salvar ao sair

## 🛠️ Estrutura do Projeto
projeto/
│
├── mepa.py           # Interpretador MEPA
├── factorial.mepa    # Exemplo de programa
└── README.md         # Este arquivo