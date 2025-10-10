# Лабораторня работа 1. Nginx: трагикомедия в трех актах
## Дисклеймер
Между описанием лабораторной работы буду проскакивать несмешные картинки с несмешными подписями (см. пример 1). 
Читателю может показаться что они никак не помогают описанию. Однако это не так: для того, чтобы описание 
существовало, необходимо, чтобы пишущий его человек оставался в сравнительно здравом рассудке, а с этим 
подобные картинки очень помогают.
<p align=center>
  <img width="389" height="391" alt="image" src="https://github.com/user-attachments/assets/d43a64a4-6618-42bb-aa3e-5ebc14c5d114" />
</p>
<p align=center>
  Рис. 1. Пример 1
</p>

## Осознание nginx
Установили nginx, создали конфиг файл с одним хостом, вовзращающий плейсхолдерную страничку index.html, дабы понять, как вообще этот зверь работает (скриншотов ранней эпохи, увы, сделать не додумались,так что скрин снизу - это реплика).

<img width="979" height="325" alt="image" src="https://github.com/user-attachments/assets/6ff3ebc1-a906-4c38-a0ad-bf58b862125b" />

Отправили запрос иииии барабанная дробь... Получили ошибку 403 verboden. Поняли, что дело в том, что файлы для сайта лежат в домашней папке, а у nginx к ней нет доступа. Хранить котиков в корневой папке нам показалось грешным, так что, дабы не разбираться с тем, кто такой nginx и как дать права конкретно ему, выдали вообще всем пользователям (благо их кроме нас с nginxом и нет) права исполнять файлы из ~:

```
chmod ~ 701
```

Заработало.
<p align=center>
  <img width="651" height="363" alt="image" src="https://github.com/user-attachments/assets/2e8399f9-7551-44f3-bcf8-174c667ef6b5" />
</p>

## Создание сертификата
Создали самописный сертификат.

```
openssl req -x509 -newkey rsa:4096 -keyout key.pem -out cert.pem -sha256 -days 3650 -nodes -subj "/C=RU/ST=Russia/L=StPetersburg/O=MedievalHorses/OU=MedievalPoni
es/CN=localhost"
```

<img width="879" height="349" alt="image" src="https://github.com/user-attachments/assets/6427d996-f2f7-4748-9d7b-63339187111e" />

## Собственно работа
Написали nginx.conf для сайта: два сервера слушают 443 порт и отвечают на запросы по соответствующему доменному имени, первый переводит http запроы на https. Для каждого сервера создали aliasы к папкам с используемыми файлами. Оба хоста используют один и тот же сертификат.

<img width="1199" height="1134" alt="image" src="https://github.com/user-attachments/assets/ccacd895-6bb8-44cb-a39d-aa7763053304" />


Итоговая структура проекта:

<img width="706" height="528" alt="image" src="https://github.com/user-attachments/assets/a3f223df-1ce8-42e6-8221-04e9e433fe98" />

Запустили nginx (и заставили учесть обновления в конфигурационном файле):

```
sudo nginx
sudo nginx -s reload
```

Проверяем /etc/hosts. Наши серверы там есть. Ура.

<img width="403" height="121" alt="image" src="https://github.com/user-attachments/assets/7347b6d4-5d33-4603-848b-11d631285ef5" />

При запросе браузер ругается на наш сертификат, так как он самописный. Убеждаем его, что знаем, что делаем. 

<img width="571" height="333" alt="image" src="https://github.com/user-attachments/assets/ffa68205-6ba9-4909-8c09-559d53c7f73d" />

Так выглядят наш сайты:

Первый:
<img width="1637" height="1017" alt="image" src="https://github.com/user-attachments/assets/f81848ea-7d19-4230-8b07-0914ed8b44ba" />

Второй:
<img width="1552" height="1018" alt="image" src="https://github.com/user-attachments/assets/e82252c9-74ec-475e-9410-4c6b18d098f4" />

Проверили, что работают aliasы

<img width="877" height="361" alt="image" src="https://github.com/user-attachments/assets/233fcf29-042b-47ec-9702-4867ad3a887f" />
<p align=center>
  <img width="879" height="581" alt="image" src="https://github.com/user-attachments/assets/03452a7a-109e-4238-8f48-6d7429c03afe" />
</p>






