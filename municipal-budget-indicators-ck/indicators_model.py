from dataclasses import dataclass
from decimal import Decimal
from datetime import date

@dataclass
class FSO_MSK_Indicator:
    value: Decimal
    score: str = '-'
 
@dataclass
class FSO_MSK_Indicators:
    RS: FSO_MSK_Indicator
    SBR: FSO_MSK_Indicator
    BUKBV: FSO_MSK_Indicator
    BUKBP: FSO_MSK_Indicator
    KVBP: FSO_MSK_Indicator
    VPCP: FSO_MSK_Indicator
    CPBR: FSO_MSK_Indicator
    URM: FSO_MSK_Indicator
    IA: FSO_MSK_Indicator
    KSKV: FSO_MSK_Indicator
    SKR: FSO_MSK_Indicator
    KPIT: FSO_MSK_Indicator
    KVSBR: FSO_MSK_Indicator
    CDSBR: FSO_MSK_Indicator
    DSSBR: FSO_MSK_Indicator
    PUSBR: FSO_MSK_Indicator
    DSC: FSO_MSK_Indicator
    KDS: FSO_MSK_Indicator
    CZCA: FSO_MSK_Indicator
    CZCA1: FSO_MSK_Indicator
    CL: FSO_MSK_Indicator
    OL: FSO_MSK_Indicator
    FZ: FSO_MSK_Indicator
    # helpers
    # rozdil deficitu a zustatku / musi byt kladny
    RS_RZD: Decimal
    # identification
    year: int = date.today().year-1
    organization_id: str ='00261220'
