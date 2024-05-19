from flask import jsonify
import os

from booking_doa import BookingDOA
from db import Session

from datetime import datetime
from sqlalchemy.sql import text
# import the refund publish event
from booking_pub import publish_refund_event

class DataManager:
    @staticmethod
    def get_next_id(table_name: str) -> int:
        session = Session()
        query = text(f'SELECT MAX(id) as max_id FROM {table_name}')
        result = session.execute(query).fetchone()
        print(result)
        return int((result[0] or 0) + 1)
    
class Booking:
    @staticmethod
    def create(body:dict) -> tuple:
        """
        Create a new booking for a listing.

        Args:
            body (dict): The request body containing booking information.

        Returns:
            tuple: A tuple containing JSON response and HTTP status code.
        """

        session = Session()
        booking = BookingDOA(
            id = DataManager.get_next_id(BookingDOA.__tablename__),
            begin_date= datetime.strptime(body['begin_date'],'%Y-%m-%d'),
            end_date=datetime.strptime(body['end_date'],'%Y-%m-%d'),
            price=body['price'],  
            refund = False,
            status=body['status'],

        )
        session.add(booking)
        session.commit()
        session.refresh(booking)
        session.close()
        return jsonify({'booking_id': booking.id}), 200

    # Get one specific booking based on both the listing_id and booking_id
    @staticmethod
    def get_one(booking_id:int) -> tuple:
        """
        Retrieve information about a specific booking.

        Args:
            booking_id (int): The ID of the booking.

        Returns:
            tuple: A tuple containing JSON response and HTTP status code.
        """
        # Cast the booking_id to an int
        booking_id = int(booking_id)

        session = Session()
        booking = session.query(BookingDOA).filter(BookingDOA.id == booking_id).first()
        if booking:
            booking_info = {
                "begin_date": booking.begin_date.isoformat(),
                "end_date": booking.end_date.isoformat(),
                "price": booking.price,
                "refund": booking.refund,
                "status": booking.status
            }
            session.close()
            return jsonify(booking_info), 200
        else:
            session.close()
            return jsonify({'message': f'No booking found with id {booking_id}'}), 404
    
    # Get all bookings from one listing
    @staticmethod
    def get_all() -> tuple:
        """
        Retrieve all bookings.

        Args:
        None

        Returns:
            tuple: A tuple containing JSON response and HTTP status code.
        """
        session = Session()
        bookings = session.query(BookingDOA).all()
        booking_info = []
        if bookings:
            for booking in bookings:
                booking_info.append({
                    "begin_date": booking.begin_date.isoformat(),
                    "end_date": booking.end_date.isoformat(),
                    "price": booking.price,
                    "refund": booking.refund,
                    "status": booking.status,
                })
            session.close()
            return jsonify(booking_info), 200
        else:
            session.close()
            return jsonify({'message': f'No bookings'}), 404

    @staticmethod
    def update(booking_id:int, body:dict) -> tuple:
        """
        Update information about a specific booking.

        Args:
            booking_id (int): The ID of the booking.
            body (dict): The request body containing updated booking information.

        Returns:
            tuple: A tuple containing JSON response and HTTP status code.
        """
        # Cast the booking_id to an int
        booking_id = int(booking_id)

        session = Session()
        booking = session.query(BookingDOA).filter(BookingDOA.id == booking_id).first()
        if booking:
            booking.begin_date = body.get('begin_date', datetime.strptime(body["begin_date"],'%Y-%m-%d'))
            booking.end_date = body.get('end_date', datetime.strptime(body['end_date'],'%Y-%m-%d'))
            booking.price = body.get('price', body["price"])
            booking.refund = body.get("refund",body["refund"]) 
            booking.status = body.get('status', body["status"]) 
            session.commit()
            session.refresh(booking)
             # Publish the listing event after the listing is created
            if booking.refund:
                booking_id = booking.id
                refund_amount = booking.price
                project_id = os.getenv('GOOGLE_CLOUD_PROJECT_ID') or 'emerald-diagram-413020'
                booking_topic_id = os.getenv('BOOKING_TOPIC_ID') or 'booking_refund'

                publish_refund_event(project_id=project_id,booking_topic_id=booking_topic_id,
                                    booking_id=booking_id,refund_amount=refund_amount)
                session.close()
                return jsonify({'message': 'Booking updated successfully'}), 200
        else:
            session.close()
            return jsonify({'message': f'No booking found with id {booking_id}'}), 404

    @staticmethod
    def delete(booking_id: int) -> tuple:
        """
        Delete a specific booking.

        Args:
            booking_id (int): The ID of the booking.

        Returns:
            tuple: A tuple containing JSON response and HTTP status code.
        """
        # Cast the booking_id to an int
        booking_id = int(booking_id)
        
        session = Session()
        affected_rows = session.query(BookingDOA).filter(BookingDOA.id == booking_id).delete()
        session.commit()
        session.close()
        if affected_rows == 0:
            return jsonify({'message': f'No booking found with id {booking_id}'}), 404
        else:
            return jsonify({'message': 'Booking deleted successfully'}), 200