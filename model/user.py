from database import SQLite
from errors import ApplicationError
from flask_login import UserMixin

class User(UserMixin):
 
    def __init__(self, name, password, choice, rating, room_id, user_id=None):
        self.id = user_id
        self.name = name
        self.password = password
        self.choice = choice
        self.rating = rating
        self.room_id = room_id
 
    def to_dict(self):
        user_data = self.__dict__
        return user_data

    def to_viewable(self):
        user_data = self.__dict__
        del user_data["password"]
        return user_data
 
    def save(self):
        with SQLite() as db:
            cursor = db.execute(self.__get_save_query())
            self.id = cursor.lastrowid
        return self
 
    @staticmethod
    def delete(user_id):
        result = None
        with SQLite() as db:
            result = db.execute("DELETE FROM user WHERE id = ?",
                    (user_id,))
        if result.rowcount == 0:
            raise ApplicationError("No value present", 404)
 
    @staticmethod
    def find(user_id):
        result = None
        with SQLite() as db:
            result = db.execute(
                    "SELECT name, password, choice, rating, room_id, id FROM user WHERE id = ?",
                    (user_id,))
        user = result.fetchone()
        # if user is None:
        #     raise ApplicationError(
        #             "User with id {} not found".format(user_id), 404)
        # return User(*user)

    @staticmethod
    def find_by_name(name):
        result = None
        with SQLite() as db:
            result = db.execute(
                    "SELECT name, password, choice, rating, room_id, id FROM user WHERE name = ?",
                    (name,))
        user = result.fetchone()
        if user is None:
            return None
        return User(*user)

    @staticmethod
    def find_closest_rating(choice, rating):
        print(choice)
        print(rating)
        result = None
        with SQLite() as db:
            result = db.execute(
                    "SELECT name, password, choice, rating, room_id, id FROM user WHERE choice = ? ORDER BY ABS(? - rating) LIMIT 1",
                    (choice, rating))
        user = result.fetchone()
        return User(*user)

    @staticmethod
    def update_choice(choice, name):
        result = None
        with SQLite() as db:
            result = db.execute("UPDATE user SET choice = ? WHERE name = ?",
                    (choice, name))
        if result.rowcount == 0:
            raise ApplicationError("No user present", 404)

    @staticmethod
    def get_last_registered():
        result = None
        with SQLite() as db:
            result = db.execute(
                    "SELECT * FROM user ORDER BY id DESC LIMIT 1",
                    )
        user = result.fetchone()
        if user is None:
            return None
        return User(*user)
    
 
    @staticmethod
    def all():
        with SQLite() as db:
            result = db.execute(
                    "SELECT name, password, choice, rating, room_id, id FROM user").fetchall()
            return [User(*row) for row in result]
 
    def __get_save_query(self):
        query = "{} INTO user {} VALUES {}"
        if self.id == None:
            args = (self.name, self.password, self.choice, self.rating, self.room_id)
            query = query.format("INSERT", "(name, password, choice, rating, room_id)", args)
        else:
            args = (self.id, self.name, self.password, self.choice, self.rating, self.room_id)
            query = query.format("REPLACE", "(id, name, password, choice, rating, room_id)", args)
        return query
