import random
from FuzzyficateFunctions import obtain_trapezoid_fuzzy_value
from FuzzyficateFunctions import obtain_gaussian_fuzzy_value
from FuzzyficateFunctions import obtain_sigmoid_fuzzy_value
from FuzzyficateFunctions import obtain_triangular_fuzzy_value
from FuzzyficateFunctions import plot_sigmoid_fuzzy_value
from FuzzyficateFunctions import plot_cup_gaussian_fuzzy_value
from FuzzyficateFunctions import plot_trapezoid_fuzzy_value
from FuzzyficateFunctions import plot_triangular_fuzzy_value


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


class VericiguatTherapy:

    def __init__(self):
        self.fuzzy_ranges = {
            "false": [0, 0, 0.5, 0.5],
            "true": [0.5, 0.5, 1, 1],
        }

    def calc_fuzzy(self, uziva_vericiguat, stk=None, gfr=None, symptomaticka_hypotenzia=None):

        if stk is not None and (isinstance(stk, int) or isinstance(stk, float)):
            stk = min(100, max(0, stk))
        if gfr is not None and (isinstance(gfr, int) or isinstance(gfr, float)):
            gfr = min(100, max(0, gfr))

        if uziva_vericiguat == "true":
            uziva_vericiguat = 1
        elif uziva_vericiguat == "false":
            uziva_vericiguat = 0

        if symptomaticka_hypotenzia == "true":
            symptomaticka_hypotenzia = 1.0
        elif symptomaticka_hypotenzia == "false":
            symptomaticka_hypotenzia = 0.0

        if stk is not None:
            plot_trapezoid_fuzzy_value(
                0, 100, stk, 0, 10, 20, 100, "sTK")
        if gfr is not None:
            plot_trapezoid_fuzzy_value(
                0, 100, gfr, 0, 15, 25, 100, "GFR")
        if symptomaticka_hypotenzia is not None:
            plot_triangular_fuzzy_value(
                0, 1.0, symptomaticka_hypotenzia, 0, 1, 1, "Symptomaticka hypotenzia")

        if uziva_vericiguat == 0 and stk is not None and stk < 100:
            print("uziva_vericiguat == 0 and stk is not None and stk < 100")
            return uziva_vericiguat, round(obtain_trapezoid_fuzzy_value(stk, [0, 10, 20, 100]), 2)
        elif uziva_vericiguat == 0 and gfr is not None and gfr < 15:
            print("uziva_vericiguat == 0 and gfr is not None and gfr < 15")

            return uziva_vericiguat, round(obtain_trapezoid_fuzzy_value(gfr, [0, 15, 20, 100]), 2)
        elif uziva_vericiguat == 1 and stk is not None and stk < 90:
            print("uziva_vericiguat == 1 and stk is not None and stk < 90")
            return uziva_vericiguat, round(obtain_trapezoid_fuzzy_value(stk, [0, 10, 20, 100]), 2)
        elif uziva_vericiguat == 1 and gfr is not None and gfr < 15:
            print("uziva_vericiguat == 1 and gfr is not None and gfr < 15")
            return uziva_vericiguat, round(obtain_trapezoid_fuzzy_value(gfr, [0, 15, 20, 100]), 2)
        elif uziva_vericiguat == 1 and symptomaticka_hypotenzia == 1:
            print("uziva_vericiguat == 1 and symptomaticka_hypotenzia == 1")
            return uziva_vericiguat, round(obtain_triangular_fuzzy_value(symptomaticka_hypotenzia, [0, 1.01, 1.01]), 2)
        elif uziva_vericiguat == 0 and stk is None and gfr is None and symptomaticka_hypotenzia is None:
            print("uziva_vericiguat == 0")
            uziva_vericiguat = 0.5
            return uziva_vericiguat
        else:
            print("Nespravna hodnota")
            return -1


