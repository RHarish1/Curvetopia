from flask import Flask, request, jsonify
import numpy as np
from PIL import Image, ImageDraw
import io

app = Flask(__name__)

# Function to generate vertices of a regular polygon
def generate_polygon(center, radius, num_sides):
    angle = 360 / num_sides  # Angle between vertices
    vertices = []
    for i in range(num_sides):
        x = center[0] + int(radius * np.cos(np.deg2rad(i * angle)))
        y = center[1] + int(radius * np.sin(np.deg2rad(i * angle)))
        vertices.append((x, y))
    return vertices

@app.route('/analyze', methods=['POST'])
def analyze_image():
    # Load image
    file = request.files['image'].read()
    image = Image.open(io.BytesIO(file)).convert('RGBA')

    # Define center and radius for the pentagon
    width, height = image.size
    center = (width // 2, height // 2)
    radius = min(center) // 2

    # Generate pentagon vertices
    pentagon_vertices = generate_polygon(center, radius, num_sides=5)

    # Draw pentagon on image
    draw = ImageDraw.Draw(image)
    draw.polygon(pentagon_vertices, outline="red")

    # Convert image to byte array
    img_byte_arr = io.BytesIO()
    image.save(img_byte_arr, format='PNG')
    img_byte_arr = img_byte_arr.getvalue()

    # Encode image in base64 to return as JSON
    encoded_img = base64.b64encode(img_byte_arr).decode('utf-8')

    return jsonify({"vertices": pentagon_vertices, "image": encoded_img})

if __name__ == '__main__':
    app.run(debug=True)
