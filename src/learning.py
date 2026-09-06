"""Small formative assessment of the mechanism, with explanatory feedback."""

QUIZ = (
    {
        "question": "The encoder stayed identical, but predictions adapted. What carried the new association?",
        "options": ("The temporary fast memory", "A newly trained encoder", "The ordinary digit classifier"),
        "answer": "The temporary fast memory",
        "explanation": "Demonstrations update the memory matrix. The encoder's parameter tensors remain exactly unchanged.",
    },
    {
        "question": "After Clear Memory, what is still available?",
        "options": ("The encoder's digit representations", "All the episode's label associations", "Neither the encoder nor the memory"),
        "answer": "The encoder's digit representations",
        "explanation": "Reset removes temporary associations and returns predictions to abstention. It does not erase or retrain the encoder.",
    },
    {
        "question": "A wrong-label demonstration is added. What should we expect?",
        "options": ("The memory changes; measure the effect on predictions", "Accuracy must fall in every episode", "The frozen encoder rejects the label automatically"),
        "answer": "The memory changes; measure the effect on predictions",
        "explanation": "Fast memory accepts the supplied value, including a wrong one. Scores change, but accuracy may rise, fall or stay the same.",
    },
)


def quiz_feedback(question_index: int, answer: str) -> tuple[bool, str]:
    question = QUIZ[question_index]
    if answer not in question["options"]:
        raise ValueError("Answer is not one of the provided options")
    return answer == question["answer"], question["explanation"]
