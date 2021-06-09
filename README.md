# hasker

Hasker: Poor Man's Stackoverflow



### Запуск агента celery

На сервере необходимо иметь запущенный redis-server  

./venv/bin/celery -A haskerengine worker -n normal@haskerengine & ./venv/bin/celery -A haskerengine beat -l INFO --pidfile=celerybeat1.pid


### Использование API

curl -H 'Accept: application/json' -u user:**** http://127.0.0.1:8000/api/get_users/

