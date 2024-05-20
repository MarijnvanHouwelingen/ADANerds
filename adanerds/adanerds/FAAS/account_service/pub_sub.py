from google.cloud import pubsub_v1
import json

def create_topic(project, topic):
    try:
        publisher = pubsub_v1.PublisherClient()
        topic_path = publisher.topic_path(project, topic)
        topic = publisher.create_topic(request={"name": topic_path})
        print("Created topic: {}".format(topic.name))
    except Exception as ex:
        print(f"Error creating topic or subscription: {ex}")
        
def publish_message(project, topic, message):
    publisher = pubsub_v1.PublisherClient()
    topic_path = publisher.topic_path(project, topic)
    message = json.dumps(message).encode("utf-8")
    try:
        future = publisher.publish(topic_path, message)
        future.result()
        print("Message published successfully.")
    except Exception as ex:
        print(f"Error creating message: {ex}")
        
def create_subscription(project, topic, subscription):
    try:
        publisher = pubsub_v1.PublisherClient()
        subscriber = pubsub_v1.SubscriberClient()
        topic_path = publisher.topic_path(project, topic)
        subscription_path = subscriber.subscription_path(project, subscription)
        with subscriber:
            subscription_info = subscriber.create_subscription(request={"name": subscription_path, "topic": topic_path})
        print(f"Subscription created: {subscription_info}")
    except Exception as ex:
        print(f"Error creating subscription: {ex}.")
           