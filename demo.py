import random
import analyse


MIN_SIZE = 2
MAX_SIZE = 1000
DEFAULT_BITS = 512


class Demo:

    def __init__(self, scenario_number, n, nbits=DEFAULT_BITS, min_size=MIN_SIZE, max_size=MAX_SIZE):
        self.messages = self.message_generator(n, min_size, max_size)
        if scenario_number == 1:
            self.scenario1(nbits)
        elif scenario_number == 2:
            self.scenario2()
        elif scenario_number == 3:
            self.scenario3()

    @staticmethod
    def message_generator(n, min_size, max_size):
        messages = []
        for i in range(1, n + 1):
            messages.append(random.randrange(min_size, max_size))
        return messages

    def scenario1(self, nbits):
        time_classic = analyse.time_classic(self.messages, nbits)
        time_modified = analyse.time_modified(self.messages, nbits)
        analyse.draw_compare(time_classic, time_modified, "Time compare")

    def scenario2(self):
        '''_time = [0.092, 0.116, 0.197, 1.037, 9.423]
        bits = [128, 256, 512, 1024, 2048]
        analyse.draw_by_points(_time, bits)'''
        _time = []
        _time.append(analyse.time_modified(self.messages, 128))
        _time.append(analyse.time_modified(self.messages, 256))
        _time.append(analyse.time_modified(self.messages, 512))
        _time.append(analyse.time_modified(self.messages, 1024))
        _time.append(analyse.time_simple(self.messages, 2048))
        analyse.draw_many(_time, "Modified method with different key sizes")

    def scenario3(self):
        time1 = [0.069, 0.088, 0.261, 2.46, 28.399]
        time2 = [0.092, 0.116, 0.197, 1.037, 9.423]
        bits = [128, 256, 512, 1024, 2048]
        analyse.draw_by_points(time1, time2, bits)
        '''_time = []
        _time.append(analyse.time_classic(self.messages, 128))
        _time.append(analyse.time_classic(self.messages, 256))
        _time.append(analyse.time_classic(self.messages, 512))
        _time.append(analyse.time_classic(self.messages, 1024))
        _time.append(analyse.time_simple(self.messages, 2048))
        analyse.draw_many(_time, "Classic method with different key sizes")'''