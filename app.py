import re


from flask import Flask, request, redirect, session, render_template
import mysql.connector
import os
from werkzeug.utils import secure_filename

app = Flask(__name__)
app.secret_key = os.getenv("SECRET_KEY", "inventory_secret_key")

db = mysql.connector.connect(
    host=os.getenv("DB_HOST", "localhost"),
    user=os.getenv("DB_USER", "root"),
    password=os.getenv("DB_PASSWORD", " "),
    database=os.getenv("DB_NAME", "inventory_db"),
    port=int(os.getenv("DB_PORT", "3306"))
)
    

@app.route("/search")
def search():

    name = request.args.get("name", "")

    cursor = db.cursor()
    cursor.execute(
        "SELECT * FROM products WHERE name LIKE %s",
        ("%" + name + "%",)
    )

    products = cursor.fetchall()
    cursor.close()

    html = """
    <head>
          <link rel="stylesheet" href="/static/style.css">
    </head>
    <h1>Search Products</h1>

    <form method="GET">
        <input name="name" placeholder="Search product">
        <button type="submit">Search</button>
    </form>

    <br>

    <a href="/products">View All Products</a>

    <br><br>

    <table border="1" cellpadding="10">
        <tr>
            <th>ID</th>
            <th>Name</th>
            <th>Price</th>
            <th>Quantity</th>
            <th>Category</th>
        </tr>
    """

    for product in products:
        html += f"""
        <tr>
            <td>{product[0]}</td>
            <td>{product[1]}</td>
            <td>₹{product[2]}</td>
            <td>{product[3]}</td>
            <td>{product[4]}</td>
        </tr>
        """
    html += "</table>"

    return html


@app.route("/")
def welcome():
    return render_template("welcome.html")


@app.route("/add", methods=["POST"])
def add_product():

    if "admin" not in session:
        return redirect("/login")

    name = request.form["name"]
    price = request.form["price"]
    quantity = request.form["quantity"]
    category = request.form["category"]
    supplier_id = request.form.get("supplier_id") or None

    # Get image
    image = request.files.get("image")

    filename = None

    if image and image.filename:

        # Get original extension
        extension = os.path.splitext(image.filename)[1]

        # Make filename from product name
        filename = secure_filename(name) + extension

        # Save image inside static/product_images
        image_path = os.path.join(
            app.static_folder,
            "product_images",
            filename
        )

        image.save(image_path)


    cursor = db.cursor()

    cursor.execute("""
        INSERT INTO products
        (name, price, quantity, category, supplier_id)
        VALUES (%s, %s, %s, %s, %s)
    """, (name, price, quantity, category, supplier_id))

    db.commit()
    cursor.close()

    return redirect("/products")

@app.route("/add-product")
def add_product_page():

    if "admin" not in session:
        return redirect("/login")

    cursor = db.cursor()

    cursor.execute("SELECT * FROM categories")
    categories = cursor.fetchall()

    cursor.execute("SELECT * FROM suppliers")
    suppliers = cursor.fetchall()

    cursor.close()

    return render_template(
        "add_product.html",
        categories=categories,
        suppliers=suppliers
    )

@app.route("/products")
def products():

    if "admin" not in session:
        return redirect("/login")

    cursor = db.cursor()
    
    cursor.execute("""
        SELECT 
            products.id,
            products.name,
            products.category,
            suppliers.name,
            products.price,
            products.quantity
        FROM products
        LEFT JOIN suppliers
            ON products.supplier_id = suppliers.id
    """)

    products = cursor.fetchall()
    cursor.close()

    return render_template(
        "products.html",
        products=products
    )

@app.route("/delete/<int:id>")
def delete_product(id):

    if "admin" not in session:
        return redirect("/login")

    cursor = db.cursor()

    cursor.execute(
        "DELETE FROM sales WHERE product_id = %s",
        (id,)
    )

    cursor.execute(
        "DELETE FROM purchases WHERE product_id = %s",
        (id,)
    )

    cursor.execute(
        "DELETE FROM products WHERE id = %s",
        (id,)
    )

    db.commit()
    cursor.close()

    return redirect("/products")


@app.route("/edit/<int:id>", methods=["GET", "POST"])
def edit_product(id):

    if "admin" not in session:
        return redirect("/login")

    cursor = db.cursor()
    cursor.execute("SELECT * FROM categories")
    categories = cursor.fetchall()

    if request.method == "POST":

        name = request.form["name"]
        price = request.form["price"]
        quantity = request.form["quantity"]
        category = request.form["category"]

        cursor.execute("""
            UPDATE products
            SET name=%s, price=%s, quantity=%s, category=%s
            WHERE id=%s
        """, (name, price, quantity, category, id))

        db.commit()
        cursor.close()

        return redirect("/products")

    cursor.execute(
        "SELECT * FROM products WHERE id=%s",
        (id,)
    )

    product = cursor.fetchone()
    cursor.close()

    return render_template(
        "edit_product.html",
        product=product,
        categories=categories
    )



    

