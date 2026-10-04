from flask import Flask, render_template, request, redirect, url_for, flash
from oracle_connection import get_connection

app = Flask(__name__)
app.secret_key = "grocery_secret_key"


# =========================================================
# HOME
# =========================================================

@app.route("/")
def home():
    return render_template("index.html")


# =========================================================
# PRODUCT MANAGEMENT
# =========================================================

@app.route("/products")
def products():

    search = request.args.get("search", "").strip()
    category = request.args.get("category", "").strip()
    low_stock = request.args.get("low_stock", "")

    connection = get_connection()
    cursor = connection.cursor()

    query = """
        SELECT
            product_id,
            product_name,
            category,
            price,
            quantity
        FROM products
        WHERE 1 = 1
    """

    parameters = {}

    if search:
        query += """
            AND LOWER(product_name)
            LIKE LOWER(:search)
        """
        parameters["search"] = f"%{search}%"

    if category:
        query += """
            AND LOWER(category)
            = LOWER(:category)
        """
        parameters["category"] = category

    if low_stock:
        query += """
            AND quantity <= 10
        """

    query += " ORDER BY product_id"

    cursor.execute(query, parameters)

    products_data = cursor.fetchall()

    cursor.execute("""
        SELECT DISTINCT category
        FROM products
        ORDER BY category
    """)

    categories = [row[0] for row in cursor.fetchall()]

    cursor.close()
    connection.close()

    return render_template(
        "products.html",
        products=products_data,
        categories=categories,
        search=search,
        selected_category=category,
        low_stock=low_stock
    )


# =========================================================
# ADD PRODUCT
# =========================================================

@app.route("/products/add", methods=["GET", "POST"])
def add_product():

    if request.method == "POST":

        product_id = request.form["product_id"]
        product_name = request.form["product_name"]
        category = request.form["category"]
        price = request.form["price"]
        quantity = request.form["quantity"]

        connection = get_connection()
        cursor = connection.cursor()

        try:

            cursor.execute("""
                INSERT INTO products
                (
                    product_id,
                    product_name,
                    category,
                    price,
                    quantity
                )
                VALUES
                (
                    :1,
                    :2,
                    :3,
                    :4,
                    :5
                )
            """, (
                product_id,
                product_name,
                category,
                price,
                quantity
            ))

            connection.commit()

            flash(
                "Product added successfully!",
                "success"
            )

        except Exception as e:

            connection.rollback()

            flash(
                f"Error adding product: {e}",
                "error"
            )

        finally:

            cursor.close()
            connection.close()

        return redirect(url_for("products"))

    return render_template("add_product.html")


# =========================================================
# UPDATE PRODUCT
# =========================================================

@app.route(
    "/products/update/<int:product_id>",
    methods=["GET", "POST"]
)
def update_product(product_id):

    connection = get_connection()
    cursor = connection.cursor()

    if request.method == "POST":

        product_name = request.form["product_name"]
        category = request.form["category"]
        price = request.form["price"]
        quantity = request.form["quantity"]

        try:

            cursor.execute("""
                UPDATE products
                SET
                    product_name = :1,
                    category = :2,
                    price = :3,
                    quantity = :4
                WHERE product_id = :5
            """, (
                product_name,
                category,
                price,
                quantity,
                product_id
            ))

            connection.commit()

            flash(
                "Product updated successfully!",
                "success"
            )

        except Exception as e:

            connection.rollback()

            flash(
                f"Error updating product: {e}",
                "error"
            )

        finally:

            cursor.close()
            connection.close()

        return redirect(url_for("products"))

    cursor.execute("""
        SELECT
            product_id,
            product_name,
            category,
            price,
            quantity
        FROM products
        WHERE product_id = :1
    """, (product_id,))

    product_data = cursor.fetchone()

    cursor.close()
    connection.close()

    if product_data is None:

        flash(
            "Product not found!",
            "error"
        )

        return redirect(url_for("products"))

    return render_template(
        "update_product.html",
        product=product_data
    )


# =========================================================
# DELETE PRODUCT
# =========================================================

