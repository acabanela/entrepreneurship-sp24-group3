import unittest
from unittest.mock import patch
from app import app
import base64


class TestApp(unittest.TestCase):

    def setUp(self):
        app.config['TESTING'] = True
        self.app = app.test_client()

    def tearDown(self):
        pass

    def test_index(self):
        response = self.app.get('/')
        self.assertEqual(response.status_code, 200)

    def test_about(self):
        response = self.app.get('/about')
        self.assertEqual(response.status_code, 200)

    def test_learning_center(self):
        response = self.app.get('/learning_center')
        self.assertEqual(response.status_code, 200)

    def test_webcam(self):
        response = self.app.get('/webcam')
        self.assertEqual(response.status_code, 200)

    def test_webcam_scenario(self):
        response = self.app.get('/webcam_scenario')
        self.assertEqual(response.status_code, 200)

    @patch('app.DeepFace')
    def test_analyze(self, mock_deepface):
        mock_deepface.analyze.return_value = {'dominant_emotion': 'happy'}
        img_path = './static/images/Amadeo.png'
        with open(img_path, 'rb') as f:
            img_bytes = f.read()
        img_base64 = base64.b64encode(img_bytes).decode('utf-8')
        img_data = f"data:image/jpeg;base64,{img_base64}"
        response = self.app.post('/analyze', json={'imgData': img_data})
        self.assertEqual(response.status_code, 200)
        data = response.get_json()
        self.assertEqual(data['dominant_emotion'], 'happy')


if __name__ == '__main__':
    unittest.main()