class IvabradineTherapy:

    def __init__(self):
        self.fuzzy_ranges = {
            "false": [0, 0, 0.5, 0.5],
            "true": [0.5, 0.5, 1, 1],
        }

    def calc_fuzzy(self, uziva_ivabradin, fibrilacia_predsieni=None, sf=None, vek=None, symptomaticka_bradykardia=None, gfr=None):

        if vek is not None and (isinstance(vek, int) or isinstance(vek, float)):
            vek = min(120, max(0, vek))
        if sf is not None and (isinstance(sf, int) or isinstance(sf, float)):
            sf = min(100, max(0, sf))
        if gfr is not None and (isinstance(gfr, int) or isinstance(gfr, float)):
            gfr = min(100, max(0, gfr))

        if uziva_ivabradin == "true":
            uziva_ivabradin = 1.0
        elif uziva_ivabradin == "false":
            uziva_ivabradin = 0.0

        if fibrilacia_predsieni == "true":
            fibrilacia_predsieni = 1.0
        elif fibrilacia_predsieni == "false":
            fibrilacia_predsieni = 0.0

        if symptomaticka_bradykardia == "true":
            symptomaticka_bradykardia = 1.0
        elif symptomaticka_bradykardia == "false":
            symptomaticka_bradykardia = 0.0

        if vek is not None:
            plot_trapezoid_fuzzy_value(
                0, 120, vek, 0, 60, 75, 120, "Vek")
        if sf is not None:
            plot_trapezoid_fuzzy_value(
                0, 100, sf, 0, 25, 35, 100, "SF")
        if gfr is not None:
            plot_trapezoid_fuzzy_value(
                0, 100, gfr, 0, 15, 20, 100, "GFR")
        if symptomaticka_bradykardia is not None:
            plot_triangular_fuzzy_value(
                0, 1.0, symptomaticka_bradykardia, 0, 1, 1, "Symptomaticka bradykardia")
        if fibrilacia_predsieni is not None:
            plot_triangular_fuzzy_value(
                0, 1.0, fibrilacia_predsieni, 0, 1, 1, "Fibrilacia predsieni")

        if uziva_ivabradin == 0 and gfr is not None and gfr < 15:
            print("uziva_ivabradin == 0 and gfr is not None and gfr < 15")
            return uziva_ivabradin, round(obtain_trapezoid_fuzzy_value(gfr, [0, 15, 20, 100]), 2)
        elif uziva_ivabradin == 0 and fibrilacia_predsieni is not None and fibrilacia_predsieni == 1:
            print("uziva_ivabradin == 0 and fibrilacia_predsieni == 1")
            return uziva_ivabradin, round(obtain_triangular_fuzzy_value(fibrilacia_predsieni, [0, 1.01, 1.01]), 2)
        elif uziva_ivabradin == 0 and vek is not None and vek > 75:
            print("uziva_ivabradin == 0 and vek is not None and vek > 75")
            return uziva_ivabradin, round(obtain_trapezoid_fuzzy_value(vek, [0, 60, 75, 120]), 2)
        elif uziva_ivabradin == 0 and gfr is None and fibrilacia_predsieni is None and vek is None and sf is None and symptomaticka_bradykardia is None:
            print("uziva_ivabradin == 0")
            uziva_ivabradin = 0.5
            return uziva_ivabradin
        elif uziva_ivabradin == 1 and sf is not None and sf < 50:
            print("uziva_ivabradin == 1 and sf is not None and sf < 50")
            return uziva_ivabradin, round(obtain_trapezoid_fuzzy_value(sf, [0, 25, 35, 100]), 2)
        elif uziva_ivabradin == 1 and symptomaticka_bradykardia == 1:
            print("uziva_ivabradin == 1 and symptomaticka_bradykardia == 1")
            return uziva_ivabradin, round(obtain_triangular_fuzzy_value(symptomaticka_bradykardia, [0, 1.01, 1.01]), 2)
        else:
            print("neexistujuce pravidlo")
            return None, None


"""
print(IvabradineTherapy().calc_fuzzy("false", gfr=10))
print(IvabradineTherapy().calc_fuzzy("true", None, None, None, "true", None))
print(IvabradineTherapy().calc_fuzzy("true", None, None, None, "false", None))
print(IvabradineTherapy().calc_fuzzy("false", None, None, None, None, 10))
print(IvabradineTherapy().calc_fuzzy("false", None, None, None, None, 20))
print(IvabradineTherapy().calc_fuzzy("false", "true", None, None, None, None))
print(IvabradineTherapy().calc_fuzzy("false", "false", None, None, None, None))
print(IvabradineTherapy().calc_fuzzy("false", None, 50, None, None, None))
print(IvabradineTherapy().calc_fuzzy("true", None, 40, None, None, None))
print(IvabradineTherapy().calc_fuzzy("false", None, None, 80, None, None))
print(IvabradineTherapy().calc_fuzzy("false", None, None, 70, None, None))
"""

