import os
import json
import numpy as np
import tensorflow as tf
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Dense, GlobalAveragePooling2D, Dropout
from tensorflow.keras.applications import MobileNetV2
from tensorflow.keras.applications.mobilenet_v2 import preprocess_input

models_dir = "D:/workspace/btp/folder_manager/models"
weights_path = os.path.join(models_dir, "image_classifier_model.h5")
labels_path = os.path.join(models_dir, "class_labels.json")

with open(labels_path, 'r') as f:
    class_labels = json.load(f)

num_classes = len(class_labels)

print(f"Reconstructing model with {num_classes} classes...")
IMG_HEIGHT, IMG_WIDTH = 224, 224

base_model = MobileNetV2(weights='imagenet', include_top=False, input_shape=(IMG_HEIGHT, IMG_WIDTH, 3))
base_model.trainable = False

model = Sequential([
    base_model,
    GlobalAveragePooling2D(),
    Dropout(0.3),
    Dense(256, activation='relu'),
    Dropout(0.3),
    Dense(num_classes, activation='softmax')
])

print('Model reconstructed. Loading weights from HDF5...')
try:
    model.load_weights(weights_path)
    print('Weights loaded successfully.')
except Exception as e:
    print('Error loading weights:', e)
    raise

print('Running a dummy predict...')
img = np.zeros((1, IMG_HEIGHT, IMG_WIDTH, 3), dtype=np.float32)
img = preprocess_input(img)
preds = model.predict(img)
print('Predict output shape:', preds.shape)
print('Top predicted index:', int(preds.argmax()))
