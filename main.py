import product
import customer
import order
import order_items
import invoice


# ==========================================
# MAIN MENU
# ==========================================

def main_menu():

    while True:

        print("\n")
        print("=" * 45)
        print("          GROCERY MANAGEMENT SYSTEM")
        print("=" * 45)

        print("1. Product Management")
        print("2. Customer Management")
        print("3. Order Management")
        print("4. Order Items")
        print("5. Generate Invoice")
        print("6. Exit")

        print("=" * 45)

        try:

            choice = int(
                input("Enter your choice: ")
            )

        except ValueError:

            print("\nPlease enter a valid number.")

            continue


        # ----------------------------------
        # PRODUCT MANAGEMENT
        # ----------------------------------

        if choice == 1:

            product.product_menu()


        # ----------------------------------
        # CUSTOMER MANAGEMENT
        # ----------------------------------

        elif choice == 2:

            customer.customer_menu()


        # ----------------------------------
        # ORDER MANAGEMENT
        # ----------------------------------

        elif choice == 3:

            order.order_menu()


        # ----------------------------------
        # ORDER ITEMS
        # ----------------------------------

        elif choice == 4:

            order_items.order_item_menu()


        # ----------------------------------
        # INVOICE
        # ----------------------------------

        elif choice == 5:

            invoice.invoice_menu()


        # ----------------------------------
        # EXIT
        # ----------------------------------

        elif choice == 6:

            print("\n" + "=" * 45)
            print(" Thank you for using Grocery Management System!")
            print("=" * 45)

            break


        else:

            print(
                "\nInvalid choice! Please choose 1 to 6."
            )


# ==========================================
# START APPLICATION
# ==========================================

if __name__ == "__main__":

    main_menu()