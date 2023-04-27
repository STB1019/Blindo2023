from tkinter import *
import fileManaging as fm
import os
import StaticParameter as SP
import KeyboardView
from ListAssociationView import ListAssociationView as lav
import shutil


#    funzione che mostra a video un messaggio
#    passatole come primo parametro per un tempo (in secondi) passato come secondo parametrp
def show_dialog_with_time(text, time):
    def close(to_close):
        to_close.quit()
        to_close.destroy()

    dialog = Tk()
    dialog.config(bg=SP.root_background_color_gray_scale)

    dialog.overrideredirect(1)  # rimuove la barra che permetterebbe di chiudere la finestra appena creata

    screen_width = dialog.winfo_screenwidth()
    screen_height = dialog.winfo_screenheight()

    # calculate position x and y coordinates
    x = (screen_width / 2) - 200
    y = (screen_height / 2) - 30
    dialog.geometry('+%d+%d' % (x, y))

    label = Label(dialog,
                  text=text,
                  bg=SP.standard_color_setting("pop_up_background_color"),
                  font=SP.font_piccolo,
                  wraplength=500,
                  bd=4,
                  fg=SP.root_font_color,
                  relief=GROOVE
                  )
    label.configure(anchor="center")
    label.pack(expand=True)

    # time*1000 serve a convertire i secondi passati come parametro in millisecondi richiesti dalla funzione after
    dialog.after(time * 1000, close, dialog)
    dialog.mainloop()


#  funzione per avere un pulsante di uscita dalla schermata attuale con testo variabile passato come param
def exit_button_with_text(root, text):
    exit_button = Button(root,
                         text=text,
                         command=lambda: root.destroy(),
                         bg=SP.standard_color_setting("exit_button_with_text"),
                         font=SP.font_piccolo,
                         fg=SP.button_font_color_gray_scale,
                         bd=SP.bord_size,
                         activebackground=SP.standard_color_setting("exit_button_with_text")
                         )
    exit_button.config(height=3, width=10)
    exit_button.pack(side=BOTTOM, fill=BOTH)


# questa funzione permette di creare un pulsante
# che quando premuto apre la schermata show_file
# i parametri richiesti per la creazione del bottone sono: -frame su cui il bottone verrà applicato
#                                                          -testo che apparirà sul pulsante
def bottom_with_text(frame, text):
    button = Button(frame,
                    text=text,
                    bg=SP.standard_color_setting("button_utility_view"),
                    font=SP.font_piccolo,
                    fg=SP.button_font_color_gray_scale,
                    bd=SP.bord_size,
                    relief=SP.bord_style,
                    command=lambda: show_file(text.replace("Pulsante ", "")),
                    activebackground=SP.active_background_color_gray_scale,
                    activeforeground=SP.black)

    button.config(width=20, height=3)
    return button


