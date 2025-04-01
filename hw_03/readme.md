# 1. Создайте HTTP REST API для сервисов, спроектированных в первом задании (попроектированию). Должно быть реализовано как минимум два сервиса(управления пользователем, и хотя бы один «бизнес» сервис)

Созданы - [user-service](https://user.sanekteam.ru/docs#/) и [task-service](https://task.sanekteam.ru/docs#/).

# 2. Сервис должен поддерживать аутентификацию с использованием JWT-token (Bearer)

Используется, как в примере с гита курса.

# 3. Должен быть отдельный endpoint для получения токена по логину/паролю

https://user.sanekteam.ru/auth/token

# 4. Сервис должен реализовывать как минимум GET/POST методы

Сделаны помимо еще put и delete методы

# 5. Данные сервиса должны храниться в памяти (базу данных добавим потом)

Сделано

# 6. В целях проверки должен быть заведён мастер-пользователь (имя admin, пароль secret)

Сделано, как в примере с гита курса (admin - secret).

# 7. Сделайте OpenAPI спецификацию и сохраните ее в корне проекта

[openapi_task.json](task_service/openapi_task.json)

[openapi_user.json](user_service/openapi_user.json)

# 8. Актуализируйте модель архитектуры в Structurizr DSL

Актуализированы технологии (Java -> Python FastAPI)

[workspace.dsl](../hw_01/workspace.dsl)

# 9. Ваши сервисы должны запускаться через docker-compose коммандой docker-compose up (создайте Docker файлы для каждого сервиса)

[Dockerfile](user_service/Dockerfile)

[Dockerfile](task_service/Dockerfile)

[docker-compose.yml](../hw_01/docker-compose.yml)