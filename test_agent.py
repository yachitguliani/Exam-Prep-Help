import unittest
from unittest.mock import MagicMock, patch
from agent import ExamPrepAgent

class TestExamPrepAgent(unittest.TestCase):
    @patch('llm_client.genai')
    def test_start_session(self, mock_genai):
        # Setup mock for GenerativeModel
        mock_model = MagicMock()
        mock_chat = MagicMock()
        mock_response = MagicMock()
        mock_response.text = "Mocked Session Plan"
        
        mock_genai.GenerativeModel.return_value = mock_model
        mock_model.start_chat.return_value = mock_chat
        mock_chat.send_message.return_value = mock_response

        # We need to set the env var or patch it, but llm_client reads it on import or init.
        # Since we use dotenv, it should be fine if .env exists, or we can patch os.getenv
        with patch.dict('os.environ', {'GEMINI_API_KEY': 'test_key'}):
            agent = ExamPrepAgent()
            response = agent.start_session("Photosynthesis", "School", "Beginner")

        # Verify
        self.assertEqual(response, "Mocked Session Plan")
        self.assertEqual(agent.topic, "Photosynthesis")
        
        # Verify correct model calls
        mock_genai.GenerativeModel.assert_called()
        # Verify chat started with history excluding the last message
        mock_model.start_chat.assert_called()
        # Verify message sent
        mock_chat.send_message.assert_called()

    @patch('llm_client.genai')
    def test_handle_input_flash(self, mock_genai):
        mock_model = MagicMock()
        mock_chat = MagicMock()
        mock_response = MagicMock()
        mock_response.text = "Mocked Flash Card"
        
        mock_genai.GenerativeModel.return_value = mock_model
        mock_model.start_chat.return_value = mock_chat
        mock_chat.send_message.return_value = mock_response

        with patch.dict('os.environ', {'GEMINI_API_KEY': 'test_key'}):
            agent = ExamPrepAgent()
            agent.topic = "Algebra"
            
            response = agent.handle_input("FLASH")
        
        self.assertEqual(response, "Mocked Flash Card")
        
        # Verify the content sent to send_message matches (it should be the user prompt)
        args, _ = mock_chat.send_message.call_args
        sent_message = args[0]
        self.assertIn("Give me an ultra-short revision (FLASH mode)", sent_message)

if __name__ == '__main__':
    unittest.main()
