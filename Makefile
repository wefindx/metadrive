clean:
	find . -type d -name "__pycache__" -exec rm -rf {} + > /dev/null 2>&1
	find . -type f -name "*.pyc" -exec rm -rf {} + > /dev/null 2>&1

isort:
	isort -rc metadrive

lint:
	flake8 --show-source metadrive
	isort --check-only -rc metadrive --diff

test:
	pytest metadrive

all: clean lint test