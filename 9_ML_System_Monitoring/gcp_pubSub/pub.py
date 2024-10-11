# pip install --upgrade google-cloud-pubsub
from google.cloud import pubsub_v1
import os
os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = r"service-acc/service_acc.json"


project_id = "PROJ_ID" #input("your-project-id : ")
topic_id = "thstest_topic" #input("your-topic-id : ")
publisher = pubsub_v1.PublisherClient()
# The `topic_path` method creates a fully qualified identifier
# in the form `projects/{project_id}/topics/{topic_id}`
topic_path = publisher.topic_path(project_id, topic_id)

import time
start_time = time.time()
print("Start time : ",start_time)
for n in range(1, 2):
    data_str = f"Message number {n}"
    # Data must be a bytestring
    data = data_str.encode("utf-8")
    # When you publish a message, the client returns a future.
    future = publisher.publish(topic_path, data)
    print(future.result())

print(f"Published messages to {topic_path}.")
end_time = time.time()
print("End time : ",end_time)
print("Duration : ",end_time-start_time)