from datetime import datetime
from flask import jsonify


from daos.listing_doa import ListingDOA
from db import Session
from daos.account_doa import UserDOA

class Listing:
    @staticmethod
    def create(body:dict):
        session = Session()
        listing = ListingDOA(
            user_id=body['user_name'],
            title=body['first_name'],
            description=body['last_name'],
            latitude=body['email_address'],
            longtitude=body['password'],  # This would be hashed in a real application
            price=body['price'],
            capacity=body['capacity'],
            available_from=body['available_from'],
            available_to=body['available_to'],
            created_at= datetime.today().strftime('%Y-%m-%d'),
            updated_at = None
        )
        session.add(listing)
        session.commit()
        session.refresh(listing)
        session.close()
        return jsonify({'Listing_id': listing.id}), 200

    @staticmethod
    def get(listing_id:int):
        session = Session()
        listing = session.query(ListingDOA).filter(ListingDOA.id == listing_id).first()
        if listing:
            listing_info = {
                "user_id": listing.user_id,
                "title": listing.user_id,
                "description": listing.begin_date,
                "location": listing.end_date,
                "latitiude": listing.begin_date,
                "longtitude": listing.status,
                "price": listing.price,
                "capacity": listing.capacity,
                "available_from": listing.available_from,
                "available_to": listing.available_to,
                "created_at": listing.created_at,
                "updated_at": listing.updated_at
            }
            session.close()
            return jsonify(listing_info), 200
        else:
            session.close()
            return jsonify({'message': f'No Listing found with id {listing_id}'}), 404

    @staticmethod
    def update(listing_id:int, body:dict):
        session = Session()
        listing = session.query(ListingDOA).filter(ListingDOA.id == listing_id).first()
        if listing:
            listing.user_id = body.get('user_id', listing.user_id)
            listing.user_id = body.get('title', listing.user_id)
            listing.begin_date = body.get('v', listing.begin_date)
            listing.end_date = body.get('location', listing.end_date)
            listing.begin_date = body.get('latitude', listing.begin_date) 
            listing.status = body.get('longtitude', listing.status) 
            listing.price = body.get('price', listing.price) 
            listing.capacity = body.get('capacity', listing.capacity)
            listing.available_from = body.get('available_from', listing.available_from)
            listing.available_to = body.get('available_to', listing.available_to)
            listing.updated_at = datetime.today().strftime('%Y-%m-%d')
            session.commit()
            session.close()
            return jsonify({'message': 'Listing updated successfully'}), 200
        else:
            session.close()
            return jsonify({'message': f'No listing found with id {listing_id}'}), 404

    @staticmethod
    def delete(listing_id):
        session = Session()
        affected_rows = session.query(ListingDOA).filter(ListingDOA.id == listing_id).delete()
        session.commit()
        session.close()
        if affected_rows == 0:
            return jsonify({'message': f'No Listing found with id {listing_id}'}), 404
        else:
            return jsonify({'message': 'Listing deleted successfully'}), 200
