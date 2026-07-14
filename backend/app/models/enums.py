import enum


class RolUtilizator(str, enum.Enum):
    proiectant = "proiectant"
    verificator = "verificator"
    administrator = "administrator"


class TipCladire(str, enum.Enum):
    rezidential = "rezidential"
    industrial = "industrial"


class TipReceptor(str, enum.Enum):
    iluminat = "iluminat"
    priza = "priza"
    motor = "motor"
    forta = "forta"


class TipCircuit(str, enum.Enum):
    monofazat = "monofazat"
    trifazat = "trifazat"


class StatusConformitate(str, enum.Enum):
    conform = "conform"
    neconform = "neconform"
