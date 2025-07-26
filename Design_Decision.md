# Design Decisions

## 1. API Structure
- The project uses Django REST Framework's `APIView` and generic views for clear separation of concerns.
- Each resource (Threads, Comments, Notifications, Preferences) has its own view class, making endpoints modular and maintainable.

## 2. Authentication & Permissions
- Used **Simple JWT** for stateless authentication and scalability.
- All sensitive endpoints require authentication (`IsAuthenticated`).
- Report generation and comment actions require users to be subscribed (`IsSubscribed` custom permission), ensuring only subscribed users can interact.

## 2. Database
- Used **SQLite**.
- **Postgresql** can be used too but i chose **SQLite** only because it's easy.

## 3. Data Serialization
- Custom serializers are used for each model, ensuring consistent and validated data exchange between client and server.

## 4. Notification System
- Notifications are triggered for key events (login from new device, weekly report requests, New comment posted in the thread, new subscribers in the thread).
- Notification preferences are respected, allowing users to choose how they receive alerts.
- If no preference is set by the users notification is sent in the app. 

## 5. Thread & Comment Management
- Threads and comments are linked via foreign keys, enabling efficient querying and aggregation.
- Only the users subscribed to the thread can post the comment and see the comment using **GET** request.
- Weekly reports use Django ORM annotations to count comments and subscriptions within a time window of 7 days, optimizing database access.

## 6. Django Signals
- Django signals such as `post_save` are used to trigger Celery tasks whenever a model action occurs (e.g., a new comment or a new subscription).
  This promotes **decoupled logic**, making the core application cleaner and more maintainable.
- Example: When a user posts a comment in thread `Notification` object is created via a signal, a Celery task is automatically triggered to deliver the notification based on the user’s preferences.

## 7. Database Transaction
- In our notification system, we trigger asynchronous tasks (e.g., Celery) to deliver notifications after a new Notification object is created.
- However, if the task is dispatched before the database transaction is committed, it can lead to issues like `Doesnot Exist`.
- To counter this issue, we used `transaction.on_commit()`.

## 8. Error Handling & Status Codes
- All API responses include appropriate HTTP status codes for clarity (e.g., 200 OK, 201 Created, 400 Bad Request, 403 Forbidden, 404 Not Found).
- Error messages are descriptive, aiding client-side debugging.

## 9. Extensibility
- The code is structured to allow easy addition of new features (e.g., new notification types, more thread actions).
- Use of related names in models supports efficient reverse lookups and future scalability.

## 10. WebSockets
- Integrated **Django Channels** to enable real-time notifications.
- Instead of group-based broadcasting (e.g., per-thread), the system sends **Individual WebSocket messages** to each connected subscriber.
- This ensures that notifications are sent **privately** and only to relevant users, improving security and message targeting.


## 11. Asynchronous Tasks
- Notification delivery is handled via **Celery** with **Redis** as the message broker to ensure non-blocking, scalable background processing.
- This architecture allows the system to efficiently handle multiple notification channels (in-app, email, SMS) without delaying the main request-response cycle.
- For example, when a user comments on a thread or requests a report, the notification dispatch process is offloaded to Celery.
- Task retries are supported using Celery’s built-in `max_retries` and `default_retry_delay`, ensuring robust delivery in case of temporary issues

## 12. Rate Limiting
- For avoiding spamming i used rate limiting all the views has limited request.
- For the anonymous users, i have set their rate for 20 per day and users's rate is 100 per day.

## 13. Security
- User actions are validated to prevent unauthorized access (e.g., only subscribed users can comment or request reports).
- Login records and device checks add an extra layer of security for user accounts.

---
*These decisions aim to balance maintainability, performance, and user experience for a scalable notification system.*