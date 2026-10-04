import oracledb
from oracle_connection import get_connection


# ==========================================
# VIEW ORDER ITEMS
# ==========================================

def get_order_items():

    connection = get_connection()
    cursor = connection.cursor()

    cursor.execute("""
        SELECT
            oi.order_item_id,
            oi.order_id,
            p.product_name,
            oi.quantity,
            oi.price
        FROM order_items oi
        INNER JOIN products p
            ON oi.product_id = p.product_id
        ORDER BY oi.order_item_id
    """)

    rows = cursor.fetchall()

    cursor.close()
    connection.close()

    return rows


def view_order_items():

    try:

        items = get_order_items()

        print("\n======================================================================")
        print("                         ORDER ITEM LIST")
        print("======================================================================")

        if len(items) == 0:

            print("No order items found!")

        else:

            print(
                f"{'Item ID':<10}"
                f"{'Order ID':<10}"
                f"{'Product':<20}"
                f"{'Quantity':<10}"
                f"{'Price':<12}"
                f"{'Total':<12}"
            )

            print("-" * 74)

            for item in items:

                item_id = item[0]
                order_id = item[1]
                product_name = item[2]
                quantity = item[3]
                price = item[4]

                item_total = quantity * price

                print(
                    f"{item_id:<10}"
                    f"{order_id:<10}"
                    f"{product_name:<20}"
                    f"{quantity:<10}"
                    f"{price:<12.2f}"
                    f"{item_total:<12.2f}"
                )

        print("======================================================================")


    except Exception as e:

        print("Error while viewing order items:", e)


# ==========================================
# CHECK ORDER
# ==========================================

def order_exists(order_id):

    connection = get_connection()
    cursor = connection.cursor()

    cursor.execute("""
        SELECT order_id
        FROM orders
        WHERE order_id = :1
    """, (order_id,))

    result = cursor.fetchone()

    cursor.close()
    connection.close()

    return result is not None


# ==========================================
# CHECK PRODUCT
# ==========================================

def get_product(product_id):

    connection = get_connection()
    cursor = connection.cursor()

    cursor.execute("""
        SELECT
            product_id,
            product_name,
            price,
            quantity
        FROM products
        WHERE product_id = :1
    """, (product_id,))

    result = cursor.fetchone()

    cursor.close()
    connection.close()

    return result


# ==========================================
# UPDATE ORDER TOTAL
# ==========================================

def update_order_total(connection, cursor, order_id):

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

    return total


# ==========================================
# ADD ORDER ITEM
# ==========================================

def add_order_item(
    order_item_id,
    order_id,
    product_id,
    quantity
):

    connection = None
    cursor = None

    try:

        # ----------------------------------
        # VALIDATE QUANTITY
        # ----------------------------------

        if quantity <= 0:

            print("\nQuantity must be greater than 0.")

            return


        # ----------------------------------
        # CHECK ORDER
        # ----------------------------------

        if not order_exists(order_id):

            print("\nOrder not found!")

            return


        # ----------------------------------
        # GET PRODUCT
        # ----------------------------------

        product = get_product(product_id)

        if product is None:

            print("\nProduct not found!")

            return


        product_name = product[1]
        price = product[2]
        available_stock = product[3]


        # ----------------------------------
        # CHECK STOCK
        # ----------------------------------

        if quantity > available_stock:

            print("\nInsufficient stock!")

            print("Product :", product_name)
            print("Available stock :", available_stock)
            print("Requested quantity :", quantity)

            return


        # ----------------------------------
        # DATABASE CONNECTION
        # ----------------------------------

        connection = get_connection()
        cursor = connection.cursor()


        # ----------------------------------
        # INSERT ORDER ITEM
        # ----------------------------------

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


        # ----------------------------------
        # REDUCE PRODUCT STOCK
        # ----------------------------------

        cursor.execute("""
            UPDATE products
            SET quantity = quantity - :1
            WHERE product_id = :2
        """, (
            quantity,
            product_id
        ))


        # ----------------------------------
        # UPDATE ORDER TOTAL
        # ----------------------------------

        total = update_order_total(
            connection,
            cursor,
            order_id
        )


        # ----------------------------------
        # COMMIT ALL CHANGES
        # ----------------------------------

        connection.commit()


        print("\n======================================")
        print("       ORDER ITEM ADDED")
        print("======================================")

        print("Item ID        :", order_item_id)
        print("Order ID       :", order_id)
        print("Product        :", product_name)
        print("Quantity       :", quantity)
        print("Price          :", price)
        print("Item Total     :", quantity * price)
        print("Order Total    :", total)

        print("======================================")


    except oracledb.IntegrityError:

        if connection:
            connection.rollback()

        print("\nOrder Item ID already exists!")


    except Exception as e:

        if connection:
            connection.rollback()

        print("\nError while adding order item:", e)


    finally:

        if cursor:
            cursor.close()

        if connection:
            connection.close()


# ==========================================
# ORDER ITEM MENU
# ==========================================

def order_item_menu():

    while True:

        print("\n================================")
        print("         ORDER ITEMS")
        print("================================")

        print("1. View Order Items")
        print("2. Add Order Item")
        print("3. Back")

        try:

            choice = int(input("Enter your choice: "))

        except ValueError:

            print("Please enter a valid number.")

            continue


        # ----------------------------------
        # VIEW
        # ----------------------------------

        if choice == 1:

            view_order_items()


        # ----------------------------------
        # ADD
        # ----------------------------------

        elif choice == 2:

            try:

                order_item_id = int(
                    input("Enter order item ID: ")
                )

                order_id = int(
                    input("Enter order ID: ")
                )

                product_id = int(
                    input("Enter product ID: ")
                )

                quantity = int(
                    input("Enter quantity: ")
                )


                add_order_item(
                    order_item_id,
                    order_id,
                    product_id,
                    quantity
                )


            except ValueError:

                print(
                    "Please enter valid numeric values."
                )


        # ----------------------------------
        # BACK
        # ----------------------------------

        elif choice == 3:

            break


        else:

            print(
                "Invalid choice! Please choose 1 to 3."
            )


# ==========================================
# DIRECT EXECUTION
# ==========================================

if __name__ == "__main__":

    order_item_menu()