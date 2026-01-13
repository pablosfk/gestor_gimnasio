from dataclasses import dataclass

@dataclass
class Dessert:
    name: str
    calories: int
    fat: float
    carbs: int
    protein: float
    sodium: int
    calcium: int
    iron: int

# Lista de instancias de Dessert
desserts = [
    Dessert("Frozen yogurt", 159, 6.0, 24, 4.0, 87, 14, 1),
    Dessert("Ice cream sandwich", 237, 9.0, 37, 4.3, 129, 8, 1),
    Dessert("Eclair", 262, 16.0, 24, 6.0, 337, 6, 7),
    Dessert("Cupcake", 305, 3.7, 67, 4.3, 413, 3, 8),
    Dessert("Gingerbread", 356, 16.0, 49, 3.9, 327, 7, 16),
    Dessert("Jelly bean", 375, 0.0, 94, 0.0, 50, 0, 0),
    Dessert("Lollipop", 392, 0.2, 98, 0.0, 38, 0, 2),
    Dessert("Honeycomb", 408, 3.2, 87, 6.5, 562, 0, 45),
    Dessert("Donut", 452, 25.0, 51, 4.9, 326, 2, 22),
    Dessert("KitKat", 518, 26.0, 65, 7.0, 54, 12, 6),
]