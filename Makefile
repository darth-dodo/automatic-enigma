build-image:
	docker build -t web:latest .

run-containers:
	docker run -d --name django-heroku -e "PORT=8765" -e "DEBUG=0" -p 8007:8765 web:latest

destroy-containers:
	docker stop django-heroku && docker rm django-heroku

start-fresh-server:
	$(MAKE) destroy-containers; $(MAKE) build-image && $(MAKE) run-containers


requirements:
	poetry export --dev -f requirements.txt --output requirements.txt

drop-db:
	dropdb physio_db


create-db:
	createdb physio_db


#data seeders
staff-data:
	python manage.py bootstrap_staff_data

patient-data:
	python manage.py bootstrap_patient_data

appointment-data:
	python manage.py bootstrap_appointment_data

finance-data:
	python manage.py bootstrap_finance_with_mock_data


reset-db:
	$(MAKE) drop-db && $(MAKE) create-db && python manage.py migrate  && $(MAKE) staff-data && $(MAKE) patient-data && $(MAKE) appointment-data && $(MAKE) finance-data


generate-inheritance-eerd:
	python manage.py graph_models -g -a -v 2 -o eerd.png

generate-simple-eerd:
	python manage.py graph_models -E -g -a -v 2 -o simple-eerd.png
