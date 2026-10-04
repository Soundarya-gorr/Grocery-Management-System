import oracledb
from oracle_connection import get_connection


# ==========================================
# VIEW CUSTOMERS
# ==========================================

def get_customers():

    connection = get_connection()
    cursor = connection.cursor()

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

    rows = cursor.fetchall()

    cursor.close()
    connection.close()

    return rows


def display_customers(customers):

    print("\n" + "=" * 90)
    print("                         CUSTOMER LIST")
    print("=" * 90)

    if len(customers) == 0:

        print("No customers found!")

    else:

        print(
            f"{'ID':<6}"
            f"{'Name':<18}"
            f"{'Phone':<15}"
            f"{'Email':<30}"
            f"{'Address':<20}"
        )

        print("-" * 90)

        for customer in customers:

            customer_id = customer[0]
            customer_name = customer[1]
            phone = customer[2]
            email = customer[3]
            address = customer[4]

            print(
                f"{customer_id:<6}"
                f"{customer_name:<18}"
                f"{phone:<15}"
                f"{email:<30}"
                f"{address:<20}"
            )

    print("=" * 90)


def view_customers():

    try:

        customers = get_customers()

        display_customers(customers)

    except Exception as e:

        print("Error while viewing customers:", e)


# ==========================================
# SEARCH CUSTOMER
# ==========================================

def search_customer(search_text):

    connection = None
    cursor = None

    try:

        connection = get_connection()
        cursor = connection.cursor()

        cursor.execute("""
            SELECT
                customer_id,
                customer_name,
                phone,
                email,
                address
            FROM customers
            WHERE LOWER(customer_name)
            LIKE LOWER(:1)
            ORDER BY customer_id
        """, (
            "%" + search_text + "%",
        ))

        customers = cursor.fetchall()

        if len(customers) == 0:

            print("\nNo matching customers found!")

        else:

            display_customers(customers)

    except Exception as e:

        print("\nError while searching customer:", e)

    finally:

        if cursor:
            cursor.close()

        if connection:
            connection.close()


# ==========================================
# CUSTOMER ORDER HISTORY
# ==========================================

def customer_order_history(customer_id):

    connection = None
    cursor = None

    try:

        connection = get_connection()
        cursor = connection.cursor()

        # ----------------------------------
        # CHECK CUSTOMER
        # ----------------------------------

        cursor.execute("""
            SELECT customer_name
            FROM customers
            WHERE customer_id = :1
        """, (customer_id,))

        customer = cursor.fetchone()

        if customer is None:

            print("\nCustomer not found!")

            return

        customer_name = customer[0]


        # ----------------------------------
        # GET ORDERS
        # ----------------------------------

        cursor.execute("""
            SELECT
                order_id,
                order_date,
                total_amount
            FROM orders
            WHERE customer_id = :1
            ORDER BY order_id
        """, (customer_id,))

        orders = cursor.fetchall()


        print("\n" + "=" * 65)
        print("                  CUSTOMER ORDER HISTORY")
        print("=" * 65)

        print("Customer ID   :", customer_id)
        print("Customer Name :", customer_name)

        print("-" * 65)

        if len(orders) == 0:

            print("No orders found for this customer.")

        else:

            print(
                f"{'Order ID':<12}"
                f"{'Order Date':<25}"
                f"{'Amount':<15}"
            )

            print("-" * 65)

            for order in orders:

                order_id = order[0]
                order_date = order[1]
                amount = order[2]

                if amount is None:
                    amount = 0

                print(
                    f"{order_id:<12}"
                    f"{str(order_date):<25}"
                    f"{amount:<15.2f}"
                )

        print("=" * 65)

    except Exception as e:

        print(
            "\nError while getting order history:",
            e
        )

    finally:

        if cursor:
            cursor.close()

        if connection:
            connection.close()


# ==========================================
# CUSTOMER TOTAL SPENDING
# ==========================================

def customer_total_spending(customer_id):

    connection = None
    cursor = None

    try:

        connection = get_connection()
        cursor = connection.cursor()

        cursor.execute("""
            SELECT
                c.customer_name,
                NVL(SUM(o.total_amount), 0)
            FROM customers c
            LEFT JOIN orders o
                ON c.customer_id = o.customer_id
            WHERE c.customer_id = :1
            GROUP BY
                c.customer_name
        """, (customer_id,))

        result = cursor.fetchone()

        if result is None:

            print("\nCustomer not found!")

            return

        customer_name = result[0]
        total_spending = result[1]


        print("\n==========================================")
        print("          CUSTOMER SPENDING")
        print("==========================================")

        print("Customer ID    :", customer_id)
        print("Customer Name  :", customer_name)
        print(
            "Total Spending :",
            f"{total_spending:.2f}"
        )

        print("==========================================")

    except Exception as e:

        print(
            "\nError while calculating spending:",
            e
        )

    finally:

        if cursor:
            cursor.close()

        if connection:
            connection.close()


