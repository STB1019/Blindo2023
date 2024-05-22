import pygame.mixer as PM
from math import log10, floor
import os

import StaticParameter as SP


class Reproduction:

    def reproduce_file_audio(self, id, list):
        find = False
        messaggio =""
        for audio in list:
            if int(audio.idButton) == id:
                PM.init()
                PM.music.load(os.path.join(SP.path_che_simula_la_memoria_interna_del_raspberry, audio.name))
                PM.music.play()

    # a seguire 2 funzioni per aumentare e diminuire il volume
    # ogni volta che vengono richiamate cambiano il valore del volume del 10 per cento
    def increse_vol(self):

        PM.init()
        current_volume = PM.music.get_volume()
        PM.music.set_volume(current_volume + 0.1)

    def decrese_vol(self):

        PM.init()
        current_volume = PM.music.get_volume()
        PM.music.set_volume(current_volume - 0.1)

    # funzione che restituisce il valore del volume in un range da 10 a 100
    def give_volume(self):

        PM.init()
        volume = PM.music.get_volume()
        volume = round(volume, -int(floor(log10(abs(volume)))))

        volume = volume * 100

        if volume < 20:
            volume = 10.0
        elif volume < 10:
            volume = 0
        return str(volume)[:3].replace('.',
                                       '')  # rimuove il punto decimale del volume convertito nell' intervallo 10-100

