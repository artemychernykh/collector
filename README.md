Сборщик новостей.

Запускать docker-compose.yml.

Docker-compose запускает два контейнера: 
    postgresql - запускает  postgresql и создаёт базу данных news;
    project - запускает parse.py, парсящий rss и добавляющий в базу данных news новости. Parse.py использует parse_article.py, где происходит парсинг текста новости. 