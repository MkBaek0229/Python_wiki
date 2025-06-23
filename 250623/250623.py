
"""" tkinter 라이브러리 filedialog
 활용 csv파일 읽는 코드 """
# import tkinter
# import csv
# from tkinter import filedialog
#
#
# window = tkinter.Tk()
# window.geometry("300x300")
#
# def opencsv():
#     file_path = filedialog.askopenfilename(#askopenfilename 함수 매개 변수
#         title="CSV 파일 선택", # title, filetypes : 어떤 파일 확장자 open 대상 설정
#         filetypes=[("CSV files","*csv")]
#     )
#
#     if file_path: # file_path가 True이면 askfilename 함수의 반환값이 잘 들어왔다는 의미
#         with open(file_path, newline='', encoding='utf-8') as csvfile: # 파일 객체 오픈
#             reader = csv.reader(csvfile) # csv.reader 함수로 csv파일 객체 읽음.
#             for i , row in enumerate(reader):
#                 print(row)
#                 # if row[1] == '':
#                 #     print(f"결측치 발견{i}번째")
#                 # else:
#                 #     print(row[1])
#
# openbutton = tkinter.Button(window, text="csv 파일 열기", command=opencsv)
# openbutton.pack()
#



""" ttk.Treeview 활용 tkinter 안에 csv 파일 직접 읽어오기 """
import tkinter
from tkinter import ttk
import csv
from tkinter import filedialog
import pandas as pd
import numpy as np

# mydata = pd.read_csv("서울_대기오염_데이터_2025.csv")


TreeValues = []
switch = 0

origin_my_data = pd.DataFrame()




def load_csv():
    global TreeValues
    global origin_my_data

    file_path = filedialog.askopenfilename(
            title="CSV 파일 선택",
            filetypes=[("CSV files","*csv")]
    )
    print(file_path)

    if file_path:
        with open(file_path, newline='',encoding='utf-8') as csvfile:
            origin_my_data = pd.read_csv(csvfile)


            # reader = csv.reader(csvfile)

            # headers=next(reader) # csv.reader 함수로 csv파일 객체 읽음.
            #
            tree['columns'] = tuple(origin_my_data.columns)

            tree['show'] = 'headings'

            for col in origin_my_data.columns:
                tree.heading(col, text=col)
                tree.column(col, width=100, anchor='center')
            for row in origin_my_data.values:
                tree.insert('', 'end', values=list(row))
                TreeValues.append(list(row))


# todo 이상치 처리 함수
def handle_missing_value():
    global origin_my_data

    for i, j in origin_my_data.items():
        for e in j:
            if i == ['날짜']:
                print("true")
                pass
            elif pd.isna(e):
                e = 0.0
                pct25 = origin_my_data[i].quantile(.25)
                pct75 = origin_my_data[i].quantile(.75)
                iqr = pct75 - pct25
                origin_my_data[i] = np.where((origin_my_data[i] < (pct25 - 1.5 * iqr)) | (origin_my_data[i] > (pct75 + 1.5 * iqr)), np.nan,
                                     origin_my_data[i])





def handle_missing_value():
    global origin_my_data



    for i, j in origin_my_data.items():
        # tree['columns'] = i
        # tree['show'] = 'headings'
        # tree.heading(i, text=i)
        # tree.column(i, width=100, anchor='center')
        # tree.insert('', 'end', values=j)
        # TreeValues.append(j)
        for e in j:
            if i == ['날짜']:
                pass
            elif pd.isna(e):
                e = 0.0
                pct25 = origin_my_data[i].quantile(.25)
                pct75 = origin_my_data[i].quantile(.75)
                iqr = pct75 - pct25
                origin_my_data[i] = np.where((origin_my_data[i] < (pct25 - 1.5 * iqr)) | (origin_my_data[i] > (pct75 + 1.5 * iqr)), np.nan,
                                     origin_my_data[i])


    print(origin_my_data.isna().sum())


# todo 결측치 제거
def jager():
    global origin_my_data


    # 날짜 컬럼 제외한 컬럼 리스트
    cols_to_fill = [col for col in origin_my_data.columns if col != '날짜']

    # 선택된 컬럼들만 평균으로 결측치 채우기
    origin_my_data[cols_to_fill] = origin_my_data[cols_to_fill].fillna(origin_my_data[cols_to_fill].mean())

    print(origin_my_data.isna().sum())
    # for i in origin_my_data:
    #     if i == '날짜':
    #         pass
    #     else:
    #         origin_my_data.fillna(origin_my_data[i].mean())



window = tkinter.Tk()
window.title("test")
window.geometry("700x500")
tree=ttk.Treeview(window)
tree.pack(fill = 'both', expand=1)

openbutton = tkinter.Button(window, text="csv 파일 열기", command=load_csv)
openbutton.pack()

# 이상치 처리 버튼
outlierbutton = tkinter.Button(window, text="이상치 처리",command=handle_missing_value)
outlierbutton.pack()

jagerbutton = tkinter.Button(window, text="결측치 처리",command=jager)
jagerbutton.pack()


savebutton = tkinter.Button(window, text="csv 파일 저장")
savebutton.pack()

window.mainloop()

