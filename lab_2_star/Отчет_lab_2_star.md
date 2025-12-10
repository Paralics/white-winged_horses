Работу docker compose будем проводить на примере связки веб-приложения на Flask,  базы данных MySQL и nginx.


## Плохой docker compose:
```
services:
  db:
    image: mysql:latest  # версия latest
    container_name: db-mysql
    environment:
      MYSQL_ROOT_PASSWORD: root_password  # пароли в явном виде
      MYSQL_DATABASE: app_db
      MYSQL_USER: app_user
      MYSQL_PASSWORD: app_password
    volumes:  # данные теряются при перезапуске контейнера
      - ./init.sql:/docker-entrypoint-initdb.d/init.sql
    ports:
      - "3306:3306"  # доступ к базе данных извне
    restart: always  # будет перезапускаться даже при остановке с ошибкой (риск зацикливания)


  app:
    build: .
    container_name: predict-app
    environment:
      DB_HOST: db
      DB_NAME: app_db
      DB_USER: app_user
      DB_PASSWORD: app_password
    ports:
      - "5000:5000"  # доступ не только через nginx
    depends_on:
      - db  # нет healthcheck
    restart: always  # будет перезапускаться даже при остановке с ошибкой


  nginx:
    image: nginx:latest  # версия latest
    ports:
      - "80:80"
    volumes:
      - ./nginx.conf:/etc/nginx/nginx.conf
    depends_on:
      - app
    restart: always  # будет перезапускаться даже при остановке с ошибкой
```

### Плохие практики:
1. Использование :latest тегов - нет контроля версий, что нарушает принцип воспроизводимости окружения и приводит к постоянной загрузке новых образов.
2. Пароли в открытом виде - безопасность под угрозой, невозможность использования разных паролей для разных окружений.
3. Открытые порты БД - уязвимость безопасности, можно подключиться с любого устройства сети и из Интернета, если проброшены порты на роутере.
4. Открытый порт приложения - нарушение архитектуры, доступ должен быть только через nginx.
5. Нет healthcheck - без проверки доступности сервиса могут возникать ошибки, например, попытка подключения к базе данных, когда та ещё не готова принимать подключения.
6. Нет постоянного хранилища - записи в БД будут потеряны после перезапуска контейнера.
7. Перезапуск контейнера всегда - может привести к зацикливанию, если есть ошибка, приводящая к завершению работы контейнера

### Запуск:
<img width="1889" height="596" alt="Screenshot 2025-12-08 195908" src="https://github.com/user-attachments/assets/1d3dc4e9-4304-4f2e-acaf-88e9a1ac5968" />

<img width="1888" height="116" alt="image" src="https://github.com/user-attachments/assets/d3295901-390b-4358-bf3f-528ece334e03" />

----
Видим, что БД доступна с localhost, приложение - через порт 5000 и через nginx
<img width="1870" height="579" alt="image" src="https://github.com/user-attachments/assets/cf86581d-6c54-4876-8112-85c2211d03a8" />

----
В браузере всё тоже работает
<img width="807" height="230" alt="image" src="https://github.com/user-attachments/assets/3c33199c-8468-47e6-be3e-d194f4bf755f" />

<img width="299" height="239" alt="image" src="https://github.com/user-attachments/assets/a0d717db-ec0f-4b2a-9130-6df14f791791" />

<img width="1888" height="193" alt="image" src="https://github.com/user-attachments/assets/eaf067f1-a9a6-44d2-aeda-cf8ece2a008a" />


----
Ещё в процессе возникла интересная **ошибка**: до запуска этого файла был запущен другой docker compose, в котором создавалось постоянное хранилище и использовалась версия MySQL 8.0. При повторном запуске создался контейнер с таким же именем, и существующее хранилище неявно вмонтировалось в новый контейнер. Так как в новом контейнере использовалась версия latest, возник конфликт версий, а из-за режима restart: always база просто перезапускалась каждый раз при возникновении этой ошибки.
<img width="1910" height="763" alt="image" src="https://github.com/user-attachments/assets/ec9cc254-8af2-4d45-8c92-e57e4a506780" />


