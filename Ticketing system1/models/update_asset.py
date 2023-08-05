from flask import Flask, render_template, request

app = Flask(__name__)

# Asset data dictionary (example data)
assets = {
    1: {
        'name': 'Asset 1',
        'category': 'Hardware',
        'description': 'Asset description 1'
    },
    2: {
        'name': 'Asset 2',
        'category': 'Software',
        'description': 'Asset description 2'
    }
}

@app.route('/update_asset', methods=['POST'])
def update_asset():
    asset_id = int(request.form['asset_id'])
    if asset_id not in assets:
        return f"Asset with ID {asset_id} does not exist."
    name = request.form['name']
    # Update asset data
    assets[asset_id]['name'] = name
    category = request.form['category']
    assets[asset_id]['category'] = category
    assets[asset_id]['description'] = request.form['description']

    return f"Asset with ID {asset_id} updated successfully!"

if __name__ == '__main__':
    app.run()
