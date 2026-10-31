import os
import shutil
import random

SOURCE_DIR = "original_data"
BASE_DATASET = "data/dataset"
TRAIN_DIR = os.path.join(BASE_DATASET, "train")
VAL_DIR = os.path.join(BASE_DATASET, "val")
SPLIT_RATIO = 0.8

# Case-insensitive mapping for the remaining 3 folders
REMAINDER_MAP = {
    "green_leafhoppers": "green_leafhopper",
    "leaf_folders": "leaf_folder",
    "stemz_borer": "stem_borer"
}

random.seed(42)

for folder in os.listdir(SOURCE_DIR):
    clean_key = folder.strip().lower()
    if clean_key in REMAINDER_MAP:
        clean_name = REMAINDER_MAP[clean_key]
        src_path = os.path.join(SOURCE_DIR, folder)

        images = [f for f in os.listdir(src_path) if f.lower().endswith(('.png', '.jpg', '.jpeg'))]
        random.shuffle(images)

        split_idx = int(len(images) * SPLIT_RATIO)
        train_imgs = images[:split_idx]
        val_imgs = images[split_idx:]

        dst_train = os.path.join(TRAIN_DIR, clean_name)
        dst_val = os.path.join(VAL_DIR, clean_name)
        os.makedirs(dst_train, exist_ok=True)
        os.makedirs(dst_val, exist_ok=True)

        for img in train_imgs:
            shutil.copy(os.path.join(src_path, img), os.path.join(dst_train, img))
        for img in val_imgs:
            shutil.copy(os.path.join(src_path, img), os.path.join(dst_val, img))

        print(f"Added [{clean_name}] -> Train: {len(train_imgs)} | Val: {len(val_imgs)}")

print("Done. Check total folders in train.")