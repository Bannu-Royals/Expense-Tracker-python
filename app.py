from flask import Flask, render_template, request, redirect, url_for, session, abort
from flask_pymongo import PyMongo
import plotly.express as px
import plotly.graph_objects as go
import plotly.io as pio
import pandas as pd
from datetime import datetime
from bson.objectid import ObjectId  # Import ObjectId for MongoDB

app = Flask(__name__)
app.config.from_object('config.Config')

# Initialize PyMongo
mongo = PyMongo(app)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form['username']
        email = request.form['email']
        password = request.form['password']
        if mongo.db is not None:
            mongo.db.users.insert_one({"username": username, "email": email, "password": password})
        return redirect(url_for('login'))
    return render_template('register.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']
        user = mongo.db.users.find_one({"email": email})
        if user and user['password'] == password:
            session['user_id'] = str(user['_id'])
            return redirect(url_for('dashboard'))
    return render_template('login.html')

@app.route('/dashboard')
def dashboard():
    if 'user_id' not in session:
        return redirect(url_for('login'))

    user_id = session['user_id']
    expenses = list(mongo.db.expenses.find({"user_id": user_id}))

    df = pd.DataFrame(expenses)

    if not df.empty:
        df['date'] = pd.to_datetime(df['date'])
        df.sort_values(by='date', inplace=True)
        df['amount'] = df['amount'].astype(float)

        # Pie Chart
        pie_chart = px.pie(df, names='category', values='amount', title='Expenses by Category')
        pie_chart_html = pio.to_html(pie_chart, full_html=False)

        # Bar Chart
        bar_chart = px.bar(df, x='date', y='amount', title='Expenses Over Time')
        bar_chart_html = pio.to_html(bar_chart, full_html=False)

        # Line Chart
        line_chart = px.line(df, x='date', y='amount', title='Expenses Trend Over Time')
        line_chart_html = pio.to_html(line_chart, full_html=False)

        # Histogram
        histogram = px.histogram(df, x='amount', title='Distribution of Expense Amounts')
        histogram_html = pio.to_html(histogram, full_html=False)

        # Scatter Plot
        scatter_plot = px.scatter(df, x='date', y='amount', color='category', title='Expenses by Category Over Time')
        scatter_plot_html = pio.to_html(scatter_plot, full_html=False)

        # Area Chart
        area_chart = px.area(df, x='date', y='amount', color='category', title='Cumulative Expenses Over Time')
        area_chart_html = pio.to_html(area_chart, full_html=False)

        # Donut Chart
        donut_chart = px.pie(df, names='category', values='amount', hole=0.4, title='Expenses Breakdown')
        donut_chart_html = pio.to_html(donut_chart, full_html=False)

        # Treemap
        treemap = px.treemap(df, path=['category'], values='amount', title='Expenses by Category Hierarchy')
        treemap_html = pio.to_html(treemap, full_html=False)

        # Bubble Chart
        bubble_chart = px.scatter(df, x='date', y='amount', size='amount', color='category', title='Expenses by Category and Amount')
        bubble_chart_html = pio.to_html(bubble_chart, full_html=False)

        # Waterfall Chart
        waterfall_fig = go.Figure(go.Waterfall(
            measure=["absolute", "relative", "relative", "relative"],
            x=["Initial", "Expense 1", "Expense 2", "Total"],
            y=[0, 100, 50, 150],
            text=["", "100", "50", "150"],
            textposition="outside",
        ))
        waterfall_fig.update_layout(title="Expenses Flow")
        waterfall_chart_html = pio.to_html(waterfall_fig, full_html=False)

    else:
        pie_chart_html = ""
        bar_chart_html = ""
        line_chart_html = ""
        histogram_html = ""
        scatter_plot_html = ""
        area_chart_html = ""
        donut_chart_html = ""
        treemap_html = ""
        bubble_chart_html = ""
        waterfall_chart_html = ""

    return render_template('dashboard.html', pie_chart=pie_chart_html, bar_chart=bar_chart_html,
                           line_chart=line_chart_html, histogram=histogram_html, scatter_plot=scatter_plot_html,
                           area_chart=area_chart_html, donut_chart=donut_chart_html, treemap=treemap_html,
                           bubble_chart=bubble_chart_html, waterfall_chart=waterfall_chart_html, expenses=expenses)

@app.route('/add_expense', methods=['GET', 'POST'])
def add_expense():
    if request.method == 'POST':
        user_id = session['user_id']
        amount = float(request.form['amount'])
        category = request.form['category']
        date = request.form['date']
        mongo.db.expenses.insert_one({
            "user_id": user_id,
            "amount": amount,
            "category": category,
            "date": datetime.strptime(date, '%Y-%m-%d')
        })
        return redirect(url_for('dashboard'))
    return render_template('add_expense.html')

@app.route('/update_expense/<expense_id>', methods=['GET', 'POST'])
def update_expense(expense_id):
    if 'user_id' not in session:
        return redirect(url_for('login'))
    
    user_id = session['user_id']
    
    try:
        expense_id = ObjectId(expense_id)  # Convert string to ObjectId
    except Exception as e:
        print(f"Error converting expense_id: {e}")
        return abort(404, description="Invalid Expense ID")

    expense = mongo.db.expenses.find_one({"_id": expense_id, "user_id": user_id})

    if expense is None:
        return abort(404, description="Expense not found")

    if request.method == 'POST':
        amount = float(request.form['amount'])
        category = request.form['category']
        date = request.form['date']
        mongo.db.expenses.update_one({"_id": expense_id}, {
            "$set": {
                "amount": amount,
                "category": category,
                "date": datetime.strptime(date, '%Y-%m-%d')
            }
        })
        return redirect(url_for('dashboard'))
    
    # Ensure the date is a datetime object
    expense['date'] = expense['date'].strftime('%Y-%m-%d') if isinstance(expense['date'], datetime) else expense['date']

    return render_template('update_expense.html', expense=expense)


@app.route('/delete_expense/<expense_id>', methods=['POST'])
def delete_expense(expense_id):
    if 'user_id' not in session:
        return redirect(url_for('login'))

    user_id = session['user_id']
    
    try:
        expense_id = ObjectId(expense_id)  # Convert string to ObjectId
    except Exception as e:
        print(f"Error converting expense_id: {e}")
        return abort(404, description="Invalid Expense ID")

    result = mongo.db.expenses.delete_one({"_id": expense_id, "user_id": user_id})
    if result.deleted_count == 0:
        return abort(404, description="Expense not found")
    
    return redirect(url_for('dashboard'))

if __name__ == '__main__':
    app.run(debug=True)
