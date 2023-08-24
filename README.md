<h1>Gestão de Clientes e Busca de Citações em PDF - ⚖️</h1>

## Objetivos
O objetivo desse repositório é elaborar um MVP de um sistema que realiza a gestão de clientes de um escritório a partir de um arquivo CSV e busca possíveis citações desses clientes em um arquivo PDF. 
Criado a partir da demanda do escritório CAMPELLO CASTRO CONSULTORIA E ASSECORIA JURÍDIA com a ideia de gerenciar e armazenar os clientes possibilitanto, ainda, realizar a busca das citações destes clientes no Diário Oficial da União (DOU).
A ideia principal é realizar a validação deste MVP para, posteriormente, desenvolver uma plataforma web escalável e robusta.
A documentação a seguir apresenta a estrutura do código e detalhes sobre suas funções e classes.

## Fundamentos
Baseado em programação orientada a objetos, esse sistema tem alguma classes principais que são criadas para facilitar o manuzeio das informações.
Sempre que o sistema se inicia, todos os dados são lidos do arquivp CSV e as classes são preenchidas conforme.
Assim, sempre que uma lateração é feita em algum desses objetos, a classe é alterada e logo em seguida o arquivo CSV também.

## Classes
### `Client`
- Atributos:
    - `ID`, `name`,`subname_01` a `subname_04`,`cnpj`,`number`,`email`,`representative`,`cited`,`selected``actived`,

### `ClientsList`
- Atributos:
    - `clients`, `ActivedClients`,`InactivedClients`

## Interface
Foi utilizada a biblioteca CustomTKInter que é uma variação da biblioteca TKInter. Com ela foi possível desenvolver uma interface simples mas agradável e moderna.
Por se tratar de um MVP que será validade por poucas pessoas, não foram atentados à detalhes de responsividade.

## Conclusão
Sendo a ideia principal um sistema simples e de validação, o código possui algumas poucas lógicas não muito recomendadas do ponto de vista da programação orientada a objetos.
Isso se dá devido ao fato da implementação e teste ter se dado mais rápida dessa forma, atingindo ao objetivo necessário.
### FIM
O MVP foi concluido em Agosto/2023, e iniciou-se o processo de validação pelas advogadas da CAMPELLO CASTRO CONSULTORIA E ASSECORIA JURÍDIA.
