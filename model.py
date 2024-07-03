import copy

from database.DAO import DAO


class Model:
    def __init__(self):
        self._solBest = []
        self._tot_persone = -1
        self._disservizio_tot = 0
        self._listNerc = None
        self._listEvents = None
        self.loadNerc()



    def worstCase(self, nerc, maxY, maxH):
        # TO FILL
        self._solBest = []
        self._tot_persone = 0
        self._disservizio_tot = 0
        self._listEvents = self.loadEvents(nerc)
        self.ricorsione([], maxY, maxH, 0)


    def ricorsione(self, parziale, maxY, maxH, pos):
        # TO FILL

        persone = self.calcola_persone(parziale)
        if persone > self._tot_persone:
            self._solBest = copy.deepcopy(parziale)
            self._tot_persone = persone
            ore_tot = self.calcola_disservizio(parziale)
            self._disservizio_tot = ore_tot


        for evento in self._listEvents[pos:]:
            if evento not in parziale:
                parziale.append(evento)
                if self.ammissibile(parziale, maxY, maxH):
                    self.ricorsione(parziale, maxY, maxH, pos + 1)
                parziale.pop()




    def ammissibile(self, parziale, maxY, maxH):

        if len(parziale) == 0:
            return True

        primo_anno = parziale[0].date_event_began.year
        ultimo_anno = parziale[-1].date_event_finished.year

        disservizio = self.calcola_disservizio(parziale)
        if disservizio > maxH:
            return False

        #for evento in parziale:
        if (ultimo_anno - primo_anno) > maxY:
            return False

        return True


    def calcola_disservizio(self, parziale):
        disservizio = 0
        for evento in parziale:
            disservizio += (evento.date_event_finished.timestamp() - evento.date_event_began.timestamp())

        disservizio = disservizio/3600

        return disservizio


    def calcola_persone(self, parziale):
        persone = 0
        for evento in parziale:
            persone += evento.customers_affected

        return persone


    def loadEvents(self, nerc):
        self._listEvents = DAO.getAllEvents(nerc)
        return self._listEvents

    def loadNerc(self):
        risultati = self._listNerc = DAO.getAllNerc()
        return risultati


    @property
    def listNerc(self):
        return self._listNerc