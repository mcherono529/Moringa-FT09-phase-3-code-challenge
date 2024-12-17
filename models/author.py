from database.connection import cursor, conn

class Author:
    def __init__(self,id, name):
        self.name = name
        self.id = id
    @property
    def id(self):
        return self._id
    @id.setter
    def id(self, id):
        if not isinstance(id, int):
            raise Exception("Invalid Id")
        cursor.execute('''
                       INSERT INTO authors (id,name) VALUES (?,?)
                       ''', (self._id, self._name))
        self._id = cursor.lastrowid()
    @property
    def id(self):
        return self._id
    @id.setter
    def id(self, id):
        if not isinstance(id, int):
            raise Exception('Invalid id')
        self._id = id
    @property
    def name(self):
        return self._name

    @name.setter
    def name(self, value):
        if not hasattr(self, '_name'):
            if isinstance(value, str) and len(value) > 0:
                self._name = value
            else:
                raise Exception("Name must be a non-empty string")
        else:
            raise Exception("Cannot change name after initialization")

    def articles(self):
        cursor.execute("""
            SELECT articles.id, articles.title, magazines.id, magazines.name, magazines.category
            FROM articles
            JOIN magazines ON articles.magazine_id = magazines.id
            WHERE articles.author_id = ?
        """, (self.id,))
        articles = cursor.fetchall()
        return articles

    def magazines(self):
        cursor.execute("""
            SELECT DISTINCT magazines.id, magazines.name, magazines.category
            FROM magazines
            JOIN articles ON articles.magazine_id = magazines.id
            WHERE articles.author_id = ?
        """, (self.id,))
        magazines = cursor.fetchall()
        return magazines
    def __repr__(self):
        return f'<Author {self.name}>'