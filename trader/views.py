from PyQt5.QtWidgets import QMainWindow
import pandas as pd

from trader.form import Ui_MainWindow
from module.bot import MyBot


class Trader(QMainWindow):
    def __init__(self):
        QMainWindow.__init__(self)
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)

        self.my_bot = MyBot()

        self.market_price_flag = False
        self.kosdac_info = self.my_bot.get_kosdac_market_info()
        self.kospi_info = self.my_bot.get_kospi_market_info()
        self.etf_info = self.my_bot.get_etf_market_info()
        self.market_info = pd.concat([self.kosdac_info, self.kospi_info])
        self.current_company_code = "000000"

        self.init()
    
    def init(self):
        ## connect
        self.ui.pushButton_buy_order.clicked.connect(self.click_pushButton_buy_order)
        self.ui.pushButton_sell_order.clicked.connect(self.click_pushButton_sell_order)
        self.ui.pushButton_fix_order.clicked.connect(self.click_pushButton_sell_order)
        self.ui.pushButton_cancel_order.clicked.connect(self.click_pushButton_cancle_order)
        self.ui.checkBox_market_price.stateChanged.connect(self.change_checkbox_market_price)
        self.ui.pushButton_search_company.clicked.connect(self.click_pushButton_search_company)

        ## get basic info
        self._update_label_company_code()        
        self.ui.label_user_id.setText(f"아이디 : {self.my_bot.user_id}")
        self.ui.label_user_name.setText(f"이름 : {self.my_bot.user_name}")
        self.ui.label_account_count.setText(f"계좌수 : {self.my_bot.account_count}")
        ## TODO : 복수 계좌
        self.ui.label_account.setText(f"선택계좌 : {self.my_bot.account}")   
        self.ui.label_keyboard_secure_exception.setText(f"키보드 보안 처리 : {self.my_bot.keyboard_secure_exception}")
        self.ui.label_waterwall_setup.setText(f"방화벽 설정 : {self.my_bot.waterwall_setup}")
        self.ui.label_connection.setText(f"연결 : {self.my_bot.connection}")
        self.ui.lineEdit_company_name.setPlaceholderText("종목명")

    def _update_label_company_code(self):
        self.ui.label_company_code.setText(self.current_company_code)

    def _get_quantity(self):
        quantity = self.ui.lineEdit_order_quantity.text()
        flag = False
        if quantity == '':
            print(f"[Error] [_get_quantity] 주식 수량을 입력해 주세요.")
        else:
            try:
                quantity = abs(int(quantity))
                flag= True
            except ValueError:
                print(f"[Error] [_get_quantity] 주식 수량({quantity})이 유효하지 않습니다.")

        return quantity, flag


    def _get_custom_price(self):
        price = self.ui.lineEdit_order_price.text()
        flag = False
        if price == '':
            print(f"[Error] [_get_custom_price] 지정가를 입력해 주세요.")
        else:
            try:
                price = abs(int(price))
                flag = True
            except ValueError:
                print(f"[Error] [_get_custom_price] 지정가({price})가 유효하지 않습니다.")

        return price, flag

    def click_pushButton_search_company(self):
        current_text = self.ui.lineEdit_company_name.text()
        search_result = self.market_info[self.market_info["종목명"] == current_text]["코드"].values
        if len(search_result) == 1:
            result, = search_result
            self.current_company_code = result
        else:
            self.current_company_code = "000000"
        self._update_label_company_code() 

    def click_pushButton_buy_order(self):
        code = self.current_company_code
        quantity, quantity_flag = self._get_quantity()
        if not quantity_flag:
            return False
        if self.market_price_flag:
            self.my_bot.order_buy_market_price(code, quantity)
        else:
            custom_price, custom_price_flag = self._get_custom_price()
            if not custom_price_flag:
                return False
            self.my_bot.order_buy_custom_price(code, quantity, custom_price)

    def click_pushButton_sell_order(self):
        code = self.current_company_code
        quantity, quantity_flag = self._get_quantity()
        if not quantity_flag:
            return False
        if self.market_price_flag:
            self.my_bot.order_sell_market_price(code, quantity)
        else:
            custom_price, custom_price_flag = self._get_custom_price()
            if not custom_price_flag:
                return False
            self.my_bot.order_sell_custom_price(code, quantity, custom_price)

    def click_pushButton_fix_order(self):
        pass

    def click_pushButton_cancle_order(self):
        pass

    def change_checkbox_market_price(self):
        if self.ui.checkBox_market_price.isChecked():
            self.ui.lineEdit_order_price.setDisabled(True)
            self.market_price_flag = True
        else:
            self.ui.lineEdit_order_price.setEnabled(True)
            self.market_price_flag = False