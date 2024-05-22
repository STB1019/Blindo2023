from tkinter import *
import Reproduction
import StaticParameter as SP
import UtilityView as uv



class SettingsView:
    def set_aspect(self):
        root = Tk()
        root.attributes('-fullscreen', SP.full_screen_option)
        root.config(bg=SP.root_background_color_gray_scale)
        frame = Frame(root)
        frame.config(bg=SP.root_background_color_gray_scale)
        frame.pack()
        label = Label(root, text="Scegli il tuo bordo preferito",
                      bg=SP.root_background_color_gray_scale,
                      fg=SP.root_font_color,
                      width=0, height=1,
                      font=SP.font_medium
                      )
        label.pack(side=TOP)

        for i in range(6):
            relif_button = Button(
                                frame,
                                text=SP.bord_styles_set[i],
                                font=SP.font_small,
                                fg=SP.button_font_color_gray_scale,
                                command=lambda: SP.set_bord_style(i),
                                bg=SP.button_background_color_grey_scale,
                                relief=SP.bord_styles_set[i],
                                bd=20,
                                activebackground=SP.active_background_color_gray_scale,
                                activeforeground=SP.button_font_color_gray_scale)
            relif_button.config(height=4, width=10)
            relif_button.grid(row=3,column=i)

    def choose_button_aspect(self):
        root = Tk()
        root.attributes('-fullscreen', SP.full_screen_option)
        root.config(bg=SP.root_background_color_gray_scale)
        frame = Frame(root)
        frame.config(bg=SP.root_background_color_gray_scale)
        frame.pack()
        label = Label(frame, text="Cosa vuoi?",
                      bg=SP.root_background_color_gray_scale,
                      fg=SP.root_font_color,
                      width=90, height=4,
                      font=SP.font_medium
                      )
        label.pack()

        change_size_button = Button(frame,
                                    text="set size",
                                    bg=SP.button_background_color_grey_scale,
                                    command=lambda: SP.set_bord_size(),
                                    font=SP.font_small,
                                    fg=SP.button_font_color_gray_scale,
                                    relief=SP.bord_style,
                                    bd=SP.bord_size,
                                    #activebackground=SP.active_background_color_gray_scale
                                    )
        change_size_button.config(height=5, width=23)
        change_size_button.pack(side=LEFT)

        change_style_button = Button(frame,
                                     text="set style",
                                     bg=SP.button_background_color_grey_scale,
                                     fg=SP.button_font_color_gray_scale,
                                     command=lambda: SettingsView.set_aspect(),
                                     font=SP.font_small,
                                     relief=SP.bord_style,
                                     bd=SP.bord_size,
                                     #activebackground=SP.active_background_color_gray_scale
                                     )
        change_style_button.config(height=5, width=23)  # altezza 5
        change_style_button.pack(side=RIGHT)
        uv.exit_button_with_text(root, SP.exit_text)
        root.mainloop()

    def setting_view(self):
        root = Tk()
        root.attributes('-fullscreen', SP.full_screen_option)
        root.config(bg=SP.root_background_color_gray_scale)
        frame = Frame(root)
        frame.config(bg=SP.root_background_color_gray_scale)
        frame.pack()
        label = Label(frame, text="Impostazioni",
                      bg=SP.root_background_color_gray_scale,
                      fg=SP.root_font_color,
                      width=90, height=4,
                      font=SP.font_medium
                      )
        label.pack()

        change_size_button = Button(frame,
                                    text="caratteristiche pulsanti",
                                    bg=SP.button_background_color_grey_scale,
                                    command=lambda: SettingsView.choose_button_aspect(),
                                    font=SP.font_small,
                                    fg=SP.button_font_color_gray_scale,
                                    relief=SP.bord_style,
                                    bd=SP.bord_size,
                                    #activebackground=SP.active_background_color_gray_scale
                                    )
        change_size_button.config(height=5, width=23)
        change_size_button.pack(side=LEFT)

        change_style_button = Button(frame,
                                     text="volume",
                                     bg=SP.button_background_color_grey_scale,
                                     fg=SP.button_font_color_gray_scale,
                                     command=lambda: SettingsView.volume_view(),
                                     font=SP.font_small,
                                     relief=SP.bord_style,
                                     bd=SP.bord_size,
                                     #activebackground=SP.active_background_color_gray_scale
                                     )
        change_style_button.config(height=5, width=23)  # altezza 5
        change_style_button.pack(side=RIGHT)
        uv.exit_button_with_text(root, SP.exit_text)
        root.mainloop()

    def volume_view(self):
            current_volume = Reproduction.Reproduction.give_volume()
            # funzione che aggiorna il valore del volume cmostrato all'utente
            def change_volume_on_display():
                current_vol_label.configure(text=Reproduction.Reproduction.give_volume())

            # funzione che aumenta il volume e aggiorna il valore nel label
            def increse_and_change():
                Reproduction.Reproduction.increse_vol()
                change_volume_on_display()

            # funzione che abbassa il volume e aggiorna il valore nel label
            def decrese_and_change():
                Reproduction.Reproduction.decrese_vol()
                change_volume_on_display()

            root = Tk()
            root.attributes('-fullscreen', SP.full_screen_option)
            root.config(bg=SP.standard_color_setting("root_setting_view"))
            frame = Frame(root)
            frame.config(bg=SP.standard_color_setting("frame_setting_view"))
            frame.pack()


            # visualizza del valore del volume in un intervallo 10-100
            current_vol_label = Label(
                                    frame,
                                    text=current_volume,
                                    font=SP.font_large,
                                    width=4,
                                    bg=SP.standard_color_setting("label_setting_view"),
                                    fg=SP.root_font_color
                                    )
            current_vol_label.grid(row=1, column=1)

            # pulsante per diminuire il volume
            decrese_vol_button = Button(
                                  frame,
                                  text="-",
                                  font=SP.font_large,
                                  fg=SP.button_font_color_gray_scale,
                                  command=decrese_and_change,
                                  bg=SP.standard_color_setting("button_setting_view"),
                                  relief=SP.bord_style,
                                  bd=SP.bord_size,
                                  activebackground=SP.standard_color_setting("button_setting_view"),
                                  activeforeground=SP.button_font_color_gray_scale)
            decrese_vol_button.grid(row=1)
            decrese_vol_button.config(height=1, width=2)

            # pulsante per aumentare il volume
            increse_vol_button = Button(
                                  frame,
                                  text="+",
                                  font=SP.font_large,
                                  fg=SP.button_font_color_gray_scale,
                                  command=increse_and_change,
                                  bg=SP.standard_color_setting("button_setting_view"),
                                  activebackground=SP.standard_color_setting("button_setting_view"),
                                  activeforeground=SP.button_font_color_gray_scale,
                                  relief=SP.bord_style,
                                  bd=SP.bord_size)
            increse_vol_button.grid(row=1, column=2)
            increse_vol_button.config(height=1, width=2)

            scritta_vol = Label(frame,
                                text="Volume",
                                heigh=2,
                                font=SP.font_medium,
                                fg=SP.root_font_color,
                                bg=SP.standard_color_setting("label_setting_view"))

            scritta_vol.grid(row=0, column=1)
            uv.exit_button_with_text(root, SP.exit_text)
            root.mainloop()
