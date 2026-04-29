Desafio: Implementação de Estrutura com Docker Compose - Jogo de Adivinhação com Flask

Objetivo: Deverá implementar uma estrutura com Docker Compose que englobe os seguintes serviços:

Um container para o backend em Python (Flask).
Um container para o banco de dados Postgres.
Um container NGINX atuando como proxy reverso e servindo as páginas do frontend React.

# Resumo

Este é um simples jogo de adivinhação desenvolvido utilizando o framework Flask. O jogador deve adivinhar uma senha criada aleatoriamente, e o sistema fornecerá feedback sobre o número de letras corretas e suas respectivas posições.

# Funcionalidades
Criação de um novo jogo com uma senha fornecida pelo usuário.
Adivinhe a senha e receba feedback se as letras estão corretas e/ou em posições corretas.
As senhas são armazenadas utilizando base64.
As adivinhações incorretas retornam uma mensagem com dicas.


# Requisitos

Containers Backend e Frontend:
O container do backend Python executará aplicação Flask do jogo de adivinhação.
O container NGINX servirá como proxy reverso, balanceando a carga entre instâncias do backend, e também servirá o frontend React.
Python 3.8+
Flask
Um banco de dados local - Postgres
node 18.17.0


# Banco de Dados Postgres:
O container do Postgres deverá armazenar os dados do jogo.
O banco de dados deverá ser mantido em um volume separado para garantir a persistência dos dados.


# Resiliência e Manutenção:
1) Reinício de Containers: Se algum container falhar, ele deve ser reiniciado automaticamente.
2) Balanceamento de Carga no Proxy Reverso: O NGINX deve ser configurado para fazer o balanceamento de carga entre múltiplos containers do backend.
3) Volumes Separados para o Banco de Dados: O banco de dados Postgres deve ser armazenado em um volume persistente.
4) Facilidade de Atualização: A estrutura deve permitir a atualização de qualquer componente (backend, frontend, banco de dados) apenas trocando a versão do container correspondente.

# Entrega

O projeto deverá ser entregue como um repositório no GitHub com as seguintes características:

# Estrutura do Repositório:

Docker Compose File (docker-compose.yml): Para definir e orquestrar os serviços.
Dockerfile do Backend Python: Para configurar o container que executa a aplicação Flask.
Dockerfile do Frontend React: Para configurar o container que serve a aplicação frontend via NGINX.
Configuração do NGINX: Para definir o proxy reverso e o balanceamento de carga entre múltiplas instâncias do backend.

# Documentação (README.md):
1) Explicação das opções de design adotadas, como a escolha de serviços, volumes, redes, e estratégia de balanceamento de carga.
2) Instruções detalhadas sobre como instalar, rodar e atualizar os serviços.
3) Detalhes sobre como cada componente pode ser atualizado facilmente trocando a versão da imagem Docker.


# Avaliação

Os seguintes critérios serão considerados na avaliação do projeto:

1) Funcionamento Correto: Todos os containers devem se comunicar corretamente e o sistema deve funcionar como esperado, com resiliência em caso de falhas. Favor informar qual a URL deve ser utilizada após o docker-compose up.  
2) Facilidade de Atualização: O projeto deve permitir a fácil atualização dos componentes (backend, frontend, banco de dados) sem necessidade de mudanças complexas no código.
Documentação Completa e Clara: O README.md deve conter instruções claras de instalação, uso, e explicações sobre as decisões de design adotadas.