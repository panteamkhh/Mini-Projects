"""Unit tests for Question and QuizApp."""

import json
from main import Question, QuizApp


def test_question_is_correct():
    q = Question("2 + 2 = ?", ["3", "4", "5"], answer=1)
    assert q.is_correct(1) is True
    assert q.is_correct(0) is False


def test_quiz_app_loads_and_scores(tmp_path):
    questions_data = [
        {"text": "1 + 1 = ?", "options": ["1", "2", "3"], "answer": 1}
    ]
    file_path = tmp_path / "questions.json"
    file_path.write_text(json.dumps(questions_data))

    app = QuizApp(questions_file=str(file_path))
    assert len(app.questions) == 1
    assert app.questions[0].is_correct(1) is True
