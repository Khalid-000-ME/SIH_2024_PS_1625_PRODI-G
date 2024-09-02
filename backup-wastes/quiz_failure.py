from transformers import T5ForConditionalGeneration, T5Tokenizer, Trainer, TrainingArguments
from datasets import load_dataset

# Load the dataset
dataset = load_dataset('json', data_files={'train': 'E:/sih2024/quiz/data.json'})

# Split the dataset into training and validation sets
split_datasets = dataset['train'].train_test_split(test_size=0.2)  # 20% for validation

# Access the train and validation datasets
train_dataset = split_datasets['train']
val_dataset = split_datasets['test']

# Load a pretrained T5 model and tokenizer
model_name = "t5-small"  # You can also use "t5-base" or "t5-large"
model = T5ForConditionalGeneration.from_pretrained(model_name)
tokenizer = T5Tokenizer.from_pretrained(model_name, legacy=False)

def preprocess_function(examples):
    inputs = examples['context']
    targets = examples['question']
    
    # Tokenize inputs and targets
    model_inputs = tokenizer(inputs, max_length=512, truncation=True, padding='max_length')
    with tokenizer.as_target_tokenizer():
        labels = tokenizer(targets, max_length=64, truncation=True, padding='max_length')

    model_inputs['labels'] = labels['input_ids']
    return model_inputs

# Process the datasets
processed_train_dataset = train_dataset.map(preprocess_function, batched=True)
processed_val_dataset = val_dataset.map(preprocess_function, batched=True)

# Define training arguments
training_args = TrainingArguments(
    per_device_train_batch_size=4,
    per_device_eval_batch_size=4,
    num_train_epochs=3,
    logging_dir='./logs',
    logging_steps=10,
    eval_strategy="epoch",  # Updated from 'evaluation_strategy'
    save_strategy="epoch",
    output_dir='./results'
)

# Initialize Trainer with both train and eval datasets
trainer = Trainer(
    model=model,
    args=training_args,
    train_dataset=processed_train_dataset,
    eval_dataset=processed_val_dataset
)

# Train the model
trainer.train()

# Save the fine-tuned model and tokenizer
model.save_pretrained('./fine-tuned-t5')
tokenizer.save_pretrained('./fine-tuned-t5')

# Reload the fine-tuned model and tokenizer
model = T5ForConditionalGeneration.from_pretrained('./fine-tuned-t5')
tokenizer = T5Tokenizer.from_pretrained('./fine-tuned-t5')

# Function to generate questions
def generate_question(text):
    input_text = f"question: {text}"
    input_ids = tokenizer.encode(input_text, return_tensors="pt")

    # Generate question
    outputs = model.generate(
        input_ids,
        max_length=64,
        num_beams=5,
        early_stopping=True,
        do_sample=True
    )
    question = tokenizer.decode(outputs[0], skip_special_tokens=True, clean_up_tokenization_spaces=True)
    
    return question

# Example usage
text = "The Eiffel Tower is a wrought-iron lattice tower on the Champ de Mars in Paris, France."
print(generate_question(text))
