"""Print evidence about the ImageNet CNN models used by this application.

Run:
    python verify_cnn_models.py

Each model is loaded with ``weights="imagenet"``, exactly like
``mini_photoshop.ml.CNNRecognizer``. TensorFlow automatically downloads the
weights to its local cache when they are not available yet.
"""

from __future__ import annotations

import gc
import inspect
import os
from collections import Counter
from importlib import import_module
from pathlib import Path
from typing import Any

import tensorflow as tf

from mini_photoshop.ml import CNNRecognizer, MODEL_SPECS


def format_default(value: Any) -> str:
    """Return a compact representation of a constructor default value."""
    if value is inspect.Parameter.empty:
        return "<required>"
    return repr(value)


def print_application_evidence() -> None:
    """Print the application's model-loading statement."""
    source_file = inspect.getsourcefile(CNNRecognizer) or "<unknown>"
    source_lines, start_line = inspect.getsourcelines(CNNRecognizer.__init__)

    print("=" * 88)
    print("BUKTI KONFIGURASI APLIKASI")
    print("=" * 88)
    for offset, line in enumerate(source_lines):
        if 'model_factory(weights="imagenet")' in line:
            line_number = start_line + offset
            print(f"File       : {source_file}:{line_number}")
            print(f"Pemanggilan: {line.strip()}")
            print("Kesimpulan : aplikasi meminta bobot pretrained ImageNet.")
            return

    raise RuntimeError('Pemanggilan model_factory(weights="imagenet") tidak ditemukan.')


def inspect_model(model_name: str) -> None:
    """Load and print evidence for one configured CNN model."""
    spec = MODEL_SPECS[model_name]
    module = import_module(spec.module)
    model_factory = getattr(module, spec.class_name)
    signature = inspect.signature(model_factory)

    print("\n" + "=" * 88)
    print(model_name)
    print("=" * 88)
    print(f"Factory       : {spec.module}.{spec.class_name}")
    print(f"Input aplikasi: {spec.input_size[0]} x {spec.input_size[1]}")
    print('Bobot dimuat  : weights="imagenet" (akan di-download otomatis jika belum ada)')

    relevant_defaults = (
        "include_top",
        "weights",
        "pooling",
        "classes",
        "classifier_activation",
    )
    print("\nDefault constructor:")
    for parameter_name in relevant_defaults:
        parameter = signature.parameters.get(parameter_name)
        if parameter is not None:
            print(f"  {parameter_name:<22} = {format_default(parameter.default)}")

    model = model_factory(weights="imagenet")
    layer_type_counts = Counter(type(layer).__name__ for layer in model.layers)
    pooling_counts = {
        layer_type: count
        for layer_type, count in layer_type_counts.items()
        if "Pooling" in layer_type
    }
    pooling_layers = [
        f"{type(layer).__name__}: {layer.name}"
        for layer in model.layers
        if "Pooling" in type(layer).__name__
    ]

    final_layer = model.layers[-1]
    final_activation = getattr(
        getattr(final_layer, "activation", None),
        "__name__",
        "<tidak ada>",
    )

    print("\nHasil model yang dimuat:")
    print(f"  Jumlah layer Keras : {len(model.layers):,}")
    print(f"  Jumlah parameter   : {model.count_params():,}")
    print(f"  Bentuk output      : {model.output_shape}")
    print(f"  Layer terakhir     : {type(final_layer).__name__}: {final_layer.name}")
    print(f"  Aktivasi terakhir  : {final_activation}")
    print(f"  Jenis pooling      : {pooling_counts or 'tidak ada'}")
    print("  Daftar pooling:")
    for pooling_layer in pooling_layers:
        print(f"    - {pooling_layer}")

    assert final_activation == "softmax", (
        f"{model_name}: aktivasi terakhir bukan softmax, tetapi {final_activation!r}"
    )
    assert model.output_shape[-1] == 1000, (
        f"{model_name}: output bukan 1.000 kelas ImageNet: {model.output_shape}"
    )
    print("  Verifikasi         : PASS - softmax dengan output 1.000 kelas ImageNet")

    del model
    tf.keras.backend.clear_session()
    gc.collect()


def main() -> None:
    keras_home = Path(os.environ.get("KERAS_HOME", Path.home() / ".keras"))

    print(f"TensorFlow version : {tf.__version__}")
    print(f"Cache Keras        : {keras_home}")
    print(
        "Catatan            : proses pertama dapat mengunduh bobot ImageNet; "
        "proses berikutnya memakai cache."
    )

    print_application_evidence()
    for model_name in MODEL_SPECS:
        inspect_model(model_name)

    print("\n" + "=" * 88)
    print("SEMUA PEMERIKSAAN PASS")
    print("=" * 88)


if __name__ == "__main__":
    main()
