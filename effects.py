""" Base effects to create visual patterns using PWMLEDs."""

from helper import Helper
from time import sleep


class Blink:
    @staticmethod
    def simultaneous(config):
        """Blinks the clients simultaneously."""

        attack_steps = max(1, int(config.attack * config.resolution))
        decay_steps = max(1, int(config.decay * config.resolution))

        # now provide increment values for getting from min_intensity to max_intensity
        # linear
        if config.curve == "lin":
            attack_increment = (config.max_intensity -
                                config.min_intensity) / attack_steps
            decay_increment = (config.max_intensity -
                               config.min_intensity) / decay_steps

        intensity = config.min_intensity
        for step in range(attack_steps):
            for client in config.clients:
                client.value = min(intensity, config.max_intensity)
                intensity += attack_increment

        sleep(config.width / 1000)

        intensity = config.max_intensity
        for step in range(decay_steps):
            for client in config.clients:
                client.value = max(intensity, config.min_intensity)
                intensity -= decay_increment

        for client in config.clients:
            client.value = config.min_intensity

        sleep(config.spacing / 1000)

    @staticmethod
    def sequential(config):
        """Blinks the clients sequentially."""

        attack_steps = max(1, int(config.attack * config.resolution))
        decay_steps = max(1, int(config.decay * config.resolution))

        # now provide increment values for getting from min_intensity to max_intensity
        # linear
        if config.curve == "lin":
            attack_increment = (config.max_intensity -
                                config.min_intensity) / attack_steps
            decay_increment = (config.max_intensity -
                               config.min_intensity) / decay_steps

        for client in config.clients:
            intensity = config.min_intensity
            for step in range(attack_steps):
                client.value = min(intensity, config.max_intensity)
                intensity += attack_increment

            intensity = config.max_intensity
            for step in range(decay_steps):
                client.value = max(intensity, config.min_intensity)
                intensity -= decay_increment

            client.value = config.min_intensity

            sleep(config.width / 1000)

        sleep(config.spacing / 1000)

    @staticmethod
    def parallel(config):
        """Blinks the clients with an offset, allowing parallelized intensity transitions."""
        # TODO: Not fully implemented yet.
        attack_steps = max(20, int(config.attack * config.resolution))
        decay_steps = max(20, int(config.decay * config.resolution))

        if config.curve == "lin":
            attack_increment = (config.max_intensity -
                                config.min_intensity) / attack_steps
            decay_increment = (config.max_intensity -
                               config.min_intensity) / decay_steps

        # make a list for the intensity values, initialize with a single starting value
        intensity = config.min_intensity
        intensity_list = [intensity]

        for step in range(attack_steps):
            intensity = min(intensity, config.max_intensity)
            intensity_list.append(intensity)
            intensity += attack_increment

        for step in range(decay_steps):
            intensity = max(intensity, config.min_intensity)
            intensity_list.append(intensity)
            intensity -= decay_increment

        # pad list with zeros in line with width parameter to make an offset between clients
        # don't forget padding the end as well
        offset = max(len(intensity_list), config.width) * [0]
        print(offset)
        offset_multiplier = 0
        # add some margin to offset
        padded_intensity_list = offset + intensity_list + offset
        print(padded_intensity_list)

        # process the list with a for client in clients loop, but add length of padding and padding*2 to two clients
        for index in range(len(intensity_list)):
            for client in config.clients:
                offset_multiplier = offset_multiplier % len(config.clients)
                client.value = padded_intensity_list[index + offset_multiplier * config.width]
                offset_multiplier += 1

        sleep(config.spacing / 1000)

    @staticmethod
    def random(config):
        """Blinks a random client."""
        attack_steps = max(1, int(config.attack * config.resolution))
        decay_steps = max(1, int(config.decay * config.resolution))

        # now provide increment values for getting from min_intensity to max_intensity
        # linear
        if config.curve == "lin":
            attack_increment = (config.max_intensity -
                                config.min_intensity) / attack_steps
            decay_increment = (config.max_intensity -
                               config.min_intensity) / decay_steps

        client = Helper.random_client(config.clients)
        intensity = config.min_intensity
        for step in range(attack_steps):
            client.value = min(intensity, config.max_intensity)
            intensity += attack_increment

        intensity = config.max_intensity
        for step in range(decay_steps):
            client.value = max(intensity, config.min_intensity)
            intensity -= decay_increment

        client.value = config.min_intensity

        sleep(Helper.random_pause(max_pause=config.spacing) / 1000)

    @staticmethod
    def binary(config):
        """Hard cut-off parallel blinks."""
        sleep(0.001)
        intensity = config.max_intensity
        for client in config.clients:
            client.value = intensity

        sleep(config.width / 1000)

        for client in config.clients:
            client.value = config.min_intensity

        sleep(config.spacing / 1000)

    @staticmethod
    def binary_sequential(config):
        """Hard cut-off sequential blinks."""
        sleep(0.001)
        intensity = config.max_intensity
        for client in config.clients:
            client.value = intensity

            sleep(config.width / 1000)

            client.value = config.min_intensity

            sleep(config.spacing / 1000)
