# prova-backend-c-Thiago-Panchiniak
Resolução de Desafio Tecnico Para IPM

## Parte 1: Questão teórica 

A arquitetura apresentada tem como objetivo permitir a integração entre drones DJI, aplicações clientes, serviços de backend, armazenamento de dados e ferramentas de monitoramento. A comunicação é centralizada por um **API Gateway**, enquanto serviços especializados cuidam do processamento das informações, armazenamento de arquivos, comunicação em tempo real e observabilidade do ambiente.

### Usuário

Representa o operador responsável pela utilização do drone e dos serviços disponibilizados pela plataforma. O usuário pode interagir diretamente com o controle remoto DJI e, indiretamente, com os serviços da plataforma por meio dos aplicativos e APIs disponíveis.

### Drone DJI

É o equipamento responsável pela captura e geração dos dados utilizados pela plataforma, como imagens, vídeos, telemetria, posição geográfica e informações relacionadas ao voo. O drone mantém comunicação com o controle remoto e, através dele, com a aplicação DJI.

### Controle Remoto DJI

É o dispositivo utilizado para controlar o drone e intermediar a comunicação entre o equipamento, o operador e a aplicação instalada no dispositivo associado ao controle. Além dos comandos de voo, pode transmitir informações de telemetria e outros dados provenientes do drone.

### Android App

Representa a aplicação responsável pela integração entre os equipamentos DJI e a infraestrutura de backend. A aplicação pode utilizar recursos disponibilizados pela DJI Cloud API para enviar informações do drone, receber comandos e estabelecer canais de comunicação HTTP ou WebSocket com os serviços da plataforma.

### Kong – API Gateway / Proxy Reverso

O **Kong** funciona como ponto central de entrada para os serviços da arquitetura. Seu objetivo é receber as requisições realizadas pelas aplicações clientes e encaminhá-las para o serviço apropriado.

Além do roteamento, o Gateway pode ser responsável por funções como autenticação, autorização, controle de acesso, limitação de requisições (*rate limiting*), registro de logs e gerenciamento de diferentes versões das APIs. Dessa forma, os serviços internos não precisam ser diretamente expostos para aplicações externas.

### API REST / Microsserviço de Storage

A **API REST** apresentada no diagrama atua como uma camada intermediária entre as aplicações e o serviço de armazenamento de objetos.

Seu principal objetivo é abstrair o acesso ao **Amazon S3**, evitando que aplicações clientes tenham acesso direto às credenciais ou aos mecanismos internos do armazenamento. Esse microsserviço pode implementar regras de autenticação, autorização, geração de URLs temporárias, validação de arquivos e controle de acesso aos dados.

### Amazon S3

O **Amazon Simple Storage Service (S3)** é utilizado para armazenamento de objetos e arquivos de maior volume. Dentro de uma plataforma envolvendo drones, pode armazenar imagens, vídeos, ortofotos, arquivos produzidos durante missões e outros dados que não são adequados para armazenamento diretamente em um banco de dados relacional.

O S3 também oferece características importantes para esse tipo de sistema, como alta disponibilidade, escalabilidade e controle de acesso.

### API Java

Representa um dos principais serviços de backend da arquitetura. É responsável por implementar regras de negócio e realizar a comunicação com diferentes componentes, como banco de dados, Redis e broker MQTT.

Pode receber requisições provenientes do Gateway, processar informações relacionadas aos drones e usuários e coordenar a persistência ou distribuição dos dados entre os demais serviços.

### MySQL

O **MySQL** funciona como banco de dados relacional da aplicação. Seu objetivo é armazenar informações estruturadas e que precisam manter relacionamentos entre si.

Exemplos incluem usuários, drones cadastrados, dispositivos, configurações, missões, permissões, informações administrativas e referências aos arquivos armazenados no S3.

### Redis

O **Redis** é um banco de dados em memória utilizado principalmente para informações que precisam ser acessadas com grande velocidade.

Na arquitetura ele pode ser empregado como cache, armazenamento temporário de sessões, controle de estados, gerenciamento de tokens ou armazenamento temporário de informações relacionadas à comunicação com os drones.

### EMQX

