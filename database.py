import mysql.connector
from mysql.connector import Error
from dotenv import load_dotenv
import os
import bcrypt

load_dotenv()

DB_HOST = os.getenv("DB_HOST")
DB_USER = os.getenv("DB_USER")
DB_PASSWORD = os.getenv("DB_PASSWORD")
DB_NAME = os.getenv("DB_NAME")


def get_connection():
    try:
        connection = mysql.connector.connect(
            host=DB_HOST,
            user=DB_USER,
            password=DB_PASSWORD,
            database=DB_NAME
        )
        return connection

    except Error as e:
        print("Database connection error:", e)
        return None


# ---------------- USER FUNCTIONS ----------------

def create_user(username, email, password, role="staff"):

    conn = get_connection()
    cursor = conn.cursor()

    hashed_password = bcrypt.hashpw(password.encode(), bcrypt.gensalt())

    query = """
    INSERT INTO users (username, email, password_hash, role)
    VALUES (%s, %s, %s, %s)
    """

    try:
        cursor.execute(query, (username, email, hashed_password, role))
        conn.commit()
        return True

    except Exception as e:
        print(e)
        return False

    finally:
        cursor.close()
        conn.close()


def verify_user(username, password):

    conn = get_connection()
    cursor = conn.cursor(dictionary=True)

    query = "SELECT * FROM users WHERE username=%s"

    cursor.execute(query, (username,))
    user = cursor.fetchone()

    cursor.close()
    conn.close()

    if user:
        stored_password = user["password_hash"]

        if bcrypt.checkpw(
            password.encode(),
            stored_password.encode() if isinstance(stored_password, str) else stored_password
        ):
            return user

    return None


# ---------------- CATEGORY ----------------

def get_categories():

    conn = get_connection()
    cursor = conn.cursor(dictionary=True)

    cursor.execute("SELECT * FROM categories")

    data = cursor.fetchall()

    cursor.close()
    conn.close()

    return data


# ---------------- PRODUCTS ----------------

def get_all_products():

    conn = get_connection()
    cursor = conn.cursor(dictionary=True)

    query = """
    SELECT p.*, c.name AS category_name
    FROM products p
    LEFT JOIN categories c ON p.category_id = c.id
    ORDER BY p.created_at DESC
    """

    cursor.execute(query)

    data = cursor.fetchall()

    cursor.close()
    conn.close()

    return data


def add_product(name, sku, category_id, quantity, unit, price,
                reorder_level, location, description):

    conn = get_connection()
    cursor = conn.cursor()

    query = """
    INSERT INTO products
    (name, sku, category_id, quantity, unit, price,
     reorder_level, location, description)
    VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s)
    """

    try:
        cursor.execute(query, (
            name, sku, category_id, quantity,
            unit, price, reorder_level,
            location, description
        ))

        conn.commit()
        return True

    except Exception as e:
        print(e)
        return False

    finally:
        cursor.close()
        conn.close()


# ---------------- STOCK ----------------

def stock_in(product_id, quantity, user_id):

    conn = get_connection()
    cursor = conn.cursor()

    try:
        cursor.execute("""
        UPDATE products
        SET quantity = quantity + %s
        WHERE id = %s
        """, (quantity, product_id))

        cursor.execute("""
        INSERT INTO transactions
        (product_id, type, quantity, user_id)
        VALUES (%s, 'IN', %s, %s)
        """, (product_id, quantity, user_id))

        conn.commit()
        return True

    except Exception as e:
        print(e)
        return False

    finally:
        cursor.close()
        conn.close()


def stock_out(product_id, quantity, user_id):

    conn = get_connection()
    cursor = conn.cursor(dictionary=True)

    cursor.execute("SELECT quantity FROM products WHERE id=%s", (product_id,))
    product = cursor.fetchone()

    if product["quantity"] < quantity:
        return False

    try:
        cursor.execute("""
        UPDATE products
        SET quantity = quantity - %s
        WHERE id = %s
        """, (quantity, product_id))

        cursor.execute("""
        INSERT INTO transactions
        (product_id, type, quantity, user_id)
        VALUES (%s, 'OUT', %s, %s)
        """, (product_id, quantity, user_id))

        conn.commit()
        return True

    except Exception as e:
        print(e)
        return False

    finally:
        cursor.close()
        conn.close()


