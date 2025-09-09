🎬 Movie Review App (Django + DRF)






A full-stack Movie Review application built with Django and Django REST Framework. Users can browse movies, submit reviews, and manage their profiles. Authenticated users can edit or delete their own reviews. The project integrates an external movie API for enriched movie data.

👨‍💻 Project Overview

Author: Yeabsira Samuel
Date: 08/03/2025
Capstone Project: Software Engineering

This project demonstrates the ability to build a functional web application backend with authentication, CRUD operations, and API integration. Users can explore a database of movies, leave reviews, and interact with a modern RESTful API.

🌟 Features
✅ Authentication & Authorization

User registration and login

JWT-based session management

Protected endpoints for creating, updating, or deleting reviews

🎥 Movies

List all movies with search and filter functionality

Detailed view of individual movies

Publicly viewable information: title, genre, description, release date, director

📝 Reviews

Authenticated users can create reviews for movies

Users can edit or delete their own reviews only

Fields: movie, user, rating (1–5), comment, timestamp

🔍 Filtering & Search

Filter movies by genre, release year, or director

Search movies by title or description

⚡ API Endpoints
Endpoint	Method	Description
/api/movies/<id>/reviews/	GET	List all reviews for a movie
/api/movies/<id>/reviews/create/	POST	Create a review for a movie
/api/reviews/<id>/update/	PUT	Update a review (user only)
/api/reviews/<id>/delete/	DELETE	Delete a review (user only)
📊 Tech Stack

Backend: Django, Django REST Framework

Authentication: JWT (via DRF SimpleJWT)

Database: SQLite (local), PostgreSQL (production-ready)

Hosting: PythonAnywhere / Render / Railway

API Docs: DRF browsable API

🏗 Project Workflow

Initialize Django project Movie and create MySQL/SQLite database Movie Muse.

Implement user authentication (JWT, login/signup).

Create models for Movie, Review, and User.

Integrate external movie API for ratings, trailers, and posters.

Build REST API endpoints for:

Movie browsing & searching

Review creation, editing, deletion

User profile management

Implement frontend using Django templates connected to the API.

Test application thoroughly for bugs and edge cases.

Deploy on PythonAnywhere or Render.

🗂 Database Models
Movie
class Movie(models.Model):
    title = models.CharField(max_length=255)
    genre = models.CharField(max_length=100)
    description = models.TextField()
    release_date = models.DateField()
    director = models.CharField(max_length=100)

Review
class Review(models.Model):
    movie = models.ForeignKey(Movie, on_delete=models.CASCADE, related_name='reviews')
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    rating = models.IntegerField(validators=[MinValueValidator(1), MaxValueValidator(5)])
    comment = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

🚀 Deployment Plan

Use GitHub for version control

Configure settings.py for production:

Set ALLOWED_HOSTS

Use .env for secret keys and sensitive config

Deploy to PythonAnywhere / Render / Railway

Optional: Configure PostgreSQL for production

📄 Deliverables

GitHub repository with full Django project

Deployed backend link (API URL)

Postman Collection or Swagger API documentation

README.md with setup and usage instructions

Optional: Short video demo or screenshots of API in action

🌟 Stretch Goals (Optional)

Upload movie posters via ImageField

User profile avatars

Tag-based filtering (genres, tags)

Rate limiting / throttling

📌 How to Run Locally
# Clone repository
git clone https://github.com/Yroyzan/Movie_Review.git
cd Movie_Review

# Create virtual environment
python -m venv venv
source venv/bin/activate  # Linux/Mac
venv\Scripts\activate     # Windows

# Install dependencies
pip install -r requirements.txt

# Apply migrations
python manage.py migrate

# Create superuser (admin)
python manage.py createsuperuser

# Run development server
python manage.py runserver

🎨 Screenshots

(You can add screenshots of your frontend or API responses here)

📫 Contact

Author: Yeabsira Samuel
GitHub: https://github.com/Yroyzan

Email: yeabsirasamueladmasu25@gmail.com
