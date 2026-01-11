# jbi100_app/utils/country_meta.py
from __future__ import annotations

from pathlib import Path
from functools import lru_cache
import re
import difflib
import unicodedata

import pandas as pd


# Alias map for common mismatches between your dataset country names and the ISO table names.
# NOTE: We normalize these keys/values at lookup time, so you can write them naturally here.
ALIASES = {
    "BAHAMAS, THE": "BAHAMAS",
    "GAMBIA, THE": "GAMBIA",
    "BOLIVIA": "BOLIVIA, PLURINATIONAL STATE OF",
    "VENEZUELA": "VENEZUELA, BOLIVARIAN REPUBLIC OF",
    "IRAN": "IRAN, ISLAMIC REPUBLIC OF",
    "BRUNEI": "BRUNEI DARUSSALAM",
    "BURMA": "MYANMAR",
    "KOREA, NORTH": "KOREA, DEMOCRATIC PEOPLE'S REPUBLIC OF",
    "KOREA, SOUTH": "KOREA, REPUBLIC OF",
    "LAOS": "LAO PEOPLE'S DEMOCRATIC REPUBLIC",
    "MACAU": "MACAO",
    "MOLDOVA": "MOLDOVA, REPUBLIC OF",
    "RUSSIA": "RUSSIAN FEDERATION",
    "SYRIA": "SYRIAN ARAB REPUBLIC",
    "TAIWAN": "TAIWAN, PROVINCE OF CHINA",
    "TANZANIA": "TANZANIA, UNITED REPUBLIC OF",
    "VIETNAM": "VIET NAM",

    # USA/UK common variants
    "UNITED STATES": "UNITED STATES OF AMERICA",
    "U.S.": "UNITED STATES OF AMERICA",
    "US": "UNITED STATES OF AMERICA",
    "United Kingdom": "United Kingdom of Great Britain and Northern Ireland",
    "UK": "United Kingdom of Great Britain and Northern Ireland",
    "U.K.": "United Kingdom of Great Britain and Northern Ireland",

    # Your all.csv uses "Netherlands, Kingdom of the"
    "NETHERLANDS": "Netherlands, Kingdom of the",

    # Your all.csv uses "Türkiye"
    "TURKEY (TURKIYE)": "Türkiye",
    "TURKEY": "Türkiye",
    "TURKIYE": "Türkiye",

    # Others seen in your unmapped list
    "CONGO, REPUBLIC OF THE": "CONGO",
    "HOLY SEE (VATICAN CITY)": "HOLY SEE",

    # Some additional common ones (harmless if unused)
    "COTE DIVOIRE": "Côte d'Ivoire",
    "IVORY COAST": "Côte d'Ivoire",
    "CONGO (BRAZZAVILLE)": "CONGO",
    "CONGO (KINSHASA)": "CONGO, DEMOCRATIC REPUBLIC OF THE",
    "DR CONGO": "CONGO, DEMOCRATIC REPUBLIC OF THE",
    "CABO VERDE": "CAPE VERDE",
    "SWAZILAND": "ESWATINI",
    "PALESTINE": "PALESTINE, STATE OF",
    "BOSNIA": "BOSNIA AND HERZEGOVINA",
    "CZECH REPUBLIC": "CZECHIA",
    "TAIWAN": "Taiwan, Province of China"
}


def _strip_accents(s: str) -> str:
    """Convert 'Türkiye' -> 'Turkiye' etc."""
    s = unicodedata.normalize("NFKD", s)
    return "".join(ch for ch in s if not unicodedata.combining(ch))


def _norm(s: str) -> str:
    """
    Normalize a country name into a robust match key:
      - uppercase
      - remove accents
      - remove punctuation / parentheses
      - normalize whitespace
    """
    s = str(s).strip()
    s = _strip_accents(s).upper()

    s = s.replace("&", " AND ")
    s = re.sub(r"[’']", "", s)                 # remove apostrophes
    s = re.sub(r"[\(\)\.,\-]", " ", s)         # punctuation -> space
    s = re.sub(r"\s+", " ", s).strip()         # collapse whitespace
    return s


@lru_cache(maxsize=1)
def _iso_table() -> pd.DataFrame:
    """
    Load ISO/UN metadata from jbi100_app/meta/all.csv.
    Expected columns: name, alpha-3, region, (optionally sub-region, etc.)
    """
    path = Path(__file__).parent.parent / "meta" / "all.csv"
    if not path.exists():
        raise FileNotFoundError(
            "Missing jbi100_app/meta/all.csv. Put the ISO+region file there "
            "(separate from data_sets) so the map and region ranking work."
        )

    iso = pd.read_csv(path)
    if "name" not in iso.columns or "alpha-3" not in iso.columns or "region" not in iso.columns:
        raise ValueError("meta/all.csv must contain at least columns: name, alpha-3, region")

    # IMPORTANT: normalize ISO names using the same normalization as your dataset
    iso["iso_key"] = iso["name"].apply(_norm)
    return iso


@lru_cache(maxsize=1)
def _iso_maps():
    iso = _iso_table()
    iso_keys = set(iso["iso_key"])
    region_map = dict(zip(iso["iso_key"], iso["region"]))
    a3_map = dict(zip(iso["iso_key"], iso["alpha-3"]))
    return iso_keys, region_map, a3_map


@lru_cache(maxsize=1)
def _norm_aliases():
    # Normalize aliases once so you can write them in a readable way above.
    return {_norm(k): _norm(v) for k, v in ALIASES.items()}


def resolve_iso_key(country_name: str) -> str | None:
    """
    Convert your dataset's Country string into the normalized iso_key used by meta/all.csv.
    Returns None if no match found.
    """
    iso_keys, _, _ = _iso_maps()
    c = _norm(country_name)

    if c in iso_keys:
        return c

    aliases = _norm_aliases()
    if c in aliases:
        cand = aliases[c]
        if cand in iso_keys:
            return cand

    # Fuzzy fallback (kept fairly strict)
    match = difflib.get_close_matches(c, list(iso_keys), n=1, cutoff=0.85)
    return match[0] if match else None


def attach_country_meta(df: pd.DataFrame) -> pd.DataFrame:
    """
    Return a copy of df with:
      - iso3 : ISO alpha-3 code (for plotting)
      - region : region label (for coloring and filtering)
      - country_display : nicer UI label
    """
    _, region_map, a3_map = _iso_maps()

    out = df.copy()
    out["iso_key"] = out["Country"].apply(resolve_iso_key)
    out["iso3"] = out["iso_key"].map(a3_map)
    out["region"] = out["iso_key"].map(region_map)
    out["country_display"] = out["Country"].astype(str).str.title()
    
    # Manual region overrides for better continent sense
    out.loc[out["iso3"] == "RUS", "region"] = "Asia"
    return out
