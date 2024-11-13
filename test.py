from tkinter import *
from tkinter import messagebox

root = Tk()
root.title('LUAN DEP TRAI')

def Tiep():
    a.set("")
    b.set("")
    X.set("")

def Giai():
    a_value = float(a.get())
    b_value = float(b.get())
    if a_value == 0:
        if b_value == 0:
            x.set("Phương trình vô số nghiệm")
        else:
            x.set("Phương trình vô nghiệm")
    else:
        result = -b_value / a_value
        x.set(f"x = {result:.2f}")

a = StringVar()
b = StringVar()
x = StringVar()

Label(root, text='Phương trình Bậc 1', justify=CENTER, foreground='red').grid(row=0, columnspan=2)

Label(root, text='Hệ số a: ', justify=LEFT).grid(row=1, column=0)
Entry(root, textvariable=a).grid(row=1, column=1)

Label(root, text='Hệ số b: ', justify=LEFT).grid(row=2, column=0)
Entry(root, textvariable=b).grid(row=2, column=1)

Label(root, text='Hệ số c: ', justify=LEFT).grid(row=2, column=0)
Entry(root, textvariable=b).grid(row=3, column=1)

frame = Frame(root) 

Button(frame, text='Giải', command=Giai).pack(side=LEFT)
Button(frame, text='Tiếp', command=Tiep).pack(side=LEFT)
Button(frame, text='Thoát', command=root.quit).pack(side=LEFT)

frame.grid(row=4, columnspan=2)

Label(root, text='Kết quả: ', justify=LEFT).grid(row=5, column=0)
Entry(root, textvariable=x ).grid(row=5, column=1)

root.mainloop()