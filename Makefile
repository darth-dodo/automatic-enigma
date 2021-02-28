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