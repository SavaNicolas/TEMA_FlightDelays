from dataclasses import dataclass

from model.airport import Airport


@dataclass
class Arco:
    aereoportoP: Airport
    aereoportoD: Airport
    peso:int