pip freeze > requirements.txt
docker-compose up
flak8 .  before running server so i make sure everything is fine
write unit tests and integration tests

docker-compose run --rm app python manage.py makemigrations
docker-compose run --rm app python manage.py migrate
docker-compose run --rm app python manage.py fetch_posts_comments


sensitive Data should not be pushed, should be added to gitignore, all env vars are env file .env.dev

use celery as task runner
rabbitmq to work alongside with celery

use normal uer, not root in docker

changed the settings for Databases.


 django.db.utils.OperationalError: connection to server on socket "/var/run/postgresql/.s.PGSQL.5432" failed: No such file or directory