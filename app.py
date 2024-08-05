from flask import Flask, render_template, request, redirect, url_for
from datetime import datetime
from models import session, FoodItem

app = Flask(__name__)

@app.route('/')
def home():

    filter_type = request.args.get('filter_type')
    filter_value = request.args.get('filter_value')

    query = session.query(FoodItem)

    # Queries for the filteration ()
    if filter_type and filter_value:

        if filter_type == 'location':
            query = query.filter(FoodItem.location == filter_value)

        elif filter_type == 'food_type':
            query = query.filter(FoodItem.food_type == filter_value)

        elif filter_type == 'other_tags':
            query = query.filter(FoodItem.other_tags.like(f'%{filter_value}%'))

        elif filter_type == 'owner':
            query = query.filter(FoodItem.owner == filter_value)

        elif filter_type == 'expiry':
            query = query.order_by(FoodItem.expiry_date)

    food_items = query.all()

    return render_template('home.html', food_items=food_items)

@app.route('/add', methods=['GET', 'POST'])

def add_item():

    # forms to get input
    if request.method == 'POST':
        name = request.form['name']
        expiry_date = request.form['expiry_date']
        owner = request.form['owner']
        location = request.form['location']
        food_type = request.form['food_type']
        other_tags = request.form['other_tags']


        new_item = FoodItem(
            name=name,
            expiry_date=datetime.strptime(expiry_date, '%Y-%m-%d'),
            owner=owner,
            location=location,
            food_type=food_type,
            other_tags=other_tags
        )

        # adding the info from forms
        session.add(new_item)
        session.commit()
        
        # sends back to home
        return redirect(url_for('home'))

    # this template is rendered/loaded when adding items
    return render_template('add_item.html')

# for editing existing food items in database
@app.route('/edit/<int:item_id>', methods=['GET', 'POST'])

def edit_item(item_id):

    item = session.query(FoodItem).get(item_id)

    if request.method == 'POST':
        item.name = request.form['name']
        item.expiry_date = datetime.strptime(request.form['expiry_date'], '%Y-%m-%d')
        item.owner = request.form['owner']
        item.location = request.form['location']
        item.food_type = request.form['food_type']
        item.other_tags = request.form['other_tags']

        # saving/commiting the changes to data base
        session.commit()
        
        # back to home
        return redirect(url_for('home'))

    # this template is rendered/loaded when editing items
    return render_template('edit_item.html', item=item)

if __name__ == '__main__':
    app.run(debug=True)