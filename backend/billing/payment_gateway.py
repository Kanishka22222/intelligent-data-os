import time
import json
import uuid

class PaymentGateway:
    @staticmethod
    def create_checkout_session(plan_id, currency="INR", user_email="customer@enterprise.com"):
        amount = 249900 if plan_id == "plan_pro" else 1699900  # in paise
        order_id = f"order_dataos_{uuid.uuid4().hex[:10]}"
        
        # Razorpay & Stripe unified session mock payload
        session = {
            "order_id": order_id,
            "plan_id": plan_id,
            "currency": currency,
            "amount": amount,
            "display_amount": f"₹{amount/100:,.2f}" if currency == "INR" else f"${amount/100:,.2f}",
            "razorpay_key": "rzp_test_DataOSLiveEnterpriseKey",
            "stripe_session_id": f"cs_test_{uuid.uuid4().hex}",
            "customer": {
                "name": "Enterprise Data Lead",
                "email": user_email,
                "contact": "+919876543210"
            },
            "status": "CREATED",
            "created_at": time.strftime("%Y-%m-%d %H:%M:%S")
        }
        return session

    @staticmethod
    def verify_payment_and_generate_invoice(order_id, plan_id, payment_id="pay_simulated_success", currency="INR"):
        invoice_no = f"INV-DATAOS-{int(time.time())}"
        amount_str = "₹2,499.00" if plan_id == "plan_pro" else "₹16,999.00"
        tax_str = "₹449.82" if plan_id == "plan_pro" else "₹3,059.82"
        plan_title = "Pro Data Strategist Plan (1 Month)" if plan_id == "plan_pro" else "Enterprise Autonomous Brain Plan (1 Month)"

        invoice = {
            "invoice_number": invoice_no,
            "order_id": order_id,
            "payment_id": payment_id,
            "payment_status": "PAID_VERIFIED",
            "payment_method": "Razorpay / UPI / Credit Card (Encrypted)",
            "date": time.strftime("%B %d, %Y"),
            "supplier": {
                "name": "Data Operating System (DataOS) Inc.",
                "gstin": "27AAACD9988P1Z3",
                "address": "Bandra Kurla Complex, Mumbai, Maharashtra 400051"
            },
            "buyer": {
                "name": "Verified Customer Account",
                "email": "customer@enterprise.com",
                "gstin": "27AABCT2345M1Z2"
            },
            "items": [
                {
                    "hsn": "998313",
                    "description": plan_title,
                    "quantity": 1,
                    "taxable_value": "₹2,049.18" if plan_id == "plan_pro" else "₹13,939.18",
                    "cgst_9pct": "₹184.41" if plan_id == "plan_pro" else "₹1,254.51",
                    "sgst_9pct": "₹184.41" if plan_id == "plan_pro" else "₹1,254.51",
                    "total": amount_str
                }
            ],
            "total_paid": amount_str,
            "receipt_download_url": f"/api/billing/invoice/{invoice_no}"
        }
        return invoice
