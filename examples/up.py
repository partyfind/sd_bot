import json
import requests
import io
import base64
import gzip
import urllib3
from PIL import Image, PngImagePlugin
from io import BytesIO

pil_image = Image.open("C:\OSPanel\domains\sd\examples\dog.png")
#Convert image to base64
def pil_to_base64(pil_image):
    with BytesIO() as stream:
        pil_image.save(stream, "PNG", pnginfo=None)
        base64_str = str(base64.b64encode(stream.getvalue()), "utf-8")
        return "data:image/png;base64," + base64_str

payload = {
"resize_mode": 0,
  "show_extras_results": True,
  "gfpgan_visibility": 0,
  "codeformer_visibility": 0,
  "codeformer_weight": 0,
  "upscaling_resize": 2,
  "upscaling_resize_w": 512,
  "upscaling_resize_h": 512,
  "upscaling_crop": True,
  "upscaler_1": "R-ESRGAN 4x+",
  "upscaler_2": "None",
  "extras_upscaler_2_visibility": 0,
  "upscale_first": False,
  "image": [pil_to_base64(pil_image)]
}

response = requests.post('http://127.0.0.1:7861/sdapi/v1/extra-single-image', json.dumps(payload))

#r = response.json()
#print(response.content)
#response = requests.get('your-url-here')
data = urllib3.response.GzipDecoder().decompress(response.content)
print(data)  # decoded contents of page
#for item in response.json()['detail'][0]:
#    print(item[0])
#Image.open(io.BytesIO(base64.b64decode(r['image'].split(",",1)[0]))).save('Upscaled.png')