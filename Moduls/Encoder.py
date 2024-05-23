import RPi.GPIO as GPIO

class RotaryEncoder:
    def __init__(self, pin_a, pin_b):
        self.pin_a = pin_a
        self.pin_b = pin_b
        self.position = 0

        GPIO.setmode(GPIO.BCM)
        GPIO.setup(self.pin_a, GPIO.IN, pull_up_down=GPIO.PUD_UP)
        GPIO.setup(self.pin_b, GPIO.IN, pull_up_down=GPIO.PUD_UP)

        GPIO.add_event_detect(self.pin_a, GPIO.RISING, callback=self.pin_rising)
        GPIO.add_event_detect(self.pin_b, GPIO.RISING, callback=self.pin_rising)

    def pin_rising(self, channel):
        self.position += 1

    def get_position(self, ppr=1900):
        anglecurr = (360 / ppr * self.position + 0) % 360
        return anglecurr



if '__main__' == __name__:
    encoder = RotaryEncoder(5, 6)
    while True:
        print(encoder.get_position())
