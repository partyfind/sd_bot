import json

data = {
    "enable_hr": False,
    "prompt": "",
    "subseed_strength2": "3434",
    "seed": -1,
    "override_settings_restore_afterwards": -1,
    "subseed_strength": 0
}

str = '/seed 555 77 prompt prompt6'
substring = ''

for key in data:
    if key in str:
        substring = str[str.index(key) + len(key):]

print(found)
print(substring)