"""
NEEV - NCO Parser
Goal: Convert NCO-2015 (PDF/Excel) into structured JSON with full 8-digit hierarchy.

As a beginner, think of this file as:
- Input: NCO-2015 files (we'll begin with a placeholder CSV for now)
- Output: clean JSON you can easily load into Python for embeddings
"""

from typing import List, Dict
import json
import re

class NCOParser:
    def __init__(self):
        # Pattern hint: We'll validate 8-digit codes and their hierarchy
        self.code_pattern = re.compile(r'^\d{8}$')

    def normalize_text(self, text: str) -> str:
        """Lowercase and basic cleanup; later we’ll expand this."""
        if not text:
            return ""
        return " ".join(text.lower().strip().split())

    def validate_code(self, code: str) -> bool:
        """Ensure code is exactly 8 digits."""
        return bool(self.code_pattern.match(code))

    def parse_placeholder(self) -> List[Dict]:
        """
        Placeholder parser that returns a tiny in-memory dataset.
        Later, we will replace with a real Excel/PDF parser.
        """
        # Minimal sample with hierarchy (major→sub-major→minor→unit)
        sample = [
            {
                "code": "75330100",  # 7533.01.00 format conceptually, flattened to 8 digits
                "title": "Sewing Machine Operator",
                "description": "Operates industrial sewing machines for garment production.",
                "major_group": "75",
                "sub_major_group": "7533",
                "minor_group": "753301",
                "unit_group": "75330100"
            },
            {
                "code": "26520100",
                "title": "Classical Dancer",
                "description": "Performs traditional Indian classical dance forms.",
                "major_group": "26",
                "sub_major_group": "2652",
                "minor_group": "265201",
                "unit_group": "26520100"
            }
        ]
        # Normalize
        for item in sample:
            item["title_norm"] = self.normalize_text(item["title"])
            item["desc_norm"] = self.normalize_text(item["description"])
        return sample

    def to_json(self, data: List[Dict], out_path: str = "neev-data/nco_structured.json") -> None:
        with open(out_path, "w", encoding="utf-8") as f:
            json.dump(data, f, ensure_ascii=False, indent=2)
