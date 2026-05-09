import json
import os

NEON_DEFAULT = "#7b4dff"

THEMES = {
    "dark": {
        "bg_main": "#0d0d0d",
        "bg_sidebar": "#0f0f11",
        "bg_card": "#131313",
        "text_main": "#e6eef7",
        "text_secondary": "#9aa7b8",
        "border_card": "#2a2a2a",
        "bg_search": "#0b0b0c",
        "border_search": "#232428",
        "bg_button": "#1b1b1b",
        "bg_button_hover": "#232325",
        "bg_input": "#1b1b1b",
    },
    "light": {
        "bg_main": "#f5f5f5",
        "bg_sidebar": "#e0e0e0",
        "bg_card": "#ffffff",
        "text_main": "#1a1a1a",
        "text_secondary": "#5c5c5c",
        "border_card": "#d3d3d3",
        "bg_search": "#ffffff",
        "border_search": "#cccccc",
        "bg_button": "#e9e9e9",
        "bg_button_hover": "#dedede",
        "bg_input": "#ffffff",
    },
}