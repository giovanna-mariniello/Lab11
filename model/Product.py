from dataclasses import dataclass

@dataclass
class Product:
    _Product_number: int
    _Product_line: str
    _Product_type: str
    _Product: str
    _Product_brand: str
    _Product_color: str
    _Unit_cost: float
    _Unit_price: float

    @property
    def Color(self):
        return self._Product_color
    @property
    def Product_number(self):
        return self._Product_number
    def __str__(self):
        return self._Product_number

    def __hash__(self):
        return hash(self._Product_number)
