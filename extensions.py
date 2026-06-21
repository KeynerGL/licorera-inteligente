# ============================================================
# EXTENSIONES: Flask-Limiter
# ============================================================
from flask_limiter import Limiter
from flask_limiter.util import get_remote_address

def get_real_ip():
    """Obtiene la IP real detrás de proxies como Railway."""
    from flask import request
    forwarded = request.headers.get('X-Forwarded-For')
    if forwarded:
        return forwarded.split(',')[0].strip()
    return get_remote_address()

limiter = Limiter(
    get_real_ip,
    default_limits=[],
    storage_uri="memory://"
)