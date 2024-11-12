from transformers import pipeline

# Initialize the question-generation pipeline (customize with fine-tuned model if available)
question_generator = pipeline("question-generation", model="t5-small")
