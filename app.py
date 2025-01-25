from flask import Flask, request, jsonify
from flask_cors import CORS
from transformers import pipeline, set_seed

app = Flask(__name__)
CORS(app)

# Set a random seed for reproducibility (optional)
set_seed(42)

# Load Hugging Face model
try:
    generator = pipeline("text-generation", model="EleutherAI/gpt-neo-125M")
    print("Model loaded successfully.")
except Exception as e:
    print(f"Error loading model: {e}")

# Root route for testing
@app.route("/", methods=["GET"])
def home():
    return jsonify({
        "message": "AI Social Media Assistant is running!",
        "instructions": "Send a POST request to /generate-post with {'topic': 'your_topic'}"
    })

# Route for generating social media posts
@app.route("/generate-post", methods=["POST"])
def generate_post():
    try:
        # Parse JSON input
        data = request.json
        if not data or "topic" not in data:
            return jsonify({"error": "Missing 'topic' in request body"}), 400
        
        # Extract the topic
        topic = data.get("topic", "default")
        
        # Generate text
        response = generator(f"Write a social media post about {topic}.", max_length=50, num_return_sequences=1)
        
        # Return the generated post
        return jsonify({"post": response[0]["generated_text"]})
    
    except Exception as e:
        return jsonify({"error": f"An error occurred: {str(e)}"}), 500

if __name__ == "__main__":
    app.run(debug=True)
