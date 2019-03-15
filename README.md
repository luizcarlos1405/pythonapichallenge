# Python API Challenge: Documentação

Esta aplicação guarda informações de movimentações financeiras de usuários. É possível guardar movimentações de entrada e saída de valores e nomear cada movimentação. Cada usuário possuia acesso apenas às movimentações ligadas à sua conta.

Estão disponíveis, na API, as rotas `autenticacao/`, `formulario/` e `lista/`; e o objetivo bônus de ordenar a lista foi atingido. Esta documentação apresenta o uso de cada uma dessas rotas.

## Autenticacão

As outras rotas não são acessíveis sem autenticação, que é realizada através de sessão. Para autenticar basta enviar uma requisição **POST** com os parâmetros *username* e *password*. Exemplo:

```
POST /autenticacao/ HTTP/1.1
Host: apihost.com
username=usuario224&password=pr0p3rp4$$w0rd
```
Após essa resquisição a sessão será autenticada para o usuário *usuario224*. A aplicação cliente deve ser capaz de manter uma sessão, porém é possível autenticar a sessão do navegador acessando `apihost.com/autenticacao/` e preenchendo o formulário manualmente.

A autenticação provoca um redirecionamento para a rota `lista/`.

## Formulário

Para adicionar valores ao banco de dados basta fazer uma requisição **POST** para a rota `formulario/` com os parâmetros `nome`, `valor` e `tipo`. Sendo `nome` uma `string`, `valor` um número decimal com até duas casas após a vírgula, representando o valor em reais da movimentação financeira, e `tipo` uma de duas `strings`: `entrada` ou `saida` (note que `saida` não possui acento). Exemplo:

```
POST /formulario/ HTTP/1.1
Host: apihost.com
nome=Fatura Cartão de Crédito&valor=2460.49&tipo=saida
```
Se a sessão estiver autenticada a movimentação com nome *Fatura Cartão de Crédito* e valor *-2460.49* será adicionada ao banco de dados para o usuário atual. É possível adicionar através do browser acessando a rota `formulario/` e preenchendo o formulário diponível. Não serão adicionadas ao banco requisições que:

* Não definam um `nome`;
* Forneçam um `valor` menor ou igual a zero;
* Não especifiquem um `tipo` (`entrada` ou `saida`);
* Não estejam dentro de uma sessão autenticada;
* Forneçam um `valor` com mais de duas casas decimais;

## Lista

Para verificar as movimentações salvas para a conta atualmente autenticada deve-se fazer uma requisição **GET** na rota `lista/`. Exemplo:

```
apihost.com/lista/?format=json
```
A resposta para a requisição será um *JSON* contendo todas as movimentações disponíveis. É possível ordenar a lista considerando o *nome* e o *valor* de forma ascendente e descenedente. Para isso basta adicionar o parâmetro `ordering` e especificar qual valor e ordenação deve ser considerado. Exemplos:

```
# Para ornenar pelo nome de forma ascendente:
apihost.com/lista/?format=json&ordering=nome

# Nome descendente:
apihost.com/lista/?format=json&ordering=-nome

# Valor ascendente:
apihost.com/lista/?format=json&ordering=valor

# Valor descendente:
apihost.com/lista/?format=json&ordering=-valor
```
É possível acessar essas requisições pelo navegador.
