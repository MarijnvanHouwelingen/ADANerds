from pub_sub import publish_message

def publish_account_event(project_id, account_topic_id, account_data): 
    '''
    This function is responsible for publishing a reported user's account information 
    from the account bounded context to the event bus.
    (Pub_Account in the Component Diagram)
    '''
    account_event = {
        "type": "ReportUser",
        "data": account_data   
    }
    publish_message(project_id, account_topic_id, account_event) # Pub_Account
    print(f"Published account information for the reported user with account ID {account_data}")
    