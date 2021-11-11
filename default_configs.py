class DefaultConfig:
    def __init__(self) -> None:
        self.strobe_sync = \
            {"resolution": 1000,
             "attack": 0.001,
             "decay": 0.001,
             "curve": "lin",
             "min_intensity": 0,
             "max_intensity": 1,
             "width": 1,
             "spacing": 200}

        self.strobe_async = \
            {"resolution": 1000,
             "attack": 0.001,
             "decay": 0.001,
             "curve": "lin",
             "min_intensity": 0,
             "max_intensity": 1,
             "width": 100,
             "spacing": 200}

        self.strobe_binary = \
            {"resolution": 1000,
             "max_intensity": 1,
             "width": 0,
             "spacing": 200}

        self.strobe_binary_sequential = \
            {"resolution": 1000,
             "max_intensity": 1,
             "width": 0,
             "spacing": 200}

        self.strobe_random = \
            {"resolution": 1000,
             "attack": 0.001,
             "decay": 0.001,
             "curve": "lin",
             "min_intensity": 0,
             "max_intensity": 1,
             "width": 1000,
             "spacing": 1000}

        self.glimmer_sync = \
            {"resolution": 1000,
             "attack": 0.01,
             "decay": 0.02,
             "curve": "lin",
             "min_intensity": 0,
             "max_intensity": 0.2,
             "width": 0,
             "spacing": 0}

        self.glimmer_async = \
            {"resolution": 1000,
             "attack": 0.01,
             "decay": 0.02,
             "curve": "lin",
             "min_intensity": 0,
             "max_intensity": 1,
             "width": 10,
             "spacing": 100}

        self.glimmer_overlap = \
            {"resolution": 1000,
             "attack": 0.01,
             "decay": 0.01,
             "curve": "lin",
             "min_intensity": 0,
             "max_intensity": 1,
             "width": 10,
             "spacing": 10}

        self.standby = \
            {"resolution": 1000,
             "attack": 0.01,
             "decay": 0.15,
             "curve": "lin",
             "min_intensity": 0,
             "max_intensity": 0.3,
             "width": 200,
             "spacing": 500}

        self.zpeziale = \
            {"resolution": 1000,
             "attack": 0.1,
             "decay": 0.1,
             "curve": "lin",
             "min_intensity": 0.001,
             "max_intensity": 0.05,
             "width": 0,
             "spacing": 0}
