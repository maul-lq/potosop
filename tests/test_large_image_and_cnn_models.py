import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from PIL import Image

from mini_photoshop.app import LARGE_IMAGE_UNDO_LIMIT, LARGE_IMAGE_UNDO_PIXEL_THRESHOLD
from mini_photoshop.ml import DEFAULT_MODEL_NAME, MODEL_NAMES, MODEL_SPECS

assert Image.MAX_IMAGE_PIXELS is None
assert LARGE_IMAGE_UNDO_PIXEL_THRESHOLD > 0
assert LARGE_IMAGE_UNDO_LIMIT >= 1

expected = {"MobileNetV2", "ResNet50", "EfficientNetB0", "InceptionV3"}
assert set(MODEL_NAMES) == expected
assert DEFAULT_MODEL_NAME == "MobileNetV2"
for name in expected:
    spec = MODEL_SPECS[name]
    assert spec.input_size[0] > 0
    assert spec.input_size[1] > 0
    assert spec.class_name
    assert spec.module.startswith("tensorflow.keras.applications")

print("large image and cnn model registry tests passed")