## Хороший docker compose:
```
volumes:  # создаем постоянное внутреннее хранилище для записей бд
  db_data:

services:
  db:
    image: mysql:8.0  # конкретная версия
    container_name: db-mysql
    environment:
      MYSQL_ROOT_PASSWORD: ${DB_ROOT_PASSWORD}
      MYSQL_DATABASE: ${DB_NAME}
      MYSQL_USER: ${DB_USER}
      MYSQL_PASSWORD: ${DB_PASSWORD}
    volumes:
      - db_data:/var/lib/mysql  # данные сохраняются в volume
      - ./init.sql:/docker-entrypoint-initdb.d/init.sql:ro  # readonly
    # доступа к базе данных извне нет, только внутри сети, в крайнем случае можно открыть доступ с localhost
    healthcheck:  # проверка готовности бд
      test: [ "CMD", "mysqladmin", "ping", "-h", "localhost" ]
      timeout: 20s
      retries: 10
      interval: 30s
      start_period: 40s
    restart: unless-stopped  # не перезапускается после череды ошибок или ручной остановки


  app:
    build: .
    container_name: predict-app
    environment:
      DB_HOST: db
      DB_NAME: ${DB_NAME}
      DB_USER: ${DB_USER}
      DB_PASSWORD: ${DB_PASSWORD}  # пароли в файле .env
    # доступа к приложению извне нет, только через nginx
    depends_on:
      db:
        condition: service_healthy  # доступ только по готовности
    restart: unless-stopped  # не перезапускается после череды ошибок или ручной остановки


  nginx:
    image: nginx:1.25-alpine  # конкретная версия
    ports:
      - "80:80"
    volumes:
      - ./nginx.conf:/etc/nginx/nginx.conf:ro  # readonly
    depends_on:
      - app
    restart: unless-stopped  # не перезапускается после череды ошибок или ручной остановки
```

### Исправлено в docker-compose-good.yml:
1. Объявлены конкретные версии образов - воспроизводимость окружения и контроль за обновлениями
2. Пароли вынесены в .env
3. Закрыт порт БД - доступ только из контейнера
4. Закрыт порт приложения - доступ только через nginx
5. Добавлен healthcheck для БД (для которой это критично), есть проверка в depends_on - `condition: service_healthy`
6. Добавлен том для данных - `db_data:/var/lib/mysql`
7. `restart: unless-stopped` - останавливает контейнер после череды ошибок или ручной остановки
8. Файлы конфигурации монтируются с флагом :ro (read-only), что предотвращает их модификацию из контейнера, обеспечивая безопасность и целостность

### Запуск:
Контейнеры запускаются
<img width="1872" height="737" alt="image" src="https://github.com/user-attachments/assets/5f5944f3-2cee-4741-b4a5-10c44b366e69" />
<img width="1884" height="877" alt="image" src="https://github.com/user-attachments/assets/037c6f09-c11e-4b6c-a9e5-0613a843e22f" />
<img width="1882" height="788" alt="image" src="https://github.com/user-attachments/assets/ab812e61-932c-4649-a940-597660d8a2b3" />

---
<img width="665" height="257" alt="image" src="https://github.com/user-attachments/assets/8f3cc6f5-cfe7-4bbc-96cc-3c6c612523eb" />

<img width="451" height="300" alt="image" src="https://github.com/user-attachments/assets/b959041f-c57a-40ad-bfa1-e4866347f85c" />

*Приложение грозу не любит*

----
Проверим, что контейнеры видят друг друга по сети
<img width="1544" height="954" alt="image" src="https://github.com/user-attachments/assets/a92f9260-e931-4846-a1e0-4c1ccf413525" />
<img width="1354" height="868" alt="image" src="https://github.com/user-attachments/assets/e4413cf5-59d8-4893-85ba-43cf15a74a08" />

Но доступ снаружи есть только к nginx
<img width="1436" height="256" alt="image" src="https://github.com/user-attachments/assets/c0bd423a-c072-460d-8678-b6b1647a9272" />

## Изоляция контейнеров
Теперь сделаем так, чтобы контейнеры совсем не видели друг друга по сети: создадим для каждого контейнера изолированную сеть

```
volumes:
  db_data:

services:
  db:
    command: --default-authentication-plugin=mysql_native_password
    image: mysql:8.0
    container_name: db-mysql
    environment:
      MYSQL_ROOT_PASSWORD: ${DB_ROOT_PASSWORD}
      MYSQL_DATABASE: ${DB_NAME}
      MYSQL_USER: ${DB_USER}
      MYSQL_PASSWORD: ${DB_PASSWORD}
    volumes:
      - db_data:/var/lib/mysql
      - ./init.sql:/docker-entrypoint-initdb.d/init.sql
    healthcheck:
      test: [ "CMD", "mysqladmin", "ping", "-h", "localhost" ]
      timeout: 20s
      retries: 10
      interval: 30s
      start_period: 40s
    restart: unless-stopped
    networks:
      - db_network


  app:
    build: .
    container_name: predict-app
    environment:
      DB_HOST: db
      DB_NAME: ${DB_NAME}
      DB_USER: ${DB_USER}
      DB_PASSWORD: ${DB_PASSWORD}
    depends_on:
      db:
        condition: service_healthy
    restart: unless-stopped
    networks:
      - app_network


  nginx:
    image: nginx:1.25-alpine
    ports:
      - "80:80"
    volumes:
      - ./nginx.conf:/etc/nginx/nginx.conf:ro
    depends_on:
      - app
    restart: unless-stopped
    networks:
      - web_network


networks:
  db_network:
    driver: bridge
  app_network:
    driver: bridge
  web_network:
    driver: bridge
```

