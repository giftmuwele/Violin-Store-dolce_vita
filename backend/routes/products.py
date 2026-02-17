from flask import Blueprint, request, jsonify
from app.extensions import mysql
from ..utils.decorators import token_required, admin_required
import datetime

product_bp = Blueprint("products", __name__)


# ----------------------------------------------------
# GET ALL PRODUCTS (Public)
# ----------------------------------------------------
@product_bp.route("/products", methods=["GET"])
def get_products():
    try:
        cur = mysql.connection.cursor()
        cur.execute("SELECT * FROM products ORDER BY date_added DESC")
        rows = cur.fetchall()

        products = []
        for row in rows:
            products.append({
                "id": row[0],
                "name": row[1],
                "category": row[2],
                "price": float(row[3]),
                "description": row[4],
                "stock_quantity": row[5],
                "image_url": row[6],
                "date_added": row[7]
            })

        return jsonify(products), 200

    except Exception as e:
        return jsonify({"error": str(e)}), 500


# ----------------------------------------------------
# ADD PRODUCT (Admin Only)
# ----------------------------------------------------
@product_bp.route("/products", methods=["POST"])
@token_required
@admin_required
def add_product(decoded):
    try:
        data = request.get_json()

        name = data.get("name")
        category = data.get("category")
        price = data.get("price")
        description = data.get("description")
        stock_quantity = data.get("stock")
        image_url = data.get("image_url")

        if not name or not price:
            return jsonify({"error": "Name and price required"}), 400

        cur = mysql.connection.cursor()
        cur.execute("""
            INSERT INTO products 
            (name, category, price, description, stock_quantity, image_url, date_added)
            VALUES (%s,%s,%s,%s,%s,%s,%s)
        """, (
            name,
            category,
            price,
            description,
            stock_quantity,
            image_url,
            datetime.datetime.now()
        ))

        mysql.connection.commit()

        return jsonify({"message": "Product added successfully"}), 201

    except Exception as e:
        return jsonify({"error": str(e)}), 500


# ----------------------------------------------------
# UPDATE PRODUCT (Admin Only)
# ----------------------------------------------------
@product_bp.route("/products/<int:id>", methods=["PUT"])
@token_required
@admin_required
def update_product(decoded, id):
    try:
        data = request.get_json()

        cur = mysql.connection.cursor()
        cur.execute("""
            UPDATE products
            SET name=%s,
                category=%s,
                price=%s,
                description=%s,
                stock_quantity=%s,
                image_url=%s
            WHERE id=%s
        """, (
            data.get("name"),
            data.get("category"),
            data.get("price"),
            data.get("description"),
            data.get("stock"),
            data.get("image_url"),
            id
        ))

        mysql.connection.commit()

        return jsonify({"message": "Product updated successfully"}), 200

    except Exception as e:
        return jsonify({"error": str(e)}), 500


# ----------------------------------------------------
# DELETE PRODUCT (Admin Only)
# ----------------------------------------------------
@product_bp.route("/products/<int:id>", methods=["DELETE"])
@token_required
@admin_required
def delete_product(decoded, id):
    try:
        cur = mysql.connection.cursor()
        cur.execute("DELETE FROM products WHERE id=%s", (id,))
        mysql.connection.commit()

        return jsonify({"message": "Product deleted successfully"}), 200

    except Exception as e:
        return jsonify({"error": str(e)}), 500
