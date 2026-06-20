import os
from app import app
from database import db

with app.app_context():
    with db.engine.connect() as conn:
        conn.execute(db.text(
            "ALTER TABLE products ADD COLUMN IF NOT EXISTS image_url VARCHAR(500) DEFAULT ''"
        ))
        conn.commit()
        print("✅ Columna image_url agregada correctamente")