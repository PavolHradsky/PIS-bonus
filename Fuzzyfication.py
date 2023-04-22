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
            elif bp == 'very high':
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
            0, 2, chest_pain, 0, 1, 2, 2.01, "Bolest v hrudi")
        return obtain_trapezoid_fuzzy_value(chest_pain, [0, 1, 2, 2.01])


class VericiguatTherapy:

    def __init__(self):
        pass

    def calc_fuzzy(self, uziva_vericiguat, stk=None, gfr=None, symptomaticka_hypotenzia=None):

        if uziva_vericiguat == '0' or uziva_vericiguat == '1':
            uziva_vericiguat = int(uziva_vericiguat)

        if uziva_vericiguat == "true":
            uziva_vericiguat = 1
        elif uziva_vericiguat == "false":
            uziva_vericiguat = 0

        if symptomaticka_hypotenzia == "true":
            symptomaticka_hypotenzia = 1
        elif symptomaticka_hypotenzia == "false":
            symptomaticka_hypotenzia = 0

        if uziva_vericiguat == 0 and stk is not None and stk < 100:
            print("uziva_vericiguat == 0 and stk is not None and stk < 100")
            return uziva_vericiguat, 0
        elif uziva_vericiguat == 0 and gfr is not None and gfr < 15:
            print("uziva_vericiguat == 0 and gfr is not None and gfr < 15")
            return uziva_vericiguat, 1
        elif uziva_vericiguat == 1 and stk is not None and stk < 90:
            print("uziva_vericiguat == 1 and stk is not None and stk < 90")
            return uziva_vericiguat, 1
        elif uziva_vericiguat == 1 and gfr is not None and gfr < 15:
            print("uziva_vericiguat == 1 and gfr is not None and gfr < 15")
            return uziva_vericiguat, 1
        elif uziva_vericiguat == 1 and symptomaticka_hypotenzia == 1:
            print("uziva_vericiguat == 1 and symptomaticka_hypotenzia == 1")
            return uziva_vericiguat, 1
        elif uziva_vericiguat == 0 and stk is None and gfr is None and symptomaticka_hypotenzia is None:
            return 0
        else:
            print("neexistujuce pravidlo")
            return None


class IvabradineTherapy:

    def __init__(self):
        pass

    def calc_fuzzy(self, uziva_ivabradin, fibrilacia_predsieni=None, sf=None, vek=None, symptomaticka_bradykardia=None, gfr=None):

        if uziva_ivabradin == '0' or uziva_ivabradin == '1':
            uziva_ivabradin = int(uziva_ivabradin)

        if uziva_ivabradin == "true":
            uziva_ivabradin = 1
        elif uziva_ivabradin == "false":
            uziva_ivabradin = 0

        if fibrilacia_predsieni == "true":
            fibrilacia_predsieni = 1
        elif fibrilacia_predsieni == "false":
            fibrilacia_predsieni = 0

        if symptomaticka_bradykardia == "true":
            symptomaticka_bradykardia = 1
        elif symptomaticka_bradykardia == "false":
            symptomaticka_bradykardia = 0

        if uziva_ivabradin == 0 and gfr is not None and gfr < 15:
            print("uziva_ivabradin == 0 and gfr is not None and gfr < 15")
            return uziva_ivabradin, 0
        elif uziva_ivabradin == 0 and fibrilacia_predsieni is not None and fibrilacia_predsieni == 1:
            print("uziva_ivabradin == 0 and fibrilacia_predsieni == 1")
            return uziva_ivabradin, 0
        elif uziva_ivabradin == 0 and vek is not None and vek > 75:
            print("uziva_ivabradin == 0 and vek is not None and vek > 75")
            return uziva_ivabradin, 1
        elif uziva_ivabradin == 0 and gfr is None and fibrilacia_predsieni is None and vek is None and sf is None and symptomaticka_bradykardia is None:
            print("uziva_ivabradin == 0")
            return uziva_ivabradin
        elif uziva_ivabradin == 1 and sf is not None and sf < 50:
            print("uziva_ivabradin == 1 and sf is not None and sf < 50")
            return uziva_ivabradin, 1
        elif uziva_ivabradin == 1 and symptomaticka_bradykardia == 1:
            print("uziva_ivabradin == 1 and symptomaticka_bradykardia == 1")
            return uziva_ivabradin, 1
        else:
            print("neexistujuce pravidlo")
            return None


