from flask import Blueprint, request, jsonify
from app.extensions import mysql
from ..utils.decorators import token_required, admin_required
import datetime

order_bp = Blueprint("orders", __name__)


# ---------------------------------------------------------
# CHECKOUT
# ---------------------------------------------------------
@order_bp.route("/orders/checkout", methods=["POST"])
@token_required
def checkout(decoded):
    try:
        user_id = decoded["user_id"]

        cur = mysql.connection.cursor()

        # 1️⃣ Get cart items
        cur.execute("""
            SELECT cart_items.product_id, cart_items.quantity, products.price, products.stock_quantity
            FROM cart_items
            JOIN cart ON cart.id = cart_items.cart_id
            JOIN products ON products.id = cart_items.product_id
            WHERE cart.user_id = %s
        """, (user_id,))
        items = cur.fetchall()

        if not items:
            return jsonify({"error": "Cart is empty"}), 400

        total_amount = 0

        # 2️⃣ Check stock & calculate total
        for item in items:
            product_id, quantity, price, stock = item

            if quantity > stock:
                return jsonify({"error": f"Not enough stock for product {product_id}"}), 400

            total_amount += quantity * float(price)

        # 3️⃣ Create order
        cur.execute("""
            INSERT INTO orders (user_id, total_amount, status, created_at)
            VALUES (%s, %s, %s, %s)
        """, (
            user_id,
            total_amount,
            "Completed",
            datetime.datetime.now()
        ))

        order_id = cur.lastrowid

        # 4️⃣ Insert order items & reduce stock
        for item in items:
            product_id, quantity, price, stock = item

            cur.execute("""
                INSERT INTO order_items (order_id, product_id, quantity, price)
                VALUES (%s, %s, %s, %s)
            """, (
                order_id,
                product_id,
                quantity,
                price
            ))

            # Reduce stock
            cur.execute("""
                UPDATE products
                SET stock_quantity = stock_quantity - %s
                WHERE id = %s
            """, (
                quantity,
                product_id
            ))

        # 5️⃣ Clear cart
        cur.execute("""
            DELETE FROM cart_items
            WHERE cart_id = (SELECT id FROM cart WHERE user_id = %s)
        """, (user_id,))

        mysql.connection.commit()

        return jsonify({
            "message": "Order placed successfully",
            "order_id": order_id,
            "total": total_amount
        }), 201

    except Exception as e:
        mysql.connection.rollback()
        return jsonify({"error": str(e)}), 500


# ---------------------------------------------------------
# GET USER ORDERS
# ---------------------------------------------------------
@order_bp.route("/orders", methods=["GET"])
@token_required
def get_user_orders(decoded):
    try:
        user_id = decoded["user_id"]

        cur = mysql.connection.cursor()
        cur.execute("""
            SELECT id, total_amount, status, created_at
            FROM orders
            WHERE user_id = %s
            ORDER BY created_at DESC
        """, (user_id,))
        orders = cur.fetchall()

        result = []
        for order in orders:
            result.append({
                "id": order[0],
                "total_amount": float(order[1]),
                "status": order[2],
                "created_at": order[3]
            })

        return jsonify(result), 200

    except Exception as e:
        return jsonify({"error": str(e)}), 500


# ---------------------------------------------------------
# ADMIN: VIEW ALL ORDERS
# ---------------------------------------------------------
@order_bp.route("/admin/orders", methods=["GET"])
@token_required
@admin_required
def get_all_orders(decoded):
    try:
        cur = mysql.connection.cursor()
        cur.execute("""
            SELECT orders.id, users.email, orders.total_amount, orders.status, orders.created_at
            FROM orders
            JOIN users ON users.id = orders.user_id
            ORDER BY orders.created_at DESC
        """)
        rows = cur.fetchall()

        orders = []
        for row in rows:
            orders.append({
                "order_id": row[0],
                "user_email": row[1],
                "total_amount": float(row[2]),
                "status": row[3],
                "created_at": row[4]
            })

        return jsonify(orders), 200

    except Exception as e:
        return jsonify({"error": str(e)}), 500
