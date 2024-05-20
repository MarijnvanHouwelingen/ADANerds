from pub_sub import  publish_message

def publish_listing_event(project_id, listing_topic_id, listing_data): #####, Add information from bounded context, like listing_id, etc): #####
    '''
    This function is responsible for publishing listing information from the listing bounded context to the event bus. It should be 
    integrated into the listing bounded context service to publish listing events whenever a listing is initiated. 
    (Pub_Listing in Component Diagram)
    '''
    listing_event = {
        "type": "Listing",
        "data": listing_data ##### Add the variable which are initalized in the function here (see listing_doa.py) #####
    }
    publish_message(project_id, listing_topic_id, listing_event) # Pub_Listing
    print(f"Published listing event for listing ID {listing_data}")


