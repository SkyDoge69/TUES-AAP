from database import SQLite
from errors import ApplicationError

class Tag(object):
 
    def __init__(self, content, question_id, tag_id=None):
        self.id = tag_id
        self.content = content
        self.question_id = question_id
 
    def to_dict(self):
        tag_data = self.__dict__
        return tag_data
 
    def save(self):
        with SQLite() as db:
            cursor = db.execute(self.__get_save_query())
            self.id = cursor.lastrowid
        return self
 
    @staticmethod
    def delete(tag_id):
        result = None
        with SQLite() as db:
            result = db.execute("DELETE FROM tag WHERE id = ?",
                    (tag_id,))
        if result.rowcount == 0:
            raise ApplicationError("No value present", 404)
 
    @staticmethod
    def find(tag_id):
        result = None
        with SQLite() as db:
            result = db.execute(
                    "SELECT content, question_id, id FROM tag WHERE id = ?",
                    (tag_id,))
        tag = result.fetchone()
        if tag is None:
            raise ApplicationError(
                    "Tag with id {} not found".format(tag_id), 404)
        return Tag(*tag)
    
    @staticmethod
    def find_by_content(content):
        result = None
        with SQLite() as db:
            result = db.execute(
                    "SELECT content, question_id, id FROM tag WHERE content = ?",
                    (content,))
        tag = result.fetchone()
        if tag is None:
            return 0
        return Tag(*tag)

    @staticmethod
    def find_by_question(question_id):
        result = None
        with SQLite() as db:
            result = db.execute(
                    "SELECT content, question_id, id FROM tag WHERE question_id = ?",
                    (question_id,))
        tag = result.fetchone()
        if tag is None:
            return None
        return Tag(*tag)
    
    @staticmethod
    def all_tags():
        with SQLite() as db:
            result = db.execute(
                    "SELECT content, question_id, id FROM tag").fetchall()                    
            return [' | '.join(name) for name in result]
 
    @staticmethod
    def all():
        with SQLite() as db:
            result = db.execute(
                    "SELECT content, question_id, id FROM tag").fetchall()
            return [Tag(*row) for row in result]
 
    def __get_save_query(self):
        query = "{} INTO tag {} VALUES {}"
        if self.id == None:
            args = (self.content, self.question_id)
            query = query.format("INSERT", "(content, question_id)", args)
        else:
            args = (self.id, self.content, self.question_id)
            query = query.format("REPLACE", "(id, content, question_id)", args)
        return query
