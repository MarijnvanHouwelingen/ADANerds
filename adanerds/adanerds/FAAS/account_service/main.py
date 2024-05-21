from flask import Flask, jsonify
import json 
import base64
import functions_framework
#from pub_sub import create_topic, create_subscription

app = Flask(__name__)

project_id = "emerald-diagram-413020" 

account_topic_id = "report_users"
account_subscription_id = "account-service-subscription"

# Aleady created topic and subscription
# create_topic(project_id, account_topic_id)
# create_subscription(project_id, account_topic_id, account_subscription_id)

@functions_framework.cloud_event
def handle_account_event(cloud_event):
    '''
    This function is designed to subscribe to the report_user topic and process account information from the event bus. 
    It will be triggered whenever a new message is published to the repor_user topic.
    (Sub_Notification in Component Diagram)
    '''
    data = cloud_event.data
    message_data = json.loads(base64.b64decode(data["message"]["data"]).decode('utf-8')) #Sub_Notification (report user)
    print(f'Message data: {message_data}')

    if message_data['type'] == "ReportUser":
        user_id = message_data['data']['id']
        return jsonify({'message': f'User with ID {user_id} has been reported.'}), 200

    return jsonify({'error': f'We apologize, but we are unable to report a user with ID {user_id} at this time.'}), 400