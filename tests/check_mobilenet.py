from tensorflow.keras.applications import MobileNetV2

print('Instantiating MobileNetV2 (include_top=False)...')
model = MobileNetV2(weights='imagenet', include_top=False, input_shape=(224,224,3))

print('Model type:', type(model))
try:
    outs = model.outputs
    print('Number of outputs:', len(outs))
    for i, o in enumerate(outs):
        print(f' output[{i}]:', o)
except Exception as e:
    print('Error reading outputs:', e)

print('\nModel summary head:')
model.summary(line_length=120)
