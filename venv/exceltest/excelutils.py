import xlrd
from xToolkit import xfile
from hctest_excel_to.excel_to import Excel
import pandas as pd

class ExcelUtil:
    def __init__(self, excelPath, sheetName):
        self.data = xlrd.open_workbook(excelPath)
        self.table = self.data.sheet_by_name(sheetName)

        # 获取第一行作为key值
        self.keys = self.table.row_values(0)
        # 获取总行数
        self.rowNum = self.table.nrows
        # 获取总列数
        self.colNum = self.table.ncols

    def dict_data(self):
        if self.rowNum <= 1:
            print("总行数小于1")
        else:
            r = []
            j = 1
            for i in range(self.rowNum - 1):
                s = {}
                # 从第二行取对应values值
                values = self.table.row_values(j)
                for x in range(self.colNum):
                    s[self.keys[x]] = values[x]
                r.append(s)
                j += 1
            return r

    def get_dic_data1(self, file_path):
        datalist = xfile.read(file_path).excel_to_dict(sheet=0)
        print(datalist)

    def get_dic_data2(self, file_path):
        ex = Excel(file_path)
        ex.sheet_name = "Sheet1"
        ls_data = ex.get_key_value_list_to_list(start=2)
        js_data = ex.get_key_value_list_to_json(start=2)
        tp_data = ex.get_key_value_list_to_tuple(start=2)
        print(ls_data)
        print(js_data)
        print(tp_data)

    def get_dic_data3(self, file_path):
        # Read the Excel file into a DataFrame
        df = pd.read_excel(file_path, sheet_name=0)

        # Convert the DataFrame to a dictionary
        data_dict = df.to_dict()

        print(data_dict)


if __name__ == '__main__':
    file_path = "D:\\workspace\\pythonlearning\\venv\\exceltest\\testdata\\testdata.xlsx"
    sheet_name = "Sheet1"
    data = ExcelUtil(file_path, sheet_name)
    print(data.dict_data())

    data.get_dic_data1(file_path)
    data.get_dic_data2(file_path)
    data.get_dic_data3(file_path)
