import os
import google.generativeai as genai
from dotenv import load_dotenv
import json
import logging
import re

# Set up logging
logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)

# Load environment variables from .env file
load_dotenv()

# Configure Google Generative AI client
api_key = os.getenv("API_KEY")
if not api_key:
    logger.error("API_KEY not found in environment variables")
    raise ValueError("API_KEY not set")

genai.configure(api_key=api_key)

def generate_questions(summary):
    logger.info("Generating questions from summary")
    
    # Generate content using the model
    model = genai.GenerativeModel("gemini-1.5-pro")
    prompt = (
        "Create a 10-item multiple-choice quiz about the following summary. "
        "Format your response as a JSON array of question objects. "
        "Each question object should have 'question', 'options', and 'correct_answer' keys. "
        "The 'options' should be an array of 4 strings. "
        "The 'correct_answer' should be the index (0-3) of the correct option. "
        "Here's the summary:\n\n" + summary
    )

    try:
        response = model.generate_content(prompt)
        response_text = response.text.strip()
        logger.info("Response generated successfully")
        
        # Remove markdown code block syntax if present
        json_str = re.sub(r'```json\n|\n```', '', response_text)
        
        # Parse the cleaned response as JSON
        questions = json.loads(json_str)
        logger.info(f"Processed {len(questions)} questions")
        
        return questions
    except json.JSONDecodeError as e:
        logger.error(f"JSON parsing error: {str(e)}")
        logger.debug(f"Cleaned JSON string: {json_str}")
        return None
    except Exception as e:
        logger.error(f"Error in generate_questions: {str(e)}")
        logger.debug(f"Raw response: {response_text if 'response_text' in locals() else 'No response generated'}")
        return None

if __name__ == "__main__":
    # Test the function
    test_summary = "This is a test summary. It contains information about a specific topic."
    result = generate_questions(test_summary)
    print(json.dumps(result, indent=2))