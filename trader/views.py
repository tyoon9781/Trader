from PyQt5 import QtWidgets
from PyQt5.QtCore import Qt

from trader.form import Ui_MainWindow
from module.bot import MyBot


class Trader(QtWidgets.QMainWindow):
    def __init__(self):
        QtWidgets.QMainWindow.__init__(self)
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)

        self.my_bot = MyBot()

        self.market_price_flag = False
        self.current_buy_volume = 0
        self.current_sell_volume = 0
        self.current_proceeds = 0
        self.current_auto_trade_start_time = self.ui.dateTimeEdit_auto_trade_start_time.dateTime().time()
        self.current_auto_trade_end_time = self.ui.dateTimeEdit_auto_trade_end_time.dateTime().time()
        self.current_max_buy_stock_num = int(self.ui.lineEdit_max_buy_stock_num.text())
        self.current_total_amount_per_stock = int(self.ui.lineEdit_total_amount_per_stock.text().replace(",", ""))
        self.current_total_sell_adv_ratio = float(self.ui.lineEdit_total_sell_adv_ratio.text())
        self.current_total_sell_dis_ratio = float(self.ui.lineEdit_total_sell_dis_ratio.text())
        self.current_total_sell_time = self.ui.dateTimeEdit_total_sell_time.dateTime().time()
        self.market_info = self.my_bot.get_market_info_kosdac_n_kospi()
        self.current_company_code = "000000"
        self.condition_table_column_checkbox = QtWidgets.QCheckBox()
        self.condition_table_checkbox_list = []
        self.condition_table_all_checked = False
        self.condition_table_sorted_reverse = False

        self.init()
    
    def init(self):
        ## connect auto page
        self.ui.pushButton_auto_trading_start.clicked.connect(self.click_pushButton_auto_trading_start)
        self.ui.pushButton_auto_trading_end.clicked.connect(self.click_pushButton_auto_trading_end)
        self.ui.pushButton_select_conditional.clicked.connect(self.click_pushButton_select_conditional)
        ## get basic info
        self._update_label_buy_volume()
        self._update_label_sell_volume()
        self._update_label_proceeds()
        self._update_comboBox_conditional()
        
        ## change conditional_table_column_checkbox
        self.ui.tableWidget_contitional_search.horizontalHeader().sectionClicked.connect(self.click_tableWidget_contitional_search)

        ##########################
        ## connect manual page
        ##########################
        self.ui.pushButton_buy_order.clicked.connect(self.click_pushButton_buy_order)
        self.ui.pushButton_sell_order.clicked.connect(self.click_pushButton_sell_order)
        self.ui.pushButton_fix_order.clicked.connect(self.click_pushButton_sell_order)
        self.ui.pushButton_cancel_order.clicked.connect(self.click_pushButton_cancle_order)
        self.ui.pushButton_search_company.clicked.connect(self.click_pushButton_search_company)
        self.ui.checkBox_market_price.stateChanged.connect(self.change_checkbox_market_price)

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

    def click_tableWidget_contitional_search(self, column):
        if column == 0:
            self.condition_table_all_checked = not self.condition_table_all_checked
            for checkbox in self.condition_table_checkbox_list:
                checkbox: QtWidgets.QCheckBox
                checkbox.setChecked(self.condition_table_all_checked)
        else:
            self.condition_table_sorted_reverse = not self.condition_table_sorted_reverse
            if self.condition_table_sorted_reverse:
                self.ui.tableWidget_contitional_search.sortItems(column, order=Qt.SortOrder.AscendingOrder)
            else:
                self.ui.tableWidget_contitional_search.sortItems(column, order=Qt.SortOrder.DescendingOrder)

    def click_pushButton_select_conditional(self):
        current_conditional_text = self.ui.comboBox_conditional.currentText()
        code_list = self.my_bot.get_account_info_conditional_expression(current_conditional_text)
        self.ui.tableWidget_contitional_search.setRowCount(len(code_list))
        self.condition_table_checkbox_list = []
        for i in range(len(code_list)):
            self.condition_table_checkbox_list.append(QtWidgets.QCheckBox())
        for row_idx, code in enumerate(code_list):
            row_data = [
                "checkbox",
                "상태",
                code,
                self.my_bot.kw.GetMasterCodeName(code),     ## 종목 명
                "구문",
                self.my_bot.kw.GetCommRealData(code, 11),   ## 전일 대비
                self.my_bot.kw.GetCommRealData(code, 10),   ## 현재가
                self.my_bot.kw.GetCommRealData(code, 12),   ## 등락율
                self.my_bot.kw.GetCommRealData(code, 13),   ## 누적거래량
                "편입가",
                "편입대비",
                "수익률"
            ]
            for col_idx, item_data in enumerate(row_data):
                if col_idx == 0:
                    self.ui.tableWidget_contitional_search.setCellWidget(row_idx, col_idx, self.condition_table_checkbox_list[row_idx])
                else:
                    item = QtWidgets.QTableWidgetItem(str(item_data))
                    self.ui.tableWidget_contitional_search.setItem(row_idx, col_idx, item)
        print("click_pushButton_select_conditional")

    def click_pushButton_auto_trading_end(self):
        print("click_pushButton_auto_trading_end")

    def click_pushButton_auto_trading_start(self):
        print("click_pushButton_auto_trading_start")

    def _update_comboBox_conditional(self):
        self.ui.comboBox_conditional.addItems(self.my_bot.conditions["name"])

    def _update_label_buy_volume(self):
        self.ui.label_buy_volume.setText(str(self.current_buy_volume))

    def _update_label_sell_volume(self):
        self.ui.label_sell_volume.setText(str(self.current_sell_volume))

    def _update_label_proceeds(self):
        self.ui.label_proceeds.setText(str(self.current_proceeds))

    def _update_label_company_code(self):
        self.ui.label_company_code.setText(str(self.current_company_code))

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