@app.route(
    "/products/delete/<int:product_id>",
    methods=["POST"]
)
def delete_product(product_id):

    connection = get_connection()
    cursor = connection.cursor()

    try:

        cursor.execute("""
            DELETE FROM products
            WHERE product_id = :1
        """, (product_id,))

        connection.commit()

        flash(
            "Product deleted successfully!",
            "success"
        )

    except Exception as e:

        connection.rollback()

        flash(
            f"Error deleting product: {e}",
            "error"
        )

    finally:

        cursor.close()
        connection.close()

    return redirect(url_for("products"))


# =========================================================
# CUSTOMER MANAGEMENT
# =========================================================

@app.route("/customers")
def customers():

    search = request.args.get("search", "").strip()

    connection = get_connection()
    cursor = connection.cursor()

    if search:

        cursor.execute("""
            SELECT
                customer_id,
                customer_name,
                phone,
                email,
                address
            FROM customers
            WHERE
                LOWER(customer_name)
                LIKE LOWER(:1)
                OR phone LIKE :2
                OR LOWER(email)
                LIKE LOWER(:3)
            ORDER BY customer_id
        """, (
            f"%{search}%",
            f"%{search}%",
            f"%{search}%"
        ))

    else:

        cursor.execute("""
            SELECT
                customer_id,
                customer_name,
                phone,
                email,
                address
            FROM customers
            ORDER BY customer_id
        """)

    customers_data = cursor.fetchall()

    cursor.close()
    connection.close()

    return render_template(
        "customers.html",
        customers=customers_data,
        search=search
    )


# =========================================================
# ADD CUSTOMER
# =========================================================

@app.route("/customers/add", methods=["GET", "POST"])
def add_customer():

    if request.method == "POST":

        customer_id = request.form["customer_id"]
        customer_name = request.form["customer_name"]
        phone = request.form["phone"]
        email = request.form["email"]
        address = request.form["address"]

        connection = get_connection()
        cursor = connection.cursor()

        try:

            cursor.execute("""
                INSERT INTO customers
                (
                    customer_id,
                    customer_name,
                    phone,
                    email,
                    address
                )
                VALUES
                (
                    :1,
                    :2,
                    :3,
                    :4,
                    :5
                )
            """, (
                customer_id,
                customer_name,
                phone,
                email,
                address
            ))

            connection.commit()

            flash(
                "Customer added successfully!",
                "success"
            )

        except Exception as e:

            connection.rollback()

            flash(
                f"Error adding customer: {e}",
                "error"
            )

        finally:

            cursor.close()
            connection.close()

        return redirect(url_for("customers"))

    return render_template("add_customer.html")


# =========================================================
# UPDATE CUSTOMER
# =========================================================

@app.route(
    "/customers/update/<int:customer_id>",
    methods=["GET", "POST"]
)
def update_customer(customer_id):

    connection = get_connection()
    cursor = connection.cursor()

    if request.method == "POST":

        customer_name = request.form["customer_name"]
        phone = request.form["phone"]
        email = request.form["email"]
        address = request.form["address"]

        try:

            cursor.execute("""
                UPDATE customers
                SET
                    customer_name = :1,
                    phone = :2,
                    email = :3,
                    address = :4
                WHERE customer_id = :5
            """, (
                customer_name,
                phone,
                email,
                address,
                customer_id
            ))

            connection.commit()

            flash(
                "Customer updated successfully!",
                "success"
            )

        except Exception as e:

            connection.rollback()

            flash(
                f"Error updating customer: {e}",
                "error"
            )

        finally:

            cursor.close()
            connection.close()

        return redirect(url_for("customers"))

    cursor.execute("""
        SELECT
            customer_id,
            customer_name,
            phone,
            email,
            address
        FROM customers
        WHERE customer_id = :1
    """, (customer_id,))

    customer_data = cursor.fetchone()

    cursor.close()
    connection.close()

    if customer_data is None:

        flash(
            "Customer not found!",
            "error"
        )

        return redirect(url_for("customers"))

    return render_template(
        "update_customer.html",
        customer=customer_data
    )


# =========================================================
# DELETE CUSTOMER
# =========================================================

@app.route(
    "/customers/delete/<int:customer_id>",
    methods=["POST"]
)
def delete_customer(customer_id):

    connection = get_connection()
    cursor = connection.cursor()

    try:

        cursor.execute("""
            DELETE FROM customers
            WHERE customer_id = :1
        """, (customer_id,))

        connection.commit()

        flash(
            "Customer deleted successfully!",
            "success"
        )

    except Exception as e:

        connection.rollback()

        flash(
            f"Error deleting customer: {e}",
            "error"
        )

    finally:

        cursor.close()
        connection.close()

    return redirect(url_for("customers"))


