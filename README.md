# hasker

Hasker: Poor Man's Stackoverflow



### Запуск агента celery

На сервере необходимо иметь запущенный redis-server  

./venv/bin/celery -A haskerengine worker -n normal@haskerengine & ./venv/bin/celery -A haskerengine beat -l INFO --pidfile=celerybeat1.pid