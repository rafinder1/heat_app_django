import logging
import sys

import pandas as pd
from calculator.basic.calculator import TempCalculator
from calculator.multivariants.multivariants import MultiVariantsCalculator
from calculator.shared_data.outside_inside_thermal_data import OutsideInsideThermalData

GLOBAL_LOGGING_LEVEL = logging.INFO
logging.basicConfig(stream=sys.stdout, level=GLOBAL_LOGGING_LEVEL)


def calculate(data):
    data_building_partition = data['data_building_partition']
    data_building_partition_df = pd.DataFrame(data_building_partition)

    heat_information = data['heat_information']

    outside_inside_thermal_data = OutsideInsideThermalData(
        INSIDE_TEMPERATURE=heat_information['inside_temperature'],
        OUTSIDE_TEMPERATURE=heat_information['outside_temperature'],
        INSIDE_HEATER_POWER=heat_information['inside_heater_power'],
        OUTSIDE_HEATER_POWER=heat_information['outside_heater_power']
    )

    output = TempCalculator.calculate(data_building_partition_df, outside_inside_thermal_data,
                                      "finite_element_method")
    cumulative_thickness = 0
    cumulative_thickness_list = [cumulative_thickness]

    for index, row in output.iterrows():
        cumulative_thickness += row['thickness']
        cumulative_thickness_list.append(cumulative_thickness)

    temperatures_list = [heat_information['outside_temperature']]
    temperatures_list.extend(output.temperatures.to_list())

    return {'temp': temperatures_list, 'thickness': cumulative_thickness_list}


def multi_variant_calculate(data, thermal_isolation_json):
    data_building_partition = data['data_building_partition']
    data_building_partition_df = pd.DataFrame(data_building_partition)

    if len(data_building_partition_df) == 1:
        if 'ocieplenie' in data_building_partition_df['type_layer'].values:
            logging.warning(
                "Only Styrofoam was selected, multi-variant analysis is not possible. Empty data "
                "was passed")
            return {"name_layer": [],
                    "thickness": [],
                    "thermal_conductivity": [],
                    "cost": [],
                    "package_square_meters": [],
                    "temperatures": [],
                    "comments": []}

    heat_information = data['heat_information']
    expected_temperature = data['expected_temperature']
    if expected_temperature is None or expected_temperature == '':
        expected_temperature = 20
        logging.warning(
            f'Expected Temperature is not defined. Take the default value equal '
            f'{expected_temperature}°C')

    method = MethodName.finite_element_method

    thermal_isolation_data = pd.DataFrame(thermal_isolation_json)
    all_thermal_isolation_with_temp = MultiVariantsCalculator.change_polystyrene(
        data_building_partition=data_building_partition_df,
        outside_inside_thermal_data=heat_information,
        polystyrene_data=thermal_isolation_data, method=method)
    all_thermal_isolation_with_temp['temp_diff'] = all_thermal_isolation_with_temp[
                                                       'temperatures'] - expected_temperature
    positive_diff = all_thermal_isolation_with_temp[
        all_thermal_isolation_with_temp['temp_diff'] >= 0]
    sorted_data_by_name_layer_temp_diff = positive_diff.sort_values(by=['name_layer', 'temp_diff'])

    sorted_data_by_name_layer_temp_diff.fillna('', inplace=True)

    result = sorted_data_by_name_layer_temp_diff.groupby('name_layer').first().reset_index()

    result.sort_values(by=['cost'], inplace=True)
    print(result)
    return {"name_layer": result.name_layer.to_list(),
            "thickness": result.thickness.to_list(),
            "thermal_conductivity": result.thermal_conductivity.to_list(),
            "cost": result.cost.to_list(),
            "package_square_meters": result.package_square_meters.to_list(),
            "temperatures": result.temperatures.to_list(),
            # "comments": result.comments.to_list()
            }
