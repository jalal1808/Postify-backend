# Postify 📝

Postify is a simple **blogging platform** built with **Django REST Framework**.
It allows users to register, create posts, upload images, like and comment on posts.

---

## 🚀 Features

* User authentication (Register/Login)
* Create posts with title, content, and images
* Like and comment on posts
* View post statistics (likes & comments count)
* **AI-powered blog title suggestions** using **Google Gemini API**

---

## 🛠️ Tech Stack

* **Backend:** Django, Django REST Framework
* **Database:** PostgreSQL
* **Authentication:** JWT
* **AI Integration:** Gemini API (for title suggestions)

---

## ⚙️ Setup & Installation

1. **Clone the repository**

   ```bash
   git clone https://github.com/your-username/postify.git
   cd postify
   ```

2. **Create & activate virtual environment**

   ```bash
   python -m venv venv
   source venv/bin/activate   # macOS/Linux
   venv\Scripts\activate      # Windows
   ```

3. **Install dependencies**

   ```bash
   pip install -r requirements.txt
   ```

4. **Apply migrations**

   ```bash
   python manage.py migrate
   ```

5. **Run server**

   ```bash
   python manage.py runserver
   ```

---

## 📡 API Endpoints

### Authentication

* `POST /api/auth/register/` → Register
* `POST /api/auth/login/` → Login

### Posts

* `GET /api/posts/` → List posts
* `POST /api/posts/` → Create post (with optional images)
* `POST /api/posts/<id>/like/` → Like post
* `POST /api/posts/<id>/comment/` → Comment on post

### AI (Gemini)

* `POST /api/ai/title-suggestion/` → Get AI-generated blog title suggestion
