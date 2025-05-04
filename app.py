from flask import Flask, jsonify, request
import pandas as pd

app = Flask(__name__)

# Load the dataset
try:
    df = pd.read_csv('Viral_Social_Media_Trends.csv')
except FileNotFoundError:
    df = None
    print("Error: Dataset file not found. Please ensure 'Viral_Social_Media_Trends.csv' is in the project directory.")

# Helper function to convert DataFrame rows to JSON
def df_to_json(data):
    return data.to_dict(orient='records')

# Endpoint 1: Get all posts (with pagination)
@app.route('/posts', methods=['GET'])
def get_posts():
    if df is None:
        return jsonify({"error": "Dataset not loaded"}), 500

    # Handle page and per_page parameters
    try:
        page = int(request.args.get('page', 1))  # Default to page 1
        per_page = int(request.args.get('per_page', 10))  # Default to 10 posts per page
    except ValueError:
        return jsonify({"error": "Invalid 'page' or 'per_page' value, must be integers."}), 400

    # Calculate pagination
    start = (page - 1) * per_page
    end = start + per_page

    posts = df.iloc[start:end]
    return jsonify({
        "posts": df_to_json(posts),
        "total": len(df),
        "page": page,
        "per_page": per_page
    })

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)
