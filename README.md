# Grocery Management System

A web-based Grocery Management System developed using Python, Flask, Oracle Database, HTML, CSS, and Jinja2.

## Project Overview

The Grocery Management System helps manage grocery products, customers, orders, order items, and customer invoices through a web application.

The project also includes a Python console-based version for performing the same major operations.

## Features

### Product Management

* Add new products
* View all products
* Update product information
* Delete products
* Search products
* View products by category
* Identify low-stock products

### Customer Management

* Add customers
* View customers
* Update customer information
* Delete customers
* Search customers
* View customer order history
* Calculate customer total spending

### Order Management

* Create new orders
* Search orders
* View order details
* View orders by customer
* Calculate order totals
* Generate sales reports

### Order Items

* Add products to orders
* Automatically retrieve product price
* Check available stock
* Automatically reduce product stock
* Automatically update order total
* Display order items and amounts

### Invoice Management

* Generate customer invoices
* Display customer information
* Display ordered products
* Calculate item amounts
* Display subtotal and grand total
* Print invoices

## Technologies Used

* Python
* Flask
* Oracle Database
* SQL
* HTML
* CSS
* Javascript
* Jinja2
* Oracle `oracledb` Python library

## Project Structure

```text
Grocery_Project/
│
├── app.py
├── main.py
├── oracle_connection.py
├── product.py
├── customer.py
├── order.py
├── order_items.py
├── invoice.py
├── README.md
├── .gitignore
│
├── templates/
│   ├── base.html
│   ├── index.html
│   ├── products.html
│   ├── add_product.html
│   ├── update_product.html
│   ├── customers.html
│   ├── add_customer.html
│   ├── update_customer.html
│   ├── customer_orders.html
│   ├── customer_spending.html
│   ├── orders.html
│   ├── add_order.html
│   ├── order_items.html
│   ├── order_details.html
│   ├── orders_by_customer.html
│   ├── sales_report.html
│   ├── order_search_result.html
│   └── invoice.html
│
└── static/
    ├── css/
    │   └── style.css
    │
    └── js/
        └── script.js
```

## Database

The application uses Oracle Database to store:

* Products
* Customers
* Orders
* Order Items

Main tables:

```text
products
customers
orders
order_items
```

Relationships are maintained using primary keys and foreign keys.

## How to Run

### 1. Install required Python packages

```bash
python -m pip install flask oracledb
```

### 2. Configure Oracle Database

Make sure Oracle Database is running and the required tables are created.

Update the database connection details in `oracle_connection.py`.

Do not upload your actual database password to GitHub.

### 3. Start the Flask application

Open the terminal inside the project folder and run:

```bash
python app.py
```

### 4. Open the application

Open the Flask application in your browser using the address shown in the terminal.

Usually:

```text
http://127.0.0.1:5000
```

## Application Flow

```text
Home
 │
 ├── Products
 │    ├── Add
 │    ├── Update
 │    ├── Delete
 │    ├── Search
 │    ├── Category
 │    └── Low Stock
 │
 ├── Customers
 │    ├── Add
 │    ├── Update
 │    ├── Delete
 │    ├── Search
 │    ├── Order History
 │    └── Total Spending
 │
 ├── Orders
 │    ├── Add Order
 │    ├── Search
 │    ├── Order Details
 │    ├── Customer Orders
 │    └── Sales Report
 │
 └── Invoice
      └── Generate & Print
```

## Key Implementation

The project uses Flask routes to connect the web interface with Python backend logic and Oracle Database.

Jinja2 templates are used to dynamically display database information on web pages.

The application also performs automatic stock management when products are added to an order.

## Future Enhancements

* User login and authentication
* Admin and staff roles
* Online payment integration
* Product images
* Dashboard with charts
* Advanced sales analytics
* REST API
* Deployment to AWS
* Responsive mobile interface

## Author

**Soundarya Gorr**

BE – Electrical and Electronics Engineering

Interested in Python, Full Stack Development, SQL, Cloud, and DevOps.
