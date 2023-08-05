
from flask import Flask, render_template, request

app = Flask(__name__)

@app.route('/submit_ticket', methods=['POST'])
def submit_ticket():
    if request.method != 'POST':
        return "Invalid request"
    category = request.form['category']
    priority = request.form['priority']
    description = request.form['description']

    attachments = request.files.getlist('attachments')
    attachment_paths = []

    for attachment in attachments:
        attachment.save(f'attachments/{attachment.filename}')
        attachment_paths.append(f'attachments/{attachment.filename}')

    print(f"Category: {category}")
    return "Ticket submitted successfully!"



if __name__ == '__main__':
    app.run()

