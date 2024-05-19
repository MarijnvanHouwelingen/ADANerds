from flask import Flask, jsonify
import json 
import base64
import functions_framework
from pub_sub import create_topic, publish_message, create_subscription

app = Flask(__name__)

project_id = "emerald-diagram-413020" # id of project

account_topic_id = "report_users"
account_subscription_id = "account-service-subscription"

create_topic(project_id, account_topic_id)
create_subscription(project_id, account_topic_id, account_subscription_id)

def publish_account_event(project_id, account_topic_id, account_data): #####, Add information from bounded context, like account_id) #####
    '''
    This function is responsible for publishing account information from the account bounded context to the event bus. It should be 
    integrated into the account bounded context service to publish account events whenever an account is initiated. 
    (Pub_Account in Component Diagram)
    '''
    account_event = {
        "type": "ReportUser",
        "data": account_data    ##### I think only account_id: We need to consider whether additional information about the reported user is necessary. #####
    }
    publish_message(project_id, account_topic_id, account_event) # Pub_Account
    print(f"Published account event for account ID {account_data}")
    
  
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
        ##### Get the same information that is stored in the event bus
        return "", 200

    return jsonify({'error': 'We apologize, but we are unable to report a user at this time.'}), 400