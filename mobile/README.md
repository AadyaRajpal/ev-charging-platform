# EVFind Mobile

React Native mobile app for finding nearby EV charging stations. Built with Expo.

## Screens

- **Home** — Search by location with live results list
- **Map** — Interactive map with station markers, tap to view details
- **Station Detail** — Full info, connector types, save to bookmarks
- **Saved** — Bookmarked stations

## Setup

**Prerequisites:** Node.js, Expo CLI, and the [Expo Go](https://expo.dev/client) app on your phone.

```bash
npm install
npx expo start
```

Scan the QR code with Expo Go to run on your phone.

## Backend

Requires the FastAPI backend running. See `../backend/`.

For physical device testing, update `src/api/stations.js`:
```js
const API_BASE = 'http://YOUR_LOCAL_IP:8000';
```

Find your local IP with `ipconfig` (Windows) or `ifconfig` (Mac/Linux).
