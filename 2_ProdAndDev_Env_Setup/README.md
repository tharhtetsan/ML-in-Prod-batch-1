### Anaconda
#### Anaconda Commands
```bash'
conda -h
conda env list
conda activat ths
conda create -n test python=3.10

```


Check libs and create sample requirements.txt
```bash
pip list
pip freeze > requirements.txt
```


### Pipenv
Solving libs dependencies
```
pip install pipenv
pipenv install
pipenv install --dev seaborn
pipenv graph
```


Generate pipenv to requirements.txt
```bash

pipenv run python test.py
pipenv run pip freeze > requirements.txt
```