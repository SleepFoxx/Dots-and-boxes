from tkinter import *
import numpy as np

velkost_hry = 600
pocet_bodiek = 6
velkost_bodky = (velkost_hry /3 - velkost_hry / 8) / 2
hrubka_bodky = 50
farba_bodky = '#7BC043'
hrac1_farba = '#0492CF'
hrac1_farba_svetla = '#05b4ff'
hrac2_farba = '#EE4035'
hrac2_farba_svetla = '#EE7E77'
zelena = '#00ff2a'
sirka_bodky = 0.25*velkost_hry/pocet_bodiek
sirka_hrany = 0.1*velkost_hry/pocet_bodiek
dialka_medzi_bodkami = velkost_hry / (pocet_bodiek)

class Bodky_a_boxy():
    #okno hry
    def __init__(app):
        app.window = Tk()
        app.window.title('Bodky_a_boxy')
        app.canvas = Canvas(app.window, width=velkost_hry, height=velkost_hry).pack()
        app.window.bind('<Button-1>', app.click)
        app.hrac1_zacina = True
        app.refresh_board()
        app.hrat_znovu()

    def hrat_znovu(app):
        app.refresh_board()
        app.status_hry = np.zeros(shape=(pocet_bodiek - 1, pocet_bodiek -1))
        app.status_riadku = np.zeros(shape=(pocet_bodiek, pocet_bodiek - 1))
        app.status_stlpca = np.zeros(shape=(pocet_bodiek - 1, pocet_bodiek))


        app.hrac1_zacina = not app.hrac1_zacina
        app.hrac1_kolo = not app.hrac1_zacina
        app.reset_board = False
        app.turntext_handle = []

        app.already_marked_boxes = []
        app.display_turn_text()

    def mainloop(app):
        app.window.mainloop()

        #vsetky logicke funkcie hry
    def je_miesto_zabrate(app, logicka_pozicia, typ):
        r = logicka_pozicia[0]
        c = logicka_pozicia[1]
        zabrane = True

        if typ == 'riadok' and app.status_riadku[c][r] == 0:
            zabrane = False
        if typ == 'stlpec' and app.status_stlpca[c][r] == 0:
            zabrane = False
        
        return zabrane
    def zmenit_obrys_na_logicku_poziciu(app, obrys_pozicia):
        obrys_pozicia = np.array(logicka_pozicia)
        pozicia = (obrys_pozicia - dialka_medzi_bodkami/4)//(dialka_medzi_bodkami/2)

        typ = False
        logicka_pozicia = []
        if pozicia[1] % 2 == 0 and (pozicia[0] - 1) % 2 == 0:
            r = int((pozicia[0] - 1) // 2)
            c = int((pozicia[1] // 2))
            logicka_pozicia = [r , c]
            typ = 'riadok'
        elif pozicia[0] % 2 == 0 and (pozicia[1] - 1) % 2 == 0:
            c = int((pozicia[1] - 1) // 2)
            r = int((pozicia[0]) // 2)
            logicka_pozicia = [r, c]
            typ = 'stlpec'
        return logicka_pozicia, typ























