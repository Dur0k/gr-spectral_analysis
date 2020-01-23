from distutils.version import StrictVersion
from PyQt5 import Qt
import sys
import signal
from time import sleep
import numpy
from withall_sine import top_block

#tb = top_block()
#tb.start()
#tb.stop()
#tb.wait()
#tb.stop()
#tb.wait()
#freq = input('Frequency: ')
#tb.set_freq(float(freq))
#tb.start()

def main(top_block_cls=top_block, options=None):
    tb = top_block_cls()
    def sig_handler(sig=None, frame=None):
        tb.stop()
        tb.wait()
        sys.exit(0)

    signal.signal(signal.SIGINT, sig_handler)
    signal.signal(signal.SIGTERM, sig_handler)

    while True:
        freq = input('Frequency: ')
        tb.set_freq(float(freq))
        tb.start()
        sleep(5)
        tb.stop()
        tb.wait()
    try:
        input('Press Enter to quit: ')
    except EOFError:
        pass
    




main()
