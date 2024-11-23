import random

import config


class Algorithm:
    def get_path(self, state):
        pass


class ExampleAlgorithm(Algorithm):
    def get_path(self, state):
        path = []
        while not state.is_goal_state():
            possible_actions = state.get_legal_actions()


            action = possible_actions[random.randint(0, len(possible_actions) - 1)]
            path.append(action)
            state = state.generate_successor_state(action)
        return path


class Cvor:

    def __init__(self, stanje, putanja, id, prAkcije = 0, cena=0):
        self.stanje = stanje
        self.putanja = putanja
        self.id = id
        self.cena = cena
        self.prioritet = prAkcije
    #metoda __lt__ sluzi da kaze kako ce po kom fildu da se porede
    def __lt__(self, other):
        if self.cena != other.cena:
            return self.cena < other.cena
        else:
            return self.prioritet <= other.prioritet

class Blue(Algorithm):
    vec_poseceno = set()
    stek = []

    def get_path(self, state):

        putanjaDoCvora = []
        idStanja = state.get_state('S')
        koren = Cvor(state, putanjaDoCvora, idStanja)
        self.stek.append(koren)

        while not self.stek[-1].stanje.is_goal_state():
            # print("da2")
            vrhSteka = self.stek.pop()

            # print(type(putanjaDoTrenutnogStanja))
            if (vrhSteka.id in self.vec_poseceno):
                continue
            # mozda bi provera da li je poseceno stanje mogla i u okviru for petlje da bi se manje zauzelo memorije
            # ali onda traje simulacija duze jer vrv proverava i za stanja koja nikad nece biti izvucena jer se doslo do res?
            self.vec_poseceno.add(vrhSteka.id)
            moguceAkcije = vrhSteka.stanje.get_legal_actions()

            for i in range(len(moguceAkcije)):
                # print(akcija)
                sledeceStanje = vrhSteka.stanje.generate_successor_state(moguceAkcije[len(moguceAkcije) - i - 1])
                # if sledeceStanje.get_state('S') in self.vec_poseceno:
                #   continue
                novaPutanja = list(vrhSteka.putanja)
                novaPutanja.append(moguceAkcije[len(moguceAkcije) - i - 1])

                self.stek.append(Cvor(sledeceStanje, novaPutanja, sledeceStanje.get_state('S')))

        return self.stek[-1].putanja


class Red(Algorithm):
    vec_poseceno = set()
    red = []

    def get_path(self, state):

        putanjaDoCvora = []
        idStanja = state.get_state('S')
        koren = Cvor(state, putanjaDoCvora, idStanja)
        self.red.append(koren)

        while not self.red[0].stanje.is_goal_state():
            # print("da2")
            vrhSteka = self.red.pop(0)
            # print(vrhSteka.stanje)
            if (vrhSteka.id in self.vec_poseceno):
                continue

            # print(type(putanjaDoTrenutnogStanja))

            self.vec_poseceno.add(vrhSteka.id)
            moguceAkcije = vrhSteka.stanje.get_legal_actions()

            for i in range(len(moguceAkcije)):
                # print(moguceAkcije[i])
                sledeceStanje = vrhSteka.stanje.generate_successor_state(moguceAkcije[i])

                novaPutanja = list(vrhSteka.putanja)
                # mora izgleda neko kopiranje da se izvrsi ne sme da se dele reference
                novaPutanja.append(moguceAkcije[i])

                self.red.append(Cvor(sledeceStanje, novaPutanja, sledeceStanje.get_state('S')))

        return self.red[0].putanja


from queue import PriorityQueue


class Black(Algorithm):
    vec_poseceno = set()
    red = PriorityQueue()

    def get_path(self, state):

        putanjaDoCvora = []
        idStanja = state.get_state('S')
        koren = Cvor(state, putanjaDoCvora, idStanja, 0)
        self.red.put(koren)

        while not self.red.queue[0].stanje.is_goal_state():
            # print("da2")
            vrhSteka = self.red.get()

            # print(type(putanjaDoTrenutnogStanja))
            if (vrhSteka.id in self.vec_poseceno):
                continue
            self.vec_poseceno.add(vrhSteka.id)
            moguceAkcije = vrhSteka.stanje.get_legal_actions()
            deca = []
            for i in range(len(moguceAkcije)):
                prioritetAkcije = self.odrediPrioritetAkcije(moguceAkcije[i])
              #  print(moguceAkcije[i])
              #  print(prioritetAkcije)
                cena = vrhSteka.stanje.get_action_cost(moguceAkcije[i])

                # print(moguceAkcije[i])
                sledeceStanje = vrhSteka.stanje.generate_successor_state(moguceAkcije[i])

                novaPutanja = list(vrhSteka.putanja)
                novaPutanja.append(moguceAkcije[i])
                cena = vrhSteka.cena + cena
                cvor = Cvor(sledeceStanje, novaPutanja, sledeceStanje.get_state('S'), prioritetAkcije, cena)
                deca.append(cvor)
            deca = sorted(deca, key=lambda x: x.cena) #sad kad imas p. red vrlo upitno da li ti i treba ova linija ali ne usporava mnogo
            for i in range(len(deca)):
                self.red.put(deca[i])
            # self.red = sorted(self.red, key=lambda x: x.cena, reverse=False)

        return self.red.get().putanja

    def odrediPrioritetAkcije(self, akcija):
        if akcija[0][0] != akcija[1][0]: #menjas red (sever ili jug)
            if akcija[1][0] < akcija[0][0]:
                return 1 # sever, najveci prior
            else:
                return 3 # jug
        elif akcija[0][1] != akcija[1][1]: #menja se kolona, istok ili zapad
            if akcija[1][1] > akcija[0][1]: #ako sam otisao na vecu kolonu
                return 2 #istok
            else:
                return 4 #zapad

