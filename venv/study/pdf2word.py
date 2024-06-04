import pdf2docx
import os
from pdf2docx import Converter


def pdf2word():
    # 替换为自己文件所在目录
    file_path = r'C:\temp\pdf2word'
    # 遍历所有文件
    for file in os.listdir(file_path):
        suff_name = os.path.splitext(file)[1]  # 获取文件后缀
        # 过滤非pdf格式文件
        if suff_name != '.pdf':
            continue

        file_name = os.path.splitext(file)[0]  # 获取文件名称
        pdf_name = file_path + '\\' + file
        docx_name = file_path + '\\' + file_name + '.docx'  # 要转换的docx文件名称
        # 加载pdf文档
        cv = Converter(pdf_name)
        cv.convert(docx_name)
        cv.close()


if __name__ == '__main__':
    pdf2word()
