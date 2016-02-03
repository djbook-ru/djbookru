clean:
	find . -name "*.pyc" -exec rm -rf {} \;

test:
	coverage run --source='./src' manage.py test --keepdb
	coverage html -d cover

open_coverage_report:
	google-chrome ./cover/index.html

po_update:
	./po_update.sh

po_compile:
	./po_compile.sh
