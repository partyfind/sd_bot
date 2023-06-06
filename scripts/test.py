import os
from datetime import datetime

formatted_date = datetime.today().strftime('%Y-%m-%d')
img_dir = "C:/html/stable-diffusion-webui/outputs/txt2img-images/"+formatted_date
seed = "770102060"
files = [f for f in os.listdir(img_dir) if seed in f]
print(img_dir)
if len(files) > 0:
    last_file = sorted(files)[-1]
    last_file_name = os.path.splitext(last_file)[0]
    last_file_num = int(last_file_name.split("-")[0]) + 1
    print(f"{last_file_num:05d}-{seed}")
else:
    print("Папка пуста")
if len(os.listdir(img_dir)) == 0:
    print("00000-"+seed)