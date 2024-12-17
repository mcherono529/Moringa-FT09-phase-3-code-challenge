from database.connection import cursor
class Magazine:
    def __init__(self,id, name, category='default'):
        self.name = name
        self.category = category
        self.id = id
        
    @property
    def id(self):
        return self._id
    
    @id.setter
    def id(self, id):
        if not isinstance(id, int):
            raise Exception("Invalid Id")
        cursor.execute('''
                       INSERT INTO magazines (name, category) VALUES (?, ?)
                       ''', (self._name, self._category))
        self._id = cursor.lastrowid
    @property
    def name(self):
        return self._name

    @name.setter
    def name(self, value):
        if not isinstance(value, str) and 2 <= len(value) <= 16:
            raise Exception("Invalid name")
        self._name = value

    @property
    def category(self):
        return self._category

    @category.setter
    def category(self, value):
        if not (isinstance(value, str) and len(value) > 0):
            raise Exception("invalid category")
        self._category = value

    def articles(self):
        cursor.execute('''
                       SELECT * FROM articles WHERE articles.magazine_id = ? ''', (self.id))
        articles = cursor.fetchall()
        return articles

    def contributors(self):
        cursor.execute(''''
                       SELECT DISTINCT authors.* FROM articles JOIN authors ON articles.author_id = authors.id WHERE articles.magazine_id = ?''', (self.id))
        authors = cursor.fetchall()
        return authors

    def article_titles(self):
        articles = self.articles()
        return [article.title for article in articles] if articles else None

    def contributing_authors(self):
        cursor.execute('''
                       SELECT authors.*, COUNT(articles.id) AS article_count FROM articles JOIN authors ON articles.author_id = authors.id WHERE articles.magazine_id = ? GROUP BY authors.id, authors.name HAVING COUNT(articles.id) > 2''', (self.id))
        authors = cursor.fetchall()
        
        if authors:
            return authors
        else:
            return None
    def __repr__(self):
        return f'<Magazine {self.name}>'