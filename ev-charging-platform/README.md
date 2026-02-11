# 🔌 EV Charging & Payment Aggregator Platform (Prototype Scaffold)

A work-in-progress project exploring an **EV charging aggregator** concept: a single app that helps users discover chargers and complete payments through a unified flow across multiple charging networks.

> **Status:** Prototype scaffold. The repo contains project structure and starter code, but **external integrations (Google Maps / Firebase / Stripe) require your own credentials** and the end-to-end workflow is **not fully implemented yet**.

---

## What’s in this repo today

✅ Repository scaffolding for:
- **Mobile app** (React Native)
- **Backend API** (FastAPI)
- Optional **web dashboard** (React)

✅ Configuration templates:
- `.env.example` included (no secrets committed)

⚠️ Not implemented end-to-end yet:
- Real station availability + provider network adapters
- Production payment flow and session start/stop
- Full authentication + persistence rules
- Tests and deployment pipelines

---

## MVP roadmap

- [ ] Backend: `/health` + `/stations` using mock data
- [ ] Mobile: map screen + connector filters (mock data)
- [ ] Firebase: auth + store stations + store transactions
- [ ] Stripe (test mode): create PaymentIntent + confirm payment
- [ ] Provider adapters: mock provider A/B, simulate availability changes
- [ ] Web dashboard: view stations + transactions (optional)

---

## Planned tech stack

- **React Native** (mobile)
- **FastAPI (Python)** (backend)
- **Firebase** (auth + data)
- **Stripe** (payments)
- **Google Maps Platform** (maps)



---

## Project structure

