build:
	docker-compose build

up:
	docker-compose up -d

down:
	docker-compose down --remove-orphans

gViz:
	pyreverse --output-directory docs twitter
	dot -Tpng docs/classes.dot -o docs/classes.png
	dot -Tpng docs/packages.dot -o docs/packages.png
