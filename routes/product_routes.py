from flask import Blueprint, render_template, request, redirect, url_for, flash, Response
from models.product_model import ProductModel
import pandas as pd
import numpy as np
from sklearn.linear_model import LinearRegression
import csv
import io
from utils.auth import login_required

product_bp = Blueprint('product_bp', __name__)

@product_bp.route('/')
@login_required
def index():
    products = ProductModel.get_all_products()
    
    sort_by = request.args.get('sort_by', 'id')
    search_query = request.args.get('search', '').strip()
    
    # Calculate Dashboard KPIs before sorting/filtering
    total_products = len(products) if products else 0
    total_value = sum(p['price'] * p['quantity'] for p in products) if products else 0
    low_stock_count = sum(1 for p in products if p['quantity'] < 20) if products else 0
    
    # Use standard Algorithm 1: Merge Sort
    if products:
        products = ProductModel.merge_sort(list(products), sort_key=sort_by)
        
    # Use standard Algorithm 2: Binary Search
    if search_query:
        # Binary search requires the array to be sorted by the search key first
        sorted_for_search = ProductModel.merge_sort(list(products), sort_key='name')
        found_product = ProductModel.binary_search(sorted_for_search, search_query, search_key='name')
        if found_product:
            products = [found_product]
        else:
            products = []

    # Calculate Data for Charts
    category_data = {}
    if products:
        for p in products:
            cat = p['category'] or 'Uncategorized'
            if cat not in category_data:
                category_data[cat] = {'value': 0, 'quantity': 0}
            category_data[cat]['value'] += float(p['price']) * int(p['quantity'])
            category_data[cat]['quantity'] += int(p['quantity'])
            
    category_labels = list(category_data.keys())
    category_values = [category_data[k]['value'] for k in category_labels]
    category_quantities = [category_data[k]['quantity'] for k in category_labels]

    return render_template('index.html', 
                           products=products, 
                           sort_by=sort_by, 
                           search_query=search_query,
                           total_products=total_products,
                           total_value=total_value,
                           low_stock_count=low_stock_count,
                           category_labels=category_labels,
                           category_values=category_values,
                           category_quantities=category_quantities)

@product_bp.route('/product/<int:id>')
@login_required
def details(id):
    product = ProductModel.get_product_by_id(id)
    if not product:
        flash('Product not found!', 'danger')
        return redirect(url_for('product_bp.index'))
        
    sales_history = ProductModel.get_sales_history(id)
    return render_template('details.html', product=product, historical_data=sales_history)

@product_bp.route('/low-stock')
@login_required
def low_stock():
    products = ProductModel.get_all_products()
    low_stock_products = [p for p in products if p['quantity'] < 20] if products else []
    
    # Sort them by lowest quantity first
    low_stock_products = sorted(low_stock_products, key=lambda x: x['quantity'])
    
    return render_template('low_stock.html', products=low_stock_products)

@product_bp.route('/export')
@login_required
def export_csv():
    products = ProductModel.get_all_products()
    
    # Create an in-memory string buffer
    si = io.StringIO()
    cw = csv.writer(si)
    cw.writerow(['ID', 'Name', 'Category', 'Quantity', 'Price', 'Description'])
    
    if products:
        for p in products:
            cw.writerow([p['id'], p['name'], p['category'], p['quantity'], p['price'], p['description']])
            
    output = si.getvalue()
    return Response(
        output,
        mimetype="text/csv",
        headers={"Content-Disposition": "attachment;filename=inventory_export.csv"}
    )

@product_bp.route('/add', methods=['GET', 'POST'])
@login_required
def add():
    if request.method == 'POST':
        name = request.form['name']
        category = request.form['category']
        quantity = int(request.form['quantity'])
        price = float(request.form['price'])
        description = request.form['description']
        
        ProductModel.add_product(name, category, quantity, price, description)
        flash('Product added successfully!', 'success')
        return redirect(url_for('product_bp.index'))
        
    return render_template('add.html')

@product_bp.route('/edit/<int:id>', methods=['GET', 'POST'])
@login_required
def edit(id):
    product = ProductModel.get_product_by_id(id)
    if not product:
        flash('Product not found!', 'danger')
        return redirect(url_for('product_bp.index'))
        
    if request.method == 'POST':
        name = request.form['name']
        category = request.form['category']
        quantity = int(request.form['quantity'])
        price = float(request.form['price'])
        description = request.form['description']
        
        ProductModel.update_product(id, name, category, quantity, price, description)
        flash('Product updated successfully!', 'success')
        return redirect(url_for('product_bp.index'))
        
    return render_template('edit.html', product=product)

@product_bp.route('/delete/<int:id>', methods=['POST'])
@login_required
def delete(id):
    ProductModel.delete_product(id)
    flash('Product deleted successfully!', 'success')
    return redirect(url_for('product_bp.index'))

@product_bp.route('/predict/<int:id>')
@login_required
def predict(id):
    product = ProductModel.get_product_by_id(id)
    if not product:
        flash('Product not found!', 'danger')
        return redirect(url_for('product_bp.index'))
        
    sales_history = ProductModel.get_sales_history(id)
    
    if not sales_history or len(sales_history) < 2:
        flash('Not enough sales history to forecast demand.', 'warning')
        return redirect(url_for('product_bp.index'))
        
    # Prepare data for AI Algorithm (Linear Regression)
    df = pd.DataFrame(sales_history)
    
    # We will simply use an index for time periods since months are sequential strings
    # Assuming the data is already sorted by month from db query
    df['time_index'] = np.arange(len(df))
    
    X = df[['time_index']]
    y = df['quantity_sold']
    
    # AI Algorithm: Linear Regression for demand forecasting
    model = LinearRegression()
    X_matrix = X.values
    model.fit(X_matrix, y.values)
    
    # Predict next month (current length index)
    next_time_index = [[len(df)]]
    predicted_demand_continuous = model.predict(next_time_index)[0]
    predicted_demand = max(0, int(round(predicted_demand_continuous))) # Cannot be negative
    
    # Generate plot points for visualization
    df['predicted'] = model.predict(X_matrix)
    chart_data = {
        'labels': df['sale_month'].tolist() + ['Next Month'],
        'actual': df['quantity_sold'].tolist() + [None],
        'predicted': df['predicted'].tolist() + [predicted_demand_continuous]
    }
    
    return render_template('predict.html', 
                           product=product,
                           historical_data=sales_history,
                           prediction=predicted_demand,
                           chart_data=chart_data)

@product_bp.route('/contact', methods=['GET', 'POST'])
def contact():
    if request.method == 'POST':
        name = request.form.get('name')
        email = request.form.get('email')
        message = request.form.get('message')
        ProductModel.add_message(name, email, message)
        flash('Thank you for reaching out! We will get back to you shortly.', 'success')
        return redirect(url_for('product_bp.contact'))
    return render_template('contact.html')
