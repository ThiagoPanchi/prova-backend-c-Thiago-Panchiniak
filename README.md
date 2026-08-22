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

### Redis

O Redis foi incluído para deixar o ambiente preparado para cenários de maior escala.

Neste contexto, ele pode ser usado futuramente para:

- cache de dados acessados com frequência
- controle temporário de estados de processamento
- filas de tarefas assíncronas
- desacoplamento entre recebimento da requisição e processamento pesado de imagens

No momento, o Redis é apenas orquestrado no ambiente e configurado via `REDIS_URL`, sem uso direto na lógica da aplicação.

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

