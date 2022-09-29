from dataclasses import dataclass

@dataclass
class FSO_MSK_Indicator_desc:
    short_name: str
    unit: str
    zero_based: bool

@dataclass
class FSO_MSK_Indicators_Definition:
    VPCP: FSO_MSK_Indicator_desc = FSO_MSK_Indicator_desc('VPCP',
        '%',
        False)
    RS: FSO_MSK_Indicator_desc = FSO_MSK_Indicator_desc('RS',
        '%',
        False)
    SBR: FSO_MSK_Indicator_desc = FSO_MSK_Indicator_desc('SBR',
        '%',
        False)
    BUKBV: FSO_MSK_Indicator_desc = FSO_MSK_Indicator_desc('BUKBV',
        'měsíc',
        False)
    BUKBP: FSO_MSK_Indicator_desc = FSO_MSK_Indicator_desc('BUKBP',
        '%',
        False)
    KVBP: FSO_MSK_Indicator_desc = FSO_MSK_Indicator_desc('KVBP',
        'absolutní hodnota',
        True)
    CPBR: FSO_MSK_Indicator_desc = FSO_MSK_Indicator_desc('CPBR',
        'mil. Kč',
        False)
    URM: FSO_MSK_Indicator_desc = FSO_MSK_Indicator_desc('URM',
        '%',
        False)
    IA: FSO_MSK_Indicator_desc = FSO_MSK_Indicator_desc('IA',
        '%',
        False)
    KSKV: FSO_MSK_Indicator_desc = FSO_MSK_Indicator_desc('KSKV',
        '%',
        False)
    SKR: FSO_MSK_Indicator_desc = FSO_MSK_Indicator_desc('SKR',
        'mil. Kč',
        True)
    KPIT: FSO_MSK_Indicator_desc = FSO_MSK_Indicator_desc('KPIT',
        '%',
        False)
    KVSBR: FSO_MSK_Indicator_desc = FSO_MSK_Indicator_desc('KVSBR',
        'roky',
        False)
    CDSBR: FSO_MSK_Indicator_desc = FSO_MSK_Indicator_desc('CDSBR',
        'roky',
        True)
    DSSBR: FSO_MSK_Indicator_desc = FSO_MSK_Indicator_desc('DSSBR',
        '%',
        True)
    PUSBR: FSO_MSK_Indicator_desc = FSO_MSK_Indicator_desc('PUSBR',
        '%',
        True)
    DSC: FSO_MSK_Indicator_desc = FSO_MSK_Indicator_desc('DSC',
        '%',
        True)
    KDS: FSO_MSK_Indicator_desc = FSO_MSK_Indicator_desc('KDS',
        'index',
        False)
    CZCA: FSO_MSK_Indicator_desc = FSO_MSK_Indicator_desc('CZCA',
        '%',
        True)
    CZCA1: FSO_MSK_Indicator_desc = FSO_MSK_Indicator_desc('CZCA1',
        '%',
        True)
    CL: FSO_MSK_Indicator_desc = FSO_MSK_Indicator_desc('CL',
        '',
        False)
    OL: FSO_MSK_Indicator_desc = FSO_MSK_Indicator_desc('OL',
        '',
        False)
    FZ: FSO_MSK_Indicator_desc = FSO_MSK_Indicator_desc('FZ',
        '',
        False)

