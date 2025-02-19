# Flask Multi-User Database System

## Overview
This Flask application allows users to register, log in, and have their own dedicated SQLite database. Each user gets a unique database created dynamically upon registration.

## Features
- User authentication (Login & Registration)
- A central database (`main_users.db`) to manage user credentials
- A separate SQLite database for each user, named dynamically
- A simple dashboard displaying user-specific data
- Flask session management for user authentication

## Installation
### Prerequisites
Ensure you have Python installed, along with `pip`.

### Install dependencies
Run the following command to install required packages:
```bash
pip install flask flask-sqlalchemy
```

## Running the Application
1. Save the script as `app.py`
2. Run the script using:
   ```bash
   python app.py
   ```
3. Open `http://127.0.0.1:5000` in your web browser.

## Application Structure
- `app.py`: The main application file.
- `main_users.db`: Stores registered user credentials.
- `user_<username>.db`: Dynamically created per user.

## How It Works
1. **User Registration/Login**
   - If the username exists, authentication occurs.
   - If new, a dedicated database is created.
2. **Dashboard**
   - Displays user's unique database and stored notes.
3. **Logout**
   - Clears session data and redirects to login.

## Routes
| Route        | Method | Description |
|-------------|--------|-------------|
| `/`         | GET/POST | Login/Register users |
| `/dashboard` | GET    | Displays user-specific data |
| `/logout`   | GET    | Logs the user out |

## Security Considerations
- **Use password hashing**: Currently, passwords are stored in plaintext.
- **Session security**: Use strong secret keys and session expiration.

## Future Enhancements
- Add password hashing (`werkzeug.security`)
- Implement user role-based access
- Integrate with a frontend framework for better UI

