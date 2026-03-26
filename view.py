from common_types import Action, CropType

class TCView:
    def show_feedback(self, feedback: bool):
        print("Success!" if feedback else "Failed.")
        print()

    def show_end_day(self):
        print("Day ended.\n")

    def show_grid_status(self, pesos: int, grid: list[list[CropType | None]]):
        print(f"Pesos: {pesos}")
        for line in grid:
            for cell in line:
                print(cell if cell is not None else ".", end="")
            print()

    def show_day(self, day: int):
        print("====\n")
        print(f"Day {day}")

    def ask_for_action(self) -> Action:
        action = ""
        while action not in Action:
            print("Action: ")
            action = input("- ").lower()
        return Action(action)

    def ask_for_crop(self, valid_crops: list[str]) -> str:
        crop = ""
        while crop not in valid_crops:
            print("Crops: " + ", ".join(valid_crops))
            crop = input("- ").lower()
        return crop

    def ask_for_ij(self) -> tuple[int, int]:
        coords: tuple[int, ...] = ()
        while len(coords) != 2:
            print("Location (i, j):")
            try:
                coords = tuple(map(int, input("- ").split()))
            except ValueError:
                ...
        return coords