class DigoxinTherapy:
    def __init__(self):
        pass

    def calc_fuzzy(self, uziva_digoxin, pomaly_rytmus=None, av_blok=None, hodnota_digoxinu=None):

        if av_blok is not None and av_blok == "II" or av_blok == "III":
            av_blok = 1
        else:
            av_blok = 0

        if uziva_digoxin == '0' or uziva_digoxin == '1':
            uziva_digoxin = int(uziva_digoxin)

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
            return uziva_digoxin, pomaly_rytmus
        elif uziva_digoxin == 0 and av_blok is not None and av_blok == 1:
            print("uziva_digoxin == 0 and av_blok == 1")
            return uziva_digoxin, av_blok
        elif uziva_digoxin == 1 and pomaly_rytmus is not None and pomaly_rytmus == 1:
            print("uziva_digoxin == 1 and pomaly_rytmus == 1")
            return uziva_digoxin, pomaly_rytmus
        elif uziva_digoxin == 1 and av_blok is not None and av_blok == 1:
            print("uziva_digoxin == 1 and av_blok == 1")
            return uziva_digoxin,  av_blok
        elif uziva_digoxin == 1 and hodnota_digoxinu is not None and hodnota_digoxinu > 1.05:
            print("uziva_digoxin == 1 and hodnota_digoxinu > 1.05")
            return uziva_digoxin,  1
        else:
            print("neexistuje pravidlo")
            return None


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

    age_value = data['Vek'] if 'Vek' in data else None
    sex_value = data['Pohlavie'] if 'Pohlavie' in data else None
    height_value = data['Vyska'] if 'Vyska' in data else None
    weight_value = data['Vaha'] if 'Vaha' in data else None
    st_bp_value = data['Systolicky krvny tlak'] if 'Systolicky krvny tlak' in data else None
    dt_bp_value = data['Diastolicky krvny tlak'] if 'Diastolicky krvny tlak' in data else None
    sugar_value = data['Hladina cukru'] if 'Hladina cukru' in data else None
    cholesterol_value = data['Cholesterol'] if 'Cholesterol' in data else None
    heart_rate_value = data['Tep'] if 'Tep' in data else None
    ekg_value = data['EKG'] if 'EKG' in data else None
    chest_pain_value = data['Bolest v hrudi'] if 'Bolest v hrudi' in data else None
    age, sex, height, weight, st_bp, dt_bp, sugar, cholesterol, heart_rate, ekg, chest_pain = None, None, None, None, None, None, None, None, None, None, None

    # check if data has string value instead of number
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
        if isinstance(st_bp_value, str) and (st_bp_value == 'low' or st_bp_value == 'medium' or st_bp_value == 'high' or st_bp_value == 'very high'):
            st_bp = round(st_bp_class.calc_fuzzy(st_bp_value), 2)
        else:
            st_bp = round(st_bp_class.calc_fuzzy(int(st_bp_value)), 2)

    if dt_bp_value is not None:
        if isinstance(dt_bp_value, str) and (dt_bp_value == 'low' or dt_bp_value == 'medium' or dt_bp_value == 'high' or dt_bp_value == 'very high'):
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
        print("V petri sieti sa nenachadza ziadna nami riesenych premennych")
        return None
    else:
        data['Vek'] = age
        data['Pohlavie'] = sex
        data['Vyska'] = height
        data['Vaha'] = weight
        data['Systolicky krvny tlak'] = st_bp
        data['Diastolicky krvny tlak'] = dt_bp
        data['Hladina cukru'] = sugar
        data['Cholesterol'] = cholesterol
        data['Tep'] = heart_rate
        data['EKG'] = ekg
        data['Bolest v hrudi'] = chest_pain


class LbbbTherapy:
    def __init__(self):
        pass

    def calc_fuzzy(self, lbbb, qrs, nyha):
        if lbbb == "true":
            lbbb = 1
        elif lbbb == "false":
            lbbb = 0
        else:
            print("Nespravny format hodnoty lbbb")

        if nyha is not None and (isinstance(nyha, str)):
            if nyha == "true":
                nyha = 1
            elif nyha == "false":
                nyha = 0
        else:
            print("Nespravny format hodnoty nyha")

        if qrs is not None and (isinstance(qrs, int) or isinstance(qrs, float)):
            if qrs >= 150:
                qrs = 1
            elif qrs >= 130 and qrs <= 149:
                qrs = 0
        else:
            print("Nespravny format hodnoty qrs")

        if lbbb == 1 and qrs == 1 and nyha == 1:
            return lbbb, qrs, nyha
        elif lbbb == 1 and qrs == 0 and nyha == 1:
            return lbbb, qrs, nyha
        elif lbbb == 0 and qrs == 1 and nyha == 1:
            return lbbb, qrs, nyha
        elif lbbb == 0 and qrs == 0 and nyha == 1:
            return lbbb, qrs, nyha
        else:
            print("Nezname pravidlo")
            return None


