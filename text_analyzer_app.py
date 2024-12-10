import streamlit as st
import openai
import json
from typing import Tuple, List

# Configure OpenAI API
openai.api_key = st.secrets["OPENAI_API_KEY"]

def analyze_text(text: str) -> Tuple[str, List[dict]]:
    """Analyze text and generate quiz using ChatGPT."""
    
    # First prompt to classify the text
    classification_prompt = f"""
    Analyze the following text and classify it as either educational, operational, or procedural.
    Provide a brief explanation for your classification.
    
    Text: {text}
    """
    
    classification_response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=[{"role": "user", "content": classification_prompt}]
    )
    
    classification = classification_response.choices[0].message.content
    
    # Second prompt to generate quiz with more explicit formatting instructions
    quiz_prompt = f"""
    Create 3 multiple-choice questions based on the following text.
    Format your response as a valid JSON array of objects, with each object containing exactly these fields:
    - "question": the question text
    - "options": an array of 4 possible answers
    - "correct_answer": the correct option (must be one of the options)

    Example format:
    [
        {{
            "question": "What is the capital of France?",
            "options": ["London", "Paris", "Berlin", "Madrid"],
            "correct_answer": "Paris"
        }},
        ...
    ]

    Text: {text}
    """
    
    quiz_response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=[{"role": "user", "content": quiz_prompt}]
    )
    
    # Parse the quiz response into a structured format
    quiz_content = quiz_response.choices[0].message.content
    try:
        # Try to find JSON array in the response
        start_idx = quiz_content.find('[')
        end_idx = quiz_content.rfind(']') + 1
        if start_idx != -1 and end_idx != -1:
            json_str = quiz_content[start_idx:end_idx]
            quiz_questions = json.loads(json_str)
        else:
            st.error("Could not find valid JSON array in the response")
            quiz_questions = []
    except json.JSONDecodeError as e:
        st.error(f"Failed to parse JSON response: {str(e)}")
        quiz_questions = []
    except Exception as e:
        st.error(f"An error occurred: {str(e)}")
        quiz_questions = []
    
    return classification, quiz_questions

def main():
    st.title("Text Analysis and Quiz Generator")
    st.write("Upload a text file to analyze its type and generate a quiz.")
    
    uploaded_file = st.file_uploader("Choose a text file", type="txt")
    
    if uploaded_file is not None:
        text_content = uploaded_file.read().decode("utf-8")
        
        if st.button("Analyze and Generate Quiz"):
            with st.spinner("Analyzing text and generating quiz..."):
                try:
                    classification, quiz_questions = analyze_text(text_content)
                    
                    # Display classification
                    st.subheader("Text Classification")
                    st.write(classification)
                    
                    # Display quiz
                    st.subheader("Quiz")
                    if quiz_questions:
                        for i, question in enumerate(quiz_questions, 1):
                            st.write(f"\nQuestion {i}: {question['question']}")
                            
                            # Create radio buttons for options
                            user_answer = st.radio(
                                f"Select your answer for question {i}:",
                                question['options'],
                                key=f"question_{i}"
                            )
                            
                            # Add a button to show the correct answer
                            if st.button(f"Show correct answer for question {i}", key=f"show_answer_{i}"):
                                if user_answer == question['correct_answer']:
                                    st.success("Correct! ✅")
                                else:
                                    st.error(f"Incorrect. The correct answer is: {question['correct_answer']}")
                    else:
                        st.error("Failed to generate quiz questions. Please try again.")
                except Exception as e:
                    st.error(f"An error occurred: {str(e)}")

if __name__ == "__main__":
    main()