import sounddevice as sd
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation
import numpy as np
import queue
import sys
# Constant values
CHANNELS = 1            # Mono because why stereo?
DOWN_SAMPLE = 10        # Display every Nth sample
WINDOW = 200            # Window Size
SAMPLE_RATE = 44100     # 44.1k Samplerate
INTERVAL = 15           # Interval to update plot in ms
INPUT_DEVICE = 1        # Current input device for my Scarlet 2i2 in my pc
OUTPUT_DEVICE = 5       # Current output device for my Scarlet 2i2 in my pc

q = queue.Queue()

_channels = CHANNELS

mapping = [c - 1 for c in range(_channels)]


def audio_callback(input_data, frames, time, status):
    if status:
        print(status, file=sys.stderr)
    q.put(input_data[::DOWN_SAMPLE, mapping])


def update_plot(frame):
    global plotdata
    while True:
        try:
            data = q.get_nowait()
        except queue.Empty:
            break
        shift = len(data)
        plotdata = np.roll(plotdata, -shift, axis=0)
        plotdata[-shift:, :] = data
    for column, line in enumerate(lines):
        line.set_ydata(plotdata[:, column])
    return lines


try:
    length = int(WINDOW * SAMPLE_RATE / (1000 * DOWN_SAMPLE))
    plotdata = np.zeros((length, CHANNELS))

    fig, ax = plt.subplots()
    lines = ax.plot(plotdata)
    if (CHANNELS > 1):
        ax.legend(['channel {}'.format(c) for c in range(_channels)],
                  loc='lower left', ncol=CHANNELS)
    ax.axis((0, len(plotdata), -1, 1))
    ax.set_yticks([0])
    ax.yaxis.grid(True)
    ax.tick_params(bottom=False, top=False, labelbottom=False,
                   right=False, left=False, labelleft=False)
    fig.tight_layout(pad=0)

    # Here is where the magic happens
    stream = sd.InputStream(
        device=INPUT_DEVICE, channels=CHANNELS, samplerate=SAMPLE_RATE, callback=audio_callback)
    ani = FuncAnimation(fig, update_plot, interval=INTERVAL, blit=True)
    with stream:
        plt.show()
except Exception as e:
    print(e)
