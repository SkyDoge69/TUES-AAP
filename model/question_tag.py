from model.question import Question
from database import SQLite
from errors import ApplicationError

class Question_tag(object):
 
    def __init__(self, question_id, tag_id, question_tag_id=None):
        self.id = question_tag_id
        self.question_id = question_id
        self.tag_id = tag_id


    def to_dict(self):
        question_tag_data = self.__dict__
        return question_tag_data
 
    def save(self):
        with SQLite() as db:
            cursor = db.execute(self.__get_save_query())
            self.id = cursor.lastrowid
        return self
 
    @staticmethod
    def delete(question_tag_id):
        result = None
        with SQLite() as db:
            result = db.execute("DELETE FROM question_tag WHERE id = ?",
                    (question_tag_id,))
        if result.rowcount == 0:
            raise ApplicationError("No value present", 404)
 
    @staticmethod
    def find(question_tag_id):
        result = None
        with SQLite() as db:
            result = db.execute(
                    "SELECT question_id, tag_id, id FROM question_tag WHERE id = ?",
                    (question_tag_id,))
        tag = result.fetchone()
        if tag is None:
            raise ApplicationError(
                    "Tag with id {} not found".format(question_tag_id), 404)
        return Question_tag(*tag)
    

    @staticmethod
    def find_by_tag_id(tag_id):
        result = None
        with SQLite() as db:
            result = db.execute(
                    "SELECT question_id, tag_id, id FROM question_tag WHERE tag_id = ?",
                    (tag_id,))
        question_tag = result.fetchone()
        if question_tag is None:
            return None
        return Question_tag(*question_tag)
    
    @staticmethod
    def all_question_tags():
        with SQLite() as db:
            result = db.execute(
                    "SELECT question_id, tag_id, id FROM question_tag").fetchall()                    
            return [' | '.join(name) for name in result]
 
    @staticmethod
    def search_by_tags(tags):
        with SQLite() as db:
            query = '''
                    SELECT DISTINCT q.content, q.answer, q.user, q.category, q.id FROM question as q
                    JOIN question_tag as qt
                    on qt.question_id = q.id
                    JOIN tag as t on t.id = qt.tag_id where t.content IN ({})
                    '''.format(", ".join("?" for _ in tags))
            result = db.execute(query, tags)
            questions = result.fetchall()
            if questions is None:
                return []
            [print(q) for q in questions]
            return [Question(*q) for q in questions]

    #t.content IN (work, lady)

    @staticmethod
    def all():
        with SQLite() as db:
            result = db.execute(
                    "SELECT question_id, tag_id, id FROM question_tag").fetchall()
            return [Question_tag(*row) for row in result]
 
    def __get_save_query(self):
        query = "{} INTO question_tag {} VALUES {}"
        if self.id == None:
            args = (self.question_id, self.tag_id)
            query = query.format("INSERT", "(question_id, tag_id)", args)
        else:
            args = (self.id, self.question_id, self.tag_id)
            query = query.format("REPLACE", "(id, question_id, tag_id)", args)
        return query
