"""Configuration constants for the Mini Photoshop desktop UI."""

from __future__ import annotations

APP_TITLE = "Mini Photoshop Pro - Pengolahan Citra Digital"
DEFAULT_WINDOW_SIZE = "1440x900"
MIN_WINDOW_SIZE = (1180, 760)
CANVAS_BG = "#101827"
PANEL_BG = "#111827"
CARD_BG = "#1f2937"
ACCENT = "#38bdf8"
TEXT = "#e5e7eb"
MUTED_TEXT = "#9ca3af"
SUCCESS = "#22c55e"
WARNING = "#f59e0b"
ERROR = "#ef4444"
PREVIEW_MIN_SIZE = (360, 300)
HISTORY_LIMIT = 30

PRESETS = {
    "Ringan": 0.55,
    "Sedang": 1.0,
    "Kuat": 1.65,
}

FEATURE_CATEGORIES = [
    "Basic",
    "Enhancement",
    "Transform",
    "Restoration",
    "Binary & Edge",
    "Color",
    "Segmentation",
    "Compression",
    "Machine Learning",
]
