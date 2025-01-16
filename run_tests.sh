#!/bin/sh
echo "Running flake8..."
flake8 || exit 1

echo "Running mypy..."
mypy . || exit 1

echo "Running pylint..."
pylint ffrontier || exit 1

echo "Running pytest..."
pytest tests/ || exit 1

echo "All checks passed!"