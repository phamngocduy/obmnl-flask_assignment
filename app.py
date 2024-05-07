# Import libraries
from flask import *

# Instantiate Flask functionality
app = Flask('flask assignment')

# Sample data
transactions = [
    {'id': 1, 'date': '2024-06-01', 'amount': 100},
    {'id': 2, 'date': '2024-06-02', 'amount': -200},
    {'id': 3, 'date': '2024-06-03', 'amount': 300}
]

# Read operation: List all transactions
@app.route('/')
def get_transactions():
    return render_template('transactions.html', transactions=transactions,
                            total_balance=total_balance()['Total Balance'])

# Create operation: Display add transaction form
@app.route('/create', methods=['GET', 'POST'])
def add_transaction():
    if request.method == 'POST':
        # Create a new transaction object using form field values
        transaction = {
            'id': len(transactions) + 1,
            'date': request.form['date'],
            'amount': float(request.form['amount'])
        }
        # Append the new transaction to the list
        transactions.append(transaction)
        # Redirect to the transactions list page
        return redirect(url_for('get_transactions'))
    # Render the form template to display the add transaction form
    return render_template('form.html')

# Update operation: Display edit transaction form
@app.route('/update/<int:transaction_id>', methods=['GET', 'POST'])
def put_transaction(transaction_id):
    for transaction in transactions:
        if transaction['id'] == transaction_id:
            break
    if request.method == 'POST':
        # Extract the updated values from the form fields
        date = request.form['date']
        amount = float(request.form['amount'])
        # Find the transaction with the matching ID and update its values
        transaction['date'] = date
        transaction['amount'] = amount
        # Redirect to the transactions list page
        return redirect(url_for('get_transactions'))
    # Find the transaction with the mathcing ID and render the edit form
    return render_template('edit.html', transaction=transaction)

# Delete operation: Delete a transaction
@app.route('/delete/<int:transaction_id>')
def del_transaction(transaction_id):
    # Find the transaction with the matching ID and remove it from the list
    for transaction in transactions:
        if transaction['id'] == transaction_id:
            transactions.remove(transaction)
            break
    # Redirect to the transactions list page
    return redirect(url_for('get_transactions'))

@app.route('/search', methods=['GET', 'POST'])
def search_transactions():
    if request.method == 'POST':
        min_amount = float(request.form['min_amount'])
        max_amount = float(request.form['max_amount'])
        filtered_transactions = []
        for transaction in transactions:
            if min_amount <= transaction['amount'] <= max_amount:
                filtered_transactions.append(transaction)
        return render_template('transactions.html',
                                transactions=filtered_transactions,
                                total_balance=total_balance()['Total Balance'])
    return render_template('search.html')

@app.route('/balance')
def total_balance():
    total_balance = 0
    for transaction in transactions:
        total_balance += transaction['amount']
    return { 'Total Balance': total_balance }

# Run the Flask app
if __name__ == '__main__':
    app.run(debug=True)