 [user-service](https://user.sanekteam.ru/docs#/) и [task-service](https://task.sanekteam.ru/docs#/).
 
# Для теста - ввести логин и пароль
admin - secret 

# Запуск

```bash
docker build -t task_app hw_04/task_service/.
docker build -t user_app hw_04/user_service/.
docker-compose up --build -d
```
## Актуализирована модель архитектуры в Structurizr DSL -> добавлена MongoDB как БД для task_service
[workspace.dsl](../hw_01/workspace.dsl)

### Добавлена проверка на запуск user_service

Теперь контейнер ждет пока поднимется и будет готов принимать запросы контейнер с postgresql
