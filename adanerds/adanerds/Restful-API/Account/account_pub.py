from pub_sub import publish_message

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
    