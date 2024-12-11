class SimulationParameters:
    def __init__(self, ant_starting_position: float, rubber_band_starting_length: float, 
                 ant_walking_speed: float, rubber_band_stretch_rate: float):
        self.ant_starting_position = ant_starting_position
        self.rubber_band_starting_length = rubber_band_starting_length
        self.ant_walking_speed = ant_walking_speed
        self.rubber_band_stretch_rate = rubber_band_stretch_rate
        self.stretch_factor = 1 + rubber_band_stretch_rate  # Set the attribute directly


class Simulation:
    def __init__(self, params: SimulationParameters):
        self.params = params
        self.running_ant_position = self.params.ant_starting_position
        self.running_rubber_band_length = self.params.rubber_band_starting_length

    def simulate_time_step_ant_then_stretch(self):
        #move ant from walking
        #stretch band (update ant position and end of band)

        self.running_ant_position += self.params.ant_walking_speed
        self.running_ant_position *= self.params.stretch_factor
        self.running_rubber_band_length *= self.params.stretch_factor


    def simulate_time_step_stretch_then_ant(self):
        #stretch band (update ant position and end of band)
        #move ant from walking

        self.running_ant_position *= self.params.stretch_factor
        self.running_rubber_band_length *= self.params.stretch_factor
        self.running_ant_position += self.params.ant_walking_speed


    def simulate_time_step_half_ant_then_stretch_then_half_ant(self):
        # move ant HALFWAY from walking
        # stretch band (update ant position and end of band)
        # move ant HALFWAY from walking

        self.running_ant_position += 0.5 * self.params.ant_walking_speed

        self.running_ant_position *= self.params.stretch_factor
        self.running_rubber_band_length *= self.params.stretch_factor

        self.running_ant_position += 0.5 * self.params.ant_walking_speed
