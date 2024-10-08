from django.test import TestCase
from media_platform.models import Content


class ContentTestCase(TestCase):
    def setUp(self):
        self.c1 = Content(rating=1)
        self.c1.save()

    def tearDown(self):
        pass

    def test_content_rating_validators(self):
        # Check that ratings cannot go below zero
        self.assertRaises(Exception, Content(rating=-1).save)

        # Check that ratings cannot go above 10
        self.assertRaises(Exception, Content(rating=11).save)

        # Check that you cannot update an existing content rating
        self.c1.rating = -1
        self.assertRaises(Exception, self.c1.save)
        self.c1.rating = 11
        self.assertRaises(Exception, self.c1.save)
