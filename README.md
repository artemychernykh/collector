—борщик новостей.

«апускать docker-compose.yml.
Docker-compose запускает два контейнера: 
    postgresql - запускает  postgresql и создаЄт базу данных news;
    project - запускает parse.py, парс€щий rss и добавл€ющий в базу данных news новости. Parse.py использует parse_article.py, где происходит парсинг текста новости. 