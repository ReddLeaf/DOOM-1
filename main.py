from model_part1 import TCModel1
from view import TCView
from controller import TCController
from common_types import packets, water, make_packet, make_water
from argparse import ArgumentParser

if __name__ == "__main__":
    parser = ArgumentParser()
    parser.add_argument("-m", "--mode", choices=packets.keys(), required=True)
    parser.add_argument("-w", "--water", choices=water.keys(), required=True)
    args = parser.parse_args()

    mode = make_packet(args.mode)
    water = make_water(args.water)
    model = TCModel1(mode, water)
    view = TCView()
    controller = TCController(model, view)

    controller.run()