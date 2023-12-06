from tkinter import *
from RecordView import RecordView as rv
from ImportExportView import ImportExportView as iev
import Reproduction
import StaticParameter as SP
import UtilityView as uv
from ListAssociationView import ListAssociationView as lav
from SettingsView import SettingsView as sv
import subprocess
import pygame.mixer as PM
PM.init()
PM.music.set_volume(SP.initial_volume_set)

registr = False

class SchermateGUI:



    # schermata del MENUPRINCIPALE
    def menu_principale(self):
        root = Tk()
        root.config(bg=SP.standard_color_setting("setting_main_menu"))
        root.attributes('-fullscreen', SP.full_screen_option)
        frame = Frame(root)

        # PULSANTE REGISTRA
        pulsante_registra= Button(frame,
                                  text="Registra",
                                  bg=SP.standard_color_setting("button_record_view"),
                                  command=lambda:rv.registra(SP.path_che_simula_la_memoria_interna_del_raspberry, registr),
                                  font=SP.font_piccolo,
                                  fg=SP.button_font_color_gray_scale,
                                  relief=SP.bord_style,
                                  bd=SP.bord_size,
                                  activebackground=SP.standard_color_setting("button_record_view")
                                  )

        pulsante_registra.grid(row=0, column=0)
        pulsante_registra.config(height=6, width=24)

        # PULSANTE IMPORTA/ESPORTA
        pulsante_importa_esporta = Button(frame,
                                          text="Importa/Esporta ",
                                          bg=SP.standard_color_setting("button_import_export_view"),
                                          command=lambda:iev.import_export(SP.path_punto_accesso_chiavette,
                                                                            SP.path_che_simula_la_memoria_interna_del_raspberry),
                                          font=SP.font_piccolo,
                                          fg=SP.button_font_color_gray_scale,
                                          relief=SP.bord_style,
                                          bd=SP.bord_size,
                                          activebackground=SP.standard_color_setting("button_import_export_view"))
        pulsante_importa_esporta.grid(row=0, column=1)
        pulsante_importa_esporta.config(height=6, width=24)

            # PULSANTE gestione archivio
        pulsante_archivio = Button(frame,
                                   text="Gestione Archivio",
                                   bg=SP.standard_color_setting("button_archive_manager_view"),
                                   command=lambda:uv.raspberry_memory_manager(),
                                   font=SP.font_piccolo,
                                   fg=SP.button_font_color_gray_scale,
                                   relief=SP.bord_style,
                                   bd=SP.bord_size,
                                   activebackground=SP.standard_color_setting("button_archive_manager_view")
                                   )
        pulsante_archivio.grid(row=1, column=0)
        pulsante_archivio.config(height=6, width=24)

        # PULSANTE LISTA ASSOCIAZIONI
        pulsante_associazioni = Button(frame,
                                       text="Lista Associazioni",
                                       bg=SP.standard_color_setting("button_list_association_view"),
                                       command=lav.schermata_associazioni,
                                       font=SP.font_piccolo,
                                       fg=SP.button_font_color_gray_scale,
                                       relief=SP.bord_style,
                                       bd=SP.bord_size,
                                       activebackground=SP.standard_color_setting("button_list_association_view")
                                       )
        pulsante_associazioni.grid(row=1, column=1)
        pulsante_associazioni.config(height=6, width=24)

        #  metodo che importa il menu a cascata nel menu principale
        SchermateGUI.menu_cascata_menu_principale(root)

        frame.pack()
        root.mainloop()  # funzione che continua a tenere aperto la finetra principale



    # schermata di volume_view accessibile dal menu cascata


    # funzione che permette di avere un menu a cascata con la funzione di uscire dal main program
    def menu_cascata_menu_principale(master):
        def turn_off_device():
            choice = uv.multi_choice_view(SP.message_label_quit_device,
                                          SP.message_text_button_confirm,
                                          SP.message_text_button_abort)
            if choice:
                subprocess.Popen(['shutdown', '-h', 'now'])
            else:
                return

         # serve a rimuovere la riga tratteggiata che permette di spostare le ozioni col mouse
        master.option_add('*tearOff', FALSE)
        menu = Menu(master,
                    font=SP.font_medio,
                    fg=SP.root_font_color,
                    bg=SP.standard_color_setting("setting_main_menu"), )
        master.config(menu=menu)
        # crea il menu a cascata

        subMenu = Menu(menu,
                       font=SP.font_medio,
                       fg=SP.root_font_color,
                       bg=SP.standard_color_setting("setting_main_menu"), )

        menu.config(bd=SP.bord_size,
                    activebackground=SP.standard_color_setting("setting_main_menu"),
                    activeforeground=SP.root_font_color)

        menu.add_cascade(label="Impostazioni                                                                  ",
                         font=SP.font_medio, menu=subMenu,)  # menu a cascata
        # riga di separazione
        subMenu.add_separator()
        subMenu.add_command(label="Volume     ", font=SP.font_medio, command=lambda:sv.volume_view(),
                            activebackground=SP.standard_color_setting("setting_main_menu"),
                            activeforeground=SP.root_font_color)
        subMenu.add_separator()
        subMenu.add_command(label="Spegni    ", font=SP.font_medio, command=lambda: turn_off_device(),
                            activebackground=SP.standard_color_setting("setting_main_menu"),
                            activeforeground=SP.root_font_color)

        subMenu.add_separator()
        subMenu.add_command(label="Chiudi programma", font=SP.font_medio, command=master.destroy,
                            activebackground=SP.standard_color_setting("setting_main_menu"),
                            activeforeground=SP.root_font_color)
        subMenu.add_separator()