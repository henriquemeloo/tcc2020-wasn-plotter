import json
import serial

from matplotlib import animation
import matplotlib.pyplot as plt
import numpy as np


def create_fig():
    with open('nodes_coords.json') as file:
        nodes_coords = np.array(json.load(file)['nodes_coords'])
    for i in range(len(nodes_coords)):
        plt.plot(nodes_coords[i][0], nodes_coords[i][1], 'ro', markersize=18)
        plt.annotate(f'{i}', (nodes_coords[i][0], nodes_coords[i][1]))
    plt.gca().set_aspect('equal', adjustable='box')
    plt.grid()
    plt.xlabel('$x$ (m)')
    plt.ylabel('$y$ (m)')
    xlim = 1.1 * np.array(np.min(nodes_coords[:,0]), np.max(nodes_coords[:,0]))
    ylim = 1.1 * np.array(np.min(nodes_coords[:,1]), np.max(nodes_coords[:,1]))
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


def animate(nodes_coords):
    if len(fig.axes[0].lines) > 4:
        fig.axes[0].lines.pop(-1)
    source_coords = parse_serial()
    plt.plot(source_coords[0], source_coords[1], 'bo', markersize=18)


def main():
    ani = animation.FuncAnimation(fig, animate, init_func=create_fig)
    plt.show()


if __name__ == '__main__':
    ser = serial.Serial()
    ser.port = '/dev/ttyACM1' #Arduino serial port
    ser.baudrate = 115200
    ser.timeout = 100 #specify timeout when using readline()
    ser.open()
    if ser.is_open==True:
        print("\nAll right, serial port now open. Configuration:\n")
        print(ser, "\n") #print serial parameters
    fig = plt.figure(figsize=(8, 8))
    main()
