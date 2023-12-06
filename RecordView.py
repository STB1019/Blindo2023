'''
Disabilitare l'import sottostante per la versione PC
Abilitare l'import sottostante per la versione RASPBERRY
'''
import registrazione as reg

from tkinter import *
import KeyboardView as key
import UtilityView as uv
import StaticParameter as SP
import os

#recording = False


class RecordView:

    def registra(path_che_simula_la_memoria_interna_del_raspberry, recording):
        root = Tk()
        root.attributes('-fullscreen', SP.full_screen_option)
        root.config(bg=SP.standard_color_setting("root_record_view"))

        exitButton = uv.exit_button_with_text(root, SP.exit_text, recording)

        frame = Frame(root)
        frame.config(bg=SP.standard_color_setting("frame_record_view"))
        frame.pack()

        label = Label(frame, text="Premi su Start per registrare",
                      bg=SP.standard_color_setting("label_record_view"),
                      width=90,
                      height=3,
                      font=SP.font_medio,
                      fg=SP.root_font_color
                      )
        label.pack()

        #    funzione che fa partire la registrazione
        def start_recoding(name_recoded_file):
            global recording
            global new_name
            # nascono il pulsante PLAY REGISTRAIONE
            pulsante_play.pack_forget()
            exitButton.pack_forget()

            # visualuzzo il pulsante STOP REGISTRAZIONE
            pulsante_stop.pack()

            recording = True

            #cambio il contenuto del label informativo
            label["text"] = "Registrazione in corso.....\nPremi il pulsante per interrompere"

            final_path = os.path.join(path_che_simula_la_memoria_interna_del_raspberry, name_recoded_file)

            reg.start(final_path)

        #  funzione che ferma la registrazione e chiede all'utente il nome del file registrato
        def stop_recording():
            global recording
            # nascono il pulsante stop recording con il metodo pack_forget
            pulsante_stop.pack_forget()

            # abilito il pulsante play
            pulsante_play.pack()
            exitButton.pack(side=BOTTOM, fill=BOTH)


            #recording = False

            # lista dei file presenti nella cartella della memoria interna
            file_audio_memoria_interna= os.listdir(path_che_simula_la_memoria_interna_del_raspberry)

            if recording:
                reg.stop()
                recording = False

                # funzione che richiama la tastiera e chiede all'utente il nome del file
                file_not_found = True

                label_keboard = "Scegli il nome del file appena registrato"

                while file_not_found:

                    new_name = key.keyboard(label_keboard)

                    new_name_with_format = new_name+".wav"

                    for file in file_audio_memoria_interna:
                        if new_name_with_format == file:
                            #print("-----------------------------------trovato")
                            file_not_found = True
                            label_keboard = "File già esistente"
                            break
                        else:
                            #print("-----------------------------------non trovato")
                            file_not_found = False


                # path completo del nome del file appena registrato
                initial = os.path.join(path_che_simula_la_memoria_interna_del_raspberry, SP.name_recoded_file)

                # path completo del file registrato rinominato
                final = os.path.join(path_che_simula_la_memoria_interna_del_raspberry, new_name_with_format)

                # funzione che rinomina il file audio appena registrato
                os.rename(initial, final)

                recording = False

                label["text"] = "Premi il pulsante per registrare"

        # caratteristiche pulsante INIZIA REGISTRAZIONE
        pulsante_play = Button(frame,
                               text="Inizia a registrare",
                               bg=SP.standard_color_setting("confirm_button_background"),
                               command=lambda: start_recoding(SP.name_recoded_file),
                               font=SP.font_piccolo,
                               fg=SP.button_font_color_gray_scale,
                               relief=SP.bord_style,
                               bd=SP.bord_size,
                               activebackground=SP.standard_color_setting("confirm_button_background")
                               )
        pulsante_play.config(height=5, width=23)
        pulsante_play.pack()

        # caratteristiche pulsante  STOP REGISTRAZIONE
        pulsante_stop = Button(frame,
                               text="Interrompi la registrazione",
                               bg=SP.standard_color_setting("delete_button_background"),
                               command=lambda: stop_recording(),
                               font=SP.font_piccolo,
                               fg=SP.button_font_color_gray_scale,
                               relief=SP.bord_style,
                               bd=SP.bord_size,
                               activebackground=SP.standard_color_setting("delete_button_background")
                               )
        pulsante_stop.config(height=5, width=23)



        root.mainloop()
