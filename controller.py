from view import TCView
from model_part1 import TCModel1
from common_types import Action


class TCController:
    def __init__(self, model: TCModel1, view: TCView) -> None:
        self._model = model
        self._view =  view

    def run(self):
        model = self._model
        view = self._view

        while True:
            view.show_day(model.day)
            view.show_grid_status(model.pesos, model.grid)
            next = False
            while not next:
                fb = None
                act = view.ask_for_action()
                match act:
                    case Action.PLANT:
                        crop = view.ask_for_crop(model.valid_crops)
                        i, j = view.ask_for_ij()
                        fb = model.plant(crop, i, j)
                    case Action.WATER:
                        i, j = view.ask_for_ij()
                        fb = model.water(i, j)
                    case Action.HARVEST:
                        fb = model.harvest()
                    case Action.GRID_STATUS:
                        view.show_grid_status(model.pesos, model.grid)
                    case Action.NEXT_DAY:
                        view.show_end_day()
                        model.next_day()
                        next = True

                if fb is not None:
                    view.show_feedback(fb)