@app.route("/login", methods=["GET", "POST"])
def login():

    if request.method == "POST":

        username = request.form.get("username", "").strip()
        password = request.form.get("password", "")
        login_type = request.form.get("login_type", "")

        cursor = db.cursor()


        # =========================
        # ADMIN LOGIN
        # =========================

        if login_type == "admin":

            cursor.execute(
                """
                SELECT id, username
                FROM admins
                WHERE username = %s
                AND password = %s
                """,
                (username, password)
            )

            admin = cursor.fetchone()

            cursor.close()

            if admin:

                session.clear()

                session["admin"] = admin[1]

                return redirect("/dashboard")

            return render_template(
                "login.html",
                error="Invalid admin username or password"
            )


        # =========================
        # USER LOGIN
        # =========================

        elif login_type == "user":

            cursor.execute(
                """
                SELECT id, username
                FROM users
                WHERE username = %s
                AND password = %s
                """,
                (username, password)
            )

            user = cursor.fetchone()

            cursor.close()

            if user:

                session.clear()

                session["user"] = user[1]
                session["user_id"] = user[0]

                return redirect("/user-dashboard")

            return render_template(
                "login.html",
                error="Invalid user username or password"
            )


        # =========================
        # INVALID LOGIN TYPE
        # =========================

        cursor.close()

        return render_template(
            "login.html",
            error="Please choose Admin Login or User Login"
        )


    login_type = request.args.get("type", "")

    return render_template(
        "login.html",
        login_type=login_type
    )

@app.route("/logout")
def logout():
    session.clear()
    return redirect("/login")

@app.route("/dashboard")
def dashboard():

    if "admin" not in session:
        return redirect("/login")

    cursor = db.cursor()

    cursor.execute("SELECT COUNT(*) FROM products")
    total_products = cursor.fetchone()[0]

    cursor.execute("SELECT COALESCE(SUM(total_amount), 0) FROM sales")
    total_sales = cursor.fetchone()[0]

    cursor.execute("SELECT COUNT(*) FROM products WHERE quantity <= 5")
    low_stock = cursor.fetchone()[0]

    cursor.execute("SELECT COUNT(*) FROM products WHERE quantity = 0")
    out_of_stock = cursor.fetchone()[0]

    cursor.execute("""
        SELECT
            sales.customer_name,
            products.name,
            sales.quantity,
            sales.total_amount,
            sales.sale_date
        FROM sales
        JOIN products
            ON sales.product_id = products.id
        ORDER BY sales.sale_date DESC
        LIMIT 5
    """)

    recent_sales = cursor.fetchall()

    cursor.execute("""
        SELECT name, category, quantity
        FROM products
        WHERE quantity > 0 AND quantity <= 5
        ORDER BY quantity ASC
    """)

    low_stock_products = cursor.fetchall()

        # Get unread admin notifications
    cursor.execute("""
        SELECT id, message, created_at
        FROM admin_notifications
        WHERE is_read = 0
        ORDER BY created_at DESC
    """)
    admin_notifications = cursor.fetchall()

    cursor.close()

    return render_template(
    "dashboard.html",
    total_products=total_products,
    low_stock=low_stock,
    out_of_stock=out_of_stock,
    total_sales=total_sales,
    recent_sales=recent_sales,
    low_stock_products=low_stock_products,
    admin_notifications=admin_notifications
)



@app.route("/sales", methods=["GET", "POST"])
def sales():

    if "admin" not in session:
        return redirect("/login")

    cursor = db.cursor()

    if request.method == "POST":

        customer_name = request.form["customer_name"]
        product_id = request.form["product_id"]
        quantity = int(request.form["quantity"])

        if quantity <= 0:
            cursor.close()
            return "Quantity must be greater than 0"

        cursor.execute(
            "SELECT price, quantity FROM products WHERE id=%s",
            (product_id,)
        )

        product = cursor.fetchone()

        if not product:
            cursor.close()
            return "Product not found"

        price = float(product[0])
        stock = product[1]

        if quantity > stock:
            cursor.close()
            return "Not enough stock"

        total_amount = price * quantity

        cursor.execute(
            """
            INSERT INTO sales
            (customer_name, product_id, quantity, total_amount)
            VALUES (%s, %s, %s, %s)
            """,
            (customer_name, product_id, quantity, total_amount)
        )

        cursor.execute(
            """
            UPDATE products
            SET quantity = quantity - %s
            WHERE id = %s
            """,
            (quantity, product_id)
        )

        db.commit()

    # Sales summary
    cursor.execute("SELECT COALESCE(SUM(total_amount), 0) FROM sales")
    sales_total = cursor.fetchone()[0]

    cursor.execute("SELECT COALESCE(SUM(quantity), 0) FROM sales")
    items_sold = cursor.fetchone()[0]

    cursor.execute("SELECT COUNT(*) FROM sales")
    sales_count = cursor.fetchone()[0]

    # Sales history
    cursor.execute("""
        SELECT
            sales.id,
            sales.customer_name,
            products.name,
            sales.quantity,
            sales.total_amount,
            sales.sale_date
        FROM sales
        JOIN products
            ON sales.product_id = products.id
        ORDER BY sales.sale_date DESC
    """)

    sales_data = cursor.fetchall()

    # Available products
    cursor.execute(
        "SELECT * FROM products WHERE quantity > 0"
    )
    products = cursor.fetchall()

    cursor.close()

    return render_template(
        "sales.html",
        sales=sales_data,
        products=products,
        sales_total=sales_total,
        items_sold=items_sold,
        sales_count=sales_count
    )

