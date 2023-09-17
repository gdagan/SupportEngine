from flask import Flask, render_template, request

app = Flask(__name__)

# Asset data dictionary (example data)
assets = {}
asset_id = 1

@app.route('/add_asset', methods=['GET', 'POST'])
def add_asset():
    if request.method == 'POST':
        name = request.form['name']
        category = request.form['category']
        description = request.form['description']

        global asset_id
        assets[asset_id] = {
            'name': name,
            'category': category,
            'description': description
        }
        asset_id += 1

        return f"Asset added successfully! Asset ID: {asset_id - 1}"

    return render_template('add_asset.html')

if __name__ == '__main__':
    app.run()
