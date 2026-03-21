# Локальная установка OpenWebUI с Ollama и Nginx балансировщиком

Этот проект настраивает локальную среду для OpenWebUI, подключенной к моделям через Ollama, с Nginx в качестве reverse proxy и балансировщика нагрузки.

## Компоненты

- **OpenWebUI**: Веб-интерфейс для взаимодействия с AI моделями.
- **Ollama**: Сервис для запуска локальных AI моделей.
- **Nginx**: Reverse proxy и балансировщик нагрузки для OpenWebUI.

## Запуск

1. Убедитесь, что Docker и Docker Compose установлены.

2. Клонируйте или скачайте файлы `docker-compose.yml` и `nginx.conf` в одну папку.

3. Запустите сервисы:
   ```
   docker-compose up -d
   ```

4. Доступ к OpenWebUI через браузер: `http://localhost`

5. Для остановки:
   ```
   docker-compose down
   ```

## Настройка моделей

После запуска Ollama, скачайте нужные модели. Например:
```
docker-compose exec ollama ollama pull llama2
```

Затем в OpenWebUI выберите модель.

## Переменные окружения

Env переменные адаптированы для локальной среды. Основные изменения:
- Отключены SSL и OAuth.
- Включен Ollama API.
- Используется SQLite для базы данных (по умолчанию).
- Упрощены разрешения пользователей.

## Troubleshooting

- Если OpenWebUI не запускается, проверьте логи: `docker-compose logs openwebui`
- Для Nginx: `docker-compose logs nginx`
- Убедитесь, что порты 80 и 11434 свободны.
- Если проблемы с моделями, проверьте Ollama: `docker-compose exec ollama ollama list`

## Безопасность

Это локальная установка для обучения. Не используйте в продакшене без дополнительных настроек безопасности.# bsuir-llm
