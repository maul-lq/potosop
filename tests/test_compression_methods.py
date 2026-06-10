import sys
from pathlib import Path

import numpy as np

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from backend.main import FEATURES, PROCESSORS
from mini_photoshop import image_processor as ip


def sample_image() -> np.ndarray:
    image = np.zeros((24, 32, 3), dtype=np.uint8)
    image[:, :16] = [20, 20, 20]
    image[:, 16:] = [220, 220, 220]
    return image


def test_custom_compression_statistics_are_valid() -> None:
    image = sample_image()
    stats = [
        ip.huffman_compression_stats(image, "RGB", include_metadata=False),
        ip.huffman_compression_stats(image, "Grayscale", include_metadata=True),
        ip.arithmetic_compression_stats(image, "RGB", include_metadata=False),
        ip.arithmetic_compression_stats(image, "Grayscale", include_metadata=True),
        ip.lzw_compression_stats(image, "RGB", max_dictionary_bits=9),
        ip.lzw_compression_stats(image, "Grayscale", max_dictionary_bits=16),
        ip.rle_compression_stats(image, "RGB", max_run_length=8),
        ip.rle_compression_stats(image, "Grayscale", max_run_length=1024),
    ]
    for result in stats:
        assert result.original_bits > 0
        assert result.total_bits > 0
        assert result.ratio > 0

    assert stats[1].metadata_bits > stats[0].metadata_bits
    assert stats[7].ratio > 1
    assert ip.rle_compression_ratio(image) > 1

    rgba = np.dstack((image, np.full(image.shape[:2], 127, dtype=np.uint8)))
    assert ip.compression_data(rgba, "RGB").size == image.size


def test_web_contract_exposes_and_processes_all_compression_methods() -> None:
    by_key = {feature["key"]: feature for feature in FEATURES}
    expected = {
        "huffman_compression",
        "arithmetic_compression",
        "lzw_compression",
        "rle_compression",
        "quantization",
    }
    assert expected <= by_key.keys()
    assert all(by_key[key]["controls"] for key in expected)

    custom_params = {
        "huffman_compression": {"mode": "Grayscale", "include_metadata": False},
        "arithmetic_compression": {"mode": "RGB", "include_metadata": True},
        "lzw_compression": {"mode": "Grayscale", "max_dictionary_bits": 9},
        "rle_compression": {"mode": "RGB", "max_run_length": 32},
        "quantization": {"levels": 4},
    }
    for feature, params in custom_params.items():
        returned, message = PROCESSORS[feature](sample_image(), params)
        assert returned.shape == sample_image().shape
        assert returned.dtype == np.uint8
        assert message
        if feature != "quantization":
            assert np.array_equal(returned, sample_image())