"""
if Uziva digoxin is false AND Pomaly rytmus is true THEN "Nezačať s terapiou."
if Uziva digoxin is false AND AV vlok is II, III THEN "Nezačať s terapiou."
if Uziva digoxin is true AND Pomaly rytmus is true THEN "Vysadiť alebo redukovať digoxin."
if Uziva digoxin is true AND AV Vlok is II, III THEN "Vysadiť alebo redukovať digoxin."
if Uziva digoxin is true AND Hodnota digoxinu v krvi > 1.05  THEN "Vysadiť alebo redukovať digoxin."
if Hodnota digoxinu v krvi is [0,64..1,05] THEN "Pokračovať v aktuálnej terapii."
if Hodnota digoxinu v krvi < 0.64 THEN "Pridať digoxin."
"""


class DigoxinTherapy:
    def __init__(self):
        self.fuzzy_ranges = {
            "false": [0, 0, 0.5, 0.5],
            "true": [0.5, 0.5, 1, 1],
        }

    def calc_fuzzy(self, uziva_digoxin, pomaly_rytmus=None, av_blok=None, hodnota_digoxinu=None):

        if hodnota_digoxinu is not None and (isinstance(hodnota_digoxinu, int) or isinstance(hodnota_digoxinu, float)):
            hodnota_digoxinu = float(hodnota_digoxinu)

        if av_blok is not None and av_blok == "II" or av_blok == "III":
            av_blok = 1
        else:
            av_blok = 0

        if uziva_digoxin == "true":
            uziva_digoxin = 1
        elif uziva_digoxin == "false":
            uziva_digoxin = 0

        if pomaly_rytmus == "true":
            pomaly_rytmus = 1
        elif pomaly_rytmus == "false":
            pomaly_rytmus = 0

        if uziva_digoxin == 0 and pomaly_rytmus is not None and pomaly_rytmus == 1:
            print("uziva_digoxin == 0 and pomaly_rytmus == 1")
            return uziva_digoxin, round(obtain_triangular_fuzzy_value(pomaly_rytmus, [0, 1.01, 1.01]), 2)
        elif uziva_digoxin == 0 and av_blok is not None and av_blok == 1:
            print("uziva_digoxin == 0 and av_blok == 1")
            return uziva_digoxin, round(obtain_triangular_fuzzy_value(av_blok, [0, 1.01, 1.01]), 2)
        elif uziva_digoxin == 1 and pomaly_rytmus is not None and pomaly_rytmus == 1:
            print("uziva_digoxin == 1 and pomaly_rytmus == 1")
            return uziva_digoxin, round(obtain_triangular_fuzzy_value(pomaly_rytmus, [0, 1.01, 1.01]), 2)
        elif uziva_digoxin == 1 and av_blok is not None and av_blok == 1:
            print("uziva_digoxin == 1 and av_blok == 1")
            return uziva_digoxin, round(obtain_triangular_fuzzy_value(av_blok, [0, 1.01, 1.01]), 2)
        elif uziva_digoxin == 1 and hodnota_digoxinu is not None and hodnota_digoxinu > 1.05:
            print("uziva_digoxin == 1 and hodnota_digoxinu > 1.05")
            return uziva_digoxin, round(obtain_triangular_fuzzy_value(hodnota_digoxinu, [0, 1.01, 1.01]), 2)
        elif uziva_digoxin == 1 and hodnota_digoxinu is not None and hodnota_digoxinu < 0.64:
            print("uziva_digoxin == 1 and hodnota_digoxinu < 0.64")
            return uziva_digoxin, round(obtain_triangular_fuzzy_value(hodnota_digoxinu, [0, 1.01, 1.01]), 2)
        elif uziva_digoxin == 1 and hodnota_digoxinu is not None and hodnota_digoxinu >= 0.64 and hodnota_digoxinu <= 1.05:
            print(
                "uziva_digoxin == 1 and hodnota_digoxinu >= 0.64 and hodnota_digoxinu <= 1.05")
            return uziva_digoxin, round(obtain_triangular_fuzzy_value(hodnota_digoxinu, [0, 1.01, 1.01]), 2)
        else:
            print("neexistuje pravidlo")
            return -1


"""
print(DigoxinTherapy().calc_fuzzy("true", "true", "II", 1.07))
print(DigoxinTherapy().calc_fuzzy("true", "false", "IV", 0.0))
"""
"""

if LBBB is true AND QRS is >=150 THEN "Doporučene zavedenie CRT"
if LBBB is true AND QRS is [130,..,149] THEN "Malo by byt zvazene zavedenie CRT"
if LBBB is false AND QRS >= 150 THEN "Malo by byt zvazene zavedenie CRT"
if LBBB is false AND QRS is [130,..,149] THEN "Môže byt zvazene zavedenie CRT"


"""


