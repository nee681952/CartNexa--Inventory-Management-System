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
