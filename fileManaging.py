import pickle as pk
import os

# from IPython.utils.tests.test_wildcard import obj_t

from fileAudio import FileAudio
import shutil
import StaticParameter as SP

name_file = 'Lista di default'


def change_list(list_name):
    global name_file
    name_file = list_name


def give_id_button(audio_name):
    obj_list = load_list()
    for audio in obj_list:
        if audio.name == audio_name:
            return int(audio.idButton)


# funzione che ritorna la lista delle stringhe dei fileAudio
# presenti in "lista finale" riordinata in base al numero del pulsante
def give_sorted_list():
    final_path = os.path.join(SP.path_liste, name_file)
    list = []

    if os.path.isfile(final_path):
        try:
            with open(final_path, 'rb') as io:
                my_objects = pk.load(io)
                my_objects.sort(key=lambda x: int(str(x.idButton)))

                for audio in my_objects:
                    if str(audio.name) != "DEFAULT":
                        formattedNumber = '{:5s}'.format(str(audio.idButton))
                        list.append("Pulsante " + formattedNumber + " ------->  " + str(audio.name) + "\n")

        except Exception as e:
            print(e)
    return list


# funzione che elimina da lista finale i fileAudio che vengono eliminati tramite la GUI
def delete_element_from_list(nome_file_da_rimuovere, nome_lista):  # aggiungere la liste da conytrollare come parametro

    # final_path_element = os.path.join(SP.path_liste, nome_file_da_rimuovere)
    final_path_list = os.path.join(SP.path_liste, nome_lista)
    # print(final_path_list)

    my_objects = []
    if os.path.isfile(final_path_list):

        try:
            with open(final_path_list, 'rb') as io:
                my_objects = pk.load(io)

                for audio in my_objects:
                    if audio.name == nome_file_da_rimuovere:
                        my_objects.remove(audio)

            save_file_audio_list(my_objects, nome_lista)

        except (FileNotFoundError, IOError) as e:
            print(e)


def create_list(list_name):
    default = FileAudio('DEFAULT', 0)
    my_objects = [default]
    save_file_audio_list(my_objects, list_name)


def delete_bind(id, audio_name):
    obj_list = load_list()

    for audio in obj_list:
        if audio.idButton == id and audio.name == audio_name:
            obj_list.remove(audio)
            save_file_audio(obj_list)


# binding between the button and the name of the file audio
def bind(audio_name, id):
    # default element needed to pass through the list of file audio if it has only one element
    file_audio = FileAudio(audio_name, id)
    final_path = os.path.join(SP.path_liste, name_file)
    my_objects = []
    if os.path.isfile(final_path):
        try:
            final_path = os.path.join(SP.path_liste, name_file)
            with open(final_path, 'rb') as io:
                my_objects = pk.load(io)

                for audio in my_objects:
                    if audio.name == audio_name or audio.idButton == id:
                        my_objects.remove(audio)
                my_objects.append(file_audio)

                save_file_audio(my_objects)

        except (FileNotFoundError, IOError) as e:
            print(e)
    else:
        my_objects.append(file_audio)
        save_file_audio(my_objects)


def load_list():
    # my_objects = []
    try:
        final_path = os.path.join(SP.path_liste, name_file)
        with open(final_path, 'rb') as io:
            my_objects = pk.load(io)
    except (FileNotFoundError, IOError) as e:
        print(e)
    return my_objects


# funzione per salvare la lista di fileAudio come un unico oggetto con nome "lista finale" #####
def save_file_audio(my_objects):
    final_path = os.path.join(SP.path_liste, name_file)
    with open(final_path, 'wb') as output:
        pk.dump(my_objects, output, -1)


def save_file_audio_list(my_objects, name_list):
    final_path = os.path.join(SP.path_liste, name_list)
    with open(final_path, 'wb') as output:
        pk.dump(my_objects, output, -1)


# funzione che utilizza la funzione di sitema "shutil.copy" per copiare i file da un path ad un altro
def copy_file_from_path_to_another(initial_path, ending_path):
    shutil.copy(initial_path, ending_path)
