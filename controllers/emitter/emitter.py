# Copyright 1996-2022 Cyberbotics Ltd.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

"""
This controller gives to its node the following behavior:
Listen the keyboard. According to the pressed key, send a
message through an emitter or handle the position of Robot1.
"""


from controller import Supervisor

robot = Supervisor()

class WinBots():
    def __init__(self, robot):  
        self.robot = robot
        self.winbot = self.robot.getFromDef("winbot")
        print("r")
        print(self.winbot)
        
    def move(self, position, angle):
        self.winbot.getField("translation").setSFVec3f(position)      
        self.winbot.getField("rotation").setSFVec3f(angle)      


class Driver():
    timestep = 64
    x = -0.3
    y = -0.1
    translation = [x, y, 0]

    def __init__(self, robot):
        super(Driver, self).__init__()
        self.robot = robot
        self.emitter = self.robot.getDevice('emitter')
        self.winbot_touch = self.robot.getDevice('touch_ball_detector')
        self.winbot_touch.enable(self.timestep)
        
    def run(self):

        # Main loop.
        while True:
            # Send a new message through the emitter device.
            
            message = str(self.winbot_touch.getValue())
            #print("Emitter: "+str(message))
            self.emitter.send(message.encode('utf-8'))
            # Perform a simulation step, quit the loop when
            # Webots is about to quit.
            if self.robot.step(self.timestep) == -1:
                break



#b = WinBots(robot)
#b.move([1,2,3], [1,2,3])

#winbot = robot.getDevice("winbot")

#print(winbot)

#winbot.getField("translation").setSFVec3f([1,2,3])      
#winbot.getField("rotation").setSFVec3f([1,2,3])   

controller = Driver(robot)
controller.run()