@app.route("/product/<int:id>")
def product_details(id):

    if "admin" not in session:
        return redirect("/login")

    cursor = db.cursor()

    cursor.execute(
        "SELECT * FROM products WHERE id=%s",
        (id,)
    )

    product = cursor.fetchone()

    if not product:
        cursor.close()
        return "Product not found"

    cursor.execute(
        "SELECT COALESCE(SUM(quantity), 0) FROM sales WHERE product_id=%s",
        (id,)
    )

    total_sold = cursor.fetchone()[0]

    cursor.execute(
        "SELECT COALESCE(SUM(total_amount), 0) FROM sales WHERE product_id=%s",
        (id,)
    )

    total_sales = cursor.fetchone()[0]

    cursor.close()

    return render_template(
        "product_details.html",
        product=product,
        total_sold=total_sold,
        total_sales=total_sales
    )

@app.route("/suppliers", methods=["GET", "POST"])
def suppliers():

    if "admin" not in session:
        return redirect("/login")

    cursor = db.cursor()

    if request.method == "POST":

        name = request.form["name"]
        phone = request.form["phone"]
        email = request.form["email"]
        company = request.form["company"]

        cursor.execute(
            """
            INSERT INTO suppliers
            (name, phone, email, company)
            VALUES (%s, %s, %s, %s)
            """,
            (name, phone, email, company)
        )

        db.commit()

    cursor.execute(
        "SELECT * FROM suppliers ORDER BY id DESC"
    )

    suppliers_data = cursor.fetchall()

    cursor.close()

    return render_template(
        "suppliers.html",
        suppliers=suppliers_data
    )

@app.route("/invoice/<int:id>")
def invoice(id):

    if "admin" not in session:
        return redirect("/login")

    cursor = db.cursor()

    cursor.execute("""
        SELECT
            sales.id,
            sales.customer_name,
            products.name,
            sales.quantity,
            sales.total_amount,
            sales.sale_date
        FROM sales
        JOIN products
            ON sales.product_id = products.id
        WHERE sales.id = %s
    """, (id,))

    sale = cursor.fetchone()
    cursor.close()

    if not sale:
        return "Invoice not found"

    return render_template(
        "invoice.html",
        sale=sale
    )

@app.route("/user-invoice/<int:id>")
def user_invoice(id):

    if "user" not in session:
        return redirect("/login")

    cursor = db.cursor()

    cursor.execute("""
        SELECT
            u.id,
            u.username,
            p.name,
            u.quantity,
            u.price,
            u.total_amount,
            u.order_date
        FROM user_orders u
        JOIN products p
            ON u.product_id = p.id
        WHERE u.id = %s
          AND u.username = %s
    """, (id, session["user"]))

    order = cursor.fetchone()

    cursor.close()

    if not order:
        return "Invoice not found"

    return render_template(
        "user_invoice.html",
        order=order
    )

@app.route("/purchases", methods=["GET", "POST"])
def purchases():

    if "admin" not in session:
        return redirect("/login")

    cursor = db.cursor()

    if request.method == "POST":

        product_id = request.form["product_id"]
        supplier_id = request.form.get("supplier_id") or None
        quantity = int(request.form["quantity"])
        purchase_price = float(request.form["purchase_price"])

        # Calculate total purchase amount
        total_amount = quantity * purchase_price

        # Check product exists
        cursor.execute(
            "SELECT id FROM products WHERE id=%s",
            (product_id,)
        )

        product = cursor.fetchone()

        if not product:
            cursor.close()
            return "Product not found"

        # Insert purchase record
        cursor.execute(
            """
            INSERT INTO purchases
            (product_id, supplier_id, quantity, purchase_price, total_amount)
            VALUES (%s, %s, %s, %s, %s)
            """,
            (
                product_id,
                supplier_id,
                quantity,
                purchase_price,
                total_amount
            )
        )

        # Increase product stock
        cursor.execute(
            """
            UPDATE products
            SET quantity = quantity + %s
            WHERE id = %s
            """,
            (quantity, product_id)
        )

        db.commit()

        cursor.close()

        return redirect("/purchases")

    # Get products
    cursor.execute(
        "SELECT * FROM products ORDER BY name"
    )
    products = cursor.fetchall()

    # Get suppliers
    cursor.execute(
        "SELECT * FROM suppliers ORDER BY name"
    )
    suppliers = cursor.fetchall()

    # Purchase summary
    cursor.execute(
        "SELECT COALESCE(SUM(total_amount), 0) FROM purchases"
    )
    purchase_total = cursor.fetchone()[0]

    cursor.execute(
        "SELECT COALESCE(SUM(quantity), 0) FROM purchases"
    )
    items_purchased = cursor.fetchone()[0]

    cursor.execute(
        "SELECT COUNT(*) FROM purchases"
    )
    purchase_count = cursor.fetchone()[0]

    # Purchase history
    cursor.execute(
        "SELECT * FROM purchases ORDER BY purchase_date DESC"
    )
    purchase_data = cursor.fetchall()

    cursor.close()

    return render_template(
        "purchases.html",
        products=products,
        suppliers=suppliers,
        purchases=purchase_data,
        purchase_total=purchase_total,
        items_purchased=items_purchased,
        purchase_count=purchase_count
    )

