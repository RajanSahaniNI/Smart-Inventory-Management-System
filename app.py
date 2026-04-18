from flask import Flask
from config import Config
from routes.product_routes import product_bp
from routes.auth_routes import auth_bp

def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)

    # Register Blueprints
    app.register_blueprint(product_bp)
    app.register_blueprint(auth_bp)

    @app.context_processor
    def inject_low_stock():
        from models.product_model import ProductModel
        try:
            products = ProductModel.get_all_products()
            low_stock_count = sum(1 for p in products if p['quantity'] < 20) if products else 0
        except Exception:
            low_stock_count = 0
        return dict(global_low_stock=low_stock_count)

    return app

if __name__ == '__main__':
    app = create_app()
    app.run(debug=True, port=5000)
