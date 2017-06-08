import pyaudio

# Return device index of string "device"
# Useful for automatic DEVICE detection
# Set "print_dev" = True to print all devices.


def get_audio_device(device, print_dev=False):
    device_index = None
    # List all audio input devices
    p = pyaudio.PyAudio()
    i = 0
    n = p.get_device_count()
    while i < n:
        dev = p.get_device_info_by_index(i)
        if dev['maxInputChannels'] > 0:
            if print_dev is True:
                print(str(i)+'. '+dev['name'])
            if device in dev['name']:
                device_index = i
                break
        i += 1
    p.terminate()
    if device_index is None:
        raise NameError
    return device_index
