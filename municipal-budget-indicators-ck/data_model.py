from dataclasses import dataclass
from datetime import date, datetime
from decimal import Decimal

@dataclass
class Year_Input_Data:
    # global
    fin_4010: Decimal = Decimal('0.0')
    fin_4020: Decimal = Decimal('0.0')
    fin_4030: Decimal = Decimal('0.0')
    fin_4040: Decimal = Decimal('0.0')
    fin_4060: Decimal = Decimal('0.0')
    fin_4210: Decimal = Decimal('0.0')
    fin_4220: Decimal = Decimal('0.0')
    fin_4250: Decimal = Decimal('0.0')
    fin_4200: Decimal = Decimal('0.0')
    fin_4430: Decimal = Decimal('0.0')
    fin_5141: Decimal = Decimal('0.0')
    fin_4470: Decimal = Decimal('0.0')
    # transfer
    fin_4111: Decimal = Decimal('0.0')
    fin_4112: Decimal = Decimal('0.0')
    fin_4113: Decimal = Decimal('0.0')  # https://fsm-msk.cms.opf.slu.cz/index.php/analytici/data-import-msk-indikatory/details/16/3092
    fin_4116: Decimal = Decimal('0.0')
    fin_4119: Decimal = Decimal('0.0')
    fin_4121: Decimal = Decimal('0.0')
    fin_4122: Decimal = Decimal('0.0')
    fin_4123: Decimal = Decimal('0.0')
    fin_4129: Decimal = Decimal('0.0')
    fin_4151: Decimal = Decimal('0.0')
    fin_4152: Decimal = Decimal('0.0')
    fin_4153: Decimal = Decimal('0.0')
    fin_4155: Decimal = Decimal('0.0')
    fin_4156: Decimal = Decimal('0.0')
    fin_4159: Decimal = Decimal('0.0')
    fin_4160: Decimal = Decimal('0.0')
    # inv prijmy
    fin_4211: Decimal = Decimal('0.0')
    fin_4212: Decimal = Decimal('0.0')
    fin_4213: Decimal = Decimal('0.0')
    fin_4214: Decimal = Decimal('0.0')
    fin_4216: Decimal = Decimal('0.0')
    fin_4218: Decimal = Decimal('0.0')
    fin_4219: Decimal = Decimal('0.0')
    fin_4221: Decimal = Decimal('0.0')
    fin_4222: Decimal = Decimal('0.0')
    fin_4229: Decimal = Decimal('0.0')
    fin_4231: Decimal = Decimal('0.0')
    fin_4232: Decimal = Decimal('0.0')
    fin_4233: Decimal = Decimal('0.0')
    fin_4234: Decimal = Decimal('0.0')
    fin_4235: Decimal = Decimal('0.0')
    # vydaje
    fin_5178: Decimal = Decimal('0.0')
    fin_6143: Decimal = Decimal('0.0')
    # own transfers
    fin_5342: Decimal = Decimal('0.0')
    fin_5344: Decimal = Decimal('0.0')
    fin_5345: Decimal = Decimal('0.0')
    fin_5347: Decimal = Decimal('0.0')
    fin_5348: Decimal = Decimal('0.0')
    fin_5349: Decimal = Decimal('0.0')
    # financing
    fin_8122: Decimal = Decimal('0.0')
    fin_8124: Decimal = Decimal('0.0')
    fin_8xx2: Decimal = Decimal('0.0')
    fin_8x14: Decimal = Decimal('0.0')
    fin_8x13: Decimal = Decimal('0.0')
    fin_8x24: Decimal = Decimal('0.0')
    fin_8x23: Decimal = Decimal('0.0')
    fin_8xx4: Decimal = Decimal('0.0')
    # summary
    roz_A_brutto: Decimal = Decimal('0.0')
    roz_B_brutto: Decimal = Decimal('0.0')
    roz_A_netto: Decimal = Decimal('0.0')
    roz_B_netto: Decimal = Decimal('0.0')
    roz_B_III: Decimal = Decimal('0.0')
    roz_D: Decimal = Decimal('0.0')
    roz_D_II: Decimal = Decimal('0.0')
    roz_D_III: Decimal = Decimal('0.0')
    roz_472: Decimal = Decimal('0.0')
    roz_068: Decimal = Decimal('0.0')
    # synthetic
    roz_281: Decimal = Decimal('0.0')
    roz_282: Decimal = Decimal('0.0')
    roz_283: Decimal = Decimal('0.0')
    roz_289: Decimal = Decimal('0.0')
    roz_322: Decimal = Decimal('0.0')
    roz_326: Decimal = Decimal('0.0')
    roz_362: Decimal = Decimal('0.0')
    roz_451: Decimal = Decimal('0.0')
    roz_452: Decimal = Decimal('0.0')
    roz_453: Decimal = Decimal('0.0')
    roz_456: Decimal = Decimal('0.0')
    roz_459: Decimal = Decimal('0.0')
    # vzz
    vzz_551: Decimal = Decimal('0.0')
    # identification
    year: str = date.today().year-1
    organization_id: str ='00261220'

    #
    # calculations
    #
    
    # celkovy dluh
    def calc_CD(self) -> Decimal:
        return Decimal(
            self.roz_281 +
            self.roz_282 +
            self.roz_283 +
            self.roz_289 +
            self.roz_322 +
            self.roz_326 +
            self.roz_362 +
            self.roz_451 +
            self.roz_452 +
            self.roz_453 +
            self.roz_456 +
            self.roz_459)
    
    # aktiva celkem
    def calc_AC(self) -> Decimal:
        return Decimal(self.roz_A_netto + self.roz_B_netto)

    # bezne prijmy
    def calc_BP(self) -> Decimal:
        return Decimal(self.fin_4010 +
            self.fin_4020 +
            self.calc_41xx())

    # prijate neinvesticni transfery
    def calc_41xx(self) -> Decimal:
        return Decimal(
            self.fin_4111 + 
            self.fin_4112 +
            self.fin_4113 +
            self.fin_4116 +
            self.fin_4119 +
            self.fin_4121 +
            self.fin_4122 +
            self.fin_4123 +
            self.fin_4129 +
            self.fin_4151 +
            self.fin_4152 +
            self.fin_4153 +
            self.fin_4155 +
            self.fin_4156 +
            self.fin_4159 +
            self.fin_4160)

    # projate investicni transfery
    def calc_42xx(self) -> Decimal:
        return Decimal(
            self.fin_4211 +
            self.fin_4212 +
            self.fin_4213 +
            self.fin_4214 +
            self.fin_4216 +
            self.fin_4218 +
            self.fin_4219 +
            self.fin_4221 +
            self.fin_4222 +
            self.fin_4229 +
            self.fin_4231 +
            self.fin_4232 +
            self.fin_4233 +
            self.fin_4234 +
            self.fin_4235
        )

    # konsolidovane bezne vydaje
    def calc_KBV(self) -> Decimal:
        return Decimal(self.fin_4210 - self.fin_4250)
    
    # dluhova sluzba dlouhodobe
    def calc_DSD(self) -> Decimal:
        return Decimal(self.fin_5141 +
            (abs(self.fin_8122 + self.fin_8124)) +
            self.fin_5178 +
            self.fin_6143)

    # dluhova sluzba celkem
    def calc_DSC(self) -> Decimal:
        return Decimal(
            self.fin_5141 +
            # self.fin_5178 +
            (self.fin_8xx2 * -1) +
            (self.fin_8xx4 * -1)
            )

    # konsolidace vydaju
    def calc_534x(self) -> Decimal:
        return Decimal(
            self.fin_5342 +
            self.fin_5344 +
            self.fin_5345 +
            self.fin_5347 +
            self.fin_5348 +
            self.fin_5349)

    # celkove kapitalove prijmy
    def calc_CKP(self) -> Decimal:
        return Decimal(
            self.fin_4030 +
            self.calc_42xx()
        )

    #
    # indicators
    #

    # in %
    def VPCP(self) -> Decimal:
        return (self.fin_4010 + self.fin_4020 + self.fin_4030) / self.fin_4200

    def CPBR(self) -> Decimal:
        return (self.calc_BP() - self.calc_KBV() + self.fin_5141 + self.fin_5178 + self.fin_6143) / 1000000

    # in %
    def RS(self) -> Decimal:
        return (self.fin_4200 - self.fin_4430) / self.fin_4200

    def RS_RZD(self) -> Decimal:
        return self.fin_4200 - self.fin_4430 + self.roz_B_III + self.roz_068

    # in %
    def SBR(self) -> Decimal:
        return (self.CPBR()*1000000 ) / self.calc_BP()

    # in months
    def BUKBV(self) -> Decimal:
        return ((self.roz_B_III + self.roz_068) / self.fin_4430) * 12

    #
    def KSKV(self) -> Decimal:
        return (((self.calc_BP() - self.calc_KBV()) + self.fin_4030 + self.calc_42xx()) / self.fin_4220)

    #
    def SKR(self) -> Decimal:
        return (self.fin_4030 + self.calc_42xx() - self.fin_4220) / 1000000

    # in %
    def BUKBP(self) -> Decimal:
        return (self.roz_B_III + self.roz_068) / self.calc_BP()

    # index
    def KVBP(self) -> Decimal:
        return self.fin_4430 / self.calc_BP()

    # # in %
    # def TRKV(self) -> Decimal:
    #     # prijate transfery po konsolidaci / kapitalove vydaje
    #     # return (self.fin_4040 - self.P534x()) / self.fin_4220
    #     return (self.fin_4040 - self.fin_4060) / self.fin_4220

    # 
    def KPIT(self) -> Decimal:
        return (self.calc_42xx() / self.fin_4220)

    #
    def KVSBR(self) -> Decimal:
        return (self.fin_4220 / (self.calc_BP() - self.calc_KBV()))

    # in %
    def IA(self) -> Decimal:
        return (self.fin_4220 / (self.calc_KBV() + self.fin_4220))

    # in %
    def URM(self) -> Decimal:
        return (self.fin_4220 / self.vzz_551) if self.vzz_551 != 0 else Decimal('0.0')

    # in months
    def CDSBR(self) -> Decimal:
        return ( self.calc_CD() / (self.calc_BP() - self.calc_KBV()))

    # in %
    def DSSBR(self) -> Decimal:
        return ( (((self.fin_8xx2 + self.fin_8xx4) * -1) + self.fin_5141) / 
            (self.calc_BP() - self.calc_KBV() - self.fin_5141)  )

    # in %
    def PUSBR(self) -> Decimal:
        return self.fin_5141 / (self.calc_BP() - self.calc_KBV() + self.fin_5141)

    # in %
    def CZCA(self) -> Decimal:
        if self.calc_AC() == 0:
            return Decimal('0.0')
        return self.roz_D / self.calc_AC()

    # in %
    def CZCA1(self) -> Decimal:
        if self.calc_AC() == 0:
            return Decimal('0.0')
        return (self.roz_D - self.roz_472) / self.calc_AC()
    
    # # in %
    # def DCZ(self) -> Decimal:
    #     return self.CD() / self.roz_D

    # in %
    def DSC(self) -> Decimal:
        # return self.calc_DSC() / (self.fin_4010 + self.fin_4020 + self.fin_4112 + self.fin_4212)
        return self.calc_DSC() / self.fin_4200

    # 
    def KDS(self) -> Decimal:
        return (self.CPBR()*1000000 / self.calc_DSD()) if self.calc_DSD() > 0 else Decimal('0.0')


    # # in %
    # def DBP(self) -> Decimal:
    #     return self.CD() / self.BP()

    # index
    def CL(self) -> Decimal:
        if self.roz_D_III == 0:
            return Decimal('0.0')
        return self.roz_B_netto / self.roz_D_III

    # index
    def OL(self) -> Decimal:
        if self.roz_D_III == 0:
            return Decimal('0.0')
        return self.roz_B_III / self.roz_D_III

    # index
    def FZ(self) -> Decimal:
        if (self.roz_D_III + self.roz_D_II) == 0:
            return Decimal('0.0')
        return (self.roz_B_III + self.roz_068) / (self.roz_D_III + self.roz_D_II)