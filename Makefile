start:
	uvicorn src.api:app --workers 1

benchmark:
	python benchmark/concurrency_test.py

evaluate:
	python evaluation/run_evaluation.py