@app.route("/reports")
def reports():

    if "admin" not in session:
        return redirect("/login")

    period = request.args.get("period", "all")


    cursor = db.cursor()

    if period == "today":

        date_condition = "DATE(sale_date) = CURDATE()"
        purchase_date_condition = "DATE(purchase_date) = CURDATE()"

    elif period == "month":

         date_condition = """
             YEAR(sale_date) = YEAR(CURDATE())
             AND MONTH(sale_date) = MONTH(CURDATE())
         """

         purchase_date_condition = """
             YEAR(purchase_date) = YEAR(CURDATE())
             AND MONTH(purchase_date) = MONTH(CURDATE())
         """

    else:

        date_condition = "1=1"
        purchase_date_condition = "1=1"


    # Total sales
    cursor.execute(
        f"""
        SELECT COALESCE(SUM(total_amount), 0)
        FROM sales
        WHERE {date_condition}
        """
    )
    total_sales = cursor.fetchone()[0]


    # Total purchases
    cursor.execute(
        f"""
        SELECT COALESCE(SUM(total_amount), 0)
        FROM purchases
        WHERE {purchase_date_condition}
        """
    )
    total_purchases = cursor.fetchone()[0]


    # Items sold
    cursor.execute(
        f"""
        SELECT COALESCE(SUM(quantity), 0)
        FROM sales
        WHERE {date_condition}
        """
    )
    items_sold = cursor.fetchone()[0]


    # Items purchased
    cursor.execute(
        f"""
        SELECT COALESCE(SUM(quantity), 0)
        FROM purchases
        WHERE {purchase_date_condition}
        """
    )
    items_purchased = cursor.fetchone()[0]
    
    
    # Simple profit calculation
    profit = float(total_sales) - float(total_purchases)

    cursor.execute(f"""
        SELECT
            p.name,
            COALESCE(s.sold_quantity, 0) AS sold_quantity,
            COALESCE(s.revenue, 0) AS revenue,
            COALESCE(s.sold_quantity * (
                SELECT SUM(pu.quantity * pu.purchase_price) / NULLIF(SUM(pu.quantity), 0) FROM purchases pu WHERE pu.product_id = p.id AND {purchase_date_condition}), 0) AS purchase_cost,
            COALESCE(s.revenue, 0) - COALESCE(s.sold_quantity * ( SELECT SUM(pu.quantity * pu.purchase_price) / NULLIF(SUM(pu.quantity), 0) FROM purchases pu WHERE pu.product_id = p.id AND {purchase_date_condition}), 0) AS profit
        FROM products p
        
        LEFT JOIN (
            SELECT
                product_id,
                SUM(quantity) AS sold_quantity,
                SUM(total_amount) AS revenue
            FROM sales
            WHERE {date_condition}
            GROUP BY product_id
        ) s
            ON p.id = s.product_id

        

        ORDER BY p.name
    """)

    product_profits = cursor.fetchall()

    cursor.close()

    return render_template(
        "reports.html",
        total_sales=total_sales,
        total_purchases=total_purchases,
        profit=profit,
        items_sold=items_sold,
        items_purchased=items_purchased,
        product_profits=product_profits
    )

@app.route("/user-dashboard")
def user_dashboard():

    if "user" not in session:
        return redirect("/login")

    cursor = db.cursor()

    cursor.execute("""
        SELECT name, category, price, quantity
        FROM products
        ORDER BY name
    """)

    products = cursor.fetchall()

    cursor.execute("""
        SELECT COUNT(*)
        FROM products
    """)

    total_products = cursor.fetchone()[0]

    cursor.execute("""
        SELECT COUNT(*)
        FROM products
        WHERE quantity > 0
    """)

    in_stock = cursor.fetchone()[0]

    cursor.close()

    return render_template(
        "user_dashboard.html",
        username=session["user"],
        products=products,
        total_products=total_products,
        in_stock=in_stock
    )

