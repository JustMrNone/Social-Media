# Network Application

<div align="center">
  <a><img src="https://justmrnone.github.io/NeverEndingPong/repersentation/social.png" width="100%"></a>
</div>

A **social network application** built with Django that allows users to register, create posts, follow others, and interact through likes and comments.

---

## Features

- **User Registration, Login, and Logout**
- **Password Validation** and Email Uniqueness Checks
- **User Search** Functionality
- **Post Creation**, Editing, and Deletion
- **Commenting** on Posts
- **Following** and Unfollowing Users
- **Liking** and Unliking Posts
- **User Profile Management** with Profile Picture Upload
- **Pagination** for Posts

---

## Requirements

- Python 3.x
- Django 3.2
- Additional dependencies are listed in `requirements.txt`

---

## Usage

### 1. **User Registration and Login**

- **Register**: Fill out the registration form. Password must meet the validation criteria.
- **Login**: Use your username and password to log in to the platform.

### 2. **Creating and Managing Posts**

- **Create**: Add a new post directly from the homepage.
- **Edit**: Update or modify your existing posts.
- **Delete**: Remove posts if needed.
- **Comment**: View posts and add comments to any post.

### 3. **Following Users**

- **Search**: Look for users using the search functionality.
- **Follow/Unfollow**: Follow or unfollow users from their profile page.
- **Following Page**: View posts only from users you're following on the dedicated "Following" page.

### 4. **Liking Posts**

- **Like/Unlike**: Like or unlike any post with a simple click.
- **Like Count**: Each post displays the total number of likes it has received.

### 5. **Editing Profile**

- **Profile Management**: Update your profile information and upload a profile picture.

---

## Configuration

The application uses Django settings for various configuration options. Some important settings to consider:

- **`MAX_REGISTRATION_ATTEMPTS`**: Set the maximum number of allowed registration attempts from a single IP address.
- **`REGISTRATION_ATTEMPT_TIMEOUT`**: Define the timeout duration (in seconds) for registration attempts.
- **`LOGIN_ATTEMPT_TIMEOUT`**: Set the timeout duration (in seconds) for login attempts.

These configurations should be added or adjusted in your `settings.py` file.

---

## Project Structure

- **`network/`**: Contains the core Django app, including models, views, forms, and templates.
- **`static/`**: Holds all static files such as CSS, JavaScript, and images.
- **`templates/`**: Includes all HTML templates for the application.

---

This layout makes the app’s purpose, features, and structure clearer while keeping it concise and easy to read. You could also link to your `requirements.txt` or other project-related files if needed.
