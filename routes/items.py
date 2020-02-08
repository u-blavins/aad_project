from flask import Blueprint, request, jsonify, redirect, url_for, flash, render_template, session
from models.Item import Item as ItemModel
from models.Unit import Unit as UnitModel

items = Blueprint('items', __name__)


@items.route('/api/items', methods=['GET'])
def get_items():
    result = ItemModel.get_all_items()
    items = []
    for item in result:
        items.append(item.__dict__)
    return jsonify(items=items)


@items.route('/api/items/item/<code>', methods=['GET'])
def get_item(code):
    item = ItemModel.get_item(code)
    return jsonify(item=item.__dict__)


@items.route('/api/items/codes', methods=['GET'])
def get_codes():
    codes = ItemModel.get_codes()
    return jsonify(codes=codes)


@items.route('/api/items/<code>/units', methods=['GET'])
def get_units(code):
    units_collection = ItemModel.get_unit_types(code)
    return jsonify(units=units_collection)


@items.route('/items/add', methods=['POST'])
def add_items():
    if request.method == 'POST':
        code = request.form['code']
        name = request.form['name']
        quantity = request.form['quantity']
        price = request.form['price']
        threshold = request.form['threshold']
        risk = request.form['risk']
        purchase = request.form['purchase']
        if code in ItemModel.get_codes():
            flash('Error: Item code already exists')
            return render_template('addItemToInventory.html')
        else:
            ItemModel.add_item(code, name, quantity, price, threshold, risk, purchase)     
            return redirect(url_for('admin.stocks'))

@items.route('/items/remove/<code>', methods=['POST'])
def remove_item(code):
    if request.method == 'POST':
        if session['privilege'] == 3:
            if code in ItemModel.get_codes():
                ItemModel.delete_item(code)
                flash('Success: Deleted item')
            else:
                flash('Error: Item does not exist')
    return redirect(url_for('admin.stocks'))


@items.route('/api/units')
def units():
    units_collection = []
    result = UnitModel.get_all_units()
    for unit in result:
        units.append(unit.__dict__)
    return jsonify(units=units_collection)