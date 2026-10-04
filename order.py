import oracledb
from oracle_connection import get_connection


# ==========================================
# VIEW ORDERS
# ==========================================

def get_orders():

    connection = get_connection()
    cursor = connection.cursor()

    cursor.execute("""
        SELECT
            o.order_id,
            c.customer_name,
            o.order_date,
            o.total_amount
        FROM orders o
        INNER JOIN customers c
            ON o.customer_id = c.customer_id
        ORDER BY o.order_id
    """)

    rows = cursor.fetchall()

    cursor.close()
    connection.close()

    return rows


def display_orders(orders):

    print("\n" + "=" * 75)
    print("                         ORDER LIST")
    print("=" * 75)

    if len(orders) == 0:

        print("No orders found!")

    else:

        print(
            f"{'Order ID':<12}"
            f"{'Customer':<20}"
            f"{'Order Date':<25}"
            f"{'Amount':<15}"
        )

        print("-" * 75)

        for order in orders:

            order_id = order[0]
            customer_name = order[1]
            order_date = order[2]
            total_amount = order[3]

            if total_amount is None:
                total_amount = 0

            print(
                f"{order_id:<12}"
                f"{customer_name:<20}"
                f"{str(order_date):<25}"
                f"{total_amount:<15.2f}"
            )

    print("=" * 75)


def view_orders():

    try:

        orders = get_orders()

        display_orders(orders)

    except Exception as e:

        print("Error while viewing orders:", e)


# ==========================================
# SEARCH ORDER
# ==========================================

def search_order(order_id):

    connection = None
    cursor = None

    try:

        connection = get_connection()
        cursor = connection.cursor()

        cursor.execute("""
            SELECT
                o.order_id,
                c.customer_name,
                o.order_date,
                o.total_amount
            FROM orders o
            INNER JOIN customers c
                ON o.customer_id = c.customer_id
            WHERE o.order_id = :1
        """, (order_id,))

        order = cursor.fetchone()

        if order is None:

            print("\nOrder not found!")

        else:

            display_orders([order])

    except Exception as e:

        print("\nError while searching order:", e)

    finally:

        if cursor:
            cursor.close()

        if connection:
            connection.close()


# ==========================================
# CHECK CUSTOMER
# ==========================================

def customer_exists(customer_id):

    connection = get_connection()
    cursor = connection.cursor()

    cursor.execute("""
        SELECT customer_id
        FROM customers
        WHERE customer_id = :1
    """, (customer_id,))

    result = cursor.fetchone()

    cursor.close()
    connection.close()

    return result is not None


# ==========================================
# ADD ORDER
# ==========================================

def add_order(order_id, customer_id):

    connection = None
    cursor = None

    try:

        if not customer_exists(customer_id):

            print("\nCustomer not found!")

            return

        connection = get_connection()
        cursor = connection.cursor()

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

        print("\nOrder added successfully!")

    except oracledb.IntegrityError:

        print("\nOrder ID already exists!")

    except Exception as e:

        print("\nError while adding order:", e)

    finally:

        if cursor:
            cursor.close()

        if connection:
            connection.close()


# ==========================================
# CALCULATE ORDER TOTAL
# ==========================================

def calculate_order_total(order_id):

    connection = None
    cursor = None

    try:

        connection = get_connection()
        cursor = connection.cursor()

        cursor.execute("""
            SELECT order_id
            FROM orders
            WHERE order_id = :1
        """, (order_id,))

        order = cursor.fetchone()

        if order is None:

            print("\nOrder not found!")

            return

        cursor.execute("""
            SELECT
                NVL(SUM(quantity * price), 0)
            FROM order_items
            WHERE order_id = :1
        """, (order_id,))

        result = cursor.fetchone()

        total = result[0]

        cursor.execute("""
            UPDATE orders
            SET total_amount = :1
            WHERE order_id = :2
        """, (
            total,
            order_id
        ))

        connection.commit()

        print("\nOrder total updated successfully!")
        print("Order ID    :", order_id)
        print("Total Amount:", total)

    except Exception as e:

        print(
            "\nError while calculating order total:",
            e
        )

    finally:

        if cursor:
            cursor.close()

        if connection:
            connection.close()