O **EMQX** funciona como um **broker MQTT**, responsável por intermediar a comunicação baseada no protocolo MQTT.

Esse protocolo é bastante utilizado em aplicações IoT e sistemas distribuídos porque permite comunicação eficiente através do modelo **publish/subscribe**. Dessa forma, diferentes componentes podem publicar informações em determinados tópicos enquanto outros componentes recebem essas informações por meio de assinaturas.

No contexto da DJI Cloud API, esse mecanismo pode ser utilizado para troca de telemetria, comandos, estados dos equipamentos e eventos relacionados às operações dos drones.

### MQTT

O **MQTT** é o protocolo utilizado para a comunicação entre alguns componentes da arquitetura e o EMQX. Diferentemente de uma API HTTP tradicional, o MQTT permite manter uma comunicação contínua e assíncrona entre dispositivos e serviços.

Essa característica é especialmente importante para informações que precisam ser transmitidas com frequência, como posição, velocidade, bateria e estado operacional dos drones.

### WebSocket

A comunicação **WebSocket** permite estabelecer uma conexão persistente e bidirecional entre a aplicação cliente e o servidor.

No diagrama, essa comunicação pode ser utilizada para fornecer dados em tempo real para o aplicativo Android. O Kong pode atuar como intermediário dessa conexão, permitindo que aplicações clientes mantenham comunicação contínua com os serviços internos sem acessá-los diretamente.

### HTTP / REST

O protocolo HTTP é utilizado para operações tradicionais de requisição e resposta entre as aplicações e as APIs. É adequado principalmente para operações como consultas, cadastros, autenticação, gerenciamento de usuários, obtenção de informações de missões e solicitação de arquivos.

### Prometheus

O **Prometheus** é responsável pela coleta e armazenamento de métricas relacionadas ao funcionamento da infraestrutura.

Ele pode acompanhar informações como consumo de CPU e memória, número de requisições, quantidade de conexões, tempo de resposta dos serviços, erros, utilização do broker MQTT e disponibilidade dos componentes.

Essas informações permitem detectar problemas de desempenho ou indisponibilidade na plataforma.

### Grafana

O **Grafana** é utilizado para visualização das métricas coletadas pelo Prometheus.

Através de dashboards, os responsáveis técnicos pela plataforma podem acompanhar o comportamento do sistema praticamente em tempo real, observando indicadores de desempenho, disponibilidade dos serviços, utilização de recursos e possíveis falhas.

Também é possível configurar alertas para identificar situações anormais no ambiente.

### Técnico

Representa o responsável pela administração e monitoramento da infraestrutura. O técnico pode acessar ferramentas como Grafana e serviços administrativos do EMQX para analisar métricas, verificar o funcionamento dos componentes e identificar problemas na plataforma.

### Visão geral do fluxo

De maneira geral, o **Android App conectado ao ecossistema DJI envia informações para o Kong**, que funciona como ponto de entrada da infraestrutura. O Gateway direciona cada comunicação para o serviço adequado.

Operações relacionadas às regras de negócio são direcionadas para a API principal, enquanto arquivos como imagens e vídeos podem ser enviados para o microsserviço responsável pela comunicação segura com o S3. Informações estruturadas são armazenadas no MySQL, dados temporários ou de rápido acesso podem utilizar Redis e comunicações assíncronas ou em tempo real relacionadas aos drones podem utilizar MQTT através do EMQX.

Paralelamente, **Prometheus e Grafana formam a camada de observabilidade**, permitindo que a equipe técnica acompanhe o funcionamento e o desempenho de toda a infraestrutura.

Essa separação de responsabilidades torna a arquitetura mais **segura, modular e escalável**, além de facilitar a manutenção e a evolução independente de cada serviço.


## Parte 2: Desenvolvimento de API RESTful

### Como instalar e executar a API

Crie e ative um ambiente virtual:

```bash
python3 -m venv .venv
source .venv/bin/activate
```

Instale as dependências:

```bash
pip install -r requirements.txt
```

Execute a aplicação:

```bash
uvicorn app.main:app --reload
```

A API ficará disponível em:

```text
http://127.0.0.1:8000
```

