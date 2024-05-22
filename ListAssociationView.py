from tkinter import *
import pickle as pk
import fileManaging as fm
import UtilityView as uv
import KeyboardView as kv
import StaticParameter as SP
import os
import shutil
from time import sleep


class ListAssociationView:

    #  schermata che appare dopo aver cliccato il pulsante ASSOCIAZIONI nel MENU PRINCIPALE
    def schermata_associazioni():
        # variablile globale
        # in questo modo è più semplice gestire la chiusura di questa schermata
        global root
        root = Tk()
        root.attributes('-fullscreen', SP.full_screen_option)

        root.config(bg=SP.standard_color_setting("root_list_association_view"))

        current_list = fm.name_file
        frame = Frame(root)
        frame.config(bg=SP.standard_color_setting("frame_list_association_view"))

        label_memo = Label(frame, text=current_list,
                           font=SP.font_small,
                           bg=SP.standard_color_setting("label_list_association_view"),
                           fg=SP.root_font_color,
                           bd=20,
                           width=200,
                           height=2)
        label_memo.pack(side=TOP, )
        sorted_list = fm.give_sorted_list()

        my_list = Listbox(root,  # yscrollcommand = scrollbar.set ,
                          name='my_list',
                          font=SP.font_small,
                          fg=SP.root_font_color,
                          width=90,
                          height=8,
                          bg=SP.standard_color_setting("listbox_list_association_view"),
                          activestyle="none")

        for audio in sorted_list:
            my_list.insert(END, audio)

        # my_list.bind('<<ListboxSelect>>', ListAssociationView.drop_menu_list_association)

        frame.pack()
        my_list.pack()
        ListAssociationView.menu_cascata_schermata_associazioni(root)
        uv.exit_button_with_text(root, SP.exit_text)
        root.mainloop()
        # _______________________ end of schermata_associazioni ___________________________

    # funzione che importa automaticamente l'unica lista presente sottoforma di cartella
    # nella cartella "Liste" di blindo
    def auto_import_list():
        # uv.show_dialog_with_time("Attendere\ncaricamento automatico in corso...", 2)
        chiavetta = os.listdir(SP.path_punto_accesso_chiavette)

        # finchè il path adibito all'accoglienza delle chiavette non viene riempito
        # con la usb key collegata, il ciclo previene un errore causato #
        # dalla differenza di velocità tra il comportamento sopracitato #
        # e la velocità dell' event detect che triggera questa funzione
        # l'event detect può essere trovato nel file GPIO mamaging
        while len(chiavetta) == 0:
            chiavetta = os.listdir(SP.path_punto_accesso_chiavette)
            sleep(1)

        path_folder_liste = os.path.join(SP.path_punto_accesso_chiavette,
                                         os.path.join(chiavetta[0], SP.export_folder_name))

        # se non trovo la cartella "Liste" la creo ed esco
        # dalla funzione auto_import perchè non c'è nulla da importare
        if not os.path.exists(path_folder_liste):
            oldmask = os.umask(0o77)
            os.makedirs(path_folder_liste, 0o1411)
            os.umask(oldmask)
            return

        # ulteriore controllo ridondante
        if len(chiavetta) > 0:

            folder_lista = os.listdir(path_folder_liste)

            path_folder_lista = os.path.join(path_folder_liste, folder_lista[0])

            # ciclo che scorre il contenuto della cartella che rappresenta la lista
            # al suo interno esistono sia i file audio
            # che l'oggetto lista
            # ognuno di questi file finisce in un posto diverso all' interno della memoria del raspberry
            for file in os.listdir(path_folder_lista):

                path_file = os.path.join(path_folder_lista, file)

                if file == folder_lista[0]:
                    fm.copy_file_from_path_to_another(path_file, SP.path_liste)

                else:
                    fm.copy_file_from_path_to_another(path_file, SP.path_che_simula_la_memoria_interna_del_raspberry)

            fm.change_list(folder_lista[0])
            # uv.show_dialog_with_time("Lista "+folder_lista[0]+" importata con successo",2)


        else:
            print("nessuna chiavetta inserita")

    '''
    funzione disabilitata 

    def drop_menu_list_association(evt):

        def unbind_and_closing(unbind_root):
            global root
            root.destroy()
            unbind_root.destroy()
            fm.delete_bind(id_button, name_audio)
            ListAssociationView.schermata_associazioni()

        def delete_and_closing(unbind_root):
            global root
            root.destroy()
            unbind_root.destroy()
            uv.elimina_file_con_conferma(SP.path_che_simula_la_memoria_interna_del_raspberry, name_audio)
            ListAssociationView.schermata_associazioni()

        # Note here that Tkinter passes an event object to onselect()
        w = evt.widget

        index = int(w.curselection()[0])
        value = w.get(index)

        root = Tk()
        root.overrideredirect(True)

        root_width = 140
        root_height = 200

        screen_width = root.winfo_screenwidth()
        screen_height = root.winfo_screenheight()

        # calculate position x and y coordinates
        x = (screen_width / 2) - (root_width / 2)
        y = (screen_height / 2) - (root_height / 2)
        root.geometry('%dx%d+%d+%d' % (root_width, root_height, x, y))

        frame = Frame(root,
                      bg=SP.standard_color_setting("frame_list_association_view"))

        # str(value)[a:b] ritorna la substring con i caratteri
        # str(value)[a:b] ritorna la substring con i caratteri
        # che vanno dalla posizione a(compresa) alla posizione b(esclusa)
        # in questo caso b è la lunghezza stessa di value
        # value si presenta nel formato [Pulsante x --------> nomefile]
        # l'ultimo carattere è \n quindi lo rimuovo, ecco perchè sottraggo 1 a len(str(value))
        name_audio = str(value)[25:len(str(value))-1]
        id_button = int(str(value)[9:11])

        unbind_button = Button(frame,
                               text="Disassocia",
                               height=1, width=8,
                               bg=SP.standard_color_setting("button_list_association_view"),
                               fg=SP.button_font_color_gray_scale,
                               command=lambda: unbind_and_closing(root),
                               font = SP.font_piccolo,
                               relief = SP.bord_style,
                               bd = SP.bord_size,
                               activebackground = SP.active_background_color_gray_scale)

        pulsante_annulla = Button(frame,
                                  text="  Annulla  ",
                                  height=1, width=8,
                                  bg=SP.standard_color_setting("button_list_association_view"),
                                  fg=SP.button_font_color_gray_scale,
                                  command=lambda: root.destroy(),
                                  font=SP.font_piccolo,
                                  relief=SP.bord_style,
                                  bd=SP.bord_size,
                                  activebackground=SP.active_background_color_gray_scale)
        pulsante_elimina = Button(frame,
                                  text="   Elimina   ",
                                  height=1, width=8,
                                  bg=SP.standard_color_setting("button_list_association_view"),
                                  fg=SP.button_font_color_gray_scale,
                                  command=lambda: delete_and_closing(root),
                                  font=SP.font_piccolo,
                                  relief=SP.bord_style,
                                  bd=SP.bord_size,
                                  activebackground=SP.active_background_color_gray_scale)

        orientation=TOP
        unbind_button.pack(side=orientation)
        pulsante_elimina.pack(side=orientation)
        pulsante_annulla.pack(side=orientation)

        frame.pack(fill=BOTH, expand=YES)
        # _________________________________end of drop_menu_list_association()____________________
    '''

    # schermata che stampa tanti punsanti (sw) quanti pulsanti (hw) sono collegati a Blindo
    def schermata_pulsanti(closingroot, number_of_button):

        def close(root):
            root.destroy()
            ListAssociationView.schermata_associazioni()
            # _____________end of close()____________________

        # ____________________ start of schermata_pulsanti______________________
        closingroot.destroy()
        root = Tk()
        root.attributes('-fullscreen', SP.full_screen_option)
        root.config(bg=SP.standard_color_setting("root_list_association_view"))

        frame = Frame(root)
        frame.config(bg=SP.standard_color_setting("frame_list_association_view"))

        # caratteristiche della scrollbar
        text = Text(frame, wrap="none", bg=SP.standard_color_setting("frame_list_association_view"))
        vsb = Scrollbar(frame, orient="vertical", command=text.yview, width=40)
        vsb.config(width=90)
        text.configure(yscrollcommand=vsb.set, width=3, bg=SP.standard_color_setting("frame_list_association_view"))
        vsb.pack(side="left", fill="y")
        text.pack(side="left", fill="both", expand=True)

        exit_button = Button(frame,
                             text="Torna \nindietro",
                             command=lambda: close(root),
                             bd=SP.bord_size,
                             relief=SP.bord_style,
                             bg=SP.standard_color_setting("exit_button_with_text"),
                             font=SP.font_small,
                             fg=SP.button_font_color_gray_scale,
                             activebackground=SP.standard_color_setting("exit_button_with_text")
                             )
        exit_button.config(height=50, width=18)

        #  ciclo che crea "number_of_button" pulsanti
        for i in range(number_of_button):
            pulsante = uv.bottom_with_text(frame, "Pulsante " + str(i + 1))
            pulsante.pack(side=TOP, fill=BOTH)
            text.window_create("end", window=pulsante)
            text.insert("end", "\n")

        text.configure(state="disabled")
        frame.pack(fill=BOTH, expand=True)
        exit_button.pack(side=RIGHT, fill=BOTH)
        root.mainloop()
        # ________________________end of schermata_pulsanti__________________

    def new_list_view(root):
        root.destroy()
        find_list_existing_name = False
        existing_list = os.listdir(SP.path_liste)

        new_list_name = kv.keyboard("Inserisci il nome della lista")

        for list in existing_list:
            if list == new_list_name:
                find_list_existing_name = True

        if find_list_existing_name:
            choice = uv.multi_choice_view("Lista già presente!\nSostituisci oppure \nannulla l'operazione",
                                          "Sostituisci",
                                          "Annulla")

            if choice:
                fm.create_list(new_list_name)
            else:
                return

        else:
            fm.create_list(new_list_name)
        fm.change_list(new_list_name)
        ListAssociationView.schermata_associazioni()
        # ______________________________end of new_list_view__________________

    def show_list(closing_root):
        closing_root.destroy()

        def delete_item(root):

            list_name = mylist.get('active')
            uv.elimina_file_con_conferma(SP.path_liste, list_name)

            if list_name == fm.name_file:
                fm.change_list('Lista di default')

            # senza questo destroy() l'eliminazione della lista non avviene finchè il programma non viene chiuso
            # questa tecnica è usata anche nella funzione select_items_and_copy
            # root.destroy()
            # ListAssociationView.show_list(closing_root)
            root.destroy()
            ListAssociationView.schermata_associazioni()
            # _______________  END OF delete_item _______________________

        def upload_list(root):
            list_name = mylist.get('active')
            fm.change_list(list_name)
            root.destroy()
            ListAssociationView.schermata_associazioni()
            # ____________________ end of upload_list  ___________________

        def show_chiavette():
            root = Tk()
            root.attributes('-fullscreen', SP.full_screen_option)
            root.config(bg=SP.standard_color_setting("root_list_association_view"))

            frame = Frame(root, bg=SP.standard_color_setting("frame_list_association_view"))
            frame.pack()

            # passo alla funzione pi\media e quindi verranno visualizzate a schermo le chiavette disponibili
            dirs = os.listdir(SP.path_punto_accesso_chiavette)

            label = Label(frame,
                          text="Selezionare la chiavetta su cui esportare la lista",
                          bd=20,
                          bg=SP.standard_color_setting("frame_list_association_view"),
                          font=SP.font_small,
                          fg=SP.root_font_color)
            label.grid(row=1, column=0)
            label.config(width=50, height=4)

            # ciclo che stampa tante "chiavette" quante inserite nel device
            for USB_key in dirs:
                path_chiavetta = os.path.join(SP.path_punto_accesso_chiavette, USB_key)
                pulsante = Button(frame, text=USB_key,
                                  bg=SP.standard_color_setting("button_list_association_view"),
                                  font=SP.font_small,
                                  fg=SP.button_font_color_gray_scale,
                                  bd=SP.bord_size,
                                  relief=SP.bord_style,
                                  activebackground=SP.active_background_color_gray_scale,
                                  # Using the "path_chiavetta=path_chiavetta" trick
                                  # causes your function to store the current value
                                  # of "path_chiavetta" at the time your lambda is defined,
                                  # instead of waiting to look up the value of "path_chiavetta" later.
                                  command=lambda path_chiavetta=path_chiavetta: esporta_lista(root, path_chiavetta)
                                  )
                pulsante.config(width=40, height=3)
                pulsante.grid()

            uv.exit_button_with_text(root, SP.exit_text)

            root.mainloop()
            # _______________________ end of show_chiavette

        def esporta_lista(root, path_chiavetta_destinazione):
            root.destroy()
            list_name = mylist.get('active')

            final_path_list = os.path.join(SP.path_liste, list_name)

            final_path_cartella_liste = os.path.join(path_chiavetta_destinazione, SP.export_folder_name)
            # print(final_path_cartella_liste)

            cartella_lista_esportata = os.path.join(final_path_cartella_liste, list_name)
            # print(cartella_lista_esportata)

            rewite = True

            if os.path.exists(cartella_lista_esportata):

                # variabile booleana assegnata dalla risposta dell' utente
                user_choice = uv.multi_choice_view("Attenzione!\nEsiste già una versione di\n'" + list_name[0:20] + "'",
                                                   "Sovrascrivi",
                                                   "Annulla")

                if user_choice:
                    shutil.rmtree(cartella_lista_esportata)
                    rewite = True

                    # umask serve a garantire tutti i diritti di scrittura/lettura
                    # alla cartella creata con makedirs
                    oldmask = os.umask(0o77)
                    os.makedirs(cartella_lista_esportata, 0o1411)
                    os.umask(oldmask)
                    uv.show_dialog_with_time("Esportazione in corso...", 2)
                    uv.show_dialog_with_time("Operazione conclusa con successo", 2)
                else:
                    rewite = False

            else:

                oldmask = os.umask(0o77)
                #                os.makedirs(final_path_cartella_liste, 0o1411)
                os.makedirs(cartella_lista_esportata, 0o1411)
                os.umask(oldmask)
                uv.show_dialog_with_time("Esportazione in corso...", 2)
                uv.show_dialog_with_time("Operazione conclusa con successo", 2)

            # carico la lista selezionata dall'utente e la metto nell'oggetto "list_obj"
            if rewite:

                try:
                    with open(final_path_list, 'rb') as io:
                        list_objects = pk.load(io)
                        fm.copy_file_from_path_to_another(final_path_list, cartella_lista_esportata)

                        for audio in list_objects:
                            if audio.name != "DEFAULT":
                                name_file = str(audio.name)
                                path_scr = os.path.join(SP.path_che_simula_la_memoria_interna_del_raspberry, name_file)

                                fm.copy_file_from_path_to_another(path_scr,
                                                                  cartella_lista_esportata)

                except (FileNotFoundError, IOError) as e:
                    print(e)
            # pop up informativo

            # ____________________________  end of export_list ____________________________

        def rename_selected_element(root):
            # array con tutti gli elementi selezionati
            selected_items = [mylist.get(idx) for idx in mylist.curselection()]

            # file_in_memory= os.listdir(SP.path_che_simula_la_memoria_interna_del_raspberry)
            # selezione del primo elemento dell'array
            selected = selected_items[0]
            if selected != "Lista di default":
                new_name = kv.keyboard("Rinomina '" + selected + "'")

                # path file da rinominare
                scr = os.path.join(SP.path_liste, selected)
                # path file rinominato
                dst = os.path.join(SP.path_liste, new_name)
                os.rename(scr, dst)
                root.destroy()
                ListAssociationView.schermata_associazioni()
            else:
                uv.show_dialog_with_time("Attenzione\nImpossibile rinominare 'Lista di default'", 2)

            # _______________ end of rename_selected_element

        # ________________________  START OF show_list
        root = Tk()
        root.attributes('-fullscreen', SP.full_screen_option)
        root.config(bg=SP.standard_color_setting("root_list_association_view"))

        scrollbar = Scrollbar(root)
        scrollbar.config(width=70)
        scrollbar.pack(side=LEFT, fill=Y)

        mylist = Listbox(root,
                         yscrollcommand=scrollbar.set,
                         name='mylist',
                         font=SP.font_small,
                         width=90,
                         height=8,
                         bg=SP.standard_color_setting("listbox_list_association_view"),
                         fg=SP.root_font_color,
                         activestyle="none")

        # questo ciclo controlla tutte le sottocartelle del path passato in os.walk
        # e inserisce in mylist tutti i file con un'estensione contenuta in "formats"
        lists = os.listdir(SP.path_liste)
        for l in lists:
            mylist.insert(END, l)

        mylist.pack(side=LEFT, fill=BOTH, expand=True)

        mylist.pack(side=LEFT, fill=BOTH, expand=1, )
        scrollbar.config(command=mylist.yview)

        upload_list_button = Button(root,
                                    text="Carica lista",
                                    command=lambda: upload_list(root),
                                    bg=SP.standard_color_setting("button_list_association_view"),
                                    font=SP.font_small,
                                    fg=SP.button_font_color_gray_scale,
                                    bd=SP.bord_size,
                                    relief=SP.bord_style,
                                    activebackground=SP.standard_color_setting("button_list_association_view"))
        upload_list_button.config(height=2, width=25)
        upload_list_button.pack(side=TOP, fill=BOTH)

        export_list_button = Button(root,
                                    text="Esporta lista",
                                    command=lambda: show_chiavette(),
                                    bg=SP.standard_color_setting("button_list_association_view"),
                                    font=SP.font_small,
                                    fg=SP.button_font_color_gray_scale,
                                    bd=SP.bord_size,
                                    relief=SP.bord_style,
                                    activebackground=SP.standard_color_setting("button_list_association_view"))
        export_list_button.config(height=2, width=25)
        export_list_button.pack(side=TOP, fill=BOTH)

        rename_list_button = Button(root,
                                    text="Rinomina lista",
                                    command=lambda: rename_selected_element(root),
                                    bg=SP.standard_color_setting("button_list_association_view"),
                                    font=SP.font_small,
                                    fg=SP.button_font_color_gray_scale,
                                    bd=SP.bord_size,
                                    relief=SP.bord_style,
                                    activebackground=SP.standard_color_setting("button_list_association_view"))
        rename_list_button.config(height=2, width=25)
        rename_list_button.pack(side=TOP, fill=BOTH)

        #  pulsante per eliminare le liste selezionate
        delete_list_button = Button(root,
                                    text="Elimina lista",
                                    command=lambda: delete_item(root),
                                    bg=SP.standard_color_setting("delete_button_background"),
                                    bd=SP.bord_size,
                                    relief=SP.bord_style,
                                    activebackground=SP.standard_color_setting("delete_button_background"),
                                    font=SP.font_small,
                                    fg=SP.button_font_color_gray_scale)

        delete_list_button.config(height=2, width=25)
        delete_list_button.pack(fill=BOTH)

        uv.exit_button_with_text(root, "Torna al menu principale ")

    def import_list(list_association_root):
        list_association_root.destroy()
        usb_key = os.listdir(SP.path_punto_accesso_chiavette)

        root = Tk()
        root.attributes('-fullscreen', SP.full_screen_option)
        root.config(bg=SP.standard_color_setting("root_list_association_view"))

        frame = Frame(root, bg=SP.standard_color_setting("frame_list_association_view"))
        frame.pack()

        label = Label(frame,
                      text="Selezionare la chiavetta da cui importare le liste",
                      bd=SP.bord_size,
                      bg=SP.standard_color_setting("label_list_association_view"),
                      font=SP.font_small,
                      fg=SP.root_font_color)
        label.grid(row=1, column=0)
        label.config(width=50, height=4)

        # stampa delle chiavette sottoforma di pulsanti
        for usb in usb_key:
            pulsante = ListAssociationView.button_USB_key(frame, usb, root)
            pulsante.grid()

        uv.exit_button_with_text(root, "torna indietro")

        root.mainloop()

    def button_USB_key(frame, nome_chiavetta, closing_root):
        #
        path_key = os.path.join(SP.path_punto_accesso_chiavette, nome_chiavetta)

        button = Button(frame, text=nome_chiavetta,
                        bg=SP.standard_color_setting("button_list_association_view"),
                        font=SP.font_small,
                        fg=SP.button_font_color_gray_scale,
                        bd=SP.bord_size,
                        relief=SP.bord_style,
                        activebackground=SP.standard_color_setting("button_list_association_view"),
                        command=lambda: ListAssociationView.show_and_import_list(path_key, closing_root)
                        )
        button.config(width=40, height=3)
        return button

    def show_and_import_list(path_usb_key, closing_root):

        closing_root.destroy()
        ''' 
        funzione disabilitata per problematiche di esecuzione su raspberry
        il drop menu si apre tante volte quante sono le selezioni dell'utente

        def drop_menu_list_manager(evt):

            def import_list_and_closing():

                # root del drop_menu
                #unbind_root.destroy()
                fm.change_list(name_list)
                # path della cartella contenente la lista e i file sulla chiavetta

                list_folder = os.path.join(path_list_folders, name_list)

                for file in os.listdir(list_folder):

                    # path del singolo file analizzato
                    path_file = os.path.join(list_folder, file)
                    if file == name_list:
                        fm.copy_file_from_path_to_another(path_file, SP.path_liste)
                    else:
                        fm.copy_file_from_path_to_another(path_file,
                                                          SP.path_che_simula_la_memoria_interna_del_raspberry)
                # ___________________ end of import_list_and_closing________________________

            def delete_list(drop_menu_root):

                drop_menu_root.destroy()
                main_root.destroy()
                uv.elimina_file_con_conferma(path_list_folders, name_list)
                ListAssociationView.show_and_import_list(path_usb_key)
                # __________________________end of delete_list ____________________________
            # Note here that Tkinter passes an event object to onselect()
            w = evt.widget

            index = int(w.curselection()[0])
            name_list = w.get(index)

            root = Tk()
            root.overrideredirect(True)

            root_width = 140
            root_height = 150

            screen_width = root.winfo_screenwidth()
            screen_height = root.winfo_screenheight()

            # calculate position x and y coordinates
            x = (screen_width / 2) - (root_width / 2)
            y = (screen_height / 2) - (root_height / 2)
            root.geometry('%dx%d+%d+%d' % (root_width, root_height, x, y))

            frame = Frame(root,
                          bg=SP.standard_color_setting("frame_list_association_view"))

            import_list_button_drop_menu = Button(frame,
                                                  text="Importa",
                                                  height=1, width=8,
                                                  bg=SP.standard_color_setting("button_list_association_view"),
                                                  fg=SP.button_font_color_gray_scale,
                                                  command=lambda: import_list_and_closing(root),
                                                  font=SP.font_piccolo,
                                                  relief=SP.bord_style,
                                                  bd=SP.bord_size,
                                                  activebackground=SP.standard_color_setting("button_list_association_view")
                                                  )

            abort_button = Button(frame,
                                  text="  Annulla  ",
                                  height=1, width=8,
                                  bg=SP.standard_color_setting("button_list_association_view"),
                                  fg=SP.button_font_color_gray_scale,
                                  command=lambda: root.destroy(),
                                  font=SP.font_piccolo,
                                  relief=SP.bord_style,
                                  bd=SP.bord_size,
                                  activebackground=SP.standard_color_setting("button_list_association_view")
                                  )
            delete_button = Button(frame,
                                      text="   Elimina   ",
                                      height=1, width=8,
                                      bg=SP.standard_color_setting("delete_button_background"),
                                      fg=SP.button_font_color_gray_scale,
                                      command=lambda: delete_list(root),
                                      font=SP.font_piccolo,
                                      relief=SP.bord_style,
                                      bd=SP.bord_size,
                                      activebackground=SP.standard_color_setting("button_list_association_view")
                                      )

            import_list_button_drop_menu.pack(side=TOP)
            delete_button.pack(side=TOP)
            abort_button.pack(side=TOP)

            frame.pack(fill=BOTH, expand=YES)
            # ________________________ End of drop_menu_list:list_managetr ____________________________
        '''

        def import_list_with_button(name_list, cl_root):

            # root del drop_menu
            # unbind_root.destroy()
            fm.change_list(name_list)
            # path della cartella contenente la lista e i file sulla chiavetta

            list_folder = os.path.join(path_list_folders, name_list)
            saved_list = os.listdir(SP.path_liste)

            found_existing_list = False
            # controllo se la lista che si prova ad importare è già esistente in memoria
            for list in saved_list:
                if list == name_list:
                    found_existing_list = True
                    break
                else:
                    found_existing_list = False

            user_choice = True
            if found_existing_list:
                user_choice = uv.multi_choice_view("Attenzione\n'" + name_list[0:20] + "'\nè già presente",
                                                   "Sovrascrivi", "Annulla")

            if user_choice:

                for file in os.listdir(list_folder):

                    # path del singolo file analizzato
                    path_file = os.path.join(list_folder, file)
                    # copio l'ggetto lista nella cartella "liste"
                    if file == name_list:
                        fm.copy_file_from_path_to_another(path_file, SP.path_liste)
                    # copio i file audio nella meoria interna
                    else:
                        fm.copy_file_from_path_to_another(path_file,
                                                          SP.path_che_simula_la_memoria_interna_del_raspberry)

                    uv.show_dialog_with_time("Caricamento in corso....\n"
                                             "Attendere qualche secondo.", 2)
                    uv.show_dialog_with_time("Operazione conclusa con successo", 2)
                    cl_root.destroy()

                    ListAssociationView.schermata_associazioni()
            # ____________________________end of import_list_with_button_________________________

        # ______________________________start of show_import_list____________________________

        path_list_folders = os.path.join(path_usb_key, SP.export_folder_name)
        # se la cartella "Liste" non esiste la creo immediatamente

        if not os.path.exists(path_list_folders):
            oldmask = os.umask(0o77)
            os.makedirs(os.path.join(path_usb_key, SP.export_folder_name), 0o1411)
            os.umask(oldmask)

        main_root = Tk()
        main_root.attributes('-fullscreen', SP.full_screen_option)
        main_root.config(bg=SP.standard_color_setting("root_list_association_view"))

        frame = Frame(main_root, bg=SP.standard_color_setting("frame_list_association_view"))
        frame.pack()

        label_info = Label(main_root,
                           text="Scegli lista e importa",
                           bg=SP.standard_color_setting("label_list_association_view"),
                           fg=SP.root_font_color,
                           font=SP.font_small,
                           width=90, height=3,
                           )
        label_info.pack()
        # visualizzazione liste con scrollbar
        scrollbar = Scrollbar(main_root)
        scrollbar.pack(side=LEFT, fill=Y)

        my_list = Listbox(main_root,
                          yscrollcommand=scrollbar.set,
                          font=SP.font_small,
                          fg=SP.root_font_color,
                          bg=SP.standard_color_setting("listbox_list_association_view")
                          )

        for list in os.listdir(path_list_folders):
            my_list.insert(END, list)
        # questo evento trigghera una funzione (drop_menu_list_manager  in questo caso)
        # dopo la pressione di un elemento nella listbox
        # my_list.bind('<<ListboxSelect>>', drop_menu_list_manager)
        my_list.pack(side=LEFT, fill=BOTH, expand=True)
        scrollbar.config(width=70, command=my_list.yview)

        list_name = my_list.get('active')

        import_list_button = Button(main_root,
                                    text="Importa lista",
                                    command=lambda: import_list_with_button(list_name, main_root),
                                    bg=SP.standard_color_setting("button_list_association_view"),
                                    font=SP.font_small,
                                    fg=SP.button_font_color_gray_scale,
                                    bd=SP.bord_size,
                                    relief=SP.bord_style,
                                    activebackground=SP.standard_color_setting("button_list_association_view")
                                    )
        import_list_button.config(height=4, width=25)
        import_list_button.pack(side=TOP, fill=BOTH)

        uv.exit_button_with_text(main_root, "Torna indietro")

        main_root.mainloop()
        # _________________end of show_and_import_list__________________

    def menu_cascata_schermata_associazioni(master):
        # serve a rimuovere la riga tratteggiata che permette di spostare le opzioni col mouse
        master.option_add('*tearOff', FALSE)
        menu = Menu(master,
                    font=SP.font_medium,
                    bg=SP.standard_color_setting("menu_list_association_view"),
                    fg=SP.root_font_color)
        master.config(menu=menu)
        # crea il menu a cascata
        subMenu = Menu(menu,
                       font=SP.font_medium,
                       bg=SP.standard_color_setting("menu_list_association_view"),
                       fg=SP.root_font_color)
        menu.add_cascade(label="Opzioni                                                            ",
                         font=SP.font_medium,
                         menu=subMenu)  # menu a cascata
        # riga di separazione
        menu.config(bd=SP.bord_size, activebackground=SP.standard_color_setting("menu_list_association_view"))
        subMenu.add_command(label="Nuova Lista     ", font=SP.font_medium,
                            command=lambda: ListAssociationView.new_list_view(master),
                            activebackground=SP.standard_color_setting("menu_list_association_view"),
                            activeforeground=SP.root_font_color)
        subMenu.add_separator()
        subMenu.add_command(label="Mostra Liste    ", font=SP.font_medium,
                            command=lambda: ListAssociationView.show_list(master),
                            activebackground=SP.standard_color_setting("menu_list_association_view"),
                            activeforeground=SP.root_font_color)
        subMenu.add_separator()
        subMenu.add_command(label="Modifica Lista", font=SP.font_medium,
                            command=lambda: ListAssociationView.schermata_pulsanti(master, 5),
                            activebackground=SP.standard_color_setting("menu_list_association_view"),
                            activeforeground=SP.root_font_color)
        subMenu.add_separator()
        subMenu.add_command(label="Importa Liste  ", font=SP.font_medium,
                            command=lambda: ListAssociationView.import_list(master),
                            activebackground=SP.standard_color_setting("menu_list_association_view"),
                            activeforeground=SP.root_font_color)
        # subMenu.add_separator()
