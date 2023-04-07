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
            "young": [0, 30],
            "middle age": [30, 50],
            "old": [50, 75],
            "very old": [75, 100]
        }

    def calc_fuzzy(self, age):
        # if age is string
        if isinstance(age, str):
            if age == 'young':
                age = (0 + 30)/2
            elif age == 'middle age':
                age = (30 + 50)/2
            elif age == 'old':
                age = (50 + random.randint(50, 75))/2
            elif age == 'very old':
                age = (75 + 100)/2
        plot_sigmoid_fuzzy_value(0, 100, age, 50, 10, "Vek")
        return obtain_sigmoid_fuzzy_value(age, 50, 10)

# typical singletone function


class Sex:

    def __init__(self):
        self.fuzzy_ranges = {
            "M": 0.5,
            "F": 0.3
        }

    def calc_fuzzy(self, sex):

        if sex == 'M':
            return 0.5
        else:
            return 0.3


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
        plot_cup_gaussian_fuzzy_value(60, 210, height, 150, 25, "Vyska")
        return 1 - obtain_gaussian_fuzzy_value(height, 150, 25)


class Weight:

    def __init__(self):
        self.fuzzy_ranges = {
            "light": [20, 50],
            "medium": [50, 80],
            "heavy": [80, 120]
        }

    def calc_fuzzy(self, weight):
        if isinstance(weight, str):
            if weight == 'light':
                weight = (20 + 50)/2
            elif weight == 'medium':
                weight = (50 + 80)/2
            elif weight == 'heavy':
                weight = (80 + 120)/2
        plot_cup_gaussian_fuzzy_value(20, 120, weight, 60, 20, "Vaha")
        return 1 - obtain_gaussian_fuzzy_value(weight, 60, 20)


class ST_BloodPressure:

    def __init__(self):
        self.fuzzy_ranges = {
            "low": [0, 0, 70, 100],
            "medium": [70, 70, 100, 120],
            "high": [100, 100, 120, 140],
            "very high": [120, 120, 170, 170]
        }

    def calc_fuzzy(self, bp):
        if isinstance(bp, str):
            if bp == 'low':
                bp = (70 + 100)/2
            elif bp == 'medium':
                bp = (100 + 120)/2
            elif bp == 'high':
                bp = (120 + random.randint(120, 140))/2
            elif bp == 'very heigh':
                bp = (140 + 170)/2
        plot_sigmoid_fuzzy_value(
            0, 170, bp, 120, 10, "Systolic Blood Pressure")
        return obtain_sigmoid_fuzzy_value(bp, 120, 10)


class DT_BloodPressure:

    def __init__(self):
        self.fuzzy_ranges = {
            "low": [0, 0, 60, 80],
            "medium": [60, 60, 80, 90],
            "high": [80, 80, 90, 120]
        }

    def calc_fuzzy(self, bp):
        if isinstance(bp, str):
            if bp == 'low':
                bp = (0 + 60)/2
            elif bp == 'medium':
                bp = (60 + 80)/2
            elif bp == 'high':
                bp = (80 + random.randint(80, 90))/2
            elif bp == 'very high':
                bp = (90 + 120)/2
        plot_sigmoid_fuzzy_value(
            0, 120, bp, 78, 10, "Diastolic Blood Pressure")
        return obtain_sigmoid_fuzzy_value(bp, 78, 10)


class Cholesterol:

    def __init__(self):
        self.fuzzy_ranges = {
            "low": [0, 0, 40, 130],
            "medium high": [40, 40, 130, 160],
            "high": [130, 130, 160, 190],
            "very high": [160, 160, 190, 200],
            "extremely high": [190, 190, 300, 300]
        }

    def calc_fuzzy(self, cholesterol):
        if isinstance(cholesterol, str):
            if cholesterol == 'low':
                cholesterol = (40 + 130)/2
            elif cholesterol == 'medium high':
                cholesterol = (130 + 160)/2
            elif cholesterol == 'high':
                cholesterol = (160 + 190)/2
            elif cholesterol == 'very high':
                cholesterol = (190 + 200)/2
            elif cholesterol == 'extremely high':
                cholesterol = (200 + 300)/2
        plot_sigmoid_fuzzy_value(0, 300, cholesterol, 160, 40, "Cholesterol")
        return obtain_sigmoid_fuzzy_value(cholesterol, 160, 40)


class Sugar:

    def __init__(self):
        self.fuzzy_ranges = {
            "low": [0, 0, 100, 120],
            "medium": [100, 100, 120, 150],
            "high": [120, 120, 150, 240]
        }

    def calc_fuzzy(self, sugar):
        if isinstance(sugar, str):
            if sugar == 'low':
                sugar = (0 + 100)/2
            elif sugar == 'medium':
                sugar = (100 + 120)/2
            elif sugar == 'high':
                sugar = (120 + 150)/2
        plot_trapezoid_fuzzy_value(
            0, 240, sugar, 0, 220, 240, 241, "Hladina cukru")
        return obtain_trapezoid_fuzzy_value(sugar, [0, 220, 240, 240])