# ==========================================
# SALES REPORT
# ==========================================

def sales_report():

    connection = None
    cursor = None

    try:

        connection = get_connection()
        cursor = connection.cursor()

        # ----------------------------------
        # TOTAL ORDERS
        # ----------------------------------

        cursor.execute("""
            SELECT COUNT(*)
            FROM orders
        """)

        total_orders = cursor.fetchone()[0]


        # ----------------------------------
        # TOTAL SALES
        # ----------------------------------

        cursor.execute("""
            SELECT
                NVL(SUM(total_amount), 0)
            FROM orders
        """)

        total_sales = cursor.fetchone()[0]


        # ----------------------------------
        # AVERAGE ORDER VALUE
        # ----------------------------------

        cursor.execute("""
            SELECT
                NVL(AVG(total_amount), 0)
            FROM orders
        """)

        average_order = cursor.fetchone()[0]


        # ----------------------------------
        # HIGHEST ORDER
        # ----------------------------------

        cursor.execute("""
            SELECT
                NVL(MAX(total_amount), 0)
            FROM orders
        """)

        highest_order = cursor.fetchone()[0]


        print("\n" + "=" * 50)
        print("                  SALES REPORT")
        print("=" * 50)

        print(
            "Total Orders       :",
            total_orders
        )

        print(
            "Total Sales        :",
            f"{total_sales:.2f}"
        )

        print(
            "Average Order      :",
            f"{average_order:.2f}"
        )

        print(
            "Highest Order      :",
            f"{highest_order:.2f}"
        )

        print("=" * 50)

    except Exception as e:

        print(
            "\nError while generating sales report:",
            e
        )

    finally:

        if cursor:
            cursor.close()

        if connection:
            connection.close()


# ==========================================
# ORDERS BY CUSTOMER
# ==========================================

def orders_by_customer(customer_id):

    connection = None
    cursor = None

    try:

        connection = get_connection()
        cursor = connection.cursor()

        cursor.execute("""
            SELECT
                c.customer_name,
                o.order_id,
                o.order_date,
                o.total_amount
            FROM customers c
            INNER JOIN orders o
                ON c.customer_id = o.customer_id
            WHERE c.customer_id = :1
            ORDER BY o.order_id
        """, (customer_id,))

        orders = cursor.fetchall()

        if len(orders) == 0:

            print(
                "\nNo orders found for this customer!"
            )

        else:

            customer_name = orders[0][0]

            print("\n" + "=" * 70)
            print("                  CUSTOMER ORDERS")
            print("=" * 70)

            print("Customer ID   :", customer_id)
            print("Customer Name :", customer_name)

            print("-" * 70)

            print(
                f"{'Order ID':<12}"
                f"{'Order Date':<25}"
                f"{'Amount':<15}"
            )

            print("-" * 70)

            for order in orders:

                order_id = order[1]
                order_date = order[2]
                amount = order[3]

                if amount is None:
                    amount = 0

                print(
                    f"{order_id:<12}"
                    f"{str(order_date):<25}"
                    f"{amount:<15.2f}"
                )

            print("=" * 70)

    except Exception as e:

        print(
            "\nError while getting customer orders:",
            e
        )

    finally:

        if cursor:
            cursor.close()

        if connection:
            connection.close()


# ==========================================
# ORDER DETAILS
# ==========================================

