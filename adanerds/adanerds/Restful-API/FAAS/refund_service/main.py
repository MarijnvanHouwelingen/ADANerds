import json 
import base64
import functions_framework
from pub_sub import create_topic, publish_message, create_subscription
from flask import Flask, jsonify
app = Flask(__name__)

project_id = 'emerald-diagram-413020'
booking_topic_id = 'booking_refund'
refund_subscription_id = 'refund-service-subscription'
refund_status_topic_id = 'refund_status'

create_topic(project_id, booking_topic_id)
create_subscription(project_id, booking_topic_id, refund_subscription_id)
create_topic(project_id, refund_status_topic_id)

@functions_framework.cloud_event
def handle_refund_event(cloud_event):
    '''
    This function is designed to subscribe to the booking-refunds topic and process refund information from the event bus. 
    It will be triggered whenever a new message is published to the booking-refunds topic and publish the refund status 
    to the refund-status topic.
    (Sub_Refund and Pub_Refund in Component Diagram)
    '''
    data = cloud_event.data
    message_data = json.loads(base64.b64decode(data["message"]["data"]).decode('utf-8')) #Sub_Refund
    print(f'Message data: {message_data}')

    if message_data['type'] == "Refund":
        booking_id = message_data['data']['booking_id']
        refund_amount = message_data['data']['refund_amount']
        print(f"Processing refund of ${refund_amount} for booking ID {booking_id}")
        
        refund_status = {
            "type": "RefundStatus",
            "data": {
                "booking_id": booking_id,
                "status": "Processed",
                "refund_amount": refund_amount
            }
        }
        publish_message(project_id, refund_status_topic_id, refund_status) # Pub_Refund
        print(f"Published refund status for booking ID {booking_id}")
        return jsonify({'message': f'Refund of ${refund_amount} for booking ID {booking_id} has been processed'}), 200

    return jsonify({'error': 'We apologize, but we are unable to issue a refund at this time.'}), 400




