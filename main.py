import firebase_admin
from firebase_admin import firestore
import flask

app = flask.Flask(__name__)

firebase_admin.initialize_app()
TRACKS = firestore.client().collection('tracks')

@app.route('/tracks', methods=['POST'])
def create_track():
    req = flask.request.json
    track = TRACKS.document()
    track.set(req)
    return flask.jsonify({'id': track.id}), 201

@app.route('/tracks/<id>')
def read_track(id):
    return flask.jsonify(_ensure_track(id).to_dict())

@app.route('/tracks/<id>', methods=['PUT'])
def update_track(id):
    _ensure_track(id)
    req = flask.request.json
    TRACKS.document(id).set(req)
    return flask.jsonify({'success': True})

@app.route('/tracks/<id>', methods=['DELETE'])
def delete_track(id):
    _ensure_track(id)
    TRACKS.document(id).delete()
    return flask.jsonify({'success': True})

def _ensure_track(id):
    try:
        return TRACKS.document(id).get()
    except:
        flask.abort(404)

if __name__ == '__main__':
    app.run(host='127.0.0.1', port=8080, debug=True)