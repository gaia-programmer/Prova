import flet as ft


class Controller:
    def __init__(self, view, model):
        # the view, with the graphical elements of the UI
        self._view = view
        # the model, which implements the logic of the program and holds the data
        self._model = model


    def fillDD(self):
        anni = [2015,2016,2017,2018]
        for a in anni:
            self._view._ddYear1.options.append(ft.dropdown.Option(str(a)))
        self._view.update_page()

        brand= self._model.getBrands()
        for a in brand:
            self._view._ddBrand.options.append(ft.dropdown.Option(str(a)))
        self._view.update_page()

    def handleBuildGraph(self, e):
        self._view._txt_result.controls.clear()

        if self._view._ddBrand.value is None:
            self._view._txt_result.controls.append(ft.Text(f"brand not selected", color ="red"))
            self._view.update_page()
            return

        if self._view._ddYear1.value is None:
            self._view._txt_result.controls.append(ft.Text(f"year not selected", color="red"))
            self._view.update_page()
            return


        self._model.buildGraph(self._view._ddBrand.value, int(self._view._ddYear1.value))
        n,a = self._model.graphdettails()
        self._view._txt_result.controls.append(ft.Text(f"numero nodi: {n}"))
        self._view._txt_result.controls.append(ft.Text(f"numero archi: {a}"))
        best, lista = self._model.bestPeso()
        for b in best:
            self._view._txt_result.controls.append(ft.Text(f"{b[0]}, {b[1]}  peso: {b[2]["weight"]}"))
        for l in lista:
            self._view._txt_result.controls.append(ft.Text(f"{l}"))


        self._view.update_page()

    def handlePrintDetails(self, e):
        pass

    def handleCercaTeamSfortunati(self, e):
        pass
