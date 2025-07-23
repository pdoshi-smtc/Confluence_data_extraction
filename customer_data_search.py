from flask import Flask, render_template, request, jsonify
import json
from rapidfuzz import process, fuzz

app = Flask(__name__)

# Load JSON once
with open('customer_data.json', 'r', encoding='utf-8') as f:
    tables = json.load(f)

all_rows = [row for table in tables for row in table]
customer_names = [row.get("Customer Name", "") for row in all_rows]

@app.route('/')
def home():
    return render_template('search.html')

@app.route('/search', methods=['POST'])
def search_customer():
    search_query = request.form.get('customer_name', '').strip()
    result = None
    suggestions = []

    # Exact match
    for row in all_rows:
        if search_query.lower() == row.get("Customer Name", "").lower():
            result = row
            break

    # No match → provide top 5 suggestions
    if not result:
        matches = process.extract(
            search_query,
            customer_names,
            scorer=fuzz.WRatio,
            limit=5
        )
        suggestions = [match[0] for match in matches if match[1] > 50]

    return render_template('search.html', result=result, search_query=search_query, suggestions=suggestions)

@app.route('/suggest', methods=['GET'])
def suggest():
    q = request.args.get('q', '').strip().lower()
    if not q:
        return jsonify([])

    # Filter names that start with input (case-insensitive)
    matches = [name for name in customer_names if name.lower().startswith(q)]
    return jsonify(matches[:5])

if __name__ == '__main__':
    app.run(debug=True)
