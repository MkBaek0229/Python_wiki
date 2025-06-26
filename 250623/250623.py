""" ttk.Treeview 활용 tkinter 안에 csv 파일 직접 읽어오기 """
import tkinter
from tkinter import ttk
import csv
from tkinter import filedialog
import customtkinter

import pandas as pd
import numpy as np



# todo 이상치 결측치 누르면 나오는 결과값
origin_my_data = pd.DataFrame()

# todo 처음에 불러오는거
historyData = pd.DataFrame()

# todo 드롭박스 필터링 기능을 위한 카피본
historyData_copy = pd.DataFrame()

# todo 파일 경로 저장하는거
file_path = ""

# todo 어느상황에서 tree를 그리는지 상황별로 코드값 부여
RENDER_FIRST = 101
RENDER_REPLAY = 102
RENDER_RESET = 103
RENDER_FILTER = 104


combobox = None
value_choice = None

# todo ############
sort_value = {}

# todo 헤더 누르면 정렬(내림차순, 오름차순)
def sort_head(val):
    global historyData
    # sort_value.clear()

    # ascending에 넣을 속성 값을 처음 클릭시에는 오름차순으로
    res = sort_value.get(val, True)

    # todo ########## by= "정렬 기준이 되는 헤더"
    historyData = historyData.sort_values(by=val,ascending=res)
    sort_value[val] = not res

    load_csv(RENDER_REPLAY)


#todo tree 그리는 함수
def draw_tree(df):
        # 전개연산자 *로 tree.get.childeren()의 값들 요소로 분리.
        tree.delete(*tree.get_children())
        tree['columns'] = tuple(df.columns)
        tree['show'] = 'headings'
        for col in df.columns:
            tree.heading(col, text=col, command=lambda x=col : sort_head(x))
            tree.column(col, width=100, anchor='center')
        for row in df.values:
            tree.insert('', 'end', values=list(row))



# todo 데이터 불러오는 함수
def load_csv(code):
    global historyData
    global origin_my_data
    global file_path

    if code == RENDER_FIRST:
        file_path = filedialog.askopenfilename(
                title="CSV 파일 선택",
                filetypes=[("CSV files","*csv")]
        )
        if file_path:
            window.title(file_path)
            origin_my_data = pd.read_csv(file_path)
            historyData = origin_my_data.copy()
            draw_tree(origin_my_data)
            combobox['values'] = list(origin_my_data.columns)

    elif code == RENDER_RESET:
        historyData = origin_my_data.copy()
        draw_tree(origin_my_data)

    elif code == RENDER_REPLAY:
        draw_tree(historyData)

    elif code == RENDER_FILTER:
        draw_tree(historyData_copy)


# todo 이상치 처리 함수
def handle_missing_value():
    global historyData

    for i, j in historyData.items():
        for e in j:
            if i == '날짜':
                pass
            elif pd.isna(e):
                e = 0.0
                pct25 = historyData[i].quantile(.25)
                pct75 = historyData[i].quantile(.75)
                iqr = pct75 - pct25
                historyData[i] = np.where((historyData[i] < (pct25 - 1.5 * iqr)) | (historyData[i] > (pct75 + 1.5 * iqr)), np.nan,
                                    historyData[i])

    print(historyData.isna().sum())

    load_csv(RENDER_REPLAY)



# todo 결측치 제거
def jager():
    global historyData

    # 날짜 컬럼 제외한 컬럼 리스트
    cols_to_fill = [col for col in historyData.columns if col != '날짜']

    # 선택된 컬럼들만 평균으로 결측치 채우기
    historyData[cols_to_fill] = historyData[cols_to_fill].fillna(historyData[cols_to_fill].mean())

    print(historyData.isna().sum())

    load_csv(RENDER_REPLAY)


# todo. 파일 데이터의 shape및 동계 요약 출력 버튼
def ssum():
    global origin_my_data
    global historyData

    # 통계 요약 및 전치
    desc = historyData.describe().transpose()

    # 인덱스를 컬럼으로 변경
    desc.reset_index(inplace=True)

    # index라는 컬럼명을 '통계기준' 등으로 변경하면 더 명확
    desc.rename(columns={'index': '통계'}, inplace=True)

    # Treeview 렌더링용으로 전달
    historyData = desc

    # 전달된 Tree뷰를 다시 렌더링 요청
    load_csv(RENDER_REPLAY)


