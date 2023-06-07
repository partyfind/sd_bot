import os
from datetime import datetime

formatted_date = datetime.today().strftime('%Y-%m-%d')
img_dir = "C:/html/stable-diffusion-webui/outputs/txt2img-images/"+formatted_date
seed = "3439358289"
files = [f for f in os.listdir(img_dir) if seed in f]
print(img_dir)
if len(files) > 0:
    last_file = sorted(files)[-1]
    last_file_name = os.path.splitext(last_file)[0]
    last_file_num = int(last_file_name.split("-")[0])
    last_file_num_next = last_file_num + 1
    print(13)
    print(last_file_num)
    print(last_file_num_next)
    print(f"{last_file_num:05d}-{seed}")
else:
    print("Папка пуста")
if len(os.listdir(img_dir)) == 0:
    print(18)
    print("00000-"+seed)