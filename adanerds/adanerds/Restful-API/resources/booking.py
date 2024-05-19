from flask import jsonify
import os

from daos.booking_doa import BookingDOA
from db import Session

from Listing.listing_doa import ListingDOA
from sqlalchemy import and_

# import the refund FAAS
from FAAS.refund_service.main import publish_refund_event

class Booking:
    @staticmethod
    def create(listing_id:int,body:dict) -> tuple:
        """
        Create a new booking for a listing.

        Args:
            listing_id (int): The ID of the listing.
            body (dict): The request body containing booking information.

        Returns:
            tuple: A tuple containing JSON response and HTTP status code.
        """
        session = Session()
        listing = session.query(ListingDOA).filter(ListingDOA.id == listing_id).first()
        booking = BookingDOA(
            begin_date=body['begin_date'],
            end_date=body['end_date'],
            price=body['price'],  
            refund = False,
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
    def get_one(listing_id:int,booking_id:int) -> tuple:
        """
        Retrieve information about a specific booking.

        Args:
            listing_id (int): The ID of the listing.
            booking_id (int): The ID of the booking.

        Returns:
            tuple: A tuple containing JSON response and HTTP status code.
        """
        session = Session()
        booking = session.query(BookingDOA).filter(and_(BookingDOA.id == booking_id,BookingDOA.listing_id == listing_id)).first()
        if booking:
            booking_info = {
                "begin_date": booking.begin_date,
                "end_date": booking.end_date,
                "price": booking.price,
                "refund": booking.refund,
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
    def get_all(listing_id:int) -> tuple:
        """
        Retrieve all bookings for a specific listing.

        Args:
            listing_id (int): The ID of the listing.

        Returns:
            tuple: A tuple containing JSON response and HTTP status code.
        """
        session = Session()
        bookings = session.query(BookingDOA).filter(BookingDOA.listing_id == listing_id).all()
        booking_info = []
        if bookings:
            for booking in bookings:
                booking_info.append({
                    "begin_date": booking.begin_date,
                    "end_date": booking.end_date,
                    "price": booking.price,
                    "refund": booking.refund,
                    "status": booking.status,
                    "listing_id":booking.listing_id
                })
            session.close()
            return jsonify(booking_info), 200
        else:
            session.close()
            return jsonify({'message': f'No bookings found with listing id {listing_id}'}), 404

    @staticmethod
    def update(listing_id:int,booking_id:int, body:dict) -> tuple:
        """
        Update information about a specific booking.

        Args:
            listing_id (int): The ID of the listing.
            booking_id (int): The ID of the booking.
            body (dict): The request body containing updated booking information.

        Returns:
            tuple: A tuple containing JSON response and HTTP status code.
        """
        session = Session()
        booking = session.query(BookingDOA).filter(and_(BookingDOA.id == booking_id, BookingDOA.listing_id == listing_id)).first()
        if booking:
            booking.begin_date = body.get('begin_date', booking.begin_date)
            booking.end_date = body.get('end_date', booking.end_date)
            booking.price = body.get('price', booking.price)
            booking.refund = body.get("refund",booking.refund) 
            booking.status = body.get('status', booking.status) 
            session.commit()
            session.refresh(booking)
             # Publish the listing event after the listing is created
            if booking.refund:
                booking_id = booking.id
                refund_amount = booking.price
                project_id = os.getenv('GOOGLE_CLOUD_PROJECT_ID')
                booking_topic_id = os.getenv('BOOKING_TOPIC_ID')

                publish_refund_event(project_id=project_id,booking_topic_id=booking_topic_id,
                                    booking_id=booking_id,refund_amount=refund_amount)
                session.close()
                return jsonify({'message': 'Booking updated successfully'}), 200
        else:
            session.close()
            return jsonify({'message': f'No booking found with id {booking_id}'}), 404

    @staticmethod
    def delete(listing_id: int,booking_id: int) -> tuple:
        """
        Delete a specific booking.

        Args:
            listing_id (int): The ID of the listing.
            booking_id (int): The ID of the booking.

        Returns:
            tuple: A tuple containing JSON response and HTTP status code.
        """
        session = Session()
        affected_rows = session.query(BookingDOA).filter(and_(BookingDOA.id == booking_id,BookingDOA.listing_id == listing_id)).delete()
        session.commit()
        session.close()
        if affected_rows == 0:
            return jsonify({'message': f'No booking found with id {booking_id}'}), 404
        else:
            return jsonify({'message': 'Booking deleted successfully'}), 200