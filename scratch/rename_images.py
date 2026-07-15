
import os
import shutil

mapping = {
    "emu_war_illustration_1777543576186.png": "0.png",
    "insomnia_illustration_1777543601975.png": "1.png",
    "mirror_illustration_1777543621028.png": "2.png",
    "coffee_history_3_1777604501142.png": "3.png",
    "quietest_room_4_1777604518346.png": "4.png",
    "ten_yen_coin_10_1777604550328.png": "10.png",
    "brinicle_11_1777604627418.png": "11.png",
    "codex_atlanticus_12_1777604749482.png": "12.png",
    "tartar_sauce_13_1777604809489.png": "13.png"
}

image_dir = 'images'
for old_name, new_name in mapping.items():
    old_path = os.path.join(image_dir, old_name)
    new_path = os.path.join(image_dir, new_name)
    if os.path.exists(old_path):
        print(f"Renaming {old_name} to {new_name}")
        shutil.move(old_path, new_path)
    else:
        print(f"Skipping {old_name} (not found)")
