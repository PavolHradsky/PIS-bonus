from typing import List

from PetriNet import PetriNet
from functions import read_xml
from Rpn import Rpn
import tkinter as tk



def main():
    # places, transitions, arcs = read_xml(input("file name: "))
    places, transitions, arcs = read_xml("test.xml")
    net: PetriNet = PetriNet(places, transitions, arcs)

    M: List[Rpn] = []
    H: List = []

    M.append(Rpn(net.M0))

    for m in M:
        if not m.visited:
            for t in net.T:
                if net.step(t, m.state) is not None:
                    new_m = net.step(t, m.state)
                    if new_m not in [a.state for a in M]:
                        M.append(Rpn(new_m))
                    H.append((m.state, t, new_m))
            m.visited = True


    for m in M:
        print(m.state)
    for h in H:
        print(h[0], h[1].name, h[2])

    master = tk.Tk()
    canvas = tk.Canvas(master, width=400, height=400, bg='white')
    canvas.pack()

    x = 100
    y = 100

    M_coords = []
    for i, m in enumerate(M):
        canvas.create_text(x, y, text=str(m.state))
        M_coords.append((x, y))
        y += 50
        if i == len(M)//2-1:
            x = 250
            y = 100

    for h in H:
        x1, y1 = M_coords[[m.state for m in M].index(h[0])]
        x2, y2 = M_coords[[m.state for m in M].index(h[2])]
        canvas.create_line(x1, y1, x2, y2, arrow=tk.LAST)
        canvas.create_text(x1+(x2-x1)/2, y1+(y2-y1)/2, text=str(h[1].name), fill="green", font='Arial 20')

    tk.mainloop()


if __name__ == '__main__':
    main()
