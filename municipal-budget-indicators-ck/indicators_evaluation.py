from indicators_model import FSO_MSK_Indicators, FSO_MSK_Indicator
from decimal import Decimal

def eval_RS(obj: FSO_MSK_Indicator, rzd_value: Decimal):
    if obj.value >= Decimal('0.0'):
        obj.score = 'A'
    elif obj.value < Decimal('0.0') and rzd_value > Decimal('0.0'):
        obj.score = 'B'
    else:
        obj.score = 'C'

def eval_SBR(obj: FSO_MSK_Indicator):
    if obj.value >= Decimal('0.25'):
        obj.score = 'A'
    elif obj.value < Decimal('0.25') and obj.value >= Decimal('0.0'):
        obj.score = 'B'
    else:
        obj.score = 'C'

def eval_BUKBV(obj: FSO_MSK_Indicator):
    if obj.value >= Decimal('4.0'):
        obj.score = 'A'
    elif obj.value < Decimal('4.0') and obj.value >= Decimal('1.0'):
        obj.score = 'B'
    else:
        obj.score = 'C'

def eval_BUKBP(obj: FSO_MSK_Indicator):
    if obj.value >= Decimal('0.3'):
        obj.score = 'A'
    elif obj.value < Decimal('0.3') and obj.value >= Decimal('0.08'):
        obj.score = 'B'
    else:
        obj.score = 'C'

def eval_KVBP(obj: FSO_MSK_Indicator):
    if obj.value >= Decimal('0.0') and obj.value <= Decimal('1.0'):
        obj.score = 'A'
    elif obj.value <= Decimal('1.2') and obj.value > Decimal('1.0'):
        obj.score = 'B'
    elif obj.value > Decimal('1.2'):
        obj.score = 'C'
    else:
        obj.score = 'X'   # error in calculation

def eval_CPBR(obj: FSO_MSK_Indicator):
    if obj.value >= Decimal('0.0'):
        obj.score = 'A'
    else:
        obj.score = 'B'

def eval_VPCP(obj: FSO_MSK_Indicator):
    if obj.value >= Decimal('0.9'):
        obj.score = 'A'
    elif obj.value < Decimal('0.9') and obj.value >= Decimal('0.8'):
        obj.score = 'B'
    elif obj.value >= Decimal('0') and obj.value < Decimal('0.8'):
        obj.score = 'C'
    else:
        obj.score = 'X'   # error in calculation

def eval_URM(obj: FSO_MSK_Indicator):
    if obj.value <= Decimal('2.0') and obj.value >= Decimal('1.2'):
        obj.score = 'A'
    elif (obj.value < Decimal('1.2') and obj.value >= Decimal('1.0')) or (obj.value > Decimal('2.0')):
        obj.score = 'B'
    elif obj.value < Decimal('1.0') and obj.value > Decimal('0'):
        obj.score = 'C'
    else:
        obj.score = 'X'   # error in calculation

def eval_IA(obj: FSO_MSK_Indicator):
    if obj.value >= Decimal('0.2'):
        obj.score = 'A'
    elif obj.value < Decimal('0.2') and obj.value >= Decimal('0.1'):
        obj.score = 'B'
    elif obj.value < Decimal('0.1') and obj.value >= Decimal('0'):
        obj.score = 'C'
    else:
        obj.score = 'X'   # error in calculation

def eval_KSKV(obj: FSO_MSK_Indicator):
    if obj.value >= Decimal('0.98'):
        obj.score = 'A'
    elif obj.value < Decimal('0.98') and obj.value >= Decimal('0.75'):
        obj.score = 'B'
    elif obj.value < Decimal('0.75') and obj.value >= Decimal('0'):
        obj.score = 'C'
    else:
        obj.score = 'X'   # error in calculation

def eval_SKR(obj: FSO_MSK_Indicator):
    if obj.value >= Decimal('0'):
        obj.score = 'A'
    else:
        obj.score = 'B'

