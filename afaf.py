
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