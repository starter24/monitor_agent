from transformers import pipeline

# Load the summarization model once (using a smaller, faster model)
summarizer = pipeline("summarization", model="facebook/bart-large-cnn")

def summarize_text(text):
    try:
        # Clean and prepare the text
        text = text.strip()
        if len(text) < 10:
            return text
        
        # BART works best with text between 50-1024 tokens
        # Allow slightly longer summaries for better quality
        result = summarizer(
            text, 
            max_length=20,  # Increased from 15 for better sentences
            min_length=8, 
            do_sample=False,
            truncation=True
        )
        return result[0]['summary_text']
    except Exception as e:
        print(f"Summarization error: {e}")
        return "[Error] Failed to generate summary."

