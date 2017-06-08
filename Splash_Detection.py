import pyaudio
import struct
import math
import time
from AudioDevice import *


# TAP_THRESHOLD Ranges
# ------------------------------------------------------------------------------------------------
# TAP_THRESHOLD = 0.003-0.006 (-50dB to -44dB) an obnoxiously loud central heating fan in my house
# TAP_THRESHOLD = 0.010-0.40 (-40dB to -8dB) typing on the same laptop
# TAP_THRESHOLD = 0.10 (-20dB) snapping fingers softly at 1' distance
# TAP_THRESHOLD = 0.60 (-4.4dB) snapping fingers loudly at 1'
# ------------------------------------------------------------------------------------------------

try:
    FISHING_TIME = 25
    DEVICE = get_audio_device('Stereo Mix')
    TAP_THRESHOLD = 0.0005
    FORMAT = pyaudio.paInt16
    SHORT_NORMALIZE = (1.0/32768.0)
    CHANNELS = 1
    RATE = 44100
    INPUT_BLOCK_TIME = 0.01
    INPUT_FRAMES_PER_BLOCK = int(RATE*INPUT_BLOCK_TIME)
except NameError:
    print("Could not find device.\n" + "Make sure 'Stereo Mix' is enabled!")
    exit(1)


def get_rms(block):

    """Get root mean square as a measure of loudness"""

    global SHORT_NORMALIZE

    count = len(block)/2
    format = "%dh" % (count)
    shorts = struct.unpack(format, block)
    sum_squares = 0.0
    for sample in shorts:
        n = sample * SHORT_NORMALIZE
        sum_squares += n*n
    return math.sqrt(sum_squares / count)


def hook_listener():
    print("listening for fish")
    # Open the mic
    stream = pyaudio.PyAudio().open(format=FORMAT,
                                    channels=CHANNELS,
                                    rate=RATE,
                                    input=True,
                                    input_device_index=DEVICE,
                                    frames_per_buffer=INPUT_FRAMES_PER_BLOCK)

    start_time = time.time()
    # Listen until a sound has been detected or time exceed FISHING_TIME
    while time.time() - start_time <= FISHING_TIME:
        try:
            block = stream.read(INPUT_FRAMES_PER_BLOCK)
        except IOError:
            print(IOError)
        loudness = get_rms(block)
        # print(loudness)
        if loudness > TAP_THRESHOLD:
            print("Fish detected!\n"+"Time: ", time.time() - start_time)
            print("loudness", loudness)
            return True
    # Close the mic
    stream.close()
    return False

# hook_listener()
