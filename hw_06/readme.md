 [user-service](https://user.sanekteam.ru/docs#/) и [task-service](https://task.sanekteam.ru/docs#/).
 
_P.S. на ВМ kafka очень много требует памяти и как
следствие все виснет. Поэтому там версия 5-ой лабы._

# Для теста - ввести логин и пароль
admin - secret 

# Запуск

```bash
docker build -t task_app hw_06/task_service/.
docker build -t user_app hw_06/user_service/.
docker build -t consumer hw_06/consumer_service/.
docker-compose up --build -d
```
## Актуализирована модель архитектуры в Structurizr DSL -> добавлен redis
[workspace.dsl](../hw_01/workspace.dsl)
