import os
import google.generativeai as genai
from dotenv import load_dotenv
import json
import re

def process_response(response_text):
    print("Processing response...")
    print("Raw response text:")
    print(response_text)
    print("\n" + "=" * 50 + "\n")

    lines = response_text.split('\n')
    questions = []
    current_question = None
    options = {}
    answer_key = {}
    processing_questions = True

    for line in lines:
        line = line.strip()
        if line.startswith('**Answer Key:**') or line.startswith('Answer Key'):
            processing_questions = False
            if current_question:
                questions.append({
                    "question": current_question,
                    "options": options,
                    "answer": None  # We'll fill this in later
                })
            break
        
        if processing_questions:
            if line.startswith('**') and line.endswith('**'):
                if current_question:
                    questions.append({
                        "question": current_question,
                        "options": options,
                        "answer": None  # We'll fill this in later
                    })
                current_question = line.strip('**').strip(':')
                options = {}
            elif line.startswith(('a)', 'b)', 'c)', 'd)')):
                option, text = line.split(')', 1)
                options[option.strip()] = text.strip()

   # Add the last question if there was one
    if current_question:
        questions.append({
            "question": current_question,
            "options": options,
            "answer": None
        })

    # Process Answer Key
    answer_key_start = response_text.index('Answer Key')

    if answer_key_start != -1:
        answer_key_text = response_text[answer_key_start:]
        answer_lines = answer_key_text.split('\n')[1:]  # Skip the "Answer Key:" line
        for line in answer_lines:
            if line.strip():
                num, answer = line.split('.', 1)
                # Clean the answer by removing any unwanted characters
                cleaned_answer = answer.strip().replace('**', '').replace(')', '').strip()

                if cleaned_answer:
                    answer_key[int(num.strip()) - 1] = cleaned_answer[0]
                else:
                    print(f"Warning: Empty answer for question {num.strip()}")
                # answer_key[int(num.strip()) - 1] = answer.strip()[0] # Use 0-based index

    # Add answers to questions
    for i, question in enumerate(questions):
        if i in answer_key:
            question["answer"] = answer_key[i]

    print("\nProcessed Questions with Answers:")
    print(json.dumps(questions, indent=2))

    return questions

# Load environment variables from .env file
load_dotenv()

# Configure Google Generative AI client
genai.configure(api_key=os.getenv("API_KEY"))

# Read transcription from the text file
try:
    with open("summarized.txt", "r") as file:
        transcription = file.read()
    print("Transcription loaded successfully")
except IOError as e:
    print(f"Error reading summarized.txt: {e}")
    exit(1)

# Generate content using the model
model = genai.GenerativeModel("gemini-1.5-flash")
prompt = (
    "Create a 10-item multiple-choice quiz about the summary:\n\n" + transcription +  "\n\nPlease provide the answer key"
)

try:
    response = model.generate_content(prompt)
    response_text = response.text.strip()
    print("Response generated successfully")
except Exception as e:
    print(f"Error generating content: {e}")
    exit(1)

# Process the response
questions = process_response(response_text)

# Check if we have any questions
if not questions:
    print("No questions were extracted. Please check the response format.")
    exit(1)

# Save questions with answers to quiz.json
try:
    with open('quiz.json', 'w') as quiz_file:
        json.dump({"questions": questions}, quiz_file, indent=4)
    print("Quiz with questions and answers saved to quiz.json")
except IOError as e:
    print(f"Error writing to quiz.json: {e}")

print("Script execution completed.")