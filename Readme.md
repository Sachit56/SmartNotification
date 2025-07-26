# Smart Notification System

## Overview
This is a Django-based Smart Notification System built with Django and Django REST Framework. It allows users to receive notifications triggered by events (new comment, new login, weekly summary,new subscribers) through preferred channels (in-app, mocked email, mocked SMS). The system includes RESTful APIs for managing notifications, user preferences, and event triggers, with role-based permissions and delivery status tracking. Authentication is handled via Simple JWT with register and login views, SQLite is used as the database, and WebSocket support is included for real-time in-app notifications. The application is dockerized for easy deployment.

## Setup Instructions
### Prerequisites
- Docker
- Docker Compose
- Python
- SQLite

### Installation
1. **Clone the repository**:
   ```bash
   git clone git@github.com:Sachit56/SmartNotification.git
   cd SmartNotification
   ```

2. **Database**:
   - One can use the given sqlite database.

3. **Build and run the application**:
   ```bash
   docker compose up
   ```
   This command builds the Docker images and starts the application, including the Django server and WebSocket support.

4. **Access the app**:
   - API: `http://127.0.0.1:8000/api/v1/notifications/`
   - Admin: `http://127.0.0.1:8000/admin/`
   - WebSocket: `ws://127.0.0.1:8000/ws/notifications/`

5. **Create a superuser (for admin access)**:
   In a new terminal, access the Docker container and create a superuser:
   ```bash
   docker exec -it <container_id> python manage.py createsuperuser
   ```
   Replace `<container_id>` with the name of the running Django container Id(for eg: `docker exec -it 038e2c5d55cf python3 manage.py createsuperuser`) .


## API Endpoints

The API provides endpoints for user,thread,comment and notification management, for more detailed one we can access use `Smart Notification.postman_collection.json` Postman collection in the repository itself. Below is a summary of the available endpoints:

  

### User Management

1.  **Register User**
-  **Method**: POST
-  **URL**: `/api/v1/notifications/register/`
-  **Description**: Registers a new user with details such as email, username, and password.
-  **Body**: Form-data (e.g., `email`, `username`, `password`)
-  **Response**: Returns a message `user created successfully` on successful registration (HTTP 201).

2.  **Login User**
-  **Method**: POST
-  **URL**: `/api/v1/notifications/login/`
-  **Description**: Authenticates a user and returns JWT access tokens and the user will get notified if they logged in using any other user agent than the previous ones.
-  **Body**: JSON (e.g., `{"username": "newuser", "password": "admin"}`)
-  **Response**: Returns `access_token` (HTTP 200).

  ### Thread Management

3.  **Threads**
-  **Method**: GET
-  **URL**: `/api/v1/notifications/threads/`
-  **Description**: Retrieves all the available threads.
-  **Authentication**: Bearer Token (JWT)
-  **Response**: Returns user details including `{ "threads : [{"title":"Post One"},{"title":"Post Two"}]"}` (HTTP 200).

4.  **Threads**
-  **Method**: POST
-  **URL**: `/api/v1/notifications/threads/`
-  **Description**: Creates a new thread.
-  **Authentication**: Bearer Token (JWT)
-  **Body**: `{"title":"New Post"}`
-  **Response**: Returns a created thread object and message `new thread created successfully` (HTTP 201).
  ### Thread Subscription

5.  **Thread Subscription**
-  **Method**: POST
-  **URL**: `/api/v1/notifications/thread-subscription/`
-  **Description**: Subscribes to the thread; a notification is also sent to subscribed users as per their preference.
-  **Authentication**: Bearer Token (JWT)
-  **Body**: `{"threads": 1}`
-  **Response**: Returns a message `Subcribed successfully` (HTTP 201).
  ### Notification Preference
6.  **Notification Preference**
-  **Method**: GET
-  **URL**: `/v1/notifications/preferences/`
-  **Description**: Retrieves the user's notification preference.
-  **Authentication**: Bearer Token (JWT)
-  **Response**: Returns a message`Preference has not been set yet.` else provides the user's preference(app,email,sms) (HTTP 201).

7.  **Notification Preference**
-  **Method**: POST
-  **URL**: `/v1/notifications/preferences/`
-  **Description**: Adds user's notification preference.
-  **Authentication**: Bearer Token (JWT)
-   **Body**: `{"preference":"sms"}`
-  **Response**: Returns a message `Preference Added successfully` (HTTP 201).

7.  **Notification Preference**
-  **Method**: PUT
-  **URL**: `/v1/notifications/preferences/`
-  **Description**: Update user's notification preference.
-  **Authentication**: Bearer Token (JWT)
-   **Body**: `{"preference":"app"}`
-  **Response**: Returns a message `Preference updated successfully` with the user's update preference object (HTTP 200).
 ### Notification
 8.  **Unread Notification**
