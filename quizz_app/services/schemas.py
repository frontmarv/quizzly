from pydantic import BaseModel


class QuestionSchema(BaseModel):
    """Schema for a quiz question with options.

    Attributes:
        question_title: The question text
        question_options: List of possible answers
        correct_answer_index: Index of the correct answer (0-3 for 4 options)
    """
    question_title: str
    question_options: list[str]
    correct_answer_index: int


class QuizSchema(BaseModel):
    """Schema for a complete quiz with multiple questions.

    Attributes:
        title: Title of the quiz
        description: Description of the quiz content
        questions: List of questions in the quiz
    """
    title: str
    description: str
    questions: list[QuestionSchema]
