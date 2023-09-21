from enum import Enum
import pandas as pd

from calculator.basic.calculator import TempCalculator
from calculator.multivariants.multivariants import MultiVariantsCalculator


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


def multi_variant_calculate(data, polystyrene_json):
    data_building_partition = data['data_building_partition']
    data_building_partition_df = pd.DataFrame(data_building_partition)

    heat_information = data['heat_information']
    expected_temperature = data['expected_temperature']

    method = MethodName.finite_element_method

    polystyrene_df = pd.DataFrame(polystyrene_json)
    polystyrene_data = pd.concat(objs=[polystyrene_df.drop(['fields'], axis=1),
                                       polystyrene_df['fields'].apply(pd.Series)], axis=1)

    all_polystyrene_with_temp = MultiVariantsCalculator.change_polystyrene(
        data_building_partition=data_building_partition_df,
        heat_information=heat_information,
        polystyrene_data=polystyrene_data, method=method)
    all_polystyrene_with_temp['temp_diff'] = all_polystyrene_with_temp['temperatures'] - expected_temperature
    positive_diff = all_polystyrene_with_temp[all_polystyrene_with_temp['temp_diff'] >= 0]
    sorted_data_by_name_layer_temp_diff = positive_diff.sort_values(by=['name_layer', 'temp_diff'])

    sorted_data_by_name_layer_temp_diff.fillna('', inplace=True)

    result = sorted_data_by_name_layer_temp_diff.groupby('name_layer').first().reset_index()

    return {"name_layer": result.name_layer.to_list(),
            "thickness": result.thickness.to_list(),
            "thermal_conductivity": result.thermal_conductivity.to_list(),
            "cost": result.cost.to_list(),
            "temperatures": result.temperatures.to_list(),
            "comments": result.comments.to_list()}
