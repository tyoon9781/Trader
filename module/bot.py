from pykiwoom.kiwoom import Kiwoom
import pandas as pd
import time
from datetime import datetime

from multiprocessing import Queue

class MyBot:
    TEST_SCREEN = "0970"
    TEST_SCREEN2 = "0971"
    주식체결="주식체결"
    def __init__(self):
        kiwoom = Kiwoom()
        kiwoom.CommConnect(block=True)
        self.kw = kiwoom
        self.account_count = self.kw.GetLoginInfo("ACCOUNT_CNT")
        self.account_list = self.kw.GetLoginInfo("ACCNO")
        self.account, = self.account_list
        self.user_id = self.kw.GetLoginInfo("USER_ID")
        self.user_name = self.kw.GetLoginInfo("USER_NAME")
        self.keyboard_secure_exception = bool(self.kw.GetLoginInfo("KEY_BSECGB"))
        self.waterwall_setup = bool(self.kw.GetLoginInfo("FIREW_SECGB"))
        self.connection = bool(self.kw.GetConnectState())
        self.conditions:pd.DataFrame = self.get_conditions()
        self.init()

    def init(self):
        print("My bot start")
        ## call back connect
        self.kw.ocx.OnReceiveRealData.connect(self.test_get_real_time_data)

    def get_conditions(self):
        self.kw.GetConditionLoad()
        return pd.DataFrame(self.kw.GetConditionNameList(), columns=["index", "name"])

    ## call
    def test_real_time_info_connect(self):
        self.kw.SetRealReg(self.TEST_SCREEN, "048530;005930;000020", "10:20", 0)
        # self.kw.SetRealReg(self.TEST_SCREEN2, "000020", "10", 0)
        print("Connect test")
    ## disconnect
    def test_real_time_info_disconnect(self):
        self.kw.DisconnectRealData(self.TEST_SCREEN)
        # self.kw.DisconnectRealData(self.TEST_SCREEN2)
        print("Disconnect test")

    ## back
    def test_get_real_time_data(self, code, real_type, data):
        print("real_type:", real_type, "code:", code, "data:", data)
        ## 주식시세
        print("====주식시세====")
        print(f"현재가 {code} Data :", self.kw.GetCommRealData(code, "10"))
        print(f"전일대비 {code} Data :", self.kw.GetCommRealData(code, "11"))
        print(f"등락율 {code} Data :", self.kw.GetCommRealData(code, "12"))
        print(f"최우선매도호가 {code} Data :", self.kw.GetCommRealData(code, "27"))
        print(f"최우선매수호가 {code} Data :", self.kw.GetCommRealData(code, "28"))
        print(f"누적거래량 {code} Data :", self.kw.GetCommRealData(code, "13"))
        print(f"누적거래대금 {code} Data :", self.kw.GetCommRealData(code, "14"))
        print(f"시가 {code} Data :", self.kw.GetCommRealData(code, "16"))
        print(f"고가 {code} Data :", self.kw.GetCommRealData(code, "17"))
        print(f"저가 {code} Data :", self.kw.GetCommRealData(code, "18"))
        print(f"전일대비기호 {code} Data :", self.kw.GetCommRealData(code, "25"))
        print(f"전일거래량대비(계약, 주) {code} Data :", self.kw.GetCommRealData(code, "26"))
        print(f"거래대금증감 {code} Data :", self.kw.GetCommRealData(code, "29"))
        print(f"전일거래량대비(비율) {code} Data :", self.kw.GetCommRealData(code, "30"))
        print(f"거래회전율 {code} Data :", self.kw.GetCommRealData(code, "31"))
        print(f"거래비용 {code} Data :", self.kw.GetCommRealData(code, "32"))
        print(f"시가총액(억) {code} Data :", self.kw.GetCommRealData(code, "311"))
        print(f"상한가발생시간 {code} Data :", self.kw.GetCommRealData(code, "567"))
        print(f"하한가발생시간 {code} Data :", self.kw.GetCommRealData(code, "568"))
        print()

        ## 주식체결
        print("====주식체결====")
        print(f"체결시간 {code} Data :", self.kw.GetCommRealData(code, "20"))
        print(f"현재가 {code} Data :", self.kw.GetCommRealData(code, "10"))
        print(f"전일대비 {code} Data :", self.kw.GetCommRealData(code, "11"))
        print(f"등락율 {code} Data :", self.kw.GetCommRealData(code, "12"))
        print(f"최우선매도호가 {code} Data :", self.kw.GetCommRealData(code, "27"))
        print(f"최우선매수호가 {code} Data :", self.kw.GetCommRealData(code, "28"))
        print(f"거래량(+매수, -매도) {code} Data :", self.kw.GetCommRealData(code, "15"))
        print(f"누적거래량 {code} Data :", self.kw.GetCommRealData(code, "13"))
        print(f"누적거래대금 {code} Data :", self.kw.GetCommRealData(code, "14"))
        print(f"시가 {code} Data :", self.kw.GetCommRealData(code, "16"))
        print(f"고가 {code} Data :", self.kw.GetCommRealData(code, "17"))
        print(f"저가 {code} Data :", self.kw.GetCommRealData(code, "18"))
        print(f"전일대비기호 {code} Data :", self.kw.GetCommRealData(code, "25"))
        print(f"전일거래량대비(계약, 주) {code} Data :", self.kw.GetCommRealData(code, "26"))
        print(f"거래대금증감 {code} Data :", self.kw.GetCommRealData(code, "29"))
        print(f"전일거래량대비(비율) {code} Data :", self.kw.GetCommRealData(code, "30"))
        print(f"거래회전율 {code} Data :", self.kw.GetCommRealData(code, "31"))
        print(f"거래비용 {code} Data :", self.kw.GetCommRealData(code, "32"))
        print(f"시가총액(억) {code} Data :", self.kw.GetCommRealData(code, "311"))
        print(f"장구분 {code} Data :", self.kw.GetCommRealData(code, "290"))
        print(f"KO접근도 {code} Data :", self.kw.GetCommRealData(code, "691"))
        print(f"상한가발생시간 {code} Data :", self.kw.GetCommRealData(code, "567"))
        print(f"하한가발생시간 {code} Data :", self.kw.GetCommRealData(code, "568"))
        print(f"전일 동시간 거래량 비율 {code} Data :", self.kw.GetCommRealData(code, "851"))
        print()


    def request_day_history_info(self, code, date, count=5):
        """
        code = string
        date = string: "20200424"
        flag = 0:수정주가구분 적용 안함, 1: 수정주가구분 적용
        next = 0:단일, 2: 연속
        """
        def _next_block_request(_dfs, code, date):
            _df = self.kw.block_request("opt10081", 종목코드=code, 기준일자=date, 수정주가구분=1, output="주식일봉차트조회", next=2)
            _dfs.append(_df)
            time.sleep(0.5)
            return _dfs
        
        dfs = []
        df = self.kw.block_request("opt10081", 종목코드=code, 기준일자=date, 수정주가구분=1, output="주식일봉차트조회", next=0)
        dfs.append(df)

        if count == 0:
            while self.kw.tr_remained:
                dfs = _next_block_request(dfs, code, date)
        elif count > 0:
            for _ in range(count - 1):
                dfs = _next_block_request(dfs, code, date)

        return dfs

    def request_minute_history_info(self, code, date, count):
        """
        code = string
        date = string: "20200424"
        flag = 0:수정주가구분 적용 안함, 1: 수정주가구분 적용
        next = 0:단일, 2: 연속
        """
        def _next_block_request(_dfs, code, date):
            _df = self.kw.block_request("opt10080", 종목코드=code, 기준일자=date, 수정주가구분=1, output="주식주봉차트조회", next=2)
            _dfs.append(_df)
            time.sleep(0.5)
            return _dfs
        
        dfs = []
        df = self.kw.block_request("opt10080", 종목코드=code, 기준일자=date, 수정주가구분=1, output="주식주봉차트조회", next=0)
        dfs.append(df)

        if count == 0:
            while self.kw.tr_remained:
                dfs = _next_block_request(dfs, code, date)
        elif count > 0:
            for _ in range(count - 1):
                dfs = _next_block_request(dfs, code, date)

        return dfs

    def request_basic_info(self, code) -> pd.DataFrame:
        return self.kw.block_request("opt10001", 종목코드=code, output="주식기본정보", next=0)

    ## todo
    def is_exist_order_no(order_no):
        pass

    ######################################
    # well-made methods
    ######################################
    def get_history_day_info_once(self, code) -> pd.DataFrame:
        return self.kw.block_request("opt10081", 종목코드=code, 기준일자=datetime.now().strftime("%Y%m%d"), 수정주가구분=1, output="주식일봉차트조회", next=0)
    
    def get_history_minute_info_once(self, code) -> pd.DataFrame:
        return self.kw.block_request("opt10080", 종목코드=code, 기준일자=datetime.now().strftime("%Y%m%d"), 수정주가구분=1, output="주식분봉차트조회", next=0)
    
    def get_history_tick_info_once(self, code) -> pd.DataFrame:
        return self.kw.block_request("opt10079", 종목코드=code, 기준일자=datetime.now().strftime("%Y%m%d"), 수정주가구분=1, output="주식틱봉차트조회", next=0)

    def get_basic_info_themes(self, format: str="gc"):
        if format == "gc":
            print(self.kw.GetThemeGroupList(1))  ## {그룹명 : 코드}
        elif format == "cg":
            print(self.kw.GetThemeGroupList(0))  ## {코드 : 그룹명}
        else:
            print("no match format")

    def get_account_info_conditional_expression(self, name):
        index = self.conditions.loc[self.conditions["name"] == name].iloc[0]["index"]
        return self.kw.SendCondition("0101", name, index, 0)

    def get_market_info_etf(self) -> pd.DataFrame:
        etf = self.kw.GetCodeListByMarket('8')
        return self._get_detail_info_from_codes(etf)

    def get_market_info_kosdac(self) -> pd.DataFrame:
        kosdaq = self.kw.GetCodeListByMarket('10')
        return self._get_detail_info_from_codes(kosdaq)

    def get_market_info_kospi(self) -> pd.DataFrame:
        _info = self.kw.GetCodeListByMarket('0')
        mutual = self.kw.GetCodeListByMarket('4')
        reits = self.kw.GetCodeListByMarket('6')
        etf = self.kw.GetCodeListByMarket('8')
        delete_list = mutual + reits + etf
        kospi = [x for x in _info if x not in delete_list]
        return self._get_detail_info_from_codes(kospi)

    def get_market_info_kosdac_n_kospi(self) -> pd.DataFrame:
        return pd.concat([self.get_market_info_kospi(), self.get_market_info_kosdac()])

    def _get_detail_info_from_codes(self, codes: list) -> pd.DataFrame:
        result = []
        for code in codes:
            c0 = code
            c1 = self.kw.GetMasterCodeName(code)         ## 종목명
            c2 = self.kw.GetMasterListedStockCnt(code)   ## 주식 수
            c3 = self.kw.GetMasterConstruction(code)     ## 감리구분
            c4 = self.kw.GetMasterListedStockDate(code)  ## 상장일
            c5 = self.kw.GetMasterLastPrice(code)        ## 전일가
            c6 = self.kw.GetMasterStockState(code)       ## 종목상태
            result.append([c0, c1, c2, c3, c4, c5, c6])
        df = pd.DataFrame(result, columns=["code", "종목명", "주식 수", "감리구분", "상장일", "전일가", "종목상태"])
        return df

    def order_buy_market_price(self, code, quantity):
        """ 회사, 주식량 시장가 매수 """
        self.kw.SendOrder(rqname="시장가매수", screen="0101", accno=self.account, order_type=1, code=code, quantity=quantity, price=0, hoga="03", order_no="")

    def order_sell_market_price(self, code, quantity):
        """ 회사, 주식량 시장가 매도 """
        self.kw.SendOrder(rqname="시장가매도", screen="0101", accno=self.account, order_type=2, code=code, quantity=quantity, price=0, hoga="03", order_no="")

    def order_buy_custom_price(self, code, quantity, price):
        """ 회사, 주식량, 지정가 매수 """
        self.kw.SendOrder(rqname="지정가매수", screen="0101", accno=self.account, order_type=1, code=code, quantity=quantity, price=price, hoga="00", order_no="")

    def order_sell_custom_price(self, code, quantity, price):
        """ 회사, 주식량, 지정가 매도 """
        self.kw.SendOrder(rqname="지정가매도", screen="0101", accno=self.account, order_type=2, code=code, quantity=quantity, price=price, hoga="00", order_no="")

    def cancel_buy_market_price(self, code, quantity, order_no):
        """ 회사, 주식량 시장가 매수 취소 """
        self.kw.SendOrder(rqname="시장가매수", screen="0101", accno=self.account, order_type=1, code=code, quantity=quantity, price=0, hoga="03", order_no=order_no)

    def cancel_sell_market_price(self, code, quantity, order_no):
        """ 회사, 주식량 시장가 매도 취소 """
        self.kw.SendOrder(rqname="시장가매도", screen="0101", accno=self.account, order_type=2, code=code, quantity=quantity, price=0, hoga="03", order_no=order_no)

    def cancel_buy_custom_price(self, code, quantity, price, order_no):
        """ 회사, 주식량, 지정가 매수 취소 """
        self.kw.SendOrder(rqname="지정가매수", screen="0101", accno=self.account, order_type=1, code=code, quantity=quantity, price=price, hoga="00", order_no=order_no)

    def cancel_sell_custom_price(self, code, quantity, price, order_no):
        """ 회사, 주식량, 지정가 매도 취소 """
        self.kw.SendOrder(rqname="지정가매도", screen="0101", accno=self.account, order_type=2, code=code, quantity=quantity, price=price, hoga="00", order_no=order_no)

    @staticmethod
    def is_code_valid(code: str):
        if isinstance(code, str) and len(code) == 6:
            return True
        return False

    @staticmethod
    def is_order_number_valid(number: int):
        if isinstance(number, int) and number > 0:
            return True
        return False
    

