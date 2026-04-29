import os
import base64
from datetime import datetime
from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)

DATABASE_URL = os.getenv("DATABASE_URL", "postgresql://postgres:postgres@postgres:5432/gamedb")
app.config['SQLALCHEMY_DATABASE_URI'] = DATABASE_URL
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)


class Game(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    secret_b64 = db.Column(db.String, nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)


def encode_secret(secret: str) -> str:
    return base64.b64encode(secret.encode()).decode()


def decode_secret(b64: str) -> str:
    return base64.b64decode(b64.encode()).decode()


@app.before_first_request
def create_tables():
    db.create_all()


@app.route('/health')
def health():
    return jsonify({'status': 'ok'})


@app.route('/games', methods=['POST'])
def create_game():
    data = request.get_json() or {}
    secret = data.get('secret')
    if not secret:
        return jsonify({'error': 'secret is required'}), 400
    g = Game(secret_b64=encode_secret(secret))
    db.session.add(g)
    db.session.commit()
    return jsonify({'game_id': g.id}), 201


@app.route('/games/<int:game_id>/guess', methods=['POST'])
def guess_game(game_id):
    data = request.get_json() or {}
    guess = data.get('guess')
    if not guess:
        return jsonify({'error': 'guess is required'}), 400
    g = Game.query.get(game_id)
    if not g:
        return jsonify({'error': 'game not found'}), 404
    secret = decode_secret(g.secret_b64)

    # compute feedback: correct letters and correct positions
    correct_positions = sum(1 for a, b in zip(secret, guess) if a == b)
    # count letters regardless of position
    secret_counts = {}
    for ch in secret:
        secret_counts[ch] = secret_counts.get(ch, 0) + 1
    guess_counts = {}
    for ch in guess:
        guess_counts[ch] = guess_counts.get(ch, 0) + 1
    common = 0
    for ch, cnt in guess_counts.items():
        common += min(cnt, secret_counts.get(ch, 0))

    if guess == secret:
        return jsonify({'correct': True, 'message': 'Parabéns! senha correta.'})

    return jsonify({
        'correct': False,
        'correct_positions': correct_positions,
        'common_letters': common,
        'message': f'Dicas: {correct_positions} letras na posição correta; {common} letras corretas em qualquer posição.'
    })


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
