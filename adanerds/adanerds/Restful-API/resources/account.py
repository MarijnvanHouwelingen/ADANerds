from datetime import datetime
from flask import jsonify


from daos.account_doa import UserDAO,NotificationSettingsDAO,ProfileDAO
from db import Session

class User:
    @staticmethod
    def create(body):
        session = Session()
        user = UserDAO(
            user_name=body['user_name'],
            first_name=body['first_name'],
            last_name=body['last_name'],
            email_address=body['email_address'],
            password=body['password']  # This would be hashed in a real application
        )
        session.add(user)
        session.commit()
        session.refresh(user)
        session.close()
        return jsonify({'user_id': user.id}), 200

    @staticmethod
    def get(user_id):
        session = Session()
        user = session.query(UserDAO).filter(UserDAO.id == user_id).first()
        if user:
            user_info = {
                "user_name": user.user_name,
                "first_name": user.first_name,
                "last_name": user.last_name,
                "email_address": user.email_address
            }
            session.close()
            return jsonify(user_info), 200
        else:
            session.close()
            return jsonify({'message': f'No user found with id {user_id}'}), 404

    @staticmethod
    def update(user_id, body):
        session = Session()
        user = session.query(UserDAO).filter(UserDAO.id == user_id).first()
        if user:
            user.user_name = body.get('user_name', user.user_name)
            user.first_name = body.get('first_name', user.first_name)
            user.last_name = body.get('last_name', user.last_name)
            user.email_address = body.get('email_address', user.email_address)
            user.password = body.get('password', user.password)  # Again, consider hashing
            session.commit()
            session.close()
            return jsonify({'message': 'User updated successfully'}), 200
        else:
            session.close()
            return jsonify({'message': f'No user found with id {user_id}'}), 404

    @staticmethod
    def delete(user_id):
        session = Session()
        affected_rows = session.query(UserDAO).filter(UserDAO.id == user_id).delete()
        session.commit()
        session.close()
        if affected_rows == 0:
            return jsonify({'message': f'No user found with id {user_id}'}), 404
        else:
            return jsonify({'message': 'User deleted successfully'}), 200

class Profile:
    @staticmethod
    def create(user_id, body):
        session = Session()
        profile = ProfileDAO(
            user_id=user_id,
            date_of_birth=datetime.strptime(body['date_of_birth'], '%Y-%m-%d'),
            gender=body['gender'],
            phone_number=body['phone_number'],
            address=body['address']
        )
        session.add(profile)
        session.commit()
        session.refresh(profile)
        session.close()
        return jsonify({'profile_id': profile.id}), 200

    @staticmethod
    def get(user_id):
        session = Session()
        profile = session.query(ProfileDAO).filter(ProfileDAO.user_id == user_id).first()
        if profile:
            profile_info = {
                "user_id": profile.user_id,
                "date_of_birth": profile.date_of_birth.isoformat(),
                "gender": profile.gender,
                "phone_number": profile.phone_number,
                "address": profile.address
            }
            session.close()
            return jsonify(profile_info), 200
        else:
            session.close()
            return jsonify({'message': f'No profile found with user id {user_id}'}), 404
    
    @staticmethod
    def delete(user_id):
        session = Session()
        affected_rows = session.query(ProfileDAO).filter(ProfileDAO.id == user_id).delete()
        session.commit()
        session.close()
        if affected_rows == 0:
            return jsonify({'message': f'No profile found with id {user_id}'}), 404
        else:
            return jsonify({'message': 'User deleted successfully'}), 200
    
    @staticmethod
    def update(user_id,body):
        session = Session()
        profile = session.query(ProfileDAO).filter(ProfileDAO.user_id == user_id).first()
        if profile:
            profile.user_id = body.get('user_name', profile.user_id)
            profile.date_of_birth = body.get('first_name', profile.date_of_birth)
            profile.gender = body.get('last_name', profile.gender)
            profile.phone_number = body.get('email_address', profile.phone_number)
            profile.address = body.get('password', profile.address) 
            session.commit()
            session.close()
            return jsonify({'message': 'Profile updated successfully'}), 200
        else:
            session.close()
            return jsonify({'message': f'No profile found with id {user_id}'}), 404
        
class NotificationSettings:
    @staticmethod
    def get(user_id):
        session = Session()
        settings = session.query(NotificationSettingsDAO).filter(NotificationSettingsDAO.user_id == user_id).first()
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
            return jsonify({'message': f'No settings found for user id {user_id}'}), 404

    @staticmethod
    def update(user_id, body):
        session = Session()
        settings = session.query(NotificationSettingsDAO).filter(NotificationSettingsDAO.user_id == user_id).first()
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
            return jsonify({'message': f'No user found with id {user_id}'}), 404