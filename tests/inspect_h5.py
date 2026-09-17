import os
import json
import h5py

models_dir = "D:/workspace/btp/folder_manager/models"
model_path = os.path.join(models_dir, "image_classifier_model.h5")

print("Opening HDF5 model:", model_path)
with h5py.File(model_path, 'r') as f:
    # Try several locations for config
    model_config = None
    if 'model_config' in f.attrs:
        raw = f.attrs['model_config']
        if isinstance(raw, (bytes, bytearray)):
            raw = raw.decode('utf-8')
        model_config = json.loads(raw)
    elif 'model_config' in f:
        raw = f['model_config'][()]
        if isinstance(raw, (bytes, bytearray)):
            raw = raw.decode('utf-8')
        model_config = json.loads(raw)
    else:
        # Some Keras versions store as json in 'keras_metadata' or attrs
        if 'keras_metadata' in f.attrs:
            try:
                raw = f.attrs['keras_metadata']
                if isinstance(raw, (bytes, bytearray)):
                    raw = raw.decode('utf-8')
                meta = json.loads(raw)
                model_config = meta.get('model_config')
            except Exception:
                model_config = None

    if model_config is None:
        print("Could not find model_config in HDF5 file. Printing root keys:")
        print(list(f.keys()))
        raise SystemExit(1)

    # For Sequential models the layers are usually under model_config['config']['layers']
    layers = None
    try:
        layers = model_config['config'].get('layers') or model_config['config'].get('layers', [])
    except Exception:
        # fallback for nested formats
        try:
            layers = model_config.get('config', {}).get('layers', [])
        except Exception:
            layers = []

    if not layers:
        # Try functional model format
        layers = model_config.get('config', {}).get('layers', [])

    print(f"Found {len(layers)} layer entries in config")

    for i, layer in enumerate(layers):
        name = layer.get('config', {}).get('name') or layer.get('name') or f"layer_{i}"
        class_name = layer.get('class_name') or layer.get('class_name')
        inbound = layer.get('inbound_nodes') if 'inbound_nodes' in layer else layer.get('inbound_nodes', [])
        print(f"{i:03d}: name={name}, class={class_name}")
        # Print inbound nodes shape/length
        try:
            if inbound:
                print("    inbound_nodes:")
                for node_group in inbound:
                    print("      node_group:")
                    for node in node_group:
                        print(f"        {node}")
        except Exception as e:
            print("    error reading inbound_nodes:", e)

    # Extra: look specifically for Dense layers
    print("\nDense layer details:")
    for layer in layers:
        class_name = layer.get('class_name')
        if class_name == 'Dense':
            name = layer.get('config', {}).get('name')
            inbound = layer.get('inbound_nodes')
            print(f"Dense '{name}' inbound_nodes count: {len(inbound) if inbound is not None else 0}")
            print(json.dumps(layer.get('config', {}), indent=2)[:1000])

print("Done.")
