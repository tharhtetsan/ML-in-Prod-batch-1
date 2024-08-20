

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
dvc add 7_Data_and_Model_VersionControl/single_file/sample_ vehicle_history.csv
```