class LbbbTherapy:
    def __init__(self):
        self.fuzzy_ranges = {
            "false": [0, 0, 0.5, 0.5],
            "true": [0.5, 0.5, 1, 1],
        }

    def calc_fuzzy(self, lbbb, qrs):
        if lbbb == "true":
            lbbb = 1
        elif lbbb == "false":
            lbbb = 0

        if qrs is not None and (isinstance(qrs, int) or isinstance(qrs, float)):
            qrs = float(qrs)

        if lbbb == 1 and qrs >= 150:
            return lbbb, round(obtain_triangular_fuzzy_value(qrs, [0, 200.1, 300.0]), 2)
        elif lbbb == 1 and qrs >= 130 and qrs <= 149:
            return lbbb, round(obtain_triangular_fuzzy_value(qrs, [0, 130.0, 150.1]), 2)
        elif lbbb == 0 and qrs >= 150:
            return lbbb, round(obtain_triangular_fuzzy_value(qrs, [0, 150.1, 400.0]), 2)
        elif lbbb == 0 and qrs >= 130 and qrs <= 149:
            return lbbb, round(obtain_triangular_fuzzy_value(qrs, [0, 130.0, 149.0]), 2)
        else:
            return -1


print(LbbbTherapy().calc_fuzzy("true", 150))
print(LbbbTherapy().calc_fuzzy("true", 149))
print(LbbbTherapy().calc_fuzzy("false", 165))
print(LbbbTherapy().calc_fuzzy("false", 130))


def get_final_result_fuzzy(data):
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

    age_value = data['Vek']
    sex_value = data['Pohlavie']
    height_value = data['Vyska']
    weight_value = data['Vaha']
    st_bp_value = data['Systolický krvný tlak']
    dt_bp_value = data['Diastolický krvný tlak']
    sugar_value = data['Hladina cukru']
    cholesterol_value = data['Cholesterol']
    heart_rate_value = data['Tep']
    ekg_value = data['EKG']
    chest_pain_value = data['Bolesť v hrudi']
    age, sex, height, weight, st_bp, dt_bp, sugar, cholesterol, heart_rate, ekg, chest_pain = None, None, None, None, None, None, None, None, None, None, None

    # check if data has string value instad of number
    if age_value is not None:
        if isinstance(age_value, str) and (age_value == 'young' or age_value == 'middle age' or age_value == 'old' or age_value == 'very old'):
            age = round(age_class.calc_fuzzy(age_value), 2)
        else:
            age = round(age_class.calc_fuzzy(int(age_value)), 2)

    if sex_value is not None:
        if isinstance(sex_value, str) and (sex_value == 'M' or sex_value == 'F'):
            sex = round(sex_class.calc_fuzzy(str(sex_value)), 2)
        else:
            print("Pohlavie musi byt M alebo F")

    if height_value is not None:
        if isinstance(height_value, str) and (height_value == 'short' or height_value == 'medium' or height_value == 'tall'):
            height = round(height_class.calc_fuzzy(height_value), 2)
        else:
            height = round(height_class.calc_fuzzy(float(height_value)), 2)

    if weight_value is not None:
        if isinstance(weight_value, str) and (weight_value == 'light' or weight_value == 'medium' or weight_value == 'heavy'):
            weight = round(weight_class.calc_fuzzy(weight_value), 2)
        else:
            weight = round(weight_class.calc_fuzzy(float(weight_value)), 2)

    if st_bp_value is not None:
        if isinstance(st_bp_value, str) and (st_bp_value == 'low' or st_bp_value == 'medium' or st_bp_value == 'high'):
            st_bp = round(st_bp_class.calc_fuzzy(st_bp_value), 2)
        else:
            st_bp = round(st_bp_class.calc_fuzzy(int(st_bp_value)), 2)

    if dt_bp_value is not None:
        if isinstance(dt_bp_value, str) and (dt_bp_value == 'low' or dt_bp_value == 'medium' or dt_bp_value == 'high'):
            dt_bp = round(dt_bp_class.calc_fuzzy(dt_bp_value), 2)
        else:
            dt_bp = round(dt_bp_class.calc_fuzzy(int(dt_bp_value)), 2)

    if sugar_value is not None:
        if isinstance(sugar_value, str) and (sugar_value == 'low' or sugar_value == 'medium' or sugar_value == 'high'):
            sugar = round(sugar_class.calc_fuzzy(sugar_value), 2)
        else:
            sugar = round(sugar_class.calc_fuzzy(int(sugar_value)), 2)

    if cholesterol_value is not None:
        if isinstance(cholesterol_value, str) and (cholesterol_value == 'low' or cholesterol_value == 'medium high' or cholesterol_value == 'high' or cholesterol_value == 'very high' or cholesterol_value == 'extremely high'):
            cholesterol = round(
                cholesterol_class.calc_fuzzy(cholesterol_value), 2)
        else:
            cholesterol = round(cholesterol_class.calc_fuzzy(
                int(cholesterol_value)), 2)

    if heart_rate_value is not None:
        if isinstance(heart_rate_value, str) and (heart_rate_value == 'low' or heart_rate_value == 'medium' or heart_rate_value == 'high'):
            heart_rate = round(
                heart_rate_class.calc_fuzzy(heart_rate_value), 2)
        else:
            heart_rate = round(heart_rate_class.calc_fuzzy(
                int(heart_rate_value)), 2)

    if ekg_value is not None:
        if isinstance(ekg_value, str) and (ekg_value == 'normal' or ekg_value == 'abnormal' or ekg_value == 'hypertrophy'):
            ekg = round(ekg_class.calc_fuzzy(ekg_value), 2)
        else:
            ekg = round(ekg_class.calc_fuzzy(float(ekg_value)), 2)

    if chest_pain_value is not None:
        if isinstance(chest_pain_value, str) and (chest_pain_value == 'typical' or chest_pain_value == 'atypical' or chest_pain_value == 'non-anginal' or chest_pain_value == 'asymptomatic'):
            chest_pain = round(
                chest_pain_class.calc_fuzzy(chest_pain_value), 2)
        else:
            print("chyba v chest pain")

    # if all of these  age, sex, height, weight, st_bp, dt_bp, sugar, cholesterol, heart_rate, ekg, chest_pain are None then return None
    if age is None and sex is None and height is None and weight is None and st_bp is None and dt_bp is None and sugar is None and cholesterol is None and heart_rate is None and ekg is None and chest_pain is None:
        print("V petri sieti sa nenachadza ziadna z hodnot")
        return None
    else:
        data['Vek'] = age
        data['Pohlavie'] = sex
        data['Vyska'] = height
        data['Vaha'] = weight
        data['Systolický krvný tlak'] = st_bp
        data['Diastolický krvný tlak'] = dt_bp
        data['Hladina cukru'] = sugar
        data['Cholesterol'] = cholesterol
        data['Tep'] = heart_rate
        data['EKG'] = ekg
        data['Bolesť v hrudi'] = chest_pain


