# 🚀 DigiStore

Modern E-Commerce Web Application (Laptops, Mobiles, Tablets)

DigiStore is a modern and fully-featured Django-based e-commerce platform designed for selling laptops, mobile phones, and tablets.
It includes a powerful product system, shopping cart, payments, seller dashboard, authentication via phone OTP, and a minimal modern UI.

⸻

## 📌 Features

### 🛍️ Core Features
	•	Product listing & filtering (by category)
	•	Product detail pages with stock control
	•	Store (seller) system
	•	Customer dashboard
	•	Seller dashboard (products, orders, revenue summary)

### 🛒 Cart & Orders
	•	Add / remove items from cart
	•	Checkout page
	•	Order creation with stock validation
	•	Orders list & detailed view
	•	Seller order management

### 💳 Payments
	•	Mock payment gateway
	•	Simulated success/fail callbacks
	•	Each order has a connected Payment model

### 🔐 Authentication
	•	Login / Signup with phone number + OTP
	•	No username/email required
	•	Session-based secure login
	•	Separate dashboards: customer vs seller

### 🖥️ UI / Frontend
	•	Fully responsive (Bootstrap 5)
	•	Modern black navbar
	•	Home hero banner
	•	Clean product cards
	•	RTL (Persian) support
	•	Custom CSS & IranSans font integration

### 🗂️ Tech Stack
	•	Django 5
	•	Python 3.12
	•	Bootstrap 5.3
	•	PostgreSQL (recommended)
	•	Session-based cart
	•	Class-based views
	•	Static & media handling

⸻

## 📁 Project Structure

DigiStore/
│
├── digistore/
│   ├── settings.py
│   ├── urls.py
│   └── wsgi.py
│
├── apps/
│   ├── account/     # OTP auth, login, signup
│   ├── home/        # Homepage, about
│   ├── product/     # Products & categories
│   ├── store/       # Seller stores
│   ├── cart/        # Shopping cart
│   ├── orders/      # Orders, checkout
│   ├── payments/    # Mock payments
│   └── dashboard/   # Seller & customer dashboards
│
├── templates/
│   ├── base.html
│   ├── home/
│   ├── product/
│   ├── dashboard/
│   └── includes/
│
├── static/
│   ├── css/style.css
│   ├── images/logo.png
│   └── images/banner.png
│
└── manage.py

⸻

## ⚙️ Installation & Setup

### 1️⃣ Clone the repository
    
    git clone https://github.com/mohamad-mgn/DigiStore.git
    cd DigiStore

### 2️⃣ Create Virtual Environment
    
    python3 -m venv venv
    source venv/bin/activate

### 3️⃣ Install Dependencies
    
    pip install -r requirements.txt

### 4️⃣ Apply Migrations
    
    python manage.py makemigrations
    python manage.py migrate

### 5️⃣ Create Superuser
    
    python manage.py createsuperuser

### 6️⃣ Run Development Server

    python manage.py runserver

⸻

## 🧪 Testing Login & OTP

The project uses phone-based OTP authentication.

Flow:
	1.	Enter phone number
	2.	Receive OTP (mocked, shown in console)
	3.	Login instantly without password

⸻

## 🧾 URL Structure

| Section              | URL                      |
|----------------------|--------------------------|
| Home                 | /                        |
| About                | /about/                  |
| Products             | /product/                |
| Product detail       | /product/<slug>/         |
| Cart                 | /cart/                   |
| Checkout             | /orders/checkout/        |
| Dashboard (customer) | /dashboard/customer/     |
| Dashboard (seller)   | /dashboard/seller/       |
| Payment mock page    | /payments/mock-pay/<id>/ |

⸻

## 🛠️ Future Improvements
	•	Real payment gateway (ZarinPal / Stripe)
	•	Product reviews & ratings
	•	Coupon system
	•	Advanced seller analytics
	•	React or Vue frontend
	•	Docker deployment

⸻

## 📸 Screenshots (Optional)

You can add images like this:

    ![Home Page](static/images/banner.png)
    ![Navbar](static/images/logo.png)

⸻

## 🧑‍💻 Author

Mohammad Moghanloo
DigiStore Project — 2025

⸻

## ⭐ Contribution

Pull requests are welcome.
If you like this project, please give it a star ⭐ on GitHub!