venv:
	source /venv/bin/activate

install:
	pip install -r requirements.txt

fastapi:
	uvicorn main:app --reload --port 8000

fastenv:
	source /venv/bin/activate && uvicorn main:app --reload --port 8000

uninstall:
	pip uninstall -y $(package)

delete_venv:
	rm -rf venv