# =========================================================
# CUSTOMER ORDER HISTORY
# =========================================================

@app.route("/customers/<int:customer_id>/orders")
def customer_orders(customer_id):

    connection = get_connection()
    cursor = connection.cursor()

    cursor.execute("""
        SELECT
            c.customer_name,
            o.order_id,
            o.order_date,
            o.total_amount
        FROM customers c
        JOIN orders o
            ON c.customer_id = o.customer_id
        WHERE c.customer_id = :1
        ORDER BY o.order_date DESC
    """, (customer_id,))

    order_data = cursor.fetchall()

    customer_name = None

    if order_data:

        customer_name = order_data[0][0]

    else:

        cursor.execute("""
            SELECT customer_name
            FROM customers
            WHERE customer_id = :1
        """, (customer_id,))

        customer = cursor.fetchone()

        if customer:
            customer_name = customer[0]

    cursor.close()
    connection.close()

    if customer_name is None:

        flash(
            "Customer not found!",
            "error"
        )

        return redirect(url_for("customers"))

    return render_template(
        "customer_orders.html",
        customer_name=customer_name,
        orders=order_data
    )


# =========================================================
# CUSTOMER TOTAL SPENDING
# =========================================================

@app.route("/customers/<int:customer_id>/spending")
def customer_spending(customer_id):

    connection = get_connection()
    cursor = connection.cursor()

    cursor.execute("""
        SELECT customer_name
        FROM customers
        WHERE customer_id = :1
    """, (customer_id,))

    customer = cursor.fetchone()

    if customer is None:

        cursor.close()
        connection.close()

        flash(
            "Customer not found!",
            "error"
        )

        return redirect(url_for("customers"))

    customer_name = customer[0]

    cursor.execute("""
        SELECT
            COUNT(order_id),
            NVL(SUM(total_amount), 0)
        FROM orders
        WHERE customer_id = :1
    """, (customer_id,))

    spending = cursor.fetchone()

    order_count = spending[0]
    total_spending = spending[1]

    cursor.close()
    connection.close()

    return render_template(
        "customer_spending.html",
        customer_name=customer_name,
        order_count=order_count,
        total_spending=total_spending
    )


# =========================================================
# ORDER MANAGEMENT
# =========================================================

@app.route("/orders")
def orders():

    search = request.args.get("search", "").strip()

    connection = get_connection()
    cursor = connection.cursor()

    if search:

        cursor.execute("""
            SELECT
                o.order_id,
                o.customer_id,
                c.customer_name,
                o.order_date,
                o.total_amount
            FROM orders o
            JOIN customers c
                ON o.customer_id = c.customer_id
            WHERE
                TO_CHAR(o.order_id) LIKE :1
                OR LOWER(c.customer_name)
                LIKE LOWER(:2)
            ORDER BY o.order_id
        """, (
            f"%{search}%",
            f"%{search}%"
        ))

    else:

        cursor.execute("""
            SELECT
                o.order_id,
                o.customer_id,
                c.customer_name,
                o.order_date,
                o.total_amount
            FROM orders o
            JOIN customers c
                ON o.customer_id = c.customer_id
            ORDER BY o.order_id
        """)

    orders_data = cursor.fetchall()

    cursor.close()
    connection.close()

    return render_template(
        "orders.html",
        orders=orders_data,
        search=search
    )


# =========================================================
# ADD ORDER
# =========================================================

@app.route("/orders/add", methods=["GET", "POST"])
def add_order():

    connection = get_connection()
    cursor = connection.cursor()

    if request.method == "POST":

        order_id = request.form["order_id"]
        customer_id = request.form["customer_id"]

        try:

            cursor.execute("""
                SELECT customer_id
                FROM customers
                WHERE customer_id = :1
            """, (customer_id,))

            customer = cursor.fetchone()

            if customer is None:

                flash(
                    "Customer does not exist!",
                    "error"
                )

            else:

                cursor.execute("""
                    INSERT INTO orders
                    (
                        order_id,
                        customer_id,
                        order_date,
                        total_amount
                    )
                    VALUES
                    (
                        :1,
                        :2,
                        SYSDATE,
                        0
                    )
                """, (
                    order_id,
                    customer_id
                ))

                connection.commit()

                flash(
                    "Order created successfully! "
                    "Now add order items.",
                    "success"
                )

                cursor.close()
                connection.close()

                return redirect(
                    url_for(
                        "order_items",
                        order_id=order_id
                    )
                )

        except Exception as e:

            connection.rollback()

            flash(
                f"Error creating order: {e}",
                "error"
            )

    cursor.execute("""
        SELECT
            customer_id,
            customer_name
        FROM customers
        ORDER BY customer_id
    """)

    customers_data = cursor.fetchall()

    cursor.close()
    connection.close()

    return render_template(
        "add_order.html",
        customers=customers_data
    )


