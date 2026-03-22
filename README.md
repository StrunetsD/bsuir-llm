# OpenWebUI с Load Balancing

Мини-система для тестирования OpenWebUI с балансировкой нагрузки между тестовыми LLM серверами.

## Архитектура

```
┌─────────────────┐    ┌─────────────┐    ┌─────────────────┐
│   Browser       │────│   Nginx     │────│   OpenWebUI     │
│   localhost:80  │    │   :80       │    │   :8080         │
└─────────────────┘    └─────────────┘    └─────────────────┘
                                │
                                ▼
                       ┌─────────────────┐
                       │   Nginx-LB      │
                       │   :8080         │
                       └─────────────────┘
                                │
                    ┌───────────┼───────────┐
                    │           │           │
           ┌────────▼───┐ ┌────▼───┐ ┌────▼───┐
           │ Test-Server│ │ Test-  │ │ Test-  │
           │     1      │ │ Server │ │ Server │
           │   :8000    │ │   2    │ │   3    │
           └────────────┘ └────────┘ └────────┘
```

## Быстрый старт

```bash
cp .env.example .env

docker compose up --build

docker compose ps

open http://localhost

curl http://localhost:8080/v1/models
```

Все чувствительные и значимые параметры вынесены в `.env`. Файл `.env` не коммитится, для репозитория используется только `.env.example`.

## Компоненты

### OpenWebUI
- **Порт**: 8080 (внутренний)
- **База данных**: PostgreSQL
- **LLM API**: Через nginx-lb (localhost:8080/v1)

### PostgreSQL
- **Порт**: 5432
- **База**: openwebui
- **Пользователь**: задаётся через `.env`

### Nginx (Frontend)
- **Порт**: 80
- Проксирует запросы к OpenWebUI

### Nginx-LB (Load Balancer)
- **Порт**: 8080
- Балансировка между test-server-1 и test-server-2
- Алгоритм: least_conn

### Test Servers
- **test-server-1/2**: Python Flask серверы
- Имитируют OpenAI-compatible API
- Эндпоинты: /v1/models, /v1/chat/completions, /v1/embeddings, /health

## Тестирование балансировки

```bash

for i in {1..10}; do
  curl -s http://localhost:8080/v1/models | jq -r '.data[0].server_id'
done

# Должно показать чередование: server-1, server-2, server-1, server-2...
```

## Логи

```bash
docker compose logs -f

docker compose logs -f openwebui
docker compose logs -f nginx-lb
```

## Остановка

```bash
docker compose down
docker compose down -v  # с удалением volumes
```

## Разработка

### Добавление нового test-server

1. Скопировать блок test-server-1 в docker-compose.yml
2. Изменить имя на test-server-3
3. Добавить в upstream llm_backend в nginx-lb.conf

### Масштабирование

```bash
docker compose up --scale test-server-1=2
```
