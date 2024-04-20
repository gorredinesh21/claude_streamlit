from flask import Flask, request, jsonify
from pypdf import PdfReader
import anthropic

app = Flask(__name__)

# Initialize Anthropoc client
client = anthropic.Anthropic(api_key="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")

# Model name for text generation
MODEL_NAME = "claude-3-opus-20240229"

def get_completion(client, prompt):
    return client.messages.create(
        model=MODEL_NAME,
        max_tokens=2048,
        messages=[{"role": 'user', "content": prompt}]
    ).content[0].text

@app.route('/generate_summary', methods=['POST'])
def generate_summary():
    if 'pdf_file' not in request.files:
        return jsonify({'error': 'No PDF file provided'}), 400

    pdf_file = request.files['pdf_file']
    if pdf_file.filename == '':
        return jsonify({'error': 'No PDF file selected'}), 400

    reader = PdfReader(pdf_file)
    text = ''.join([page.extract_text() for page in reader.pages])

    prompt = f"""This is a Discovery call between 2 parties who are buyer and seller of a SAAS product , Company Litmos is Buyer and 6sense is seller . : <discovery_call>{text}</discovery_call>

Please do the following:
1. What are the Buying Criteria Litmos have?
2. What are the pain points or difficulties Litmos has?
3. What are the Business Initiatives Litmos has as a company?"""

    summary = get_completion(client, prompt)
    return jsonify({'summary': summary}), 200

if __name__ == '__main__':
    app.run(host='0.0.0.0',port=8000)
