from llm_client import LLMClient
from prompts import (
    SYSTEM_PROMPT, 
    INITIAL_SESSION_PROMPT, 
    EVALUATION_PROMPT,
    FLASH_PREFIX,
    DRILL_PREFIX,
    PAST_PAPER_PREFIX,
    INTERVIEW_PREFIX,
    CHEATSHEET_PREFIX,
    TEACH_PREFIX,
    COMPARE_PREFIX
)

class ExamPrepAgent:
    def __init__(self):
        self.llm = LLMClient()
        self.history = [{"role": "system", "content": SYSTEM_PROMPT}]
        self.topic = None
        self.exam_type = None
        self.difficulty = None
        self.weak_areas = []

    def start_session(self, topic, exam_type, difficulty):
        self.topic = topic
        self.exam_type = exam_type
        self.difficulty = difficulty
        
        prompt = INITIAL_SESSION_PROMPT.format(
            topic=topic,
            exam_type=exam_type,
            difficulty=difficulty
        )
        self.history.append({"role": "user", "content": prompt})
        
        response = self.llm.generate_response(self.history)
        self.history.append({"role": "assistant", "content": response})
        return response

    def handle_input(self, user_input):
        # customized prompt based on keywords or mode
        msg_content = user_input
        
        # Check for specific command keywords if explicitly passed, 
        # but usually the main loop handles the logic of "FLASH" etc. 
        # Here we just append to history and generate.
        
        # If the last assistant message was a question (Drill mode), we might want to evaluate.
        # But for simplicity, we rely on the system instruction to "Evaluate" if the user answers.
        
        # If user initiates a mode:
        cmd = user_input.split()[0].upper()
        if cmd == "FLASH":
            msg_content = FLASH_PREFIX + self.topic
        elif cmd == "DRILL":
            msg_content = DRILL_PREFIX + self.topic
        elif cmd == "PAST-PAPER":
            msg_content = PAST_PAPER_PREFIX + self.topic
        elif cmd == "INTERVIEW":
            msg_content = INTERVIEW_PREFIX + self.topic
        elif cmd == "CHEATSHEET":
            msg_content = CHEATSHEET_PREFIX + self.topic
        elif cmd == "TEACH":
            msg_content = TEACH_PREFIX + self.topic
        elif cmd == "COMPARE":
             msg_content = COMPARE_PREFIX + self.topic
        # ADAPTIVE is less of a prompt and more of a behavior; we can prompt the agent to be adaptive.
        
        self.history.append({"role": "user", "content": msg_content})
        
        response = self.llm.generate_response(self.history)
        self.history.append({"role": "assistant", "content": response})
        return response