# ---------------- TRANSACTIONS ----------------

def get_transactions():

    conn = get_connection()
    cursor = conn.cursor(dictionary=True)

    query = """
    SELECT
        t.id,
        p.name AS product_name,
        t.type,
        t.quantity,
        u.username,
        t.created_at
    FROM transactions t
    LEFT JOIN products p ON t.product_id = p.id
    LEFT JOIN users u ON t.user_id = u.id
    ORDER BY t.created_at DESC
    """

    cursor.execute(query)

    data = cursor.fetchall()

    cursor.close()
    conn.close()

    return data


# ---------------- DASHBOARD STATS ----------------

def get_dashboard_stats():

    conn = get_connection()
    cursor = conn.cursor(dictionary=True)

    stats = {}

    cursor.execute("SELECT COUNT(*) AS total FROM products")
    stats["total_products"] = cursor.fetchone()["total"]

    cursor.execute("SELECT SUM(quantity * price) AS total_value FROM products")
    result = cursor.fetchone()["total_value"]
    stats["total_value"] = result if result else 0

    cursor.execute(
        "SELECT COUNT(*) AS low_stock FROM products WHERE quantity <= reorder_level"
    )
    stats["low_stock"] = cursor.fetchone()["low_stock"]

    cursor.execute(
        "SELECT COUNT(*) AS today_tx FROM transactions WHERE DATE(created_at)=CURDATE()"
    )
    stats["today_transactions"] = cursor.fetchone()["today_tx"]

    cursor.close()
    conn.close()

    return stats


# ---------------- CHART DATA ----------------

def get_products_by_category():

    conn = get_connection()
    cursor = conn.cursor(dictionary=True)

    query = """
    SELECT 
        c.name AS category,
        SUM(p.quantity) AS total_stock
    FROM products p
    JOIN categories c ON p.category_id = c.id
    WHERE p.quantity > 0
    GROUP BY c.name
    """

    cursor.execute(query)

    data = cursor.fetchall()

    cursor.close()
    conn.close()

    return data


def get_stock_movement():

    conn = get_connection()
    cursor = conn.cursor(dictionary=True)

    query = """
    SELECT 
        c.name AS category,
        t.type,
        COALESCE(SUM(t.quantity), 0) AS total
    FROM categories c
    LEFT JOIN products p ON p.category_id = c.id
    LEFT JOIN transactions t ON t.product_id = p.id
    GROUP BY c.name, t.type
    ORDER BY c.name
    """

    cursor.execute(query)

    data = cursor.fetchall()

    cursor.close()
    conn.close()

    return data


# ---------------- LOW STOCK ----------------

def get_low_stock_products():

    conn = get_connection()
    cursor = conn.cursor(dictionary=True)

    query = """
    SELECT 
        p.name,
        c.name AS category,
        p.quantity,
        p.reorder_level
    FROM products p
    JOIN categories c ON p.category_id = c.id
    WHERE p.quantity <= p.reorder_level
    """

    cursor.execute(query)

    data = cursor.fetchall()

    cursor.close()
    conn.close()

    return data

def get_transactions_by_date(start_date, end_date):

    conn = get_connection()
    cursor = conn.cursor(dictionary=True)

    query = """
    SELECT 
        DATE(created_at) AS date,
        type,
        SUM(quantity) AS total
    FROM transactions
    WHERE DATE(created_at) BETWEEN %s AND %s
    GROUP BY DATE(created_at), type
    ORDER BY date
    """

    cursor.execute(query, (start_date, end_date))

    data = cursor.fetchall()

    cursor.close()
    conn.close()

    return data