class White(Algorithm):
    vec_poseceno = set()
    red = PriorityQueue()

    def get_path(self, state):
        # print(state.goals)
        pozicijeCilja = []
        kopijaCiljeva = state.goals
        pozicija = 0
        while kopijaCiljeva:
            flag = kopijaCiljeva & 1
            if flag:
                pozicijeCilja.append(pozicija)
            kopijaCiljeva = kopijaCiljeva >> 1
            pozicija = pozicija + 1
        for i in range(len(pozicijeCilja)):
            vrsta = pozicijeCilja[i] // config.N  # broj kolona odredjuje duzinu vrste zato  sa N delis
            kolona = pozicijeCilja[i] % config.N
            pozicijeCilja[i] = (vrsta, kolona)
        # print(pozicijeCilja)

        # HEURISTIKA ZA KOREN?

        putanjaDoCvora = []
        idStanja = state.get_state('S')
        koren = Cvor(state, putanjaDoCvora, idStanja, 0)
        self.red.put(koren)

        while not self.red.queue[0].stanje.is_goal_state():
            # print("da2")
            vrhSteka = self.red.get()

            # print(type(putanjaDoTrenutnogStanja))
            if (vrhSteka.id in self.vec_poseceno):
                continue
            self.vec_poseceno.add(vrhSteka.id)
            moguceAkcije = vrhSteka.stanje.get_legal_actions()
            deca = []
            for i in range(len(moguceAkcije)):
                prioritetAkcije = self.odrediPrioritetAkcije(moguceAkcije[i])
                cena = vrhSteka.stanje.get_action_cost(moguceAkcije[i])

                # print(moguceAkcije[i])
                sledeceStanje = vrhSteka.stanje.generate_successor_state(moguceAkcije[i])
                pozicijeBrodova = self.dohvatiPozicijeBrodova(sledeceStanje)
                # print(pozicijeBrodova)
                zauzeteGaraze = []
                sveHeuristika = []
                for k in range(len(pozicijeBrodova)):
                    minTrenutniBrod = 999
                    zauzeteGaraze.append(0)  # cisto da bude inicijalizovan odgovarajuci element liste
                    sveHeuristika.append(0)
                    for j in range(len(pozicijeCilja)):
                        # print("menHeten")
                        # print(self.menHetenDistanca(pozicijeBrodova[k], pozicijeCilja[j]))
                        if self.menHetenDistanca(pozicijeBrodova[k],
                                                 pozicijeCilja[j]) < minTrenutniBrod and pozicijeCilja[
                            j] not in zauzeteGaraze:
                            minTrenutniBrod = self.menHetenDistanca(pozicijeBrodova[k], pozicijeCilja[j])
                            zauzeteGaraze[k] = pozicijeCilja[j]

                            sveHeuristika[k] = self.menHetenDistanca(pozicijeBrodova[k], pozicijeCilja[j])
                        #  print("cena")
                        # print(sveHeuristika[i])

                heuristika = 0
                for c in sveHeuristika:
                    heuristika += c

                novaPutanja = list(vrhSteka.putanja)
                novaPutanja.append(moguceAkcije[i])
                cena = vrhSteka.cena + cena + heuristika

                cvor = Cvor(sledeceStanje, novaPutanja, sledeceStanje.get_state('S'), prioritetAkcije, cena)
                deca.append(cvor)
            # mozda bi radilo brze ako ovde stavis neki prioritetni red/heap?
            deca = sorted(deca, key=lambda x: x.cena)
            for i in range(len(deca)):
                self.red.put(deca[i])
            # self.red = sorted(self.red, key=lambda x: x.cena, reverse=False)

        return self.red.queue[0].putanja

    def dohvatiPozicijeBrodova(self, stanje):
        pozicijeBrodova = []
        kopijeBrodova = stanje.spaceships
        pozicija = 0
        while kopijeBrodova:
            flag = kopijeBrodova & 1
            if flag:
                pozicijeBrodova.append(pozicija)
            kopijeBrodova = kopijeBrodova >> 1
            pozicija = pozicija + 1
        for i in range(len(pozicijeBrodova)):
            vrsta = pozicijeBrodova[i] // config.N  # broj kolona odredjuje duzinu vrste zato  sa N delis
            kolona = pozicijeBrodova[i] % config.N
            pozicijeBrodova[i] = (vrsta, kolona)
        # print(pozicijeBrodova)
        return pozicijeBrodova

    def menHetenDistanca(self, torka1, torka2):
        return abs(torka1[0] - torka2[0]) + abs(torka1[1] - torka2[1])

    def odrediPrioritetAkcije(self, akcija):
        if akcija[0][0] != akcija[1][0]: #menjas red (sever ili jug)
            if akcija[1][0] < akcija[0][0]:
                return 1 # sever, najveci prior
            else:
                return 3 # jug
        elif akcija[0][1] != akcija[1][1]: #menja se kolona, istok ili zapad
            if akcija[1][1] > akcija[0][1]: #ako sam otisao na vecu kolonu
                return 2 #istok
            else:
                return 4 #zapad
