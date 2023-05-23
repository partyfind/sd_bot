import json
data = {
  "enable_hr": False,
  "prompt": "",
  "styles": [
    "string"
  ],
  "seed": -1,
  "subseed": -1,
  "subseed_strength": 0,
  "seed_resize_from_h": -1,
  "seed_resize_from_w": -1,
  "sampler_name": "string",
  "steps": 50,
  "cfg_scale": 7,
  "width": 512,
  "height": 512,
  "override_settings": {},
  "override_settings_restore_afterwards": True,
  "script_args": [],
  "alwayson_scripts": {}
}
print('____')
print(data)
print('____')
data["height"] = 256
for key, value in data.items():
    print('key = '+key)
print('____')
print(data)