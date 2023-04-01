import random
from FuzzyficateFunctions import obtain_trapezoid_fuzzy_value
from FuzzyficateFunctions import obtain_gaussian_fuzzy_value
from FuzzyficateFunctions import obtain_sigmoid_fuzzy_value
from FuzzyficateFunctions import plot_sigmoid_fuzzy_value
from FuzzyficateFunctions import plot_cup_gaussian_fuzzy_value
from FuzzyficateFunctions import plot_trapezoid_fuzzy_value


class Age:

    def __init__(self):
        self.fuzzy_ranges = {
            "young": [0, 25],
            "middle_age": [25, 50],
            "old": [50, 75],
            "very_old": [75, 100]
        }

    def calc_fuzzy(self, age):
        # if age is string
        if isinstance(age, str):
            if age == 'young':
                age = (0 + 25)/2
            elif age == 'middle age':
                age = (25 + 50)/2
            elif age == 'old':
                age = (50 + 75)/2
            elif age == 'very old':
                age = (75 + 100)/2
        plot_sigmoid_fuzzy_value(0, 100, age, 50, 10, "Vek")
        return obtain_sigmoid_fuzzy_value(age, 50, 10)

# typical singletone function


class Sex:

    def __init__(self):
        self.fuzzy_ranges = {
            "M": 0.3,
            "F": 0.1
        }

    def calc_fuzzy(self, sex):

        if sex == 'M':
            return 0.3
        else:
            return 0.1


class Height:

    def __init__(self):
        self.fuzzy_ranges = {
            "short": [60, 155],
            "medium": [155, 175],
            "tall": [175, 210]
        }

    def calc_fuzzy(self, height):
        if isinstance(height, str):
            if height == 'short':
                height = (60 + 155)/2
            elif height == 'medium':
                height = (155 + 175)/2
            elif height == 'tall':
                height = (175 + 210)/2
        plot_cup_gaussian_fuzzy_value(60, 210, height, 160, 25, "Vyska")
        return 1 - obtain_gaussian_fuzzy_value(height, 160, 25)


class Weight:

    def __init__(self):
        self.fuzzy_ranges = {
            "light": [20, 20, 50, 50],
            "medium": [50, 50, 80, 80],
            "heavy": [80, 80, 120, 120]
        }

    def calc_fuzzy(self, weight):
        if isinstance(weight, str):
            if weight == 'light':
                weight = (20 + 50)/2
            elif weight == 'medium':
                weight = (50 + 80)/2
            elif weight == 'heavy':
                weight = (80 + 120)/2
        plot_cup_gaussian_fuzzy_value(20, 120, weight, 60, 10, "Vaha")
        return 1 - obtain_gaussian_fuzzy_value(weight, 60, 10)


class ST_BloodPressure:

    def __init__(self):
        self.fuzzy_ranges = {
            "low": [0, 0, 89, 99],
            "medium": [100, 100, 119, 129],
            "high": [130, 130, 149, 149],
            "very_heigh": [150, 150, 170, 170]
        }

    def calc_fuzzy(self, bp):
        if isinstance(bp, str):
            if bp == 'low':
                bp = (0 + 89)/2
            elif bp == 'medium':
                bp = (100 + 119)/2
            elif bp == 'high':
                bp = (130 + 149)/2
            elif bp == 'very heigh':
                bp = (150 + 170)/2
        plot_sigmoid_fuzzy_value(
            0, 180, bp, 125, 10, "Systolic Blood Pressure")
        return obtain_sigmoid_fuzzy_value(bp, 125, 10)


class DT_BloodPressure:

    def __init__(self):
        self.fuzzy_ranges = {
            "low": [0, 0, 59, 69],
            "medium": [70, 70, 79, 89],
            "high": [90, 90, 99, 99],
            "very_high": [100, 100, 109, 109],
        }

    def calc_fuzzy(self, bp):
        if isinstance(bp, str):
            if bp == 'low':
                bp = (0 + 59)/2
            elif bp == 'medium':
                bp = (70 + 79)/2
            elif bp == 'high':
                bp = (90 + 99)/2
            elif bp == 'very high':
                bp = (100 + 109)/2
        plot_sigmoid_fuzzy_value(
            0, 120, bp, 80, 10, "Diastolic Blood Pressure")
        return obtain_sigmoid_fuzzy_value(bp, 80, 10)


