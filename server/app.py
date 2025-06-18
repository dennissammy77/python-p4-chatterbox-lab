from flask import Flask, request, make_response, jsonify
from flask_cors import CORS
from flask_migrate import Migrate

from models import db, Message

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///app.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.json.compact = False

CORS(app)
migrate = Migrate(app, db)

db.init_app(app)
app.json.compact=False

@app.route('/')
def index():
    return make_response("Welcome to chatterbox",200)

@app.route('/messages', methods=['GET', 'POST'])
def messages():
    if request.method == 'GET':
        messages = Message.query.all()
        return make_response([message.to_dict() for message in messages], 200)
    elif request.method == 'POST':
        data=request.get_json()
        new_message = Message(
           body=data["body"],
           username=data["username"],
        )
        db.session.add(new_message)
        db.session.commit()

        return jsonify(new_message.to_dict()), 201

# PATCH /messages/<int:id>
@app.route('/messages/<int:id>', methods=['PATCH'])
def update_message(id):
    msg = Message.query.get_or_404(id)
    data = request.get_json()
    if not data or 'body' not in data:
        return jsonify({"error": "body required"}), 400

    msg.body = data['body']
    db.session.commit()
    return jsonify(msg.to_dict())

# DELETE /messages/<int:id>
@app.route('/messages/<int:id>', methods=['DELETE'])
def delete_message(id):
    msg = Message.query.get_or_404(id)
    db.session.delete(msg)
    db.session.commit()
    return jsonify({"message": "Message deleted successfully."}), 200

@app.route('/messages/<int:id>')
def messages_by_id(id):
    return ''

if __name__ == '__main__':
    app.run(port=5555)
