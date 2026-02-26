# OpenSearch stack con inxestión vía Data Prepper

Repositorio baseado en Docker Compose para despregar un contorno centrado en **OpenSearch** como motor de almacenamento e indexación de datos, empregando **Data Prepper** como compoñente intermedio de inxestión e uns produtores HTTP en Python como xeradores de eventos.

O foco principal da arquitectura é OpenSearch. Data Prepper actúa como capa de entrada e transformación previa á indexación.

---

## Servizos definidos

O ficheiro `docker-compose.yml` orquestra os seguintes servizos:

### OpenSearch

Motor principal do sistema.

Responsabilidades:

- Almacenamento de documentos
- Indexación de eventos
- Xestión de índices
- Exposición de API REST para consulta e administración
- Base para análises e visualización posterior

É o compoñente central da arquitectura.

---

### Data Prepper

Servizo intermedio que actúa como pasarela de inxestión.

Responsabilidades:

- Recepción de eventos vía HTTP
- Aplicación de pipelines definidos en YAML
- Envío dos eventos procesados a OpenSearch

Non é o elemento principal do repositorio, senón un complemento que facilita a integración cos produtores.

---

### Producers HTTP

Contedores Python que xeran ou recollen datos e os envían a Data Prepper mediante peticións HTTP.

A súa función é alimentar o sistema con eventos estruturados.

---

## Estrutura do repositorio

```
.
├── docker-compose.yml
├── .env
├── data-prepper-config.yaml
├── pipelines/
└── producers/
```

---

## Descrición dos ficheiros e cartafoles

### docker-compose.yml

Define a infraestrutura completa:

- Servizo OpenSearch
- Servizo Data Prepper
- Servizos producers
- Redes internas
- Portos publicados
- Volumes persistentes
- Variables de contorno

É o punto de entrada para levantar o stack completo.

---

### .env

Ficheiro de variables de contorno empregado por Docker Compose para parametrizar a configuración do despregue.

Permite modificar valores sen alterar os ficheiros principais.

---

### data-prepper-config.yaml

Configuración xeral do servizo Data Prepper.

Inclúe parámetros globais e referencia aos pipelines que deben cargarse no arranque.

---

### pipelines/

Cartafol onde se almacenan os **pipelines de Data Prepper en formato YAML**.

Cada pipeline define:

- Fonte de entrada de eventos
- Posibles procesadores intermedios
- Destino final en OpenSearch

Representa a capa de integración entre os produtores e OpenSearch.

---

### producers/

Cartafol que contén o código dos produtores en Python.

Inclúe:

- Scripts de xeración/envío de eventos
- Ficheiro `requirements.txt` coas dependencias

Estes scripts envían eventos estruturados ao endpoint HTTP de Data Prepper, que posteriormente os indexa en OpenSearch.

---

## Arquitectura lóxica

```
Producers HTTP → Data Prepper → OpenSearch
```

OpenSearch é o destino final e compoñente central do sistema.  
Data Prepper actúa como mecanismo de inxestión e encamiñamento de eventos cara ao motor de indexación.

---

## Obxectivo do repositorio

Dispor dunha estrutura organizada para:

- Despregue dun nodo OpenSearch
- Inxestión estruturada de eventos
- Separación clara entre infraestrutura, procesamento e xeración de datos
- Facilitar ampliacións futuras (novos pipelines, novos produtores ou novas integracións)

O deseño modular permite evolucionar o sistema mantendo OpenSearch como núcleo da arquitectura.