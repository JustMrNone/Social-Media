# Network

A social network application built with Django.

## Features

- User registration, login, and logout
- Password validation and email uniqueness checks
- User search functionality
- Post creation, editing, and deletion
- Commenting on posts
- Following and unfollowing users
- Liking and unliking posts
- User profile management with profile picture upload
- Pagination for posts

## Requirements

- Python 3.x
- Django 3.2
- Additional dependencies listed in `requirements.txt`

## Usage

### User Registration and Login

- Register a new user by filling out the registration form. Make sure your password meets the validation criteria.
- Log in using your username and password.

### Creating and Managing Posts

- Create a new post from the homepage.
- Edit or delete your posts as needed.
- View and add comments to posts.

### Following Users

- Search for other users and view their profiles.
- Follow or unfollow users directly from their profile pages.
- View posts from users you follow on the "Following" page.

### Liking Posts

- Like or unlike posts with a single click.
- View the total number of likes on each post.

### Editing Profile

- Edit your profile information and upload a profile picture.

## Configuration

The application relies on Django settings for configuration. Here are some important settings you might want to configure:

- `MAX_REGISTRATION_ATTEMPTS`: Maximum allowed registration attempts from a single IP address.
- `REGISTRATION_ATTEMPT_TIMEOUT`: Timeout for registration attempts cache in seconds.
- `LOGIN_ATTEMPT_TIMEOUT`: Timeout for login attempts cache in seconds.

These settings should be added in your `settings.py` file.

## Project Structure

- `network/`: Contains the Django app with models, views, forms, and templates.
- `static/`: Contains static files like CSS, JavaScript, and images.
- `templates/`: Contains HTML templates for the app.
