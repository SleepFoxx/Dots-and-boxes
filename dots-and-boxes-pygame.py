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

    def kontrola_vyhry(self):
        if not self.vyherca:
            if self.strany == [True]*4:
                self.vyherca = True

    def update(self, okno):
        if self.vyherca:
            pygame.draw.rect(okno, cervena, self.rect)
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
    #oznacenie miesta kliku
    #if pozicia:
        #pygame.draw.circle(okno, cervena, pozicia, 2)

    for box in boxy:
        box.update(okno)
        if pozicia and box.rect.collidepoint(pozicia):
            bbox = box
    if bbox:  
        index = bbox.index
        pygame.draw.circle(okno, cervena, (bbox.rect.centerx, bbox.rect.centery), 2)
            
        if hore:
            bbox.strany[0] = True
            if index - riadky >= 0:
                boxy[index - riadky].strany[2] = True
        if vpravo:
            bbox.strany[1] = True
            if (index + 1) % stlpce > 0:
                boxy[index + 1].strany[3] = True
        if dole:
            bbox.strany[2] = True
            if (index + riadky) < len(boxy):
                boxy[index + riadky].strany[0] = True
        if vlavo:
            bbox.strany[3] = True
            if index % stlpce > 0:
                boxy[index - 1].strany[1] = True

        bbox.kontrola_vyhry()
    #updatovanie hry aby sme videli vsetky akcie ktore vykoname
    pygame.display.update()
#vypnutie hry
pygame.quit()