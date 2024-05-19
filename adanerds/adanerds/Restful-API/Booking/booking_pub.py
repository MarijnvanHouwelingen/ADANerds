from pub_sub import publish_message

def publish_refund_event(project_id, booking_topic_id, booking_id, refund_amount): 
    '''
    This function is responsible for publishing refund information from the booking bounded context to the event bus. It should be 
    integrated into the booking bounded context service to publish refund events whenever a refund is initiated. 
    (Pub_Booking in Component Diagram)
    '''
    refund_event = {
        "type": "Refund",
        "data": {
            "booking_id": booking_id,
            "refund_amount": refund_amount
        }
    }
    publish_message(project_id, booking_topic_id, refund_event)
    print(f"Published refund event for booking ID {booking_id}")