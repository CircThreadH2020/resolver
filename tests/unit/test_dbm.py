import pytest
from .example_tags_importer import read_json_and_get_tags
from resolver.tagparser.dbm import DatabaseManagement, Tagstyle, RegexPattern

@pytest.fixture(scope="module")
def db_manager():
    # Initialize DatabaseManagement instance
    manager = DatabaseManagement()
    # Create a clean database for testing
    manager.initialize_db()
    yield manager
    # Delete all tags after testing
    manager.delete_all_tags()

@pytest.fixture
def sample_tags():
    path = './resolver/data/tagstyles.json'
    return read_json_and_get_tags(path)

def test_initialize_db(db_manager):
    # Check if tables are created
    assert db_manager.initialize_db() == True

def test_health_check(db_manager):
    # Test health check method
    assert db_manager.health_check() == True

def test_add_tags(db_manager, sample_tags):
    # Test adding tags
    for tag in sample_tags:
        assert db_manager.add_tag(tag) == True

def test_retrieve_tag_by_id(db_manager, sample_tags):
    # Add tags first
    for tag in sample_tags:
        db_manager.add_tag(tag)
    # Retrieve the added tags by id
    for index, tag in enumerate(sample_tags):
        retrieved_tag = db_manager.retrieve_tag_by_id(index + 1)
        # Check if retrieved tag matches the added tag
        assert retrieved_tag.entire_pattern.name == tag.entire_pattern.name
        assert retrieved_tag.entire_pattern.pattern == tag.entire_pattern.pattern
        assert retrieved_tag.contents[0].name == tag.contents[0].name
        assert retrieved_tag.contents[0].pattern == tag.contents[0].pattern

def test_update_tag_by_name(db_manager, sample_tags):
    # Add tags first
    for tag in sample_tags:
        db_manager.add_tag(tag)
    # Update the added tags
    for index in range(len(sample_tags)):
        updated_tag = Tagstyle(
            entire_pattern=RegexPattern(name=f"updated_name_{index}", pattern=f"updated_pattern_{index}"),
            contents=[
                RegexPattern(name=f"updated_content_name_{index}", pattern=f"updated_content_pattern_{index}")
            ]
        )
        assert db_manager.update_tag_by_name(index + 1, updated_tag) == True
        # Retrieve the updated tag by id
        retrieved_tag = db_manager.retrieve_tag_by_id(index + 1)
        # Check if retrieved tag matches the updated tag
        assert retrieved_tag.entire_pattern.name == updated_tag.entire_pattern.name
        assert retrieved_tag.entire_pattern.pattern == updated_tag.entire_pattern.pattern
        assert retrieved_tag.contents[0].name == updated_tag.contents[0].name
        assert retrieved_tag.contents[0].pattern == updated_tag.contents[0].pattern

def test_delete_tag_by_id(db_manager, sample_tags):
    # Add tags first
    for tag in sample_tags:
        db_manager.add_tag(tag)
    # Delete the added tags
    for index in range(len(sample_tags)):
        assert db_manager.delete_tag_by_id(index + 1) == True
        # Attempt to retrieve the deleted tag
        assert db_manager.retrieve_tag_by_id(index + 1) == None

def test_delete_all_tags(db_manager, sample_tags):
    # Add tags first
    for tag in sample_tags:
        db_manager.add_tag(tag)
    # Delete all tags
    assert db_manager.delete_all_tags() == True
    # Attempt to retrieve any tags after deletion
    assert db_manager.retrieve_all_tags_completly() == []
