from flask import Flask, render_template, request, jsonify
import json
from rapidfuzz import process, fuzz

app = Flask(__name__)

# Load table data
with open('handbook.json', 'r', encoding='utf-8') as f:
    tables = json.load(f)

# Flatten rows
all_rows = [row for table in tables for row in table]

# Extract first column values for search
first_col_values = []
for row in all_rows:
    if row:
        first_col_values.append(list(row.values())[0])

@app.route('/', methods=['GET', 'POST'])
def home():
    query = ""
    result = None
    suggestions = []

    if request.method == 'POST':
        query = request.form.get('term', '').strip()

        # Exact match on first column value
        for row in all_rows:
            first_val = list(row.values())[0] if row else ""
            if first_val.lower() == query.lower():
                result = row
                break

        # No exact match → use fuzzy suggestion
        if not result:
            matches = process.extract(query, first_col_values, scorer=fuzz.WRatio, limit=5)
            suggestions = [match[0] for match in matches if match[1] > 40]

    return render_template('term_search.html', query=query, result=result, suggestions=suggestions)

@app.route('/suggest', methods=['GET'])
def suggest():
    q = request.args.get('q', '').strip().lower()
    if not q:
        return jsonify([])

    matches = [val for val in first_col_values if val.lower().startswith(q)]
    return jsonify(matches[:5])

if __name__ == '__main__':
    app.run(debug=True)