A documentação interativa pode ser acessada em:

```text
http://127.0.0.1:8000/docs
```

## Parte 3: Integração de Modelos de IA

Foi criado um módulo para simular a integração com modelos de IA responsáveis pelo processamento de imagens aéreas de drones.

O endpoint principal recebe uma imagem, valida os parâmetros enviados, executa o processamento através de um serviço dedicado e registra o histórico da execução no banco de dados.

### Endpoint de processamento

```http
POST /api/v1/ai-processing/process
```

O endpoint recebe dados no formato `multipart/form-data`:

| Campo | Tipo | Descrição |
|---|---|---|
| `mission_id` | integer | ID da missão relacionada ao processamento |
| `confidence_threshold` | float | Valor entre `0` e `1` usado como limite de confiança |
| `image` | file | Imagem aérea enviada para processamento |

Exemplo com `curl`:

```bash
curl.exe -X POST "http://127.0.0.1:8000/api/v1/ai-processing/process" ^
  -H "Authorization: Bearer SEU_TOKEN" ^
  -F "mission_id=1" ^
  -F "confidence_threshold=0.7" ^
  -F "image=@C:/Dev/teste-api/drone-images/imagem.tif;type=image/tiff"
```

### Validações da imagem

Antes de enviar a imagem para o modelo, a API valida:

- tipo do arquivo
- extensão do arquivo
- arquivo vazio
- arquivo inválido ou corrompido
- tamanho máximo do arquivo

Formatos aceitos:

- `.jpg`
- `.jpeg`
- `.tif`
- `.tiff`
- `.geotiff`

### Modelo de IA

O modelo é carregado no `lifespan` do FastAPI, durante a inicialização da aplicação. Dessa forma, ele é carregado apenas uma vez e permanece em memória para ser reutilizado pelas requisições.

Atualmente, o projeto utiliza um modelo falso apenas para validar o fluxo de entrada, processamento, saída e registro de histórico.

Modelo configurado no momento:

```text
MODEL_NAME = "aerial_mapping_yolo"
MODEL_VERSION = "1.0.0"
```

### Histórico de processamentos

Cada processamento é registrado na tabela de histórico com os seguintes campos:

- `id`
- `mission_id`
- `created_at`
- `model_name`
- `model_version`
- `inference_time`
- `status`
- `result`
- `error_message`

O campo `result` é salvo como JSON, por exemplo:

```json
{
  "detections": 17,
  "classes": {
    "building": 10,
    "road": 4,
    "vehicle": 3
  }
}
```

Também são registrados casos de falha, incluindo a mensagem do erro no campo `error_message`.

### Endpoints de histórico

```http
GET    /api/v1/predictions
GET    /api/v1/predictions/{id}
PUT    /api/v1/predictions/{id}
DELETE /api/v1/predictions/{id}
GET    /api/v1/missions/{mission_id}/predictions
```

Todos os endpoints de processamento e histórico exigem autenticação JWT via header:

```http
Authorization: Bearer <token>
```

### A fazer

Substituir o modelo falso por um modelo real previamente treinado, mantendo a mesma interface de serviço para carregamento, inferência, versionamento e registro de histórico.

## Parte 4: Docker e Orquestração de Contêineres

A aplicação foi preparada para executar em contêineres utilizando Docker e Docker Compose.

Foram configurados três serviços principais:

- `api`: aplicação FastAPI
- `postgres`: banco de dados PostgreSQL
- `redis`: serviço Redis preparado para uso futuro em cache, filas ou processamento assíncrono

### Como subir o ambiente com Docker

Na raiz do projeto, execute:

```bash
docker compose up --build
```

Esse comando constrói a imagem da API e inicia os serviços `api`, `postgres` e `redis`.

Após a inicialização, a API ficará disponível em:

```text
http://127.0.0.1:8000
```

A documentação interativa pode ser acessada em:

```text
http://127.0.0.1:8000/docs
```

### Variáveis de ambiente

As principais variáveis usadas pela aplicação estão no arquivo `.env.example`:

