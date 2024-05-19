from datetime import datetime
from flask import jsonify

import os
from listing_doa import ListingDOA
from db import Session
from sqlalchemy.sql import text

# The listing publish event function
from listing_sub import publish_listing_event 


class DataManager:
    @staticmethod
    def get_next_id(table_name: str) -> int:
        session = Session()
        query = text(f'SELECT MAX(id) as max_id FROM {table_name}')
        result = session.execute(query).fetchone()
        print(result)
        return int((result[0] or 0) + 1)
    
class Listing:
    @staticmethod
    def create(body:dict) -> tuple:
        """
        Create a new listing.

        Args:
            body (dict): The request body containing listing information.

        Returns:
            tuple: A tuple containing JSON response and HTTP status code.
        """
        try:
            listing_id = DataManager.get_next_id(ListingDOA.__tablename__)
            
            session = Session()
            listing = ListingDOA(
                id = listing_id,
                begin_date=datetime.strptime(body['begin_date'],'%Y-%m-%d'),
                end_date=datetime.strptime(body['end_date'],'%Y-%m-%d'),
                status=body['status'], 
                price=body['price'],
                capacity=body['capacity'],
                available_from=datetime.strptime(body['available_from'],'%Y-%m-%d'),
                available_to=datetime.strptime(body['available_to'],'%Y-%m-%d'),
                created_at= datetime.today(),
                updated_at = datetime.fromisoformat('1000-01-01')
            )
            session.add(listing)
            session.commit()
            session.refresh(listing)
            # Publish the listing event after the listing is created
            listing_data = {
                "id": listing.id,
                "begin_date": listing.begin_date.isoformat(),
                "end_date": listing.end_date.isoformat(),
                "status": listing.status,
                "price": listing.price,
                "capacity": listing.capacity,
                "available_from": listing.available_from.isoformat(),
                "available_to": listing.available_to.isoformat()
            }
            
            project_id = os.getenv('GOOGLE_CLOUD_PROJECT_ID') 
            listing_topic_id = os.getenv('LISTING_TOPIC_ID') 

            publish_listing_event(project_id=project_id,listing_topic_id=listing_topic_id,listing_data=listing_data)
            
            return jsonify({'Listing_id': listing.id}), 200
        except Exception as e:
            session.rollback()
            print(f"Error creating listing: {e}")
            return jsonify({'error': 'An error occurred while creating the listing'}), 500
        finally:
            session.close()
            

    @staticmethod
    def get(listing_id:int) -> tuple:
        """
        Retrieve information about a specific listing.

        Args:
            listing_id (int): The ID of the listing.

        Returns:
            tuple: A tuple containing JSON response and HTTP status code.
        """

        # Cast the listing_id to an int
        listing_id = int(listing_id)


        session = Session()
        listing = session.query(ListingDOA).filter(ListingDOA.id == listing_id).first()
        if listing:
            listing_info = {
                "begin_date": listing.begin_date.isoformat(),
                "end_date": listing.end_date.isoformat(),
                "status": listing.status,
                "price": listing.price,
                "capacity": listing.capacity,
                "available_from": listing.available_from.isoformat(),
                "available_to": listing.available_to.isoformat(),
                "created_at": listing.created_at.isoformat(),
                "updated_at": listing.updated_at.isoformat()
            }
            session.close()
            return jsonify(listing_info), 200
        else:
            session.close()
            return jsonify({'message': f'No Listing found with id {listing_id}'}), 404

    @staticmethod
    def update(listing_id:int, body:dict) -> tuple:
        """
        Update information about a specific listing.

        Args:
            listing_id (int): The ID of the listing.
            body (dict): The request body containing updated listing information.

        Returns:
            tuple: A tuple containing JSON response and HTTP status code.
        """

        # Cast the listing_id to an int
        listing_id = int(listing_id)

        session = Session()
        listing = session.query(ListingDOA).filter(ListingDOA.id == listing_id).first()
        if listing:
            listing.begin_date = body.get('begin_date', datetime.strptime(body["begin_date"],'%Y-%m-%d'))
            listing.end_date = body.get('end_date', datetime.strptime(body['end_date'],'%Y-%m-%d'))
            listing.status = body.get('status', body["status"]) 
            listing.price = body.get('price', body["price"]) 
            listing.capacity = body.get('capacity', body["capacity"])
            listing.available_from = body.get('available_from', datetime.strptime(body["available_from"],'%Y-%m-%d'))
            listing.available_to = body.get('available_to', datetime.strptime(body["available_to"],'%Y-%m-%d'))
            listing.updated_at = datetime.today()
            session.commit()
            session.close()
            return jsonify({'message': 'Listing updated successfully'}), 200
        else:
            session.close()
            return jsonify({'message': f'No listing found with id {listing_id}'}), 404

    @staticmethod
    def delete(listing_id) -> tuple:
        """
        Delete a specific listing.

        Args:
            listing_id (int): The ID of the listing.

        Returns:
            tuple: A tuple containing JSON response and HTTP status code.
        """

        # Cast the listing_id to an int
        listing_id = int(listing_id)

        session = Session()
        affected_rows = session.query(ListingDOA).filter(ListingDOA.id == listing_id).delete()
        session.commit()
        session.close()
        if affected_rows == 0:
            return jsonify({'message': f'No Listing found with id {listing_id}'}), 404
        else:
            return jsonify({'message': 'Listing deleted successfully'}), 200