@app.route("/user-products")
def user_products():

    if "user" not in session:
        return redirect("/login")

    cursor = db.cursor()

    cursor.execute("""
        SELECT id, name, category, price, quantity, image
        FROM products
        ORDER BY name
    """)

    products = cursor.fetchall()

    print("PRODUCTS DATA:", products)

    cursor.close()

    return render_template(
        "user_products.html",
        products=products
    )

@app.route("/user-product/<int:id>")
def user_product_details(id):

    if "user" not in session:
        return redirect("/login")

    cursor = db.cursor()

    # =========================================
    # GET PRODUCT
    # =========================================

    cursor.execute("""
        SELECT id, name, category, price, quantity, image
        FROM products
        WHERE id = %s
    """, (id,))

    product = cursor.fetchone()

    if not product:
        cursor.close()
        return "Product not found"


    # =========================================
    # CHECK WISHLIST
    # =========================================

    cursor.execute("""
        SELECT id
        FROM wishlist
        WHERE user_id = %s
        AND product_id = %s
    """, (
        session["user_id"],
        id
    ))

    wishlist_item = cursor.fetchone()

    in_wishlist = wishlist_item is not None


    # =========================================
    # GET REVIEWS
    # =========================================

    cursor.execute("""
        SELECT
            r.id,
            r.rating,
            r.review_text,
            r.created_at,
            u.username
        FROM product_reviews r
        JOIN users u
            ON r.user_id = u.id
        WHERE r.product_id = %s
        ORDER BY r.created_at DESC
    """, (id,))

    reviews = cursor.fetchall()


    # =========================================
    # CHECK VERIFIED PURCHASE FOR EACH REVIEW
    # =========================================

    verified_reviews = []

    for review in reviews:

        cursor.execute("""
            SELECT id
            FROM user_orders
            WHERE username = %s
            AND product_id = %s
            LIMIT 1
        """, (
            review[4],
            id
        ))

        purchase = cursor.fetchone()

        if purchase:
            verified_purchase_for_review = 1
        else:
            verified_purchase_for_review = 0

        verified_reviews.append(
            (
                review[0],
                review[1],
                review[2],
                review[3],
                review[4],
                verified_purchase_for_review
            )
        )

    reviews = verified_reviews

    # ========================================= 
    # GET HELPFUL COUNT FOR EACH REVIEW
    # =========================================

    reviews_with_helpful = []

    for review in reviews:


        cursor.execute("""
            SELECT COUNT(*)
            FROM review_helpful
            WHERE review_id = %s
        """, (review[0],))

        helpful_data = cursor.fetchone()

        helpful_count = helpful_data[0] if helpful_data else 0


        reviews_with_helpful.append(
            (
                review[0],
                review[1],
                review[2],
                review[3],
                review[4],
                review[5],
                helpful_count
            )
        )

    reviews = reviews_with_helpful

    # =========================================
    # GET AVERAGE RATING
    # =========================================

    cursor.execute("""
        SELECT
            AVG(rating),
            COUNT(*)
        FROM product_reviews
        WHERE product_id = %s
    """, (id,))

    rating_data = cursor.fetchone()

    average_rating = rating_data[0] if rating_data[0] else 0
    review_count = rating_data[1]

    # =========================================
    # RATING DISTRIBUTION
    # =========================================

    cursor.execute("""
        SELECT
            rating,
            COUNT(*)
        FROM product_reviews
        WHERE product_id = %s
        GROUP BY rating
        ORDER BY rating DESC
    """, (id,))

    rating_rows = cursor.fetchall()


    rating_distribution = {
        5: 0,
        4: 0,
        3: 0,
        2: 0,
        1: 0
    }

    for row in rating_rows:

        rating_distribution[row[0]] = row[1]

    
    # =========================================
    # RATING PERCENTAGES
    # =========================================

    rating_percentages = {}


    for rating in range(5, 0, -1):

        if review_count > 0:

            rating_percentages[rating] = round(
                (
                    rating_distribution[rating]
                    / review_count
                ) * 100
            )

        else:

            rating_percentages[rating] = 0



    # =========================================
    # CHECK CURRENT USER REVIEW
    # =========================================

    cursor.execute("""
        SELECT
            id,
            rating,
            review_text
        FROM product_reviews
        WHERE user_id = %s
        AND product_id = %s
    """, (
        session["user_id"],
        id
    ))

    user_review = cursor.fetchone()

    # =========================================
    # CHECK VERIFIED PURCHASE
    # =========================================

    cursor.execute("""
        SELECT id
        FROM user_orders
        WHERE username = %s
        AND product_id = %s
        LIMIT 1
    """, (
        session["user"],
        id
    ))

    purchase = cursor.fetchone()

    verified_purchase = purchase is not None


    cursor.close()


    return render_template(
        "user_product_details.html",
        product=product,
        in_wishlist=in_wishlist,
        reviews=reviews,
        average_rating=average_rating,
        review_count=review_count,
        user_review=user_review,
        verified_purchase=verified_purchase,
        rating_distribution=rating_distribution,
        rating_percentages=rating_percentages
    )

