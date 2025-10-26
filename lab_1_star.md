# Лабораторная работа 1 со звездочкой

Попытались взломать сайт redcom.ru

### Ffuf
Попытались ffufить с помощью ffufа и вордлиста fuzz_wordlist.txt [отсюда](https://github.com/OctaYus/Wordlists) но ничего не нашли(. 
Потом использовали сайт [Pentest tools](https://pentest-tools.com/), и нашли много чего

<img width="1280" height="648" alt="image" src="https://github.com/user-attachments/assets/f8611eaf-8375-4dcb-8718-78aa46c6d88d" />

<img width="1280" height="497" alt="image" src="https://github.com/user-attachments/assets/7004672c-c492-4aa7-9414-e85388c63c51" />

И много другого. Восновном много разнообразного gitа.

### Path traversal
Для этих путей:
<img width="1280" height="165" alt="image" src="https://github.com/user-attachments/assets/77a35111-3f66-488c-aa9d-7f6e12f02b95" />
обнаруженных ffufом, пошли в родительские папки. Нашли версию сайта 2022 года. Звучит как успех.
<img width="733" height="1129" alt="image" src="https://github.com/user-attachments/assets/d73015f5-4e21-4ffe-a993-ef36e16d58da" />

<img width="808" height="1132" alt="image" src="https://github.com/user-attachments/assets/5f57a37c-8714-41b4-b591-3df1c8a0c5d3" />

### XSS
Попытались ввести скрипт в поле для текста
<img width="810" height="466" alt="image" src="https://github.com/user-attachments/assets/717d26c4-197e-4831-8bf8-02a617c5a26d" />

Не получилось(

<img width="879" height="503" alt="image" src="https://github.com/user-attachments/assets/afa1fc8c-4827-451f-a4d2-38debadcc005" />

### Подытожим
Реальных уязвимостей не нашли, но зато явно попали куда не нужно было (на старую версию сайта).
