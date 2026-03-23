test:
	python src/manage.py test functional_tests

test-docker:
	TEST_SERVER=localhost:8888 python src/manage.py test functional_tests --failfast