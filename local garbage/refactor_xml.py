import xml.etree.ElementTree as ET
import tkinter as tk
from itertools import chain

from functions import read_xml

tree = ET.parse('reštaurácia_varenie.xml')
root = tree.getroot()

dict_roles = {}
dict_places = {}
dict_transitions = {}

places, transitions, arcs, roles = read_xml("reštaurácia_varenie.xml",0)

j = 0
for i in roles:
    dict_roles[j] = i.name
    j += 1
res1 = list(set(chain.from_iterable(sub.values() for sub in [dict_roles])))
print(res1)

j = 0
for i in places:
    dict_places[j] = i.name, i.tokens
    j += 1
res2 = list(set(chain.from_iterable(sub.values() for sub in [dict_places])))
print(res2)

j = 0
for i in transitions:
    dict_transitions[j] = i.name, i.label
    j += 1
res3 = list(set(chain.from_iterable(sub.values() for sub in [dict_transitions])))
print(res3)

k = 0
for rank in root.iter('place'):
    for i in rank:
        dict_places[k] = i.text
        k += 1
res4 = list(set(chain.from_iterable(sub.values() for sub in [dict_places])))


dict_transitions = {}
l = 0
for rank in root.iter('transition'):
    for i in rank:
        dict_transitions[l] = i.text
        l += 1
res = list(set(chain.from_iterable(sub.values() for sub in [dict_transitions])))

win = tk.Tk()
win.geometry("600x400")
name_var = tk.StringVar()


def submit():
    name = name_var.get()
    print("The name is : " + name)


name_label = tk.Label(win, text='Role', font=('calibre', 10, 'bold'))
name_label.grid(row=0, column=0)
p = 0
for i in res1:
    name_label = tk.Label(win, text=i, font=('calibre', 10, 'bold'))
    #name_entry = tk.Entry(win, textvariable=name_var, font=('calibre', 10, 'normal'))
    #name_entry.grid(row=p, column=2)
    #sub_btn = tk.Button(win, text='Submit', command=submit)
    #sub_btn.grid(row=p, column=3)
    name_label.grid(row=p, column=1)
    p += 1
j=p
name_label = tk.Label(win, text='Miesta', font=('calibre', 10, 'bold'))
name_label.grid(row=j, column=0)

for i in res2:
    name_label = tk.Label(win, text=i, font=('calibre', 10, 'bold'))
    #name_entry = tk.Entry(win, textvariable=name_var, font=('calibre', 10, 'normal'))
    #name_entry.grid(row=p, column=2)
    #sub_btn = tk.Button(win, text='Submit', command=submit)
    #sub_btn.grid(row=p, column=3)
    name_label.grid(row=j, column=1)
    j += 1
l = j
name_label = tk.Label(win, text='Prechody', font=('calibre', 10, 'bold'))
name_label.grid(row=l, column=0)

for i in res3:
    name_label = tk.Label(win, text=i, font=('calibre', 10, 'bold'))
    #name_entry = tk.Entry(win, textvariable=name_var, font=('calibre', 10, 'normal'))
    #name_entry.grid(row=p, column=2)
    #sub_btn = tk.Button(win, text='Submit', command=submit)
    #sub_btn.grid(row=p, column=3)
    name_label.grid(row=l, column=1)
    l += 1
z = l

name_label = tk.Label(win, text='Hrany', font=('calibre', 10, 'bold'))
name_label.grid(row=2, column=1)

"""
p = 4
for i in res:
    name_label = tk.Label(win, text=i, font=('calibre', 10, 'bold'))
    #name_entry = tk.Entry(win, textvariable=name_var, font=('calibre', 10, 'normal'))
    #name_entry.grid(row=p, column=2)
    #sub_btn = tk.Button(win, text='Submit', command=submit)
    #sub_btn.grid(row=p, column=3)
    name_label.grid(row=p, column=1)
    p += 1
"""
win.mainloop()

for rank in root.iter('role'):
    for i in rank:
        if i.text == 'Čašník':
            i.text = str(name_var.get())

tree.write('output.xml', encoding="UTF-8", xml_declaration=True)
