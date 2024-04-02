import numpy as np
import gymnasium as gym
from gymnasium.envs.box2d.lunar_lander import *
from typing import TYPE_CHECKING, Optional


class STEP_LUNAR(LunarLander):
    def __init__(
        self,
        render_mode: Optional[str] = None,
        continuous: bool = False,
        gravity: float = -10.0,
        enable_wind: bool = False,
        wind_power: float = 15.0,
        turbulence_power: float = 1.5,):
        self.helipad_y = None
        super().__init__(
            render_mode=render_mode,
            continuous=continuous,
            gravity=gravity,
            enable_wind=enable_wind,
            wind_power=wind_power,
            turbulence_power=turbulence_power,
        )
        # assert False
    
    def reset(self,
        *,
        seed: Optional[int] = None,
        options: Optional[dict] = None,):
        return
    
    def step(self, action):
        return super().step(action)
