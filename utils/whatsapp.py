# ============================================================
# UTILIDAD: Notificaciones WhatsApp con Twilio
# ============================================================
import os
from twilio.rest import Client

def send_low_stock_alert(products):
    """Envía alerta de stock bajo por WhatsApp."""
    try:
        account_sid = os.environ.get('TWILIO_ACCOUNT_SID')
        auth_token  = os.environ.get('TWILIO_AUTH_TOKEN')
        to_number   = os.environ.get('TWILIO_WHATSAPP_TO')

        if not all([account_sid, auth_token, to_number]):
            print("⚠️ Variables de Twilio no configuradas.")
            return False

        client = Client(account_sid, auth_token)

        # Armar mensaje
        lista = '\n'.join([f'📦 {p.name} → Solo {p.quantity} unidades' for p in products])
        mensaje = f'⚠️ *Licorera Inteligente*\n\nProductos con stock bajo:\n{lista}'

        client.messages.create(
            from_='whatsapp:+14155238886',
            to=f'whatsapp:{to_number}',
            body=mensaje
        )
        print("✅ Alerta WhatsApp enviada.")
        return True

    except Exception as e:
        print(f"❌ Error enviando WhatsApp: {e}")
        return False