class HeartRate:

    def __init__(self):
        self.fuzzy_ranges = {
            "low": [0, 0, 60, 100],
            "medium": [60, 60, 100, 140],
            "high": [100, 100, 140, 200]
        }

    def calc_fuzzy(self, hr):
        if isinstance(hr, str):
            if hr == 'low':
                hr = (0 + 60)/2
            elif hr == 'medium':
                hr = (60 + random.randint(60, 140))/2
            elif hr == 'high':
                hr = (100 + random.randint(150, 200))/2
        plot_trapezoid_fuzzy_value(
            0, 200, hr, 0, 165, 200, 201, "Tepova frekvencia")
        return obtain_trapezoid_fuzzy_value(hr, [0, 165, 200, 200])


class EKG:

    def __init__(self):
        self.fuzzy_ranges = {
            "normal": [-0.5, -0.5, 0.4, 0.4],
            "abnormal": [0.4, 0.4, 1, 1],
            "hypertrophy": [1, 1, 2, 2.01]
        }

    def calc_fuzzy(self, ekg):
        if isinstance(ekg, str):
            if ekg == 'normal':
                ekg = random.uniform(-0.5, 0.4)
            elif ekg == 'abnormal':
                ekg = random.uniform(0.4, 1)
            elif ekg == 'hypertrophy':
                ekg = random.uniform(1, 2)
        plot_trapezoid_fuzzy_value(
            -0.5, 2, ekg, -0.5, 1.5, 2, 2.01, "EKG")
        return obtain_trapezoid_fuzzy_value(ekg, [-0.5, 1.5, 2, 2.01])


class ChestPain:

    def __init__(self):
        self.fuzzy_ranges = {
            "typical": [0, 0, 0.25, 0.25],
            "atypical": [0.25, 0.25, 0.45, 0.45],
            "non-anginal": [0.45, 0.45, 0.65, 0.65],
            "asymptomatic": [0.65, 0.65, 1, 1]
        }

    def calc_fuzzy(self, chest_pain):
        if isinstance(chest_pain, str):
            if chest_pain == 'typical':
                chest_pain = random.uniform(0, 0.25)
            elif chest_pain == 'atypical':
                chest_pain = random.uniform(0.26, 0.45)
            elif chest_pain == 'non-anginal':
                chest_pain = random.uniform(0.46, 0.65)
            elif chest_pain == 'asymptomatic':
                chest_pain = random.uniform(0.66, 1)
        plot_trapezoid_fuzzy_value(
            0, 2, chest_pain, 0, 1, 2, 2.01, "Bolest v hrudnej kosti")
        return obtain_trapezoid_fuzzy_value(chest_pain, [0, 1, 2, 2.01])


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

    if data['Hladina cukru'] == 'low' or data['Hladina cukru'] == 'medium' or data['Hladina cukru'] == 'high':
        sugar = sugar_class.calc_fuzzy(data['Hladina cukru'])
    else:
        sugar = sugar_class.calc_fuzzy(int(data['Hladina cukru']))

    if data['Cholesterol'] == 'low' or data['Cholesterol'] == 'medium high' or data['Cholesterol'] == 'high' or data['Cholesterol'] == 'very high' or data['Cholesterol'] == 'extremely high':
        cholesterol = cholesterol_class.calc_fuzzy(data['Cholesterol'])
    else:
        cholesterol = cholesterol_class.calc_fuzzy(int(data['Cholesterol']))

    if data['Tep'] == 'low' or data['Tep'] == 'medium' or data['Tep'] == 'high':
        heart_rate = heart_rate_class.calc_fuzzy(data['Tep'])
    else:
        heart_rate = heart_rate_class.calc_fuzzy(int(data['Tep']))

    if data['EKG'] == 'normal' or data['EKG'] == 'abnormal' or data['EKG'] == 'hypertrophy':
        ekg = ekg_class.calc_fuzzy(data['EKG'])
    else:
        ekg = ekg_class.calc_fuzzy(float(data['EKG']))

    if data['Bolesť v hrudi'] == 'typical' or data['Bolesť v hrudi'] == 'atypical' or data['Bolesť v hrudi'] == 'non-anginal' or data['Bolesť v hrudi'] == 'asymptomatic':
        chest_pain = chest_pain_class.calc_fuzzy(data['Bolesť v hrudi'])
    else:
        print("chyba v chest pain")

    age, sex, height, weight, st_bp, dt_bp, sugar, cholesterol, heart_rate, ekg, chest_pain = [round(
        var, 2) for var in (age, sex, height, weight, st_bp, dt_bp, sugar, cholesterol, heart_rate, ekg, chest_pain)]
    return age, sex, height, weight, st_bp, dt_bp, sugar, cholesterol, heart_rate, ekg, chest_pain