# funzione che richiama una schermata chiedendo all'utente la conferma dell'eliminazione del file selezionato
def elimina_file_con_conferma(path, nome_file):
    def confirmed_deletion(path, nome_file):
        for list in os.listdir(SP.path_liste):
            fm.delete_element_from_list(nome_file, list)

        path_file = os.path.join(path, nome_file)

        # se si vuole eliminare una cartella, si usa il comando shutile.rmtree
        # se si vuole eliminare un file si usa il comando di os
        if os.path.isdir(path_file):
            shutil.rmtree(path_file)

        else:
            os.remove(path_file)
        root.quit()
        root.destroy()

    def abort_deletion():

        # root.quit()
        root.destroy()

    root = Tk()
    root.attributes('-fullscreen', SP.full_screen_option)
    root.config(bg=SP.standard_color_setting("root_utility_view"))

    frame = Frame(root)
    frame.config(bg=SP.standard_color_setting("frame_utility_view"))
    frame.pack()

    label = Label(frame,
                  text="Attenzione!\nVuoi eliminare\n" + nome_file + " ?",
                  bg=SP.standard_color_setting("root_utility_view"),
                  fg=SP.root_font_color,
                  width=90, height=3,
                  font=SP.font_medio)
    label.pack()

    delete_button = Button(frame,
                           text="Elimina",
                           bg=SP.standard_color_setting("delete_button_background"),
                           command=lambda: confirmed_deletion(path, nome_file),
                           font=SP.font_piccolo,
                           fg=SP.button_font_color_gray_scale,
                           relief=SP.bord_style,
                           bd=SP.bord_size,
                           activebackground=SP.standard_color_setting("delete_button_background"))
    delete_button.config(height=5, width=23)
    delete_button.pack(side=LEFT)

    abort_button = Button(frame,
                          text="Annulla",
                          bg=SP.standard_color_setting("confirm_button_background"),
                          command=lambda: abort_deletion(),
                          font=SP.font_piccolo,
                          fg=SP.button_font_color_gray_scale,
                          relief=SP.bord_style,
                          bd=SP.bord_size,
                          activebackground=SP.standard_color_setting("confirm_button_background"))
    abort_button.config(height=5, width=23)  # altezza 5
    abort_button.pack(side=RIGHT)
    root.mainloop()


def multiple_delete_with_choice(selected_file):
    def confirmed_deletion():
        for list in os.listdir(SP.path_liste):
            for file in selected_file:
                fm.delete_element_from_list(file, list)

        for el in selected_file:
            os.remove(os.path.join(SP.path_che_simula_la_memoria_interna_del_raspberry, el))
        root.quit()
        root.destroy()

    def abort_deletion():
        root.quit()
        root.destroy()

    root = Tk()
    root.attributes('-fullscreen', SP.full_screen_option)
    root.config(bg=SP.standard_color_setting("root_utility_view"))

    frame = Frame(root)
    frame.config(bg=SP.standard_color_setting("frame_utility_view"))
    frame.pack()

    label = Label(
        frame, text="Attenzione!\nVuoi eliminare " + str(len(selected_file)) + " file audio?",
        bg=SP.standard_color_setting("label_utility_view"),
        fg=SP.button_font_color_gray_scale,
        width=90, height=3,
        font=SP.font_medio)
    label.pack()

    delete_button = Button(frame,
                           text="Elimina",
                           bg=SP.standard_color_setting("delete_button_background"),
                           fg=SP.button_font_color_gray_scale,
                           command=lambda: confirmed_deletion(),
                           font=SP.font_piccolo,
                           relief=SP.bord_style,
                           bd=SP.bord_size,
                           activebackground=SP.standard_color_setting("delete_button_background"))
    delete_button.config(height=5, width=23)
    delete_button.pack(side=LEFT)

    abort_button = Button(frame,
                          text="Annulla",
                          bg=SP.standard_color_setting("confirm_button_background"),
                          fg=SP.button_font_color_gray_scale,
                          command=lambda: abort_deletion(),
                          font=SP.font_piccolo,
                          relief=SP.bord_style,
                          bd=SP.bord_size,
                          activebackground=SP.standard_color_setting("confirm_button_background"))
    abort_button.config(height=5, width=23)  # altezza 5
    abort_button.pack(side=RIGHT)
    root.mainloop()


