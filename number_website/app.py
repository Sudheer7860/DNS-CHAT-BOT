"""
Number Information Website - Flask Application
"""
from flask import Flask, render_template, request, jsonify
from number_utils import get_number_info, get_fun_facts

app = Flask(__name__)


@app.route('/')
def index():
    """Main page"""
    return render_template('index.html')


@app.route('/number/<int:num>')
def number_info(num):
    """Display information about a specific number"""
    info = get_number_info(num)
    facts = get_fun_facts(num)
    return render_template('result.html', info=info, facts=facts)


@app.route('/api/number/<int:num>')
def api_number_info(num):
    """API endpoint for number information"""
    info = get_number_info(num)
    facts = get_fun_facts(num)
    return jsonify({
        'info': info,
        'facts': facts
    })


@app.route('/search', methods=['POST'])
def search():
    """Handle number search"""
    try:
        number = int(request.form.get('number', 0))
        info = get_number_info(number)
        facts = get_fun_facts(number)
        return render_template('result.html', info=info, facts=facts)
    except ValueError:
        return render_template('index.html', error="Please enter a valid integer")


if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)