@app.route("/toggle-wishlist/<int:id>", methods=["POST"])
def toggle_wishlist(id):

    if "user" not in session:
        return redirect("/login")

    cursor = db.cursor()

    # Check if product exists
    cursor.execute(
        "SELECT id FROM products WHERE id = %s",
        (id,)
    )

    product = cursor.fetchone()

    if not product:
        cursor.close()
        return "Product not found"

    # Check if product is already in wishlist
    cursor.execute(
        """
        SELECT id
        FROM wishlist
        WHERE user_id = %s
        AND product_id = %s
        """,
        (session["user_id"], id)
    )

    wishlist_item = cursor.fetchone()

    if wishlist_item:

        # Remove from wishlist
        cursor.execute(
            """
            DELETE FROM wishlist
            WHERE user_id = %s
            AND product_id = %s
            """,
            (session["user_id"], id)
        )

    else:

        # Add to wishlist
        cursor.execute(
            """
            INSERT INTO wishlist
            (user_id, product_id)
            VALUES (%s, %s)
            """,
            (session["user_id"], id)
        )

    db.commit()

    cursor.close()

    return redirect("/user-product/{}".format(id))

@app.route("/wishlist")
def wishlist():

    if "user" not in session:
        return redirect("/login")

    cursor = db.cursor()

    cursor.execute("""
        SELECT
            w.id,
            p.id,
            p.name,
            p.category,
            p.price,
            p.quantity,
            p.image
        FROM wishlist w
        JOIN products p
            ON w.product_id = p.id
        WHERE w.user_id = %s
        ORDER BY w.created_at DESC
    """, (session["user_id"],))

    wishlist_items = cursor.fetchall()

    cursor.close()

    return render_template(
        "wishlist.html",
        wishlist_items=wishlist_items
    )

@app.route("/add-review/<int:id>", methods=["POST"])
def add_review(id):

    if "user" not in session:
        return redirect("/login")

    rating = request.form.get("rating")
    review_text = request.form.get("review_text", "").strip()

    # Validate rating
    try:
        rating = int(rating)
    except (TypeError, ValueError):
        return "Invalid rating"

    if rating < 1 or rating > 5:
        return "Rating must be between 1 and 5"

    # Validate review text
    if not review_text:
        return redirect("/user-product/{}".format(id))

    if len(review_text) > 500:
        return "Review must be 500 characters or less"

    cursor = db.cursor()

    # Check product exists
    cursor.execute(
        """
        SELECT id
        FROM products
        WHERE id = %s
        """,
        (id,)
    )

    product = cursor.fetchone()

    if not product:
        cursor.close()
        return "Product not found"

    # =========================================
    # VERIFIED PURCHASE CHECK
    # =========================================

    cursor.execute(
        """
        SELECT id
        FROM user_orders
        WHERE username = %s
        AND product_id = %s
        LIMIT 1
        """,
        (
            session["user"],
            id
        )
    )

    purchase = cursor.fetchone()

    if not purchase:
        cursor.close()
        return redirect("/user-product/{}".format(id))

    # =========================================
    # CHECK EXISTING REVIEW
    # =========================================

    cursor.execute(
        """
        SELECT id
        FROM product_reviews
        WHERE user_id = %s
        AND product_id = %s
        """,
        (
            session["user_id"],
            id
        )
    )

    existing_review = cursor.fetchone()

    if existing_review:
        cursor.close()
        return redirect("/user-product/{}".format(id))
        
    
    # =========================================
    # SAVE REVIEW
    # =========================================

    cursor.execute(
        """
        INSERT INTO product_reviews
        (
            user_id,
            product_id,
            rating,
            review_text
        )
        VALUES (%s, %s, %s, %s)
        """,
        (
            session["user_id"],
            id,
            rating,
            review_text
        )
    )

    db.commit()

    cursor.close()

    return redirect("/user-product/{}".format(id))


@app.route("/review/<int:review_id>/helpful", methods=["POST"])
def mark_review_helpful(review_id):

    if "user" not in session:
        return redirect("/login")

    cursor = db.cursor()

    # Check whether this user already marked this review helpful
    cursor.execute("""
        SELECT id
        FROM review_helpful
        WHERE review_id = %s
        AND user_id = %s
    """, (
        review_id,
        session["user_id"]
    ))

    existing_vote = cursor.fetchone()

    if existing_vote:

        cursor.close()

        return redirect(request.referrer or "/user-products")


    # Add helpful vote
    cursor.execute("""
        INSERT INTO review_helpful
        (review_id, user_id)
        VALUES (%s, %s)
    """, (
        review_id,
        session["user_id"]
    ))

    db.commit()

    cursor.close()

    return redirect(request.referrer or "/user-products")
        

