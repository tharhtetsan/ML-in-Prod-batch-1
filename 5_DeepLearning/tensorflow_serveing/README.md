```bash
conda create -n ths python==3.10
conda activate ths
which python3.10

```


Solve pipenv
```bash
pipenv clean
pipenv run python --version
# remove wrong python path
pipenv --rm
# set python path
pipenv --python /opt/anaconda3/envs/ths/bin/python3.10
```
