import unittest
from peewee import *

from app import TimelinePost

MODELS = [TimelinePost]

test_db = SqliteDatabase(':memory:')

class TestTimelinePost(unittest.TestCase):
    def setUp(self):
        test_db.bind(MODELS, bind_refs=False, bind_backrefs=False)
        test_db.connect()
        test_db.create_tables(MODELS)
        
    def tearDown(self):
        test_db.drop_tables(MODELS)
        test_db.close()
        
    def test_create_timeline_post(self):
        post = TimelinePost.create(name="John Doe", email="john@example.com", content="Hello, world!")
        self.assertEqual(post.id, 1)
        second_post = TimelinePost.create(name="Jane Doe", email="jane@example.com", content="Hello, world!")
        self.assertEqual(second_post.id, 2)
        
        # Get timeline posts and assert that the posts are correct
        posts = TimelinePost.select()

        # Check that both posts were gotten
        self.assertEqual(len(posts), 2)

        # Check the content of the first post is correct
        self.assertEqual(posts[0].name, "John Doe")
        self.assertEqual(posts[0].email, "john@example.com")
        self.assertEqual(posts[0].content, "Hello, world!")

        # Check the content of the second post is correct
        self.assertEqual(posts[1].name, "Jane Doe")
        self.assertEqual(posts[1].email, "jane@example.com")
        self.assertEqual(posts[1].content, "Hello, world!")