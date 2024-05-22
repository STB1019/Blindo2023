from tkinter import *
import UtilityView as uv
import os
import StaticParameter as SP


class ImportExportView:

    # schermata che permette di importare ed esportare i file da/su chiavetta
    def import_export(path_punto_accesso_chiavette, path_che_simula_la_memoria_interna_del_raspberry):
        root = Tk()
        root.attributes('-fullscreen', SP.full_screen_option)
        root.config(bg=SP.standard_color_setting("root_import_export_view"))

        frame = Frame(root)
        frame.config(bg=SP.standard_color_setting("frame_import_export_view"))
        frame.pack()

        label = Label(frame, text="Scegli l'azione desiderata",
                      bg=SP.standard_color_setting("label_import_export_view"),
                      width=90, height=3,
                      font=SP.font_medium,
                      fg=SP.root_font_color
                      )
        label.pack();

        # numbers_of_key is the number of connected key
        numbers_of_key = len(os.listdir(path_punto_accesso_chiavette))

        # le funzioni IMPORTA/ESPORTA vengono visualizzate
        # solamente se è collegata almeno una chiavetta
        if numbers_of_key > 0:
            import_button = Button(frame,
                                   text="Importa",
                                   bg=SP.standard_color_setting("import_button_background"),
                                   command=lambda: choose_key_and_import(root),
                                   font=SP.font_small,
                                   fg=SP.button_font_color_gray_scale,
                                   bd=SP.bord_size,
                                   relief=SP.bord_style,
                                   activebackground=SP.standard_color_setting("import_button_background")
                                   )
            import_button.pack(side=LEFT)
            import_button.config(height=5, width=22)

            export_button = Button(frame,
                                   text="Esporta",
                                   bg=SP.standard_color_setting("export_button_background"),
                                   command=lambda: choose_key_and_export(root),
                                   font=SP.font_small,
                                   fg=SP.button_font_color_gray_scale,
                                   bd=SP.bord_size,
                                   relief=SP.bord_style,
                                   activebackground=SP.standard_color_setting("export_button_background")
                                   )
            export_button.pack(side=RIGHT)
            export_button.config(height=5, width=22)

        else:
            # cambio il contenuto e la grandezza del label
            label["text"] = "Inserisci una chiavetta \nper accedere alle altre funzionalità"
            label["height"] = 3
            '''
            # pulsante mostrato solo se NON è inserita nessuna chiavetta
            raspberry_memory_button = Button(frame,
                                             text="Accedi alla memoria interna",
                                             bg=SP.standard_color_setting("button_import_export_view"),
                                             command=lambda: uv.raspberry_memory_manager(),
                                             font=SP.font_piccolo,
                                             fg=SP.button_font_color_gray_scale,
                                             bd=SP.bord_size,
                                             relief=SP.bord_style,
                                             activebackground=SP.standard_color_setting("button_import_export_view")
                                             )
            raspberry_memory_button.pack()
            raspberry_memory_button.config(height=5, width=25)
            '''
        #    funzione che richiama la sottoschermata dopo aver cliccato su "ESPORTA"
        def choose_key_and_export(cl_root):

            root = Tk()
            root.attributes('-fullscreen', SP.full_screen_option)
            root.config(bg=SP.standard_color_setting("root_import_export_view"))

            frame = Frame(root, bg=SP.standard_color_setting("frame_import_export_view"))
            frame.pack()

            # passo alla funzione pi\media e quindi verranno visualizzate a schermo le chiavette disponibili
            dirs = os.listdir(path_punto_accesso_chiavette)

            label = Label(frame,
                          text="Selezionare la chiavetta su cui esportare i file audio",
                          bd=20,
                          bg=SP.standard_color_setting("label_import_export_view"),
                          font=SP.font_small,
                          fg=SP.root_font_color)
            label.grid(row=1, column=0)
            label.config(width=50, height=4)

            # index necessario all' incolonnamento dei pulsanti, utilizzato in pulsante.grid() qualche riga sotto
            index = 2
            # ciclo che stampa tante "chiavette" quante inserite nel device
            for cartella in dirs:
                path_chiavetta = os.path.join(path_punto_accesso_chiavette, cartella)
                pulsante = uv.button_usb_key(frame, "esportare", cartella,
                                             path_che_simula_la_memoria_interna_del_raspberry, path_chiavetta,root)
                pulsante.grid(row=index, column=0)
                index += 1

            uv.exit_button_with_text(root, SP.exit_text)
            cl_root.destroy()
            root.mainloop()

        #    funzione che richiama la sottoschermata dopo aver cliccato su "IMPORTA"
        def choose_key_and_import(cl_root):

            root = Tk()
            root.attributes('-fullscreen', SP.full_screen_option)
            root.config(bg=SP.standard_color_setting("root_import_export_view"))

            frame = Frame(root, bg=SP.standard_color_setting("frame_import_export_view"))
            frame.pack()

            # passo alla funzione pi\media e quindi verranno visualizzate a schermo le chiavette disponibili
            dirs = os.listdir(path_punto_accesso_chiavette)

            label = Label(frame, text="Selezionare la chiavetta da cui importare i file audio",
                          bd=20,
                          bg=SP.standard_color_setting("label_import_export_view"),
                          font=SP.font_small,
                          fg=SP.root_font_color)
            label.grid(row=1, column=0)
            label.config(width=50, height=4)

            # index necessario a posizionare il pulsante sulla schermata (indice della riga del pulsante)
            index = 2
            # ciclo che stampa tante "chiavette" quante inserite nel device
            for cartella in dirs:
                path_chiavetta = os.path.join(path_punto_accesso_chiavette, cartella)
                pulsante = uv.button_usb_key(frame,
                                             "importare",
                                             cartella,
                                             path_chiavetta,
                                             path_che_simula_la_memoria_interna_del_raspberry,root)
                pulsante.grid(row=index, column=0)
                index += 1

            uv.exit_button_with_text(root, SP.exit_text)
            cl_root.destroy()
            root.mainloop()

        uv.exit_button_with_text(root, SP.exit_text)
        root.mainloop()