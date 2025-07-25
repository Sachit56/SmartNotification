# Smart Notification System

## Overview
This is a Django-based Smart Notification System built with Django 4.x and Django REST Framework. It allows users to receive notifications triggered by events (new comment, new login, weekly summary,new subscribers) through preferred channels (in-app, mocked email, mocked SMS). The system includes RESTful APIs for managing notifications, user preferences, and event triggers, with role-based permissions and delivery status tracking. Authentication is handled via Simple JWT with register and login views, SQLite is used as the database, and WebSocket support is included for real-time in-app notifications. The application is dockerized for easy deployment.

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

## API Documentation

You can test all API endpoints using the Postman collection in the same file structure.


### WebSocket for Real-Time Notifications
- Connect to `http://127.0.0.1:8000/api/v1/notifications/thread-socket/` after logging into the django admin.
- Then,create new user and use all the endpoints it notification will be triggered using websocket if the user's preference is `app`.
- You can see the notification message in **console**.

## Features
- JWT-based user authentication (register & login)
- Role-based and Subscriber-based permission checks
- Notification delivery via:
  - In-app (WebSocket)
  - Mocked email (console)
  - Mocked SMS (console)
- User-configurable notification preferences
- Real-time notifications using Django Channels
- API endpoints to manage:
  - Notification history
  - Mark as read/unread
  - Update preferences
  - Trigger events(Comment,Subscription,Login,Report Generation)
  - For recognizing new device when logging in, I have used user_agent for now.If the user's user_agent while logging in is different than before then,they will get notified.
- Delivery status tracking
- Dockerized for easy setup and deployment

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