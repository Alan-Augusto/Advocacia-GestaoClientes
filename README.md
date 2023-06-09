# Gestão de Clientes e Busca de Citações em PDF

O código a seguir realiza a gestão de clientes a partir de um arquivo CSV e busca possíveis citações desses clientes em um arquivo PDF. A documentação a seguir apresenta a estrutura do código e detalhes sobre suas funções e classes.

## Pacotes Necessários
- pdfplumber
- csv
- tkinter
- re
- customtkinter
- PIL

## Variáveis Globais
- `CLIENTS_CSV_FILE`: caminho para o arquivo CSV que contém os dados dos clientes
- `NUM_SEARCHES`: contador de buscas realizadas pelo usuário

## Classes
### `Client`
- Atributos:
    - `ID`: número inteiro, inicializado como `-1`
    - `name`: nome do cliente, string
    - `subname_01` a `subname_04`: subnomes do cliente, strings
    - `cnpj`: número do CNPJ do cliente, string
    - `number`: número de telefone do cliente, string
    - `email`: endereço de email do cliente, string
    - `representative`: representante do cliente, string
    - `cited`: indicador booleano que informa se o cliente foi citado no arquivo PDF, inicializado como `False`
    - `selected`: indicador booleano que informa se o cliente foi selecionado pelo usuário, inicializado como `False`
    - `actived`: indicador booleano que informa se o cliente está ativo, inicializado como `True` (a menos que a coluna "ativo" do CSV seja "FALSE")
- Métodos:
    - `set_ID(number)`: define o ID do cliente como o número fornecido
    - `change_name(new_name)`: altera o nome do cliente para o nome fornecido
    - `change_cnpj(new_cnpj)`: altera o CNPJ do cliente para o número fornecido
    - `change_number(new_number)`: altera o número de telefone do cliente para o número fornecido
    - `change_email(new_email)`: altera o endereço de email do cliente para o endereço fornecido
    - `make_cited()`: altera o atributo `cited` para `True`
    - `select()`: altera o atributo `selected` para `True`
    - `print()`: imprime na tela os atributos do cliente

### `ClientsList`
- Atributos:
    - `clients`: lista de clientes, inicializada como uma lista vazia
- Métodos:
    - `add_client(client)`: adiciona um cliente à lista de clientes
    - `remove_client(clientID)`: remove um cliente da lista com base em seu ID
    - `print()`: imprime na tela os atributos de todos os clientes da lista
    - `searched_names()`: retorna uma lista com os nomes dos clientes que estão marcados como ativos

## Funções Globais
### `fill_list()`
- Retorna uma lista de clientes preenchida com os dados do arquivo CSV `CLIENTS_CSV_FILE`.

### `browse_pdf()`
- Abre uma caixa de diálogo para o usuário selecionar o arquivo PDF desejado.

### `buscar_palavras(app)`
- Realiza a busca das palavras-chave dos clientes no arquivo PDF selecionado pelo usuário. Imprime na tela as citações encontradas e marca os clientes como citados.

## Utilização do Código
- Executar a função `buscar_palavras
