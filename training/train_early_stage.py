import os
import json
import torch
import torch.nn as nn
from torchvision import datasets, transforms, models
from torch.utils.data import DataLoader

DEVICE = torch.device("mps" if torch.backends.mps.is_available() else ("cuda" if torch.cuda.is_available() else "cpu"))
MODEL_PATH = "ml/model.pth"
DATA_DIR = "data/early_stage_dataset"

# Load the existing class mapping
CLASS_MAP_PATH = "data/dataset/class_names.json"
if not os.path.exists(CLASS_MAP_PATH):
    CLASS_MAP_PATH = "data/class_names.json"

with open(CLASS_MAP_PATH, "r") as f:
    CLASSES = json.load(f)

# Heavy augmentation for very small sample sets
train_transform = transforms.Compose([
    transforms.Resize((224, 224)),
    transforms.RandomHorizontalFlip(p=0.5),
    transforms.RandomVerticalFlip(p=0.5),
    transforms.RandomRotation(degrees=30),
    transforms.ColorJitter(brightness=0.2, contrast=0.2),
    transforms.ToTensor(),
    transforms.Normalize([0.485, 0.456, 0.406], [0.229, 0.224, 0.225])
])

dataset = datasets.ImageFolder(DATA_DIR, transform=train_transform)

# Map the two new folder names directly to the original model class indices
TARGET_INDEX_MAP = {
    "earlystage_brownhopper": CLASSES.index("brown_planthopper"),
    "earlystage_cottonboll": CLASSES.index("bollworm")
}

# Re-map dataset targets to the exact 14-class indices
remapped_samples = []
for path, target in dataset.samples:
    folder_name = dataset.classes[target]
    if folder_name in TARGET_INDEX_MAP:
        remapped_samples.append((path, TARGET_INDEX_MAP[folder_name]))

dataset.samples = remapped_samples
dataset.targets = [s[1] for s in remapped_samples]

loader = DataLoader(dataset, batch_size=2, shuffle=True)

# Load existing MobileNetV2 without changing structure
model = models.mobilenet_v2(weights=None)
model.classifier = nn.Sequential(
    nn.Dropout(p=0.3),
    nn.Linear(model.last_channel, 256),
    nn.ReLU(inplace=True),
    nn.Dropout(p=0.2),
    nn.Linear(256, len(CLASSES))
)

if os.path.exists(MODEL_PATH):
    state = torch.load(MODEL_PATH, map_location=DEVICE, weights_only=True)
    model.load_state_dict(state)

# Freeze feature extraction layers so original knowledge remains intact
for param in model.features.parameters():
    param.requires_grad = False

model.to(DEVICE)
model.train()

criterion = nn.CrossEntropyLoss()
optimizer = torch.optim.AdamW(model.classifier.parameters(), lr=5e-5, weight_decay=1e-3)

print(f"Fine-tuning early stage detection on {DEVICE}...")
for epoch in range(15):
    running_loss = 0.0
    for images, labels in loader:
        images, labels = images.to(DEVICE), labels.to(DEVICE)
        optimizer.zero_grad()
        outputs = model(images)
        loss = criterion(outputs, labels)
        loss.backward()
        optimizer.step()
        running_loss += loss.item()

    if (epoch + 1) % 5 == 0:
        print(f"Epoch {epoch+1:02d}/15 - Loss: {running_loss:.4f}")

torch.save(model.state_dict(), MODEL_PATH)
print("Updated weights saved to ml/model.pth successfully.")