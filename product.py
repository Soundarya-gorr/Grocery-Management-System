import oracledb
from oracle_connection import get_connection


# ==========================================
# VIEW PRODUCTS
# ==========================================

def get_products():

    connection = get_connection()
    cursor = connection.cursor()

    cursor.execute("""
        SELECT
            product_id,
            product_name,
            category,
            price,
            quantity
        FROM products
        ORDER BY product_id
    """)

    rows = cursor.fetchall()

    cursor.close()
    connection.close()

    return rows


def display_products(products):

    print("\n============================================================")
    print("                     PRODUCT LIST")
    print("============================================================")

    if len(products) == 0:

        print("No products found!")

    else:

        print(
            f"{'ID':<6}"
            f"{'Product Name':<20}"
            f"{'Category':<16}"
            f"{'Price':<12}"
            f"{'Quantity':<10}"
        )

        print("-" * 64)

        for product in products:

            product_id = product[0]
            product_name = product[1]
            category = product[2]
            price = product[3]
            quantity = product[4]

            print(
                f"{product_id:<6}"
                f"{product_name:<20}"
                f"{category:<16}"
                f"{price:<12.2f}"
                f"{quantity:<10}"
            )

    print("============================================================")


def view_products():

    try:

        products = get_products()

        display_products(products)

    except Exception as e:

        print("Error while viewing products:", e)


# ==========================================
# SEARCH PRODUCT
# ==========================================

def search_product(search_text):

    connection = None
    cursor = None

    try:

        connection = get_connection()
        cursor = connection.cursor()

        cursor.execute("""
            SELECT
                product_id,
                product_name,
                category,
                price,
                quantity
            FROM products
            WHERE LOWER(product_name)
            LIKE LOWER(:1)
            ORDER BY product_id
        """, (
            "%" + search_text + "%",
        ))

        products = cursor.fetchall()

        if len(products) == 0:

            print("\nNo matching products found!")

        else:

            print("\nSearch Results:")

            display_products(products)

    except Exception as e:

        print("\nError while searching product:", e)

    finally:

        if cursor:
            cursor.close()

        if connection:
            connection.close()


# ==========================================
# LOW STOCK PRODUCTS
# ==========================================

def low_stock_products():

    connection = None
    cursor = None

    try:

        connection = get_connection()
        cursor = connection.cursor()

        cursor.execute("""
            SELECT
                product_id,
                product_name,
                category,
                price,
                quantity
            FROM products
            WHERE quantity <= 10
            ORDER BY quantity
        """)

        products = cursor.fetchall()

        print("\n==============================================")
        print("             LOW STOCK PRODUCTS")
        print("==============================================")

        if len(products) == 0:

            print("No low-stock products!")

        else:

            display_products(products)

    except Exception as e:

        print("\nError while checking low stock:", e)

    finally:

        if cursor:
            cursor.close()

        if connection:
            connection.close()


# ==========================================
# PRODUCTS BY CATEGORY
# ==========================================

def products_by_category(category):

    connection = None
    cursor = None

    try:

        connection = get_connection()
        cursor = connection.cursor()

        cursor.execute("""
            SELECT
                product_id,
                product_name,
                category,
                price,
                quantity
            FROM products
            WHERE LOWER(category) = LOWER(:1)
            ORDER BY product_id
        """, (category,))

        products = cursor.fetchall()

        if len(products) == 0:

            print("\nNo products found in this category!")

        else:

            print(
                f"\nProducts in category: {category}"
            )

            display_products(products)

    except Exception as e:

        print(
            "\nError while searching category:",
            e
        )

    finally:

        if cursor:
            cursor.close()

        if connection:
            connection.close()


# ==========================================
# ADD PRODUCT
# ==========================================

def add_product(
    product_id,
    product_name,
    category,
    price,
    quantity
):

    connection = None
    cursor = None

    try:

        connection = get_connection()
        cursor = connection.cursor()

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

        print("\nProduct added successfully!")

    except oracledb.IntegrityError:

        print("\nProduct ID already exists!")

    except Exception as e:

        print("\nError while adding product:", e)

    finally:

        if cursor:
            cursor.close()

        if connection:
            connection.close()


