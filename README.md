# Digital Invoice Intelligence (Smart Service Portal)

![Python](https://img.shields.io/badge/Python-3.14-blue.svg)
![Django](https://img.shields.io/badge/Django-6.0-green.svg)
![Bootstrap](https://img.shields.io/badge/Bootstrap-4.6-purple.svg)

A complete, dual-role electronic invoicing and service management system built with Django. Designed with a sleek, custom "Smart Blue Fusion" AdminLTE v3 interface, this portal streamlines field service operations by connecting technicians, administrators, and customers through automated workflows and OTP-verified invoicing.

## ✨ Features

### 👨‍💻 Admin Features
* **Smart Dashboard**: Dynamic, interactive Chart.js revenue analytics and quick-action metrics.
* **Excel Bulk Upload**: Ingest hundreds of `Product Inventories` and `Service Types` instantly via `.xlsx` parsing.
* **Database Management**: Fully custom, decoupled CRUD interfaces for Invoices, Technician Profiles, and Customer Feedbacks.
* **Global Search**: Instantly query invoices by Customer Name, Phone, or UUID.

### 🔧 Technician Features
* **Field Portal**: A streamlined, mobile-friendly interface to quickly generate invoices on the go.
* **Dynamic Search & Add**: Autocomplete parts and services with live pricing injection.
* **OTP Verification Workflow**: Invoices require a 4-digit OTP sent to the customer for status verification (Pending -> Verified).

### 👥 Customer Features
* **Digital Invoices**: Clean, printable HTML invoice summaries detailing parts, labor, and tax.
* **Feedback Engine**: A 5-point Likert scale feedback system (Behavior, Quality, Punctuality) unlocked only after OTP verification.

## 🛠️ Technology Stack
* **Backend**: Django (Python)
* **Frontend**: Bootstrap 4, AdminLTE v3, custom CSS styling
* **Database**: SQLite (Development)
* **Data Processing**: Pandas, OpenPyXL (Excel Ingestion)

## 🚀 Quick Start

### Prerequisites
* Python 3.8+
* pip package manager

### Installation

1. **Clone the repository**
   ```bash
   git clone https://github.com/YusraNoor332/digital-invoice-intelligence.git
   cd digital-invoice-intelligence
   ```

2. **Create and activate a virtual environment**
   ```bash
   python -m venv venv
   # On Windows
   venv\Scripts\activate
   # On macOS/Linux
   source venv/bin/activate
   ```

3. **Install dependencies**
   ```bash
   pip install django pandas openpyxl
   ```

4. **Apply database migrations**
   ```bash
   python manage.py makemigrations
   python manage.py migrate
   ```

5. **Create a superuser (Admin)**
   ```bash
   python manage.py createsuperuser
   ```

6. **Run the development server**
   ```bash
   python manage.py runserver
   ```

7. **Access the Application**
   * **Admin Login**: `http://127.0.0.1:8000/login/` (Route to `/admin/dashboard/`)
   * **Technician Login**: `http://127.0.0.1:8000/technician/login/`

## 📁 Project Structure

```
E_invoice_system/
├── E_invoice_system/      # Core settings and root URL routing
├── invoices/              # Main application module
│   ├── templates/         # Clean, modular HTML templates (Admin, Tech, Auth)
│   ├── static/            # CSS, JavaScript, AdminLTE assets
│   ├── views.py           # Custom view logic overriding native Django admin
│   ├── models.py          # Relational database models
│   ├── services.py        # Excel ingestion logic
│   └── urls.py            # App-level routing
└── manage.py              # Django execution script
```

## 🎨 Architecture Note
This project intentionally decouples from Django's native `admin/` module for database list views to enforce a strict, unified UI/UX. All database tables are rendered through custom views extending a unified `base.html` structure to prevent framework CSS interference.

## 📄 License
This project is licensed under the MIT License.
