#import zakladneho modulu
import pygame
#rozmery hry
obrazovka = sirka, vyska = 300, 300
velkost_boxov = 40
padding = 20
riadky = stlpce = (sirka - 4*padding) // velkost_boxov
print(riadky, stlpce)
#definicia okna
pygame.init()
okno = pygame.display.set_mode(obrazovka)
#definicie farieb ktore budu pouzite v hre
biela = (255, 255, 255)
cervena = (255, 0, 0)
modra = (0, 0, 255)
zelena = (0, 255, 0)
cierna = (0, 0, 0)

font = pygame.font.SysFont('cursive', 25)
#classa samotneho okna
class miesto:
    def __init__(self, r, c):
        self.r = r
        self.c = c
        self.index = self.r * riadky + self.c
        self.rect = pygame.Rect((self.c*velkost_boxov + 2*padding, r*velkost_boxov + 3*padding, velkost_boxov, velkost_boxov))

        self.vlavo = self.rect.left
        self.hore = self.rect.top
        self.dole = self.rect.bottom
        self.vpravo = self.rect.right

        self.okraj = [
                        [(self.vlavo, self.hore), (self.vpravo, self.hore)],
                         [(self.vpravo, self.hore),(self.vpravo, self.dole)],
                         [(self.vpravo, self.dole),(self.vlavo, self.dole)],
                         [(self.vlavo, self.dole),(self.vlavo, self.hore)]
                        

                    ]
        self.strany = [False, False, False, False]
        self.vyherca = None

    def kontrola_vyhry(self, vyherca):
        if not self.vyherca:
            if self.strany == [True]*4:
                self.vyherca = vyherca
                if vyherca == 'X':
                    self.color = zelena
                else:
                    self.color = cervena
                self.text = font.render(self.vyherca, True, biela)

                return 1
            return 0

    def update(self, okno):
        if self.vyherca:
            pygame.draw.rect(okno, self.color, self.rect)
            okno.blit(self.text, (self.rect.centerx - 5, self.rect.centery - 7))
        for index,  side in enumerate(self.strany):
            if side:
                pygame.draw.line(okno, biela, (self.okraj[index][0]),
                                 self.okraj[index][1], 2)

#list boxov
boxy = []
for r in range(riadky):
    for c in range(stlpce):
        box = miesto(r, c)
        boxy.append(box)


#upravenie pozicie mysi na None
pozicia = None
bbox = None
bbox = box
hore = False
vpravo = False
vlavo = False
dole = False

kolo = 0
hraci = ['X', 'O']
hrac = hraci[kolo]
dalsie_kolo = False

hrac1_skore = 0
hrac2_skore = 0

#okno hry a priebeh
bezi = True
while bezi:
    okno.fill(cierna)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            bezi = False
        #zaznamenanie klikov v okne hry 
        if event.type == pygame.MOUSEBUTTONDOWN:
            pozicia = event.pos
        if event.type == pygame.MOUSEBUTTONUP:
            pozicia = None
        if event.type == pygame.KEYDOWN:
            #onkeypress nakreslenie strany
            if event.key == pygame.K_UP:
                hore = True
            if event.key == pygame.K_DOWN:
                dole = True
            if event.key == pygame.K_LEFT:
                vlavo = True
            if event.key == pygame.K_RIGHT:
                vpravo = True
                
        #on key release 
        if event.type == pygame.KEYUP:
            if event.key == pygame.K_UP:
                hore = False
            if event.key == pygame.K_DOWN:
                dole = False
            if event.key == pygame.K_LEFT:
                vlavo = False
            if event.key == pygame.K_RIGHT:
                vpravo = False


    #vykreslenie hracej plochy 
    for r in range(riadky+1):
        for c in range(stlpce+1):
            pygame.draw.circle(okno, biela, (c*velkost_boxov + 2*padding, r*velkost_boxov + 3*padding), 2)
    
    #oznacenie stredu aktualne vybrateho stvorca
    for box in boxy:
        box.update(okno)
        if pozicia and box.rect.collidepoint(pozicia):
            bbox = box
    if bbox:  
        index = bbox.index
        if not bbox.vyherca:
            pygame.draw.circle(okno, cervena, (bbox.rect.centerx, bbox.rect.centery), 2)
        # definicia strany boxov, prepnutie kola po vyplneni strany
        if hore and not bbox.strany[0]:
            bbox.strany[0] = True
            if index - riadky >= 0:
                boxy[index - riadky].strany[2] = True
                dalsie_kolo = True
        if vpravo and not bbox.strany[1]:
            bbox.strany[1] = True
            if (index + 1) % stlpce > 0:
                boxy[index + 1].strany[3] = True
                dalsie_kolo = True
        if dole and not bbox.strany[2]:
            bbox.strany[2] = True
            if (index + riadky) < len(boxy):
                boxy[index + riadky].strany[0] = True
                dalsie_kolo = True
        if vlavo and not bbox.strany[3]:
            bbox.strany[3] = True
            if index % stlpce > 0:
                boxy[index - 1].strany[1] = True
                dalsie_kolo = True
        # kontrola vyhri + pocitac kol
        
        res = bbox.kontrola_vyhry(hrac)
        if res:
            if hrac == 'X':
                hrac1_skore += 1
            else:
                hrac2_skore += 1



        if dalsie_kolo:
            kolo = (kolo + 1) % len(hraci)
            hrac = hraci[kolo]
            dalsie_kolo = False
    #upresnenie parametrov textu hraca 1

    hrac1foto = font.render(f'Hrac 1: {hrac1_skore}', True, modra)
    hrac1rect = hrac1foto.get_rect()
    hrac1rect.x, hrac1rect.y = 2*padding, 15

    
    #upresnenie parametrov textu hraca 2

    hrac2foto = font.render(f'Hrac 2: {hrac2_skore}', True, modra)
    hrac2rect = hrac2foto.get_rect()
    hrac2rect.right, hrac2rect.y = sirka-2*padding, 15


    #vypisanie textu hore

    okno.blit(hrac1foto, hrac1rect)
    okno.blit(hrac2foto, hrac2rect)


    #podciarknutie (ukazatel) aktualneho hraca

    if hrac == 'X':
        pygame.draw.line(okno, modra, (hrac1rect.x, hrac1rect.bottom + 2),
                            (hrac1rect.right, hrac1rect.bottom + 2), 1)
    else:
        pygame.draw.line(okno, modra, (hrac2rect.x, hrac2rect.bottom + 2),
                            (hrac2rect.right, hrac2rect.bottom + 2), 1)


    #updatovanie hry aby sme videli vsetky akcie ktore vykoname
    pygame.display.update()
#vypnutie hry
pygame.quit()