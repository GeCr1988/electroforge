import json
from functools import lru_cache
from pathlib import Path

STANDARDS_DIR = Path(__file__).resolve().parent.parent / "standards"


@lru_cache
def load_standard(name: str) -> dict:
    path = STANDARDS_DIR / f"{name}.json"
    with open(path, encoding="utf-8") as f:
        return json.load(f)


def curenti_admisibili() -> dict:
    return load_standard("curenti_admisibili")


def ku_ks() -> dict:
    return load_standard("ku_ks")


def cadere_tensiune() -> dict:
    return load_standard("cadere_tensiune")


def sectiuni_standard() -> list[float]:
    return load_standard("sectiuni_standard")["sectiuni_mm2"]
