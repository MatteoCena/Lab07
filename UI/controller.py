import flet as ft
from UI.view import View
from model.model import Model

'''
    CONTROLLER:
    - Funziona da intermediario tra MODELLO e VIEW
    - Gestisce la logica del flusso dell'applicazione
'''

class Controller:
    def __init__(self, view: View, model: Model):
        self._model = model
        self._view = view

        # Variabili per memorizzare le selezioni correnti
        self.museo_selezionato = None
        self.epoca_selezionata = None

    # POPOLA DROPDOWN
    # TODO
    def popola_dropdowns(self):
        """ Legge i dati dal Model/DAO e popola i dropdown della View. """

        # --- Popola Museo Dropdown ---

        # 1. Aggiungi l'opzione "Nessun filtro"
        self._view.dd_museo.options.append(ft.dropdown.Option("Nessun filtro"))

        # 2. Leggi i musei dal database (il Model userà il MuseoDAO)
        musei = self._model.get_all_musei()  # Assumiamo che ritorni oggetti MuseoDTO

        # 3. Aggiungi gli altri musei
        for museo in musei:
            # Uso l'ID come valore e il nome per l'etichetta
            self._view.dd_museo.options.append(ft.dropdown.Option(
                key=museo.id,  # Assumiamo che MuseoDTO abbia un attributo 'id'
                text=museo.nome  # Assumiamo che MuseoDTO abbia un attributo 'nome'
            ))

        # --- Popola Epoca Dropdown ---

        # 1. Aggiungi l'opzione "Nessun filtro"
        self._view.dd_epoca.options.append(ft.dropdown.Option("Nessun filtro"))

        # 2. Leggi le epoche distinte (il Model userà l'ArtefattoDAO)
        epoche = self._model.get_all_epoche()  # Assumiamo che ritorni una lista di stringhe

        # 3. Aggiungi le epoche
        for epoca in epoche:
            self._view.dd_epoca.options.append(ft.dropdown.Option(epoca))

        self._view.update()

    # CALLBACKS DROPDOWN
    # TODO
    def seleziona_museo(self, e):
        """ Aggiorna la variabile di controllo in base alla selezione del museo. """
        # Il valore è l'ID (key) o "Nessun filtro" (value)
        self.museo_selezionato = e.control.value

    def seleziona_epoca(self, e):
        """ Aggiorna la variabile di controllo in base alla selezione dell'epoca. """
        # Il valore è la stringa dell'epoca o "Nessun filtro"
        self.epoca_selezionata = e.control.value

    # AZIONE: MOSTRA ARTEFATTI
    # TODO
    def mostra_artefatti_handler(self, e):
        """ Gestisce il click sul pulsante: recupera gli artefatti e aggiorna la View. """

        # Prepara i valori da passare al Model/DAO
        # Passiamo None se l'utente ha selezionato "Nessun filtro", altrimenti il valore selezionato (ID o stringa epoca)

        filtro_museo = None if self.museo_selezionato == "Nessun filtro" else self.museo_selezionato
        filtro_epoca = None if self.epoca_selezionata == "Nessun filtro" else self.epoca_selezionata

        # 1. Chiedi al Model/DAO di filtrare
        # Assumiamo che la funzione in Model sia: get_artefatti_filtrati(id_museo, epoca)
        try:
            artefatti = self._model.get_artefatti_filtrati(filtro_museo, filtro_epoca)
        except Exception as err:
            self._view.show_alert(f"Errore durante il recupero dei dati: {err}")
            return

        # 2. Aggiorna la ListView nella View

        self._view.lv_artefatti.controls.clear()

        if not artefatti:
            # Nessun artefatto trovato, mostra un alert come richiesto
            self._view.show_alert("⚠️ Nessun artefatto trovato che soddisfi i criteri di filtraggio selezionati.")
            self._view.lv_artefatti.controls.append(ft.Text("Nessun artefatto trovato."))
        else:
            # Popola la lista con gli artefatti
            self._view.lv_artefatti.controls.append(
                ft.Text(f"Trovati {len(artefatti)} artefatti:", weight=ft.FontWeight.BOLD))
            for artefatto in artefatti:
                # Assumiamo che ArtefattoDTO abbia una rappresentazione __str__ o attributi chiari
                testo_artefatto = f"ID: {artefatto.id} | Nome: {artefatto.nome} | Epoca: {artefatto.epoca}"
                self._view.lv_artefatti.controls.append(ft.Text(testo_artefatto))

        self._view.update()
