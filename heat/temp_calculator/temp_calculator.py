import pandas as pd
from enum import Enum

from calculator.calculator import TempCalculator


class MethodName(Enum):
    finite_element_method = "finite_element_method"


def calculate(data):
    data_building_partition = data['data_building_partition']
    data_building_partition_df = pd.DataFrame(data_building_partition)

    heat_information = data['heat_information']

    method = MethodName.finite_element_method

    output = TempCalculator.calculate(data_building_partition_df, heat_information, method)

    cumulative_thickness = 0
    cumulative_thickness_list = [cumulative_thickness]

    for index, row in output.iterrows():
        cumulative_thickness += row['thickness']
        cumulative_thickness_list.append(cumulative_thickness)

    temperatures_list = [heat_information['outside_temperature']]
    temperatures_list.extend(output.temperatures.to_list())

    return {'temp': temperatures_list, 'thickness': cumulative_thickness_list}
