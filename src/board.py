import time

import gpiozero as gpio


class NixieHW:
    def __init__(self):
        self._CLK_SLEEP = 0

        # TODO: correct pin numbers
        _SCK_PIN = 23
        _SDO_PIN = 22
        _RCK_PIN = 25
        _EN_PIN  = 26

        self.sck = gpio.OutputDevice(pin=_SCK_PIN, active_high=False, initial_value=True)
        self.sdo = gpio.OutputDevice(pin=_SDO_PIN, active_high=False, initial_value=False)
        self.rck = gpio.OutputDevice(pin=_RCK_PIN, active_high=False, initial_value=True)
        self.en  = gpio.OutputDevice(pin=_EN_PIN,  active_high=True,  initial_value=True)

    def _wr_bit(self, b):
        self.sdo.value = b & 0x1
        self.sck.value = 0
        time.sleep(self._CLK_SLEEP)
        self.sck.value = 1

    def _latch(self):
        self.rck.value = 0
        time.sleep(self._CLK_SLEEP)
        self.rck.value = 1

    def wr_time(self, time_str):
        assert len(time_str) == 4

        # write leading 0 to turn off the final SDO LED
        # after all the clock data has been shifted in
        self._wr_bit(0)

        # write 40 bits of clock data, 10 bits per digit
        for i in range(len(time_str)):
            # reverse digit because shifted data travels from cathode 0 -> cathode 9
            # so if you want to turn on cathode 9, you write 1 followed by 8 0's
            # this is why the "9 - "
            digit = 9 - int(time_str[i])
            for j in range(10):
                if j == digit:
                    self._wr_bit(1)
                else:
                    self._wr_bit(0)

        # once all data is shifted in, pulse the output register clock
        self._latch()
