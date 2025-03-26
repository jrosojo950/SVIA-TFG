from flask import Flask, render_template, request, jsonify
import os

app = Flask(__name__)

PHOTO_FOLDER = "static/fotos"

@app.route('/')
def index():
    photos = sorted(os.listdir(PHOTO_FOLDER), reverse=True)
    return render_template('index.html', photos=photos)

@app.route('/delete/<photo_name>', methods=['DELETE'])
def delete_photo(photo_name):
    try:
        photo_path = os.path.join(PHOTO_FOLDER, photo_name)
        if os.path.exists(photo_path):
            os.remove(photo_path)
            return jsonify({"success": True})
        else:
            return jsonify({"success": False, "error": "Archivo no encontrado"}), 404
    except Exception as e:
        return jsonify({"success": False, "error": str(e)}), 500

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