# ==========================================
# UPDATE PRODUCT
# ==========================================

def update_product(
    product_id,
    price,
    quantity
):

    connection = None
    cursor = None

    try:

        connection = get_connection()
        cursor = connection.cursor()

        cursor.execute("""
            UPDATE products
            SET
                price = :1,
                quantity = :2
            WHERE product_id = :3
        """, (
            price,
            quantity,
            product_id
        ))

        if cursor.rowcount == 0:

            print("\nProduct not found!")

        else:

            connection.commit()

            print(
                "\nProduct updated successfully!"
            )

    except Exception as e:

        print(
            "\nError while updating product:",
            e
        )

    finally:

        if cursor:
            cursor.close()

        if connection:
            connection.close()


# ==========================================
# DELETE PRODUCT
# ==========================================

def delete_product(product_id):

    connection = None
    cursor = None

    try:

        connection = get_connection()
        cursor = connection.cursor()

        cursor.execute("""
            DELETE FROM products
            WHERE product_id = :1
        """, (product_id,))

        if cursor.rowcount == 0:

            print("\nProduct not found!")

        else:

            connection.commit()

            print(
                "\nProduct deleted successfully!"
            )

    except oracledb.IntegrityError:

        print(
            "\nCannot delete this product because "
            "it is used in an order."
        )

    except Exception as e:

        print(
            "\nError while deleting product:",
            e
        )

    finally:

        if cursor:
            cursor.close()

        if connection:
            connection.close()


# ==========================================
# PRODUCT MENU
# ==========================================

def product_menu():

    while True:

        print("\n================================")
        print("       PRODUCT MANAGEMENT")
        print("================================")

        print("1. View Products")
        print("2. Add Product")
        print("3. Update Product")
        print("4. Delete Product")
        print("5. Search Product")
        print("6. Low Stock Products")
        print("7. Products by Category")
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

            view_products()


        # ----------------------------------
        # ADD
        # ----------------------------------

        elif choice == 2:

            try:

                product_id = int(
                    input("Enter product ID: ")
                )

                product_name = input(
                    "Enter product name: "
                )

                category = input(
                    "Enter category: "
                )

                price = float(
                    input("Enter price: ")
                )

                quantity = int(
                    input("Enter quantity: ")
                )

                if price < 0 or quantity < 0:

                    print(
                        "Price and quantity "
                        "cannot be negative."
                    )

                elif product_name.strip() == "":

                    print(
                        "Product name cannot be empty."
                    )

                else:

                    add_product(
                        product_id,
                        product_name,
                        category,
                        price,
                        quantity
                    )

            except ValueError:

                print(
                    "Please enter valid numeric values."
                )


        # ----------------------------------
        # UPDATE
        # ----------------------------------

        elif choice == 3:

            try:

                product_id = int(
                    input("Enter product ID: ")
                )

                price = float(
                    input("Enter new price: ")
                )

                quantity = int(
                    input("Enter new quantity: ")
                )

                if price < 0 or quantity < 0:

                    print(
                        "Price and quantity "
                        "cannot be negative."
                    )

                else:

                    update_product(
                        product_id,
                        price,
                        quantity
                    )

            except ValueError:

                print(
                    "Please enter valid numeric values."
                )


        # ----------------------------------
        # DELETE
        # ----------------------------------

        elif choice == 4:

            try:

                product_id = int(
                    input("Enter product ID: ")
                )

                delete_product(product_id)

            except ValueError:

                print(
                    "Please enter a valid product ID."
                )


        # ----------------------------------
        # SEARCH
        # ----------------------------------

        elif choice == 5:

            search_text = input(
                "Enter product name to search: "
            )

            search_product(search_text)


        # ----------------------------------
        # LOW STOCK
        # ----------------------------------

        elif choice == 6:

            low_stock_products()


        # ----------------------------------
        # CATEGORY
        # ----------------------------------

        elif choice == 7:

            category = input(
                "Enter category: "
            )

            products_by_category(category)


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

    product_menu()