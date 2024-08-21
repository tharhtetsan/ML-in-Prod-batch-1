

```bash
brew install astro
astro dev init

# check astro airflow running or not
astro dev ps
# start the astro
astro dev start
astro dev stop.


```

###  Attach Remote Running Container
1. Install remote Container Extension
2. Open a Remote Window or `Control + Ship +P` 
3. Attach to Running Container -> Choose `airflow_scheduler`
4. Open folder in this direction `/usr/local/airflow/`


### Shortcut
shift + \



## Scheduler
### Scheduler expression
```bash
None          Don’t schedule, use for exclusively “externally triggered” DAGs
@once          Schedule once and only once
@hourly          Run once an hour at the end of the hour
@daily          Run once a day at midnight (24:00)
@weekly          Run once a week at midnight (24:00) on Sunday
@monthly          Run once a month at midnight (24:00) of the first day of the month
@quarterly        Run once a quarter at midnight (24:00) on the first day
@yearly          Run once a year at midnight (24:00) of January 1
```

If you want to run your task every 3 days or every 3 week, please use CRON expressions
```bash
from datetime import timedelta

schedule = timedelta(weeks=2),
```


#### The catchup and backfilling
The catchup mechanism in Airflow allows running all non-triggered DAGRuns between the start date and the last time the DAG was triggered. The backfilling mechanism allows running historical DAGRuns or rerun already existing DAGRuns.
![catchup_andbackfill](./images/catchup_andbackfill.png)
```bash
airflow dags backfill --start-date START_DATE --end-date END_DATE dag_id
```

#### XCOM
SQLite -> 2Gb per XCOM
Postgres -> 1Gb per XCOM
MySQL -> 64MB per XCOM


### Airflow variable
Your can also write in .env file, it imported in system and cannot see in Airflow UI.


Variable keywords automatically hiding values
```bash
access_token
api_key
apikey
authorization
passphrase
passwd
password
private_key
secret
token
keyfile_dict
service_account
```

```bash
#check your dags exist in metadatabase or not
astro dev run dags list  

#check your logs
astro dev logs scheduler
```




### Sensors
A Sensor is a particular operator that waits for a condition to be true. If the condition is true, the task is marked successful , and the next task runs. If the condition is false, the sensor waits for another interval until it times out and fails.



## Airflow with GCP Storage Object file
```bash
pip install 'apache-airflow[google]'
```

### 1. GCP Credentials Setup

To connect Airflow with Google Cloud Storage (GCS), you need to configure a Google Cloud service account and set up the Airflow connection.

#### Setting Up Google Cloud Service Account

1. **Create a Service Account** in your Google Cloud project.
2. **Download the JSON key file** for the service account.
3. **Store the key file** securely on your Airflow server.

#### Environment Variable for Credentials

Set the `GOOGLE_APPLICATION_CREDENTIALS` environment variable in your Airflow environment:

```python
import os
os.environ['GOOGLE_APPLICATION_CREDENTIALS'] = "/path/to/your/service-account-file.json"
```


| Connection Id   | google_cloud_default                            |
|-----------------|-------------------------------------------------|
| Connection Type | Google Cloud                                    |
| Project ID      | your-gcp-project-id                             |
| Keyfile Path    | /path/to/your/service-account-file.json         |
| Scope           | https://www.googleapis.com/auth/cloud-platform  |


### Search module in [Astronomer Registry](https://registry.astronomer.io/)


- **GCSObjectsWithPrefixExistenceSensor:** Check for the existence of files in a GCS folder.
- **GCSObjectUpdateSensor:** Monitor a specific file for updates.
- **Custom Sensor:** Monitor a "folder" for changes by tracking modifications to the files within it.



**For complex use Sensor Decorator** 


### Docker and airflow commands
```bash
docker ps
docker exec -it  CONTAINER_ID sh
#check related libs are installed or not
airflow info
# initialize the airflow metadata databse.
airflow db init 
 # to check db connection
 airflow db check
# create airflow user
airflow users create -e gg@gmail.com -f tt_firstname -l tt_lastname -u tt_username -p tt_username -r Viewer
 airflow users create -e gg@gmail.com -f tt_firstname -l tt_lastname -u tt_username -p tt_username -r Admin


#check configs 
airflow config list

airflow cheat-sheet


# to check dags list
airflow dags report

airflow dags list-import-errors



```