def multi_choice_view(text_label, yes_button_text, no_button_text):
    def confirmed_selection():
        global choice
        choice = True
        root.quit()
        root.destroy()

    def abort_deletion():
        global choice
        choice = False
        root.quit()
        root.destroy()

    root = Tk()
    root.attributes('-fullscreen', SP.full_screen_option)
    root.config(bg=SP.standard_color_setting("root_utility_view"))

    frame = Frame(root)
    frame.config(bg=SP.standard_color_setting("frame_utility_view"))
    frame.pack()

    label = Label(
        frame, text=text_label,
        bg=SP.standard_color_setting("label_utility_view"),
        fg=SP.root_font_color,
        width=90, height=3,
        font=SP.font_medio)
    label.pack()

    confirm_button = Button(frame,
                            text=yes_button_text,
                            bg=SP.standard_color_setting("confirm_button_background"),
                            command=lambda: confirmed_selection(),
                            font=SP.font_piccolo,
                            fg=SP.button_font_color_gray_scale,
                            relief=SP.bord_style,
                            bd=SP.bord_size,
                            activebackground=SP.standard_color_setting("confirm_button_background"))
    confirm_button.config(height=5, width=23)
    confirm_button.pack(side=LEFT)

    abort_button = Button(frame,
                          text=no_button_text,
                          bg=SP.standard_color_setting("delete_button_background"),
                          command=lambda: abort_deletion(),
                          font=SP.font_piccolo,
                          fg=SP.button_font_color_gray_scale,
                          relief=SP.bord_style,
                          bd=SP.bord_size,
                          activebackground=SP.standard_color_setting("delete_button_background"))
    abort_button.config(height=5, width=23)  # altezza 5
    abort_button.pack(side=RIGHT)
    root.mainloop()
    return choice


# schermata che appare DOPO aver cliccato uno dei pulsanti della lista
# che vengono mostrati DOPO aver cliccato il pulsante ASSOCIA nel MENUPRINCIPALE
# richiede come parametro l'ID del pulsante che ha richiamato questa funzione
# parametro necessario per un trackback
def show_file(idButton):
    #  permette di fare l'associazione di un fileAudio dato un ID di un pulsante passato come parametro
    def bind_button(id, root):
        song_name = mylist.get('active')
        fm.bind(song_name, id)
        root.destroy()

    #   funzione che elimina l'elemento selezionato dopo aver chiesto all'utente      #########
    def delete_item(root):
        # for list in os.listdir(PS)
        song_name = mylist.get('active')
        elimina_file_con_conferma(SP.path_che_simula_la_memoria_interna_del_raspberry, song_name)
        root.destroy()
        # #############   END OF delete_item ####################

    #   START OF show_file
    root = Tk()
    root.attributes('-fullscreen', SP.full_screen_option)
    root.config(bg=SP.standard_color_setting("root_list_association_view"))

    scrollbar = Scrollbar(root)
    scrollbar.config(width=70)
    scrollbar.pack(side=LEFT, fill=Y)

    formats = SP.formats_audio
    mydict = {}
    mylist = Listbox(root,
                     yscrollcommand=scrollbar.set,
                     font=SP.font_piccolo,
                     fg=SP.root_font_color,
                     bg=SP.standard_color_setting("root_list_association_view"))
    # questo ciclo controlla tutte le sottocartelle del path passato in os.walk
    # e inserisce in mylist tutti i file con un'estensione contenuta in "formats"
    for radice, cartelle, files in os.walk(SP.path_che_simula_la_memoria_interna_del_raspberry, topdown=False):
        for name in files:
            for tipo in formats:
                if tipo in name:
                    temp_str = os.path.join(radice, name)
                    mydict[name] = temp_str
                    mylist.insert(END, name)
    mylist.pack(side=LEFT, fill=BOTH, expand=True)

    mylist.pack(side=LEFT, fill=BOTH, expand=1, )
    scrollbar.config(command=mylist.yview)

    #  pulsante che si trova alla destra della lista di file audio NELLA schermata  ASSOCIA
    bind_file_audio_button = Button(root,
                                    text="Scegli il file \n"
                                         "che vuoi associare\n "
                                         "al Pulsante" + idButton + "\n"
                                                                    "e poi clicca qui \n",
                                    command=lambda: bind_button(int(idButton), root),
                                    bg=SP.standard_color_setting("button_list_association_view"),
                                    font=SP.font_piccolo,
                                    fg=SP.button_font_color_gray_scale,
                                    bd=SP.bord_size,
                                    relief=SP.bord_style,
                                    activebackground=SP.standard_color_setting("button_list_association_view"))
    bind_file_audio_button.config(height=5, width=25)
    bind_file_audio_button.pack(side=TOP, fill=BOTH)

    #  pulsante per eliminare i file audio selezionati     ###############
    delete_file_audio_button = Button(root,
                                      text="Scegli il file \n"
                                           "che vuoi eliminare\n"
                                           "e clicca qui",
                                      command=lambda: delete_item(root),
                                      bg=SP.standard_color_setting("delete_button_background"),
                                      bd=SP.bord_size,
                                      relief=SP.bord_style,
                                      activebackground=SP.standard_color_setting("delete_button_background"),
                                      font=SP.font_piccolo,
                                      fg=SP.button_font_color_gray_scale)
    delete_file_audio_button.config(height=4, width=25)
    delete_file_audio_button.pack(fill=BOTH)

    exit_button_with_text(root, "Torna alla lista pulsanti")

    # questa funzione permette di creare un pulsante
    # che quando premuto apre la schermata show_file
    # i parametri richiesti per la creazione del bottone sono: -frame su cui il bottone verrà applicato
    #                                                          -testo che apparirà sul pulsante