class Cholesterol:

    def __init__(self):
        self.fuzzy_ranges = {
            "low": [0, 0, 150, 200],
            "medium_high": [150, 150, 200, 250],
            "very_high": [200, 200, 500, 600],
            "extremely_high": [500, 500, 600, 600]
        }

    def calc_fuzzy(self, cholesterol):
        if isinstance(cholesterol, str):
            if cholesterol == 'low':
                cholesterol = (0 + 150)/2
            elif cholesterol == 'medium high':
                cholesterol = (150 + 200)/2
            elif cholesterol == 'very high':
                cholesterol = (200 + 500)/2
            elif cholesterol == 'extremely high':
                cholesterol = (500 + 600)/2
        plot_sigmoid_fuzzy_value(0, 600, cholesterol, 170, 50, "Cholesterol")
        return obtain_sigmoid_fuzzy_value(cholesterol, 170, 50)


class Sugar:

    def __init__(self):
        self.fuzzy_ranges = {
            "low": [0, 0, 100, 125],
            "medium": [100, 100, 125, 200],
            "high": [125, 125, 200, 200]
        }

    def calc_fuzzy(self, sugar):
        if isinstance(sugar, str):
            if sugar == 'low':
                sugar = (0 + 100)/2
            elif sugar == 'medium':
                sugar = (100 + 125)/2
            elif sugar == 'high':
                sugar = (125 + 200)/2
        plot_trapezoid_fuzzy_value(
            0, 200, sugar, 0, 160, 200, 201, "Hladina cukru")
        return obtain_trapezoid_fuzzy_value(sugar, [0, 160, 200, 200])


class HeartRate:

    def __init__(self):
        self.fuzzy_ranges = {
            "small": [0, 0, 110, 140],
            "medium": [110, 110, 140, 200],
            "big": [140, 140, 200, 200]
        }

    def calc_fuzzy(self, hr):
        if isinstance(hr, str):
            if hr == 'small':
                hr = (0 + 100)/2
            elif hr == 'medium':
                hr = (110 + 140)/2
            elif hr == 'big':
                hr = (140 + 200)/2
        plot_trapezoid_fuzzy_value(
            0, 200, hr, 0, 110, 200, 201, "Tepova frekvencia")
        return obtain_trapezoid_fuzzy_value(hr, [0, 110, 200, 200])


class EKG:

    def __init__(self):
        self.fuzzy_ranges = {
            "normal": [-0.5, -0.5, 0.2, 0.2],
            "abnormal": [0.2, 0.2, 1, 1],
            "hypertrophy": [1, 1, 2, 2]
        }

    def calc_fuzzy(self, ekg):
        if isinstance(ekg, str):
            if ekg == 'normal':
                ekg = random.uniform(-0.5, 0.2)
            elif ekg == 'abnormal':
                ekg = random.uniform(0.2, 1)
            elif ekg == 'hypertrophy':
                ekg = random.uniform(1, 2)
        plot_trapezoid_fuzzy_value(
            -0.5, 2, ekg, -0.5, 1, 2, 2.01, "EKG")
        return obtain_trapezoid_fuzzy_value(ekg, [-0.5, 1, 2, 2.01])


class ChestPain:

    def __init__(self):
        self.fuzzy_ranges = {
            "no": [0, 0, 0.5, 0.5],
            "yes": [0.5, 0.5, 1, 1]
        }

    def calc_fuzzy(self, chest_pain):
        if isinstance(chest_pain, str):
            if chest_pain == 'no':
                chest_pain = random.uniform(0.01, 0.5)
            elif chest_pain == 'yes':
                chest_pain = random.uniform(0.5, 1)
        plot_trapezoid_fuzzy_value(
            0, 1, chest_pain, 0, 1, 1, 1.01, "Bolest v hrudi")
        return obtain_trapezoid_fuzzy_value(chest_pain, [0, 1, 1, 1.01])


