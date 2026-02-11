# 🔌 EV Charging & Payment Aggregator Platform

A unified mobile and web solution that addresses payment fragmentation in Electric Vehicle (EV) charging infrastructure by consolidating multiple service providers into a single, seamless platform.

![React Native](https://img.shields.io/badge/React_Native-20232A?style=for-the-badge&logo=react&logoColor=61DAFB)
![Python](https://img.shields.io/badge/Python-3776AB?style=for-the-badge&logo=python&logoColor=white)
![FastAPI](https://img.shields.io/badge/FastAPI-009688?style=for-the-badge&logo=fastapi&logoColor=white)
![Firebase](https://img.shields.io/badge/Firebase-FFCA28?style=for-the-badge&logo=firebase&logoColor=black)
![Stripe](https://img.shields.io/badge/Stripe-008CDD?style=for-the-badge&logo=stripe&logoColor=white)

## 🎯 Problem Statement

EV drivers face significant challenges:
- **Payment Fragmentation**: Multiple apps and accounts required for different charging networks
- **Discovery Issues**: Difficulty finding available charging stations with compatible connectors
- **Inconsistent Experience**: Each provider has different payment flows and user interfaces
- **Transaction Tracking**: No unified history across different charging services

## 🚀 Solution

This platform provides a **single aggregator interface** that unifies:
- Real-time station discovery with availability tracking
- One-click payment across all charging providers
- Centralized transaction history
- Seamless connector compatibility filtering

## ✨ Key Features

### 📍 Real-Time Station Discovery
- **Google Maps Integration**: Interactive map showing all nearby charging stations
- **Live Availability**: Real-time status updates for each charging point
- **Smart Filtering**: Filter by connector type (CCS, CHAdeMO, Type 2, Tesla)
- **Station Details**: Pricing, amenities, and provider information

### 💳 Unified Payment Gateway
- **Stripe Integration**: Secure, PCI-compliant payment processing
- **One-Click Checkout**: Save payment methods for instant transactions
- **Multi-Provider Support**: Single wallet works across all charging networks
- **Transaction History**: Complete record of all charging sessions

### 🔄 Real-Time Synchronization
- **Live Status Updates**: Firebase real-time database for instant availability changes
- **Session Monitoring**: Track active charging sessions in real-time
- **Push Notifications**: Alerts for charging completion and payment confirmations

### 🎨 Responsive Dashboard
- **Mobile App**: React Native cross-platform application (iOS & Android)
- **Web Interface**: Progressive web app for desktop and mobile browsers
- **User Profiles**: Manage vehicles, payment methods, and preferences
- **Analytics**: Charging history, spending insights, and carbon savings

## 🏗️ Architecture

```
┌─────────────────────────────────────────────────────────┐
│                   Frontend Layer                         │
│  ┌──────────────────────┐  ┌──────────────────────────┐ │
│  │  React Native App    │  │   Web Dashboard (React)  │ │
│  │  (iOS & Android)     │  │   (Progressive Web App)  │ │
│  └──────────────────────┘  └──────────────────────────┘ │
└─────────────────────────────────────────────────────────┘
                            │
                    ┌───────▼────────┐
                    │   REST API     │
                    │   (FastAPI)    │
                    └───────┬────────┘
                            │
        ┌───────────────────┼───────────────────┐
        │                   │                   │
┌───────▼────────┐  ┌──────▼──────┐  ┌─────────▼─────────┐
│  Firebase DB   │  │ Stripe API  │  │  Provider APIs    │
│  (Real-time)   │  │  (Payment)  │  │  (ChargePoint,    │
│                │  │             │  │   EVgo, etc.)     │
└────────────────┘  └─────────────┘  └───────────────────┘
```

## 📂 Project Structure

```
ev-charging-platform/
├── mobile/                      # React Native mobile app
│   ├── src/
│   │   ├── components/         # Reusable UI components
│   │   ├── screens/            # App screens
│   │   ├── navigation/         # Navigation configuration
│   │   ├── services/           # API services
│   │   ├── utils/              # Utility functions
│   │   └── App.js
│   ├── android/
│   ├── ios/
│   └── package.json
│
├── backend/                     # FastAPI Python backend
│   ├── app/
│   │   ├── api/                # API endpoints
│   │   │   ├── routes/
│   │   │   └── dependencies.py
│   │   ├── core/               # Core configurations
│   │   │   ├── config.py
│   │   │   └── security.py
│   │   ├── models/             # Data models
│   │   ├── services/           # Business logic
│   │   │   ├── firebase_service.py
│   │   │   ├── stripe_service.py
│   │   │   ├── maps_service.py
│   │   │   └── provider_aggregator.py
│   │   └── main.py
│   ├── requirements.txt
│   └── Dockerfile
│
├── web/                         # React web dashboard (optional)
│   ├── src/
│   └── package.json
│
├── docs/                        # Documentation
│   ├── API.md
│   ├── SETUP.md
│   └── DEPLOYMENT.md
│
├── .env.example
├── docker-compose.yml
└── README.md
```

## 🛠️ Tech Stack

### Frontend
- **React Native**: Cross-platform mobile development
- **React Navigation**: Screen navigation and routing
- **React Native Maps**: Google Maps integration
- **Axios**: HTTP client for API requests
- **React Context API**: State management
- **Stripe React Native SDK**: Payment processing

### Backend
- **FastAPI**: High-performance Python web framework
- **Firebase Admin SDK**: Real-time database and authentication
- **Stripe Python SDK**: Payment gateway integration
- **Google Maps Platform**: Geocoding and Places API
- **Uvicorn**: ASGI server
- **Pydantic**: Data validation
- **SQLAlchemy**: Database ORM (for persistent data)
- **Redis**: Caching layer

### Infrastructure
- **Docker**: Containerization
- **Docker Compose**: Multi-container orchestration
- **Firebase**: Real-time database and hosting
- **Heroku/AWS**: Backend deployment
- **Expo**: React Native build and deployment

## 🚦 Getting Started

### Prerequisites

- Node.js (v16+)
- Python 3.9+
- Firebase Account
- Stripe Account
- Google Cloud Platform Account (Maps API)
- React Native development environment


### Backend Setup

```bash
cd backend

# Create virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Run migrations
alembic upgrade head

# Start development server
uvicorn app.main:app --reload
```

The API will be available at `http://localhost:8000`

### Mobile App Setup

```bash
cd mobile

# Install dependencies
npm install

# iOS setup (Mac only)
cd ios && pod install && cd ..

# Run on iOS
npm run ios

# Run on Android
npm run android
```

### Web Dashboard Setup (Optional)

```bash
cd web

# Install dependencies
npm install

# Start development server
npm start
```


## 🔐 Security Features

- JWT-based authentication
- HTTPS/TLS encryption
- Stripe PCI compliance
- Firebase security rules
- API rate limiting
- Input validation and sanitization
- CORS configuration
- Environment variable protection

## 🧪 Testing

```bash
# Backend tests
cd backend
pytest

# Frontend tests
cd mobile
npm test
```
 Membership subscriptions

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.



what else to change/remove