def bottom_with_text(frame, text):
    button = Button(frame,
                    text=text,
                    bg=SP.standard_color_setting("button_list_association_view"),
                    font=SP.font_piccolo,
                    fg=SP.button_font_color_gray_scale,
                    bd=SP.bord_size,
                    relief=SP.bord_style,
                    command=lambda: show_file(text.replace("Pulsante", "")),
                    activebackground=SP.standard_color_setting("button_list_association_view"),

                    )

    button.config(width=20, height=3)
    return button


# funzione che crea un pulsante che visualizza i file da un path di origine
# e li copia in un path destinzaione
# mod: può essere "ESPORTA" o "IMPORTA" serve a rendere questa funzione più generale
def button_usb_key(frame, mod, nome_chiavetta, path_origine, path_destinzaione, cl_root):
    # cl_root.destroy
    button = Button(frame, text=nome_chiavetta,
                    bg=SP.standard_color_setting("usb_key_button"),
                    font=SP.font_piccolo,
                    fg=SP.button_font_color_gray_scale,
                    bd=SP.bord_size,
                    relief=SP.bord_style,
                    activebackground=SP.standard_color_setting("usb_key_button"),
                    command=lambda: show_and_select_item_from_path(mod, path_origine, path_destinzaione, nome_chiavetta,
                                                                   cl_root)
                    )
    button.config(width=40, height=3)
    return button


'''
function not used in project
'''


def button_usb_key_list(frame, nome_chiavetta):
    button = Button(frame, text=nome_chiavetta,
                    bg=SP.standard_color_setting("usb_key_button"),
                    font=SP.font_piccolo,
                    fg=SP.button_font_color_gray_scale,
                    bd=SP.bord_size,
                    relief=SP.bord_style,
                    activebackground=SP.standard_color_setting("usb_key_button"),
                    # command=lav.show_list().es
                    )
    button.config(width=40, height=3)
    return button


