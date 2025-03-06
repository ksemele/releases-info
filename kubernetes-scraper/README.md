# WIP
## How to run

Local script for run (test purposes):

```bash
cd kubernetes-scraper
./local-run.sh
```

Than you can see Prometheus-like metrics on localhost:
http://localhost:8000


```shell
python3 -m venv venv
source venv/bin/activate

pip install -e .

pip install -e ".[test]"

pytest

pytest tests/test_image.py

pytest -v -m "not slow"

pytest --cov=releases_info --cov-report=html

ptw
```
