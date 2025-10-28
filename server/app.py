from flask import Flask, render_template, jsonify
from swiss_inflation import get_inflation_predictions

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/api/predictions')
def predictions():
    df = get_inflation_predictions()
    return jsonify(df.to_dict(orient='records'))

if __name__ == '__main__':
    app.run(debug=True)