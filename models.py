from sqlalchemy.dialects.postgresql import JSON
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
import json

db = SQLAlchemy()

class Product(db.Model):
    __tablename__ = 'products'

    id = db.Column(db.Integer, primary_key=True)
    product_index = db.Column(db.String(50), unique=True, nullable=False)

    name = db.Column(db.String(100), nullable=False)
    buying_price = db.Column(db.Float, nullable=False)
    selling_price = db.Column(db.Float, nullable=False)
    quantity = db.Column(db.Integer, default=0, nullable=False)

    alert_config = db.Column(db.Text, nullable=False)  #! Will store JSON as string

    description = db.Column(db.Text, nullable=True)
    supplier_name = db.Column(db.String(100), nullable=True)
    last_updated = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    # Add category field
    category = db.Column(db.String(100), nullable=True)  #! Optional category field

    @property
    def stock_alert(self):
        """
        Determine alert level based on quantity and thresholds in alert_config.
        """
        try:
            config = json.loads(self.alert_config)
            in_stock = config.get("in_stock", 999999)
            low_stock = config.get("low_stock", 0)

            if self.quantity <= 0:
                return "Out of Stock"
            elif self.quantity <= low_stock:
                return "Low Stock"
            elif self.quantity >= in_stock:
                return "In Stock"
            else:
                return "Moderate Stock"
        except Exception:
            return "Alert Config Error"

    def to_dict(self):
        return {
            "id": self.id,
            "product_index": self.product_index,
            "name": self.name,
            "buying_price": self.buying_price,
            "selling_price": self.selling_price,
            "quantity": self.quantity,
            "alert_level": self.stock_alert,
            "alert_config": self.alert_config,
            "description": self.description,
            "supplier_name": self.supplier_name,
            "category": self.category,  # Include category in the dictionary
            "last_updated": self.last_updated.isoformat()
        }
