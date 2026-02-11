from fastapi import APIRouter, Depends, HTTPException, Header
from pydantic import BaseModel
from typing import List, Optional
from app.api.routes.auth import get_current_user_dependency
from app.services.stripe_service import stripe_service

router = APIRouter()

# Request/Response Models
class PaymentMethodCreate(BaseModel):
    payment_method_id: str

class PaymentIntentCreate(BaseModel):
    amount: float  # Amount in dollars
    currency: str = "usd"
    payment_method_id: Optional[str] = None
    session_id: str
    station_id: str

class RefundRequest(BaseModel):
    payment_intent_id: str
    amount: Optional[float] = None
    reason: Optional[str] = None

@router.post("/methods")
async def add_payment_method(
    payment_data: PaymentMethodCreate,
    current_user: dict = Depends(get_current_user_dependency)
):
    """Add a payment method to user's account"""
    
    user_id = current_user['user_id']
    
    # Get or create Stripe customer
    stripe_customer_id = current_user.get('stripe_customer_id')
    
    if not stripe_customer_id:
        # Create new Stripe customer
        customer = await stripe_service.create_customer(
            email=current_user['email'],
            name=current_user['name'],
            metadata={'user_id': user_id}
        )
        stripe_customer_id = customer['customer_id']
        # Update user record with stripe_customer_id (in production)
    
    # Attach payment method
    payment_method = await stripe_service.attach_payment_method(
        payment_data.payment_method_id,
        stripe_customer_id
    )
    
    return {
        "message": "Payment method added successfully",
        "payment_method": payment_method
    }

@router.get("/methods")
async def list_payment_methods(
    current_user: dict = Depends(get_current_user_dependency)
):
    """Get all payment methods for user"""
    
    stripe_customer_id = current_user.get('stripe_customer_id')
    
    if not stripe_customer_id:
        return {"payment_methods": []}
    
    payment_methods = await stripe_service.list_payment_methods(stripe_customer_id)
    
    return {"payment_methods": payment_methods}

@router.delete("/methods/{payment_method_id}")
async def remove_payment_method(
    payment_method_id: str,
    current_user: dict = Depends(get_current_user_dependency)
):
    """Remove a payment method"""
    
    success = await stripe_service.detach_payment_method(payment_method_id)
    
    if not success:
        raise HTTPException(status_code=400, detail="Failed to remove payment method")
    
    return {"message": "Payment method removed successfully"}

@router.post("/create-intent")
async def create_payment_intent(
    payment_data: PaymentIntentCreate,
    current_user: dict = Depends(get_current_user_dependency)
):
    """Create a payment intent for charging session"""
    
    stripe_customer_id = current_user.get('stripe_customer_id')
    
    if not stripe_customer_id:
        raise HTTPException(status_code=400, detail="No payment methods configured")
    
    # Convert amount to cents
    amount_cents = int(payment_data.amount * 100)
    
    # Create payment intent
    intent = await stripe_service.create_payment_intent(
        amount=amount_cents,
        currency=payment_data.currency,
        customer_id=stripe_customer_id,
        payment_method_id=payment_data.payment_method_id,
        metadata={
            'user_id': current_user['user_id'],
            'session_id': payment_data.session_id,
            'station_id': payment_data.station_id
        }
    )
    
    return {
        "payment_intent": intent,
        "message": "Payment intent created successfully"
    }

@router.post("/confirm")
async def confirm_payment(
    payment_intent_id: str,
    current_user: dict = Depends(get_current_user_dependency)
):
    """Confirm a payment intent"""
    
    intent = await stripe_service.confirm_payment_intent(payment_intent_id)
    
    return {
        "payment_intent": intent,
        "message": "Payment confirmed successfully"
    }

@router.get("/intent/{payment_intent_id}")
async def get_payment_intent(
    payment_intent_id: str,
    current_user: dict = Depends(get_current_user_dependency)
):
    """Get payment intent details"""
    
    intent = await stripe_service.get_payment_intent(payment_intent_id)
    
    if not intent:
        raise HTTPException(status_code=404, detail="Payment intent not found")
    
    return {"payment_intent": intent}

@router.post("/refund")
async def create_refund(
    refund_data: RefundRequest,
    current_user: dict = Depends(get_current_user_dependency)
):
    """Create a refund for a payment"""
    
    # Convert amount to cents if provided
    amount_cents = int(refund_data.amount * 100) if refund_data.amount else None
    
    refund = await stripe_service.create_refund(
        payment_intent_id=refund_data.payment_intent_id,
        amount=amount_cents,
        reason=refund_data.reason
    )
    
    return {
        "refund": refund,
        "message": "Refund created successfully"
    }

@router.get("/history")
async def get_payment_history(
    limit: int = 10,
    current_user: dict = Depends(get_current_user_dependency)
):
    """Get payment history for user"""
    
    stripe_customer_id = current_user.get('stripe_customer_id')
    
    if not stripe_customer_id:
        return {"payments": []}
    
    charges = await stripe_service.get_charge_history(stripe_customer_id, limit)
    
    return {"payments": charges}

@router.post("/webhook")
async def stripe_webhook(
    payload: bytes,
    stripe_signature: str = Header(None, alias="Stripe-Signature")
):
    """Handle Stripe webhook events"""
    
    if not stripe_signature:
        raise HTTPException(status_code=400, detail="Missing signature")
    
    try:
        event = await stripe_service.verify_webhook_signature(payload, stripe_signature)
        
        # Handle different event types
        event_type = event['type']
        
        if event_type == 'payment_intent.succeeded':
            # Handle successful payment
            payment_intent = event['data']['object']
            # Update session status, send notification, etc.
            pass
        
        elif event_type == 'payment_intent.payment_failed':
            # Handle failed payment
            payment_intent = event['data']['object']
            # Notify user, cancel session, etc.
            pass
        
        return {"status": "success"}
    
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))
