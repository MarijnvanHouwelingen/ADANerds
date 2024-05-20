from datetime import datetime
from flask import jsonify
from flask import request

from account_doa import UserDOA,NotificationSettingsDAO,ProfileDAO
from sqlalchemy.sql import text
from db import Session
import os

# import account pub event
from account_pub import publish_account_event

class DataManager:
    @staticmethod
    def get_next_id(table_name: str) -> int:
        session = Session()
        query = text(f'SELECT MAX(id) as max_id FROM {table_name}')
        result = session.execute(query).fetchone()
        print(result)
        return int((result[0] or 0) + 1)
    
class User:
    @staticmethod
    def create(body: dict) -> tuple:
        """
        Create a new user.

        Args:
            body (dict): The request body containing user information.

        Returns:
            tuple: A tuple containing JSON response and HTTP status code.
        """
        # Get the max_id from the datamanager class
        user_id = DataManager.get_next_id(UserDOA.__tablename__)
        notification_settings_id = DataManager.get_next_id(NotificationSettingsDAO.__tablename__)
        session = Session()
        try:
            notification_settings = NotificationSettingsDAO(
                id = notification_settings_id,
                chat_notification=False,
                forum_notification=False,
                review_notification=False,
                booking_notification=False
            )
            user = UserDOA(
                id = user_id,
                user_name=body['user_name'],
                first_name=body['first_name'],
                last_name=body['last_name'],
                email_address=body['email_address'],
                password=body['password'],
                report = False,
                notification_settings= notification_settings,
                notification_id= notification_settings.id
            )
            
            session.add(user)
            session.commit()
            session.refresh(user)
            return jsonify({'user_id': user.id}), 200
        except Exception as e:
            session.rollback()
            print(f"Error creating listing: {e}")
            return jsonify({'error': 'An error occurred while creating the listing'}), 500
        finally:
            session.close()
            
        

        

    @staticmethod
    def get(user_id: str) -> tuple:
        """
        Retrieve information about a specific user.

        Args:
            user_id (string): The ID of the user.

        Returns:
            tuple: A tuple containing JSON response and HTTP status code.
        """
        # Cast the user_id to an int
        user_id = int(user_id)

        session = Session()
        user = session.query(UserDOA).filter(UserDOA.id == user_id).first()
        if user:
            user_info = {
                "id": user.id,
                "user_name": user.user_name,
                "first_name": user.first_name,
                "last_name": user.last_name,
                "email_address": user.email_address,
                "password": user.password,
                'report': user.report
            }
            session.close()
            return jsonify(user_info), 200
        else:
            session.close()
            return jsonify({'message': f'No user found with id {user_id}'}), 404

    @staticmethod
    def update(user_id: str, body: dict) -> tuple:
        """
        Update information about a specific user.

        Args:
            user_id (str): The ID of the user.
            body (dict): The request body containing updated user information.

        Returns:
            tuple: A tuple containing JSON response and HTTP status code.
        """

        # Cast the user_id to an int
        user_id = int(user_id)

        session = Session()
        user = session.query(UserDOA).filter(UserDOA.id == user_id).first()
        if user:
            user.user_name = body.get('user_name', body["user_name"])
            user.first_name = body.get('first_name', body["first_name"])
            user.last_name = body.get('last_name', body["last_name"])
            user.email_address = body.get('email_address', body["email_address"])
            user.password = body.get('password', body["password"])  # Again, consider hashing
            user.report = body.get('report',body['report'])
            session.commit()
            session.refresh(user)
            if user.report:
                # Publish the listing event after the listing is created
                user_data = {
                    "id": user.id,
                    "user_name": user.user_name,
                    "first_name": user.first_name,
                    "last_name": user.last_name,
                    "email_address": user.email_address,
                    "password": user.password,
                    "notification_id": user.notification_id,
                }
                
                project_id = os.getenv('GOOGLE_CLOUD_PROJECT_ID') or 'emerald-diagram-413020'
                account_listing_id = os.getenv('LISTING_TOPIC_ID') or 'report_users'

                publish_account_event(project_id=project_id,account_topic_id=account_listing_id,account_data=user_data)
                session.close()
                return jsonify({'message': 'User updated successfully'}), 200
            return jsonify({'user_id': user.id}), 200
               
        else:
            session.close()
            return jsonify({'message': f'No user found with id {user_id}'}), 404

    @staticmethod
    def delete(user_id: int) -> tuple:
        """
        Delete a specific user.

        Args:
            user_id (int): The ID of the user.

        Returns:
            tuple: A tuple containing JSON response and HTTP status code.
        """
        # Cast the user_id to an int
        user_id = int(user_id)

        session = Session()
        affected_rows = session.query(UserDOA).filter(UserDOA.id == user_id).delete()
        session.commit()
        session.close()
        if affected_rows == 0:
            return jsonify({'message': f'No user found with id {user_id}'}), 404
        else:
            return jsonify({'message': 'User deleted successfully'}), 200