# ==========================================
# ADD CUSTOMER
# ==========================================

def add_customer(
    customer_id,
    customer_name,
    phone,
    email,
    address
):

    connection = None
    cursor = None

    try:

        connection = get_connection()
        cursor = connection.cursor()

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

        print("\nCustomer added successfully!")

    except oracledb.IntegrityError:

        print("\nCustomer ID already exists!")

    except Exception as e:

        print(
            "\nError while adding customer:",
            e
        )

    finally:

        if cursor:
            cursor.close()

        if connection:
            connection.close()


# ==========================================
# UPDATE CUSTOMER
# ==========================================

def update_customer(
    customer_id,
    phone,
    email,
    address
):

    connection = None
    cursor = None

    try:

        connection = get_connection()
        cursor = connection.cursor()

        cursor.execute("""
            UPDATE customers
            SET
                phone = :1,
                email = :2,
                address = :3
            WHERE customer_id = :4
        """, (
            phone,
            email,
            address,
            customer_id
        ))

        if cursor.rowcount == 0:

            print("\nCustomer not found!")

        else:

            connection.commit()

            print(
                "\nCustomer updated successfully!"
            )

    except Exception as e:

        print(
            "\nError while updating customer:",
            e
        )

    finally:

        if cursor:
            cursor.close()

        if connection:
            connection.close()


# ==========================================
# DELETE CUSTOMER
# ==========================================

def delete_customer(customer_id):

    connection = None
    cursor = None

    try:

        connection = get_connection()
        cursor = connection.cursor()

        cursor.execute("""
            DELETE FROM customers
            WHERE customer_id = :1
        """, (customer_id,))

        if cursor.rowcount == 0:

            print("\nCustomer not found!")

        else:

            connection.commit()

            print(
                "\nCustomer deleted successfully!"
            )

    except oracledb.IntegrityError:

        print(
            "\nCannot delete this customer because "
            "they have existing orders."
        )

    except Exception as e:

        print(
            "\nError while deleting customer:",
            e
        )

    finally:

        if cursor:
            cursor.close()

        if connection:
            connection.close()


# ==========================================
# CUSTOMER MENU
# ==========================================

def customer_menu():

    while True:

        print("\n================================")
        print("       CUSTOMER MANAGEMENT")
        print("================================")

        print("1. View Customers")
        print("2. Add Customer")
        print("3. Update Customer")
        print("4. Delete Customer")
        print("5. Search Customer")
        print("6. Customer Order History")
        print("7. Customer Total Spending")
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

            view_customers()


        # ----------------------------------
        # ADD
        # ----------------------------------

        elif choice == 2:

            try:

                customer_id = int(
                    input("Enter customer ID: ")
                )

                customer_name = input(
                    "Enter customer name: "
                )

                phone = input(
                    "Enter phone: "
                )

                email = input(
                    "Enter email: "
                )

                address = input(
                    "Enter address: "
                )

                if customer_name.strip() == "":

                    print(
                        "Customer name cannot be empty."
                    )

                elif phone.strip() == "":

                    print(
                        "Phone cannot be empty."
                    )

                else:

                    add_customer(
                        customer_id,
                        customer_name,
                        phone,
                        email,
                        address
                    )

            except ValueError:

                print(
                    "Please enter a valid customer ID."
                )


        # ----------------------------------
        # UPDATE
        # ----------------------------------

        elif choice == 3:

            try:

                customer_id = int(
                    input("Enter customer ID: ")
                )

                phone = input(
                    "Enter new phone: "
                )

                email = input(
                    "Enter new email: "
                )

                address = input(
                    "Enter new address: "
                )

                update_customer(
                    customer_id,
                    phone,
                    email,
                    address
                )

            except ValueError:

                print(
                    "Please enter a valid customer ID."
                )


        # ----------------------------------
        # DELETE
        # ----------------------------------

        elif choice == 4:

            try:

                customer_id = int(
                    input("Enter customer ID: ")
                )

                delete_customer(customer_id)

            except ValueError:

                print(
                    "Please enter a valid customer ID."
                )


        # ----------------------------------
        # SEARCH
        # ----------------------------------

        elif choice == 5:

            search_text = input(
                "Enter customer name to search: "
            )

            search_customer(search_text)


        # ----------------------------------
        # ORDER HISTORY
        # ----------------------------------

        elif choice == 6:

            try:

                customer_id = int(
                    input("Enter customer ID: ")
                )

                customer_order_history(
                    customer_id
                )

            except ValueError:

                print(
                    "Please enter a valid customer ID."
                )


        # ----------------------------------
        # TOTAL SPENDING
        # ----------------------------------

        elif choice == 7:

            try:

                customer_id = int(
                    input("Enter customer ID: ")
                )

                customer_total_spending(
                    customer_id
                )

            except ValueError:

                print(
                    "Please enter a valid customer ID."
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

    customer_menu()