from datetime import datetime
from flask import jsonify


from daos.booking_doa import BookingDOA
from db import Session
from daos.account_doa import UserDOA
from daos.listing_doa import ListingDOA
from sqlalchemy import and_

class Booking:
    @staticmethod
    def create(listing_id,body:dict):
        session = Session()
        listing = session.query(ListingDOA).filter(ListingDOA.id == listing_id).first()
        booking = BookingDOA(
            begin_date=body['begin_date'],
            end_date=body['end_date'],
            price=body['price'],  
            status=body['status'],
            listing= listing,
            listing_id=listing_id
        )
        session.add(booking)
        session.commit()
        session.refresh(booking)
        session.close()
        return jsonify({'booking_id': booking.id}), 200

    # Get one specific booking based on both the listing_id and booking_id
    @staticmethod
    def get_one(listing_id:int,booking_id:int):
        session = Session()
        booking = session.query(BookingDOA).filter(and_(BookingDOA.id == booking_id,BookingDOA.listing_id == listing_id)).first()
        if booking:
            booking_info = {
                "begin_date": booking.begin_date,
                "end_date": booking.end_date,
                "price": booking.price,
                "status": booking.status,
                "listing_id":booking.listing_id
            }
            session.close()
            return jsonify(booking_info), 200
        else:
            session.close()
            return jsonify({'message': f'No booking found with id {booking_id}'}), 404
    
    # Get all bookings from one listing
    @staticmethod
    def get_all(listing_id:int):
        session = Session()
        bookings = session.query(BookingDOA).filter(BookingDOA.listing_id == listing_id).all()
        booking_info = []
        if bookings:
            for booking in bookings:
                booking_info.append({
                    "begin_date": booking.begin_date,
                    "end_date": booking.end_date,
                    "price": booking.price,
                    "status": booking.status,
                    "listing_id":booking.listing_id
                })
            session.close()
            return jsonify(booking_info), 200
        else:
            session.close()
            return jsonify({'message': f'No bookings found with listing id {listing_id}'}), 404

    @staticmethod
    def update(listing_id:int,booking_id:int, body:dict):
        session = Session()
        booking = session.query(BookingDOA).filter(and_(BookingDOA.id == booking_id, BookingDOA.listing_id == listing_id)).first()
        if booking:
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
    def delete(listing_id,booking_id):
        session = Session()
        affected_rows = session.query(BookingDOA).filter(and_(BookingDOA.id == booking_id,BookingDOA.listing_id == listing_id)).delete()
        session.commit()
        session.close()
        if affected_rows == 0:
            return jsonify({'message': f'No booking found with id {booking_id}'}), 404
        else:
            return jsonify({'message': 'Booking deleted successfully'}), 200