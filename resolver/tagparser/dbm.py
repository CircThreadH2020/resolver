import os
import sqlite3
from typing import List, Optional

from pydantic import BaseModel


class RegexPattern(BaseModel):
    """Model representing a regular expression pattern."""
    name: str
    pattern: str


class Tagstyle(BaseModel):
    """Model representing a tag style with an entire pattern and contents."""
    entire_pattern: RegexPattern
    contents: List[RegexPattern]


class DatabaseManagement:
    """Class for managing a SQLite database."""
    def __init__(self):
        """Initialize the DatabaseManagement class."""
        self.db_name = 'tagstyles.db'
        self.db_path = './resolver/tagparser'
        self.full_path = os.path.join(self.db_path, self.db_name)

    def health_check(self) -> bool:
        """Check the health of the database connection."""
        try:
            if not os.path.exists(self.full_path):
                print(f"Database file '{self.full_path}' does not exist.")
                return False

            conn = sqlite3.connect(self.full_path)
            conn.close()
            print("Database connection successful.")
            return True

        except sqlite3.Error as e:
            print(f"An error occurred while connecting to the database: {e}")
            raise

    def initialize_db(self) -> bool:
        """Initialize the database schema if it doesn't exist."""
        try:
            conn = sqlite3.connect(self.full_path)
            cur = conn.cursor()

            cur.execute('''
                CREATE TABLE IF NOT EXISTS tagstyles (
                    id INTEGER PRIMARY KEY,
                    name TEXT NOT NULL,
                    entire_pattern TEXT NOT NULL
                )
            ''')

            cur.execute('''
                CREATE TABLE IF NOT EXISTS contents (
                    id INTEGER PRIMARY KEY,
                    tagstyle_id INTEGER NOT NULL,
                    name TEXT NOT NULL,
                    pattern TEXT NOT NULL,
                    FOREIGN KEY (tagstyle_id) REFERENCES tagstyles(id)
                )
            ''')

            conn.commit()
        except sqlite3.Error as e:
            print(f"An error occurred: {e}")
            raise
        finally:
            if conn:
                conn.close()

        return True

    def add_tag(self, new_tag: Tagstyle) -> bool:
        """Add a new tag to the database."""
        try:
            conn = sqlite3.connect(self.full_path)
            cur = conn.cursor()

            cur.execute('''
                INSERT INTO tagstyles (name, entire_pattern)
                VALUES (?, ?)
            ''', (new_tag.entire_pattern.name, new_tag.entire_pattern.pattern))

            tagstyle_id = cur.lastrowid

            for content in new_tag.contents:
                cur.execute('''
                    INSERT INTO contents (tagstyle_id, name, pattern)
                    VALUES (?, ?, ?)
                ''', (tagstyle_id, content.name, content.pattern))

            conn.commit()
        except sqlite3.Error as e:
            print(f"An error occurred: {e}")
            raise
        finally:
            if conn:
                conn.close()

        return True

    def delete_tag_by_id(self, tagid: int) -> bool:
        """Delete a tag from the database by its ID."""
        try:
            conn = sqlite3.connect(self.full_path)
            cur = conn.cursor()

            cur.execute('DELETE FROM contents WHERE tagstyle_id = ?', (tagid,))
            cur.execute('DELETE FROM tagstyles WHERE id = ?', (tagid,))

            conn.commit()
        except sqlite3.Error as e:
            print(f"An error occurred: {e}")
            raise
        finally:
            if conn:
                conn.close()

        return True

    def delete_all_tags(self) -> bool:
        """Delete all tags from the database."""
        try:
            conn = sqlite3.connect(self.full_path)
            cur = conn.cursor()

            cur.execute('DELETE FROM contents')
            cur.execute('DELETE FROM tagstyles')

            conn.commit()
        except sqlite3.Error as e:
            print(f"An error occurred: {e}")
            raise
        finally:
            if conn:
                conn.close()

        return True

    def retrieve_all_tags_completly(self) -> List[Tagstyle]:
        """Retrieve all tags including all their contents."""
        tagstyles_rows = self.retrieve_all_tagstyles()
        all_tagstyles = []

        for tagstyle_row in tagstyles_rows:
            tagstyle_id, name, pattern = tagstyle_row

            try:
                tagstyle = self.retrieve_tag_by_id(tagstyle_id)
                if tagstyle:
                    all_tagstyles.append(tagstyle)
            except Exception as e:
                print(f"An error occurred while retrieving tag with ID {tagstyle_id}: {e}")
                raise

        return all_tagstyles

    def retrieve_all_tagstyles(self) -> List:
        """Retrieve all tags excluding the contents."""
        try:
            conn = sqlite3.connect(self.full_path)
            cur = conn.cursor()

            cur.execute('SELECT * FROM tagstyles')
            tagstyles_rows = cur.fetchall()

        except sqlite3.Error as e:
            print(f"An error occurred: {e}")
            raise
        finally:
            if conn:
                conn.close()

        return tagstyles_rows

    def retrieve_tag_by_id(self, tagid: int) -> Optional[Tagstyle]:
        """Retrieve a single tag by its ID."""
        try:
            conn = sqlite3.connect(self.full_path)
            cur = conn.cursor()

            cur.execute('SELECT * FROM tagstyles WHERE id = ?', (tagid,))
            tagstyle_row = cur.fetchone()

            if tagstyle_row is None:
                return None

            tagstyle_id, name, pattern = tagstyle_row

            cur.execute('SELECT name, pattern FROM contents WHERE tagstyle_id = ?', (tagstyle_id,))
            contents_rows = cur.fetchall()

            contents = [RegexPattern(name=row[0], pattern=row[1]) for row in contents_rows]
            entire_pattern = RegexPattern(name=name, pattern=pattern)
            tagstyle = Tagstyle(entire_pattern=entire_pattern, contents=contents)

        except sqlite3.Error as e:
            print(f"An error occurred: {e}")
            raise
        finally:
            if conn:
                conn.close()

        return tagstyle

    def update_tag_by_name(self, tagid: int, updated_tag: Tagstyle) -> bool:
        """Update a tagstyle entry in the database."""
        try:
            conn = sqlite3.connect(self.full_path)
            cur = conn.cursor()

            cur.execute('''
                UPDATE tagstyles
                SET name = ?, entire_pattern = ?
                WHERE id = ?
            ''', (updated_tag.entire_pattern.name, updated_tag.entire_pattern.pattern, tagid))

            cur.execute('DELETE FROM contents WHERE tagstyle_id = ?', (tagid,))

            for content in updated_tag.contents:
                cur.execute('''
                    INSERT INTO contents (tagstyle_id, name, pattern)
                    VALUES (?, ?, ?)
                ''', (tagid, content.name, content.pattern))

            conn.commit()
        except sqlite3.Error as e:
            print(f"An error occurred: {e}")
            raise
        finally:
            if conn:
                conn.close()

        return True
