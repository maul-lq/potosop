"""Reusable Tkinter/ttk widgets used by the main app."""

from __future__ import annotations

from typing import Callable

import tkinter as tk
from tkinter import ttk


class ScrollableFrame(ttk.Frame):
    """A vertical scrollable frame for many controls."""

    def __init__(self, parent: tk.Widget, *args, **kwargs) -> None:
        super().__init__(parent, *args, **kwargs)
        self.canvas = tk.Canvas(self, highlightthickness=0, borderwidth=0)
        self.scrollbar = ttk.Scrollbar(self, orient="vertical", command=self.canvas.yview)
        self.body = ttk.Frame(self.canvas)
        self._window_id = self.canvas.create_window((0, 0), window=self.body, anchor="nw")
        self.canvas.configure(yscrollcommand=self.scrollbar.set)
        self.canvas.pack(side="left", fill="both", expand=True)
        self.scrollbar.pack(side="right", fill="y")
        self.body.bind("<Configure>", self._on_body_configure)
        self.canvas.bind("<Configure>", self._on_canvas_configure)
        self.canvas.bind_all("<MouseWheel>", self._on_mousewheel)

    def _on_body_configure(self, _event: tk.Event) -> None:
        self.canvas.configure(scrollregion=self.canvas.bbox("all"))

    def _on_canvas_configure(self, event: tk.Event) -> None:
        self.canvas.itemconfigure(self._window_id, width=event.width)

    def _on_mousewheel(self, event: tk.Event) -> None:
        try:
            if self.winfo_ismapped():
                self.canvas.yview_scroll(int(-1 * (event.delta / 120)), "units")
        except tk.TclError:
            pass


def labeled_value(parent: tk.Widget, label: str, value_var: tk.Variable, row: int) -> tuple[ttk.Label, ttk.Label]:
    title = ttk.Label(parent, text=label)
    value = ttk.Label(parent, textvariable=value_var, width=8, anchor="e")
    title.grid(row=row, column=0, sticky="w", pady=4)
    value.grid(row=row, column=2, sticky="e", pady=4)
    return title, value


def make_slider(
    parent: tk.Widget,
    label: str,
    variable: tk.Variable,
    from_: float,
    to: float,
    row: int,
    command: Callable[[], None],
    resolution: float = 1,
) -> ttk.Scale:
    value_var = tk.StringVar(value=str(variable.get()))

    def on_change(_value: str) -> None:
        raw = variable.get()
        if isinstance(raw, float):
            value_var.set(f"{raw:.2f}")
        else:
            value_var.set(str(raw))
        command()

    ttk.Label(parent, text=label).grid(row=row, column=0, sticky="w", pady=5)
    scale = ttk.Scale(parent, variable=variable, from_=from_, to=to, command=on_change)
    scale.grid(row=row, column=1, sticky="ew", padx=8, pady=5)
    ttk.Label(parent, textvariable=value_var, width=8, anchor="e").grid(row=row, column=2, sticky="e", pady=5)
    parent.grid_columnconfigure(1, weight=1)
    return scale


def make_action_button(parent: tk.Widget, text: str, command: Callable[[], None], row: int, column: int = 0, colspan: int = 1) -> ttk.Button:
    button = ttk.Button(parent, text=text, command=command)
    button.grid(row=row, column=column, columnspan=colspan, sticky="ew", padx=4, pady=4)
    return button
