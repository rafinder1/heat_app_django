from calculator.amount_polystyrene.amount_polystyrene import AmountPolystyreneAndPrice
from heat.calculator.APAP_data import AmountPolystyreneData


class AmountPolystyreneAndPriceCalculator:

    @classmethod
    def calculate(cls, amount_polystyrene_data: AmountPolystyreneData):
        return AmountPolystyreneAndPrice.calculate(
            wall_surface=float(amount_polystyrene_data.wall_surface),
            price_square_meter=float(amount_polystyrene_data.price_square_meter),
            amount_polystyrene_in_one_package=float(amount_polystyrene_data.amount_package))
