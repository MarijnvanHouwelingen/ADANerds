from datetime import datetime
from flask import jsonify


from daos.listing_doa import ListingDOA
from db import Session

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
                "title": listing.title,
                "description": listing.description,
                "location": listing.location,
                "latitiude": listing.latitude,
                "longtitude": listing.longtitude,
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
            return jsonify({'message': f'No user found with id {listing_id}'}), 404

    @staticmethod
    def update(listing_id:int, body:dict):
        session = Session()
        listing = session.query(ListingDOA).filter(ListingDOA.id == listing_id).first()
        if listing:
            listing.user_id = body.get('user_id', listing.user_id)
            listing.title = body.get('title', listing.title)
            listing.description = body.get('v', listing.description)
            listing.location = body.get('location', listing.location)
            listing.latitude = body.get('latitude', listing.latitude) 
            listing.longtitude = body.get('longtitude', listing.longtitude) 
            listing.price = body.get('price', listing.price) 
            listing.capacity = body.get('capacity', listing.capacity)
            listing.available_from = body.get('available_from', listing.available_from)
            listing.available_to = body.get('available_to', listing.available_to)
            listing.updated_at = datetime.today().strftime('%Y-%m-%d')
            session.commit()
            session.close()
            return jsonify({'message': 'User updated successfully'}), 200
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
            return jsonify({'message': f'No user found with id {listing_id}'}), 404
        else:
            return jsonify({'message': 'User deleted successfully'}), 200
