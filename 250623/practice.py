""" ttk.Treeview 활용 tkinter 안에 csv 파일 직접 읽어오기 """
import tkinter
from distutils.dist import command_re
from tkinter import ttk
import csv
from tkinter import filedialog
import pandas as pd
import numpy as np

# todo 이상치 결측치 누르면 나오는 결과값
origin_my_data = pd.DataFrame()

# todo 처음에 불러오는거
historyData = pd.DataFrame()

# todo 파일 경로 저장하는거
file_path = ""

combobox = None
value_choice = None

# todo ############
sort_value = {}

# todo ############ 헤더 누르면 정렬(내림차순, 오름차순)
def sort_head(val):
    global historyData
    # sort_value.clear()
    res = sort_value.get(val, True)
    # todo ########## by= "정렬 기준이 되는 헤더"
    historyData = historyData.sort_values(by=val,ascending=res)
    sort_value[val] = not res
    rerender()




# todo 데이터 불러오는 함수
def load_csv():
    global historyData
    global origin_my_data
    global file_path
    global value_choice
    global combobox


    file_path = filedialog.askopenfilename(
            title="CSV 파일 선택",
            filetypes=[("CSV files","*csv")]
    )
    print(file_path)

    if file_path:
        with open(file_path, newline='',encoding='utf-8') as csvfile:
            origin_my_data = pd.read_csv(csvfile)
            # 원본 복사 histroyData
            historyData = origin_my_data
            # reader = csv.reader(csvfile)

            # headers=next(reader) # csv.reader 함수로 csv파일 객체 읽음.
            #
            tree['columns'] = tuple(origin_my_data.columns)
            tree['show'] = 'headings'

            for col in origin_my_data.columns:
                # todo ############## 헤더클릭 시 동작추가
                tree.heading(col, text=col, command = lambda x=col : sort_head(x))
                tree.column(col, width=100, anchor='center')

            #for row in origin_my_data.values:
                # tree.insert('', 'end', values=list(row))
                # historyData.append(list(row))
            for row in origin_my_data.values:
                tree.insert('', 'end', values=list(row))

            values = list(origin_my_data.columns)
            combobox['values'] = values
            value_choice.set(values[0])  # 첫 번째 컬럼으로 선택값 초기화






# todo 데이터 지우고 새롭게 그려 주는 함수
def rerender():
    tree.delete(*tree.get_children())

    tree['columns'] = tuple(historyData.columns)
    tree['show'] = 'headings'

    for col in historyData.columns:
        # todo ############## 헤더클릭 시 동작추가
        tree.heading(col, text=col, command = lambda x=col : sort_head(x))
        tree.column(col, width=100, anchor='center')

    for row in historyData.values:
        tree.insert('', 'end', values=list(row))

# todo 드롭다운 필터링 전용 새롭게 그리는 함수
# def rerender(ip):
#     global origin_my_data
#     tree.delete(*tree.get_children())
#
#     origin_my_data = origin_my_data[ip]
#
#     tree['columns'] = tuple(origin_my_data.columns)
#     tree['show'] = 'headings'
#
#     for col in origin_my_data.columns:
#         tree.heading(col, text=col)
#         tree.column(col, width=100, anchor='center')
#
#     for row in origin_my_data.values:
#         tree.insert('', 'end', values=list(row))


# todo 이상치 처리 함수
def handle_missing_value():
    global historyData

    for i, j in historyData.items():
        # tree['columns'] = i
        # tree['show'] = 'headings'
        # tree.heading(i, text=i)
        # tree.column(i, width=100, anchor='center')
        # tree.insert('', 'end', values=j)
        # historyData.append(j)
        for e in j:
            if i == ['날짜']:
                pass
            elif pd.isna(e):
                e = 0.0
                pct25 = historyData[i].quantile(.25)
                pct75 = historyData[i].quantile(.75)
                iqr = pct75 - pct25
                historyData[i] = np.where((historyData[i] < (pct25 - 1.5 * iqr)) | (historyData[i] > (pct75 + 1.5 * iqr)), np.nan,
                                    historyData[i])

    print(historyData.isna().sum())

    # reader = csv.reader(csvfile)

    # headers=next(reader) # csv.reader 함수로 csv파일 객체 읽음.
    rerender()



# todo 결측치 제거
def jager():
    global historyData

    #  -- 기존 방식 -- 안되서 수정
    # for i in origin_my_data:
    #     if i == '날짜':
    #         pass
    #     else:
    #         origin_my_data.fillna(origin_my_data[i].mean())

    # 날짜 컬럼 제외한 컬럼 리스트
    cols_to_fill = [col for col in historyData.columns if col != '날짜']

    # 선택된 컬럼들만 평균으로 결측치 채우기
    historyData[cols_to_fill] = historyData[cols_to_fill].fillna(historyData[cols_to_fill].mean())

    print(historyData.isna().sum())

    rerender()


# todo. 파일 데이터의 shape및 동계 요약 출력 버튼
def stasum():
    global origin_my_data
    global historyData
    print(historyData.shape)
    historyData = origin_my_data.describe()
    rerender()

window = tkinter.Tk()
window.title("test")
window.geometry("1280x846")


tree=ttk.Treeview(window)
tree.pack(fill = 'both', expand=1 , side='bottom')

# 드롭다운 메뉴에 표시될 값 목록
values = []

value_choice = tkinter.StringVar(window)



# 콤보박스 생성
combobox = ttk.Combobox(window, textvariable=value_choice, values=values)
combobox.pack(padx=20, pady=20)
combobox.bind("<<ComboboxSelected>>", lambda event: print(origin_my_data[value_choice.get()]))





# todo place holder를 위한 함수
def on_focus_in(event):
    if entry_1.get() == "Enter text here...":
        entry_1.delete(0, tkinter.END)
        entry_1.config(fg="black") # Change text color to black

def on_focus_out(event):
    if entry_1.get() == "":
        entry_1.insert(0, "Enter text here...")
        entry_1.config(fg="gray") # Change text color to gray

def searching():
    print(entry_1.get())

entry_frame = tkinter.Frame(window)
entry_frame.pack(pady=10, padx=10, side=tkinter.TOP)

entry_1 = tkinter.Entry(entry_frame, width=20,fg='gray')
entry_1.insert(0, "Enter text here...")
entry_1.pack(side=tkinter.LEFT, padx=5)

entry_1.bind("<FocusIn>", on_focus_in)
entry_1.bind("<FocusOut>", on_focus_out)




# todo 버튼 목록들
openbutton = tkinter.Button(window, text="csv 파일 열기", command=load_csv, bg='blue', fg='white')
openbutton.pack(side=tkinter.LEFT)

outlierbutton = tkinter.Button(window, text="이상치 처리",command=handle_missing_value, bg='blue',fg='white')
outlierbutton.pack(side=tkinter.LEFT)

jagerbutton = tkinter.Button(window, text="결측치 처리",command=jager, bg='blue',fg='white')
jagerbutton.pack(side=tkinter.LEFT)


savebutton = tkinter.Button(window, text="csv 파일 저장")
savebutton.pack(side=tkinter.LEFT)

shapebutton = tkinter.Button(window, text="통계 출력", command=stasum , bg='blue', fg='white')
shapebutton.pack(side=tkinter.LEFT)

searchbutton = tkinter.Button(window, text="검색", command=searching)
searchbutton.pack(side=tkinter.LEFT)

resetbutton = tkinter.Button(window, text="처음으로",command=load_csv)
resetbutton.pack(side=tkinter.LEFT)





window.mainloop()
