import numpy as np
from FuzzyficateFunctions import obtain_triangular_fuzzy_value
from FuzzyficateFunctions import draw_triangular_fuzzy_value
from FuzzyficateFunctions import obtain_trapezoid_fuzzy_value
from FuzzyficateFunctions import draw_trapezoid_fuzzy_value
from FuzzyficateFunctions import obtain_gaussian_fuzzy_value
from FuzzyficateFunctions import draw_gaussian_fuzzy_value
from FuzzyficateFunctions import obtain_sigmoid_fuzzy_value
from FuzzyficateFunctions import draw_sigmoid_fuzzy_value


class Age:

    def __init__(self):
        pass

    def calc_fuzzy(self, age):
        return {'young': obtain_trapezoid_fuzzy_value(age, [0, 0, 29, 38]),
                'middle-age': obtain_triangular_fuzzy_value(age, [33, 38, 45]),
                'old': obtain_triangular_fuzzy_value(age, [40, 48, 52])}

# typical singletone function


class Sex:

    def __init__(self):
        pass

    def calc_fuzzy(self, sex):

        if sex == 'M':
            res = {'Muž': 1,
                   'Žena': 0}
            return res

        else:
            res = {'Muž': 0,
                   'Žena': 1}
            return res


class Height:

    def __init__(self):
        pass

    def calc_fuzzy(self, height):
        return {'short': obtain_triangular_fuzzy_value(height, [0, 0, 150]),
                'medium': obtain_triangular_fuzzy_value(height, [140, 170, 200]),
                'tall': obtain_triangular_fuzzy_value(height, [190, 220, 220])
                }


class Weight:

    def __init__(self):
        pass

    def calc_fuzzy(self, weight):
        return {'thin': obtain_triangular_fuzzy_value(weight, [0, 0, 50]),
                'average': obtain_triangular_fuzzy_value(weight, [40, 70, 100]),
                'overweight': obtain_triangular_fuzzy_value(weight, [90, 120, 120])
                }


class Pulse:
    def __init__(self):
        pass

    def calc_fuzzy(self, pulse):
        return {"low": obtain_trapezoid_fuzzy_value(pulse, [0, 0, 50, 60]),
                "medium": obtain_trapezoid_fuzzy_value(pulse, [50, 70, 90, 110]),
                "high": obtain_trapezoid_fuzzy_value(pulse, [100, 140, 160, 160])
                }


class Oxygenation:

    def __init__(self):
        pass

    def calc_fuzzy(self, oxygenation):
        return {"low": obtain_trapezoid_fuzzy_value(oxygenation, [0, 0, 80, 90]),
                "medium": obtain_trapezoid_fuzzy_value(oxygenation, [85, 92, 97, 97]),
                "high": obtain_trapezoid_fuzzy_value(oxygenation, [95, 100, 100, 100])
                }


class ST_BloodPressure:

    def __init__(self):
        self.fuzzy_ranges = {
            "low": [0, 0, 89, 99],
            "normal": [100, 100, 119, 129],
            "elevated": [130, 130, 139, 139],
            "stage_1": [140, 140, 159, 159],
            "hypertensive_crisis": [160, 160, 250, 250]
        }

    def calc_fuzzy(self, bp):
        fuzzy_values = {}
        for term, ranges in self.fuzzy_ranges.items():
            fuzzy_values[term] = obtain_trapezoid_fuzzy_value(bp, ranges)
        return fuzzy_values
        # return draw_trapezoid_fuzzy_value(np.arange(0, 250, 0.1), bp, [0, 100, 141, 200], [0, 111, 152, 194], [0, 152, 210, 250])


class DT_BloodPressure:

    def __init__(self):
        self.fuzzy_ranges = {
            "low": [0, 0, 59, 69],
            "normal": [70, 70, 79, 89],
            "elevated": [90, 90, 99, 99],
            "stage_1": [100, 100, 109, 109],
            "hypertensive_crisis": [110, 110, 200, 200]
        }

    def calc_fuzzy(self, bp):
        fuzzy_values = {}
        for term, ranges in self.fuzzy_ranges.items():
            fuzzy_values[term] = obtain_trapezoid_fuzzy_value(bp, ranges)
        return fuzzy_values


def fuzzify_inputs(inputs):
    fuzzy_inputs = []
    symptom_sets = {
        'sick1': obtain_triangular_fuzzy_value(inputs['sick1'], [0, 0, 0.5]),
        'sick2': obtain_triangular_fuzzy_value(inputs['sick2'], [0.5, 1, 1]),
        'sick3': obtain_triangular_fuzzy_value(inputs['sick3'], [0.25, 0.75, 1]),
        'sick4': obtain_triangular_fuzzy_value(inputs['sick4'], [0, 0, 0]),
        'healthy': obtain_triangular_fuzzy_value(inputs['healthy'], [0.25, 0.75, 1])
    }
    for key in symptom_sets.keys():
        fuzzy_inputs.append(inputs[key])

    return fuzzy_inputs


def infer_degree_of_disease(inputs):
    # Initialize arrays for output fuzzy sets
    healthy = [0, 0, 0.5]
    mild = [0.5, 1, 1]
    moderate = [0.25, 0.75, 1]
    serious = [0, 0, 0]
    severe = [0.25, 0.75, 1]

    output_sets = [healthy, mild, moderate, serious, severe]
    degrees_of_membership = []

    # Compute degrees of membership for each output fuzzy set
    for output_set in output_sets:
        degrees = []
        for i in range(len(output_set)):
            degrees.append(min(output_set[i], max(inputs)))
        degrees_of_membership.append(max(degrees))

    # Construct dictionary of degrees of membership for output fuzzy sets
    degree_of_disease = {'Healthy': degrees_of_membership[0],
                         'Mild': degrees_of_membership[1],
                         'Moderate': degrees_of_membership[2],
                         'Serious': degrees_of_membership[3],
                         'Severe': degrees_of_membership[4]}
    return degree_of_disease


def get_final_result(data):
    age_class = Age()
    sex_class = Sex()
    height_class = Height()
    weight_class = Weight()
    pulse_class = Pulse()
    oxygenation_class = Oxygenation()
    st_bp_class = ST_BloodPressure()
    dt_bp_class = DT_BloodPressure()

    age = age_class.calc_fuzzy(int(data['Vek']))
    sex = sex_class.calc_fuzzy(str(data['Pohlavie']))
    height = height_class.calc_fuzzy(float(data['Vyska']))
    weight = weight_class.calc_fuzzy(float(data['Vaha']))
    pulse = pulse_class.calc_fuzzy(int(data['Pulz']))
    oxygenation = oxygenation_class.calc_fuzzy(float(data['Okyslicenie krvi']))
    st_bp = st_bp_class.calc_fuzzy(int(data['Systolický krvný tlak']))
    dt_bp = dt_bp_class.calc_fuzzy(int(data['Diastolický krvný tlak']))

    return (age, sex, height, weight, pulse, oxygenation, st_bp, dt_bp)
