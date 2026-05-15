"""Undo/redo history manager for image arrays."""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Optional

import numpy as np


@dataclass
class ImageHistory:
    """Small bounded history stack for committed image states."""

    limit: int = 30
    _undo: list[np.ndarray] = field(default_factory=list)
    _redo: list[np.ndarray] = field(default_factory=list)

    def clear(self) -> None:
        self._undo.clear()
        self._redo.clear()

    def push(self, image: np.ndarray) -> None:
        self._undo.append(image.copy())
        if len(self._undo) > self.limit:
            self._undo.pop(0)
        self._redo.clear()

    def undo(self, current: np.ndarray) -> Optional[np.ndarray]:
        if not self._undo:
            return None
        self._redo.append(current.copy())
        return self._undo.pop()

    def redo(self, current: np.ndarray) -> Optional[np.ndarray]:
        if not self._redo:
            return None
        self._undo.append(current.copy())
        return self._redo.pop()

    @property
    def can_undo(self) -> bool:
        return bool(self._undo)

    @property
    def can_redo(self) -> bool:
        return bool(self._redo)
