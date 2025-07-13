from flask_login import UserMixin

class User(UserMixin):
    def __init__(self, user_data):
        self.id = str(user_data['_id'])
        self.reg_id = user_data['reg_id']
        self.role = user_data['role']
