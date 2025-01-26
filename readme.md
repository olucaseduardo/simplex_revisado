
# PROGRAMAÇÃO LINEAR

## SIMPLEX REVISADO

A presente aplicação foi feita com intuito de aplicar de forma prática o método `simplex revisado` em uma interface gráfica, permitindo entrada de dados manual ou por arquivo de texto.

![alt text](https://github.com/olucaseduardo/simplex_revisado/assets/interface_1.png)

### ENTRADA DE DADOS

A entrada de dados pode ser realizada de duas maneiras:

- Manual:
  - Para a entrada manual de dados é necessário a inserção dos campos: `objetivo da função`,`Restrições`,`Variáveis`,`Solução Inicial`.
    - Objetivo da Função: Objetivo pretendido no problema, sendo eles: `Maximização` ou `Minimização`;
    - Restrições: Número de restrições presentes no problema, permitidos somente números inteiros positivos;
    - Variáveis: Número de variáveis presentes no problema, permitidos somente números inteiros positivos;
    - Solução Inicial: Método de busca de solução inicial quando necessário.

![alt text](https://github.com/olucaseduardo/simplex_revisado/assets/interface_2.png)

- Arquivo de Texto
  - Para a entrada por arquivo de text, é necessário a formatação do PPL em arquivo, como o exemplo a seguir:
  ```text
  Max 2 3 4

  -2 0  3 >= 15
   1 2 -3 <= 10
   1 1  0  = 8
  ```
  - Após a importação do arquivo de texto, o tableau é gerado automaticamente.