def order_details(order_id):

    connection = None
    cursor = None

    try:

        connection = get_connection()
        cursor = connection.cursor()

        cursor.execute("""
            SELECT
                o.order_id,
                c.customer_name,
                o.order_date,
                p.product_name,
                oi.quantity,
                oi.price
            FROM orders o
            INNER JOIN customers c
                ON o.customer_id = c.customer_id
            INNER JOIN order_items oi
                ON o.order_id = oi.order_id
            INNER JOIN products p
                ON oi.product_id = p.product_id
            WHERE o.order_id = :1
            ORDER BY oi.order_item_id
        """, (order_id,))

        items = cursor.fetchall()

        if len(items) == 0:

            print("\nOrder not found or has no items!")

            return

        order = items[0]

        print("\n" + "=" * 80)
        print("                       ORDER DETAILS")
        print("=" * 80)

        print("Order ID      :", order[0])
        print("Customer Name :", order[1])
        print("Order Date    :", order[2])

        print("-" * 80)

        print(
            f"{'Product':<25}"
            f"{'Quantity':<12}"
            f"{'Price':<15}"
            f"{'Amount':<15}"
        )

        print("-" * 80)

        grand_total = 0

        for item in items:

            product_name = item[3]
            quantity = item[4]
            price = item[5]

            amount = quantity * price

            grand_total += amount

            print(
                f"{product_name:<25}"
                f"{quantity:<12}"
                f"{price:<15.2f}"
                f"{amount:<15.2f}"
            )

        print("-" * 80)

        print(
            f"{'GRAND TOTAL':<52}"
            f"{grand_total:>15.2f}"
        )

        print("=" * 80)

    except Exception as e:

        print(
            "\nError while getting order details:",
            e
        )

    finally:

        if cursor:
            cursor.close()

        if connection:
            connection.close()


# ==========================================
# ORDER MENU
# ==========================================

def order_menu():

    while True:

        print("\n================================")
        print("        ORDER MANAGEMENT")
        print("================================")

        print("1. View Orders")
        print("2. Add Order")
        print("3. Calculate Order Total")
        print("4. Search Order")
        print("5. Sales Report")
        print("6. Orders by Customer")
        print("7. Order Details")
        print("8. Back")

        try:

            choice = int(
                input("Enter your choice: ")
            )

        except ValueError:

            print(
                "Please enter a valid number."
            )

            continue


        # ----------------------------------
        # VIEW
        # ----------------------------------

        if choice == 1:

            view_orders()


        # ----------------------------------
        # ADD
        # ----------------------------------

        elif choice == 2:

            try:

                order_id = int(
                    input("Enter order ID: ")
                )

                customer_id = int(
                    input("Enter customer ID: ")
                )

                add_order(
                    order_id,
                    customer_id
                )

            except ValueError:

                print(
                    "Please enter valid numeric values."
                )


        # ----------------------------------
        # CALCULATE TOTAL
        # ----------------------------------

        elif choice == 3:

            try:

                order_id = int(
                    input("Enter order ID: ")
                )

                calculate_order_total(
                    order_id
                )

            except ValueError:

                print(
                    "Please enter a valid order ID."
                )


        # ----------------------------------
        # SEARCH
        # ----------------------------------

        elif choice == 4:

            try:

                order_id = int(
                    input("Enter order ID: ")
                )

                search_order(order_id)

            except ValueError:

                print(
                    "Please enter a valid order ID."
                )


        # ----------------------------------
        # SALES REPORT
        # ----------------------------------

        elif choice == 5:

            sales_report()


        # ----------------------------------
        # CUSTOMER ORDERS
        # ----------------------------------

        elif choice == 6:

            try:

                customer_id = int(
                    input("Enter customer ID: ")
                )

                orders_by_customer(
                    customer_id
                )

            except ValueError:

                print(
                    "Please enter a valid customer ID."
                )


        # ----------------------------------
        # ORDER DETAILS
        # ----------------------------------

        elif choice == 7:

            try:

                order_id = int(
                    input("Enter order ID: ")
                )

                order_details(order_id)

            except ValueError:

                print(
                    "Please enter a valid order ID."
                )


        # ----------------------------------
        # BACK
        # ----------------------------------

        elif choice == 8:

            break


        else:

            print(
                "Invalid choice! Please choose 1 to 8."
            )


# ==========================================
# DIRECT EXECUTION
# ==========================================

if __name__ == "__main__":

    order_menu()