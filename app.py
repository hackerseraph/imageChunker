import os
pip install -r requirements.txt
from flask import Flask, render_template, request  
from PIL import Image
import math
from datetime import datetime

app = Flask(__name__, static_folder="static")

date_format = '%Y-%m-%d-%H-%M-%S' 

@app.route("/")
def index():
  return render_template("index.html")

@app.route("/process", methods=["POST"])
def process():

  now = datetime.now()
  original_filename = f"original_{now.strftime(date_format)}.jpg"
  
  app_dir = os.path.dirname(os.path.abspath(__file__))
  original_path = os.path.join(app_dir, 'originals', original_filename)  

  img = request.files["image"]
  img.save(original_path)

  original = Image.open(original_path)

  width, height = original.size
  ratio = height / width
  new_width = 500
  new_height = int(new_width * ratio)
  resized = original.resize((new_width, new_height))

  block_count = math.ceil(new_height / 500)

  for i in range(block_count):
    left = 0
    top = i*500
    right = 500
    bottom = (i+1)*500
    block = resized.crop((left, top, right, bottom))
    
    save_path = os.path.join(app_dir, 'static', f'block_{i}.jpg')
    
    block.save(save_path)

  return "Processed into {} blocks".format(block_count)

if __name__ == "__main__":
  app.run(debug=True)