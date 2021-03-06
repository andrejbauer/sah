# šahovnica
# GUI: tukaj se riše in zaznava klike, za pravila povprašamo logiko

# Zvrsti graficnih objektov
POLJE="polje" # ta se nariše enkrat in se potem ne briše več
FIGURA="figura"
PLAVI="plavi"

import tkinter as tk
#import logika
import sah2

def narisi_sahovnico(platno, velikost_polj, odmik):
    '''Nariše šahovnico 8d X 8d. Desno spodaj je belo polje.'''
    x1, y1 = odmik, odmik # določimo odmik
    for i in range(8): # vrstice
        for j in range(8): # stolpci
            barva = ''
            if (i + j) % 2 == 0:
                barva = 'white'
            else:
                barva = 'gray'
            platno.create_rectangle(x1, y1, x1 + velikost_polj, y1 + velikost_polj, fill=barva, tag=POLJE)
            x1 += velikost_polj # naslednji kvadratek v vrsti
        x1, y1 = odmik, odmik + velikost_polj * (i + 1) # premaknemo se eno vrstico navzdol

def narisi_plave(platno, velikost_polj, odmik, plave_tocke):
    '''Nariše šahovnico 8d X 8d. Desno spodaj je belo polje.'''
    for (j,i) in plave_tocke:
        barva = "blue"
        x1 = odmik + j * velikost_polj
        y1 = odmik + i * velikost_polj
        platno.create_rectangle(x1, y1, x1 + velikost_polj, y1 + velikost_polj, fill=barva, tag=PLAVI)




class Sahovnica:
    #print("RAZRED ŠAHOVNICA")

    def __init__(self, master):
        # nastavitve velikosti
        self.velikost_polj = 100
        self.odmik = 30
        self.platno = tk.Canvas(master, width=self.velikost_polj * 10, height=self.velikost_polj * 10)
        self.platno.pack()
        self.prvi_klik = True
        self.dovoljeni_drugi_kliki = []
        self.prvi_klikx = self.prvi_kliky = 0
        self.sah = sah2.sah()
        self.oznacena_figura = None
        # narišemo šahovnico
        narisi_sahovnico(self.platno, self.velikost_polj, self.odmik)
        # registriramo se za klike z miško
        self.platno.bind('<Button-1>', self.klik)
        # naredimo oznako za izpisovanje
        self.okvir_oznake = tk.LabelFrame(self.platno)
        self.okvir_oznake.pack()
        self.izpis_potez = tk.StringVar(value='klikni nekam')
        oznaka_izpis_potez = tk.Label(self.okvir_oznake, textvariable=self.izpis_potez)
        oznaka_izpis_potez.pack()
        x, y = self.odmik + 8 * self.velikost_polj / 2, self.odmik / 2
        self.platno.create_window(x, y, window=self.okvir_oznake, width = 140)
        # self.platno.create_text(600, 20, text=self.izpis_potez.get()) ZAKAJ SE TO NE SPREMINJA?
        self.zacni_igro()
    def klik(self, event):
        if self.prvi_klik:
            #preberemo prvi klik (označimo figuro ki jo želimo premikat)
            i = int((event.y - self.odmik) // self.velikost_polj) # vrstica
            j = int((event.x - self.odmik) // self.velikost_polj) # stolpec
            if sah2.v_sahovnici((j,i)) and (self.sah.slika[j][i] != None) and (self.sah.na_vrsti == self.sah.slika[j][i].barva):
                self.dovoljene_poteze = list(self.sah.slika[j][i].dovoljene_poteze_iterator(self.sah.slika, self.sah.igra))
            else:
                return
            if len(self.dovoljene_poteze) == 0:
                self.prvi_klik = True
                return
            oznaka_izpis_potez = tk.Label(self.okvir_oznake, textvariable=tk.StringVar(value=str(j)+", "+str(i)+'\t1.klik'))
            oznaka_izpis_potez.pack()
            self.prvi_klik = False
            self.prvi_klikx = j
            self.prvi_kliky = i
            #pobarvamo dovoljena polja
            pobarvane_tocke = []
            for poteza in self.dovoljene_poteze:
                xz, yz, xk, yk = poteza
                pobarvane_tocke.append((xk,yk))
            self.prikaz_figur(plave_tocke = pobarvane_tocke)
            return
		#izračunamo dovoljene končne lokacije označene figure. shranimo v dovoljeni_drugi_kliki -seznam
        #preberemo drugi klik
        k = int((event.y - self.odmik) // self.velikost_polj) # vrstica
        l = int((event.x - self.odmik) // self.velikost_polj) # stolpec
        if sah2.v_sahovnici((l,k)) and (self.prvi_klikx, self.prvi_kliky, l, k) in self.dovoljene_poteze:
            self.sah.naredi_potezo((self.prvi_klikx, self.prvi_kliky, l,k))
            self.prvi_klik = True
            oznaka_izpis_potez = tk.Label(self.okvir_oznake, textvariable=tk.StringVar(value=str(l)+", "+str(k)+'\t2.klik'))
            oznaka_izpis_potez.pack()
            self.prikaz_figur()
            return
        self.prvi_klik = True
        self.prikaz_figur()
    def zacni_igro(self):
        '''Prične igro.'''
        self.prikaz_figur()
        # nastavi odštevalnik ure
    def prikaz_figur(self, plave_tocke = []):
        self.platno.delete(FIGURA)
        self.platno.delete(PLAVI)
        narisi_plave(self.platno, self.velikost_polj, self.odmik, plave_tocke)
        bele = self.sah.figure['bel']
        crne = self.sah.figure['crn']
        for figura in bele + crne:
            foto = figura.foto
            x = self.odmik + (figura.x * self.velikost_polj) + self.velikost_polj/2
            y = self.odmik + (figura.y * self.velikost_polj) + self.velikost_polj/2
            foto_id = self.platno.create_image(x, y, image=foto, tag=FIGURA)
            figura.foto_id = foto_id


root = tk.Tk()

partija_saha = Sahovnica(root)

root.mainloop()


#===========================================================#
#                  NASVETI PROFESORJA                       #
#===========================================================#
# matrika je zaradi rekonstrukcije, zato da programer vidi, kaj se dogaja
# IGRA v logiki
# najprej spremeniš v logiki, nato sporočiš GUI, da nariše drugam
# class Figura: x, y, barva -> kar je skupno vsem figuram
# class Kmet(Figura): mozne poteze, slika
