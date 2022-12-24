from clean import __extmain__ as input_string
from tkinter import *
from tkinter import filedialog


def clicked():
    lbl.configure(text='Йде обробка даних...')
    pole = filedialog.askdirectory() 
    input_string(pole)
    
    

window = Tk()
window.title ('Обробка та сортування файлів в папці')
window.geometry('440x50')
txt = Entry(window, width=10)
txt.grid(column=1, row=0)
btn = Button(window, text='Вибір папки для аналізу', bg='yellow', fg='green', command= clicked)
btn.grid(column=0, row=1)
lbl = Label(window, text='Програма готова до роботи')
lbl.grid(column=0, row=0)



window.mainloop()