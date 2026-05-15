"""Optional CNN object recognition using TensorFlow/Keras ImageNet models.

The main application imports and instantiates recognizers lazily when the user
presses the ML button. This keeps the editor usable on computers that only
install the core image-processing dependencies.
"""

from __future__ import annotations

from dataclasses import dataclass
from typing import Callable, Dict, List, Tuple

import numpy as np


@dataclass
class Prediction:
    label: str
    confidence: float


@dataclass(frozen=True)
class ModelSpec:
    name: str
    module: str
    class_name: str
    preprocess_name: str
    decode_name: str
    input_size: Tuple[int, int]


MODEL_SPECS: Dict[str, ModelSpec] = {
    "MobileNetV2": ModelSpec(
        name="MobileNetV2",
        module="tensorflow.keras.applications.mobilenet_v2",
        class_name="MobileNetV2",
        preprocess_name="preprocess_input",
        decode_name="decode_predictions",
        input_size=(224, 224),
    ),
    "ResNet50": ModelSpec(
        name="ResNet50",
        module="tensorflow.keras.applications.resnet50",
        class_name="ResNet50",
        preprocess_name="preprocess_input",
        decode_name="decode_predictions",
        input_size=(224, 224),
    ),
    "EfficientNetB0": ModelSpec(
        name="EfficientNetB0",
        module="tensorflow.keras.applications.efficientnet",
        class_name="EfficientNetB0",
        preprocess_name="preprocess_input",
        decode_name="decode_predictions",
        input_size=(224, 224),
    ),
    "InceptionV3": ModelSpec(
        name="InceptionV3",
        module="tensorflow.keras.applications.inception_v3",
        class_name="InceptionV3",
        preprocess_name="preprocess_input",
        decode_name="decode_predictions",
        input_size=(299, 299),
    ),
}

MODEL_NAMES = tuple(MODEL_SPECS.keys())
DEFAULT_MODEL_NAME = "MobileNetV2"


class CNNRecognizer:
    """ImageNet recognizer with selectable CNN backbone.

    Available models: MobileNetV2, ResNet50, EfficientNetB0, and InceptionV3.
    TensorFlow/Keras may download ImageNet weights on first use if they are not
    already cached on the user's machine.
    """

    def __init__(self, model_name: str = DEFAULT_MODEL_NAME) -> None:
        if model_name not in MODEL_SPECS:
            names = ", ".join(MODEL_NAMES)
            raise ValueError(f"Model CNN tidak dikenal: {model_name}. Pilihan: {names}")

        self.model_name = model_name
        self.spec = MODEL_SPECS[model_name]

        try:
            from importlib import import_module

            module = import_module(self.spec.module)
            model_factory = getattr(module, self.spec.class_name)
            self._preprocess_input: Callable[[np.ndarray], np.ndarray] = getattr(module, self.spec.preprocess_name)
            self._decode_predictions = getattr(module, self.spec.decode_name)
        except Exception as exc:  # pragma: no cover - depends on optional package
            raise RuntimeError(
                "Fitur CNN membutuhkan TensorFlow. Instal opsional dengan: "
                "pip install -r requirements-ml.txt"
            ) from exc

        self._model = model_factory(weights="imagenet")

    def predict(self, image_rgb: np.ndarray, top_k: int = 5) -> List[Prediction]:
        from cv2 import resize

        top_k = max(1, min(int(top_k), 10))
        width, height = self.spec.input_size
        resized = resize(image_rgb, (width, height)).astype(np.float32)
        batch = np.expand_dims(resized, axis=0)
        batch = self._preprocess_input(batch)
        preds = self._model.predict(batch, verbose=0)
        decoded = self._decode_predictions(preds, top=top_k)[0]
        return [Prediction(label=item[1].replace("_", " "), confidence=float(item[2])) for item in decoded]
