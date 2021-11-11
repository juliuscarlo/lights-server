"""Helper functions for generating randomness."""

import random


class Helper:
    @staticmethod
    def random_client(clients):
        random_index = random.randint(0, len(clients)-1)
        return clients[random_index]

    @staticmethod
    def random_pause(max_pause):
        random_pause = random.randint(0, max_pause)
        return random_pause
