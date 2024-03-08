#!/usr/bin/python

import sys
import time
import math
import pathlib
from pynput import keyboard
from enum import Enum
import threading

script_path = pathlib.Path(__file__).parent.resolve()

sys.path.append(f'{script_path}/lib/')
import robot_interface as sdk


class my_keyboard:
    def __init__(self,parent=None):
        self.pressed_keys = set()
        self.parent = parent

        self.key_act_d = {}
        self.key_act_d['walk_forward']   = keyboard.Key.up
        self.key_act_d['walk_backwards'] = keyboard.Key.down
        self.key_act_d['walk_left']      = keyboard.KeyCode.from_char('q')
        self.key_act_d['walk_right']     = keyboard.KeyCode.from_char('e')
        self.key_act_d['turn_left']      = keyboard.Key.left
        self.key_act_d['turn_right']     = keyboard.Key.right
        self.key_act_d['height_low']     = keyboard.KeyCode.from_char('z')
        self.key_act_d['height_idle']    = keyboard.KeyCode.from_char('x')
        self.key_act_d['height_high']    = keyboard.KeyCode.from_char('c')

        self.key_act_d['look_left']      = keyboard.KeyCode.from_char('a')
        self.key_act_d['look_right']     = keyboard.KeyCode.from_char('d')
        self.key_act_d['look_up']        = keyboard.KeyCode.from_char('w')
        self.key_act_d['look_down']      = keyboard.KeyCode.from_char('s')
        self.key_act_d['look_wierd1']    = keyboard.KeyCode.from_char('r')
        self.key_act_d['look_wierd2']    = keyboard.KeyCode.from_char('f')

        self.key_act_d['speed_1']        = keyboard.KeyCode.from_char('1')
        self.key_act_d['speed_2']        = keyboard.KeyCode.from_char('2')
        self.key_act_d['speed_3']        = keyboard.KeyCode.from_char('3')
        # self.key_act_d['ang_speed_1']    = keyboard.KeyCode(vk=49)   #vk=49 == ctrl+1
        # self.key_act_d['ang_speed_2']    = keyboard.KeyCode(vk=50)   #vk=50 == ctrl+2
        # self.key_act_d['ang_speed_3']    = keyboard.KeyCode(vk=51)   #vk=51 == ctrl+3
        

        self.trigger_acts = []
        self.trigger_acts.append('height_low')
        self.trigger_acts.append('height_idle')
        self.trigger_acts.append('height_high')
        self.trigger_acts.append('speed_1')
        self.trigger_acts.append('speed_2')
        self.trigger_acts.append('speed_3')
        # self.trigger_acts.append('ang_speed_1')
        # self.trigger_acts.append('ang_speed_2')
        # self.trigger_acts.append('ang_speed_3')

        listen_thrd = threading.Thread(target=self.listen)
        listen_thrd.daemon = True  # Allow the thread to exit when the main program finishes
        listen_thrd.start()


    def listen(self):
        with keyboard.Listener(on_press=self.on_press,on_release=self.on_release) as listener:
            listener.join()

    def on_press(self,key):
        try:
            if key not in self.pressed_keys:
                self.pressed_keys.add(key)
        except AttributeError:
            pass
        for act in self.trigger_acts:
            if key == self.key_act_d[act]:
                self.parent.trigger_act(act)

    def on_release(self,key):
        try:
            if key in self.pressed_keys:
                self.pressed_keys.remove(key)
        except AttributeError:
            pass

    def pressed(self,act):
        key = self.key_act_d[act]
        return key in self.pressed_keys

    def is_look_pressed(self):
        if self.pressed('look_right'):
            return True
        if self.pressed('look_left'):
            return True
        if self.pressed('look_up'):
            return True
        if self.pressed('look_down'):
            return True
        if self.pressed('look_wierd2'):
            return True
        if self.pressed('look_wierd1'):
            return True
        return False