# =========================================================
# ORDER SEARCH
# =========================================================

@app.route("/orders/search")
def search_order():

    order_id = request.args.get(
        "order_id",
        ""
    ).strip()

    if not order_id:

        flash(
            "Please enter an Order ID.",
            "error"
        )

        return redirect(url_for("orders"))

    connection = get_connection()
    cursor = connection.cursor()

    cursor.execute("""
        SELECT
            o.order_id,
            o.customer_id,
            c.customer_name,
            o.order_date,
            o.total_amount
        FROM orders o
        JOIN customers c
            ON o.customer_id = c.customer_id
        WHERE o.order_id = :1
    """, (order_id,))

    order_data = cursor.fetchone()

    cursor.close()
    connection.close()

    if order_data is None:

        flash(
            "Order not found!",
            "error"
        )

        return redirect(url_for("orders"))

    return render_template(
        "order_search_result.html",
        order=order_data
    )


# =========================================================
# ORDER DETAILS
# =========================================================

@app.route("/orders/<int:order_id>")
def order_details(order_id):

    connection = get_connection()
    cursor = connection.cursor()

    cursor.execute("""
        SELECT
            o.order_id,
            o.order_date,
            c.customer_id,
            c.customer_name,
            c.phone,
            c.email,
            c.address
        FROM orders o
        JOIN customers c
            ON o.customer_id = c.customer_id
        WHERE o.order_id = :1
    """, (order_id,))

    order = cursor.fetchone()

    if order is None:

        cursor.close()
        connection.close()

        flash(
            "Order not found!",
            "error"
        )

        return redirect(url_for("orders"))

    cursor.execute("""
        SELECT
            oi.order_item_id,
            p.product_name,
            oi.quantity,
            oi.price,
            oi.quantity * oi.price
        FROM order_items oi
        JOIN products p
            ON oi.product_id = p.product_id
        WHERE oi.order_id = :1
        ORDER BY oi.order_item_id
    """, (order_id,))

    items = cursor.fetchall()

    cursor.execute("""
        SELECT
            NVL(SUM(quantity * price), 0)
        FROM order_items
        WHERE order_id = :1
    """, (order_id,))

    total = cursor.fetchone()[0]

    cursor.close()
    connection.close()

    return render_template(
        "order_details.html",
        order=order,
        items=items,
        total=total
    )


# =========================================================
# CALCULATE ORDER TOTAL
# =========================================================

@app.route(
    "/orders/<int:order_id>/calculate",
    methods=["POST"]
)
def calculate_order_total(order_id):

    connection = get_connection()
    cursor = connection.cursor()

    try:

        cursor.execute("""
            SELECT
                NVL(SUM(quantity * price), 0)
            FROM order_items
            WHERE order_id = :1
        """, (order_id,))

        total = cursor.fetchone()[0]

        cursor.execute("""
            UPDATE orders
            SET total_amount = :1
            WHERE order_id = :2
        """, (
            total,
            order_id
        ))

        connection.commit()

        flash(
            f"Order total updated successfully: ₹{total:.2f}",
            "success"
        )

    except Exception as e:

        connection.rollback()

        flash(
            f"Error calculating total: {e}",
            "error"
        )

    finally:

        cursor.close()
        connection.close()

    return redirect(
        url_for(
            "order_details",
            order_id=order_id
        )
    )


# =========================================================
# ORDERS BY CUSTOMER
# =========================================================

