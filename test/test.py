# 유형 테스트 진행 -> 결과를 csv로 저장한다. -> csv로 유형분포도 그래프를 그려본다.
# 유형 테스트는 과일의 진화 정도 테스트를 확인한다.

import tkinter as tk
import tkinter.font
import questionlist as q

print(q.question_list)



window = tkinter.Tk()
window.geometry('300x300')

font = tk.font.Font(size=24, weight="bold")
font2 = tk.font.Font(size=12, weight="normal")
font3 = tk.font.Font(size=14, weight="bold")

state = {"now_pack_list": [], "current": 0,
         "check_list": [], "var":None}



def print_list():
    question = tk.Label(window, text=f"{q.question_list[state['current']]['question']} ")
    question.pack()

def handle_next():
    selected_value = state["var"].get()
    state["check_list"].append(selected_value)
    print(f"값을 추가 하였음 : {state['check_list']}")

    if state["current"] < len(q.question_list) - 1:
        state["current"] += 1
    else:
        print(f"설문 완료 : {state['check_list']}")





def start():
    global state
    for pl in state["now_pack_list"]:
        pl.pack_forget()

    state['var']= tkinter.StringVar()

    for option_value in q.question_list[state['current']]['options']:
        tkinter.Radiobutton(
            window,
            text=f'{option_value}',
            value=f"{option_value}",
            variable=state["var"]
        ).pack()

    check_button = tkinter.Button(window, text="선택 확인" , command=handle_next)
    check_button.pack()



header = tk.Label(window, text="에겐,테토 테스트", font=font)
header.pack()
state["now_pack_list"].append(header)

dsc = tk.Label(window, text=f"나의 성향을 알아 보아요", font=font2)
dsc.pack()
state["now_pack_list"].append(dsc)

StartButton = tkinter.Button(window, text='시작', bg='yellow', font=font3, padx=10, pady=1, command=start)
StartButton.pack()
state["now_pack_list"].append(StartButton)

window.mainloop()