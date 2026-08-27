# 🛒 CartNexa – Inventory Management System

CartNexa is a web-based **Inventory Management System** developed using Python and Flask. The application helps administrators manage products, categories, suppliers, purchases, sales, and customer orders, while users can browse products, maintain wishlists, place orders, and submit product reviews.

The project provides separate interfaces for **Administrators and Users** and uses a MySQL database for storing application data.

---

## 📌 Project Overview

CartNexa is designed to simplify inventory and online product management through a centralized web application.

### 👨‍💼 Admin

Administrators can:

- Manage products
- Add, edit, and delete products
- Manage product categories
- Manage suppliers
- Record purchases
- Manage sales
- Monitor inventory
- Identify low-stock products
- View out-of-stock products
- Manage customer orders
- Update order status
- View sales reports
- View purchase reports
- Calculate sales, purchase totals, and profit
- Generate invoices
- Monitor customer reviews

### 👤 User

Registered users can:

- Create an account
- Login securely
- Browse available products
- Search products
- View product details
- View product prices and stock
- Add products to wishlist
- Remove products from wishlist
- Place product orders
- Select payment methods
- Provide delivery information
- View order history
- View order details
- View invoices
- Submit product reviews
- Give product ratings
- Mark reviews as helpful
- View verified purchase reviews

---

# ✨ Features

## 🔐 Authentication

- Admin login
- User registration
- User login
- Session-based authentication
- Logout functionality
- Password validation during registration

## 📦 Product Management

- Add products
- Edit products
- Delete products
- Product categories
- Product pricing
- Product quantity/stock management
- Product images
- Product search
- Product details

## 🏷️ Category Management

The system supports product categorization to organize inventory efficiently.

## 🚚 Supplier Management

Administrators can:

- Add suppliers
- Store supplier contact information
- Store company information
- View supplier records

## 🛍️ Purchase Management

Administrators can:

- Record purchases
- Select products
- Select suppliers
- Enter purchase quantity
- Enter purchase price
- Calculate total purchase amount
- Automatically increase product stock
- View purchase history

## 💰 Sales Management

Administrators can:

- Record sales
- Select products
- Enter customer information
- Select quantity
- Calculate total sales amount
- Automatically reduce product stock
- View sales history

## 📊 Inventory Dashboard

The admin dashboard provides information such as:

- Total products
- Total sales
- Low-stock products
- Out-of-stock products
- Recent sales
- Inventory status

## 📈 Reports

The reporting section provides:

- Total sales
- Total purchases
- Items sold
- Items purchased
- Profit calculation
- Product-wise sales information
- Product-wise profit information
- Daily reports
- Monthly reports
- Overall reports

## 🛒 Shopping Features

Users can:

- Browse products
- Search products
- View product information
- Check stock availability
- Select product quantity
- Place orders
- View order history

## ❤️ Wishlist

Users can:

- Add products to wishlist
- Remove products from wishlist
- View saved products

## ⭐ Product Reviews & Ratings

Users can:

- Give ratings from 1 to 5
- Write product reviews
- View other users' reviews
- See average product ratings
- View rating distribution
- Mark reviews as helpful
- See verified purchase reviews

## 📦 Order Management

Users can:

- Place orders
- Provide customer details
- Enter delivery address
- Select payment method
- View order status
- View order history
- View order details
- View invoices

Administrators can:

- View all customer orders
- Update order status
- Track order progress
- Generate sales records when orders are confirmed

---

# 🛠️ Technologies Used

## Frontend

- HTML5
- CSS3
- JavaScript
- Bootstrap

## Backend

- Python
- Flask

## Database

- MySQL

## Database Connector

- MySQL Connector/Python

## Server

- Gunicorn

## Deployment

- Render
- Aiven MySQL

## Development Tools

- Visual Studio Code
- MySQL Workbench
- Git
- GitHub

---

# 🏗️ System Architecture

```text
                    ┌──────────────────────┐
                    │       User/Admin     │
                    └──────────┬───────────┘
                               │
                               ▼
                    ┌──────────────────────┐
                    │     Web Browser      │
                    └──────────┬───────────┘
                               │
                               ▼
                    ┌──────────────────────┐
                    │      Flask App       │
                    │       app.py         │
                    └──────────┬───────────┘
                               │
                               ▼
                    ┌──────────────────────┐
                    │     MySQL Database   │
                    │       defaultdb      │
                    └──────────────────────┘
```
# 🗄️ Database Structure

CartNexa uses MySQL for storing application information.

The database contains the following tables:

```text
admins
categories
products
product_reviews
purchases
review_helpful
sales
suppliers
user_orders
users
wishlist

```
🔑 Environment Variables

The application uses environment variables for database configuration.

```text
DB_HOST=your_database_host
DB_USER=your_database_user
DB_PASSWORD=your_database_password
DB_NAME=your_database_name
DB_PORT=your_database_port
SECRET_KEY=your_secret_key
```
💻 Local Installation

1. Clone the Repository
```text
git clone https://github.com/nee681952/CartNexa--Inventory-Management-System.git
```
2. Open the Project
```text
cd CartNexa--Inventory-Management-System
```
3. Create a Virtual Environment

Windows:
```text
python -m venv venv
```
Activate it:
```text
venv\Scripts\activate
```
4. Install Dependencies
```text
pip install -r requirements.txt
```
5. Configure MySQL

Create a MySQL database and configure the following environment variables:
```text
DB_HOST
DB_USER
DB_PASSWORD
DB_NAME
DB_PORT
```
6. Import the Database

The repository contains:
```text
inventory_db.sql
```
Import this SQL file into your MySQL database using MySQL Workbench or another MySQL client.

7. Run the Application
```text
python app.py
```
The application will normally run at:
```text
http://localhost:5000
```
🚀 Deployment

CartNexa is deployed using:

Application Hosting

Render

Database Hosting

Aiven MySQL

The Flask application uses environment variables to securely connect to the hosted MySQL database.

🔒 Security Considerations

The project includes several basic security practices:

Session-based authentication
Login validation
Registration validation
Password confirmation
Password strength validation
Access control for admin pages
Access control for user pages
Input validation
Environment variables for database credentials

📌 Future Enhancements

Possible future improvements include:

Mobile application
Payment gateway integration
Email order notifications
SMS notifications
Advanced analytics dashboard
Barcode scanning
PDF invoice generation
Product recommendations
Admin analytics
Password reset functionality
Two-factor authentication
REST API
Android application
Progressive Web App (PWA)
Cloud image storage

🎯 Project Objectives

The main objectives of CartNexa are:

To simplify inventory management.
To maintain product information efficiently.
To manage suppliers and purchases.
To track sales and inventory levels.
To provide an online product browsing system.
To allow users to place orders.
To provide wishlist functionality.
To allow customers to review products.
To provide sales and purchase reports.
To provide separate admin and user interfaces.

👨‍💻 Author
Neeraj J

MCA Graduate

Python | Flask | MySQL | Web Development

📄 License

This project is developed for educational, academic, and portfolio purposes.

⭐ Support

If you find this project useful, consider giving the repository a ⭐ on GitHub.

