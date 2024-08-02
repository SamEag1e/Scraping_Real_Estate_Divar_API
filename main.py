"""Schedule work between modules"""

import get_divar
import tools

categories = ["apartment-sell", "house-villa-sell", "plot-old"]

for city_name in tools.city_code:
    for category in categories:
        get_divar.tokens(city_name=city_name, category=category)
        get_divar.data()