# funzione che appare nel menu principale dopo aver cliccato su "Gestisci archivio")
def raspberry_memory_manager():
    # funzione che permette du selezionare ed eliminare elementi multipli
    def delete_selected_elements(root):
        selected_items = [mylist.get(idx) for idx in mylist.curselection()]
        if len(selected_items) > 0:
            multiple_delete_with_choice(selected_items)
            root.destroy()
            raspberry_memory_manager()
        # _____________________ end of delete_selected_elements______________________________

    # funzione che permette du selezionare e rinominare elementi multipli
    # solamente il primo elemento il lista verrà rinominato
    def rename_selected_element(root):
        # array con tutti gli elementi selezionati
        selected_items = [mylist.get(idx) for idx in mylist.curselection()]

        # selezione del primo elemento dell'array
        if len(selected_items) > 0:
            selected = selected_items[0]
            size = len(selected)
            new_name = KeyboardView.keyboard("Rinomina '" + selected[0:size - 4] + "'")
            format = selected[size - 4:size]
            final_name = new_name + format
            # format accoglie gli ultimi 4 caratteri del primo elemento di tutti i file selezionati dall'utente

            file_in_memory = os.listdir(SP.path_che_simula_la_memoria_interna_del_raspberry)
            choice = True
            for el in file_in_memory:
                if final_name == el:
                    # richiesta all'utente
                    choice = multi_choice_view("Nome file \n'" + el + "'\n già presente", "Sostituisci", "Annulla")
                    if choice:
                        os.remove(os.path.join(SP.path_che_simula_la_memoria_interna_del_raspberry, el))
                    break

            if choice:
                # path file da rinominare
                src = os.path.join(SP.path_che_simula_la_memoria_interna_del_raspberry, selected)
                # path file rinominato
                dst = os.path.join(SP.path_che_simula_la_memoria_interna_del_raspberry, final_name)

                id_renamed_element = fm.give_id_button(selected)
                os.rename(src, dst)
                if id_renamed_element is not None:
                    fm.bind(final_name, id_renamed_element)

            root.destroy()
            raspberry_memory_manager()

    root = Tk()
    root.attributes('-fullscreen', SP.full_screen_option)
    root.config(bg=SP.standard_color_setting("root_archive_manager_view"))
    # lista di formati audio manipolabili
    formats = [".mp3", ".wav", ".wma", ".ogg", ".flac"]
    text_layer = "Memoria interna"

    label_info = Label(root, text=text_layer,
                       bg=SP.standard_color_setting("label_archive_manager_view"),
                       fg=SP.root_font_color,
                       width=90, height=3,
                       font=SP.font_piccolo
                       )
    label_info.pack()

    # visualizzazione brani con scrollbar
    scrollbar = Scrollbar(root)
    scrollbar.pack(side=LEFT, fill=Y)
    mylist = Listbox(root,
                     yscrollcommand=scrollbar.set,
                     selectmode=MULTIPLE,
                     font=SP.font_piccolo,
                     fg=SP.root_font_color,
                     bg=SP.standard_color_setting("listbox_archive_manager_view")
                     )
    mydict = {}

    # ciclo che aggiunge i file audio alla scrolbar
    for radice, cartelle, files in os.walk(SP.path_che_simula_la_memoria_interna_del_raspberry, topdown=False):
        for name in files:
            for tipo in formats:
                if tipo in name:
                    temp_str = os.path.join(radice, name)
                    mydict[name] = temp_str
                    mylist.insert(END, name)
    mylist.pack(side=LEFT, fill=BOTH, expand=True)
    scrollbar.config(width=70, command=mylist.yview)
    button_delete = Button(root,
                           text="Scegli i file \nche vuoi eliminare",
                           bg=SP.standard_color_setting("delete_button_background"),
                           fg=SP.button_font_color_gray_scale,
                           command=lambda: delete_selected_elements(root),
                           font=SP.font_piccolo,
                           bd=SP.bord_size,
                           relief=SP.bord_style,
                           activebackground=SP.standard_color_setting("delete_button_background")
                           )
    button_delete.config(height=4, width=20)
    button_delete.pack(side=TOP, fill=BOTH)

    button_rename = Button(root,
                           text="Scegli il file \nche vuoi rinominare",
                           bg=SP.standard_color_setting("button_archive_manager_view"),
                           fg=SP.button_font_color_gray_scale,
                           command=lambda: rename_selected_element(root),
                           font=SP.font_piccolo,
                           bd=SP.bord_size,
                           relief=SP.bord_style,
                           activebackground=SP.standard_color_setting("button_archive_manager_view")
                           )
    button_rename.config(height=4, width=20)
    button_rename.pack(side=TOP, fill=BOTH)

    exit_button_with_text(root, "Torna indietro")