@app.route("/buy/<int:id>", methods=["POST"])
def buy_product(id):

    if "user" not in session:
        return redirect("/login")

    quantity = int(request.form["quantity"])

    cursor = db.cursor()

    # Get product
    cursor.execute(
        """
        SELECT id, name, price, quantity
        FROM products
        WHERE id=%s
        """,
        (id,)
    )

    product = cursor.fetchone()

    if not product:
        cursor.close()
        return "Product not found"

    product_id = product[0]
    name = product[1]
    price = float(product[2])
    stock = product[3]

    # Check stock
    if quantity < 1:
        cursor.close()
        return "Invalid quantity"

    if quantity > stock:
        cursor.close()
        return "Not enough stock"

    total_amount = price * quantity

    cursor.close()

    # DO NOT create the order here.
    # Send the user to checkout first.

    return render_template(
        "checkout.html",
        product_id=product_id,
        product_name=name,
        quantity=quantity,
        price=price,
        total_amount=total_amount
    )


@app.route("/place-order", methods=["POST"])
def place_order():

    if "user" not in session:
        return redirect("/login")

    product_id = int(request.form["product_id"])
    quantity = int(request.form["quantity"])

    customer_name = request.form["customer_name"].strip()
    address1 = request.form["address1"].strip()
    address2 = request.form.get("address2", "").strip()
    city = request.form["city"].strip()
    state = request.form["state"].strip()
    country = request.form["country"].strip()
    pincode = request.form["pincode"].strip()
    landmark = request.form.get("landmark", "").strip()
    payment_method = request.form["payment_method"]

    # Basic validation

    if not customer_name:
        return "Name is required"

    if not address1:
        return "Address is required"

    if not city:
        return "City is required"

    if not state:
        return "State is required"

    if not country:
        return "Country is required"

    if not pincode.isdigit() or len(pincode) != 6:
        return "Invalid pincode"

    allowed_payments = [
        "Cash on Delivery",
        "UPI",
        "Debit Card",
        "Credit Card",
        "Net Banking"
    ]

    if payment_method not in allowed_payments:
        return "Invalid payment method"

    cursor = db.cursor()

    # Get latest product information
    cursor.execute(
        """
        SELECT name, price, quantity
        FROM products
        WHERE id=%s
        """,
        (product_id,)
    )

    product = cursor.fetchone()

    if not product:
        cursor.close()
        return "Product not found"

    product_name = product[0]
    price = float(product[1])
    stock = product[2]

    # Check stock again
    if quantity < 1:
        cursor.close()
        return "Invalid quantity"

    if quantity > stock:
        cursor.close()
        return "Not enough stock"

    total_amount = price * quantity

    # Reduce stock
    cursor.execute(
        """
        UPDATE products
        SET quantity = quantity - %s
        WHERE id = %s
        """,
        (quantity, product_id)
    )

    # Create order
    cursor.execute(
        """
        INSERT INTO user_orders
        (
            username,
            product_id,
            quantity,
            price,
            total_amount,
            status,
            customer_name,
            address1,
            address2,
            city,
            state,
            country,
            pincode,
            landmark,
            payment_method
        )
        VALUES
        (
            %s, %s, %s, %s, %s, %s,
            %s, %s, %s, %s, %s, %s,
            %s, %s, %s
        )
        """,
        (
            session["user"],
            product_id,
            quantity,
            price,
            total_amount,
            "Pending",
            customer_name,
            address1,
            address2,
            city,
            state,
            country,
            pincode,
            landmark,
            payment_method
        )
    )

    order_id = cursor.lastrowid

    db.commit()

    cursor.close()

    return render_template(
        "buy_success.html",
        order_id=order_id,
        product_name=product_name,
        quantity=quantity,
        price=price,
        total_amount=total_amount,
        customer_name=customer_name,
        address1=address1,
        address2=address2,
        pincode=pincode,
        landmark=landmark,
        payment_method=payment_method
    )

@app.route("/my-orders")
def my_orders():

    if "user" not in session:
        return redirect("/login")

    cursor = db.cursor()

    cursor.execute(
        """
        SELECT
            u.id,
            p.name,
            p.image,
            u.quantity,
            u.price,
            u.total_amount,
            u.order_date,
            u.status
        FROM user_orders u
        JOIN products p ON u.product_id = p.id
        WHERE u.username = %s
        ORDER BY u.order_date DESC
        """,
        (session["user"],)
    )

    orders = cursor.fetchall()

    cursor.execute(
        """
        SELECT COUNT(*)
        FROM user_orders
        WHERE username = %s
        """,
        (session["user"],)
    )

    total_orders = cursor.fetchone()[0]

    cursor.execute(
        """
        SELECT COALESCE(SUM(quantity), 0)
        FROM user_orders
        WHERE username = %s
        """,
        (session["user"],)
    )

    total_items = cursor.fetchone()[0]

    cursor.execute(
        """
        SELECT COALESCE(SUM(total_amount), 0)
        FROM user_orders
        WHERE username = %s
        """,
        (session["user"],)
    )

    total_spent = cursor.fetchone()[0]

    cursor.close()

    return render_template(
        "my_orders.html",
        orders=orders,
        total_orders=total_orders,
        total_items=total_items,
        total_spent=total_spent
    )

