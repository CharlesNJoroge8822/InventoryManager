from flask import Blueprint, request, jsonify
from models import Product, db
import json
from sqlalchemy.exc import SQLAlchemyError

product_bp = Blueprint('product', __name__, url_prefix='/api/products')

# Helper function for error responses
def error_response(message, status_code):
    return jsonify({
        "status": "error",
        "message": message
    }), status_code

# ================================
# 📦 Get All Products (Improved)
# ================================
@product_bp.route('/', methods=['GET'])
def get_all_products():
    """Retrieve a list of all products with pagination."""
    try:
        # Get pagination parameters from query string
        page = request.args.get('page', 1, type=int)
        per_page = request.args.get('per_page', 25, type=int)
        
        # Query products with pagination
        products = Product.query.paginate(
            page=page,
            per_page=per_page,
            error_out=False
        )
        
        # Prepare response data
        response = {
            "status": "success",
            "data": [product.to_dict() for product in products.items],
            "pagination": {
                "total": products.total,
                "pages": products.pages,
                "current_page": page,
                "per_page": per_page,
                "has_next": products.has_next,
                "has_prev": products.has_prev
            }
        }
        
        return jsonify(response), 200
    
    except Exception as e:
        return error_response(f"Failed to fetch products: {str(e)}", 500)

# ================================
# 🔍 Get Single Product by ID (Improved)
# ================================
@product_bp.route('/<int:product_id>', methods=['GET'])
def get_single_product(product_id):
    """Retrieve a specific product by its ID."""
    try:
        product = Product.query.get(product_id)
        if not product:
            return error_response("Product not found", 404)
            
        return jsonify({
            "status": "success",
            "data": product.to_dict()
        }), 200
        
    except Exception as e:
        return error_response(f"Failed to fetch product: {str(e)}", 500)

# ================================
# ➕ Create a New Product (Improved)
# ================================
@product_bp.route('/', methods=['POST'])
def create_new_product():
    """Create a new product entry."""
    try:
        # Ensure request has JSON data
        if not request.is_json:
            return error_response("Request must be JSON", 400)
            
        data = request.get_json()

        # Validate required fields
        required_fields = ['product_index', 'name', 'buying_price', 'selling_price', 'quantity', 'alert_config']
        missing_fields = [field for field in required_fields if field not in data]
        if missing_fields:
            return error_response(f"Missing fields: {', '.join(missing_fields)}", 400)

        # Validate alert_config
        try:
            alert_config = json.dumps(data['alert_config'])
        except (TypeError, ValueError) as e:
            return error_response("Invalid alert_config format", 400)

        # Check for duplicate product_index
        if Product.query.filter_by(product_index=data['product_index']).first():
            return error_response("Product index already exists", 400)

        # Create new product
        new_product = Product(
            product_index=data['product_index'],
            name=data['name'],
            buying_price=float(data['buying_price']),
            selling_price=float(data['selling_price']),
            quantity=int(data['quantity']),
            alert_config=alert_config,
            description=data.get('description', ''),
            supplier_name=data.get('supplier_name', ''),
            category=data.get('category', '')
        )

        db.session.add(new_product)
        db.session.commit()
        
        return jsonify({
            "status": "success",
            "message": "Product created successfully",
            "data": new_product.to_dict()
        }), 201
        
    except ValueError as e:
        return error_response(f"Invalid data format: {str(e)}", 400)
    except SQLAlchemyError as e:
        db.session.rollback()
        return error_response(f"Database error: {str(e)}", 500)
    except Exception as e:
        return error_response(f"Unexpected error: {str(e)}", 500)

# ================================
# 🔄 Update an Existing Product (Improved)
# ================================
@product_bp.route('/<int:product_id>', methods=['PUT'])
def update_product(product_id):
    """Update an existing product."""
    try:
        # Ensure request has JSON data
        if not request.is_json:
            return error_response("Request must be JSON", 400)
            
        product = Product.query.get(product_id)
        if not product:
            return error_response("Product not found", 404)

        data = request.get_json()

        # Update fields if they exist in request
        if 'name' in data:
            product.name = data['name']
        if 'buying_price' in data:
            try:
                product.buying_price = float(data['buying_price'])
            except ValueError:
                return error_response("Invalid buying_price format", 400)
        if 'selling_price' in data:
            try:
                product.selling_price = float(data['selling_price'])
            except ValueError:
                return error_response("Invalid selling_price format", 400)
        if 'quantity' in data:
            try:
                product.quantity = int(data['quantity'])
            except ValueError:
                return error_response("Invalid quantity format", 400)
        if 'alert_config' in data:
            try:
                product.alert_config = json.dumps(data['alert_config'])
            except (TypeError, ValueError):
                return error_response("Invalid alert_config format", 400)
        if 'description' in data:
            product.description = data['description']
        if 'supplier_name' in data:
            product.supplier_name = data['supplier_name']
        if 'category' in data:
            product.category = data['category']

        db.session.commit()
        
        return jsonify({
            "status": "success",
            "message": "Product updated successfully",
            "data": product.to_dict()
        }), 200
        
    except SQLAlchemyError as e:
        db.session.rollback()
        return error_response(f"Database error: {str(e)}", 500)
    except Exception as e:
        return error_response(f"Unexpected error: {str(e)}", 500)

# ================================
# ❌ Delete a Product (Improved)
# ================================
@product_bp.route('/<int:product_id>', methods=['DELETE'])
def delete_product(product_id):
    """Delete a product by ID."""
    try:
        product = Product.query.get(product_id)
        if not product:
            return error_response("Product not found", 404)

        db.session.delete(product)
        db.session.commit()
        
        return jsonify({
            "status": "success",
            "message": "Product deleted successfully"
        }), 200
        
    except SQLAlchemyError as e:
        db.session.rollback()
        return error_response(f"Database error: {str(e)}", 500)
    except Exception as e:
        return error_response(f"Unexpected error: {str(e)}", 500)