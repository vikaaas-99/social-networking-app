# Social Networking Application

This is a Django REST Framework project that implements a social networking API with functionalities for user signup, login, searching users, sending and managing friend requests.

## Features

- User signup/login with email
- User search by email or name (with pagination)
- Friend request system (send, accept, reject)
- List friends and pending friend requests
- Throttling applied for friend requests (max 3 requests per minute)

## Setup Instructions

1. **Clone the repository**:
    ```bash
    git clone https://github.com/vikaaas-99/social-networking-app.git
    ```

2. **Create Virtual Environment**:
   ```bash
   python -m venv venv
   ```

3. **Install dependencies**:
    - Using pip:
      ```bash
      pip install -r requirements.txt
      ```

4. **Run migrations**:
    ```bash
    python manage.py migrate
    ```

5. **Run the development server**:
    ```bash
    python manage.py runserver
    ```

6. **Using Docker**:
    - To run the application using Docker, simply run:
      ```bash
      docker-compose up --build
      ```

## API Endpoints

- **POST** `users/signup/` - User signup
- **POST** `users/login/` - User login
- **GET** `users/search/<query>&page=<page_number>` - Search users (paginated)
- **POST** `users/send-request/` - Send a friend request
- **POST** `users/respond-request/` - Accept or reject a friend request
- **GET** `users/friends-list/` - List friends
- **GET** `users/friend-requests/` - List pending friend requests

## Throttling

- **Friend Request Throttling**: Users are limited to sending 3 friend requests per minute.

## Postman Collection

A Postman collection with all API endpoints is available in the project. [Download here](https://github.com/vikaaas-99/social-networking-app/blob/8585f7e449fe643d449595347b51023435ab3fb3/Accuknox.postman_collection.json).

## Docker

This project is containerized using Docker. You can run the project with:
```bash
docker-compose up --build
```

## Created by

[![LinkedIn](https://img.shields.io/badge/LinkedIn-%40vikaas-%2Dsharma-blue)](https://www.linkedin.com/in/vikaas-sharma/)
[![GitHub](https://img.shields.io/badge/GitHub-%40vikaaas-%2D99-darkgrey)](https://github.com/vikaaas-99)
