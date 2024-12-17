from database.connection import cursor, conn

class Article:
    def __init__(self, id, title, content, author_id, magazine_id):
        self.id = id
        self.title = title
        self.content = content
        self.author_id = author_id
        self.magazine_id = magazine_id
        self._save_to_db()

    def _save_to_db(self):
        cursor.execute(
            """
            INSERT INTO articles (title, content, author_id, magazine_id)
            VALUES (?, ?, ?, ?)
            """,
            (self.title, self.content, self.author_id, self.magazine_id)
        )
        conn.commit()
        self._id = cursor.lastrowid

    @property
    def title(self):
        return self._title

    @title.setter
    def title(self, value):
        if hasattr(self, "_title"):
            raise AttributeError("Title cannot be modified after initialization.")
        if not isinstance(value, str) or not (5 <= len(value) <= 50):
            raise ValueError("Title must be a string between 5 and 50 characters.")
        self._title = value

    def author(self):
        cursor.execute("SELECT * FROM authors WHERE id = ?", (self.author_id,))
        return cursor.fetchone()

    def magazine(self):
        cursor.execute("SELECT * FROM magazines WHERE id = ?", (self.magazine_id,))
        return cursor.fetchone()

    def __repr__(self):
        return f"Article(title='{self.title}')"
