from heat.calculator.APAP_data import AmountPolystyreneData
from calculator.amount_polystyrene.amount_polystyrene import AmountPolystyreneAndPrice


class AmountPolystyreneAndPriceCalculator:

    @classmethod
    def calculate(cls, amount_polystyrene_data: AmountPolystyreneData):
        data = AmountPolystyreneAndPrice.calculate(wall_surface=amount_polystyrene_data.wall_surface,
                                                   price_square_meter=amount_polystyrene_data.price_square_meter,
                                                   amount_package=amount_polystyrene_data.amount_package)
        return data
