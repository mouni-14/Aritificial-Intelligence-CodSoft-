import os
from flask import Flask, render_template, request, redirect, url_for
from transformers import BlipProcessor, BlipForConditionalGeneration
from PIL import Image

# Initialize Flask
app = Flask(__name__)
UPLOAD_FOLDER = "static/uploads"
os.makedirs(UPLOAD_FOLDER, exist_ok=True)
app.config["UPLOAD_FOLDER"] = UPLOAD_FOLDER

# Load BLIP model once
processor = BlipProcessor.from_pretrained("Salesforce/blip-image-captioning-base")
model = BlipForConditionalGeneration.from_pretrained("Salesforce/blip-image-captioning-base")

@app.route("/", methods=["GET", "POST"])
def index():
    caption = None
    image_url = None

    if request.method == "POST":
        if "image" not in request.files:
            return redirect(request.url)
        file = request.files["image"]
        if file.filename == "":
            return redirect(request.url)

        if file:
            # Save uploaded image
            filepath = os.path.join(app.config["UPLOAD_FOLDER"], file.filename)
            file.save(filepath)
            image_url = url_for("static", filename=f"uploads/{file.filename}")

            # Open and caption the image
            image = Image.open(filepath).convert("RGB")
            inputs = processor(images=image, return_tensors="pt")
            out = model.generate(**inputs)
            caption = processor.decode(out[0], skip_special_tokens=True)

    return render_template("index.html", caption=caption, image_url=image_url)

if __name__ == "__main__":
    app.run(debug=True)
