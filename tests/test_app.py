import unittest
import os

os.environ["TESTING"] = "true"

from app import app

class AppTestCase(unittest.TestCase):
    def setUp(self):
       self.client = app.test_client()
    
    def test_home_page(self):
        response = self.client.get("/")
        # Check that the status code is 200
        self.assertEqual(response.status_code, 200)
        html = response.get_data(as_text=True)
        # Check the title of the website
        self.assertIn("<title>About</title>", html)
        
        # Check that the skills and hobbies are in the homepage
        skills = ['React', 'Python', 'JavaScript', 'Flask', 'REST APIs']
        hobbies = ['Soccer', 'Calisthenics', 'TV Shows', 'Gaming']

        for skill in skills:
            self.assertIn(f"<li>{skill}</li>", html)

        for hobby in hobbies:
            self.assertIn(f"<li>{hobby}</li>", html)
       
    def test_timeline(self):
        response = self.client.get('/api/timeline_post')
        self.assertEqual(response.status_code, 200)
        assert response.is_json
        json = response.get_json()
        
        self.assertIn("timeline_posts", json)
        
        # Add a timeline post and verify that it is added
        response = self.client.post('/api/timeline_post', data={'name': 'Andrew A', 'email': 'andrew@a.com', 'content': 'Andrew says hello'})
        self.assertEqual(response.status_code, 200)
        assert response.is_json
        response_json = response.get_json()
        self.assertEqual(response_json['name'], 'Andrew A')
        self.assertEqual(response_json['email'], 'andrew@a.com')
        self.assertEqual(response_json['content'], 'Andrew says hello')

    def test_malformed_timeline_post(self):
        response = self.client.post("/api/timeline_post", data={
            "email": "john@example.com",
            "content": "Hello world, I'm John!"
        })
        self.assertEqual(response.status_code, 400)
        self.assertIn("Invalid name", response.get_data(as_text=True))

        response = self.client.post("/api/timeline_post", data={
            "name": "John Doe",
            "email": "john@example.com",
            "content": ""
        })
        self.assertEqual(response.status_code, 400)
        self.assertIn("Invalid content", response.get_data(as_text=True))

        response = self.client.post("/api/timeline_post", data={
            "name": "John Doe",
            "email": "not-an-email",
            "content": "Hello world, I'm John!"
        })
        self.assertEqual(response.status_code, 400)
        self.assertIn("Invalid email", response.get_data(as_text=True))
