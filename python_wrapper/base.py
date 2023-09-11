#!/usr/bin/python

import sys
import time
import math
import pathlib
from pynput import keyboard
from enum import Enum
import threading
import copy

script_path = pathlib.Path(__file__).parent.resolve()

sys.path.append(f'{script_path}/lib/')
import robot_interface as sdk


class my_keyboard:
    def __init__(self,parent=None):
        self.pressed_keys = set()
        self.parent = parent
        self.set_key_bindings()

        # a thread that manages key presses
        listen_thrd = threading.Thread(target=self.listen)
        listen_thrd.daemon = True  # Allow the thread to exit when the main program finishes
        listen_thrd.start()

    def set_key_bindings(self):
        self.idle_key_d = {}
        self.idle_key_d[keyboard.Key.up]                 = 'walk_forward'
        self.idle_key_d[keyboard.Key.down]               = 'walk_backwards'
        self.idle_key_d[keyboard.Key.left]               = 'turn_left'
        self.idle_key_d[keyboard.Key.right]              = 'turn_right'
        self.idle_key_d[keyboard.KeyCode.from_char('q')] = 'look_tilt_l'
        self.idle_key_d[keyboard.KeyCode.from_char('e')] = 'look_tilt_r'
        self.idle_key_d[keyboard.KeyCode.from_char('a')] = 'look_left'
        self.idle_key_d[keyboard.KeyCode.from_char('d')] = 'look_right'
        self.idle_key_d[keyboard.KeyCode.from_char('w')] = 'look_up'
        self.idle_key_d[keyboard.KeyCode.from_char('s')] = 'look_down'
        self.idle_key_d[keyboard.KeyCode.from_char('z')] = 'height_low'
        self.idle_key_d[keyboard.KeyCode.from_char('x')] = 'height_idle'
        self.idle_key_d[keyboard.KeyCode.from_char('c')] = 'height_high'
        self.idle_key_d[keyboard.KeyCode.from_char('1')] = 'speed_1'
        self.idle_key_d[keyboard.KeyCode.from_char('2')] = 'speed_2'
        self.idle_key_d[keyboard.KeyCode.from_char('3')] = 'speed_3'
        self.idle_key_d[keyboard.KeyCode(vk=49)]         = 'vel_speed_1' #vk=49 == ctrl+1
        self.idle_key_d[keyboard.KeyCode(vk=50)]         = 'vel_speed_2' #vk=50 == ctrl+2
        self.idle_key_d[keyboard.KeyCode(vk=51)]         = 'vel_speed_3' #vk=51 == ctrl+3

        self.ctrl_key_d = copy.deepcopy(self.idle_key_d)
        self.ctrl_key_d[keyboard.Key.left]               = 'walk_left'
        self.ctrl_key_d[keyboard.Key.right]              = 'walk_right'


        self.key_d = self.idle_key_d # first key binding set

        self.trigger_acts = []
        self.trigger_acts.append('height_low')
        self.trigger_acts.append('height_idle')
        self.trigger_acts.append('height_high')
        self.trigger_acts.append('speed_1')
        self.trigger_acts.append('speed_2')
        self.trigger_acts.append('speed_3')
        self.trigger_acts.append('vel_speed_1')
        self.trigger_acts.append('vel_speed_2')
        self.trigger_acts.append('vel_speed_3')

    def ctrl_l_press(self):
        self.key_d = self.ctrl_key_d
    def ctrl_l_release(self):
        self.key_d = self.idle_key_d


    def get_act_key(self,act):
        act_d = {}
        for k,v in self.key_d.items():
            if v == act:
                return k
        return None

    def listen(self):
        with keyboard.Listener(on_press=self.on_press,on_release=self.on_release) as listener:
            listener.join()

    def on_press(self,key):
        if key == keyboard.Key.ctrl_l:
            self.ctrl_l_press()
            return
        try:
            if key not in self.pressed_keys:
                self.pressed_keys.add(key)
        except AttributeError:
            pass
        # print(key)
        # print(key.char)
        # print(key.is_dead)
        # print(key.vk)
        # print(type(key))
        # print(self.trigger_acts)
        for act in self.trigger_acts:
            act_key = self.get_act_key(act)
            if key == act_key or (isinstance(key,keyboard.KeyCode) and key.char==None and key.vk==act_key.vk): # second part handles messy keys such as ctrl+1
                self.parent.trigger_act(act)

    def on_release(self,key):
        if key == keyboard.Key.ctrl_l:
            self.ctrl_l_release()
            return
        try:
            if key in self.pressed_keys:
                self.pressed_keys.remove(key)
        except AttributeError:
            pass

    def pressed(self,act):
        key = self.get_act_key(act)
        return key in self.pressed_keys

class robot:
    def __init__(self):
        self.keyb      = my_keyboard(self)
        self.speed     = 0.2
        self.ang_speed = 1
        self.height    = 0

    def trigger_act(self,act):

        if act == 'height_low':
            self.height = -0.2
        elif act == 'height_idle':
            self.height = 0
        elif act == 'height_high':
            self.height = 0.1
        elif act == 'speed_1':
            self.speed = 0.1
        elif act == 'speed_2':
            self.speed = 0.2
        elif act == 'speed_3':
            self.speed = 0.3
        elif act == 'vel_speed_1':
            self.ang_speed = 0.5
        elif act == 'vel_speed_2':
            self.ang_speed = 1
        elif act == 'vel_speed_3':
            self.ang_speed = 1.5

    def set_cmd(self,cmd,state):
        cmd.mode            = 8      # 0:idle, default stand      1:forced stand     2:walk continuously
        cmd.gaitType        = 0
        cmd.speedLevel      = 0
        cmd.footRaiseHeight = 0
        cmd.reserve         = 0

        vel_y = 0
        vel_y += self.speed if self.keyb.pressed('walk_forward') else 0
        vel_y -= self.speed if self.keyb.pressed('walk_backwards') else 0

        vel_x = 0
        vel_x += self.speed if self.keyb.pressed('walk_right') else 0
        vel_x -= self.speed if self.keyb.pressed('walk_left') else 0

        ang_v = 0
        ang_v += self.ang_speed if self.keyb.pressed('turn_right') else 0
        ang_v -= self.ang_speed if self.keyb.pressed('turn_left') else 0

        eul_0 = 0
        eul_0 += 0.3 if self.keyb.pressed('look_tilt_l') else 0
        eul_0 -= 0.3 if self.keyb.pressed('look_tilt_r') else 0

        eul_1 = 0
        eul_1 += 0.2 if self.keyb.pressed('look_down') else 0
        eul_1 -= 0.2 if self.keyb.pressed('look_up') else 0

        eul_2 = 0
        eul_2 += 0.2 if self.keyb.pressed('look_right') else 0
        eul_2 -= 0.2 if self.keyb.pressed('look_left') else 0

        cmd.yawSpeed   = ang_v
        cmd.velocity   = [vel_y, vel_x]
        cmd.bodyHeight = self.height
        cmd.euler      = [eul_0, eul_1, eul_2]

        # TODO: manage cmd.mode selection
        # TODO: manage cmd.gaitType selection

import inspect

class cmd_dummy:
    pass
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
    # for k, v in rob.keyb.key_act_d.items():
    #     print(f'{k} : {v}')

    udp = sdk.UDP(HIGHLEVEL, 8080, "192.168.123.161", 8082)

    cmd = sdk.HighCmd()
    # cmd = cmd_dummy()
    # state = cmd_dummy()


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