def get_final_result(data):
    age_class = Age()
    sex_class = Sex()
    height_class = Height()
    weight_class = Weight()

    st_bp_class = ST_BloodPressure()
    dt_bp_class = DT_BloodPressure()
    sugar_class = Sugar()
    cholesterol_class = Cholesterol()
    heart_rate_class = HeartRate()
    ekg_class = EKG()
    chest_pain_class = ChestPain()

    # check if data has string value instad of number
    if data['Vek'] == 'young' or data['Vek'] == 'middle age' or data['Vek'] == 'old' or data['Vek'] == 'very old':
        age = age_class.calc_fuzzy(data['Vek'])
    else:
        age = age_class.calc_fuzzy(int(data['Vek']))

    if data['Pohlavie'] == 'M' or data['Pohlavie'] == 'F':
        sex = sex_class.calc_fuzzy(str(data['Pohlavie']))
    else:
        print("Pohlavie musi byt M alebo F")

    if data['Vyska'] == 'short' or data['Vyska'] == 'medium' or data['Vyska'] == 'tall':
        height = height_class.calc_fuzzy(data['Vyska'])
    else:
        height = height_class.calc_fuzzy(float(data['Vyska']))

    if data['Vaha'] == 'light' or data['Vaha'] == 'medium' or data['Vaha'] == 'heavy':
        weight = weight_class.calc_fuzzy(data['Vaha'])
    else:
        weight = weight_class.calc_fuzzy(float(data['Vaha']))

    if data['Systolický krvný tlak'] == 'low' or data['Systolický krvný tlak'] == 'medium' or data['Systolický krvný tlak'] == 'high':
        st_bp = st_bp_class.calc_fuzzy(data['Systolický krvný tlak'])
    else:
        st_bp = st_bp_class.calc_fuzzy(int(data['Systolický krvný tlak']))

    if data['Diastolický krvný tlak'] == 'low' or data['Diastolický krvný tlak'] == 'medium' or data['Diastolický krvný tlak'] == 'high':
        dt_bp = dt_bp_class.calc_fuzzy(data['Diastolický krvný tlak'])
    else:
        dt_bp = dt_bp_class.calc_fuzzy(int(data['Diastolický krvný tlak']))

    if data['Hladina cukru'] == 'low' or data['Hladina cukru'] == 'medim' or data['Hladina cukru'] == 'high':
        sugar = sugar_class.calc_fuzzy(data['Hladina cukru'])
    else:
        sugar = sugar_class.calc_fuzzy(int(data['Hladina cukru']))

    if data['Cholesterol'] == 'low' or data['Cholesterol'] == 'medium high' or data['Cholesterol'] == 'very high' or data['Cholesterol'] == 'extremely high':
        cholesterol = cholesterol_class.calc_fuzzy(data['Cholesterol'])
    else:
        cholesterol = cholesterol_class.calc_fuzzy(int(data['Cholesterol']))

    if data['Tep'] == 'small' or data['Tep'] == 'medium' or data['Tep'] == 'big':
        heart_rate = heart_rate_class.calc_fuzzy(data['Tep'])
    else:
        heart_rate = heart_rate_class.calc_fuzzy(int(data['Tep']))

    if data['EKG'] == 'normal' or data['EKG'] == 'abnormal' or data['EKG'] == 'hypertrophy':
        ekg = ekg_class.calc_fuzzy(data['EKG'])
    else:
        ekg = ekg_class.calc_fuzzy(float(data['EKG']))

    if data['Bolesť v hrudi'] == 'no' or data['Bolesť v hrudi'] == 'yes':
        chest_pain = chest_pain_class.calc_fuzzy(data['Bolesť v hrudi'])
    else:
        print("chyba v chest pain")

    age, sex, height, weight, st_bp, dt_bp, sugar, cholesterol, heart_rate, ekg, chest_pain = [round(
        var, 2) for var in (age, sex, height, weight, st_bp, dt_bp, sugar, cholesterol, heart_rate, ekg, chest_pain)]
    return age, sex, height, weight, st_bp, dt_bp, sugar, cholesterol, heart_rate, ekg, chest_pain