```env
DATABASE_URL=sqlite:///./missions.db
REDIS_URL=redis://localhost:6379/0
SECRET_KEY=change-this-secret-key
AI_MODEL_NAME=aerial_mapping_yolo
AI_MODEL_VERSION=1.0.0
MAX_IMAGE_SIZE_MB=50
```

No Docker Compose, a API utiliza PostgreSQL e Redis através das URLs internas dos serviços:

```env
DATABASE_URL=postgresql+psycopg://drone_user:drone_password@postgres:5432/drone_mapping
REDIS_URL=redis://redis:6379/0
```

### PostgreSQL

O PostgreSQL é usado como banco de dados relacional no ambiente Docker.

As tabelas são criadas automaticamente na inicialização da aplicação através do SQLAlchemy.

O serviço utiliza volume Docker para persistência dos dados:

```yaml
postgres_data:/var/lib/postgresql/data
```

### Healthcheck da API

A API possui o endpoint:

```http
GET /api/v1/health
```

Ele pode ser testado com:

```bash
curl http://127.0.0.1:8000/api/v1/health
```

Resposta esperada:

```json
{"status":"ok"}
```

No `docker-compose.yml`, esse endpoint também é usado como `healthcheck` do serviço `api`, permitindo que o Docker identifique se a aplicação está saudável.

### Aguardando o banco de dados

O PostgreSQL possui um `healthcheck` usando `pg_isready`:

```yaml
healthcheck:
  test: ["CMD-SHELL", "pg_isready -U drone_user -d drone_mapping"]
```

A API depende desse healthcheck antes de iniciar:

```yaml
depends_on:
  postgres:
    condition: service_healthy
```

Com isso, a API só inicia depois que o PostgreSQL estiver pronto para aceitar conexões.

### Ordem de implementação

A configuração Docker foi implementada em etapas:

1. Configuração por variáveis de ambiente
2. Adição do driver PostgreSQL `psycopg`
3. Criação do `Dockerfile`
4. Criação do `docker-compose.yml`
5. Configuração dos healthchecks
6. Configuração para a API aguardar o banco de dados

### Redis

O Redis foi incluído para deixar o ambiente preparado para cenários de maior escala.

Neste contexto, ele pode ser usado futuramente para:

- cache de dados acessados com frequência
- controle temporário de estados de processamento
- filas de tarefas assíncronas
- desacoplamento entre recebimento da requisição e processamento pesado de imagens

No momento, o Redis é apenas orquestrado no ambiente e configurado via `REDIS_URL`, sem uso direto na lógica da aplicação.

### Por que utilizar Redis neste cenário?

O Redis é útil porque o processamento de imagens aéreas pode ser demorado e gerar alto volume de requisições simultâneas.

Neste cenário, ele pode apoiar a aplicação em pontos como cache, controle de estado temporário e gerenciamento de filas de processamento. Por exemplo, ao receber uma solicitação de processamento, a API poderia registrar a tarefa, colocar o trabalho em uma fila e retornar rapidamente para o cliente, enquanto workers processam as imagens em segundo plano.

Isso evita que a API fique bloqueada durante inferências pesadas e melhora a capacidade de atender múltiplos usuários ao mesmo tempo.

### Como escalar para processar milhares de imagens simultaneamente?

Para processar milhares de imagens simultaneamente, a API não deveria executar todo o processamento diretamente durante a requisição HTTP.

A abordagem recomendada seria separar a aplicação em componentes:

- API FastAPI para autenticação, validação, criação de tarefas e consulta de status
- fila de mensagens para armazenar solicitações de processamento
- workers especializados para executar inferência de IA em paralelo
- storage externo para armazenar imagens e resultados grandes
- banco de dados para persistir metadados, status e histórico

Com essa arquitetura, seria possível escalar horizontalmente a API e os workers de forma independente. Se o gargalo estiver na entrada de requisições, aumentam-se réplicas da API. Se o gargalo estiver na inferência, aumentam-se workers, inclusive em máquinas com GPU.

Também seria importante limitar tamanho de arquivos, controlar concorrência, aplicar rate limiting e usar observabilidade com métricas de fila, tempo médio de processamento e taxa de falhas.

### Como faria o deploy em AWS?

