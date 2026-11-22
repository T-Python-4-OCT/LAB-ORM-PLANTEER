# 🌱 Planteer — Plant Discovery & Management Platform

**Planteer** is a responsive, database-driven web application built with Django and Python. It provides a platform for discovering plants, exploring their characteristics and uses, sharing knowledge, and managing plant information.

Developed as part of the **Django ORM Lab at Tuwaiq Academy**, the project has been extended with authentication, image galleries, user profiles, comments, and a custom administration dashboard.

## ✨ Features

### 🌿 Plant Discovery
- Browse a collection of 120 real plants.
- Search plants by name and description.
- Filter plants by category and edibility.
- View detailed plant information and uses.
- Explore related plants from the same category.
- View plant photographs and interactive image galleries.

### 🔐 Authentication & Profiles
- User registration, login, and logout.
- Personal user profiles.
- Create, update, and delete owned plants.
- Browse plants added by each user.
- Secure access to administrative functionality.

### 📸 Plant Management
- Create and edit plants with descriptive information.
- Upload a main cover image.
- Upload and manage additional gallery images.
- Preview images before saving.
- Drag-and-drop image upload interface.
- Responsive, modern plant editor.

### 💬 Community & Contact
- Post comments on plant detail pages.
- Browse community discussions.
- Submit messages through the Contact Us page.

### 📊 Custom Admin Dashboard
- Overview of plants, users, comments, and contact messages.
- Manage plants and browse registered users.
- Search, filter, and paginate administrative records.
- Review and delete comments.
- Manage contact messages.
- Staff-only access controls.

## 🛠️ Tech Stack

| Technology | Purpose |
|---|---|
| Python | Backend programming |
| Django | Web framework and ORM |
| SQLite | Database |
| HTML5 | Page structure |
| CSS3 | Styling and responsive design |
| JavaScript | Interactive UI and image previews |
| Django Templates | Dynamic rendering and template inheritance |
| Git & GitHub | Version control |

## 📁 Project Structure

```text
LAB-ORM-PLANTEER_/
├── Planteer/           # Django project configuration
├── apps/
│   ├── core/           # Home and contact functionality
│   ├── plants/         # Plant models, views and forms
│   ├── accounts/       # Authentication and profiles
│   └── dashboard/      # Administrative dashboard
├── templates/          # HTML templates
├── static/
│   ├── css/            # Stylesheets
│   ├── js/             # JavaScript
│   └── images/         # Static images and icons
├── media/
│   └── plants/         # Plant covers and galleries
├── db.sqlite3
├── manage.py
├── requirements.txt
└── README.md
```

## 🚀 Installation & Setup

**1. Clone the repository**

```bash
git clone https://github.com/AAQ224/LAB-ORM-PLANTEER_.git
cd LAB-ORM-PLANTEER_
```

**2. Create a virtual environment**

```bash
python -m venv .venv
```

Activate it on Windows:

```powershell
.\.venv\Scripts\Activate.ps1
```

**3. Install dependencies**

```bash
pip install -r requirements.txt
```

**4. Apply database migrations**

```bash
python manage.py migrate
```

**5. Start the development server**

```bash
python manage.py runserver
```

Open the application at:

http://127.0.0.1:8000/

## 🔑 Demo Administrator Account

For the local development database only:

| Field | Value |
|---|---|
| Username | `admin` |
| Password | `123` |
| Admin Panel | `http://127.0.0.1:8000/admin/` |
| Custom Dashboard | `http://127.0.0.1:8000/dashboard/` |

**Security notice:** These are development credentials, not suitable for a public deployment. Change the administrator password before making the application accessible online. Never reuse these credentials in production.

## 📚 Django ORM Concepts

This project demonstrates:

- Django models and database migrations.
- CRUD operations.
- `ForeignKey` and model relationships.
- ORM queries, filtering, and searching.
- Django ModelForms and inline formsets.
- User authentication and permissions.
- Template inheritance.
- Static and media file management.
- Pagination and related-object queries.

## 🎓 Academic Context

**Program:** Web Development with Python  
**Academy:** Tuwaiq Academy  
**Project:** Django ORM Lab — Planteer

## 👨‍💻 Developer

**Abdulrahman Al-Qahtani**

GitHub: [@AAQ224](https://github.com/AAQ224)

---

*Built with Django, Python, and a passion for learning web development.* 🌱