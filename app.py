from flask import Flask, request, jsonify
import numpy as np
from PIL import Image
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
    image = Image.open(io.BytesIO(file))

    # Define center and radius for the pentagon
    center = (250, 250)  # Center of the pentagon
    radius = 100  # Radius of the circle on which the pentagon is inscribed

    # Generate pentagon vertices
    pentagon_polyline = generate_polygon(center, radius, num_sides=5)

    # Return the polygon vertices
    return jsonify(pentagon_polyline)

if __name__ == '__main__':
    app.run(debug=True)
