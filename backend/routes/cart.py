from flask import Blueprint, request, jsonify
from app.extensions import mysql
from ..utils.decorators  import token_required

cart_bp = Blueprint("cart_bp", __name__)

# ---------------------------------------------------
# 1️⃣ GET USER CART
# ---------------------------------------------------
@cart_bp.route("/cart", methods=["GET"])
@token_required
def get_cart(decoded):

    user_id = decoded["user_id"]
    cur = mysql.connection.cursor()

    # Get cart id
    cur.execute("SELECT id FROM cart WHERE user_id=%s", (user_id,))
    cart = cur.fetchone()

    if not cart:
        return jsonify({
            "items": [],
            "total_items": 0,
            "subtotal": 0
        })

    cart_id = cart[0]

    cur.execute("""
        SELECT products.id, products.name, products.price,
               products.image_url, cart_items.quantity
        FROM cart_items
        JOIN products ON cart_items.product_id = products.id
        WHERE cart_items.cart_id=%s
    """, (cart_id,))

    items = []
    total_items = 0
    subtotal = 0

    for row in cur.fetchall():
        product_id, name, price, image_url, quantity = row

        total_items += quantity
        subtotal += float(price) * quantity

        items.append({
            "product_id": product_id,
            "name": name,
            "price": float(price),
            "image_url": image_url,
            "quantity": quantity
        })

    return jsonify({
        "items": items,
        "total_items": total_items,
        "subtotal": subtotal
    })


# ---------------------------------------------------
# 2️⃣ ADD TO CART
# ---------------------------------------------------
@cart_bp.route("/cart/add", methods=["POST"])
@token_required
def add_to_cart(decoded):

    user_id = decoded["user_id"]
    data = request.json
    product_id = data.get("product_id")
    quantity = data.get("quantity", 1)

    cur = mysql.connection.cursor()

    # Check product exists
    cur.execute("SELECT stock FROM products WHERE id=%s", (product_id,))
    product = cur.fetchone()

    if not product:
        return jsonify({"error":"Product not found"}), 404

    if product[0] < quantity:
        return jsonify({"error":"Not enough stock"}), 400

    # Get or create cart
    cur.execute("SELECT id FROM cart WHERE user_id=%s", (user_id,))
    cart = cur.fetchone()

    if not cart:
        cur.execute("INSERT INTO cart(user_id) VALUES(%s)", (user_id,))
        mysql.connection.commit()
        cart_id = cur.lastrowid
    else:
        cart_id = cart[0]

    # Check if item already exists
    cur.execute("""
        SELECT id, quantity FROM cart_items
        WHERE cart_id=%s AND product_id=%s
    """, (cart_id, product_id))

    item = cur.fetchone()

    if item:
        new_quantity = item[1] + quantity
        cur.execute("""
            UPDATE cart_items
            SET quantity=%s
            WHERE id=%s
        """, (new_quantity, item[0]))
    else:
        cur.execute("""
            INSERT INTO cart_items(cart_id,product_id,quantity)
            VALUES(%s,%s,%s)
        """, (cart_id, product_id, quantity))

    mysql.connection.commit()

    return jsonify({"message":"Added to cart"}), 201


# ---------------------------------------------------
# 3️⃣ UPDATE CART ITEM
# ---------------------------------------------------
@cart_bp.route("/cart/update", methods=["PUT"])
@token_required
def update_cart(decoded):

    user_id = decoded["user_id"]
    data = request.json
    product_id = data.get("product_id")
    quantity = data.get("quantity")

    if quantity <= 0:
        return jsonify({"error":"Quantity must be greater than 0"}), 400

    cur = mysql.connection.cursor()

    cur.execute("SELECT id FROM cart WHERE user_id=%s", (user_id,))
    cart = cur.fetchone()

    if not cart:
        return jsonify({"error":"Cart not found"}), 404

    cart_id = cart[0]

    cur.execute("""
        UPDATE cart_items
        SET quantity=%s
        WHERE cart_id=%s AND product_id=%s
    """, (quantity, cart_id, product_id))

    mysql.connection.commit()

    return jsonify({"message":"Cart updated"})


# ---------------------------------------------------
# 4️⃣ REMOVE ITEM
# ---------------------------------------------------
@cart_bp.route("/cart/remove", methods=["DELETE"])
@token_required
def remove_item(decoded):

    user_id = decoded["user_id"]
    data = request.json
    product_id = data.get("product_id")

    cur = mysql.connection.cursor()

    cur.execute("SELECT id FROM cart WHERE user_id=%s", (user_id,))
    cart = cur.fetchone()

    if not cart:
        return jsonify({"error":"Cart not found"}), 404

    cart_id = cart[0]

    cur.execute("""
        DELETE FROM cart_items
        WHERE cart_id=%s AND product_id=%s
    """, (cart_id, product_id))

    mysql.connection.commit()

    return jsonify({"message":"Item removed"})
