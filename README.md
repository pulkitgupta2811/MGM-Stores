# MGM-Stores

A modern Django-based Point of Sale (POS) and Store management application.

## Getting Started

### 1. Prerequisites
- Python 3.10+ installed on your system.

### 2. Setup Virtual Environment
Create and activate a virtual environment at the root of the project:
```bash
python -m venv .venv

# On Windows (Command Prompt):
.venv\Scripts\activate

# On Windows (PowerShell):
.venv\Scripts\Activate.ps1

# On macOS/Linux:
source .venv/bin/activate
```

### 3. Install Dependencies
Install all requirements from the `requirements.txt` file:
```bash
pip install -r requirements.txt
```

### 4. Local Environment Configuration
Create a `.env` file at the root of the project (next to `manage.py`) with local defaults:
```env
SECRET_KEY=django-insecure-dummy-key-for-local-development-12345
DEBUG=True
EMAIL_HOST_USER=dummy_user@gmail.com
EMAIL_HOST_PASSWORD=dummy_password
```

### 5. Setup SQLite Database & Migrate
Run the migrations to create the SQLite database and initialize schemas:
```bash
python manage.py migrate
```

### 6. Seed Dummy Data
Seed the local SQLite database with realistic categories, products, test user accounts, orders, and programmatically generated image placeholders:
```bash
python manage.py seed_db
```

### 7. Run the Local Server
Start the Django development server:
```bash
python manage.py runserver
```
Open [http://127.0.0.1:8000/](http://127.0.0.1:800) in your web browser.

---

## Seeded Test Accounts

After running `python manage.py seed_db`, you can use the following accounts:

### 👤 Standard User Accounts
- **User 1**: Mobile `1234567890` | Password: `user123`
- **User 2**: Mobile `9876543210` | Password: `user123`

### 🔑 Admin/Staff Account
- **Admin**: Mobile `9999999999` | Password: `admin123`
- Admin Panel: [http://127.0.0.1:8000/admin](http://127.0.0.1:800/admin)
