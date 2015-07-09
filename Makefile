clean:
	find . -name "*.pyc" -exec rm -rf {} \;

test:
	python manage.py test -k

po_update:
	./po_update.sh

po_compile:
	./po_compile.sh