# schermata che stampa a video i file contenuti in un determinato path
def show_and_select_item_from_path(mod, path_origine, path_destinzaione, nome_chiavetta, cl_root):
    #     funzione che copia la lista dei file selezionati in un'altra directory
    #     dall'utente nella schermata IMPORTA, dopo aver cliccato sul pulsante
    #     avente la scritta, appunto IMPORTA
    def select_items_and_copy(root):

        # lista contenente i brani selezionati
        selected = [mylist.get(idx) for idx in mylist.curselection()]

        # pop up con durata 2 secondi che informa di attendere
        show_dialog_with_time("L'operazione potrebbe richedere alcuni istanti...", 2)

        # ciclo che copia tutti i file selezionati dall'utente
        for file in selected:
            fm.copy_file_from_path_to_another(mydict[file], path_destinzaione)

        # poup-up informativo
        show_dialog_with_time("Operazione conclusa con successo", 2)
        root.destroy()
        # ######                 END OF select_items_and_copy    ###################

    def delete_selected_elements(root):
        selected = [mylist.get(idx) for idx in mylist.curselection()]

        # elimina_file_con_conferma(path_origine, str(number_of_deleted_file) + " file audio")
        multiple_delete_with_choice(selected)
        # root.destroy()

    root = Tk()
    root.attributes('-fullscreen', SP.full_screen_option)
    root.config(bg=SP.standard_color_setting("root_import_export_view"))
    formats = [".mp3", ".wav", ".wma", ".ogg", ".flac"]

    if mod == "esportare":
        text_layer = "Memoria interna"
        bg_label_color = SP.standard_color_setting("export_root_background")
        bg_list_color = SP.standard_color_setting("export_root_background")
    else:
        text_layer = nome_chiavetta
        bg_label_color = SP.standard_color_setting("import_root_background")
        bg_list_color = SP.standard_color_setting("import_root_background")

    label_info = Label(root, text=text_layer,
                       bg=bg_label_color,
                       fg=SP.root_font_color,
                       width=90, height=3,
                       font=SP.font_piccolo
                       )
    label_info.pack()

    # visualizzazione brani con scrollbar
    scrollbar = Scrollbar(root)
    scrollbar.pack(side=LEFT, fill=Y)
    mylist = Listbox(root,
                     yscrollcommand=scrollbar.set,
                     selectmode=MULTIPLE,
                     font=SP.font_piccolo,
                     fg=SP.root_font_color,
                     bg=bg_list_color
                     )
    mydict = {}

    # ciclo che aggiunge i file audio alla scrolbar
    for radice, cartelle, files in os.walk(path_origine, topdown=False):
        for name in files:
            for tipo in formats:
                if tipo in name:
                    temp_str = os.path.join(radice, name)
                    mydict[name] = temp_str
                    mylist.insert(END, name)
    mylist.pack(side=LEFT, fill=BOTH, expand=True)
    scrollbar.config(width=70, command=mylist.yview)
    exit_button_with_text(root, "Torna al menu principale")

    # ############        caratteristiche pulsante IMPORTA/ESPORTA        ######################
    button_text = "Seleziona i file \nche desideri " + mod + "\ne poi clicca qui"

    # se sono presenti chiavette viene abilitato il pulsante "IMPORTA"
    # otherwise viene visualizzato solamente il pulsante ELIMINA BRANI
    if mod != "Memoria interna":
        import_button = Button(root,
                               text=button_text,
                               bg=SP.standard_color_setting("import_button_background"),
                               command=lambda: select_items_and_copy(root),
                               font=SP.font_piccolo,
                               fg=SP.button_font_color_gray_scale,
                               bd=SP.bord_size,
                               relief=SP.bord_style,
                               activebackground=SP.standard_color_setting("import_button_background"))
        import_button.config(height=3, width=20)
        import_button.pack(side=TOP, fill=BOTH)

    # visualizza il pulsante ELIMINA solo in modalità esporta o se NON sono presenti chiavette
    cl_root.destroy()
    root.mainloop()
