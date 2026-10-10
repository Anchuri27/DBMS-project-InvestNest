# InvestNest

### Virtual Stock Trading Platform

> **Practice Investing. Build a Better Tomorrow.**


InvestNest is a web-based virtual stock trading platform that allows users to buy and sell stocks using virtual money in a safe and risk-free environment.

The application provides an interactive interface for performing simulated stock transactions and manages user information, stock details, virtual account balances, and transaction records through a MySQL database.

## Key Features

- User Registration and Login
- Virtual Starting Balance of ₹1,00,000
- Stock Buying and Selling
- Portfolio Management
- Transaction History
- Leaderboard

## Technology Stack

- **Python** – Backend Programming
- **Flask** – Web Application Framework
- **MySQL** – Database Management
- **Aiven Cloud** – Cloud Database Hosting
- **HTML** – Frontend Structure
- **CSS** – User Interface Styling
- **Git** – Version Control
- **GitHub** – Code Collaboration

## How the Application Works

1. Users register or log in to the application.
2. Each user receives a virtual starting balance.
3. Users select available stocks for trading.
4. Users can buy or sell stocks using virtual money.
5. The application updates the user's virtual balance and stock holdings.
6. Transaction details are stored in the MySQL database.
7. Users can view their portfolio and transaction history.

## Starting Virtual Balance

Each user receives a virtual starting balance of:

**₹1,00,000**

The balance is used for simulated stock transactions and does not involve real money.

## Database Design

The application uses a MySQL database hosted on Aiven Cloud to store and manage trading-related information.

Main database tables include:

- **Users** – Stores user account details and virtual balances.
- **Stocks** – Stores stock information and current prices.
- **Transactions** – Stores buying and selling records.

The database is integrated with the Flask application to support storing, retrieving, and updating application data.

## Project Structure

```text
InvestNest/
│
├── app.py
├── requirements.txt
├── schema.sql
├── templates/
├── static/
└── README.md