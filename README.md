pip freeze > requirements.txt
docker-compose up
flak8 .  before running server so i make sure everything is fine
write unit tests and integration tests

docker-compose run --rm app python manage.py makemigrations
docker-compose run --rm app python manage.py migrate
docker-compose run --rm app python manage.py fetch_posts_comments


use celery as task runner
redis to work alongside with celery