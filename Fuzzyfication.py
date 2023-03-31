import numpy as np
from FuzzyficateFunctions import obtain_triangular_fuzzy_value
from FuzzyficateFunctions import draw_triangular_fuzzy_value
from FuzzyficateFunctions import obtain_trapezoid_fuzzy_value
from FuzzyficateFunctions import draw_trapezoid_fuzzy_value
from FuzzyficateFunctions import obtain_gaussian_fuzzy_value
from FuzzyficateFunctions import draw_gaussian_fuzzy_value
from FuzzyficateFunctions import obtain_sigmoid_fuzzy_value
from FuzzyficateFunctions import draw_sigmoid_fuzzy_value
from FuzzyficateFunctions import plot_sigmoid_fuzzy_value
from FuzzyficateFunctions import plot_cup_gaussian_fuzzy_value


class Age:

    def __init__(self):
        pass

    def calc_fuzzy(self, age):
        # if age is string
        if isinstance(age, str):
            if age == 'mlady':
                age = (0 + 25)/2
            elif age == 'stredne stary':
                age = (25 + 50)/2
            elif age == 'stary':
                age = (50 + 75)/2
            elif age == 'velmi stary':
                age = (75 + 100)/2
        plot_sigmoid_fuzzy_value(0, 100, age, 50, 10, "Vek")
        return obtain_sigmoid_fuzzy_value(age, 50, 10)

# typical singletone function


class Sex:

    def __init__(self):
        pass

    def calc_fuzzy(self, sex):

        if sex == 'M':
            return 0.3

        else:
            return 0.1


class Height:

    def __init__(self):
        pass

    def calc_fuzzy(self, height):
        if isinstance(height, str):
            if height == 'maly':
                height = (50 + 155)/2
            elif height == 'stredny':
                height = (155 + 177)/2
            elif height == 'velky':
                height = (177 + 200)/2
        plot_cup_gaussian_fuzzy_value(50, 200, height, 165, 10, "Vyska")
        return obtain_gaussian_fuzzy_value(height, 165, 10)


class Weight:

    def __init__(self):
        pass

    def calc_fuzzy(self, weight):
        if isinstance(weight, str):
            if weight == 'lahky':
                weight = (20 + 50)/2
            elif weight == 'stredne tazka':
                weight = (50 + 80)/2
            elif weight == 'tazky':
                weight = (80 + 120)/2
        plot_cup_gaussian_fuzzy_value(20, 120, weight, 60, 10, "Vaha")
        return obtain_gaussian_fuzzy_value(weight, 60, 10)


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


def get_final_result(data):
    age_class = Age()
    sex_class = Sex()
    height_class = Height()
    weight_class = Weight()
    pulse_class = Pulse()
    oxygenation_class = Oxygenation()
    st_bp_class = ST_BloodPressure()
    dt_bp_class = DT_BloodPressure()

    # check if data has string value instad of number

    if data['Vek'] == 'mlady' or data['Vek'] == 'stredne stary' or data['Vek'] == 'stary' or data['Vek'] == 'velmi stary':
        age = age_class.calc_fuzzy(data['Vek'])
    else:
        age = age_class.calc_fuzzy(int(data['Vek']))

    sex = sex_class.calc_fuzzy(str(data['Pohlavie']))
    if data['Vyska'] == 'maly' or data['Vyska'] == 'stredny' or data['Vyska'] == 'velky':
        height = height_class.calc_fuzzy(data['Vyska'])
    else:
        height = height_class.calc_fuzzy(float(data['Vyska']))

    weight = weight_class.calc_fuzzy(float(data['Vaha']))
    pulse = pulse_class.calc_fuzzy(int(data['Pulz']))
    oxygenation = oxygenation_class.calc_fuzzy(float(data['Okyslicenie krvi']))
    st_bp = st_bp_class.calc_fuzzy(int(data['Systolický krvný tlak']))
    dt_bp = dt_bp_class.calc_fuzzy(int(data['Diastolický krvný tlak']))

    return (age, sex, height, weight, pulse, oxygenation, st_bp, dt_bp)
