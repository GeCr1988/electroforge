"""Calcul putere instalată (Pi) și putere de calcul/simultaneitate (Pc).

Referință: specificatii-complete.md secțiunea 4.3, I7-2011.
"""


def calc_putere_instalata(puteri_nominale_w: list[float]) -> float:
    """Pi = suma puterilor nominale ale receptorilor dintr-un tablou/circuit."""
    return sum(puteri_nominale_w)


def calc_putere_calcul(receptori: list[tuple[float, float]], ks: float) -> float:
    """Pc = (suma Pi * Ku per receptor) * Ks.

    `receptori` e o listă de tupluri (putere_nominala_w, ku).
    """
    suma_utilizata = sum(putere * ku for putere, ku in receptori)
    return suma_utilizata * ks