class robot:
    def __init__(self):
        self.keyb      = my_keyboard(self)
        self.dir       = 'idle'
        self.speed     = 0.2
        self.ang_speed = 1
        self.height    = 0

    def trigger_act(self,act):

        if act == 'height_low':
            self.height = -0.2
        elif act == 'height_idle':
            self.height = -0.05
        elif act == 'height_high':
            self.height = 0
        elif act == 'speed_1':
            self.speed = 0.1
            self.ang_speed = 0.5
        elif act == 'speed_2':
            self.ang_speed = 1
            self.speed = 0.2
        elif act == 'speed_3':
            self.speed = 0.3
            self.ang_speed = 1.5




    def set_cmd(self,cmd,state):
        # mode options:
        # 0:idle, default stand
        # 1:forced stand
        # 2:walk continuously
        # 4:lie down
        # 6:stand back up
        # 7:go to sleep

        cmd.mode            = 2
        cmd.gaitType        = 0
        cmd.speedLevel      = 0
        cmd.footRaiseHeight = 0
        cmd.euler           = [0, 0, 0]
        cmd.reserve         = 0

        vel_y = 0
        vel_y += self.speed if self.keyb.pressed('walk_forward') else 0
        vel_y -= self.speed if self.keyb.pressed('walk_backwards') else 0
        vel_x = 0
        vel_x -= self.speed if self.keyb.pressed('walk_right') else 0
        vel_x += self.speed if self.keyb.pressed('walk_left') else 0
        ang_v = 0
        ang_v += self.ang_speed if self.keyb.pressed('turn_left') else 0
        ang_v -= self.ang_speed if self.keyb.pressed('turn_right') else 0
        eu1 = 0
        eu2 = 0
        eu3 = 0


        if self.keyb.is_look_pressed():
            cmd.mode = 1
            eu1 += 0.3 if self.keyb.pressed('look_right') else 0
            eu1 -= 0.3 if self.keyb.pressed('look_left') else 0
            eu2 -= 0.2 if self.keyb.pressed('look_up') else 0
            eu2 += 0.2 if self.keyb.pressed('look_down') else 0
            eu3 -= 0.2 if self.keyb.pressed('look_wierd2') else 0
            eu3 += 0.2 if self.keyb.pressed('look_wierd1') else 0
        


        cmd.yawSpeed   = ang_v
        cmd.velocity   = [vel_y, vel_x]
        cmd.bodyHeight = self.height
        cmd.euler      = [eu1, eu2, eu3]


import inspect

def props(obj): # temp
    pr = {}
    for name in dir(obj):
        value = getattr(obj, name)
        if not name.startswith('__') and not inspect.ismethod(value):
            pr[name] = value
    return pr


if __name__ == '__main__':

    HIGHLEVEL = 0xee
    LOWLEVEL  = 0xff

    rob = robot()
    for k, v in rob.keyb.key_act_d.items():
        print(f'{k} : {v}')

    udp = sdk.UDP(HIGHLEVEL, 8080, "192.168.123.161", 8082)

    cmd = sdk.HighCmd()


    # cmd_d = props(cmd)
    # for k,v in cmd_d.items():
    #     print(f'{k = }  :\n{v = }\n\n')

    state = sdk.HighState()

    # state_d = props(state)
    # for k,v in state_d.items():
    #     print(f'{k = }  :\n{v = }\n\n')

    udp.InitCmdData(cmd)

    t = 0
    while True:
        time.sleep(0.002)
        t = t + 1

        udp.Recv()
        udp.GetRecv(state)

        rob.set_cmd(cmd,state)

        # if t % 500 == 0:
        #     print(f'dir is: {rob.dir}')
        #     print(state)


        udp.SetSend(cmd)
        udp.Send()

        if t % 250 ==0:
            print(f'{cmd.bodyHeight = }\n{cmd.velocity = }\n{cmd.yawSpeed = }\n{cmd.euler = }\n')