from concurrent.futures import TimeoutError
from google.cloud import pubsub_v1

import os
os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = r"service_acc/service_acc.json"


# TODO(developer)
project_id = "PROJ_ID" #input("your-project-id : ")
subscription_id = "thstest_topic-sub-1" #input("your-subscription-id :")
# Number of seconds the subscriber should listen for messages 
timeout = 60.0

subscriber = pubsub_v1.SubscriberClient()
# The `subscription_path` method creates a fully qualified identifier
# in the form `projects/{project_id}/subscriptions/{subscription_id}`
subscription_path = subscriber.subscription_path(project_id, subscription_id)

def callback(message: pubsub_v1.subscriber.message.Message) -> None:
    import time
    print(f"Received {message}.")
    print("Receive Time : ",time.time())
    message.ack()

streaming_pull_future = subscriber.subscribe(subscription_path, callback=callback)
print(f"Listening for messages on {subscription_path}..\n")

# Wrap subscriber in a 'with' block to automatically call close() when done.
with subscriber:
    try:
        # When `timeout` is not set, result() will block indefinitely,
        # unless an exception is encountered first.
        streaming_pull_future.result(timeout=timeout)
    except TimeoutError:
        streaming_pull_future.cancel()  # Trigger the shutdown.
        streaming_pull_future.result()  # Block until the shutdown is complete. 