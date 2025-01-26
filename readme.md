# PROGRAMAÇÃO LINEAR

## SIMPLEX REVISADO

A presente aplicação foi feita com intuito de aplicar de forma prática o método `simplex revisado` em uma interface
gráfica, permitindo entrada de dados manual ou por arquivo de texto.

![alt text](https://github.com/olucaseduardo/simplex_revisado/blob/master/assets/interface_1.png?raw=true)

### ENTRADA DE DADOS

A entrada de dados pode ser realizada de duas maneiras:

- Manual:
    - Para a entrada manual de dados é necessário a inserção dos campos: `objetivo da função`,`Restrições`,`Variáveis`,
      `Solução Inicial`.
        - Objetivo da Função: Objetivo pretendido no problema, sendo eles: `Maximização` ou `Minimização`;
        - Restrições: Número de restrições presentes no problema, permitidos somente números inteiros positivos;
        - Variáveis: Número de variáveis presentes no problema, permitidos somente números inteiros positivos;
        - Solução Inicial: Método de busca de solução inicial quando necessário.
    - Ao clicar em `Gerar Tableau`, surgirá o tableau de dados e função objetivo para serem preenchidas com o PPL

![alt text](https://github.com/olucaseduardo/simplex_revisado/blob/master/assets/interface_2.png?raw=true)

- Arquivo de Texto
    - Para a entrada por arquivo de text, é necessário a formatação do PPL em arquivo, como o exemplo a seguir:
  ```text
  Max 2 3 4

  -2 0  3 >= 15
   1 2 -3 <= 10
   1 1  0  = 8
  ```
    - Após a importação do arquivo de texto, o tableau é gerado automaticamente.

![alt text](https://github.com/olucaseduardo/simplex_revisado/blob/master/assets/interface_5.png?raw=true)

## FORMA PADRÃO

Inicialmente o PPL é inserido em sua forma modelada, para a correta busca pela solução do problema, é necessário a
transformação do PPL em sua forma padrão. A forma padrão é realizada na classe `StandardForm` em seu método `execute()`,
são passadas os valores necessários para a transformação, e retornados em sua forma padrão como `np.array`.

## SIMPLEX

A escolha do método simplex apropriado para o PPL e preferências do usuário é realizada na classe `SimplexMethods` e
então é chamada a class `ReviewedSimplex` para a execução efetiva do método.

São possíveis 3 modelos de retorno:

* **PPL ILIMITADO** - É considerado ilimitado quando o teste da razão origina divisões oriundas de divisor igual a 0 ou
  com resultados negativo.
* **PPL INVIÁVEL** - É considerado inviável quando não há total retirada de variáveis artificiais da base com valores
  diferentes de 0.
* **PPL VIÁVEL** - É considerado viável quando nenhum dos casos acima é encontrado.

Exemplo de Retorno PPL VIÁVEL

![alt text](https://github.com/olucaseduardo/simplex_revisado/blob/master/assets/interface_6.png?raw=true)


### Formulas

Atualizar as variáveis não básicas na FO

* cR = cR − cB ⋅ B⁻¹ ⋅ R

Definir o novo valor das variáveis básicas
* b = B⁻¹ ⋅ b

Calcular os coeficientes das variáveis não básicas
* R = B⁻¹ ⋅ R

Recalcular o valor da Função-objetivo
* FO = cB ⋅ B⁻¹ ⋅ b

### Rotulação

* B - Matriz de valores presentes na base
* R - Matriz de valores não presentes na base
* b - Vetor coluna de soluções do PPL
* cR - Vetor linha de variáveis fora da base da função objetivo
* cB - Vetor linha de variáveis na base da função objetivo
* FO - Valor calculado da função objetivo


## Desenvolvedor

**Lucas Eduardo**  
Engenheiro de Software | Desenvolvedor de Sistemas  
[GitHub](https://github.com/olucaseduardo) | [LinkedIn](https://www.linkedin.com/in/lucas-eduardo-89a92a328/) | [E-mail](mailto:le.eduardp.dev@gmail.com)
