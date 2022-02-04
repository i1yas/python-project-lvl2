install:
	poetry install

package-install:
	python3 -m pip install --user dist/*.whl --force-reinstall
	
build:
	poetry build
	
publish:
	poetry publish --dry-run

lint:
	poetry run flake8 gendiff 

test:
	poetry run pytest
