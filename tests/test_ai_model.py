from ai_integration.ai_model import AIModel

def test_answer():
    model = AIModel()
    context = "The sky is blue."
    question = "What color is the sky?"
    assert "blue" in model.answer(context, question)
