clean:
	find . -name "*.pyc" -exec rm -rf {} \;

test:
	python manage.py test
