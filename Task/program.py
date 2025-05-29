from flask import Flask, render_template, request, redirect, url_for
from flask_sqlalchemy import SQLAlchemy
import os

app = Flask("Hardware Expenses", template_folder="Task/templates")
basedir = os.path.abspath(os.path.dirname(__file__))
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + os.path.join(basedir, 'hardware_expenses.db')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

class Expense(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    hardware_part = db.Column(db.String(100), nullable=False)
    price = db.Column(db.Float, nullable=False)

    def __repr__(self):
        return f"<Expense {self.hardware_part} - {self.price}>"

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        hardware_part = request.form['hardware_part']
        price = request.form['price']
        try:
            price = float(price)
        except ValueError:
            price = 0.0

        if hardware_part and price >= 0:
            new_expense = Expense(hardware_part=hardware_part, price=price)
            db.session.add(new_expense)
            db.session.commit()
        return redirect(url_for('index'))
    
    expenses = Expense.query.all()
    total_price = sum(exp.price for exp in expenses)
    return render_template('index.html', expenses=expenses, total_price=total_price)

@app.route('/delete/<int:id>')
def delete_expense(id):
    exp_del = Expense.query.get_or_404(id)
    db.session.delete(exp_del)
    db.session.commit()
    return redirect(url_for('index'))

@app.route('/clear', methods=['POST'])
def clear_all():
    db.session.query(Expense).delete()
    db.session.commit()
    return redirect(url_for('index'))

if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(debug=True)
