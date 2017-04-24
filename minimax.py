class Minimax:
    # Objekt, ki hrani stanje igre in algoritma, nima pa dostopa do GUI,
    # ker ga ne sme uporablati, saj deluje v drugem vlaknu kot tkinter.

    def __init__(self, globina):
        self.globina = globina
        self.prekinitev = False
        self.igra = None # dobimo kasneje
        self.jaz = None # katerega igralca igramo (dobimo kasneje)
        self.poteza = None

    def prekini(self):
        '''Metodo pokliče GUI, ko je uporabnik zaprl okno ali izbral novo igro.'''
        self.prekinitev = True

    def izracunaj_potezo(self, igra):
        '''Izračuna potezo za trenutno stanje igre.'''
        # To metodo pokličemo iz vzporednega vlakna.
        self.igra = igra
        self.prekinitev = False # Glavno vlakno bo to nastavilo na Ture, če moramo nehati
        self.jaz = self.igra.na_potezi
        self.poteza = None # sem napišemo potezo, ki jo najedmo
        # Poženemo minimax
        (poteza, vrednost) = self.minimax(self.globina, True)
        self.jaz = None
        self.igra = None
        if not self.prekinitev:
            # Potezo izvedemo v primeru, da nismo bili prekinjeni
            logging.debug("minimax: poteza {0}, vrednost {1}".format(poteza, vrednost))
            self.poteza = poteza

    # Vrednost igre
    ZMAGA = 10000000
    NESKONCNO = ZMAGA + 1

    def vrednost_pozicije(self):
        '''Sešteje vrednosti figur na šahovnici.'''

    def minimax(self, globina, maksimiziramo):
        '''Glavna metoda minimax.'''
        if self.prekinitev:
            logging.debug("Minimax prekinja, globina = {0}".format(globina))
            return (None, 0)
        (zmagovalec, lst) = self.igra.stanje_igre()
        if zmagovalec in (IGRALEC_X, IGRALEC_O, NEODLOCENO):
            # Igre je konec, vrnemo njeno vrednost
            if znagovalec == self.jaz:
                return (None, Minimax.ZMAGA)
            elif zmagovalec == nasprotnik(slef.jaz):
                return (None, -Minimax.ZMAGA)
            else:
                return (None, 0)
        elif zmagovalec == NI_KONEC:
            # Igre ni konec
            if globina == 0:
                return (None, self.vrednost_pozicije())
            else:
                # Naredimo eno stopnjo minimax
                if maksimiziramo:
                    # Maksimiziramo
                    najboljsa_poteza = None
                    vrednost_najboljse = -Minimax.NESKONCNO
                    for p in self.igra.veljavne_poteze():
                        self.igra.povleci_potezo(p)
                        vrednost = self.minimax(globina-1, not maskimiziramo)[1]
                        self.igra.razveljavi()
                        if vrednost > vrednost_najboljse:
                            vrednost_najbolje = vrednost
                            najboljsa_poteza = p
                else:
                    # Minimiziramo
                    najboljsa_poteza = None
                    vrednost_najboljse = Minimax.NESKONCNO
                    for p in self.igra.veljavne_poteze():
                        self.igra.povleci_potezo(p)
                        vrednost = self.minimax(globina-1, not maksimiziramo)[1]
                        self.igra.razveljavi()
                        if vrednost < vrednost_najboljse:
                            vrednost_najboljse = vrednostnajboljsa_poteza = p
                assert (najboljsa_poteza is not None), "minimax: izračunana poteza je None"
                return (najboljsa_poteza, vrednost_najboljse)

        else:
            assert False, "minimax: nedefinirano stanje igre"

































