import json
import random

import gevent
from locust import User, task, between
from websocket import create_connection, WebSocketTimeoutException


class WebSocketQuizUser(User):
    wait_time = between(3, 5)

    def on_start(self):
        self.quiz_id = "quiz_111111"
        self.user_id = f"user_{random.randint(1, 100000)}"
        self.ws_url = f"ws://localhost:8000/api/v1/quiz/{self.quiz_id}?user_id={self.user_id}"
        self.ws = create_connection(self.ws_url, timeout=5)
        try:
            join_msg = self.ws.recv()
            print(f"[{self.user_id}] Joined: {join_msg}")
        except Exception as e:
            print(f"[{self.user_id}] Error on join: {e}")

    @task
    def submit_random_answer(self):
        possible_answers = [
            "A", "B", "C", "D",
            "True", "False",
            "42", "Python", "FastAPI",
            f"random_{random.randint(1, 1000)}"
        ]
        answer = random.choice(possible_answers)
        payload = {
            "event": "SUBMIT_ANSWER",
            "data": {"answer": answer}
        }
        try:
            self.ws.send(json.dumps(payload))
            response = self.ws.recv()
            print(f"[{self.user_id}] Sent answer '{answer}', received: {response}")
            gevent.sleep(random.uniform(0.1, 0.5))
        except WebSocketTimeoutException:
            print(f"[{self.user_id}] Timeout waiting for server response")
        except Exception as e:
            print(f"[{self.user_id}] Error during answer: {e}")

    def on_stop(self):
        try:
            self.ws.close()
        except Exception:
            pass
