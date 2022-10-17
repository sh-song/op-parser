from cereal.messaging import SubMaster
from sig_int_handler import Activate_Signal_Interrupt_Handler
import rospy
from std_msgs.msg import Float64
import threading
from time import sleep
class OPParser:
    def __init__(self, addr, rate):
        self.sm = SubMaster(['controlsState'], addr=addr)
        self.dt = 1 / rate
        self.cs = None

    def update(self):
        while True:
            self.sm.update(0)
            if self.sm['controlsState']:
                self.cs = self.sm['controlsState']
                print(self.cs)
            sleep(self.dt)



    def get_steer(self):
        #TODO: remove other states after check
        #states = [self.cs.lateralControlState.angleState,
        #        self.cs.lateralControlState.pidState,
        #        self.cs.lateralControlState.lqrState,
        #        self.cs.lateralControlState.indiState]
        #for state in states[1:]:
        state = self.cs.lateralControlState.pidState
        if state:
            print(f"state: {state}")
            lac_log = state
            isActive = lac_log.active #self.active
            steer_angle = lac_log.steeringAngleDeg #CS.steeringAngleDeg
            steer = lac_log.output #actuators.steer
            print(f"steer: {steer}")
            print(f"steer_angle: {steer_angle}")
            print('--------------------------')
            #TODO: check steer, steer_angle types
            return steer_angle 

if __name__ == "__main__":
    Activate_Signal_Interrupt_Handler()
    #ROS
    rospy.init_node("openpilot", anonymous=False)
    pub = rospy.Publisher("/op_steer", Float64, queue_size=1)
    msg = Float64()

    #Openpilot
    addr = '192.168.101.100'
    pp = OPParser(addr=addr, rate=50)
    th_update = threading.Thread(target=pp.update, args=())
    th_update.start()

    #Main Loop
    ros_rate = rospy.Rate(20)    
    while True:
        #steer = pp.get_steer()
        #msg.data = steer
        #pub.publish(msg)
        #ros_rate.sleep()
        pass
