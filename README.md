# CS50 Finance Plus!
#### Video Demo:  <URL HERE>
#### Description:
This is a web project based on **Flask**, which simulates a finance app where users can manage fictional stocks. The project includes features like buying and selling stocks, transaction history, and checking real-time stock prices.

## Folder Structure

- `flask_session/`: Directory where user sessions are stored.
- `static/`: Contains static files like images and stylesheets.
  - `favicon.ico`: Website icon.
  - `l_heart_validator.png`: Image used in the project.
  - `styles.css`: Stylesheet for the frontend.
- `templates/`: Directory with HTML files used as templates for rendering.
  - `apology.html`: Template to display error or apology messages.
  - `buy.html`: Page for buying stocks.
  - `chart.html`: Page to display charts.
  - `history.html`: User's transaction history.
  - `index.html`: Website homepage.
  - `layout.html`: Main layout template of the project.
  - `login.html`: User login page.
  - `quote.html`: Page to check stock quotes.
  - `register.html`: Page to register new users.
  - `sell.html`: Page for selling stocks.
  - `teste.html`: Test page (used for development or internal tests).
- `app.py`: Main file of the Flask project, responsible for running the server and handling routes.
- `databases.py`: Script related to the database, managing communication with the SQLite file.
- `finance.db`: SQLite database that stores user and transaction information.
- `helpers.py`: Helper functions used in the app to simplify operations.
- `README.md`: This file.
- `requirements.txt`: File with the Python dependencies needed to run the project.

## Features

- **Register and Login**: Allows users to sign up and log in to the system.
- **Stock Quotes**: Users can check stock prices in real-time.
- **Buy and Sell Stocks**: Users can simulate buying and selling stocks.
- **Transaction History**: Users can view a history of all transactions made.
- **Charts**: Displays charts for data visualization.

## How to Run the Project

### Requirements

- Python 3.7+
- Flask
- SQLite

### Installation

1. Clone this repository to your local machine:
   ```bash
   git clone https://github.com/carloshsrosa/finance-plus.git
