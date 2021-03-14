build-image:
	docker build -t web:latest .

run-containers:
	docker run -d --name django-heroku -e "PORT=8765" -e "DEBUG=0" -p 8007:8765 web:latest

destroy-containers:
	docker stop django-heroku && docker rm django-heroku

start-fresh-server:
	$(MAKE) destroy-containers; $(MAKE) build-image && $(MAKE) run-containers


requirements:
	poetry export -f requirements.txt --output requirements.txt

drop-db:
	dropdb physio_db


create-db:
	createdb physio_db


#data seeders
staff-data:
	python manage.py bootstrap_staff_data


reset-db:
	$(MAKE) drop-db && $(MAKE) create-db && python manage.py migrate  && $(MAKE) staff-data


generate-erd:
	python manage.py graph_models -g -a -o eerd.png
