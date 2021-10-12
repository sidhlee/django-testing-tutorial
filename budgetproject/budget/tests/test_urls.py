from django.test import SimpleTestCase

# use SimpleTestCase when you don't need access database
class TestUrls(SimpleTestCase):

    def test_list_url_is_resolved(self):
        assert 1 == 2