# todo 드롭다운 메뉴 선택
def dropdown_control(e):
    global historyData
    global historyData_copy
    # DataFrame의 형태는 사용시 2차원 데이터
    historyData_copy = historyData.copy()
    historyData_copy = historyData[[e]]
    load_csv(RENDER_FILTER)

# todo 검색 기능 함수
def searching():
    keyword = entry_1.get().strip()
    if keyword == "" or keyword == "Enter text here...":
        return  # 아무것도 입력하지 않으면 종료

    global historyData

    # 키워드가 포함된 행만 필터링 (부분 일치)
    matched_df = historyData[[keyword in ' '.join(map(str, row)) for row in historyData.values]]

    # 결과 렌더링
    draw_tree(matched_df)


def save():
    global historyData

    file_path = filedialog.asksaveasfilename(
        defaultextension='*.csv',
        title="CSV 파일로 저장",
        filetypes=[("CSV files", "*.csv")]
    )
    if file_path:
        try:
            historyData.to_csv(file_path, index=False)
            print("성공", f"{file_path} 파일로 저장되었습니다.")
        except Exception as e:
            print("오류", f"파일 저장 중 오류 발생:\n{e}")


window = tkinter.Tk()
window.title("main")
window.geometry("1280x846")


tree=ttk.Treeview(window)
tree.pack(fill = 'both', expand=1 , side='bottom')





# 드롭다운 메뉴에 표시될 값 목록
values = []

value_choice = tkinter.StringVar(window)



# 콤보박스 생성
combobox = ttk.Combobox(window, textvariable=value_choice, values=values)
combobox.pack(padx=20, pady=20)
# combobox.bind("<<ComboboxSelected>>", lambda event: print(origin_my_data[value_choice.get()]))
combobox.bind("<<ComboboxSelected>>", lambda event : dropdown_control(value_choice.get()))





# todo place holder를 위한 함수
def on_focus_in(event):
    if entry_1.get() == "특정셀의 값 검색":
        entry_1.delete(0, tkinter.END)
        entry_1.config(fg="black")

def on_focus_out(event):
    if entry_1.get() == "":
        entry_1.insert(0, "특정셀의 값 검색")
        entry_1.config(fg="gray")



# todo 검색 버튼
searchbutton = tkinter.Button(window, text="검색", command=searching, bg='blue', fg='white')
searchbutton.pack(side=tkinter.RIGHT, padx=5, ipadx=10)


# todo 검색 입력창 위젯 생성
entry_1 = tkinter.Entry(window, width=20,fg='gray')
entry_1.insert(0, "특정셀의 값 검색")
entry_1.pack(side=tkinter.RIGHT,  padx=3 , ipady=5)

entry_1.bind("<FocusIn>", on_focus_in)
entry_1.bind("<FocusOut>", on_focus_out)




# todo 버튼 목록들
openbutton = tkinter.Button(window, text="csv 파일 열기", command=lambda :load_csv(RENDER_FIRST),  bg='blue', fg='white')
openbutton.pack(side=tkinter.LEFT)

outlierbutton = tkinter.Button(window, text="이상치 처리",command=handle_missing_value, bg='blue',fg='white')
outlierbutton.pack(side=tkinter.LEFT)

jagerbutton = tkinter.Button(window, text="결측치 처리",command=jager, bg='blue',fg='white')
jagerbutton.pack(side=tkinter.LEFT)


savebutton = tkinter.Button(window, text="csv 파일 저장", command=save, bg='blue', fg='white')
savebutton.pack(side=tkinter.LEFT)

shapebutton = tkinter.Button(window, text="통계 출력", command=ssum , bg='blue', fg='white')
shapebutton.pack(side=tkinter.LEFT)


resetbutton = tkinter.Button(window, text="처음으로",command=lambda :load_csv(RENDER_RESET), bg='blue', fg='white')
resetbutton.pack(side=tkinter.LEFT)





window.mainloop()
