from tkinter import *
import UtilityView as uv
from StaticParameter import Setting as SP


class AssociateView:

    # Schermata che appare dopo aver cliccato su ASSOCIA nel MENU PRINCIPALE
    def schermata_pulsanti(closingroot, number_of_button):

        closingroot.quit()
        root = Tk()
        root.attributes('-fullscreen', True)

        frame = Frame(root)

        text = Text(frame, wrap="none", bg=SP.root_background_color)
        vsb = Scrollbar(frame, orient="vertical", command=text.yview,width=40)
        vsb.config(width=90)
        text.configure(yscrollcommand=vsb.set, width=3, bg=SP.root_background_color)
        vsb.pack(side="left", fill="y")
        text.pack(side="left", fill="both", expand=True)

        pulstante_uscita = Button(frame,
                                  text="Menu principale",
                                  command=lambda: root.destroy(),
                                  bd=SP.bord_size,
                                  relief=SP.bord_style,
                                  bg=SP.button_background_color,
                                  font=SP.font_small,
                                  fg=SP.button_font_color,
                                  activebackground=SP.active_background_color)
        pulstante_uscita.config(height=50, width=18)

        #  ciclo che crea "number_of_button" pulsanti
        for i in range(number_of_button):
            pulsante = uv.bottom_with_text(frame, "Pulsante " + str(i + 1))
            pulsante.pack(side=TOP, fill=BOTH)
            text.window_create("end", window=pulsante)
            text.insert("end", "\n")

        text.configure(state="disabled")
        frame.pack(fill="both", expand=True)
        pulstante_uscita.pack(side=RIGHT, fill=BOTH)
        root.mainloop()