Но тогда наш сервис не запустится, так как контейнеры не смогут общаться между собой. Начнется череда перезапусков из-за ошибок.
<img width="1378" height="355" alt="image" src="https://github.com/user-attachments/assets/993f235d-005e-4644-beef-feea9e5acb58" />

Так что создадим две изолированные сети и будем использовать app как шлюз:

```
volumes:
  db_data:

services:
  db:
    command: --default-authentication-plugin=mysql_native_password
    image: mysql:8.0
    container_name: db-mysql
    environment:
      MYSQL_ROOT_PASSWORD: ${DB_ROOT_PASSWORD}
      MYSQL_DATABASE: ${DB_NAME}
      MYSQL_USER: ${DB_USER}
      MYSQL_PASSWORD: ${DB_PASSWORD}
    volumes:
      - db_data:/var/lib/mysql
      - ./init.sql:/docker-entrypoint-initdb.d/init.sql
    healthcheck:
      test: [ "CMD", "mysqladmin", "ping", "-h", "localhost" ]
      timeout: 20s
      retries: 10
      interval: 30s
      start_period: 40s
    restart: unless-stopped
    networks:
      - db_app_network


  app:
    build: .
    container_name: predict-app
    environment:
      DB_HOST: db
      DB_NAME: ${DB_NAME}
      DB_USER: ${DB_USER}
      DB_PASSWORD: ${DB_PASSWORD}
    depends_on:
      db:
        condition: service_healthy
    restart: unless-stopped
    networks:
      - db_app_network
      - app_web_network


  nginx:
    image: nginx:1.25-alpine
    ports:
      - "80:80"
    volumes:
      - ./nginx.conf:/etc/nginx/nginx.conf:ro
    depends_on:
      - app
    restart: unless-stopped
    networks:
      - app_web_network


networks:
  db_app_network:
    driver: bridge
  app_web_network:
    driver: bridge
```
Теперь всё работает

<img width="643" height="222" alt="Screenshot 2025-12-09 202015" src="https://github.com/user-attachments/assets/2836b65d-a51e-46d0-9f83-2716439d3fbe" />

<img width="655" height="311" alt="image" src="https://github.com/user-attachments/assets/bceed6cb-8179-4975-9a08-9daaec5b1116" />

_Онет, передали секрет! (хахаха)_

### Список сетей:
<img width="1333" height="163" alt="image" src="https://github.com/user-attachments/assets/1a172443-c605-4591-97b3-0e1c3189e749" />

### Информация о сетях:

**Сеть для nginx**

<img width="961" height="95" alt="image" src="https://github.com/user-attachments/assets/5169c811-2d0a-43ef-840d-eb1bed607eba" />
<img width="1085" height="372" alt="image" src="https://github.com/user-attachments/assets/a20f8599-f848-416b-b222-257b85dd5d8d" />

**Сеть для БД**

<img width="907" height="71" alt="image" src="https://github.com/user-attachments/assets/6c98319a-3a3f-4320-aa19-c64d2639ec3f" />
<img width="1104" height="355" alt="image" src="https://github.com/user-attachments/assets/aa266ef7-75c3-4ca6-832c-0aba53062527" />

**Nginx не видит базу данных**

<img width="1577" height="51" alt="image" src="https://github.com/user-attachments/assets/1bf95e66-dcc6-43d2-be1f-d34974256849" />


### Как работает такая изоляция?
Для каждого кластера создаётся своя изолированная виртуальная сеть Docker. Внутри одной сети контейнеры могут обращаться друг к другу по IP или по имени контейнера (так как в Docker есть встроенный DNS), но напрямую контейнеры, находящиеся в разных сетях, общаться не могут. Взаимодействие происходит через контейнер-маршрутизатор, подклученный сразу к нескольким сетям.

### Вывод
Docker compose предоставляет прикольные возможности для конфигурации контейнеров и настройки сетевого соединения между сервисами. Поначалу было сложно разобраться, и постоянно возникали ошибки с базой данных, но в итоге всё получилось! Нам понравилось!

<img width="427" height="320" alt="image" src="https://github.com/user-attachments/assets/5bd4a568-9156-4baa-8a20-c921abad65e3" />
