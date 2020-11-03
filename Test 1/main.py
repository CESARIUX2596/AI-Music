# import pyaudio
# import wave
# import sys


# CHUNK = 1024

# if len(sys.argv) < 2:
#     print("Plays a wave file.\n\nUsage: %s filename.wav" % sys.argv[0])
#     sys.exit(-1)

# wf = wave.open(sys.argv[1], 'rb')

# # instantiate PyAudio (1)
# p = pyaudio.PyAudio()

# # open stream (2)
# stream = p.open(format=p.get_format_from_width(wf.getsampwidth()),
#                 channels=wf.getnchannels(),
#                 rate=wf.getframerate(),
#                 output=True)

# # read data
# data = wf.readframes(CHUNK)

# # play stream (3)
# while len(data) > 0:
#     stream.write(data)
#     data = wf.readframes(CHUNK)

# # stop stream (4)
# stream.stop_stream()
# stream.close()

# # close PyAudio (5)
# p.terminate()


import pyaudio
import time

WIDTH = 2
CHANNELS = 1
RATE = 96600

p = pyaudio.PyAudio()

def callback(in_data, frame_count, time_info, status):
    return (in_data, pyaudio.paContinue)

stream = p.open(format=p.get_format_from_width(WIDTH),
                channels=CHANNELS,
                rate=RATE,
                input=True,
                output=True,
                stream_callback=callback)

stream.start_stream()

while stream.is_active():
    time.sleep(.1)
    # print('test')

stream.stop_stream()
stream.close()

p.terminate()