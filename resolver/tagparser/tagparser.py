import re
import sqlite3
from typing import Dict
from resolver.tagparser.dbm import DatabaseManagement, Tagstyle, RegexPattern


class AmbiguousTagError(Exception):
    """Exception raised when a tag is ambiguous to stored patterns."""

    def __init__(self, message="Tag is ambiguous to stored patterns"):
        super().__init__(message)


class InvalidTagError(Exception):
    """Exception raised when a tag is invalid according to stored patterns."""

    def __init__(self, message="Tag is invalid according to stored patterns"):
        super().__init__(message)


class Parser:
    """Parser class to parse tags against stored tag patterns in the database."""

    def __init__(self):
        """Initialize the Parser with a DatabaseManagement instance."""
        self.manager = DatabaseManagement()

    def parse_tag(self, tag: str) -> Tagstyle:
        """
        Parse a tag and extract its contents based on stored tag patterns.

        Args:
            tag (str): The tag to parse.

        Returns:
            Tagstyle: A Tagstyle object with the matched entire pattern and contents.

        Raises:
            AmbiguousTagError: If multiple patterns match the tag.
            InvalidTagError: If no patterns match the tag.
            Exception: If a database error occurs.
        """
        try:
            candidates = self.match_entire_pattern(tag)
            if len(candidates) != 1:
                if len(candidates) > 1:
                    raise AmbiguousTagError()
                else:
                    raise InvalidTagError()

            tagstyle_name = list(candidates.keys())[0]
            tagstyle_id = candidates[tagstyle_name]
            contents = self.match_contents(tagstyle_id, tag)

            items = [
                RegexPattern(name=item_name, pattern=item_pattern)
                for item_name, item_pattern in contents.items()
            ]
            parsed_tag = Tagstyle(
                entire_pattern=RegexPattern(name=tagstyle_name, pattern=tag),
                contents=items
            )
            return parsed_tag

        except sqlite3.Error as e:
            raise Exception(f"Database error: {e}")

    def match_entire_pattern(self, tag: str) -> Dict[str, int]:
        """
        Match the entire tag pattern against stored tag patterns.

        Args:
            tag (str): The tag to match.

        Returns:
            Dict[str, int]: A dictionary with tagstyle names as keys and their IDs as values.
        """
        tagstyles_rows = self.manager.retrieve_all_tagstyles()
        matches = {}
        for tagstyle_id, name, pattern in tagstyles_rows:
            if re.fullmatch(pattern, tag):
                matches[name] = tagstyle_id
        return matches

    def match_contents(self, tagstyle_id: int, tag: str) -> Dict[str, str]:
        """
        Match the contents of the tag against the stored tag pattern contents.

        Args:
            tagstyle_id (int): The ID of the tagstyle to match.
            tag (str): The tag to extract contents from.

        Returns:
            Dict[str, str]: A dictionary of extracted contents.

        Raises:
            InvalidTagError: If no matching tagstyle is found.
        """
        tagstyle = self.manager.retrieve_tag_by_id(tagstyle_id)
        if not tagstyle:
            raise InvalidTagError("No matching tag style found.")

        contents = {}
        for content in tagstyle.contents:
            match = re.search(content.pattern, tag)
            if match:
                contents[content.name] = match.group(1)

        return contents
        