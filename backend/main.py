from flask import Flask, jsonify, request
from flask_cors import CORS
from PIL import Image
import numpy as np
from tensorflow.keras.models import load_model
import io, json

main = Flask(__name__)
CORS(main)

model = load_model("best_model.keras")
print(f"Model loaded successfully: {model}")

with open ("labels.json", "r") as l:
    labels = json.load(l)

def split_image_into_grid(image, r=3, c=3):
    w, h = image.size
    tile_w, tile_h = w // c, h // r

    tiles = []
    for i in range(r):
        for j in range(c):
            left = j * tile_w
            upper = i * tile_h
            right = (j + 1) * tile_w
            lower = (i + 1) * tile_h
            tile = image.crop((left, upper, right, lower))
            tiles.append(tile)

    return tiles

def decode_prediction(prediction):
    idx = int(np.argmax(prediction))
    label = labels[str(idx)]
    return label

def predict_objects(tiles, model, size=(150,150)):
    res = []
    batch = []
    for tile in tiles:
        tile = tile.resize(size)
        tile = tile.convert("RGB")
        img_array = np.array(tile) / 255.0
        batch.append(img_array)
    batch = np.array(batch)
    predictions = model.predict(batch)
    for pred in predictions:
        label = decode_prediction(pred)
        res.append(label)
    return res

@main.route("/predict_captcha", methods=["POST"])
def detect_captcha():
    try:
        if 'image' not in request.files or 'target' not in request.form:
            return jsonify({'error': 'Image and Target required'}), 400
        
        file = request.files['image']
        target_label = request.form['target'].lower()

        img = Image.open(io.BytesIO(file.read()))
        tiles = split_image_into_grid(img)
        detections = predict_objects(tiles, model)

        print(f"Model detections", detections)

        # Check match found and return the location of the objects in the image
        matched_indices = [i for i, det in enumerate(detections) if det.lower() == target_label.lower()]
        match_found = len(matched_indices) > 0
        matched_label = detections[matched_indices[0]] if match_found else None

        return jsonify({
            "match_found": match_found,
            "matched_label": matched_label,
            "detections": detections,
            "matched_positions": matched_indices
        })

    except Exception as e:
        print("Error:", e)
        return jsonify({'error': str(e)}), 500

if __name__ == "__main__":
    main.run(host="0.0.0.0", port="9000", debug=True)