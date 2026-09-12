from flask import Flask, request
from flask import render_template
import mysql.connector
import os
from dotenv import load_dotenv

load_dotenv()

app = Flask(__name__)


# Database connection
def get_db_connection():
    return mysql.connector.connect(
        host=os.getenv("DB_HOST"),
        user=os.getenv("DB_USER"),
        password=os.getenv("DB_PASSWORD"),
        database=os.getenv("DB_NAME"),
        port=int(os.getenv("DB_PORT", 3306))
    )


# Home
@app.route("/")
def home():
    return "Welcome to InvestNest - Virtual Stock Trading Platform"


# Buy
@app.route("/buy", methods=["POST"])
def buy():
    user_id = request.form["user_id"]
    stock_id = request.form["stock_id"]

    try:
        quantity = int(request.form["quantity"])
    except (ValueError, TypeError):
        return "Quantity must be a valid number."

    if quantity <= 0:
        return "Quantity must be positive."

    db = get_db_connection()
    cursor = db.cursor(dictionary=True)

    try:
        # Get stock price
        cursor.execute(
            "SELECT current_price FROM stocks WHERE stock_id = %s",
            (stock_id,)
        )

        stock = cursor.fetchone()

        if stock is None:
            return "Stock not found."

        price = stock["current_price"]
        total_amount = price * quantity

        # Get user's cash balance
        cursor.execute(
            "SELECT cash_balance FROM users WHERE user_id = %s",
            (user_id,)
        )

        user = cursor.fetchone()

        if user is None:
            return "User not found."

        # Check available cash
        if user["cash_balance"] < total_amount:
            return "Insufficient cash."

        # Record BUY transaction
        cursor.execute(
            """
            INSERT INTO transactions
            (user_id, stock_id, txn_type, quantity, price_per_share)
            VALUES (%s, %s, 'BUY', %s, %s)
            """,
            (user_id, stock_id, quantity, price)
        )

        # Deduct cash
        cursor.execute(
            """
            UPDATE users
            SET cash_balance = cash_balance - %s
            WHERE user_id = %s
            """,
            (total_amount, user_id)
        )

        db.commit()

        return "Stock bought successfully."

    except Exception as e:
        db.rollback()
        return f"Transaction failed: {e}"

    finally:
        cursor.close()
        db.close()


# Sell
@app.route("/sell", methods=["POST"])
def sell():
    user_id = request.form["user_id"]
    stock_id = request.form["stock_id"]

    try:
        quantity = int(request.form["quantity"])
    except (ValueError, TypeError):
        return "Quantity must be a valid number."

    if quantity <= 0:
        return "Quantity must be positive."

    db = get_db_connection()
    cursor = db.cursor(dictionary=True)

    try:
        # Calculate current holdings
        cursor.execute(
            """
            SELECT COALESCE(
                SUM(
                    CASE
                        WHEN txn_type = 'BUY' THEN quantity
                        ELSE -quantity
                    END
                ), 0
            ) AS holdings
            FROM transactions
            WHERE user_id = %s AND stock_id = %s
            """,
            (user_id, stock_id)
        )

        result = cursor.fetchone()
        holdings = result["holdings"]

        # Check whether user owns enough shares
        if holdings < quantity:
            return "Not enough shares to sell."

        # Get current stock price
        cursor.execute(
            "SELECT current_price FROM stocks WHERE stock_id = %s",
            (stock_id,)
        )

        stock = cursor.fetchone()

        if stock is None:
            return "Stock not found."

        price = stock["current_price"]
        total_amount = price * quantity

        # Record SELL transaction
        cursor.execute(
            """
            INSERT INTO transactions
            (user_id, stock_id, txn_type, quantity, price_per_share)
            VALUES (%s, %s, 'SELL', %s, %s)
            """,
            (user_id, stock_id, quantity, price)
        )

        # Add cash to user's balance
        cursor.execute(
            """
            UPDATE users
            SET cash_balance = cash_balance + %s
            WHERE user_id = %s
            """,
            (total_amount, user_id)
        )

        db.commit()

        return "Stock sold successfully."

    except Exception as e:
        db.rollback()
        return f"Transaction failed: {e}"

    finally:
        cursor.close()
        db.close()





# Dashboard
# Dashboard
@app.route("/dashboard")
def dashboard():
    user_id = request.args.get("user_id", 1)
    search = request.args.get("search", "").strip()
    price_filter = request.args.get("price_filter", "").strip()

    db = get_db_connection()
    cursor = db.cursor(dictionary=True)

    try:
        # Get user information
        cursor.execute(
            """
            SELECT user_id, username, cash_balance, is_admin
            FROM users
            WHERE user_id = %s
            """,
            (user_id,)
        )

        user = cursor.fetchone()

        if user is None:
            return "User not found."

        # Get available stocks
        query = """
            SELECT stock_id, ticker, company_name, current_price
            FROM stocks
            WHERE 1=1
            """

        params = []

        if search:
        
            
            query += """
                AND (
                    ticker LIKE %s
                    OR company_name LIKE %s
                )
            """
            params.append(f"%{search}%")
            params.append(f"%{search}%")

        if price_filter == "below_1000":
            query += " AND current_price < %s"
            params.append(1000)

        elif price_filter == "1000_3000":
            query += " AND current_price BETWEEN %s AND %s"
            params.append(1000)
            params.append(3000)

        elif price_filter == "above_3000":
            query += " AND current_price > %s"
            params.append(3000)

        query += " ORDER BY ticker"

        cursor.execute(query, params)

        stocks = cursor.fetchall()

        return render_template(
            "dashboard.html",
            user=user,
            stocks=stocks
        )

    finally:
        cursor.close()
        db.close()

# Admin - Update Stock Price
@app.route("/admin/update-price", methods=["POST"])
def update_price():
    user_id = request.form["user_id"]
    stock_id = request.form["stock_id"]

    try:
        new_price = float(request.form["new_price"])
    except (ValueError, TypeError):
        return "Price must be a valid number."

    if new_price <= 0:
        return "Price must be positive."

    db = get_db_connection()
    cursor = db.cursor(dictionary=True)

    try:
        # Check whether user is admin
        cursor.execute(
            """
            SELECT is_admin
            FROM users
            WHERE user_id = %s
            """,
            (user_id,)
        )

        user = cursor.fetchone()

        if user is None:
            return "User not found."

        if not user["is_admin"]:
            return "Unauthorized. Admin access required."

        # Update stock price
        cursor.execute(
            """
            UPDATE stocks
            SET current_price = %s
            WHERE stock_id = %s
            """,
            (new_price, stock_id)
        )

        if cursor.rowcount == 0:
            return "Stock not found."

        db.commit()

        return "Stock price updated successfully."

    except Exception as e:
        db.rollback()
        return f"Price update failed: {e}"

    finally:
        cursor.close()
        db.close()


if __name__ == "__main__":
    app.run(debug=True)