def eval_KPIT(obj: FSO_MSK_Indicator):
    if obj.value >= Decimal('0.5'):
        obj.score = 'A'
    elif obj.value < Decimal('0.5') and obj.value >= Decimal('0.25'):
        obj.score = 'B'
    elif obj.value < Decimal('0.25') and obj.value >= Decimal('0'):
        obj.score = 'C'
    else:
        obj.score = 'X'   # error in calculation


def eval_CDSBR(obj: FSO_MSK_Indicator):
    if obj.value <= Decimal('3.0') and obj.value > Decimal('0'):
        obj.score = 'A'
    elif obj.value > Decimal('3.0') and obj.value <= Decimal('6.0'):
        obj.score = 'B'
    elif obj.value > Decimal('6.0'):
        obj.score = 'C'
    else:
        obj.score = 'X'  # error in calculation

def eval_DSSBR(obj: FSO_MSK_Indicator):
    if obj.value <= Decimal('0.4') and obj.value >= Decimal('0.0'):
        obj.score = 'A'
    elif obj.value > Decimal('0.4') and obj.value <= Decimal('0.8'):
        obj.score = 'B'
    elif obj.value > Decimal('0.8'):
        obj.score = 'C'
    else:
        obj.score = 'X'  # error in calculation

def eval_PUSBR(obj: FSO_MSK_Indicator):
    if obj.value <= Decimal('0.04') and obj.value >= Decimal('0'):
        obj.score = 'A'
    elif obj.value <= Decimal('0.08') and obj.value > Decimal('0.04'):
        obj.score = 'B'
    elif obj.value > Decimal('0.08'):
        obj.score = 'C'
    else:
        obj.score = 'X'  # error in calculation

def eval_KDS(obj: FSO_MSK_Indicator):
    if obj.value >= Decimal('1.2'):
        obj.score = 'A'
    elif obj.value < Decimal('1.2') and obj.value >= Decimal('1.0'):
        obj.score = 'B'
    elif obj.value < Decimal('1.0') and obj.value >= Decimal('0'):
        obj.score = 'C'
    else:
        obj.score = 'X'   # error in calculation


def eval_CZCA(obj: FSO_MSK_Indicator):
    if obj.value >= Decimal('0.0') and obj.value < Decimal('0.1'):
        obj.score = 'A'
    elif obj.value >= Decimal('0.1') and obj.value < Decimal('0.25'):
        obj.score = 'B'
    elif obj.value >= Decimal('0.25'):
        obj.score = 'C'
    else:
        obj.score = 'X'  # error in calculation

def eval_CZCA1(obj: FSO_MSK_Indicator):
    if obj.value >= Decimal('0.0') and obj.value < Decimal('0.1'):
        obj.score = 'A'
    elif obj.value >= Decimal('0.1') and obj.value < Decimal('0.25'):
        obj.score = 'B'
    elif obj.value >= Decimal('0.25'):
        obj.score = 'C'
    else:
        obj.score = 'X'  # error in calculation

def eval_DSC(obj: FSO_MSK_Indicator):
    if obj.value <= Decimal('0.2') and obj.value >= Decimal('0.0'):
        obj.score = 'A'
    elif obj.value > Decimal('0.2') and obj.value <= Decimal('0.3'):
        obj.score = 'B'
    elif obj.value > Decimal('0.3'):
        obj.score = 'C'
    else:
        obj.score = 'X'    # error in calculation

def eval_CL(obj: FSO_MSK_Indicator):
    if obj.value <= Decimal('1.0'):
        obj.score = 'C'
    elif obj.value > Decimal('1.0') and obj.value <= Decimal('5.0'):
        obj.score = 'B'
    else:
        obj.score = 'A'

def eval_OL(obj: FSO_MSK_Indicator):
    if obj.value <= Decimal('1.0'):
        obj.score = 'C'
    elif obj.value > Decimal('1.0') and obj.value <= Decimal('1.75'):
        obj.score = 'B'
    else:
        obj.score = 'A'

def eval_FZ(obj: FSO_MSK_Indicator):
    if obj.value <= Decimal('0.05'):
        obj.score = 'C'
    elif obj.value > Decimal('0.05') and obj.value <= Decimal('0.5'):
        obj.score = 'B'
    else:
        obj.score = 'A'