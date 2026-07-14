"""Calcul curent nominal pe circuit, monofazat și trifazat.

Referință: specificatii-complete.md secțiunea 4.3.
"""
import math


def calc_curent_monofazat(putere_w: float, tensiune_v: float = 230, cos_phi: float = 1.0) -> float:
    """In = P / (U * cosφ)."""
    return putere_w / (tensiune_v * cos_phi)


def calc_curent_trifazat(putere_w: float, tensiune_v: float = 400, cos_phi: float = 1.0) -> float:
    """In = P / (√3 * U * cosφ)."""
    return putere_w / (math.sqrt(3) * tensiune_v * cos_phi)
