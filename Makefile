.PHONY: all help clean test open_coverage_report po_update po_compile

# target: all - Default target. Does nothing.
all:
	@echo "Hello $(LOGNAME), nothing to do by default"
	@echo "Try 'make help'"

# target: help - Display callable targets.
help:
	@egrep "^# target:" [Mm]akefile

# target: clean - Remove .pyc files.
clean:
	find . -name "*.pyc" -exec rm -rf {} \;

# target: test - Run tests with coverage.
test:
	coverage run --source='./src' manage.py test --keepdb
	coverage html -d cover

# target: open_coverage_report - Open coverage report.
open_coverage_report:
	google-chrome ./cover/index.html

# target: po_update - Update .po files.
po_update:
	cd src && ../manage.py makemessages --locale ru

# target: po_compile - Compile .po files.
po_compile:
	./po_compile.sh
