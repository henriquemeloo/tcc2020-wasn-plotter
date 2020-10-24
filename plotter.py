from functools import partial
import argparse
import json

from matplotlib import animation
import matplotlib.pyplot as plt
import numpy as np
import serial


def create_fig(nodes_coords):
    for i in range(len(nodes_coords)):
        plt.plot(nodes_coords[i][0], nodes_coords[i][1], 'ro', markersize=18)
        plt.annotate(f'{i}', (nodes_coords[i][0], nodes_coords[i][1]))
    plt.gca().set_aspect('equal', adjustable='box')
    plt.grid()
    plt.xlabel('$x$ (m)')
    plt.ylabel('$y$ (m)')
    xlim = np.array(
        np.min(nodes_coords[:,0]) - .1*np.min(nodes_coords[:,0]),
        np.max(nodes_coords[:,0]) + .1*np.max(nodes_coords[:,0])
    )
    ylim = np.array(
        np.min(nodes_coords[:,1]) - .1*np.min(nodes_coords[:,1]),
        np.max(nodes_coords[:,1]) + .1*np.max(nodes_coords[:,1])
    )
    plt.xlim(xlim)
    plt.ylim(ylim)


def parse_serial():
    line = ser.readline()
    print(line)
    str_ = str(line).replace('(', ' ').replace(')', ' ').replace(',', ' ').split()
    source_coords = []
    for _ in str_:
        try:
            source_coords.append(float(_))
        except ValueError:
            pass
    if len(source_coords) < 2:
        return [0, 0]
    return source_coords


def animate(_):
    if len(fig.axes[0].lines) > 4:
        fig.axes[0].lines.pop(-1)
    source_coords = parse_serial()
    plt.plot(source_coords[0], source_coords[1], 'bo', markersize=18)


def main():
    parser = argparse.ArgumentParser(description='Plot WASN localization.')
    parser.add_argument('--nodes_coords', default='nodes_coords.json',
                        type=str, nargs='?',
                        help='path to JSON containing nodes coords.')
    parser.add_argument('--port', default='/dev/ttyACM0',
                        type=str, nargs='?',
                        help='port to which Arduino is connected.')
    parser.add_argument('--baudrate', default=115200, type=int, nargs='?',
                        help='baudrate used in communication')
    parser.add_argument('--timeout', default=100, type=int, nargs='?',
                        help='timeout used in readlines')
    parser.add_argument('--video', type=str, nargs='?',
                        help='path to output video of figure')

    args = parser.parse_args()
    global ser
    ser = serial.Serial()
    ser.port = args.port
    ser.baudrate = args.baudrate
    ser.timeout = args.timeout
    ser.open()
    if ser.is_open==True:
        print("\nSerial port now open. Configuration:\n")
        print(ser, "\n")
    global fig
    fig = plt.figure(figsize=(8, 8))
    with open('nodes_coords.json') as file:
        nodes_coords = np.array(json.load(file)['nodes_coords'])
    ani = animation.FuncAnimation(
        fig, animate, init_func=partial(create_fig, nodes_coords)
    )
    if args.video:
        Writer = animation.writers['ffmpeg']
        writer = Writer(bitrate=1800)
        ani.save(args.video, writer=writer)
    plt.show()


if __name__ == '__main__':
    main()