Na AWS, uma arquitetura possível seria:

- API containerizada publicada no Amazon ECS Fargate ou Amazon EKS
- imagens Docker armazenadas no Amazon ECR
- PostgreSQL gerenciado pelo Amazon RDS
- Redis gerenciado pelo Amazon ElastiCache
- arquivos de imagem armazenados no Amazon S3
- fila de processamento com Amazon SQS ou Redis, dependendo do desenho final
- logs e métricas no Amazon CloudWatch
- balanceamento de carga com Application Load Balancer

O fluxo seria: o cliente acessa a API pelo Load Balancer, a API valida a requisição, registra a tarefa no banco, envia o processamento para uma fila e os workers consomem essa fila para executar a inferência. Arquivos grandes seriam enviados diretamente para o S3 usando URLs pré-assinadas, evitando trafegar imagens pesadas pela API.

### Como desacoplaria o processamento pesado da API?

O processamento pesado deve ser executado fora do ciclo da requisição HTTP.

Em vez de a API processar a imagem imediatamente, ela deveria:

- receber a solicitação
- validar usuário, missão e parâmetros
- registrar uma tarefa com status inicial, como `pending`
- enviar a tarefa para uma fila
- retornar um identificador de processamento para o cliente

Depois disso, workers independentes consumiriam a fila, carregariam o modelo de IA, executariam a inferência, salvariam o resultado no banco e atualizariam o status para `success` ou `failed`.

O cliente poderia consultar o andamento usando endpoints de histórico, como:

```http
GET /api/v1/predictions/{id}
GET /api/v1/missions/{mission_id}/predictions
```

Essa separação melhora escalabilidade, resiliência e tempo de resposta da API.

## Parte 5: Questões extras 

# Questão 4. Um usuário envia 500 imagens de drone. O processamento pode levar vários minutos. Descreva uma arquitetura para esse fluxo. 

Para esse fluxo, eu usaria uma arquitetura assíncrona, evitando que a API processe as 500 imagens diretamente durante a requisição HTTP.
Fluxo recomendado:
 1. O usuário solicita o processamento de um lote de imagens.
 2. A API autentica o usuário e valida a missão.
 3. A API cria um registro de processamento em lote no banco com status pending.
 4. As imagens são enviadas diretamente para um storage, como Amazon S3, usando URLs pré-assinadas.
 5. Para cada imagem enviada, a API cria uma tarefa individual de processamento.
 6. As tarefas são publicadas em uma fila, como Redis Queue, Celery com Redis, RabbitMQ ou Amazon SQS.
 7. Workers independentes consomem as tarefas da fila.
 8. Cada worker carrega o modelo de IA e processa uma ou mais imagens.
 9. O resultado de cada imagem é salvo no banco com status success ou failed.
10. O status geral do lote é atualizado conforme o progresso.
11. O usuário consulta o andamento pela API ou recebe atualizações via WebSocket/notification.
Componentes principais:
- FastAPI: recebe requisições, autentica, valida e registra tarefas.
- PostgreSQL: armazena missões, lotes, status e histórico de predições.
- S3 ou storage equivalente: armazena imagens grandes.
- Redis/SQS/RabbitMQ: fila de processamento.
- Workers: executam inferência de IA fora da API.
- Redis: pode armazenar estados temporários, progresso e cache.
- WebSocket ou polling: permite acompanhar progresso do processamento.
Essa arquitetura evita timeout HTTP, permite escalar workers separadamente da API e torna o processamento mais resiliente a falhas.

# Questão 5. O upload de uma imagem de 2 GB não deve passar pela API. Como você resolveria isso? 

Eu resolveria usando upload direto para um storage externo, como Amazon S3, com URL pré-assinada.
Fluxo:
1. O cliente solicita à API uma URL de upload.
2. A API autentica o usuário e valida se ele pode enviar arquivos para aquela missão.
3. A API gera uma URL pré-assinada do S3 com tempo de expiração curto.
4. O cliente envia a imagem de 2 GB diretamente para o S3.
5. A API não recebe o arquivo, apenas registra metadados como nome, tamanho, missão e caminho no storage.
6. Após o upload, o cliente confirma para a API que o arquivo foi enviado.
7. A API cria uma tarefa de processamento apontando para o objeto no S3.
8. Workers baixam/processam a imagem a partir do S3.
Vantagens:
- evita sobrecarregar a API
- reduz uso de memória e banda do backend
- melhora escalabilidade
- permite uploads grandes com controle de acesso
- facilita retomada, expiração e auditoria
A API ficaria responsável por autorização e metadados, não pelo tráfego pesado do arquivo.