@app.route("/orders/customer")
def orders_by_customer():

    customer_id = request.args.get(
        "customer_id",
        ""
    ).strip()

    connection = get_connection()
    cursor = connection.cursor()

    cursor.execute("""
        SELECT
            customer_id,
            customer_name
        FROM customers
        ORDER BY customer_id
    """)

    customers_data = cursor.fetchall()

    orders_data = []
    customer_name = None

    if customer_id:

        cursor.execute("""
            SELECT customer_name
            FROM customers
            WHERE customer_id = :1
        """, (customer_id,))

        customer = cursor.fetchone()

        if customer:

            customer_name = customer[0]

            cursor.execute("""
                SELECT
                    order_id,
                    order_date,
                    total_amount
                FROM orders
                WHERE customer_id = :1
                ORDER BY order_date DESC
            """, (customer_id,))

            orders_data = cursor.fetchall()

        else:

            flash(
                "Customer not found!",
                "error"
            )

    cursor.close()
    connection.close()

    return render_template(
        "orders_by_customer.html",
        customers=customers_data,
        orders=orders_data,
        customer_name=customer_name,
        selected_customer=customer_id
    )


# =========================================================
# SALES REPORT
# =========================================================

@app.route("/orders/report")
def sales_report():

    connection = get_connection()
    cursor = connection.cursor()

    cursor.execute("""
        SELECT
            COUNT(order_id),
            NVL(SUM(total_amount), 0),
            NVL(AVG(total_amount), 0),
            NVL(MAX(total_amount), 0)
        FROM orders
    """)

    report = cursor.fetchone()

    total_orders = report[0]
    total_sales = report[1]
    average_order = report[2]
    highest_order = report[3]

    cursor.execute("""
        SELECT
            o.order_id,
            c.customer_name,
            o.order_date,
            o.total_amount
        FROM orders o
        JOIN customers c
            ON o.customer_id = c.customer_id
        ORDER BY o.order_id DESC
    """)

    orders_data = cursor.fetchall()

    cursor.close()
    connection.close()

    return render_template(
        "sales_report.html",
        total_orders=total_orders,
        total_sales=total_sales,
        average_order=average_order,
        highest_order=highest_order,
        orders=orders_data
    )


# =========================================================
# ORDER ITEMS
# =========================================================

@app.route(
    "/orders/<int:order_id>/items",
    methods=["GET", "POST"]
)
def order_items(order_id):

    connection = get_connection()
    cursor = connection.cursor()

    # Check whether order exists
    cursor.execute("""
        SELECT
            order_id,
            customer_id
        FROM orders
        WHERE order_id = :1
    """, (order_id,))

    order = cursor.fetchone()

    if order is None:

        cursor.close()
        connection.close()

        flash(
            "Order not found!",
            "error"
        )

        return redirect(url_for("orders"))

    # -----------------------------------------------------
    # ADD ORDER ITEM
    # -----------------------------------------------------

    if request.method == "POST":

        product_id = request.form["product_id"]
        quantity = int(request.form["quantity"])

        try:

            if quantity <= 0:

                flash(
                    "Quantity must be greater than 0.",
                    "error"
                )

            else:

                # -----------------------------------------
                # Automatically generate Order Item ID
                # -----------------------------------------

                cursor.execute("""
                    SELECT NVL(MAX(order_item_id), 0) + 1
                    FROM order_items
                """)

                order_item_id = cursor.fetchone()[0]

                # -----------------------------------------
                # Get Product
                # -----------------------------------------

                cursor.execute("""
                    SELECT
                        product_name,
                        price,
                        quantity
                    FROM products
                    WHERE product_id = :1
                """, (product_id,))

                product = cursor.fetchone()

                if product is None:

                    flash(
                        "Product not found!",
                        "error"
                    )

                else:

                    product_name = product[0]
                    price = product[1]
                    stock = product[2]

                    # -------------------------------------
                    # Check Stock
                    # -------------------------------------

                    if quantity > stock:

                        flash(
                            f"Only {stock} units of "
                            f"{product_name} are available.",
                            "error"
                        )

                    else:

                        # ---------------------------------
                        # Insert Order Item
                        # ---------------------------------

                        cursor.execute("""
                            INSERT INTO order_items
                            (
                                order_item_id,
                                order_id,
                                product_id,
                                quantity,
                                price
                            )
                            VALUES
                            (
                                :1,
                                :2,
                                :3,
                                :4,
                                :5
                            )
                        """, (
                            order_item_id,
                            order_id,
                            product_id,
                            quantity,
                            price
                        ))

                        # ---------------------------------
                        # Reduce Product Stock
                        # ---------------------------------

                        cursor.execute("""
                            UPDATE products
                            SET quantity = quantity - :1
                            WHERE product_id = :2
                        """, (
                            quantity,
                            product_id
                        ))

                        # ---------------------------------
                        # Calculate Order Total
                        # ---------------------------------

                        cursor.execute("""
                            SELECT
                                NVL(
                                    SUM(quantity * price),
                                    0
                                )
                            FROM order_items
                            WHERE order_id = :1
                        """, (order_id,))

                        total = cursor.fetchone()[0]

                        # ---------------------------------
                        # Update Order Total
                        # ---------------------------------

                        cursor.execute("""
                            UPDATE orders
                            SET total_amount = :1
                            WHERE order_id = :2
                        """, (
                            total,
                            order_id
                        ))

                        connection.commit()

                        flash(
                            f"{product_name} added successfully! "
                            f"Order Item ID: {order_item_id}",
                            "success"
                        )

        except Exception as e:

            connection.rollback()

            flash(
                f"Error adding order item: {e}",
                "error"
            )

    # -----------------------------------------------------
    # Get Current Order Items
    # -----------------------------------------------------

    cursor.execute("""
        SELECT
            oi.order_item_id,
            p.product_name,
            oi.quantity,
            oi.price,
            oi.quantity * oi.price
        FROM order_items oi
        JOIN products p
            ON oi.product_id = p.product_id
        WHERE oi.order_id = :1
        ORDER BY oi.order_item_id
    """, (order_id,))

    items = cursor.fetchall()

    # -----------------------------------------------------
    # Get Order Total
    # -----------------------------------------------------

    cursor.execute("""
        SELECT
            NVL(SUM(quantity * price), 0)
        FROM order_items
        WHERE order_id = :1
    """, (order_id,))

    total = cursor.fetchone()[0]

    # -----------------------------------------------------
    # Get Products
    # -----------------------------------------------------

    cursor.execute("""
        SELECT
            product_id,
            product_name,
            price,
            quantity
        FROM products
        ORDER BY product_id
    """)

    products_data = cursor.fetchall()

    cursor.close()
    connection.close()

    return render_template(
        "order_items.html",
        order_id=order_id,
        items=items,
        total=total,
        products=products_data
    )


