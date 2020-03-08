'''
    Example controller that uses GridlabD device
'''

from riaps.run.comp import Component
import os
import time
import random

class Controller(Component):
    def __init__(self, sensor,actuator):
        super(Controller, self).__init__()
        self.logger.info("Controller.__init__ ()")
        self.sObj,self.sName,self.sAttr = sensor.split('.')
        self.aObj,self.aName,self.aAttr = actuator.split('.')
        self.control_counter = 0
        self.control_period = random.randint(20,30)
        self.control_duty = random.randint(10,20)
        self.pending = 0 
        self.first = True
        self.lastValue = None
    
    def handleActivate(self):
        self.logger.info("handleActivate()")
        self.trigger.setDelay(30.0)
        self.trigger.launch()
        
    def on_trigger(self):
        self.logger.info("on_trigger()")
        _discard = self.trigger.recv_pyobj()
        self.trigger.halt()
        if self.pending == 0: 
            msg = ['sub', (self.sObj,self.sName,self.sAttr)]
            try:
                self.command.send_pyobj(msg)
                self.logger.info("on_trigger: msg=%s" % str(msg))
            except PortError as e:
                self.logger.info("send exception : error code %s" % e.errno)
            else:
                self.pending += 1
    
    def on_command(self):
        _msg = self.command.recv_pyobj()
        self.pending -= 1 
        self.logger.info("on_command(): resp = %s" % str(_msg))
        if len(_msg) == 0:
            self.logger.info('... no response')
            return
        if _msg[0] == self.aObj: # query response
            kvar = float(_msg[3])
            value = self.control()
            if value == '1':
                set = kvar/2 
            elif value == '0':
                set = kvar*2 
            if value != self.lastValue:
                while self.pending > 0: self.on_command()
                # publish interface
                cmd = ['pub', (self.aObj,self.aName,self.aAttr,set)]
                self.logger.info("command = %s" % str(cmd))
                try:
                    self.command.send_pyobj(cmd)
                    self.pending += 1
                    self.lastValue = value
                except PortError as e:
                    self.logger.info("send exception : error code %s" % e.errno)
                else:
                    self.trigger.halt()
    
    def control(self):  
        value = '1' if self.control_counter < self.control_duty else '0'
        self.control_counter = (self.control_counter + 1) % self.control_period
        return value
        
    def on_data(self):
        msg = self.data.recv_pyobj()
        self.logger.info("on_data(): recv=%s" % str(msg))
        querycmd = ['qry', (self.aObj,self.aName,self.aAttr)] # query the last known load kvar
        try:
            self.command.send_pyobj(querycmd)
        except PortError as e:
            self.logger.info("send exception : error code %s" % e.errno)
        else:
            self.pending += 1
        
        
    def __destroy__(self):
        self.logger.info("Controller.__destroy__()")

                         
                    
                         