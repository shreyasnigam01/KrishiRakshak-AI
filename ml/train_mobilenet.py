import os
import json
import copy
import torch
import torch.nn as nn
import torch.optim as optim
from torch.utils.data import DataLoader
from torchvision import datasets, models, transforms
from collections import Counter

def train():
    # --- CONFIGURATION ---
    DATA_DIR = "data/dataset"
    TRAIN_DIR = os.path.join(DATA_DIR, "train")
    VAL_DIR = os.path.join(DATA_DIR, "val") if os.path.exists(os.path.join(DATA_DIR, "val")) else TRAIN_DIR
    MODEL_SAVE_PATH = "ml/model.pth"
    CLASS_MAPPING_PATH = "data/class_names.json"

    BATCH_SIZE = 32
    EPOCHS_WARMUP = 5      # Train classifier head only
    EPOCHS_FINETUNE = 15   # Fine-tune backbone + head
    IMAGE_SIZE = 224

    DEVICE = torch.device("mps" if torch.backends.mps.is_available() else ("cuda" if torch.cuda.is_available() else "cpu"))
    print(f"Using Compute Device: {DEVICE}")

    # --- ROBUST DATA AUGMENTATION ---
    train_transforms = transforms.Compose([
        transforms.RandomResizedCrop(IMAGE_SIZE, scale=(0.7, 1.0)),
        transforms.RandomHorizontalFlip(p=0.5),
        transforms.RandomVerticalFlip(p=0.3),
        transforms.RandomRotation(degrees=25),
        transforms.ColorJitter(brightness=0.3, contrast=0.3, saturation=0.3, hue=0.1),
        transforms.RandomPerspective(distortion_scale=0.2, p=0.4),
        transforms.GaussianBlur(kernel_size=(3, 3), sigma=(0.1, 2.0)),
        transforms.ToTensor(),
        transforms.Normalize([0.485, 0.456, 0.406], [0.229, 0.224, 0.225])
    ])

    val_transforms = transforms.Compose([
        transforms.Resize((IMAGE_SIZE, IMAGE_SIZE)),
        transforms.ToTensor(),
        transforms.Normalize([0.485, 0.456, 0.406], [0.229, 0.224, 0.225])
    ])

    # --- DATASET & CLASS WEIGHTS ---
    train_dataset = datasets.ImageFolder(TRAIN_DIR, transform=train_transforms)
    val_dataset = datasets.ImageFolder(VAL_DIR, transform=val_transforms)

    # num_workers=0 avoids macOS multiprocessing spawn crashes
    train_loader = DataLoader(train_dataset, batch_size=BATCH_SIZE, shuffle=True, num_workers=0)
    val_loader = DataLoader(val_dataset, batch_size=BATCH_SIZE, shuffle=False, num_workers=0)

    class_names = train_dataset.classes
    num_classes = len(class_names)
    print(f"Detected {num_classes} classes: {class_names}")

    # Save class indices for inference synchronization
    os.makedirs("data", exist_ok=True)
    with open(CLASS_MAPPING_PATH, "w", encoding="utf-8") as f:
        json.dump(class_names, f, indent=4)
    print(f"Class mapping exported to {CLASS_MAPPING_PATH}")

    # Handle class imbalance via weighted cross-entropy
    class_counts = Counter(train_dataset.targets)
    total_samples = len(train_dataset)
    class_weights = [total_samples / max(class_counts[i], 1) for i in range(num_classes)]
    class_weights_tensor = torch.tensor(class_weights, dtype=torch.float).to(DEVICE)

    # --- MODEL INITIALIZATION WITH PRETRAINED WEIGHTS ---
    model = models.mobilenet_v2(weights=models.MobileNet_V2_Weights.DEFAULT)

    # Replace classifier head with dropout regularization
    model.classifier = nn.Sequential(
        nn.Dropout(p=0.3),
        nn.Linear(model.last_channel, 256),
        nn.ReLU(inplace=True),
        nn.Dropout(p=0.2),
        nn.Linear(256, num_classes)
    )
    model = model.to(DEVICE)

    criterion = nn.CrossEntropyLoss(weight=class_weights_tensor, label_smoothing=0.1)

    # --- PHASE 1: WARM-UP (CLASSIFIER HEAD ONLY) ---
    print("\n--- PHASE 1: Warm-up Classifier Head ---")
    for param in model.features.parameters():
        param.requires_grad = False

    optimizer_head = optim.AdamW(model.classifier.parameters(), lr=1e-3, weight_decay=1e-4)

    for epoch in range(EPOCHS_WARMUP):
        model.train()
        running_loss, correct, total = 0.0, 0, 0
        
        for inputs, labels in train_loader:
            inputs, labels = inputs.to(DEVICE), labels.to(DEVICE)
            optimizer_head.zero_grad()
            
            outputs = model(inputs)
            loss = criterion(outputs, labels)
            loss.backward()
            optimizer_head.step()
            
            running_loss += loss.item() * inputs.size(0)
            _, preds = torch.max(outputs, 1)
            correct += torch.sum(preds == labels.data).item()
            total += labels.size(0)
            
        epoch_loss = running_loss / total
        epoch_acc = (correct / total) * 100
        print(f"Warmup Epoch [{epoch+1}/{EPOCHS_WARMUP}] - Loss: {epoch_loss:.4f} - Acc: {epoch_acc:.2f}%")

    # --- PHASE 2: FINE-TUNING (TOP BACKBONE LAYERS + HEAD) ---
    print("\n--- PHASE 2: Fine-Tuning Top Convolutional Layers ---")
    for layer in model.features[-4:]:
        for param in layer.parameters():
            param.requires_grad = True

    optimizer_finetune = optim.AdamW([
        {"params": model.features[-4:].parameters(), "lr": 1e-4},
        {"params": model.classifier.parameters(), "lr": 5e-4}
    ], weight_decay=1e-4)

    scheduler = optim.lr_scheduler.CosineAnnealingLR(optimizer_finetune, T_max=EPOCHS_FINETUNE, eta_min=1e-6)

    best_val_acc = 0.0
    best_model_weights = copy.deepcopy(model.state_dict())

    for epoch in range(EPOCHS_FINETUNE):
        model.train()
        train_loss, train_correct, train_total = 0.0, 0, 0
        
        for inputs, labels in train_loader:
            inputs, labels = inputs.to(DEVICE), labels.to(DEVICE)
            optimizer_finetune.zero_grad()
            
            outputs = model(inputs)
            loss = criterion(outputs, labels)
            loss.backward()
            optimizer_finetune.step()
            
            train_loss += loss.item() * inputs.size(0)
            _, preds = torch.max(outputs, 1)
            train_correct += torch.sum(preds == labels.data).item()
            train_total += labels.size(0)
            
        scheduler.step()
        
        # Validation Loop
        model.eval()
        val_loss, val_correct, val_total = 0.0, 0, 0
        
        with torch.no_grad():
            for inputs, labels in val_loader:
                inputs, labels = inputs.to(DEVICE), labels.to(DEVICE)
                outputs = model(inputs)
                loss = criterion(outputs, labels)
                
                val_loss += loss.item() * inputs.size(0)
                _, preds = torch.max(outputs, 1)
                val_correct += torch.sum(preds == labels.data).item()
                val_total += labels.size(0)
                
        train_acc = (train_correct / train_total) * 100
        val_acc = (val_correct / val_total) * 100 if val_total > 0 else 0.0
        
        print(f"Epoch [{epoch+1:02d}/{EPOCHS_FINETUNE:02d}] | Train Loss: {train_loss/train_total:.4f} Acc: {train_acc:.2f}% | Val Loss: {val_loss/val_total:.4f} Val Acc: {val_acc:.2f}%")
        
        if val_acc >= best_val_acc:
            best_val_acc = val_acc
            best_model_weights = copy.deepcopy(model.state_dict())

    # --- SAVE BEST MODEL ---
    os.makedirs("ml", exist_ok=True)
    torch.save(best_model_weights, MODEL_SAVE_PATH)
    print(f"\nTraining complete! Best validation accuracy: {best_val_acc:.2f}%")
    print(f"Saved optimized model weights to: {MODEL_SAVE_PATH}")

if __name__ == "__main__":
    train()