@app.route("/order/<int:id>")
def order_details(id):

    if "user" not in session:
        return redirect("/login")

    cursor = db.cursor()

    cursor.execute(
        """
        SELECT
            u.id,
            p.name,
            u.quantity,
            u.price,
            u.total_amount,
            u.order_date,
            u.username,
            u.status,
            u.customer_name,
            u.address1,
            u.address2,
            u.city,
            u.state,
            u.country,
            u.pincode,
            u.landmark,
            u.payment_method,
            p.image
        FROM user_orders u
        JOIN products p 
           ON u.product_id = p.id
        WHERE u.id = %s
        AND u.username = %s
        """,
        (id, session["user"])
    )

    order = cursor.fetchone()

    cursor.close()

    if not order:
        return "Order not found"

    return render_template(
        "order_details.html",
        order=order
    )

@app.route("/admin/update-order-status/<int:id>", methods=["POST"])
def update_order_status(id):

    if "admin" not in session:
        return redirect("/login")

    status = request.form["status"]

    allowed_statuses = [
        "Pending",
        "Confirmed",
        "Shipped",
        "Delivered"
    ]

    if status not in allowed_statuses:
        return "Invalid order status"

    cursor = db.cursor()

    # Get current order details
    cursor.execute(
        """
        SELECT
            product_id,
            quantity,
            total_amount,
            customer_name,
            status
        FROM user_orders
        WHERE id = %s
        """,
        (id,)
    )

    order = cursor.fetchone()

    if not order:
        cursor.close()
        return "Order not found"

    product_id = order[0]
    quantity = order[1]
    total_amount = order[2]
    customer_name = order[3]
    current_status = order[4]

    # Update order status
    cursor.execute(
        """
        UPDATE user_orders
        SET status = %s
        WHERE id = %s
        """,
        (status, id)
    )

    # Create a Sales record ONLY when order becomes Confirmed
    if status == "Confirmed" and current_status != "Confirmed":

        # Check whether this order already has a Sales record
        cursor.execute(
            """
            SELECT id
            FROM sales
            WHERE user_order_id = %s
            """,
            (id,)
        )

        existing_sale = cursor.fetchone()

        if not existing_sale:

            cursor.execute(
                """
                INSERT INTO sales
                (
                    product_id,
                    quantity,
                    total_amount,
                    customer_name,
                    user_order_id
                )
                VALUES
                (%s, %s, %s, %s, %s)
                """,
                (
                    product_id,
                    quantity,
                    total_amount,
                    customer_name,
                    id
                )
            )

    db.commit()

    cursor.close()

    return redirect("/admin/orders")

@app.route("/admin/orders")
def admin_orders():

    if "admin" not in session:
        return redirect("/login")

    cursor = db.cursor()

    cursor.execute(
        """
        SELECT
            u.id,
            u.username,
            p.name,
            u.quantity,
            u.price,
            u.total_amount,
            u.order_date,
            u.status
        FROM user_orders u
        JOIN products p ON u.product_id = p.id
        ORDER BY u.order_date DESC
        """
    )

    orders = cursor.fetchall()

    cursor.close()

    return render_template(
        "admin_orders.html",
        orders=orders
    )

@app.route("/register", methods=["GET", "POST"])
def register():

    if request.method == "POST":

        username = request.form["username"].strip()
        password = request.form["password"]
        confirm_password = request.form["confirm_password"]

        # Check username
        if not username:
            return "Username is required"

        # Check password confirmation
        if password != confirm_password:
            return "Passwords do not match"

        # Password must contain at least 8 characters
        if len(password) < 8:
            return "Password must contain at least 8 characters"

        # Password must contain uppercase letter
        if not re.search(r"[A-Z]", password):
            return "Password must contain at least one uppercase letter"

        # Password must contain lowercase letter
        if not re.search(r"[a-z]", password):
            return "Password must contain at least one lowercase letter"

        # Password must contain a number
        if not re.search(r"[0-9]", password):
            return "Password must contain at least one number"

        # Password must contain special character
        if not re.search(r"[^A-Za-z0-9]", password):
            return "Password must contain at least one special character"

        cursor = db.cursor()

        # Check if username already exists
        cursor.execute(
            "SELECT * FROM users WHERE username=%s",
            (username,)
        )

        existing_user = cursor.fetchone()

        if existing_user:
            cursor.close()
            return "Username already exists"

                # Create new user
        cursor.execute(
            """
            INSERT INTO users (username, password)
            VALUES (%s, %s)
            """,
            (username, password)
        )

        # Create notification for admin
        cursor.execute(
            """
            INSERT INTO admin_notifications (message)
            VALUES (%s)
            """,
            (f"New customer '{username}' has joined CartNexa.",)
        )

        db.commit()
        cursor.close()

        return redirect("/login")

    return render_template("register.html")

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)