-  **Method**: GET
-  **URL**: `/api/v1/notifications/unread/`
-  **Description**: Retrieves the user's unread notification.
-  **Authentication**: Bearer Token (JWT)
-  **Response**: Returns all the unread notifications (HTTP 200).

 9.  **Read Notification**
-  **Method**: POST
-  **URL**: `api/v1/notifications/read/`
-  **Description**: Reads all the user's unread notifications.
-  **Authentication**: Bearer Token (JWT)
- **Body**:`{"is_read": true}`
-  **Response**: Returns the message `Read all the notification.` on success. (HTTP 200).

 10.  **Notification History**
-  **Method**: GET
-  **URL**: `/api/v1/notifications/history/`
-  **Description**: Retrieves all the user's read and unread notifications.
-  **Authentication**: Bearer Token (JWT)
-  **Response**: Returns all the notifications (HTTP 200).
 ### Comment
 11.  **Comment**
-  **Method**: GET
-  **URL**: `api/v1/notifications/comments/{{thread_id}}/`
-  **Description**: Retrieves the comment's in thread if the user is subscribed; else, gets the appropriate message.
-  **Authentication**: Bearer Token (JWT)
-  **Response**: Returns all the comments in the thread if the user is subscribed (HTTP 200), else a message like`Please Subscribe to the thread first.` (HTTP 403).

 12.  **Comment**
-  **Method**: POST
-  **URL**: `api/v1/notifications/comments/{{thread_id}}/`
-  **Description**: Posts the comment in the thread if the user is subscribed; else, gets the appropriate message a notification is also sent to subscribed users as per their preference.
-  **Authentication**: Bearer Token (JWT)
- **Body**:`{"text":"very nice post"}`
-  **Response**: Returns a message`Comment posted successfully.` and the comment just posted in the thread if the user is subscribed (HTTP 200), else a message like`Please Subscribe to the thread first.` (HTTP 403).

 ### Weekly Report Generation
  13.  **Weekly Report**
-  **Method**: GET
-  **URL**: `/api/v1/notifications/report/{{thread_id}}/`
-  **Description**: Retrieves the thread's subscribers, ID, and comments posted on them in the last 7 days a notification is also sent to subscribed users as per their preference.
-  **Authentication**: Bearer Token (JWT)
-  **Response**: Returns all the thread IDs and total comments in the thread and total subscriptions in the given thread.

 ### Trigger Notification
 14.  **Trigger Notification**
-  **Method**: POST
-  **URL**: `api/v1/notifications/trigger/{{thread_id}}/`
-  **Description**: Posts the comment in the thread if the user is subscribed; else, gets the appropriate message and a notification is also sent to subscribed users as per their preference.
-  **Authentication**: Bearer Token (JWT)
- **Body**:`{"text":"very nice post"}`
-  **Response**: Returns a message`Comment posted successfully.` and the comment just posted in the thread if the user is subscribed (HTTP 200), else a message like`Please Subscribe to the thread first.` (HTTP 403).

### Importing the Postman Collection

1. Open Postman.
2. Click **Import** > **File** and select `Smart Notification.postman_collection.json`.
3. Update the base URL if your server runs on a different host or port.
4. For authenticated endpoints, replace the `token` in the Bearer Token field with a valid JWT obtained from the Login User endpoint.


### WebSocket for Real-Time Notifications
- Connect to `http://127.0.0.1:8000/api/v1/notifications/thread-socket/` after logging into the django admin.
- Then,create new user and use access token after which is provided after successful login to access all the endpoints. Notifications will be triggered on events(comments,subscriptions,login,report generation) and sent to the related or subscribed users using websocket if the user's preference is `app`.
- You can see the notification message in **console**.

## Features
- JWT-based user authentication (register & login)
- Role-based and Subscriber-based permission checks
- Notification delivery via:
  - In-app (WebSocket)
  - Mocked email (console)
  - Mocked SMS (console)
- User-configurable notification preferences
- Django Signals are used whenever events like new subscriptions and new comments are posted.
- Real-time notifications using Django Channels
- API endpoints to manage:
  - Notification history
  - Mark as read
  - Update preferences
  - Trigger events(Comment,Subscription,Login,Report Generation)
  - For recognizing new device when logging in, I have used user agent for now.If the user's useragent while logging in is different than before then,they will get notified.
- Delivery status tracking
- Dockerized for easy setup and deployment

## Desgin Descisions
- Desgin Decisons can be accessed in the repository itself with the name `Design_Decision.md` 

## Project Structure

```
Smart_Notification/
├── notifications/        # Main app for notifications
│   ├── models.py         # Notification and preferences models
│   ├── views.py          # API views
│   ├── serializers.py    # DRF serializers
│   ├── tasks.py          # Celery tasks
│   ├── consumers.py      # WebSocket consumer
|   ├── ....      
├── docker-compose.yml
├── Dockerfile
├── requirements.txt
├── manage.py
├── Design_Decision.md
├── db.sqlite3
├── ....
```

**Stop Containers**:
   - To stop and remove containers, run:
     ```bash
     docker compose down
     ```