class Profile:
    @staticmethod
    def create(user_id: str,body: dict) -> tuple:
        """
        Create a new profile for a user.

        Args:
            user_id (str): The ID of the user.
            body (dict): The request body containing profile information.

        Returns:
            tuple: A tuple containing JSON response and HTTP status code.
        """
        # Cast the user_id to an int
        user_id = int(user_id)

        # Get the max id from profile
        profile_id = DataManager.get_next_id(ProfileDAO.__tablename__)
        session = Session()
        try:
            # find the user that is connected to the user_id
            user_id = request.view_args.get('user_id')
            
            user = session.query(UserDOA).filter(UserDOA.id == user_id).first()

            # Create the corresponding profile DOA
            profile = ProfileDAO(
                id = profile_id,
                user_id=user_id,
                date_of_birth=datetime.strptime(body['date_of_birth'], '%Y-%m-%d'),
                gender=body['gender'],
                phone_number=body['phone_number'],
                address=body['address'],
                user=user
            )
            session.add(profile)
            session.commit()
            session.refresh(profile)
            return jsonify({'profile_id': profile.id}), 200
        except Exception as e:
            session.rollback()
            print(f"Error creating profile: {e}")
            return jsonify({'error': 'An error occurred while creating the profile'}), 500
        finally:
            session.close()
        
    @staticmethod
    def get(profile_id: str) -> tuple:
        """
        Retrieve information about a specific profile.

        Args:
            profile_id (str): The ID of the profile.

        Returns:
            tuple: A tuple containing JSON response and HTTP status code.
        """
        # Cast the profile_id to an int
        profile_id = int(profile_id)

        session = Session()
        profile = session.query(ProfileDAO).filter(ProfileDAO.id == profile_id).first()
        if profile:
            profile_info = {
                "date_of_birth": profile.date_of_birth.isoformat(),
                "gender": profile.gender,
                "phone_number": profile.phone_number,
                "address": profile.address
            }
            session.close()
            return jsonify(profile_info), 200
        else:
            session.close()
            return jsonify({'message': f'No profile found with user id {profile_id}'}), 404
    
    @staticmethod
    def delete(profile_id: str) -> tuple:
        """
        Delete a specific profile.

        Args:
            profile_id (str): The ID of the profile.

        Returns:
            tuple: A tuple containing JSON response and HTTP status code.
        """

        # Cast the profile_id to an int
        profile_id = int(profile_id)

        session = Session()
        affected_rows = session.query(ProfileDAO).filter(ProfileDAO.id == profile_id).delete()
        session.commit()
        session.close()
        if affected_rows == 0:
            return jsonify({'message': f'No profile found with id {profile_id}'}), 404
        else:
            return jsonify({'message': 'Profile deleted successfully'}), 200
    
    @staticmethod
    def update(profile_id: str,body: dict) -> tuple:
        """
        Update information about a specific profile.

        Args:
            profile_id (str): The ID of the profile.
            body (dict): The request body containing updated profile information.

        Returns:
            tuple: A tuple containing JSON response and HTTP status code.
        """

        # Cast the profile_id to an int
        profile_id = int(profile_id)

        session = Session()
        profile = session.query(ProfileDAO).filter(ProfileDAO.id == profile_id).first()
        if profile:
            profile.date_of_birth = body.get('first_name', profile.date_of_birth)
            profile.gender = body.get('last_name', profile.gender)
            profile.phone_number = body.get('email_address', profile.phone_number)
            profile.address = body.get('password', profile.address) 
            session.commit()
            session.close()
            return jsonify({'message': 'Profile updated successfully'}), 200
        else:
            session.close()
            return jsonify({'message': f'No profile found with id {profile_id}'}), 404
        
class NotificationSettings:
    @staticmethod
    def get(user_id: str) -> tuple:
        """
        Retrieve information about a specific notificationsetting.

        Args:
            user_id (str): The ID of the user.

        Returns:
            tuple: A tuple containing JSON response and HTTP status code.
        """
        # Cast the user_id to an int
        user_id = int(user_id)

        session = Session()
        # Find the foreign id in the user table
        settings_foreign_id = session.query(UserDOA.notification_id).filter(UserDOA.id == user_id).scalar()
     
        # Get the notification_id table with the correct primairy key
        settings = session.query(NotificationSettingsDAO).filter(NotificationSettingsDAO.id == settings_foreign_id).first()
        
        if settings:
            settings_info = {
                "chat_notification": settings.chat_notification,
                "forum_notification": settings.forum_notification,
                "review_notification": settings.review_notification,
                "booking_notification": settings.booking_notification
            }
            session.close()
            return jsonify(settings_info), 200
        else:
            session.close()
            return jsonify({'message': f'No settings found for Notification id {settings_foreign_id}'}), 404
    


    @staticmethod
    def update(notification_id: int, body: dict) -> tuple:
        """
        Update information about a specific notificationsetting.

        Args:
            notification_id (int): The ID of the profile.
            body (dict): The request body containing updated profile information.

        Returns:
            tuple: A tuple containing JSON response and HTTP status code.
        """
        # Cast the notification_id to an int
        notification_id = int(notification_id)
        
        session = Session()
        settings = session.query(NotificationSettingsDAO).filter(NotificationSettingsDAO.id == notification_id).first()
        if settings:
            settings.chat_notification = body.get('chat_notification', settings.chat_notification)
            settings.forum_notification = body.get('forum_notification',settings.forum_notification)
            settings.review_notification = body.get('review_notification',settings.review_notification)
            settings.booking_notification = body.get('booking_notification',settings.booking_notification)
            session.commit()
            session.close()
            return jsonify({'message': 'User updated successfully'}), 200
        else:
            session.close()
            return jsonify({'message': f'No Notification found with id {notification_id}'}), 404