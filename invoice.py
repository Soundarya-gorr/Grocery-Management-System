import oracledb
from oracle_connection import get_connection


# ==========================================
# GET INVOICE DATA
# ==========================================

def get_invoice(order_id):

    connection = get_connection()
    cursor = connection.cursor()

    # --------------------------------------
    # ORDER + CUSTOMER DETAILS
    # --------------------------------------

    cursor.execute("""
        SELECT
            o.order_id,
            o.order_date,
            c.customer_name,
            c.phone,
            c.email,
            c.address,
            o.total_amount
        FROM orders o
        INNER JOIN customers c
            ON o.customer_id = c.customer_id
        WHERE o.order_id = :1
    """, (order_id,))

    order = cursor.fetchone()

    if order is None:

        cursor.close()
        connection.close()

        return None, []


    # --------------------------------------
    # ORDER ITEMS
    # --------------------------------------

    cursor.execute("""
        SELECT
            p.product_name,
            oi.quantity,
            oi.price
        FROM order_items oi
        INNER JOIN products p
            ON oi.product_id = p.product_id
        WHERE oi.order_id = :1
        ORDER BY oi.order_item_id
    """, (order_id,))

    items = cursor.fetchall()

    cursor.close()
    connection.close()

    return order, items


# ==========================================
# GENERATE INVOICE
# ==========================================

def generate_invoice(order_id):

    try:

        order, items = get_invoice(order_id)

        # ----------------------------------
        # CHECK ORDER
        # ----------------------------------

        if order is None:

            print("\nOrder not found!")

            return


        # ----------------------------------
        # ORDER INFORMATION
        # ----------------------------------

        invoice_order_id = order[0]
        order_date = order[1]
        customer_name = order[2]
        phone = order[3]
        email = order[4]
        address = order[5]
        database_total = order[6]


        if database_total is None:

            database_total = 0


        # ----------------------------------
        # INVOICE HEADER
        # ----------------------------------

        print("\n")

        print("=" * 80)
        print(" " * 27 + "GROCERY STORE")
        print(" " * 23 + "CUSTOMER INVOICE")
        print("=" * 80)


        # ----------------------------------
        # CUSTOMER DETAILS
        # ----------------------------------

        print(
            f"Invoice No.    : {invoice_order_id}"
        )

        print(
            f"Order Date     : {order_date}"
        )

        print(
            f"Customer Name  : {customer_name}"
        )

        print(
            f"Phone          : {phone}"
        )

        print(
            f"Email          : {email}"
        )

        print(
            f"Address        : {address}"
        )


        print("-" * 80)


        # ----------------------------------
        # TABLE HEADER
        # ----------------------------------

        print(
            f"{'No.':<6}"
            f"{'Product':<25}"
            f"{'Qty':<10}"
            f"{'Price':<15}"
            f"{'Amount':<15}"
        )

        print("-" * 80)


        # ----------------------------------
        # ITEMS
        # ----------------------------------

        subtotal = 0
        item_number = 1
        total_quantity = 0


        for item in items:

            product_name = item[0]
            quantity = item[1]
            price = item[2]

            amount = quantity * price

            subtotal += amount
            total_quantity += quantity


            print(
                f"{item_number:<6}"
                f"{product_name:<25}"
                f"{quantity:<10}"
                f"{price:<15.2f}"
                f"{amount:<15.2f}"
            )

            item_number += 1


        print("-" * 80)


        # ----------------------------------
        # SUMMARY
        # ----------------------------------

        print(
            f"{'Total Items':<55}"
            f"{total_quantity:>15}"
        )

        print(
            f"{'Subtotal':<55}"
            f"{subtotal:>15.2f}"
        )

        print(
            f"{'Grand Total':<55}"
            f"{database_total:>15.2f}"
        )


        print("=" * 80)

        print(
            " " * 25 +
            "Thank you for shopping with us!"
        )

        print(
            " " * 30 +
            "Visit Again!"
        )

        print("=" * 80)


    except Exception as e:

        print(
            "\nError while generating invoice:",
            e
        )


# ==========================================
# INVOICE MENU
# ==========================================

def invoice_menu():

    while True:

        print("\n================================")
        print("        INVOICE MANAGEMENT")
        print("================================")

        print("1. Generate Invoice")
        print("2. Back")

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
        # GENERATE
        # ----------------------------------

        if choice == 1:

            try:

                order_id = int(
                    input("Enter order ID: ")
                )

                generate_invoice(order_id)

            except ValueError:

                print(
                    "Please enter a valid order ID."
                )


        # ----------------------------------
        # BACK
        # ----------------------------------

        elif choice == 2:

            break


        else:

            print(
                "Invalid choice! Please choose 1 or 2."
            )


# ==========================================
# DIRECT EXECUTION
# ==========================================

if __name__ == "__main__":

    invoice_menu()