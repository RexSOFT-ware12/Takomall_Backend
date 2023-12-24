from flask import Flask, request, jsonify
from flask_cors import CORS
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
CORS(app)  
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///businesses.db'
db = SQLAlchemy(app)

businesses = []
products = []
orders = []

class Business(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    business_name = db.Column(db.String(255), nullable=False)
    owner_info = db.Column(db.String(255), nullable=False)
    contact_info = db.Column(db.String(255), nullable=False)

class Product(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    product_name = db.Column(db.String(255), nullable=False)
    description = db.Column(db.Text, nullable=True)
    price = db.Column(db.Float, nullable=False)
    business_id = db.Column(db.Integer, db.ForeignKey('business.id'), nullable=False)
    business = db.relationship('Business', backref=db.backref('products', lazy=True))

    def __repr__(self):
        return f"<Product {self.product_name}>"

# Endpoint to manage businesses
@app.route('/admin-dashboard/manage-businesses', methods=['POST'])
def create_business():
    data = request.get_json()
    if not data or 'business_name' not in data or 'owner_info' not in data or 'contact_info' not in data:
        return jsonify({'error': 'Invalid or missing JSON data'}), 400

    new_business = Business(
        business_name=data['business_name'],
        owner_info=data['owner_info'],
        contact_info=data['contact_info']
    )

    db.session.add(new_business)
    db.session.commit()

    return jsonify({'message': 'Business created successfully', 'business': {
        'business_id': new_business.id,
        'business_name': new_business.business_name,
        'owner_info': new_business.owner_info,
        'contact_info': new_business.contact_info
    }})

# Endpoint to update manage businesses
@app.route('/admin-dashboard/update-business/<int:business_id>', methods=['PUT'])
def update_business(business_id):
    data = request.get_json()
    business = Business.query.get(business_id)

    if not business:
        return jsonify({'error': 'Business not found'}), 404

    if 'business_name' in data:
        business.business_name = data['business_name']

    if 'owner_info' in data:
        business.owner_info = data['owner_info']

    if 'contact_info' in data:
        business.contact_info = data['contact_info']

    db.session.commit()

    return jsonify({'message': 'Business updated successfully', 'business': {
        'business_id': business.id,
        'business_name': business.business_name,
        'owner_info': business.owner_info,
        'contact_info': business.contact_info
    }})

# Endpoint to get information about a specific business
@app.route('/admin-dashboard/get-business/<int:business_id>', methods=['GET'])
def get_business(business_id):
    # Query the database for the business with the given ID
    business = Business.query.get(business_id)

    # Check if the business with the given ID exists
    if not business:
        return jsonify({'error': f'Business with ID {business_id} not found'}), 404

    # Return information about the business
    return jsonify({
        'business_id': business.id,
        'business_name': business.business_name,
        'owner_info': business.owner_info,
        'contact_info': business.contact_info
    })

# Endpoint to list all businesses
@app.route('/admin-dashboard/list-businesses', methods=['GET'])
def list_businesses():
    # Query the database for all businesses
    all_businesses = Business.query.all()

    # Check if there are any businesses in the database
    if not all_businesses:
        return jsonify({'message': 'No businesses found in the database'}), 404

    # Return a list of businesses
    businesses_list = [{
        'business_id': business.id,
        'business_name': business.business_name,
        'owner_info': business.owner_info,
        'contact_info': business.contact_info
    } for business in all_businesses]

    return jsonify({'businesses': businesses_list})


# Endpoint to manage products
@app.route('/admin-dashboard/manage-products', methods=['POST'])
def create_product():
    data = request.get_json()
    new_product = Product(
        product_name=data['product_name'],
        description=data.get('description'),
        price=data['price'],
        business_id=data['business_id']
    )

    db.session.add(new_product)
    db.session.commit()

    return jsonify({'message': 'Product created successfully', 'product': {
        'product_id': new_product.id,
        'product_name': new_product.product_name,
        'description': new_product.description,
        'price': new_product.price,
        'business_id': new_product.business_id
    }})


# Endpoint to update a product
@app.route('/admin-dashboard/update-product/<int:product_id>', methods=['PUT'])
def update_product(product_id):
    data = request.get_json()
    product = Product.query.get(product_id)

    if not product:
        return jsonify({'error': 'Product not found'}), 404

    if 'product_name' in data:
        product.product_name = data['product_name']

    if 'description' in data:
        product.description = data['description']

    if 'price' in data:
        product.price = data['price']

    if 'business_id' in data:
        product.business_id = data['business_id']

    db.session.commit()

    return jsonify({'message': 'Product updated successfully', 'product': {
        'product_id': product.id,
        'product_name': product.product_name,
        'description': product.description,
        'price': product.price,
        'business_id': product.business_id
    }})
    

# Endpoint to get products for a specific business
@app.route('/admin-dashboard/get-products/<int:business_id>', methods=['GET'])
def get_products(business_id):
    # Query the database for products associated with the given business ID
    products = Product.query.filter_by(business_id=business_id).all()

    # Check if any products are found
    if not products:
        return jsonify({'message': f'No products found for business with ID {business_id}'}), 404

    # Return a list of products for the specified business
    product_list = [{
        'product_id': product.id,
        'product_name': product.product_name,
        'description': product.description,
        'price': product.price,
        'business_id': product.business_id
    } for product in products]

    return jsonify({'products': product_list})

# Endpoint to fetch all products
@app.route('/admin-dashboard/get-all-products', methods=['GET'])
def get_all_products():
    # Query the database for all products
    all_products = Product.query.all()

    # Check if any products are found
    if not all_products:
        return jsonify({'message': 'No products found in the database'}), 404

    # Return a list of all products
    all_products_list = [{
        'product_id': product.id,
        'product_name': product.product_name,
        'description': product.description,
        'price': product.price,
        'business_id': product.business_id
    } for product in all_products]

    return jsonify({'all_products': all_products_list})


# Endpoint to view order summary
@app.route('/admin-dashboard/view-order-summary/<int:order_id>', methods=['GET'])
def view_order_summary(order_id):
    order = next((o for o in orders if o['order_id'] == order_id), None)
    if order:
        return jsonify(order)
    return jsonify({'message': 'Order not found'}), 404


# Endpoint to update order status
@app.route('/admin-dashboard/update-order-status/<int:order_id>', methods=['PUT'])
def update_order_status(order_id):
    data = request.get_json()
    order = next((o for o in orders if o['order_id'] == order_id), None)
    if order:
        order['status'] = data['status']
        return jsonify({'message': 'Order status updated successfully', 'order': order})
    return jsonify({'message': 'Order not found'}), 404


# Endpoint to track orders
@app.route('/admin-dashboard/track-orders', methods=['GET'])
def track_orders():
    return jsonify({'orders': orders})


if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(debug=True)
