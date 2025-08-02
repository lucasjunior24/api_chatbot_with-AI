deploy-local:
	docker build -t api_ai_local .
	docker-compose -f compose/compose-local/docker-compose.yaml up -d
		
deploy-develop:
	docker build -t api_ai_develop .
	docker-compose -f compose/compose-develop/docker-compose.yaml up -d

test:
	python -m pytest tests

cov-total:
	python -m pytest --cov=app tests

# coverage:
# 	py.test app/application_manager.py --cov-report xml:cov.xml --cov .
	
coverage:
	py.test app/__init__.py --cov-report xml:cov.xml --cov=app tests


local-mongo:
	docker-compose -f compose/compose-local/mongo.yaml up -d
