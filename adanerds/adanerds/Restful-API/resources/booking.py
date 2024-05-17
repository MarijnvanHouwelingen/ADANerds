from datetime import datetime
from flask import jsonify


from daos.booking_doa import BookingDOA
from db import Session
from daos.account_doa import UserDOA
from daos.listing_doa import ListingDOA
class Booking:
    @staticmethod
    def create(body:dict):
        session = Session()
        booking = BookingDOA(
            listing_id=body['listing_id'],
            user_id=body['user_id'],
            begin_date=body['begin_date'],
            end_date=body['end_date'],
            price=body['price'],  
            status=body['status']
        )
        session.add(booking)
        session.commit()
        session.refresh(booking)
        session.close()
        return jsonify({'booking_id': booking.id}), 200

    @staticmethod
    def get(booking_id:int):
        session = Session()
        booking = session.query(BookingDOA).filter(BookingDOA.id == booking_id).first()
        if booking:
            listing_info = {
                "listing_id": booking.listing_id,
                "user_id": booking.user_id,
                "begin_date": booking.begin_date,
                "end_date": booking.end_date,
                "price": booking.price,
                "status": booking.status
            }
            session.close()
            return jsonify(listing_info), 200
        else:
            session.close()
            return jsonify({'message': f'No booking found with id {booking_id}'}), 404

    @staticmethod
    def update(booking_id:int, body:dict):
        session = Session()
        booking = session.query(BookingDOA).filter(BookingDOA.id == booking_id).first()
        if booking:
            booking.listing_id = body.get('listing_id', booking.listing_id)
            booking.user_id = body.get('user_id', booking.user_id)
            booking.begin_date = body.get('begin_date', booking.begin_date)
            booking.end_date = body.get('end_date', booking.end_date)
            booking.price = body.get('price', booking.price) 
            booking.status = body.get('status', booking.status) 
            session.commit()
            session.close()
            return jsonify({'message': 'Booking updated successfully'}), 200
        else:
            session.close()
            return jsonify({'message': f'No booking found with id {booking_id}'}), 404

    @staticmethod
    def delete(booking_id):
        session = Session()
        affected_rows = session.query(BookingDOA).filter(BookingDOA.id == booking_id).delete()
        session.commit()
        session.close()
        if affected_rows == 0:
            return jsonify({'message': f'No booking found with id {booking_id}'}), 404
        else:
            return jsonify({'message': 'Booking deleted successfully'}), 200