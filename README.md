# Threads-like Social Network

A social network website built with Django that allows users to make posts, follow other users, and interact with posts through likes and comments. This project simulates a Threads-like social network experience.

## Features

- **User Authentication:** Register, login, and logout functionality
- **Post Creation:** Users can create and edit posts
- **Follow System:** Follow and unfollow other users
- **Like System:** Like and unlike posts
- **Pagination:** View posts with pagination
- **Profile Pages:** View user profiles with their posts and follow status

## Technology Stack

- **Backend:** Django
- **Frontend:** HTML, CSS, JavaScript, Bootstrap
- **Database:** SQLite (default in Django)

## Prerequisites

- Python 3.x
- Django

## Installation & Setup

1. **Clone the repository:**
   ```bash
   git clone <repository-url>
   cd network
   ```
2. **Create and activate a virtual environment:**
   ```bash
    python -m venv venv
    source venv/bin/activate  # On Windows use `venv\Scripts\activate`
   ```
4. **Install Django:**
   ```bash
   pip install django
   ```
   
5. **Install PostgreSQL:** Follow the instructions on the [PostgreSQL installation page](https://www.postgresql.org/download/).
   ```bash
    # Create a database and user:
    sudo -u postgres psql
    CREATE DATABASE network;
    CREATE USER networkuser WITH PASSWORD 'password';
    ALTER ROLE networkuser SET client_encoding TO 'utf8';
    ALTER ROLE networkuser SET default_transaction_isolation TO 'read committed';
    ALTER ROLE networkuser SET timezone TO 'UTC';
    GRANT ALL PRIVILEGES ON DATABASE network TO networkuser;
    \q
    ```
6. **Apply migrations:**
    ```bash
    python manage.py makemigrations
    python manage.py migrate
    ```
8. **Run the development server:**
   ```bash
    python manage.py runserver
    ```
9. **Acess the application:** 
    Open your browser and navigate to `http://127.0.0.1L8000` to view the application.
10. **Register for an account:**
    - Click on the "Register" link to create a new user account.
    - Fill in the required fields and submit the form.

## Application Structure

### Models
- **User Model:** Extends Django's AbstractUser for user authentication
- **Post Model:** Stores posts with user, content, and timestamp
- **Follow Model:** Stores follower and following relationships
- **Like Model:** Stores likes with user and post relationships

### Views
- **Authentication:**
  - `login_view`: Handles user login
  - `logout_view`: Handles user logout
  - `register`: Handles user registration

- **Post Management:**
  - `index`: Displays posts from followed users and self
  - `explore`: Displays all posts
  - `new_post`: Handles new post creation
  - `edit_post`: Handles post editing
  - `like_post`: Handles liking and unliking posts

- **User Management:**
  - `profile`: Displays user profile with posts and follow status
  - `follow`: Handles following users
  - `unfollow`: Handles unfollowing users
  - `following`: Displays posts from followed users

### Frontend
- **HTML Templates:** Uses Django templates for rendering HTML
- **CSS:** Uses Bootstrap for styling
- **JavaScript:** Handles dynamic content loading and interactions

## Usage

1. **Register for an account:** Click on the "Register" link to create a new user account.
   - Create a new account or log in with existing credentials

2. **Navigate the network:**
   - Click on the "Explore" link to view all posts
   - Click on the "Following" link to view posts from followed users
   - Click on the "Profile" link to view your profile and posts

3. **Create and manage posts:**
   - Click on the "New Post" link to create a new post
   - Edit or delete your posts from your profile page

4. **Follow and interact with users:**
   - Follow or unfollow users from their profile pages
   - Like or unlike posts from the explore or following pages

## Project Files

- **models.py:** Contains the database models for the application
- **views.py:** Contains the views for handling requests and rendering templates
- **urls.py:** Contains the URL routing for the application
- **templates/network:** Contains HTML templates for the application
- **static/network:** Contains static files (CSS, JavaScript) for the application

## Note

This application simulates a social network where users can interact with posts and follow other users. It is a safe environment for testing and learning web development concepts.