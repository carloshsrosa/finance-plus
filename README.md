# CS50 Finance Plus!

<!-- <a href="https://carloshsrosa.github.io/finance-plus/" target="_blank"><img src="https://img.shields.io/badge/-Pages-000000?&logo=github" alt="GitHub Pages"></a> -->

#### Video Demo:  https://www.loom.com/share/516e865e41c9411c832992ea8c9a6307?sid=c8acc245-ab36-4e76-91a9-10454f6c5c32
#### Description:
This project is a web application built using **Flask**, a popular Python web framework. The application simulates a finance platform where users can manage fictional stocks. They can register for an account, log in, and perform various stock-related actions such as buying and selling stocks. Additionally, users can view the historical data of their transactions and check real-time stock prices. This project is designed to be a comprehensive learning experience, showcasing key concepts in web development, database management, and user authentication.

## Folder Structure

The project is organized into several directories and files, each serving a specific purpose. Below is a detailed description of the structure:

- **`flask_session/`**: This directory is used to store user session data. In Flask applications, sessions are used to store information about the user across different requests. This directory plays a crucial role in maintaining user authentication and ensuring that users stay logged in as they navigate the website. Flask session data can be stored in different ways (cookies, server-side, or a database), depending on the configuration of the app.

- **`static/`**: This directory contains all static files used by the application. Static files are resources that don’t change dynamically, such as images, stylesheets, and JavaScript files. These files are served directly to the client when requested.
  - `favicon.ico`: The favicon is a small icon that appears next to the page title in the browser tab. This file defines the favicon for the site.
  - `l_heart_validator.png`: This is an image file used within the application, potentially for branding or visual elements on the pages.
  - `styles.css`: The main stylesheet for the project. This file contains CSS rules that define the layout, colors, fonts, and overall appearance of the application. By customizing this file, you can change the look and feel of the website to match your design preferences.

- **`templates/`**: This folder contains all the HTML template files used by the Flask app. Flask uses the Jinja2 templating engine to render HTML templates dynamically. This allows the server to inject data into the HTML before sending it to the user's browser. Below are the specific templates used in the project:
  - `apology.html`: This template is used to display error messages or apology responses when the user encounters an issue. For instance, if the user tries to access a page they do not have permission for or inputs invalid data, this page will display an appropriate error message.
  - `buy.html`: This page is where users can buy stocks. It typically contains a form where the user enters the stock ticker and the number of shares they want to purchase. Once the user submits the form, the backend processes the transaction.
  - `chart.html`: Displays charts for visualizing stock data. This could include graphs showing stock performance over time, helping users make informed decisions about buying or selling stocks.
  - `history.html`: This template shows a user's transaction history, including all past stock purchases, sales, and the respective dates of each transaction. This is important for users to track their investment performance.
  - `index.html`: The homepage of the application. This page is typically the first one users see after logging in. It might provide an overview of the user's portfolio, including current stock holdings and account balance.
  - `layout.html`: The main layout template that all other pages inherit from. This file likely contains the common structure of the site, such as the header, footer, and navigation bar. It helps maintain a consistent look across all pages of the application.
  - `login.html`: The login page where users can enter their credentials to access their accounts. This form submits the user's email or username and password to the backend for authentication.
  - `quote.html`: This page allows users to check the real-time price of a stock. The user inputs a stock ticker symbol, and the app fetches and displays the latest price using an external API.
  - `register.html`: The page where new users can sign up for an account. This form typically collects information like username, email, and password, which are stored in the database for future logins.
  - `sell.html`: Similar to `buy.html`, this page is used to sell stocks. Users can select a stock they own and choose how many shares to sell.

- **`app.py`**: The main entry point for the Flask application. This file defines the routes (URLs) for the app and connects them to the appropriate functions. Each function renders a template or returns data to the user. For example, there may be a route for the homepage (`/`), one for checking stock quotes (`/quote`), and others for buying and selling stocks. This file also contains the configuration settings for the app, including session management and database connections.

- **`databases.py`**: This script manages the interactions between the Flask app and the database. It handles tasks such as querying the database for user data, inserting new transactions, and updating stock information. The project uses SQLite as its database, but this script can be adapted to work with other relational databases like PostgreSQL or MySQL if needed.

- **`finance.db`**: The SQLite database file. This is where all user data, stock transactions, and other relevant information are stored. SQLite is a lightweight database, making it ideal for small projects or development environments.

- **`helpers.py`**: This file contains helper functions that are used throughout the application to simplify code. For example, there may be a function to look up stock prices from an external API, a function to calculate the total value of a user's portfolio, or a function to handle user authentication.

- **`README.md`**: This file, which provides an overview of the project and instructions for setting it up and running it.

- **`requirements.txt`**: A list of all the Python dependencies required to run the project. By running `pip install -r requirements.txt`, all necessary libraries (such as Flask, requests, and any others) will be installed.

## Features

This project offers several key features that make it a comprehensive stock trading simulator:

1. **User Registration and Login**: Users can create an account and log in securely. This feature ensures that each user has their own personalized portfolio and transaction history.

2. **Real-Time Stock Quotes**: Users can check the current price of any stock by entering its ticker symbol. This feature is likely powered by an external API that provides up-to-date stock information.

3. **Buy and Sell Stocks**: Once logged in, users can buy and sell stocks. The app calculates the total cost (or profit) based on the number of shares and the stock's current price. Transactions are recorded in the user's history, and their account balance is updated accordingly.

4. **Transaction History**: Users can view a detailed history of all their past transactions, including the date, stock ticker, number of shares, and the price at which they bought or sold the stock.

5. **Data Visualization**: The app provides charts to help users visualize their stock performance over time, making it easier to track gains and losses.

## How to Run the Project

### Requirements

To run this project, you'll need the following:

- **Python 3.7+**: This project is built using Python, so you need to have Python installed on your machine.
- **Flask**: The web framework used for the project. You can install it via `pip`.
- **SQLite**: The database used to store user and stock data.

## Additional Required Libraries

In addition to the basic Flask setup, this project also requires additional Python libraries for handling data and displaying stock charts:

- **pandas**: Used for data manipulation and analysis. It simplifies working with stock data, making it easier to organize, filter, and process large datasets.
- **mplfinance**: This library is used to create financial charts such as candlestick charts, which can help visualize stock prices over time. It integrates well with pandas to create attractive visualizations of stock market data.
- **yfinance**: This library is used to fetch historical market data directly from Yahoo Finance. It simplifies getting up-to-date stock data, which can be used to display stock prices, trends, and charts in the application.

### Installation Steps

1. Clone the repository to your local machine:
   ```bash
   git clone https://github.com/carloshsrosa/finance-plus.git
