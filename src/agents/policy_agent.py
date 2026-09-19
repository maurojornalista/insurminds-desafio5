"""Agente para selecionar segurados em uma base CSV fictícia."""
from __future__ import annotations

from pathlib import Path
from typing import Any

import pandas as pd


class PolicyAgent:
    """Cruza cidade do evento e tipo de apólice com a base fictícia."""

    def __init__(self, csv_path: str | Path):
        self.csv_path = Path(csv_path)

    def find_affected(self, city: str, risk: dict[str, Any]) -> list[dict[str, Any]]:
        if not risk.get("has_risk"):
            return []
        try:
            policyholders = pd.read_csv(self.csv_path)
        except (OSError, pd.errors.ParserError):
            return []
        if not {"cidade", "tipo_apolice"}.issubset(policyholders.columns):
            return []
        affected_types = risk.get("affected_policy_types", [])
        matches = policyholders[
            (policyholders["cidade"].str.casefold() == city.casefold())
            & (policyholders["tipo_apolice"].isin(affected_types))
        ]
        return matches.to_dict(orient="records")
