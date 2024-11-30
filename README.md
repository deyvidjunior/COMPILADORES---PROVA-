# 🖥️ Interpretador MEPA

## ✒️ Autor
**Deyvid Junior Limachi Alejo** - [GitHub](https://github.com/deyvidjunior/COMPILADORES---PROVA-.git)

# 📚 Documentação do Interpretador MEPA

## Introdução 🤔
MEPA (Máquina de Execução de Programas Acadêmicos) é um interpretador educacional que simula uma máquina de pilha simples, projetado para auxiliar no aprendizado de conceitos fundamentais de programação e arquitetura de computadores.

## Arquitetura Básica 🔧
O interpretador opera com duas estruturas principais:
- 📦 **Memória**: Armazena variáveis e dados do programa
- 📚 **Pilha**: Gerencia operações e cálculos temporários

## Conjunto de Instruções 📝
| Categoria | Comando | Descrição |
|-----------|---------|-----------|
| **Controle de Programa** |
| | `INPP` | Inicializa programa |
| | `PARA` | Finaliza execução |
| | `NADA` | Instrução nula |
| **Gestão de Memória** |
| | `AMEM n` | Aloca n posições de memória |
| | `DMEM n` | Desaloca n posições de memória |
| **Operações com Dados** |
| | `CRCT k` | Carrega constante k na pilha |
| | `CRVL n` | Carrega valor da memória[n] |
| | `ARMZ n` | Armazena valor na memória[n] |
| **Operações Aritméticas** |
| | `SOMA` | Soma dois valores do topo |
| | `SUBT` | Subtrai dois valores |
| | `MULT` | Multiplica dois valores |
| | `DIVI` | Divide dois valores |
| | `INVR` | Inverte sinal |
| **Comparações** |
| | `CMEG` | Menor ou igual |
| | `CMMA` | Maior |
| | `CMME` | Menor |
| | `CMAG` | Maior ou igual |
| | `CMIG` | Igual |
| | `CMDG` | Diferente |
| **E/S** |
| | `IMPR` | Imprime valor do topo |

## Utilização do Interpretador 🎮

### Comandos do Sistema
```bash
# Iniciar interpretador
python mepa.py

# Comandos disponíveis no prompt
LOAD arquivo.mepa  # Carrega programa
RUN               # Executa programa
LIST              # Lista código
INS n instrucao   # Insere instrução na linha n
DEL n [m]         # Deleta linha n (ou linhas n até m)
DEBUG             # Inicia modo debug
NEXT              # Próxima instrução (debug)
STACK             # Mostra pilha
CLEAR_HISTORY     # Limpa pilha e memória
EXIT              # Encerra interpretador
```

### Exemplo: Cálculo de Fatorial
```mepa
10 INPP
20 AMEM 3
30 CRCT 5    # Número para calcular fatorial
40 ARMZ 1    # Armazena na memória
...
270 PARA
```

## Modo Debug 🔍
O modo debug permite:
- Execução passo a passo
- Visualização do estado da pilha
- Acompanhamento das instruções
- Análise de valores na memória


## Exemplo: Programa Fatorial 🌟

### O que é fatorial?
- É a multiplicação de um número por todos os números menores que ele até 1
- Exemplo: 5! = 5 x 4 x 3 x 2 x 1 = 120

### Como o programa factorial.mepa funciona:
1. ▶️ Inicia o programa
2. 📥 Guarda o número 5
3. 🔄 Multiplica: 5 x 4 x 3 x 2 x 1
4. 📤 Mostra o resultado (120)
5. ⏹️ Termina

## Dicas Importantes 💡
- Use `LIST` para ver seu código
- `DEBUG` ajuda a entender passo a passo
- Não esqueça de `SAVE` antes de sair
- Use `HELP` se precisar de ajuda

## Erros Comuns e Soluções 🚨
1. **Arquivo não encontrado**
   - Verifique se o nome está correto
   - Confira se está na pasta certa

2. **Comando não reconhecido**
   - Digite os comandos exatamente como mostrado
   - Comandos são em MAIÚSCULAS

## Precisa de Ajuda? 🆘
- Use `LIST` para ver o código atual
- `DEBUG` + `NEXT` para ver passo a passo
- `STACK` mostra os números na pilha

## Requisitos 📋
- Python 3.6 ou mais recente
- Arquivo .mepa para executar

## Para Iniciantes 🌱
1. Comece com programas simples
2. Use o modo DEBUG para entender cada passo
3. Experimente modificar os números no factorial.mepa
4. Pratique com os comandos básicos primeiro

---

## Requisitos Técnicos ⚙️
- Python 3.6+
- Sistema operacional: Windows/Linux/MacOS

## Observações Importantes ⚠️
- Números de linha devem ser únicos
- Instruções são case-insensitive
- Comentários usam #
- Salve alterações antes de sair

## 🛠️ Estrutura do Projeto
projeto/
│
├── mepa.py           # Interpretador MEPA
├── factorial.mepa    # Exemplo de programa
└── README.md         # Este arquivo

---
Desenvolvido para fins educacionais 📚| Versão 1.0
