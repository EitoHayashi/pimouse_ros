#!/user/bin/env python
#encoding: utf8
import unittest,rostest
import rosnode,rospy
import time
from pimouse_ros.msg import LightSensorValues

class LightsensorTest(unittest.TestCase):
    def setup(self):
        self.count = 0
        rospy.Subscriber('lightsensors',LightSensorValues,self.callback)
        self.values = LightSensorValues()

    def callback(self,data)
        self.count += 1
        self.values = data

    def check_values(self,lf,ls,rs,rf):
        vs = self.values
        self.assertEqual(vs.left_forward,lf,"different value: left_forward")


    def test_node_exist(self):
        nodes = rosnode.get_node_names()
        self.assertIn('/lightsensors',nodes,"node does not exist")

    def test_get_value(self):
        rospy.set_param('lightsensors_freq',10)
        time.sleep(2)
        with open("/dev/rtlightsensor0","w") as f:
            f.write("-1 0 123 4321\n")

        time.sleep(3)
        ###call callbackfunction 1 time and confirm value
        self.assertFalse(self.count == 0,"can not subscribe the topic")
        self.check_values(4321,123,0,-1)

    def test_change_parameter(self):
        rospy.set_param('lightsensors_freq',1)
        time.sleep(2)
        c_prev = self.count
        time.sleep(3)
        ###call callbackfunction 1 time per 3sec max 4 times
        self.assertTrue(self.count < c_prev + 4,"freq does not change")
        self.assertFalse(self.count == c_prev,"subscriver is stopped")


if __name__ == '__main__':
    time.sleep(3)
    rospy.init_node('travis_test_lightsensors')
    rostest.rosrun('pimouse_ros','travis_test_lightsensors',LightsensorTest)


