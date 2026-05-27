
test:
	python -m pytest tests

cov-total:
	python -m pytest --cov=app tests

# coverage:
# 	py.test app/application_manager.py --cov-report xml:cov.xml --cov .
	
coverage:
	py.test app/__init__.py --cov-report xml:cov.xml --cov=app tests


deploy-local:
	docker-compose up --build -d
		
deploy-develop:
	docker-compose up --build -d
	
pull-ollama:
	docker exec -it rag-enterprise-ollama-1 ollama pull llama3