def get_final_result_logical(data):

    # check if data['uziva vericiguat'] key exists

    if 'Uziva vericiguat' in data:
        if data['Uziva vericiguat'] == 'false' or data['Uziva vericiguat'] == 'true':

            vericiguat = data['Uziva vericiguat']
            sTK = float(data['sTK']) if data['sTK'] is not None else None
            GFR = float(data['GFR']) if data['GFR'] is not None else None
            symptomaticka_hypotenzia = data['symptomaticka hypotenzia']
            if sTK is not None:
                value = VericiguatTherapy().calc_fuzzy(
                    vericiguat, sTK, GFR, symptomaticka_hypotenzia)
                data['sTK'] = value[1]
                data['Uziva vericiguat'] = value[0]
            if GFR is not None:
                value = VericiguatTherapy().calc_fuzzy(
                    vericiguat, sTK, GFR, symptomaticka_hypotenzia)
                data['GFR'] = value[1]
                data['Uziva vericiguat'] = value[0]

            if symptomaticka_hypotenzia is not None:
                value = VericiguatTherapy().calc_fuzzy(
                    vericiguat, sTK, GFR, symptomaticka_hypotenzia)
                data['symptomaticka hypotenzia'] = value[1]
                data['Uziva vericiguat'] = value[0]

            if vericiguat is not None and sTK is None and GFR is None and symptomaticka_hypotenzia is None:
                data['Uziva vericiguat'] = VericiguatTherapy().calc_fuzzy(
                    vericiguat, None, None, None)[0]

        else:
            print("Uziva vericiguat musi byt true alebo false")
    if 'Uziva ivabradin' in data:
        if data['Uziva ivabradin'] == 'false' or data['Uziva ivabradin'] == 'true':

            ivabradin = data['Uziva ivabradin']
            fibrilacia_predsieni = data['fibrilacia predsieni']
            sf = float(data['sf']) if data['sf'] is not None else None
            vek = int(data['vek']) if data['vek'] is not None else None
            gfr = float(data['GFR']) if data['GFR'] is not None else None
            symptomaticka_bradykardia = data['symptomaticka bradykardia']
            if fibrilacia_predsieni is not None:
                value = IvabradineTherapy().calc_fuzzy(ivabradin, fibrilacia_predsieni,
                                                       sf, vek, symptomaticka_bradykardia, gfr)
                data['fibrilacia predsieni'] = value[1]
                data['Uziva ivabradin'] = value[0]
            if sf is not None:
                value = IvabradineTherapy().calc_fuzzy(ivabradin, fibrilacia_predsieni,
                                                       sf, vek, symptomaticka_bradykardia, gfr)
                data['sf'] = value[1]
                data['Uziva ivabradin'] = value[0]
            if vek is not None:
                value = IvabradineTherapy().calc_fuzzy(ivabradin, fibrilacia_predsieni,
                                                       sf, vek, symptomaticka_bradykardia, gfr)
                data['vek'] = value[1]
                data['Uziva ivabradin'] = value[0]
            if gfr is not None:
                value = IvabradineTherapy().calc_fuzzy(ivabradin, fibrilacia_predsieni,
                                                       sf, vek, symptomaticka_bradykardia, gfr)
                data['GFR'] = value[1]
                data['Uziva ivabradin'] = value[0]
            if symptomaticka_bradykardia is not None:
                value = IvabradineTherapy().calc_fuzzy(ivabradin, fibrilacia_predsieni,
                                                       sf, vek, symptomaticka_bradykardia, gfr)
                data['symptomaticka bradykardia'] = value[1]
                data['Uziva ivabradin'] = value[0]
            if ivabradin is not None and fibrilacia_predsieni is None and sf is None and vek is None and gfr is None and symptomaticka_bradykardia is None:
                data['Uziva ivabradin'] = IvabradineTherapy().calc_fuzzy(
                    ivabradin, None, None, None, None, None)[0]
        else:
            print("Uziva ivabradin musi byt true alebo false")

    if 'Uziva digoxin' in data:
        if data['Uziva digoxin'] == 'false' or data['Uziva digoxin'] == 'true':
            digoxin = data['Uziva digoxin']
            fibrilacia_predsieni = data['fibrilacia predsieni']
            pomaly_rytmus = data['pomaly rytmus']
            av = data['AV blok']
            di_val = data['hodnota digoxinu']

            if fibrilacia_predsieni is not None:
                value = DigoxinTherapy().calc_fuzzy(digoxin, fibrilacia_predsieni,
                                                    pomaly_rytmus, av, di_val)
                data['fibrilacia predsieni'] = value[1]
                data['Uziva digoxin'] = value[0]
            if pomaly_rytmus is not None:
                value = DigoxinTherapy().calc_fuzzy(digoxin, fibrilacia_predsieni,
                                                    pomaly_rytmus, av, di_val)
                data['pomaly rytmus'] = value[1]
                data['Uziva digoxin'] = value[0]
            if av is not None:
                value = DigoxinTherapy().calc_fuzzy(digoxin, fibrilacia_predsieni,
                                                    pomaly_rytmus, av, di_val)
                data['AV blok'] = value[1]
                data['Uziva digoxin'] = value[0]
            if di_val is not None:
                value = DigoxinTherapy().calc_fuzzy(digoxin, fibrilacia_predsieni,
                                                    pomaly_rytmus, av, di_val)
                data['hodnota digoxinu'] = value[1]
                data['Uziva digoxin'] = value[0]
            if digoxin is not None and fibrilacia_predsieni is None and pomaly_rytmus is None and av is None and di_val is None:
                data['Uziva digoxin'] = DigoxinTherapy().calc_fuzzy(
                    digoxin, None, None, None, None)[0]
        else:
            print("Uziva digoxin musi byt true alebo false")
    if 'LBBB' in data:
        if data['LBBB'] == 'false' or data['LBBB'] == 'true':
            lbbb = data['LBBB']
            qrs = float(data['QRS']) if data['QRS'] is not None else None
            if qrs is not None:
                value = LbbbTherapy().calc_fuzzy(lbbb, qrs)
                data['QRS'] = value[1]
                data['LBBB'] = value[0]
            if lbbb is not None and qrs is None:
                data['LBBB'] = LbbbTherapy().calc_fuzzy(lbbb, None)[0]
        else:
            print("LBBB musi byt true alebo false")
