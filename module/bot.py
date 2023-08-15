from pykiwoom.kiwoom import *
import pandas as pd
import time
from datetime import datetime



class MyBot:
    def __init__(self):
        kiwoom = Kiwoom()
        kiwoom.CommConnect(block=True)
        
        self.kw = kiwoom
        self.account_count = self.kw.GetLoginInfo("ACCOUNT_CNT")
        self.account_list = self.kw.GetLoginInfo("ACCNO")
        self.user_id = self.kw.GetLoginInfo("USER_ID")
        self.user_name = self.kw.GetLoginInfo("USER_NAME")
        self.keyboard_secure_exception = bool(self.kw.GetLoginInfo("KEY_BSECGB"))
        self.waterwall_setup = bool(self.kw.GetLoginInfo("FIREW_SECGB"))
        self.connection = bool(self.kw.GetConnectState())
        self.account, = self.account_list
        self.init()

    def init(self):
        print("전체 계좌수 :", self.kw.GetLoginInfo("ACCOUNT_CNT"))
        print("전체 계좌번호 리스트 :", self.kw.GetLoginInfo("ACCNO"))
        print("사용자 ID :", self.kw.GetLoginInfo("USER_ID"))
        print("사용자명 :", self.kw.GetLoginInfo("USER_NAME"))
        print("키보드 보안 처리 :", bool(self.kw.GetLoginInfo("KEY_BSECGB")))
        print("방화벽 설정 여부 :", bool(self.kw.GetLoginInfo("FIREW_SECGB")))
        print("연결 여부 :", bool(self.kw.GetConnectState()))

    def get_theme_table(self, format: str="gc"):
        if format == "gc":
            print(self.kw.GetThemeGroupList(1))  ## {그룹명 : 코드}
        elif format == "cg":
            print(self.kw.GetThemeGroupList(0))  ## {코드 : 그룹명}
        else:
            print("no match format")

    def get_condition_info(self):
        # 조건 얻기
        self.kw.GetConditionLoad()
        # 전체 조건식 리스트 얻기
        conditions = self.kw.GetConditionNameList()
        # 0번 조건식에 해당하는 종목 리스트 출력
        condition_index = conditions[0][0]
        condition_name = conditions[0][1]
        codes = self.kw.SendCondition("0101", condition_name, condition_index, 0)
        print(codes)

    def get_etf_market_info(self) -> pd.DataFrame:
        etf = self.kw.GetCodeListByMarket('8')
        return self._get_detail_info_from_codes(etf)

    def get_kosdac_market_info(self) -> pd.DataFrame:
        kosdaq = self.kw.GetCodeListByMarket('10')
        return self._get_detail_info_from_codes(kosdaq)

    def get_kospi_market_info(self) -> pd.DataFrame:
        kospi = self.kw.GetCodeListByMarket('0')
        return self._get_detail_info_from_codes(kospi)

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
        df = pd.DataFrame(result, columns=["코드", "종목명", "주식 수", "감리구분", "상장일", "전일가", "종목상태"])
        return df

    def order_buy_market_price(self, code, quantity):
        """
        회사, 주식량 시장가 매수
        """
        print(datetime.now())
        try:
            if self.is_code_valid(code) and self.is_order_number_valid(quantity):
                result = self.kw.SendOrder(rqname="시장가매수", screen="0101", accno=self.account, order_type=1, code=code, quantity=quantity, price=0, hoga="03", order_no="")
                print(result)
                print(f"[Info] [order_buy_market_price] {code}, {quantity}주, 시장가 buy order has been placed")
            else:
                print(f"[Error] [order_buy_market_price] {code} code or {quantity} quantity is incorrect")
        except Exception as e:
            print(f"[Error] {e}")

    def order_sell_market_price(self, code, quantity):
        """
        회사, 주식량 시장가 매도
        """
        print(datetime.now())
        try:
            if self.is_code_valid(code) and self.is_order_number_valid(quantity):
                result = self.kw.SendOrder(rqname="시장가매도", screen="0101", accno=self.account, order_type=2, code=code, quantity=quantity, price=0, hoga="03", order_no="")
                print(result)
                print(f"[Info] [order_sell_market_price] {code}, {quantity}주, 시장가 sell order has been placed")
            else:
                print(f"[Error] [order_sell_market_price] {code} code or {quantity} quantity is incorrect")
        except Exception as e:
            print(f"[Error] {e}")


    def order_buy_custom_price(self, code, quantity, price):
        """
        회사, 주식량, 지정가 매수
        """
        print(datetime.now())
        try:
            if self.is_code_valid(code) and self.is_order_number_valid(quantity):
                result = self.kw.SendOrder(rqname="지정가매수", screen="0101", accno=self.account, order_type=1, code=code, quantity=quantity, price=price, hoga="00", order_no="")
                print(result)
                print(f"[Info] [order_buy_custom_price] {code}, {quantity}주, {price}원 buy order has been placed")
            else:
                print(f"[Error] [order_buy_custom_price] {code} code or {quantity} quantity is incorrect")
        except Exception as e:
            print(f"[Error] {e}")

    def order_sell_custom_price(self, code, quantity, price):
        """
        회사, 주식량, 지정가 매도
        """
        print(datetime.now())
        try:
            if self.is_code_valid(code) and self.is_order_number_valid(quantity):
                result = self.kw.SendOrder(rqname="지정가매도", screen="0101", accno=self.account, order_type=2, code=code, quantity=quantity, price=price, hoga="00", order_no="")
                print(result)
                print(f"[Info] [order_sell_custom_price] {code}, {quantity}주, {price}원 sell order has been placed")
            else:
                print(f"[Error] [order_sell_custom_price] {code} code or {quantity} quantity is incorrect")
        except Exception as e:
            print(f"[Error] {e}")


    def cancel_buy_market_price(self, code, quantity, order_no):
        """
        회사, 주식량 시장가 매수 취소
        """
        print(datetime.now())
        try:
            if self.is_code_valid(code) and self.is_order_number_valid(quantity):
                if self.is_exist_order_no(order_no):
                    result = self.kw.SendOrder(rqname="시장가매수", screen="0101", accno=self.account, order_type=1, code=code, quantity=quantity, price=0, hoga="03", order_no=order_no)
                    print(result)
                    print(f"[Info] [cancel_buy_market_price] {order_no}, {code}, {quantity}주 buy order cancel complete")
                else:
                    print(f"[Warning] [cancel_buy_market_price] {order_no} order no is not exist")
            else:
                print(f"[Error] [cancel_buy_market_price] {code} code or {quantity} quantity is incorrect")
        except Exception as e:
            print(f"[Error] {e}")

    def cancel_sell_market_price(self, code, quantity, order_no):
        """
        회사, 주식량 시장가 매도 취소
        """
        print(datetime.now())
        if self.is_code_valid(code) and self.is_order_number_valid(quantity):
            if self.is_exist_order_no(order_no):
                result = self.kw.SendOrder(rqname="시장가매도", screen="0101", accno=self.account, order_type=2, code=code, quantity=quantity, price=0, hoga="03", order_no=order_no)
                print(result)
                print(f"[Info] [cancel_sell_market_price] {order_no}, {code}, {quantity}주, 시장가 sell order cancel complete")
            else:
                print(f"[Warning] [cancel_sell_market_price] {order_no} order no is not exist") 
        else:
            print(f"[Error] [cancel_sell_market_price] {code} code or {quantity} quantity is incorrect")


    def cancel_buy_custom_price(self, code, quantity, price, order_no):
        """
        회사, 주식량, 지정가 매수 취소
        """
        print(datetime.now())
        if self.is_code_valid(code) and self.is_order_number_valid(quantity):
            if self.is_exist_order_no(order_no):
                result = self.kw.SendOrder(rqname="지정가매수", screen="0101", accno=self.account, order_type=1, code=code, quantity=quantity, price=price, hoga="00", order_no=order_no)
                print(result)
                print(f"[Info] [cancel_buy_custom_price] {order_no}, {code}, {quantity}주, {price}원 buy order cancel complete")
            else:
                print(f"[Warning] [cancel_buy_custom_price] {order_no} order no is not exist") 
        else:
            print(f"[Error] [cancel_buy_custom_price] {code} code or {quantity} quantity is incorrect")


    def cancel_sell_custom_price(self, code, quantity, price, order_no):
        """
        회사, 주식량, 지정가 매도 취소
        """
        print(datetime.now())
        if self.is_code_valid(code) and self.is_order_number_valid(quantity):
            if self.is_exist_order_no(order_no):
                result = self.kw.SendOrder(rqname="지정가매도", screen="0101", accno=self.account, order_type=2, code=code, quantity=quantity, price=price, hoga="00", order_no=order_no)
                print(result)
                print(f"[Info] [cancel_buy_custom_price] {order_no}, {code}, {quantity}주, {price}원 sell order cancel complete")
            else:
                print(f"[Warning] [cancel_sell_custom_price] {order_no} order no is not exist") 
        else:
            print(f"[Error] [cancel_sell_custom_price] {code} code or {quantity} quantity is incorrect")

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
    

