# How to run

Local script for run (test purposes)

```bash
#/bin/bash

python3 -m venv venv
source venv/bin/activate
python3 -m pip install --upgrade pip
pip3 install -r requirements.txt
export PYTHONPATH=$(pwd)

python3 main.py
```