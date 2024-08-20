

```bash
dvc init
git status
Changes to be committed:
        new file:   .dvc/.gitignore
        new file:   .dvc/config
        ...
git commit -m "Initialize DVC"
git push
```

Use dvc add to start tracking the dataset file:
```bash
dvc add single_file/sample_vehicle_history.csv
```

Now dvc is creating a  cache file, please check <b> .dvc/cache/files/md5/.. </b>



To track changes in Git:
```bash
git add single_file/sample_vehicle_history.csv.dvc single_file/.gitignore
git commit -m "Add raw data"
```