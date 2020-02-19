import board
#######################
# CONFIGURATION
#######################

# temps maximum pour repondre, en secondes, apres le go
TEMPS_MAXIMUM = 5

# temps d'inactivite pour lancer l'animation, en secondes
INACTIVITE = 20

# couleur des equipes
# [vert, jaune, rouge, blanc]

couleurs_equipes = [(0,40,0),(30,30,00),(40,0,0),(30,30,30)]


#######################
# CONFIGURATION
#######################

# Bibliotheques a importer
import time
import touchio
from adafruit_circuitplayground import cp


# Initialisation des touchpads
tA1 = touchio.TouchIn(board.A1)
tA2 = touchio.TouchIn(board.A2)
tA4 = touchio.TouchIn(board.A4)
tA5 = touchio.TouchIn(board.A5)
tA6 = touchio.TouchIn(board.A6)


# liste pour definir l'animation
# couleur = (rouge, vert, bleu)
# [(couleur1), (couleur2), nombre d'etapes,etat actuel]

animation = [(40,0,0),(0,0,0),60,0]

# fonction pour animer les pixels en cas d'inactivite.

def animer():
    global animation
    etapes = animation[2]
    pas = animation[3]
    r1, v1, b1 = animation[0]
    r2, v2, b2 = animation[1]
    for i in range(0,10):
        pas = animation[3]
        difference = (etapes/5)*i
        pas += difference
        if pas > etapes*2:
            pas = pas - etapes*2
        if pas > etapes:
            pas = etapes - (pas - etapes)
        # calcul du rouge
        r = int(r1 + ((r2 - r1)/etapes)*pas)
        # calcul du vert
        v = int(v1 + ((v2 - v1)/etapes)*pas)
        # calcul du bleu
        b = int(b1 + ((b2 - b1)/etapes)*pas)
        cp.pixels[i] = (r,v,b)
    animation[3] += 1
    if animation[3] >= animation[2]*2:

        animation[3] = 0
    pass


# fonction principale
# retourne une liste avec les temps de chaque équipe.
def quizz():
    # Variables d'état
    A1_touche = False
    A2_touche = False
    A4_touche = False
    A5_touche = False
    A6_touche = False

    go = False

    temps_equipes = [0,0,0,0]
    temps_premier = None
    debut = time.monotonic_ns() // 1000000

    # boucle infinie
    while True:
        # équipe 1
        if A1_touche == False and tA1.value :
            t = time.monotonic_ns() // 1000000
            if go:
                if temps_premier == None:
                    temps_premier = t
                if temps_equipes[0] == 0:
                    temps_equipes[0] = t
            A1_touche = True
        if A1_touche and tA1.value == False:
            #print('On ne touche plus A1!')
            #cpb.play_tone(440, 0.5)
            A1_touche = False


        # équipe 2
        if A2_touche == False and tA2.value:
            t = time.monotonic_ns() // 1000000
            if go:
                if temps_premier == None:
                    temps_premier = t
                if temps_equipes[1] == 0:
                    temps_equipes[1] = t
            A2_touche = True
        if A2_touche and tA2.value == False:
            #print('On ne touche plus A2!')
            #cpb.play_tone(294, 0.5)
            A2_touche = False

        # équipe 3
        if A5_touche == False and tA5.value:
            t = time.monotonic_ns() // 1000000
            if go:
                if temps_premier == None:
                    temps_premier = t
                if temps_equipes[2] == 0:
                    temps_equipes[2] = t
            A5_touche = True
        if A5_touche and tA5.value == False:
            #print('On ne touche plus A5!')
            #cpb.play_tone(440, 0.5)
            A5_touche = False

        # équipe 4
        if A6_touche == False and tA6.value:
            t = time.monotonic_ns() // 1000000
            if go:
                if temps_premier == None:
                    temps_premier = t
                if temps_equipes[3] == 0:
                    temps_equipes[3] = t
            A6_touche = True
        if A6_touche and tA6.value == False:
            #print('On ne touche plus A6!')
            #cpb.play_tone(294, 0.5)
            A6_touche = False

        # Prof
        if A4_touche == False and tA4.value:
            #print('On touche A4!')
            A4_touche = True
        if A4_touche and tA4.value == False and go == False:
            #cp.play_tone(587, 0.4)
            if cp.switch:
                cp.play_file("/sons/smb_powerup.wav")
            cp.pixels.fill((0, 0, 30))
            # reinitialisation de l'animation
            animation[3] = 0
            temps_go = time.monotonic_ns() // 1000000
            go = True
            temps_premier = None
            print("GOOOOO")
            A4_touche = False

        # allumer la LED rouge si la switch est a off (son muet).
        cp.red_led = not cp.switch
        # condition pour finir la boucle : go == True et un temps a été enregistré il y a plus d'une seconde.
        if go and temps_premier != None and time.monotonic_ns() // 1000000 - temps_premier > 1000 :
            cp.pixels.fill((0, 0, 0))
            #fin de la boucle
            break
        # temps maximal atteint sans reponse
        if go and time.monotonic_ns() // 1000000 - temps_go > TEMPS_MAXIMUM*1000:
            break

        # inactivite
        if go == False and  time.monotonic_ns() // 1000000 - debut > INACTIVITE*1000:
            animer()
    return temps_equipes

def annoncer_vainqueur(temps_equipes):
    global couleurs_equipes
    # bipper le bon code et allumer les led correspondantes
    pixels_equipes = [(5,6,7),(7,8,9),(0,1,2),(2,3,4)]

    print(temps_equipes)
    sans_reponse = []
    vainqueur = None
    deuxieme = None
    m1 = None
    m2 = None
    for i, t in enumerate(temps_equipes):
        if t == 0:
            sans_reponse.append(i+1)
            temps_equipes[i] = t = time.monotonic_ns() // 1000000 + 1000
        if m1 == None or t <= m1:
            m1, m2 = t, m1
        elif m2 == None or t < m2:
            m2 = t
    if len(sans_reponse) == 4:
        #Pas de vainqueur, pas de réponse
        cp.pixels.fill((20, 10, 0))
        animation[0] = (40, 0, 0)
        animation[3] = 0
        if cp.switch:
            cp.play_file("/sons/smb_bowserfalls.wav")
        else:
            time.sleep(1)
        cp.pixels.fill((40, 0, 0))
        return
    vainqueur = temps_equipes.index(m1)+1

    if len(sans_reponse) <= 2:
        deuxieme = temps_equipes.index(m2)+1

    print("L'equipe", vainqueur, "gagne")

    print("Sans reponse :", sans_reponse)
    # le switch en dessous des bouttons rends muet et allume la led rouge D13
    if cp.switch:
        for _ in range(1,vainqueur+1):
            cp.play_file("/sons/smb_coin.wav")


    # allumer les bons pixels de la bonne couleur
    for p in pixels_equipes[vainqueur-1]:
        cp.pixels[p] = couleurs_equipes[vainqueur-1]
    animation[0] = couleurs_equipes[vainqueur-1]
    animation[3] = 0

    # si il y a un deuxieme, allumer juste un pixel plus faiblement.
    if deuxieme != None:
        print("L'equipe", deuxieme, "est 2e : +", m2-m1 ,"millisecondes" )
        dim_color = map(lambda x: x//6, couleurs_equipes[deuxieme-1])
        cp.pixels[pixels_equipes[deuxieme-1][1]] = tuple(dim_color)

# boucle infinie
while True:
    temps_equipes = quizz()
    annoncer_vainqueur(temps_equipes)
