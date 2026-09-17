import os
import numpy as np
import tensorflow as tf

models_dir = "D:/workspace/btp/folder_manager/models"
model_path = os.path.join(models_dir, "image_classifier_model.h5")

print("Loading model:", model_path)
model = tf.keras.models.load_model(model_path)

print("\nModel summary:")
model.summary()

print("\nLayer details:")
for layer in model.layers:
    # Safely get shapes
    try:
        inp_shape = getattr(layer, 'input_shape', None)
    except Exception:
        inp_shape = None
    print(f"- {layer.name}: type={layer.__class__.__name__}, input_shape={inp_shape}")

from tensorflow.keras.applications.mobilenet_v2 import preprocess_input

# Prepare a zero image and run predict to reproduce error
img = np.zeros((1, 224, 224, 3), dtype=np.float32)
img = preprocess_input(img)

print("\nCalling model.predict on a zero image to reproduce any runtime errors...")
try:
    preds = model.predict(img)
    print("Predict successful. Output shape:", getattr(preds, 'shape', None))
except Exception as e:
    print("Error during predict:")
    import traceback
    traceback.print_exc()

print("Done.")
