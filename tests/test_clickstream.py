import pytest


@pytest.fixture
def fake():
    from faker import Faker
    from faker_clickstream import ClickstreamProvider

    fake = Faker()
    fake.add_provider(ClickstreamProvider)
    fake.session_clickstream()
    return fake


def test_response_length(fake):
    res = fake.session_clickstream()
    assert len(res) > 0


def test_schema(fake):
    res = fake.session_clickstream()
    assert 'ip' in res[0]
