import sys
from pathlib import Path
from dataclasses import dataclass

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from mini_photoshop.app import format_predictions, prediction_to_label_score


@dataclass
class DummyPrediction:
    label: str
    confidence: float


label, confidence = prediction_to_label_score(DummyPrediction('tabby cat', 0.8123))
assert label == 'tabby cat'
assert abs(confidence - 0.8123) < 1e-9

label, confidence = prediction_to_label_score(('n02123045', 'tabby_cat', 0.8123))
assert label == 'tabby cat'
assert abs(confidence - 0.8123) < 1e-9

label, confidence = prediction_to_label_score(('dog', 0.55))
assert label == 'dog'
assert abs(confidence - 0.55) < 1e-9

message = format_predictions([DummyPrediction('tabby cat', 0.8123), ('dog', 0.55)])
assert '1. tabby cat: 81.23%' in message
assert '2. dog: 55.00%' in message
print('cnn prediction format tests passed')