# Questão 6. Como impedir que um usuário baixe imagens pertencentes a outro cliente? 

Eu impediria isso aplicando controle de acesso por cliente/tenant em todas as operações.
Estratégia:
1. Cada imagem deve estar vinculada a um client_id, user_id ou organization_id.
2. O token JWT deve conter a identidade do usuário e, se aplicável, o cliente/organização.
3. Ao solicitar download, a API verifica se a imagem pertence ao mesmo cliente do usuário autenticado.
4. Se o usuário não tiver permissão, retorna 403 Forbidden.
5. A API nunca expõe links públicos permanentes.
6. Para arquivos no S3, a API gera URLs pré-assinadas somente após validar permissão.
7. As URLs devem ter expiração curta.
8. O bucket deve permanecer privado.
9. Logs de acesso devem ser registrados para auditoria.
Fluxo seguro:
Usuário solicita download
↓
API valida JWT
↓
API busca metadados da imagem no banco
↓
API compara client_id da imagem com client_id do usuário
↓
Se permitido, gera URL pré-assinada curta
↓
Se negado, retorna 403
Assim, mesmo que um usuário descubra o ID de outra imagem, ele não consegue baixá-la sem autorização.

### Parte 6: Portfólio

https://github.com/ThiagoPanchi/geo-ia

Sistema web para consulta de eventos históricos, com proposta de enriquecimento por IA, persistência de dados georreferenciados e visualização em mapa.

O projeto ainda não foi finalizado. A integração com IA para enriquecer e apoiar as consultas históricas ficou incompleta, e a parte de WebGIS ainda precisa de melhorias, especialmente em usabilidade, organização das camadas e experiência de navegação no mapa.

Mesmo incompleto, o projeto foi importante para explorar conceitos de georreferenciamento, visualização espacial e integração entre backend, IA e interface web. Hoje, eu revisaria algumas decisões técnicas, principalmente a escolha da biblioteca de mapas. Provavelmente substituiria o Mapbox por uma alternativa como Leaflet, buscando uma solução mais simples, aberta e flexível para o contexto do projeto.

### USO DE IA

Durante a execução deste desafio técnico, utilizei ferramentas de IA como apoio ao desenvolvimento, principalmente para acelerar tarefas de estruturação inicial, revisão de organização do projeto, geração de exemplos de código e validação de boas práticas em FastAPI, Docker e arquitetura de APIs.

A IA foi utilizada como ferramenta auxiliar, não como substituta do processo de decisão técnica. As decisões sobre a divisão das etapas, escolha da estrutura do projeto, definição dos módulos, separação entre rotas, schemas, services e repositories, além da ordem de implementação, foram conduzidas e revisadas por mim ao longo do desenvolvimento.

Também revisei o código gerado, ajustei o escopo das implementações e conduzi o trabalho de forma incremental, evitando criar funcionalidades além do necessário em cada etapa. Essa abordagem permitiu manter maior controle sobre a evolução do projeto, validar cada parte separadamente e garantir que a solução permanecesse alinhada aos requisitos do desafio.

A IA também foi usada para apoiar a documentação, especialmente na organização das explicações técnicas sobre autenticação JWT, processamento de imagens, uso de Redis, Docker, PostgreSQL, healthchecks e possíveis estratégias de escalabilidade. Ainda assim, todo o conteúdo foi revisado e adaptado por mim para refletir as decisões tomadas durante o desenvolvimento.

Portanto, o uso de IA neste projeto teve papel de apoio produtivo e revisão técnica, enquanto o planejamento, a validação das decisões, a condução incremental da implementação e a análise final da solução ficaram sob minha responsabilidade.
