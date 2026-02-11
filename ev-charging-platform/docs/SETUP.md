# EV Charging Platform - Setup Guide

This guide will help you set up the EV Charging & Payment Platform on your local machine.

## Prerequisites

Before you begin, ensure you have the following installed:

- **Node.js** (v16 or higher) - [Download](https://nodejs.org/)
- **Python** (3.9 or higher) - [Download](https://python.org/)
- **Docker & Docker Compose** (optional but recommended) - [Download](https://www.docker.com/)
- **Git** - [Download](https://git-scm.com/)

## Required Accounts

You'll need to create accounts with these services:

1. **Firebase** - [console.firebase.google.com](https://console.firebase.google.com/)
2. **Stripe** - [dashboard.stripe.com](https://dashboard.stripe.com/)
3. **Google Cloud Platform** (for Maps API) - [console.cloud.google.com](https://console.cloud.google.com/)

## Step 1: Clone the Repository

```bash
git clone https://github.com/yourusername/ev-charging-platform.git
cd ev-charging-platform
```

## Step 2: Firebase Setup

### 2.1 Create Firebase Project

1. Go to [Firebase Console](https://console.firebase.google.com/)
2. Click "Add project"
3. Name your project (e.g., "EV Charging Platform")
4. Disable Google Analytics (optional)
5. Click "Create project"

### 2.2 Set up Realtime Database

1. In Firebase Console, go to "Build" → "Realtime Database"
2. Click "Create Database"
3. Select location (choose closest to your users)
4. Start in "Test mode" for development
5. Note the database URL (e.g., `https://your-project-default-rtdb.firebaseio.com`)

### 2.3 Generate Service Account Key

1. Go to Project Settings (gear icon) → "Service accounts"
2. Click "Generate new private key"
3. Save the JSON file as `firebase-credentials.json`
4. Move it to `backend/firebase-credentials.json`

### 2.4 Set up Security Rules (Production)

```json
{
  "rules": {
    "stations": {
      ".read": true,
      ".write": "auth != null"
    },
    "sessions": {
      "$sessionId": {
        ".read": "auth.uid == data.child('user_id').val()",
        ".write": "auth.uid == data.child('user_id').val()"
      }
    },
    "users": {
      "$userId": {
        ".read": "auth.uid == $userId",
        ".write": "auth.uid == $userId"
      }
    }
  }
}
```

## Step 3: Stripe Setup

### 3.1 Create Stripe Account

1. Sign up at [stripe.com](https://stripe.com)
2. Complete account verification

### 3.2 Get API Keys

1. Go to Developers → API keys
2. Copy your **Publishable key** (starts with `pk_test_`)
3. Copy your **Secret key** (starts with `sk_test_`)
4. Note: Use test keys for development

### 3.3 Set up Webhook (Optional)

1. Go to Developers → Webhooks
2. Click "Add endpoint"
3. Enter your URL: `https://yourdomain.com/api/payments/webhook`
4. Select events: `payment_intent.succeeded`, `payment_intent.payment_failed`
5. Copy the signing secret (starts with `whsec_`)

## Step 4: Google Maps Setup

### 4.1 Create Google Cloud Project

1. Go to [Google Cloud Console](https://console.cloud.google.com/)
2. Create a new project
3. Enable billing (required for Maps API)

### 4.2 Enable APIs

1. Go to "APIs & Services" → "Library"
2. Search and enable:
   - Maps JavaScript API
   - Places API
   - Geocoding API
   - Distance Matrix API
   - Directions API

### 4.3 Create API Key

1. Go to "APIs & Services" → "Credentials"
2. Click "Create Credentials" → "API key"
3. Copy your API key
4. Click "Restrict key" (recommended)
5. Set application restrictions (HTTP referrers for web, Android/iOS apps for mobile)
6. Set API restrictions to only the enabled APIs

## Step 5: Backend Setup

### 5.1 Navigate to Backend Directory

```bash
cd backend
```

### 5.2 Create Virtual Environment

```bash
# On macOS/Linux
python3 -m venv venv
source venv/bin/activate

# On Windows
python -m venv venv
venv\Scripts\activate
```

### 5.3 Install Dependencies

```bash
pip install -r requirements.txt
```

### 5.4 Configure Environment Variables

1. Copy the example env file:
```bash
cp ../.env.example .env
```

2. Edit `.env` with your values:
```env
# Firebase
FIREBASE_CREDENTIALS_PATH=./firebase-credentials.json
FIREBASE_DATABASE_URL=https://your-project-default-rtdb.firebaseio.com

# Stripe
STRIPE_SECRET_KEY=sk_test_your_secret_key
STRIPE_PUBLISHABLE_KEY=pk_test_your_publishable_key

# Google Maps
GOOGLE_MAPS_API_KEY=AIzaSy_your_api_key

# JWT
SECRET_KEY=generate_a_long_random_string_here

# Database (if using Docker, use these defaults)
DATABASE_URL=postgresql://postgres:password@localhost:5432/evcharging
```

### 5.5 Set up Database

#### Option A: Using Docker (Recommended)

```bash
# From project root
cd ..
docker-compose up -d db redis
```

#### Option B: Manual Installation

Install PostgreSQL and Redis, then create database:
```bash
createdb evcharging
```

### 5.6 Run Migrations

```bash
# If using Alembic (optional for advanced setups)
alembic upgrade head
```

### 5.7 Start Backend Server

```bash
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

The API will be available at `http://localhost:8000`
API documentation at `http://localhost:8000/api/docs`

## Step 6: Mobile App Setup

### 6.1 Navigate to Mobile Directory

```bash
cd mobile
```

### 6.2 Install Dependencies

```bash
npm install
```

### 6.3 Configure Environment

Create `.env` file in mobile directory:

```env
API_BASE_URL=http://localhost:8000/api
STRIPE_PUBLISHABLE_KEY=pk_test_your_publishable_key
GOOGLE_MAPS_API_KEY=AIzaSy_your_api_key
```

**Note:** For Android emulator, use `http://10.0.2.2:8000/api`
For iOS simulator, `http://localhost:8000/api` works fine

### 6.4 iOS Setup (Mac only)

```bash
cd ios
pod install
cd ..
```

### 6.5 Start the App

```bash
# Start Metro bundler
npm start

# In separate terminals:
# For iOS
npm run ios

# For Android
npm run android

# For Web
npm run web
```

## Step 7: Verify Installation

### 7.1 Test Backend

```bash
curl http://localhost:8000/health
```

Should return:
```json
{
  "status": "healthy",
  "version": "1.0.0",
  "service": "ev-charging-api"
}
```

### 7.2 Test Registration

```bash
curl -X POST http://localhost:8000/api/auth/register \
  -H "Content-Type: application/json" \
  -d '{
    "email": "test@example.com",
    "password": "password123",
    "name": "Test User"
  }'
```

### 7.3 Test Mobile App

1. Open the app on your device/emulator
2. Register a new account
3. Grant location permissions
4. You should see the map with nearby stations

## Docker Deployment (Alternative)

### Run Entire Stack with Docker

```bash
# From project root
docker-compose up -d
```

This will start:
- Backend API (port 8000)
- PostgreSQL (port 5432)
- Redis (port 6379)
- PgAdmin (port 5050)

Access services:
- API: http://localhost:8000
- API Docs: http://localhost:8000/api/docs
- PgAdmin: http://localhost:5050 (admin@evcharging.com / admin)

## Troubleshooting

### Common Issues

**1. Firebase Connection Error**
- Verify `firebase-credentials.json` path is correct
- Check Firebase Database URL in `.env`
- Ensure Firebase Realtime Database is created

**2. Stripe Payment Fails**
- Use test card: 4242 4242 4242 4242
- Check Stripe API keys are in test mode
- Verify publishable key matches secret key environment

**3. Google Maps Not Loading**
- Verify API key is correct
- Check billing is enabled on Google Cloud
- Ensure all required APIs are enabled

**4. Mobile App Can't Connect to Backend**
- iOS Simulator: Use `http://localhost:8000/api`
- Android Emulator: Use `http://10.0.2.2:8000/api`
- Physical Device: Use your computer's IP (e.g., `http://192.168.1.100:8000/api`)

**5. Database Connection Error**
- Ensure PostgreSQL is running
- Verify DATABASE_URL in `.env`
- Check credentials are correct

### Getting Help

- Check the [API documentation](http://localhost:8000/api/docs)
- Review logs: Backend terminal for API issues
- Enable debug mode: Set `DEBUG=True` in `.env`

## Next Steps

1. **Add Test Data**: Use the API docs to add test stations
2. **Configure Providers**: Add real charging provider API keys
3. **Customize UI**: Modify mobile app screens and styling
4. **Deploy**: See [DEPLOYMENT.md](./DEPLOYMENT.md) for production deployment

## Development Tips

### Useful Commands

```bash
# Backend
uvicorn app.main:app --reload --log-level debug

# Mobile - Clear cache
npm start -- --reset-cache

# Database - View tables
psql evcharging

# Redis - View cache
redis-cli
```

### Recommended Tools

- **Postman** - API testing
- **React Native Debugger** - Mobile debugging
- **Expo Go** - Quick mobile testing
- **PgAdmin** - Database management

## Security Notes

⚠️ **Important for Production:**

1. Change `SECRET_KEY` to a long, random string
2. Use production Stripe keys (starts with `sk_live_` and `pk_live_`)
3. Enable Firebase security rules
4. Restrict Google Maps API key
5. Use HTTPS for all endpoints
6. Set `DEBUG=False`
7. Configure CORS properly
8. Use strong database passwords

---

**Congratulations!** Your EV Charging Platform is now set up and ready for development. 🎉
