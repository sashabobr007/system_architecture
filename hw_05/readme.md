 [user-service](https://user.sanekteam.ru/docs#/) и [task-service](https://task.sanekteam.ru/docs#/).
 
# Для теста - ввести логин и пароль
admin - secret 

# Запуск

```bash
docker build -t task_app hw_05/task_service/.
docker build -t user_app hw_05/user_service/.
docker-compose up --build -d
```
## Актуализирована модель архитектуры в Structurizr DSL -> добавлен redis
[workspace.dsl](../hw_01/workspace.dsl)

## Замер производительности (время - 20 сек.)

| Количество потоков | Avg Latency, ms | Total requests|Requests/sec| Avg Latency Redis, ms | Total requests Redis|Requests/sec Redis|
|--------------------|-----------------|------|------|-----------------------|------|------|
| 1                  |40.07|10741|536.74|25.08|20672|1033.37|
| 3                  |41.52|9586|478.99|20.02|21231|1060.72|
| 5                  |38.53|11103|554.75|22.7|20857|1041.98|

_P.S Замер производился на ВМ с 2 ядрами CPU и 2 GB RAM_
