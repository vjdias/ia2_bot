
from controller import Supervisor
import numpy
import time
# create the Robot instance.
import math

class BotController():
    def __init__(self, robot ,timestep):
        timestep = 64
     
        self.robot = robot
        self.timestep = timestep
        self.rz = self.robot.getDevice("z_body_rotational_motor")
        self.rz.setPosition(0)
        self.rz.setVelocity(0.0)
        self.rz_position = self.robot.getDevice("z_body_position_sensor")
        self.rz_position.enable(self.timestep)
        
        
        self.ry = self.robot.getDevice("y_shoulder_rotational_motor")
        self.ry.setPosition(1)
        self.ry.setVelocity(0.0)
        self.ry_position = self.robot.getDevice("y_shoulder_position_sensor")
        self.ry_position.enable(self.timestep)
        
        self.shot = self.robot.getDevice("shot")
        self.shot_position = self.robot.getDevice("shot_position_sensor")
        self.shot_position.enable(self.timestep)
        
        
        self.bola = self.robot.getFromDef("bolinha")
        self.y_arm_b = self.robot.getFromDef("y_arm_b")
        self.y_arm_b_pose = self.y_arm_b.getPose()
        
        
        self.receiver = self.robot.getDevice("StevesReceiver")
        self.receiver.enable(self.timestep)
        
        self.emitter = self.robot.getDevice("StevesEmitter")
        
        self.enabled_shoot = True
                
    def toD(self, rad):
        return (rad*180/numpy.pi)%360
        
    def moved_direction(self, y_angle, z_angle , y_velocity, z_velocity):          
        stop_y = 0
        stop_z = 0
        
        if  abs(self.toD(self.ry_position.getValue()) - y_angle) > 2:
            self.ry.setVelocity(y_velocity)
        else:
            self.ry.setVelocity(0)
            stop_y = 1
               
        if  abs(self.toD(self.rz_position.getValue()) - y_angle) > 2:
            self.rz.setVelocity(z_velocity)
        else:
            self.rz.setVelocity(0)
            stop_z = 1
            
        self.print_pos(2)
        
        if stop_y and stop_z:
            self.enabled_shoot = True
        else:
            self.enabled_shoot = False
            
        return (stop_y and stop_z)
        
    
    def shoot(self, force):
        if self.enabled_shoot:
            getPostion_y_arm_b = numpy.array(self.robot.getFromDef("y_arm_b").getPosition())
            subtracted_array = numpy.subtract(getPostion_y_arm_b, [0.03, -0.07, -0.041])
            subtracted = list(subtracted_array)
            self.bola.getField("translation").setSFVec3f(subtracted)
            
            p = self.y_arm_b.getPose()
            m = numpy.array([[p[0], p[1], p[2]],
                             [p[4], p[5], p[6]],
                             [p[8], p[9], p[10]]]) @ numpy.array([-1,0,0])
            
            
            self.bola.addForce((m*force).tolist(), False)
            self.enabled_shoot = False
    
   
    def print_pos(self,d):
        y = str(round(self.toD(self.ry_position.getValue()),d))
        z = str(round(self.toD(self.rz_position.getValue()),d))
        print("Degree(y:"+y+" z:"+z+")")

    def get_pos(self):
        return self.toD(self.ry_position.getValue()), self.toD(self.rz_position.getValue())                          

    def obs(self):
        if math.isnan(self.ry_position.getValue()):
            return [0, 0]
            
        return [self.ry_position.getValue(), self.rz_position.getValue()]

    def are_colliding_windows(self):        
        if self.receiver.getQueueLength() > 0:
            message = self.receiver.getData().decode('utf-8')
            self.receiver.nextPacket()
            return message == "1.0"
        return False
    
    def action(self,a):
        print(a)
#        while(self.moved_direction(a[0],a[1], 10, 10)):
#            self.shoot(20)
            
        time_start = time.time()
        while(time_start - time_actual > 100):
            time_actual = time.time()
            if (self.are_colliding_windows(self)):
                return True
                
        return False            
    
    def recharble(self):
        time.sleep(1);
        self.enabled_shoot = True   
        