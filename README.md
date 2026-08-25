# Finance Dashboard

#### Video Demo: TODO - YouTube video link will be added after recording

#### Description:

Finance Dashboard is a personal finance and investment portfolio tracking web application built with Python and Flask. The purpose of this project is to provide users with a simple interface where they can monitor financial markets, manage their personal investment portfolio, analyze portfolio performance, and visualize their financial data.

The application displays live financial market information, including cryptocurrencies, currencies, commodities, and major market indices. Users can create an account, log in securely, add assets to their portfolio, edit or delete portfolio entries, and monitor their overall investment performance.

## Features

The application provides several features for managing and analyzing a personal portfolio.

Users can register for an account and log in using their username and password. Each user's portfolio is stored separately in the SQLite database.

The dashboard allows users to add investment assets by selecting supported assets and entering the amount and purchase price. Users can later edit or delete portfolio entries.

The application calculates portfolio information such as total invested amount, current portfolio value, profit or loss, and percentage performance.

Portfolio data is also presented visually using charts. A portfolio allocation chart shows how the user's investments are distributed between different assets, while performance charts help the user understand how the portfolio changes over time.

The home page also displays selected live market prices so users can quickly see current market conditions before opening their portfolio.

## Supported Assets

The application supports several different financial asset categories, including:

- Bitcoin
- Ethereum
- Solana
- BNB
- Gold
- USD / TRY
- EUR / TRY
- GBP / TRY
- S&P 500
- BIST 100

The application can be extended with additional assets in the future.

## How the Application Works

When a user visits the application, the home page displays a short introduction and selected live market information.

A new user can create an account from the registration page. The application checks that the username is valid and that the password and password confirmation match before creating the account.

After logging in, the user can access the personal dashboard. The dashboard contains the user's portfolio and financial statistics.

When an asset is added, the application stores information such as the asset symbol, asset name, amount, and purchase price in the SQLite database. Current market prices are retrieved when needed and are used to calculate the current value of the user's investments.

The application then compares the purchase value with the current value to calculate profit or loss.

## Files and Folders

### app.py

`app.py` is the main application file. It contains the Flask application, routes, authentication logic, database operations, market-data retrieval, portfolio calculations, and dashboard functionality.

The main routes include the home page, registration, login, logout, dashboard, portfolio asset management, and portfolio performance requests.

### templates/

The `templates` directory contains the HTML templates used by the Flask application.

The templates define the structure and user interface of the application, including the home page, login page, registration page, and dashboard pages.

### static/

The `static` directory contains the application's front-end resources.

`style.css` contains the visual design of the application, including the dashboard layout, cards, buttons, colors, responsive design, and other interface elements.

`script.js` contains JavaScript functionality used by the application for client-side interactions.

### finance.db

The application uses SQLite as its database system. The database stores user accounts and portfolio information.

The database file is intentionally excluded from the GitHub repository using `.gitignore` because it can contain user-specific information.

### requirements.txt

`requirements.txt` contains the Python packages required to run the application.

The main dependencies include Flask, Flask-Session, CS50, yFinance, Pandas, Plotly, and Werkzeug.

### .gitignore

`.gitignore` prevents files such as the SQLite database, Python cache files, virtual environments, and environment files from being uploaded to GitHub.

## Financial Data

Market data is retrieved using the `yfinance` Python library, which provides access to financial information from Yahoo Finance.

The application uses this data to display current prices and calculate portfolio performance.

Because financial market prices change continuously, the values displayed by the application may be different each time the application is used.

## Database

SQLite is used for persistent data storage.

The application stores user information and portfolio records in the database. Each portfolio record is associated with a specific user so that users can only access their own portfolio data.

The database structure allows the application to store information such as usernames, password hashes, asset symbols, asset names, investment amounts, and purchase prices.

## Design Choices

Flask was selected because it provides a simple and flexible framework for building a Python web application while allowing the project to demonstrate concepts covered in CS50.

SQLite was selected as the database because the application does not require a large database server. It is lightweight, easy to integrate with Flask, and sufficient for a personal portfolio application.

The `yfinance` library was selected because the application requires financial market data. Instead of manually entering prices, the application can retrieve current market information programmatically.

Plotly was selected for data visualization because it allows portfolio information to be presented through interactive charts. Visualizing portfolio allocation and performance makes the financial information easier to understand.

The application uses HTML and CSS for the interface and JavaScript for client-side functionality. Responsive CSS was also used so that the application can adapt to different screen sizes.

## Security

Passwords are not stored as plain text. Passwords are processed using password hashing before being stored in the database.

The application also uses sessions to keep track of authenticated users and associate portfolio data with the correct account.

## Purpose

This project was developed as my CS50x Final Project to apply concepts learned throughout the course to a complete software application.

The project combines Python, Flask, SQL, HTML, CSS, JavaScript, APIs, databases, and data visualization into one application.

While developing the project, I practiced web application development, database management, API/data integration, financial data analysis, authentication, and front-end design.

The goal was to create a practical application that could be useful for tracking personal investments while also demonstrating the programming concepts learned during CS50x.

## Future Improvements

Possible future improvements include:

- Adding more financial assets
- Adding historical market charts for individual assets
- Adding news and financial market updates
- Adding more advanced portfolio performance metrics
- Adding price alerts
- Improving mobile support
- Adding additional security features
- Adding more detailed portfolio analytics

## Author

Aynur

GitHub: https://github.com/aynur0
