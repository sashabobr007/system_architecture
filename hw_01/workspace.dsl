workspace {
    name "Планирование задач"
    description "Архитектура сервиса для планирования задач на примере https://www.leadertask.ru/"

    !identifiers hierarchical

    model {
        user = person "Пользователь"
        owner = person "Владелец"

        notification_system = softwareSystem "Notification System" {
            tags "ExternalSystem"
        }

        task_system = softwareSystem "Task Planning System" {

            -> notification_system "Отправка уведомлений" "HTTPS"

            db = container "Database PostgreSQL" {
                technology "PostgreSQL 15"
                tags "Database"
            }

            redis = container "Redis Cache" {
                technology "Redis 7.0"
                tags "Cache"
                description "Кеш для данных пользователей"
            }

            mongo = container "Database Mongo" {
                technology "MongoDB 5.0"
                tags "Database"
            }
        
            userService = container "User Service" {
                technology "Python FastAPI"
                description "Обработка данных о пользователях"
                -> db "Сохранение и получение информации о пользователях" "PostgreSQL Driver"
                -> redis "Кеширование данных пользователей" "Redis Client"
            }   

            taskService = container "Task Service" {
                technology "Python FastAPI"
                description "Управление задачами и целями"
                -> mongo "Сохранение и получение информации о задачах и целях" "MongoDB Driver"
            }

            api = container "API Gateway" {
                technology "Nginx"
                -> userService "Создание/поиск пользователей" "HTTPS"
                -> taskService "Создание/поиск/удаление задач и целей" "HTTPS"
                -> notification_system "Отправить уведомление" "HTTPS"

            }

            wa = container "Web Application"{
                technology "JS, React"
                -> api "Добавление/просмотр/удаление цели/задачи/пользователя" "HTTPS"
            }
            
        }

        owner -> task_system "Добавляет и удаляет пользователей"
        owner -> notification_system "Получает уведомления"
        user -> notification_system "Получает уведомления"
        user -> task_system "Добавляет цели, задачи, просматривает и закрывает их"

        user -> task_system.wa "Добавить/просмотреть/закрыть цель/задачу"
        owner -> task_system.wa "Добавить/удалить пользователя в/из организацию"

    }

    views {
        systemContext task_system "SystemContext" {
            include *
            autolayout lr
        }

        container task_system {
            include *
            autolayout lr
        }
        dynamic task_system "uc01" "Создание и получение задачи" {
            autoLayout lr

            user -> task_system.wa "Создать новую задачу на пути к цели"
            task_system.wa -> task_system.api "POST /goals/{goalId}/tasks"
            task_system.api -> task_system.taskService "POST /goals/{goalId}/tasks"
            task_system.taskService -> task_system.mongo "tasks_collection.insert_one(task_data)"
            
            user -> task_system.wa "Получить список задач цели"
            task_system.wa -> task_system.api "GET /goals/{goalId}/tasks"
            task_system.api -> task_system.taskService "GET /goals/{goalId}/tasks" 
            task_system.taskService -> task_system.mongo "tasks_collection.find({'goal_id': goal_id})"
        }

        styles {
            element "Element" {
                color #ffffff
            }
            element "Person" {
                background #08427b
                shape person
            }
            element "ExternalSystem" {
                background #c0c0c0
                color #ffffff
            }
            element "Software System" {
                background #438dd5
            }
            element "Container" {
                background #3B82CF
            }
            element "Database" {
                shape cylinder
            }
            element "Cache" {
                shape pipe
            }
        }
    }

    configuration {
        scope softwaresystem
    }

}