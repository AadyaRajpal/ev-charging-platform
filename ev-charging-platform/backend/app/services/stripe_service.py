import stripe
from typing import Dict, Any, List, Optional
from datetime import datetime
from app.core.config import settings

# Configure Stripe
stripe.api_key = settings.STRIPE_SECRET_KEY

class StripeService:
    """Service for handling Stripe payment operations"""
    
    def __init__(self):
        self.publishable_key = settings.STRIPE_PUBLISHABLE_KEY
    
    # Customer Management
    async def create_customer(self, email: str, name: str, metadata: Dict[str, Any] = None) -> Dict[str, Any]:
        """Create a new Stripe customer"""
        try:
            customer = stripe.Customer.create(
                email=email,
                name=name,
                metadata=metadata or {}
            )
            return {
                "customer_id": customer.id,
                "email": customer.email,
                "name": customer.name
            }
        except stripe.error.StripeError as e:
            raise Exception(f"Failed to create customer: {str(e)}")
    
    async def get_customer(self, customer_id: str) -> Optional[Dict[str, Any]]:
        """Get customer details"""
        try:
            customer = stripe.Customer.retrieve(customer_id)
            return {
                "customer_id": customer.id,
                "email": customer.email,
                "name": customer.name,
                "default_payment_method": customer.invoice_settings.default_payment_method
            }
        except stripe.error.StripeError as e:
            print(f"Error retrieving customer: {e}")
            return None
    
    # Payment Methods
    async def attach_payment_method(self, payment_method_id: str, customer_id: str) -> Dict[str, Any]:
        """Attach a payment method to a customer"""
        try:
            payment_method = stripe.PaymentMethod.attach(
                payment_method_id,
                customer=customer_id
            )
            
            # Set as default payment method
            stripe.Customer.modify(
                customer_id,
                invoice_settings={'default_payment_method': payment_method_id}
            )
            
            return self._format_payment_method(payment_method)
        except stripe.error.StripeError as e:
            raise Exception(f"Failed to attach payment method: {str(e)}")
    
    async def list_payment_methods(self, customer_id: str) -> List[Dict[str, Any]]:
        """List all payment methods for a customer"""
        try:
            payment_methods = stripe.PaymentMethod.list(
                customer=customer_id,
                type="card"
            )
            return [self._format_payment_method(pm) for pm in payment_methods.data]
        except stripe.error.StripeError as e:
            print(f"Error listing payment methods: {e}")
            return []
    
    async def detach_payment_method(self, payment_method_id: str) -> bool:
        """Detach a payment method from a customer"""
        try:
            stripe.PaymentMethod.detach(payment_method_id)
            return True
        except stripe.error.StripeError as e:
            print(f"Error detaching payment method: {e}")
            return False
    
    # Payment Intents
    async def create_payment_intent(
        self,
        amount: int,  # Amount in cents
        currency: str,
        customer_id: str,
        payment_method_id: Optional[str] = None,
        metadata: Dict[str, Any] = None
    ) -> Dict[str, Any]:
        """Create a payment intent for charging session"""
        try:
            intent_params = {
                "amount": amount,
                "currency": currency,
                "customer": customer_id,
                "metadata": metadata or {},
                "automatic_payment_methods": {"enabled": True}
            }
            
            if payment_method_id:
                intent_params["payment_method"] = payment_method_id
                intent_params["confirm"] = True
            
            intent = stripe.PaymentIntent.create(**intent_params)
            
            return {
                "payment_intent_id": intent.id,
                "client_secret": intent.client_secret,
                "status": intent.status,
                "amount": intent.amount,
                "currency": intent.currency
            }
        except stripe.error.StripeError as e:
            raise Exception(f"Failed to create payment intent: {str(e)}")
    
    async def confirm_payment_intent(self, payment_intent_id: str) -> Dict[str, Any]:
        """Confirm a payment intent"""
        try:
            intent = stripe.PaymentIntent.confirm(payment_intent_id)
            return {
                "payment_intent_id": intent.id,
                "status": intent.status,
                "amount": intent.amount,
                "currency": intent.currency
            }
        except stripe.error.StripeError as e:
            raise Exception(f"Failed to confirm payment: {str(e)}")
    
    async def get_payment_intent(self, payment_intent_id: str) -> Optional[Dict[str, Any]]:
        """Get payment intent details"""
        try:
            intent = stripe.PaymentIntent.retrieve(payment_intent_id)
            return {
                "payment_intent_id": intent.id,
                "status": intent.status,
                "amount": intent.amount,
                "currency": intent.currency,
                "created": datetime.fromtimestamp(intent.created).isoformat()
            }
        except stripe.error.StripeError as e:
            print(f"Error retrieving payment intent: {e}")
            return None
    
    async def cancel_payment_intent(self, payment_intent_id: str) -> bool:
        """Cancel a payment intent"""
        try:
            stripe.PaymentIntent.cancel(payment_intent_id)
            return True
        except stripe.error.StripeError as e:
            print(f"Error canceling payment intent: {e}")
            return False
    
    # Refunds
    async def create_refund(
        self,
        payment_intent_id: str,
        amount: Optional[int] = None,
        reason: Optional[str] = None
    ) -> Dict[str, Any]:
        """Create a refund for a payment"""
        try:
            refund_params = {"payment_intent": payment_intent_id}
            
            if amount:
                refund_params["amount"] = amount
            if reason:
                refund_params["reason"] = reason
            
            refund = stripe.Refund.create(**refund_params)
            
            return {
                "refund_id": refund.id,
                "status": refund.status,
                "amount": refund.amount,
                "currency": refund.currency
            }
        except stripe.error.StripeError as e:
            raise Exception(f"Failed to create refund: {str(e)}")
    
    # Charges and Transactions
    async def get_charge_history(self, customer_id: str, limit: int = 10) -> List[Dict[str, Any]]:
        """Get charge history for a customer"""
        try:
            charges = stripe.Charge.list(customer=customer_id, limit=limit)
            return [
                {
                    "charge_id": charge.id,
                    "amount": charge.amount,
                    "currency": charge.currency,
                    "status": charge.status,
                    "created": datetime.fromtimestamp(charge.created).isoformat(),
                    "description": charge.description
                }
                for charge in charges.data
            ]
        except stripe.error.StripeError as e:
            print(f"Error retrieving charge history: {e}")
            return []
    
    # Webhook handling
    async def verify_webhook_signature(self, payload: bytes, signature: str) -> Dict[str, Any]:
        """Verify Stripe webhook signature"""
        try:
            event = stripe.Webhook.construct_event(
                payload, signature, settings.STRIPE_WEBHOOK_SECRET
            )
            return event
        except ValueError as e:
            raise Exception("Invalid payload")
        except stripe.error.SignatureVerificationError as e:
            raise Exception("Invalid signature")
    
    # Helper methods
    def _format_payment_method(self, pm) -> Dict[str, Any]:
        """Format payment method for API response"""
        return {
            "payment_method_id": pm.id,
            "type": pm.type,
            "card": {
                "brand": pm.card.brand,
                "last4": pm.card.last4,
                "exp_month": pm.card.exp_month,
                "exp_year": pm.card.exp_year
            } if pm.type == "card" else None
        }
    
    def calculate_amount(self, kwh: float, price_per_kwh: float) -> int:
        """Calculate payment amount in cents"""
        total = kwh * price_per_kwh
        return int(total * 100)  # Convert to cents

# Singleton instance
stripe_service = StripeService()
