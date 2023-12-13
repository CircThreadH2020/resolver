from DOM_resolver.core import parse_tag
import samples


def test_parse_tag():
    expected_return = samples.TAG1_EXPECTED_PARSE
    assert parse_tag(samples.TAG1) == expected_return
