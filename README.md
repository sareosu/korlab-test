# 📝 Django Blog Application

A simple blog application built with Django, allowing registered users to create, edit, and delete posts, and leave comments on them.

## 🔧 Features

- User registration and login/logout
- Profile page with editable full name and password
- Create, edit, delete personal blog posts
- Leave comments under any post
- Comments tied to post and author
- Posts and comments visible to all users
- Basic Bootstrap-based UI

## 📁 Project Structure
app/
├── blog/ # Blog app (models, views, urls, templates)
│ ├── templates/ # Shared templates (base.html, etc.)
│ ├── urls.py # App-level URLs
│ ├── views.py
│ └── models.py
├── manage.py
└── app/ # Project config (settings.py, urls.py, etc.)
  └── static/ # Static CSS/JS files
