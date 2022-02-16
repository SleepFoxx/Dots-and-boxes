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
        self.strany = [False, False, True, False]
        self.vyherca = None
    def update(self, okno):
        for index,  side in enumerate(self.strany):
            if side:
                pygame.draw.line(okno, biela, (self.okraj[index][0]),
                                 self.okraj[index][1], 2)


boxy = []
for r in range(riadky):
    for c in range(stlpce):
        box = miesto(r, c)
        boxy.append(box)


#upravenie pozicie mysi na None
pozicia = None
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
    #vykreslenie hracej plochy 
    for r in range(riadky+1):
        for c in range(stlpce+1):
            pygame.draw.circle(okno, biela, (c*velkost_boxov + 2*padding, r*velkost_boxov + 3*padding), 2)
    #oznacenie miesta kliku
    #if pozicia:
        #pygame.draw.circle(okno, cervena, pozicia, 2)

    for box in boxy:
        box.update(okno)
        if pozicia and box.rect.collidepoint(pozicia):
            print(box.rect)
            pygame.draw.circle(okno, cervena, (box.rect.centerx, box.rect.centery), 2)
            

    #updatovanie hry aby sme videli vsetky akcie ktore vykoname
    pygame.display.update()
#vypnutie hry
pygame.quit()