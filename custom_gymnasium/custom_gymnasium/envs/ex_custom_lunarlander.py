import numpy as np
import gymnasium as gym
from gymnasium.envs.box2d.lunar_lander import *
from typing import TYPE_CHECKING, Optional

"""
# task: change the shape of the lunar lander to a custom shape just like a rocket

# hint: you can check the file of box2d/lunar_lander.py to see how the lunar lander is defined,
        and the parameter of deciding the shape of the lunar lander is LANDER_POLY.
"""
# =====================type your code here=========================
LANDER_POLY = [(-14, +30), (-17, 0), (-17, -10), (+17, -10), (+17, 0), (+14, +30)]
LANDER_DENSITY = 5.0
# =================================================================
class CustomLunarLander_v1(LunarLander, gym.Env):
    
    def __init__(
        self,
        render_mode: Optional[str] = None,
        continuous: bool = False,
        gravity: float = -10.0,
        enable_wind: bool = False,
        wind_power: float = 15.0,
        turbulence_power: float = 1.5,
    ):
        super().__init__(
            render_mode=render_mode,
            continuous=continuous,
            gravity=gravity,
            enable_wind=enable_wind,
            wind_power=wind_power,
            turbulence_power=turbulence_power,
        )

    def reset(
        self,
        *,
        seed: Optional[int] = None,
        options: Optional[dict] = None,
    ):
        """
        # task: use super() function to call the parent class step function, 
                and make your step function return the same as the parent class step function.
        
        # hint: you can check the file of box2d/lunar_lander.py to see how the step function is defined,
                and what does the step function need to take as input, and what does the step function return.
        """
        # =====================type your code here=========================
        super().reset(seed=seed)
        # gym.Env.reset(self=self, seed=seed)
        # =================================================================

        # Create Lander body
        self.lander: Box2D.b2Body = self.world.CreateDynamicBody(
            position=(initial_x, initial_y),
            angle=0.0,
            fixtures=fixtureDef(
                shape=polygonShape(
                    vertices=[(x / SCALE, y / SCALE) for x, y in LANDER_POLY]
                ),
                density=LANDER_DENSITY,
                friction=0.1,
                categoryBits=0x0010,
                maskBits=0x001,  # collide only with ground
                restitution=0.0,
            ),  # 0.99 bouncy
        )
        self.lander.color1 = (128, 102, 230)
        self.lander.color2 = (77, 77, 128)

        # Apply the initial random impulse to the lander
        self.lander.ApplyForceToCenter(
            (
                self.np_random.uniform(-INITIAL_RANDOM, INITIAL_RANDOM),
                self.np_random.uniform(-INITIAL_RANDOM, INITIAL_RANDOM),
            ),
            True,
        )

        if self.enable_wind:  # Initialize wind pattern based on index
            self.wind_idx = self.np_random.integers(-9999, 9999)
            self.torque_idx = self.np_random.integers(-9999, 9999)

        # Create Lander Legs
        self.legs = []
        for i in [-1, +1]:
            leg = self.world.CreateDynamicBody(
                position=(initial_x - i * LEG_AWAY / SCALE, initial_y),
                angle=(i * 0.05),
                fixtures=fixtureDef(
                    shape=polygonShape(box=(LEG_W / SCALE, LEG_H / SCALE)),
                    density=1.0,
                    restitution=0.0,
                    categoryBits=0x0020,
                    maskBits=0x001,
                ),
            )
            leg.ground_contact = False
            leg.color1 = (128, 102, 230)
            leg.color2 = (77, 77, 128)
            rjd = revoluteJointDef(
                bodyA=self.lander,
                bodyB=leg,
                localAnchorA=(0, 0),
                localAnchorB=(i * LEG_AWAY / SCALE, LEG_DOWN / SCALE),
                enableMotor=True,
                enableLimit=True,
                maxMotorTorque=LEG_SPRING_TORQUE,
                motorSpeed=+0.3 * i,  # low enough not to jump back into the sky
            )
            if i == -1:
                rjd.lowerAngle = (
                    +0.9 - 0.5
                )  # The most esoteric numbers here, angled legs have freedom to travel within
                rjd.upperAngle = +0.9
            else:
                rjd.lowerAngle = -0.9
                rjd.upperAngle = -0.9 + 0.5
            leg.joint = self.world.CreateJoint(rjd)
            self.legs.append(leg)

        self.drawlist = [self.lander] + self.legs

        if self.render_mode == "human":
            self.render()
        return self.step(np.array([0, 0]) if self.continuous else 0)[0], {}