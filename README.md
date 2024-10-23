# 🌐 Social Connect API


This project is a **social media backend** built using Flask and Flask-SocketIO. It utilizes **Google OAuth** for authentication, enabling users to log in using their Google accounts. The application features user authentication, profile management, content creation, interactions (such as likes and comments), and real-time notifications. It is containerized using Docker for seamless development and production deployments, and it uses **PostgreSQL** as the database for data storage.



----------

## 📋 Table of Contents

1.  [Features](#features)
2.  [Installation and Setup](#installation-and-setup)
3.  [API Endpoints](#api-endpoints)
4.  [Running with Docker](#running-with-docker)
5.  [Development](#development)
6.   [Todo](#Todo)
7.  [License](#license)
8.  [Contact](#contact)

----------

## 🚀 Features

-   **OAuth 2.0 Authentication**: Users can authenticate via Google accounts.
-   **Profile Management**: Create, update, and delete profiles, with privacy settings (public or private).
-   **Post Creation**: Users can post text, images, or videos, and mention users or use hashtags.
-   **Interactions**: Like, comment on posts, and trigger notifications for user interactions.
-   **Real-Time Notifications**: Powered by WebSockets to deliver notifications for likes, comments, and follows instantly.
-   **PostgreSQL Database**: Uses PostgreSQL for data storage.
-   **Dockerized**: The entire application is containerized for consistent development and production environments.

----------

## 🛠️ Installation and Setup

### 1. Clone the Repository

```bash
git clone https://github.com/yourusername/social-connect-api.git
cd social-connect-api` 
```
### 2. Set Environment Variables

Create a `.env` file in the project root with the following variables:

```bash
SECRET_KEY=your_secret_key
DATABASE_URL=postgresql://username:password@db:5432/db_name
JWT_SECRET_KEY=your_jwt_secret_key
GOOGLE_REDIRECT_URI=your-redirect-url
```
# OAuth credentials
```
GOOGLE_CLIENT_ID=your_google_client_id
GOOGLE_CLIENT_SECRET=your_google_client_secret`
GOOGLE_CLIENT_REDIRECT=redirect-url

```
Make sure you have PostgreSQL set up and the database created before running the application.

----------

## 🐳 Running with Docker Compose

To run the application and database using Docker Compose:

### 1. Build and Run the Docker Containers

```bash
docker-compose up --build` 
```
This command will start both the Flask application and the PostgreSQL database, as defined in the `docker-compose.yml`. The app will be running at `http://localhost:5000`.

### 2. Make and Apply Migrations

Once the containers are running, create migrations for the database models:

```bash
`docker-compose exec web flask db migrate` 
```
Then apply the migrations:

```bash
`docker-compose exec web flask db upgrade` 
```
This will ensure the database schema is up-to-date with your application models.

----------

Guide to use **Postman** for testing WebSocket connections, including connecting to your Flask-SocketIO application []

## 📡 API Endpoints

### **User Authentication**

-   `GET /`: Redirect to login page.
-   `GET /login`: Login with Google OAuth.
-   `GET /auth/callback`: Callback route for handling Google authentication.
-   `GET /profile`: Retrieve user profile information.
-   `GET /logout`: Logout and clear session.
### **Profile Management**

-   `GET /profiles/<user_id>`: Retrieve profile details.
-   `PUT /profiles/<user_id>`: Update user profile.
-   `DELETE /profiles/<user_id>`: Delete user profile.
-   `POST /profiles/<user_id>/follow`: Follow a user.
-   `POST /profiles/<user_id>/unfollow`: Unfollow a user.

### **Post Creation**

-   `POST /posts`: Create a new post (text, images, or videos).
-   `GET /posts`: Retrieve posts based on followed users.
-   `POST /posts/<post_id>/like`: Like a post.
-   `POST /posts/<post_id>/comment`: Comment on a post.

### **Notifications**

-   `GET /notifications`: Retrieve user notifications.
-   `POST /notifications/<notification_id>/read`: Mark notification as read.

----------

## 🧑‍💻 Development

For development, you can also run the application without Docker:

1.  Install Python dependencies:
    
   ``` bash
    python -m venv venv
    source venv/bin/activate
    pip install -r requirements.txt` 
   ```
2.  Set up environment variables (as mentioned above).
    
3.  Ensure PostgreSQL is installed, running, and that you’ve created a database.
    
4.  Run database migrations:
    
   ``` bash
    flask db upgrade` 
   ```
5.  Run the application:
    
   ```bash
    flask run` 
   ```

----------

### 📝TODO List

1.  **🧪 Testing**
    
    -   Write tests for:
        -  [ ]  Authentication
        -   [ ]  User management
        -  [ ]   Post creation
        -   [ ]  Notifications
2.  **🔄 CI/CD Integration**
    
    - [ ]   Implement CI/CD for automated testing and deployment.

## 📜 License

This project is licensed under the MIT License - see the LICENSE file for details.

----------

## 📧 Contact

For any inquiries or issues, please reach out to labanrotich6544@gmail.com.