import flet as ft

from model.nerc import Nerc


class Controller:
    def __init__(self, view, model):
        # the view, with the graphical elements of the UI
        self._view = view
        # the model, which implements the logic of the program and holds the data
        self._model = model
        self._idMap = {}
        self.fillIDMap()

    def handleWorstCase(self, e):
        # TO FILL
        nerc = self._view._ddNerc.value
        anni = float(self._view._txtYears.value)
        ore = float(self._view._txtHours.value)

        self._view._txtOut.controls.clear()

        if nerc is None or ore is None or anni is None:
            self._view.create_alert("Inserire tutti i campi")
            return

        self._model.worstCase(nerc, anni, ore)

        risultato = self._model._solBest

        self._view._txtOut.controls.append(ft.Text(f"Tot people affected: {self._model._tot_persone}"))
        self._view._txtOut.controls.append(ft.Text(f"Tot hours of outage: {self._model._disservizio_tot}"))

        for r in risultato:
            self._view._txtOut.controls.append(ft.Text(f"id={r.id}, customers_affected={r.customers_affected}, start_time={r.date_event_began}, end_time={r.date_event_finished}"))

        self._view.update_page()



    def fillDD(self):
        nercList = self._model.listNerc

        for n in nercList:
            self._view._ddNerc.options.append(ft.dropdown.Option(key=n._id, text=n._value))
        self._view.update_page()

    def fillIDMap(self):
        values = self._model.listNerc
        for v in values:
            self._idMap[v.value] = v
