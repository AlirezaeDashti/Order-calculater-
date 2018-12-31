
import time
import requests
import json
from tkinter import *
from tkinter import messagebox


class Compiler:
    def __init__(self, user_input):
        self.url = "https://api.jdoodle.com/v1/execute"
        self.headers = {'Content-type': 'application/json'}
        self.payload = {"clientId": "561d4b78be8ac77f9711aa827bb661c6",
                        "clientSecret": "5cadd43a0f7f4c187f428be50af70ef6bba434db749975e21598cbd4b01e2139",
                        "script": """{}""".format(user_input),
                        "language": "c",
                        "versionIndex": "0",
                        }
        self.response = requests.post(url=self.url, data=json.dumps(self.payload), headers=self.headers)
        self.pyresponse = self.response.json()
        if self.response.status_code != 200:
            print(f"Problem in compiler API, StatusCode: {self.response.status_code}")
            print(f"response: {self.pyresponse}")


class DcodeFR:
    def __init__(self, points):
        self.url = "https://www.dcode.fr/api/"
        self.headers = {'Content-type': 'application/x-www-form-urlencoded'}
        self.payload = {"tool": "lagrange-interpolating-polynomial",
                        "points": f"{points}"
                        }

        self.response = requests.post(url=self.url, data=self.payload, headers=self.headers)
        self.output = self.response.json()
        if self.response.status_code != 200:
            print(f"Problem in DCODE.FR API, StatusCode: {self.response.status_code}")
            print(f"response: {self.pyresponse}")
        # print("\n")
        # print("test output: {}".format(self.output['results']))


def compiler(source):
    compiler_req = Compiler(source)
    return compiler_req.pyresponse['output']


def point_finder(source, N):
    final_source = "\n#include<stdio.h>" + "\n" + "#define N {}\n".format(N) + source
  
    output = compiler(final_source) 

    tup = (N, len(output))
    return tup




def equation_finder(usr_src):
    points = ""
    for N in range(0, 10, 2):
        points += str(point_finder(usr_src, N))

    print("final points are: {}".format(points))
    equation_req = DcodeFR(points)
    equation = equation_req.output['results']
    print(f"Equation: {equation.strip('$$')}")
    bigo = "O(n"
    for i, letter in enumerate(equation):
        if letter == 'x' and equation[i + 1] == "^":
            bigo += equation[i + 1:i + 3] + ")"
            break
    else:
        bigo += ")"
    print(f"Complexity: {bigo}")
    return bigo


# GUI
def raise_frame(frame):
    frame.tkraise()


root = Tk()
root.title("ORDER Calculator")
root.geometry('700x700')
root.resizable(False, False)

f1 = Frame(root)
f2 = Frame(root)
f3 = Frame(root)

for frame in (f1, f2, f3):
    frame.grid(row=0, column=0, sticky='news')

#f1
photo = PhotoImage(file="main.png")
Label(f1, image=photo).place(x=0, y=0)
Button(f1, text='           Calculation          ', bg="white", fg="black", command=lambda: raise_frame(f2)).place(
    x=280, y=580)


def f3_handle():
    root.geometry('817x720')
    raise_frame(f3)


Button(f1, text='          Comparison          ', bg="white", fg="black", command=f3_handle).place(x=280,
                                                                                                   y=620)

#f2
photo2 = PhotoImage(file="shana.png")  
Label(f2, image=photo).place(x=0, y=0)

f2entry = Text(f2, bg="white", fg="black", height=30, width=65)
f2entry.place(x=85, y=30)

scrollbar = Scrollbar(f2, command=f2entry.yview)
scrollbar.place(x=591, y=31)
f2entry['yscrollcommand'] = scrollbar.set


def calc_handle():
    user_input = f2entry.get("1.0", "end-1c")
    complexity = equation_finder(user_input)
    messagebox.showinfo("Successfully calculated", "Complexity: {}".format(complexity))


btn = Button(f2, text="Calculate", bg="white", fg="black", command=calc_handle).place(x=320, y=580)

#f3
photo2 = PhotoImage(file="fram23.png")

Label(f3, image=photo2).place(x=0, y=0, relwidth=1, relheight=1)
f3entry = Text(f3, bg="white", fg="black", height=40, width=50)
f3entry.insert(END, "int main()"
                    "\n{"
                    "\n"
                    "\n"
                    "\treturn 0;"
                    "\n}")
f3entry.grid(column=1, row=1)

lbl = Label(f3, bg="white", fg="black", text="  ")
lbl.grid(column=2, row=1)

f3entry2 = Text(f3, bg="white", fg="black", height=40, width=50)
f3entry2.insert(END, "int main()"
                     "\n{"
                     "\n"
                     "\n"
                     "\treturn 0;"
                     "\n}")
f3entry2.grid(column=3, row=1)


def compare_handle():
    src1 = f3entry.get("1.0", "end-1c")
    src2 = f3entry2.get("1.0", "end-1c")
    complexity1 = equation_finder(src1)
    complexity2 = equation_finder(src2)

    if complexity1 > complexity2:
        better = "Second"
    elif complexity1 < complexity2:
        better = "First"
    else:
        better = "There is no idea which"
    messagebox.showinfo("Successfully Compared ", "{} algorithm is better.".format(better))


compare_btn = Button(f3,
                     text="                                                  Compare"
                          "                                               ",
                     bg="white", fg="black", command=compare_handle)
compare_btn.grid(row=3, columnspan=4)

# RUN GUI
raise_frame(f1)
root.mainloop()
