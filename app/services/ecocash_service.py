from paynow import Paynow
from app.config.paynow import paynow_settings

class EcoCashService:
    def __init__(self):
        if not paynow_settings.PAYNOW_INTEGRATION_ID:
            raise RuntimeError("Paynow is not configured")
        self.paynow = Paynow(
            paynow_settings.PAYNOW_INTEGRATION_ID,
            paynow_settings.PAYNOW_INTEGRATION_KEY,
            paynow_settings.PAYNOW_RETURN_URL,
            paynow_settings.PAYNOW_RESULT_URL,
        )

    def initiate_payment(self, reference, email, phone, amount):
        payment = self.paynow.create_payment(reference, email)
        payment.add("Mall WiFi Package", amount)

        response = self.paynow.send_mobile(payment, phone, "ecocash")

        if response.success:
            return {
                "poll_url": response.poll_url,
                "instructions": response.instructions,
            }
        else:
            raise Exception("EcoCash payment initiation failed")
