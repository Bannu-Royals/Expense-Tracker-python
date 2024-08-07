# Expense Tracker Application

This project is an Expense Tracker application built using Flask, MongoDB, and Plotly for data visualization. The application allows users to register, log in, add expenses, categorize them, and view various visual representations of their spending habits.

## Project Structure

### 1. Application Setup

The application starts by importing necessary modules and initializing the Flask app. It uses `flask_pymongo` for MongoDB integration and `plotly` for generating charts. The configuration is loaded from a separate `config.py` file which utilizes environment variables managed by `python-dotenv`.

### 2. MongoDB Initialization

The `PyMongo` instance is initialized with the Flask app configuration to manage the MongoDB database connection.

### 3. Routes

#### Index Route
The index route (`/`) renders the homepage.

#### Registration Route
The `/register` route handles user registration. Users can create a new account by providing a username, email, and password. The user data is stored in the MongoDB collection with an initial empty categories structure.

#### Login Route
The `/login` route manages user authentication. It verifies the user credentials and establishes a session if the credentials are correct.

#### Dashboard Route
The `/dashboard` route is accessible only to logged-in users. It retrieves the user's expense data from the database, organizes it by categories, and displays various charts (Pie Chart, Bar Chart, Line Chart, Histogram, Scatter Plot, Area Chart, Donut Chart, Treemap, Bubble Chart, Waterfall Chart) using Plotly.

#### Add Expense Route
The `/add_expense` route allows users to add new expenses. Users can input the amount, category, and date of the expense. The route updates the MongoDB document with the new expense data.

#### Update Expense Route
The `/update_expense/<expense_id>` route enables users to update existing expenses. Users can modify the amount, category, and date of an expense. If the category changes, the expense is moved to the new category, and the old category is deleted if it becomes empty.

#### Delete Expense Route
The `/delete_expense/<expense_id>` route handles the deletion of expenses. It removes the specified expense from the database and deletes the category if it becomes empty after the deletion.

### 4. Templates

The application uses Jinja2 templates to render HTML pages. The templates are stored in the `templates` directory and include `index.html`, `register.html`, `login.html`, `dashboard.html`, `add_expense.html`, and `update_expense.html`.

### 5. Data Visualization

The application uses Plotly to create various types of charts to visualize the user's expenses:
- **Pie Chart:** Shows the distribution of expenses by category.
- **Bar Chart:** Displays expenses over time.
- **Line Chart:** Illustrates the trend of expenses over time.
- **Histogram:** Represents the distribution of expense amounts.
- **Scatter Plot:** Plots expenses by category over time.
- **Area Chart:** Shows cumulative expenses over time.
- **Donut Chart:** A variant of the pie chart with a central hole, depicting expenses breakdown.
- **Treemap:** Visualizes the hierarchy of expenses by category.
- **Bubble Chart:** Similar to a scatter plot, with bubble sizes representing expense amounts.
- **Waterfall Chart:** Demonstrates the flow of expenses.

### 6. Session Management

The application uses Flask sessions to manage user login states. It stores the user ID in the session to track the logged-in user across different routes.

### 7. Error Handling

The application includes basic error handling to manage scenarios like missing users, expenses, or categories. It uses Flask's `abort` function to return appropriate HTTP status codes and messages.

## Getting Started

### Prerequisites

- Python 3.11
- MongoDB
- Flask
- Flask-PyMongo
- Plotly
- Pandas

### Installation

1. Clone the repository:

   ```bash
   git clone <repository-url>
   cd <repository-directory>
   ```

2. Create and activate a virtual environment:

   ```bash
   python3 -m venv venv
   source venv/bin/activate
   ```

3. Install the required dependencies:

   ```bash
   pip install -r requirements.txt
   ```

4. Set up environment variables:

   Create a `.env` file in the project root and add your configuration variables:

   ```plaintext
   SECRET_KEY=your_secret_key
   MONGO_URI=your_mongodb_uri
   ```

### Running the Application

1. Start the Flask development server:

   ```bash
   flask run
   ```

2. Open your web browser and navigate to `http://localhost:5000` to access the application.

### Deployment

For deployment, the application can be configured to run on a production server using WSGI servers like Gunicorn. Ensure that the MongoDB URI and other configurations are set appropriately for the production environment.

## Conclusion

This Expense Tracker application provides a comprehensive solution for tracking and visualizing personal expenses. With features for user authentication, expense categorization, and interactive data visualization, it offers a user-friendly interface to manage financial data effectively.
