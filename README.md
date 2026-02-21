# Demonstration video
Link: https://drive.google.com/file/d/1vFbiQcCAfYawr-lbI0JINvEq0YuOXXZs/view?usp=sharing


# Campus Lost & Found 🎓

A centralized platform for college campuses and organizations to report and find lost items. Students and staff can post lost items with their contact details, making it easy for finders to reach out directly.

## 📋 Problem Statement

Educational campuses and offices lose countless items daily - from water bottles and wallets to ID cards and electronics. Currently, there's no centralized system to track lost items, leading to:

- ❌ Valuable items never being recovered
- ❌ No way to contact owners when items are found
- ❌ Lost & found boxes becoming black holes
- ❌ Frustration for students and staff

## 💡 Solution

Campus Lost & Found provides a dedicated platform where:
- **Organization admins** can list their college/office
- **Students/Staff** can join their organization and post lost items with contact details
- **Finders** can directly call the owner using the provided phone number
- Items can be marked as resolved when found

## 🏗️ System Architecture

## 🛠️ Tech Stack

### Frontend
- **React 18** - UI library
- **Vite** - Build tool and dev server
- **Tailwind CSS** - Styling
- **React Router DOM** - Navigation
- **Axios** - API calls
- **React Hot Toast** - Notifications
- **Heroicons** - Icons
- **Headless UI** - UI components

### Backend
- **Flask** - Python web framework
- **Flask-PyMongo** - MongoDB integration
- **Flask-JWT-Extended** - Authentication
- **Flask-CORS** - Cross-origin resource sharing
- **Werkzeug** - Password hashing
- **Python-dotenv** - Environment variables

### Database
- **MongoDB** - NoSQL database
- **PyMongo** - MongoDB driver for Python

## ✨ Features

### For Organization Admins
- Register organization (college/office)
- View and edit organization details
- Simple, focused dashboard

### For Students & Staff
- Register with organization selection
- Post lost items with:
  - Title and description
  - Category
  - Location
  - Date
  - Phone number (mandatory)
- View all lost items in their organization
- Mark their items as resolved
- Delete their posts
- Direct call button to contact item owners

### Core Features
- 🔐 JWT Authentication
- 👥 Role-based access (Admin/User)
- 🏢 Multi-tenant data isolation
- 📱 Responsive design
- 🔔 Toast notifications
- 📞 Click-to-call functionality

## 🚀 Installation & Setup

### Prerequisites
- Python 3.8+
- Node.js 16+
- MongoDB

### Backend Setup

```bash
# Clone the repository
git clone <repository-url>
cd lost-found-backend

# Create virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Create .env file
echo "MONGO_URI=mongodb://localhost:27017/lost_found_db
JWT_SECRET_KEY=your-super-secret-key-here-make-it-long
DEBUG=True
PORT=5000" > .env

# Start MongoDB
# On macOS: brew services start mongodb-community
# On Ubuntu: sudo systemctl start mongodb

# Run the server
python app.py
```

### Frontend Setup


```bash
# Open new terminal
cd frontend

# Install dependencies
npm install

# Start development server
npm run dev

```

🎯 User Flows
Organization Admin Flow

1. Register as Organization
2. Fill organization details
3. Login to dashboard
4. View/edit organization information

Student/Staff Flow

1. Register as User
2. Select organization from dropdown
3. Login to dashboard
4. Post lost items with contact number
5. View all lost items in organization
6. When item found: Mark as resolved or delete
7. Others can call the posted number


🔒 Security Features

JWT-based authentication

Password hashing with bcrypt

Organization-level data isolation

Protected routes

Input validation

CORS configured

🎨 UI Features

Clean, modern design

Responsive for mobile/tablet/desktop

Toast notifications for feedback

Loading states

Empty states with guidance

Click-to-call buttons

Status badges (LOST/RESOLVED/YOUR POST)

🤝 Contributing

Fork the repository

Create a feature branch

Commit your changes

Push to the branch

Open a pull request