# =========================================================
# INVOICE
# =========================================================

@app.route("/invoice", methods=["GET", "POST"])
def invoice():

    invoice_data = None
    items = []
    total = 0

    if request.method == "POST":

        order_id = request.form["order_id"]

        connection = get_connection()
        cursor = connection.cursor()

        try:

            # ---------------------------------------------
            # Get Order and Customer
            # ---------------------------------------------

            cursor.execute("""
                SELECT
                    o.order_id,
                    o.order_date,
                    c.customer_id,
                    c.customer_name,
                    c.phone,
                    c.email,
                    c.address
                FROM orders o
                JOIN customers c
                    ON o.customer_id = c.customer_id
                WHERE o.order_id = :1
            """, (order_id,))

            invoice_data = cursor.fetchone()

            if invoice_data is None:

                flash(
                    "Order not found!",
                    "error"
                )

            else:

                # -----------------------------------------
                # Get Order Items
                # -----------------------------------------

                cursor.execute("""
                    SELECT
                        oi.order_item_id,
                        p.product_name,
                        oi.quantity,
                        oi.price,
                        oi.quantity * oi.price
                    FROM order_items oi
                    JOIN products p
                        ON oi.product_id = p.product_id
                    WHERE oi.order_id = :1
                    ORDER BY oi.order_item_id
                """, (order_id,))

                items = cursor.fetchall()

                # -----------------------------------------
                # Calculate Total
                # -----------------------------------------

                cursor.execute("""
                    SELECT
                        NVL(SUM(quantity * price), 0)
                    FROM order_items
                    WHERE order_id = :1
                """, (order_id,))

                total = cursor.fetchone()[0]

        except Exception as e:

            flash(
                f"Error generating invoice: {e}",
                "error"
            )

        finally:

            cursor.close()
            connection.close()

    return render_template(
        "invoice.html",
        invoice=invoice_data,
        items=items,
        total=total
    )


# =========================================================
# RUN FLASK APPLICATION
# =========================================================

if __name__ == "__main__":

    app.run(debug=True)