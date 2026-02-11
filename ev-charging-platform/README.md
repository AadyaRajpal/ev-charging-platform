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

### Environment Variables

Create a `.env` file in the backend directory:

```env
# Firebase
FIREBASE_CREDENTIALS_PATH=path/to/firebase-credentials.json

# Stripe
STRIPE_SECRET_KEY=sk_test_xxxxx
STRIPE_PUBLISHABLE_KEY=pk_test_xxxxx

# Google Maps
GOOGLE_MAPS_API_KEY=AIzaSyXXXXXXXXXXXXXXXXXXX

# Provider APIs
CHARGEPOINT_API_KEY=xxxxx
EVGO_API_KEY=xxxxx

# JWT
SECRET_KEY=your-secret-key-here
ALGORITHM=HS256

# Database
DATABASE_URL=postgresql://user:password@localhost/evcharging
```

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

## 📱 API Endpoints

### Authentication
- `POST /api/auth/register` - User registration
- `POST /api/auth/login` - User login
- `POST /api/auth/refresh` - Refresh access token

### Stations
- `GET /api/stations/nearby` - Get nearby charging stations
- `GET /api/stations/{id}` - Get station details
- `GET /api/stations/{id}/availability` - Real-time availability

### Payments
- `POST /api/payments/create-intent` - Create payment intent
- `POST /api/payments/confirm` - Confirm payment
- `GET /api/payments/methods` - Get saved payment methods
- `POST /api/payments/methods` - Add payment method

### Charging Sessions
- `POST /api/sessions/start` - Start charging session
- `POST /api/sessions/{id}/stop` - Stop charging session
- `GET /api/sessions/active` - Get active sessions
- `GET /api/sessions/history` - Get session history

### User
- `GET /api/user/profile` - Get user profile
- `PUT /api/user/profile` - Update user profile
- `GET /api/user/vehicles` - Get user vehicles
- `POST /api/user/vehicles` - Add vehicle

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

## 📊 Future Enhancements

- [ ] Multi-language support
- [ ] Route planning with charging stops
- [ ] Reservation system
- [ ] Loyalty programs and rewards
- [ ] Carbon footprint tracking
- [ ] Social features (reviews, ratings)
- [ ] Integration with vehicle telematics
- [ ] Dynamic pricing alerts
- [ ] Membership subscriptions

## 🤝 Contributing

1. Fork the repository
2. Create your feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit your changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 👥 Authors

- Your Name - [GitHub](https://github.com/yourusername)

## 🙏 Acknowledgments

- Google Maps Platform for location services
- Stripe for payment infrastructure
- Firebase for real-time capabilities
- All EV charging network providers for their APIs

## 📧 Contact

For questions or support, please open an issue or contact [your-email@example.com]

---

⚡ **Powering the future of EV charging, one transaction at a time.**
