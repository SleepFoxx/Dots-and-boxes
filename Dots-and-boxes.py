from cgitb import text
from tkinter import *
from turtle import color
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
    def oznacenie_boxu(app):
        boxy = np.argwhere(app.status_hry == -4) #zistenie nenulovych miest(zabratych)
        for box in boxy:
            if list(box) not in app.je_miesto_zabrate and list(box) !=[]:
                app.je_miesto_zabrate.append(list(box))
                farba = hrac1_farba_svetla
                app.shade_box(box, farba)
        boxy = np.argwhere(app.status_hry == 4)
        for box in boxy:
            if list(box) not in app.je_miesto_zabrate and list(box) !=[]:
                farba = hrac2_farba_svetla
                app.shade_box(box, farba)
    def aktualizovat_plochu(app, typ, logicka_pozicia):
        r = logicka_pozicia[0]
        c = logicka_pozicia[1]
        val = 1
        if app.hrac1_kolo:
            val =- 1
        if c < (pocet_bodiek-1) and r < (pocet_bodiek-1):
            app.status_hry[c][r] += val
        if typ == 'riadok':
            app.status_riadku[c][r] = 1
            if c >= 1:
                app.status_hry[c-1][r] += val
        elif type == 'stlpec':
            app.status_stlpca[c][r] = 1
            if r >= 1:
                app.status_hry[c][r-1] += val
    def koniec_hry(app):
        return (app.status_riadku == 1).all() and (app.status_stlpca == 1).all()
    
    def nakresli_okraj(app, typ, logicka_pozicia):
        if typ == 'riadok':
            zaciatok_x = dialka_medzi_bodkami /2 + logicka_pozicia[0]*dialka_medzi_bodkami
            koniec_x = zaciatok_x + dialka_medzi_bodkami
            zaciatok_y = dialka_medzi_bodkami / 2 + logicka_pozicia[1]*dialka_medzi_bodkami
            koniec_y = zaciatok_y
        elif typ == 'stlpec':
            zaciatok_y = dialka_medzi_bodkami / 2 + logicka_pozicia[1] * dialka_medzi_bodkami
            koniec_y = zaciatok_y + dialka_medzi_bodkami
            zaciatok_x = dialka_medzi_bodkami / 2 + logicka_pozicia[0] * dialka_medzi_bodkami
            koniec_x = zaciatok_x
        
        if app.hrac1_kolo:
            farba = hrac1_farba
        else:
            farba = hrac2_farba
        app.canvas.create_line(zaciatok_x, zaciatok_y, koniec_x, koniec_y, fill=farba, width=sirka_hrany)
        
        def zobraz_koniec_hry(app):
            hrac1_skore = len(np.argwhere(app.status_hry == 4))
            hrac2_skore = len(np.argwhere(app.status_hry == 4))

            if hrac1_skore > hrac2_skore:
                #vyhral hrac 1
                text = "Vyhral hrac 1"
                color = hrac1_farba
            elif hrac1_skore < hrac2_skore:
                #vyhral hrac 2
                text = "Vyhral hrac 2"
                color = hrac2_farba
            else:
                text = "Je to remiza"
                color = 'black'
            
            app.canvas.delete("all")
            app.canvas.create_text(velkost_hry / 2, velkost_hry / 2, font="comic sans-serif", fontsize=50, text=text, color=color)

            text_skore = "Skore \n"
            app.canvas.create_text(velkost_hry / 2, 5*velkost_hry / 8, font="comic sans-serif", fontsize=50, text=skore_text, fill= zelena)


            skore_text = 'Hrac 1: ' + str(hrac1_skore) + '\n'
            skore_text += 'Hrac 2' + str(hrac2_skore) + '\n'




















