from transformers import pipeline, T5Tokenizer
import re

# Step 1: Load the text file
def load_text(file_path):
    with open(file_path, 'r') as file:
        text = file.read()
    return text

# Step 2: Preprocess the text
def preprocess_text(text):
    # Remove unwanted characters and normalize whitespace
    text = re.sub(r'\n+', ' ', text)  # Remove new lines
    text = re.sub(r'\s+', ' ', text)  # Remove extra spaces
    return text.strip()

# Step 3: Extract key concepts and generate questions
def generate_questions(text, n_questions=5):
    # Initialize the question generation pipeline
    question_generator = pipeline(
        "text2text-generation", 
        model="valhalla/t5-base-qg-hl", 
        tokenizer=T5Tokenizer.from_pretrained("valhalla/t5-base-qg-hl", legacy=False)
    )
    
    # Split the text into manageable chunks (e.g., sentences)
    sentences = re.split(r'(?<=[.!?]) +', text)
    
    questions = []
    for sentence in sentences:
        if len(sentence.strip()) > 30:  # Consider only non-trivial sentences
            inputs = f"generate questions: {sentence}"
            outputs = question_generator(inputs, clean_up_tokenization_spaces=True)
            for output in outputs:
                questions.append(output['generated_text'])
                
                # Limit the number of questions generated
                if len(questions) >= n_questions:
                    return questions
    return questions

# Step 4: Main function to orchestrate the steps
def main(file_path):
    text = load_text(file_path)
    processed_text = preprocess_text(text)
    questions = generate_questions(processed_text)
    
    for i, question in enumerate(questions, 1):
        print(f"Question {i}: {question}")

# Example usage
file_path = "./NOTE.txt"  # Replace with the path to your text file
main(file_path)