def get_final_result_logical(data, net):
    keys_array = [key for key in data.keys()]
    if 'LBBB' in keys_array:
        if data['LBBB'] == 'false' or data['LBBB'] == 'true':
            LBBB = data['LBBB']
            qrs = int(data['QRS']) if 'QRS' in keys_array else None
            nyha = data['NYHA-II-III'] if 'NYHA-II-III' in keys_array else None
            if qrs is not None and nyha is not None:
                value = LbbbTherapy().calc_fuzzy(LBBB, qrs, nyha)
                if value is not None:
                    data['LBBB'] = value[0]
                    data['QRS'] = value[1]
                    data['NYHA-II-III'] = value[2]
                else:
                    data['LBBB'] = None
                    data['QRS'] = None
                    data['NYHA-II-III'] = None
                    return None
            else:
                print("Nezname pravidlo")
                for key, value in data.items():
                    data[key] = None
                return None
        else:
            print("Nespravny format hodnoty LBBB")
            for key, value in data.items():
                data[key] = None
            return None

    if 'NYHA-II-III' in keys_array and len(keys_array) == 1:
        if (data['NYHA-II-III'] == 'false' or data['NYHA-II-III'] == 'true') and 'LBBB' not in keys_array and 'QRS' not in keys_array:
            data['NYHA-II-III'] = 1 if data['NYHA-II-III'] == 'true' else 0
        else:
            for key, value in data.items():
                data[key] = None
            return None

    if 'Uzivany gliflozin' in keys_array:
        if (data['Uzivany gliflozin'] == 'false' or data['Uzivany gliflozin'] == 0) and 'GFR' in keys_array:
            gfr = int(data['GFR']) if 'GFR' in keys_array else None
            if data['Uzivany gliflozin'] == 'false':
                data['Uzivany gliflozin'] = 0
            if gfr < 20:
                data['GFR'] = 0
            elif gfr >= 20 and gfr <= 25:
                data['GFR'] = 1
            elif gfr > 25:
                data['GFR'] = 1
            else:
                print("Nespravny format hodnoty gfr")
        elif (data['Uzivany gliflozin'] == 'false' or data['Uzivany gliflozin'] == '0') and 'sTK' in keys_array:
            data['Uzivany gliflozin'] = 0
            stk = int(data['sTK']) if 'sTK' in keys_array else None
            if stk < 90:
                data['sTK'] = 0
            else:
                print("Nespravny format hodnoty sTK")

        elif (data['Uzivany gliflozin'] == 'false' or data['Uzivany gliflozin'] == '0') and 'symptomaticka hypotenzia' in keys_array:
            if data['Uzivany gliflozin'] == 'false':
                data['Uzivany gliflozin'] = 0
            if data['symptomaticka hypotenzia'] == 'true':
                data['symptomaticka hypotenzia'] = 0
            elif data['symptomaticka hypotenzia'] == 'false':
                data['symptomaticka hypotenzia'] = 1
            else:
                print("Nespravny format hodnoty symptomaticka hypotenzia")

        elif (data['Uzivany gliflozin'] == 'dapa' or data['Uzivany gliflozin'] == 'empa') and 'GFR' in keys_array:
            gfr = int(data['GFR'])
            if gfr < 20 and (data['Uzivany gliflozin'] == 'dapa' or data['Uzivany gliflozin'] == 'empa'):
                data['Uzivany gliflozin'] = 0
                data['GFR'] = 0
            elif gfr >= 20 and gfr <= 25 and data['Uzivany gliflozin'] == 'empa':
                print(gfr)
                data['Uzivany gliflozin'] = 1
                data['GFR'] = 1
            elif gfr >= 20 and gfr <= 25 and data['Uzivany gliflozin'] == 'dapa':
                data['Uzivany gliflozin'] = 0
                data['GFR'] = 1
            elif gfr > 25 and (data['Uzivany gliflozin'] == 'dapa' or data['Uzivany gliflozin'] == 'empa'):
                data['Uzivany gliflozin'] = 1
                data['GFR'] = 1
            else:
                print("Nespravny format hodnoty GFR")
        elif (data['Uzivany gliflozin'] == 'true' or data['Uzivany gliflozin'] == '1') and 'Max davka' in keys_array:
            data['Uzivany gliflozin'] = 1
            if data['Max davka'] == 'true':
                data['Max davka'] = 1
        else:
            for key, value in data.items():
                data[key] = None
            print("Nezname pravidlo")

    if 'BB' in keys_array:
        if (data['BB'] == 'false' or data['BB'] == '0') and 'TEP' in keys_array:

            if data['BB'] == 'false':
                data['BB'] = 0
            if int(data['TEP']) < 50:
                data['TEP'] = 0
            else:
                print("Nespravny format hodnoty TEP")
        if (data['BB'] == 'false' or data['BB'] == '0') and 'sTK' in keys_array:
            if data['BB'] == 'false':
                data['BB'] = 0
            if int(data['sTK']) < 90:
                data['sTK'] = 0
            else:
                print("Nespravny format hodnoty sTK")
        if (data['BB'] == 'false' or data['BB'] == '0') and 'CHOCHP' in keys_array:
            if data['BB'] == 'false':
                data['BB'] = 0
            if data['CHOCHP'] == 'true':
                data['CHOCHP'] = 0
            elif data['CHOCHP'] == 'false':
                data['CHOCHP'] = 1
            else:
                print("Nespravny format hodnoty CHOCHP")
        if (data['BB'] == 'false' or data['BB'] == '0') and 'AV blok' in keys_array:
            if data['BB'] == 'false':
                data['BB'] = 0
            if data['AV blok'] == 'true':
                data['AV blok'] = 0
            elif data['AV blok'] == 'false':
                data['AV blok'] = 1
            else:
                print("Nespravny format hodnoty AV blok")
        if (data['BB'] == 'false' or data['BB'] == '0') and 'Kreatinin' in keys_array:
            if data['BB'] == 'false':
                data['BB'] = 0
            if int(data['Kreatinin']) > 250:
                data['Kreatinin'] = 1
            else:
                print("Nespravny format hodnoty Kreatinin")

        if (data['BB'] == 'true' or data['BB'] == '1') and 'TEP' in keys_array:
            if data['BB'] == 'true':
                data['BB'] = 1
            if int(data['TEP']) < 50:
                data['TEP'] = 0
            else:
                print("Nespravny format hodnoty TEP")
        if (data['BB'] == 'true' or data['BB'] == '1') and "symptomaticka hypotenzia" in keys_array:
            if data['BB'] == 'true':
                data['BB'] = 1
            if data["symptomaticka hypotenzia"] == 'true':
                data["symptomaticka hypotenzia"] = 0
            elif data["symptomaticka hypotenzia"] == 'false':
                data["symptomaticka hypotenzia"] = 1
            else:
                print("Nespravny format hodnoty symptomaticka hypotenzia")

        if (data['BB'] == 'true' or data['BB'] == '1') and 'Kreatinin' in keys_array and 'Nebivolol' in keys_array:
            if data['BB'] == 'true':
                data['BB'] = 1
            if data["Nebivolol"] == 'true' and int(data['Kreatinin']) > 250:
                data["Nebivolol"] = 1
                data['Kreatinin'] = 1
            else:
                print("Nespravny format hodnoty Nebivolol")
        if (data['BB'] == 'true' or data['BB'] == '1') and 'AV blok' in keys_array:
            if data['BB'] == 'true':
                data['BB'] = 1
            if data['AV blok'] == 'true':
                data['AV blok'] = 0
            else:
                print("Nespravny format hodnoty AV blok")
        if (data['BB'] == 'true' or data['BB'] == '1') and 'Max davka' in keys_array:
            if data['BB'] == 'true':
                data['BB'] = 1
            if data['Max davka'] == "true":
                data['Max davka'] = 0
            elif data['Max davka'] == "false":
                data['Max davka'] = 1
            else:
                print("Nespravny format hodnoty Max davka")

    if 'ARNI' in keys_array:
        if (data['ARNI'] == 'false' or data['ARNI'] == '0') and 'GFR' in keys_array:
            if data['ARNI'] == 'false':
                data['ARNI'] = 0
            if int(data['GFR']) < 30:
                data['GFR'] = 0
            if int(data['GFR']) > 30 and int(data['GFR']) < 60:
                data['GFR'] = 1
            else:
                print("Nespravny format hodnoty GFR")
        if (data['ARNI'] == 'false' or data['ARNI'] == '0') and 'sTK' in keys_array:
            if data['ARNI'] == 'false':
                data['ARNI'] = 0
            if int(data['sTK']) < 90:
                data['sTK'] = 0
            if int(data['sTK']) > 90 and int(data['sTK']) < 110:
                data['sTK'] = 1
            else:
                print("Nespravny format hodnoty sTK")
        if (data['ARNI'] == 'false' or data['ARNI'] == '0') and 'K+' in keys_array:
            if data['ARNI'] == 'false':
                data['ARNI'] = 0
            if int(data['K+']) > 5:
                data['K+'] = 0
            else:
                print("Nespravny format hodnoty K+")
        if (data['ARNI'] == 'false' or data['ARNI'] == '0') and "symptomaticka hypotenzia" in keys_array:
            if data['ARNI'] == 'false':
                data['ARNI'] = 0
            if data["symptomaticka hypotenzia"] == 'true':
                data["symptomaticka hypotenzia"] = 0
            elif data["symptomaticka hypotenzia"] == 'false':
                data["symptomaticka hypotenzia"] = 1
            else:
                print("Nespravny format hodnoty symptomaticka hypotenzia")
        if (data['ARNI'] == 'true' or data['ARNI'] == '1') and 'GFR' in keys_array:
            if data['ARNI'] == 'true':
                data['ARNI'] = 1
            if int(data['GFR']) < 30:
                data['GFR'] = 1
            else:
                print("Nespravny format hodnoty gfr")
        if (data['ARNI'] == 'true' or data['ARNI'] == '1') and "symptomaticka hypotenzia" in keys_array:
            if data['ARNI'] == 'true':
                data['ARNI'] = 1
            if data["symptomaticka hypotenzia"] == 'true':
                data["symptomaticka hypotenzia"] = 1
            else:
                print("Nespravny format hodnoty symptomaticka hypotenzia")
        if (data['ARNI'] == 'true' or data['ARNI'] == '1') and 'K+' in keys_array:
            if data['ARNI'] == 'true':
                data['ARNI'] = 1
            if float(data['K+']) > 5.5:
                data['K+'] = 1
            else:
                print("Nespravny format hodnoty K+")
        if (data['ARNI'] == 'true' or data['ARNI'] == '1') and 'Max davka' in keys_array:
            if data['ARNI'] == 'true':
                data['ARNI'] = 1
            if data['Max davka'] == "true":
                data['Max davka'] = 0
            elif data['Max davka'] == "false":
                data['Max davka'] = 1
            else:
                print("Nespravny format hodnoty Max davka")
        else:
            print("Neexitujuce pravidlo pre ARNI")

    if 'ACEI' in keys_array:
        if (data['ACEI'] == 'false' or data['ACEI'] == '0') and 'K+' in keys_array:
            if data['ACEI'] == 'false':
                data['ACEI'] = 0
            if int(data['K+']) > 5:
                data['K+'] = 0
            else:
                data['ACEI'] = None
                data['K+'] = None
                print("Nespravny format hodnoty K+")
        elif (data['ACEI'] == 'false' or data['ACEI'] == '0') and 'sTK' in keys_array:
            if data['ACEI'] == 'false':
                data['ACEI'] = 0
            if int(data['sTK']) < 90:
                data['sTK'] = 0
            else:
                data['ACEI'] = None
                data['sTK'] = None
                print("Nespravny format hodnoty sTK")
        elif (data['ACEI'] == 'false' or data['ACEI'] == '0') and 'GFR' in keys_array:
            if data['ACEI'] == 'false':
                data['ACEI'] = 0
            if int(data['GFR']) < 30:
                data['GFR'] = 0
            else:
                data['ACEI'] = None
                data['GFR'] = None
                print("Nespravne pravidlo")

        elif (data['ACEI'] == 'true' or data['ACEI'] == '1') and 'K+' in keys_array:
            if data['ACEI'] == 'true':
                data['ACEI'] = 1
            if float(data['K+']) > 5.5:
                data['K+'] = 1
            else:
                data['ACEI'] = None
                data['K+'] = None
                print("Nespravne pravidlo")
        elif (data['ACEI'] == 'true' or data['ACEI'] == '1') and "symptomaticka hypotenzia" in keys_array:
            if data['ACEI'] == 'true':
                data['ACEI'] = 1
            if data["symptomaticka hypotenzia"] == 'true':
                data["symptomaticka hypotenzia"] = 1
            else:
                data['ACEI'] = None
                data["symptomaticka hypotenzia"] = None
                print("Nespravne pravidlo")
        elif (data['ACEI'] == 'true' or data['ACEI'] == '1') and 'GFR' in keys_array:
            if data['ACEI'] == 'true':
                data['ACEI'] = 1
            if float(data['GFR']) < 20:
                data['GFR'] = 1
            else:
                data['ACEI'] = None
                data['GFR'] = None
                print("Nespravne pravidlo")
        elif (data['ACEI'] == 'true' or data['ACEI'] == '1') and 'Max davka' in keys_array:
            if data['ACEI'] == 'true':
                data['ACEI'] = 1
            if data['Max davka'] == "true":
                data['Max davka'] = 0
            elif data['Max davka'] == "false":
                data['Max davka'] = 1
            else:
                data['ACEI'] = None
                data['Max davka'] = None
                print("Nespravne pravidlo")
        else:
            for key, value in data.items():
                data[key] = None
            print("Nezname pravidlo")

    if "MRA" in [place.label for place in net.getPlaces()]:

        if 'Max davka' in keys_array and "K+" in keys_array:
            k_value = float(str(data['K+']).replace(",", "."))
            if data['Max davka'] == "false":
                data['Max davka'] = 1
            else:
                data['Max davka'] = None
                print("Nespravny format hodnoty Max davka")
            if k_value < 5:
                data['K+'] = 1
            if k_value > 5.5 and k_value < 6:
                data['K+'] = 1
            else:
                data['K+'] = None
                print("Nespravny format hodnoty K+")
        elif 'K+' in keys_array and "Max davka" not in keys_array:
            k_value = float(str(data['K+']).replace(",", "."))
            if k_value > 5.0 and k_value < 5.5:
                data['K+'] = 0
            elif k_value > 6.0:
                data['K+'] = 1
            else:
                data['K+'] = None
                print("Nespravny format hodnoty K+")
        elif 'K+' in keys_array and "Max davka" in keys_array and "GFR" not in keys_array:
            k_value = float(str(data['K+']).replace(",", "."))
            if data['Max davka'] == "false":
                data['Max davka'] = 1
            if k_value > 5.5 and k_value < 6:
                data['K+'] = 1
            else:
                data['K+'] = None
                print("Nespravny format hodnoty K+")
        elif 'K+' not in keys_array and "Max davka" in keys_array and "GFR" in keys_array:
            if float(data['GFR']) < 30:
                data['GFR'] = 1
            if data['Max davka'] == "false":
                data['Max davka'] = 1
            else:
                data['Max davka'] = None
                data['GFR'] = None
                print("Nespravny format hodnoty GFR")
        elif 'GFR' in keys_array and "Max davka" not in keys_array and "K+" not in keys_array:
            if float(data['GFR']) < 20:
                data['GFR'] = 1
            else:
                data['GFR'] = None
                print("Nespravny format hodnoty GFR")
        elif 'GFR' not in keys_array and "Max davka" in keys_array and "K+" not in keys_array:
            if data['Max davka'] == "true":
                data['Max davka'] = 0
            else:
                data['Max davka'] = None
                print("Nespravny format hodnoty Max davka")
        else:
            for key, value in data.items():
                data[key] = None
            print("Neexitujuce pravidlo pre MRA")

    if 'Uziva vericiguat' in keys_array:

        if data['Uziva vericiguat'] == 'false' or data['Uziva vericiguat'] == 'true' or data['Uziva vericiguat'] == '0' or data['Uziva vericiguat'] == '1':

            vericiguat = data['Uziva vericiguat']
            sTK = float(data['sTK']) if 'sTK' in keys_array else None
            GFR = float(data['GFR']) if 'GFR' in keys_array else None
            symptomaticka_hypotenzia = data['symptomaticka hypotenzia'] if 'symptomaticka hypotenzia' in keys_array else None
            if sTK is not None:
                value = VericiguatTherapy().calc_fuzzy(
                    vericiguat, sTK, GFR, symptomaticka_hypotenzia)
                if value is not None:
                    data['sTK'] = value[1]
                    data['Uziva vericiguat'] = value[0]
                else:
                    data['Uziva vericiguat'] = None
                    data['sTK'] = None
            elif GFR is not None:
                value = VericiguatTherapy().calc_fuzzy(
                    vericiguat, sTK, GFR, symptomaticka_hypotenzia)
                if value is not None:
                    data['GFR'] = value[1]
                    data['Uziva vericiguat'] = value[0]
                else:
                    data['Uziva vericiguat'] = None
                    data['GFR'] = None
            elif symptomaticka_hypotenzia is not None:
                value = VericiguatTherapy().calc_fuzzy(
                    vericiguat, sTK, GFR, symptomaticka_hypotenzia)
                if value is not None:
                    data['symptomaticka hypotenzia'] = value[1]
                    data['Uziva vericiguat'] = value[0]
                else:
                    data['Uziva vericiguat'] = None
                    data['symptomaticka hypotenzia'] = None
            elif vericiguat is not None and sTK is None and GFR is None and symptomaticka_hypotenzia is None:
                data['Uziva vericiguat'] = VericiguatTherapy().calc_fuzzy(
                    vericiguat, None, None, None)
            else:
                for key, value in data.items():
                    data[key] = None
                print("Nezname pravidlo")
        else:
            for key, value in data.items():
                data[key] = None
            print("Uziva vericiguat musi byt true alebo false")

    if 'Uziva ivabradin' in keys_array:
        if data['Uziva ivabradin'] == 'false' or data['Uziva ivabradin'] == 'true' or data['Uziva ivabradin'] == '0' or data['Uziva ivabradin'] == '1':
            ivabradin = data['Uziva ivabradin']
            fibrilacia_predsieni = data['fibrilacia predsieni'] if 'fibrilacia predsieni' in keys_array else None
            sf = float(data['SF']) if 'SF' in keys_array else None
            vek = int(data['vek']) if 'vek' in keys_array else None
            gfr = float(data['GFR']) if 'GFR' in keys_array else None
            symptomaticka_bradykardia = data['symptomaticka bradykardia'] if 'symptomaticka bradykardia' in keys_array else None
            if fibrilacia_predsieni is not None:
                value = IvabradineTherapy().calc_fuzzy(ivabradin, fibrilacia_predsieni,
                                                       sf, vek, symptomaticka_bradykardia, gfr)
                if value is not None:
                    data['fibrilacia predsieni'] = value[1]
                    data['Uziva ivabradin'] = value[0]
                else:
                    data['Uziva ivabradin'] = None
                    data['fibrilacia predsieni'] = None

            elif sf is not None:
                value = IvabradineTherapy().calc_fuzzy(ivabradin, fibrilacia_predsieni,
                                                       sf, vek, symptomaticka_bradykardia, gfr)
                if value is not None:
                    data['SF'] = value[1]
                    data['Uziva ivabradin'] = value[0]
                else:
                    data['Uziva ivabradin'] = None
                    data['SF'] = None
            elif vek is not None:
                value = IvabradineTherapy().calc_fuzzy(ivabradin, fibrilacia_predsieni,
                                                       sf, vek, symptomaticka_bradykardia, gfr)
                if value is not None:
                    data['vek'] = value[1]
                    data['Uziva ivabradin'] = value[0]
                else:
                    data['Uziva ivabradin'] = None
                    data['vek'] = None
            elif gfr is not None:
                value = IvabradineTherapy().calc_fuzzy(ivabradin, fibrilacia_predsieni,
                                                       sf, vek, symptomaticka_bradykardia, gfr)
                if value is not None:
                    data['GFR'] = value[1]
                    data['Uziva ivabradin'] = value[0]
                else:
                    data['Uziva ivabradin'] = None
                    data['GFR'] = None
            elif symptomaticka_bradykardia is not None:
                value = IvabradineTherapy().calc_fuzzy(ivabradin, fibrilacia_predsieni,
                                                       sf, vek, symptomaticka_bradykardia, gfr)
                if value is not None:
                    data['symptomaticka bradykardia'] = value[1]
                    data['Uziva ivabradin'] = value[0]
                else:
                    data['Uziva ivabradin'] = None
                    data['symptomaticka bradykardia'] = None
            elif ivabradin is not None and fibrilacia_predsieni is None and sf is None and vek is None and gfr is None and symptomaticka_bradykardia is None:
                data['Uziva ivabradin'] = IvabradineTherapy().calc_fuzzy(
                    ivabradin, None, None, None, None, None)
            else:
                for key, value in data.items():
                    data[key] = None
                print("Nezname pravidlo")
        else:
            for key, value in data.items():
                data[key] = None
            print("Uziva ivabradin musi byt true alebo false")

    if 'Uziva digoxin' in keys_array:
        if data['Uziva digoxin'] == 'false' or data['Uziva digoxin'] == 'true' or data['Uziva digoxin'] == '0' or data['Uziva digoxin'] == '1':
            digoxin = data['Uziva digoxin']
            pomaly_rytmus = data['Pomaly rytmus'] if 'Pomaly rytmus' in keys_array else None
            av = data['AV blok'] if 'AV blok' in keys_array else None
            di_val = float(data['Hodnota digoxinu'].replace(
                ',', '.')) if 'Hodnota digoxinu' in keys_array else None

            if pomaly_rytmus is not None:
                value = DigoxinTherapy().calc_fuzzy(digoxin,
                                                    pomaly_rytmus, av, di_val)
                if value is not None:
                    data['Pomaly rytmus'] = value[1]
                    data['Uziva digoxin'] = value[0]
                else:
                    data['Uziva digoxin'] = None
                    data['Pomaly rytmus'] = None
            elif av is not None:
                value = DigoxinTherapy().calc_fuzzy(digoxin,
                                                    pomaly_rytmus, av, di_val)
                if value is not None:
                    data['AV blok'] = value[1]
                    data['Uziva digoxin'] = value[0]
                else:
                    data['Uziva digoxin'] = None
                    data['AV blok'] = None
            elif di_val is not None:
                value = DigoxinTherapy().calc_fuzzy(digoxin,
                                                    pomaly_rytmus, av, di_val)
                if value is not None:
                    data['Hodnota digoxinu'] = value[1]
                    data['Uziva digoxin'] = value[0]
                else:
                    data['Uziva digoxin'] = None
                    data['Hodnota digoxinu'] = None
            else:
                for key, value in data.items():
                    data[key] = None
                print("Nezname pravidlo")
        else:
            for key, value in data.items():
                data[key] = None
            print("Uziva digoxin musi byt true alebo false")

    if 'Hodnota digoxinu' in keys_array and 'Uziva digoxin' not in keys_array:
        hodnota_digoxinu = float(str(data['Hodnota digoxinu']).replace(
            ',', '.')) if 'Hodnota digoxinu' in keys_array else None
        if hodnota_digoxinu < 0.64:
            print("uziva_digoxin == 1 and hodnota_digoxinu < 0.64")
            data['Hodnota digoxinu'] = 1
        elif hodnota_digoxinu >= 0.64 and hodnota_digoxinu <= 1.05:
            print(
                "uziva_digoxin == 1 and hodnota_digoxinu >= 0.64 and hodnota_digoxinu <= 1.05")
            data['Hodnota digoxinu'] = 0
        else:
            for key, value in data.items():
                data[key] = None
            print("Nezname pravidlo pre hodnotu digoxinu")

    if 'eGRF' in keys_array and len(keys_array) == 1:
        eGRF = int(data['eGRF'])
        if eGRF < 30:
            data['eGRF'] = 1
        else:
            for key, value in data.items():
                data[key] = None
            print("Nezname pravidlo pre eGRF")

    if 'K+' in keys_array and ("MRA" not in [place.label for place in net.getPlaces()] and "ACEI" not in [place.label for place in net.getPlaces()] and "ARNI" not in [place.label for place in net.getPlaces()]):
        K = int(data['K+'])
        if K > 5:
            data['K+'] = 0
        else:
            for key, value in data.items():
                data[key] = None
            print("Nezname pravidlo pre K+")

    if 'SBP' in keys_array and len(keys_array) == 1:
        SBP = int(data['SBP'])
        if SBP < 95:
            data['SBP'] = 0
        elif SBP > 95:
            data['SBP'] = 1
        else:
            for key, value in data.items():
                data[key] = None
            print("Nezname pravidlo pre SBP")

    if 'HR' in keys_array and len(keys_array) == 1:
        HR = int(data['HR'])
        if HR < 55:
            data['HR'] = 0
        else:
            for key, value in data.items():
                data[key] = None
            print("Nezname pravidlo pre HR")

    if 'Zvysenie NTproBNP' in keys_array and len(keys_array) == 1:
        Zvysenie_NTproBNP = int(data['Zvysenie NTproBNP'])
        if Zvysenie_NTproBNP > 10:
            data['Zvysenie NTproBNP'] = 1
        else:
            for key, value in data.items():
                data[key] = None
            print("Nezname pravidlo pre Zvysenie NTproBNP")
