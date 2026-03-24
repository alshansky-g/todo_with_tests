test:
	python src/manage.py test functional_tests

test-docker:
	TEST_SERVER=localhost:8888 python src/manage.py test functional_tests

deploy:
	set -a && . $(CURDIR)/.env && set +a && ansible-playbook --user=gleb -i alshansky-g.ru, infra/deploy-playbook.yaml -vv --ask-become-pass