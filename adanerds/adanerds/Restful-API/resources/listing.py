from datetime import datetime,date
from flask import jsonify

import os
from daos.listing_doa import ListingDOA
from db import Session
from daos.account_doa import UserDOA

# The listing publish event function
from FAAS.picture_service.main import publish_listing_event 
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
            session = Session()
            listing = ListingDOA(
                begin_date=body['begin_date'],
                end_date=body['end_date'],
                status=body['status'], 
                price=body['price'],
                capacity=body['capacity'],
                available_from=body['available_from'],
                available_to=body['available_to'],
                created_at= datetime.today(),
                updated_at = datetime.fromisoformat('1000-01-01')
            )
            session.add(listing)
            session.commit()
            session.refresh(listing)
            # Publish the listing event after the listing is created
            listing_data = {
                "id": listing.id,
                "begin_date": listing.begin_date,
                "end_date": listing.end_date,
                "status": listing.status,
                "price": listing.price,
                "capacity": listing.capacity,
                "available_from": listing.available_from,
                "available_to": listing.available_to,
                "created_at": listing.created_at,
                "updated_at": listing.updated_at
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
        session = Session()
        listing = session.query(ListingDOA).filter(ListingDOA.id == listing_id).first()
        if listing:
            listing_info = {
                "begin_date": listing.begin_date,
                "end_date": listing.end_date,
                "status": listing.status,
                "price": listing.price,
                "capacity": listing.capacity,
                "available_from": listing.available_from,
                "available_to": listing.available_to,
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
        session = Session()
        listing = session.query(ListingDOA).filter(ListingDOA.id == listing_id).first()
        if listing:
            listing.begin_date = body.get('begin_date', listing.begin_date)
            listing.end_date = body.get('end_date', listing.begin_date)
            listing.status = body.get('status', listing.status) 
            listing.price = body.get('price', listing.price) 
            listing.capacity = body.get('capacity', listing.capacity)
            listing.available_from = body.get('available_from', listing.available_from)
            listing.available_to = body.get('available_to', listing.available_to)
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
        session = Session()
        affected_rows = session.query(ListingDOA).filter(ListingDOA.id == listing_id).delete()
        session.commit()
        session.close()
        if affected_rows == 0:
            return jsonify({'message': f'No Listing found with id {listing_id}'}), 404
        else:
            return jsonify({'message': 'Listing deleted successfully'}), 200
