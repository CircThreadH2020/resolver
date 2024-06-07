import pytest
from unittest.mock import patch
from resolver.tagparser.dbm import DatabaseManagement, RegexPattern, Tagstyle
from resolver.tagparser.tagparser import Parser, AmbiguousTagError, InvalidTagError

@pytest.fixture
def sample_tagstyle():
    """Fixture to create a sample Tagstyle object for testing."""
    entire_pattern = RegexPattern(name="example_tag", pattern=r"http://example.com/\d+")
    contents = [
        RegexPattern(name="id", pattern=r"http://example.com/(\d+)")
    ]
    return Tagstyle(entire_pattern=entire_pattern, contents=contents)

@pytest.fixture
def parser():
    """Fixture to create a Parser object for testing."""
    return Parser()

def test_match_entire_pattern(parser, sample_tagstyle):
    """Test matching entire pattern."""
    with patch.object(DatabaseManagement, 'retrieve_all_tagstyles', return_value=[
        (1, "example_tag", r"http://example.com/\d+")
    ]):
        matches = parser.match_entire_pattern("http://example.com/12345")
        assert matches == {"example_tag": 1}

def test_match_contents(parser, sample_tagstyle):
    """Test matching contents."""
    with patch.object(DatabaseManagement, 'retrieve_tag_by_id', return_value=sample_tagstyle):
        contents = parser.match_contents(1, "http://example.com/12345")
        assert contents == {"id": "12345"}

def test_parse_tag_valid(parser, sample_tagstyle):
    """Test parsing a valid tag."""
    with patch.object(DatabaseManagement, 'retrieve_all_tagstyles', return_value=[
        (1, "example_tag", r"http://example.com/\d+")
    ]):
        with patch.object(DatabaseManagement, 'retrieve_tag_by_id', return_value=sample_tagstyle):
            parsed_tag = parser.parse_tag("http://example.com/12345")
            assert parsed_tag.entire_pattern.name == "example_tag"
            assert parsed_tag.entire_pattern.pattern == "http://example.com/12345"
            assert parsed_tag.contents[0].name == "id"
            assert parsed_tag.contents[0].pattern == "12345"

def test_parse_tag_ambiguous(parser):
    """Test parsing an ambiguous tag."""
    with patch.object(DatabaseManagement, 'retrieve_all_tagstyles', return_value=[
        (1, "example_tag", r"http://example.com/\d+"),
        (2, "example_tag_2", r"http://example.com/\d+")
    ]):
        with pytest.raises(AmbiguousTagError):
            parser.parse_tag("http://example.com/12345")

def test_parse_tag_invalid(parser):
    """Test parsing an invalid tag."""
    with patch.object(DatabaseManagement, 'retrieve_all_tagstyles', return_value=[]):
        with pytest.raises(InvalidTagError):
            parser.parse_tag("http://example.com/12345")
