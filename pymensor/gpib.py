"""Python driver for Mensor Modular Pressure controllers, using IEEE 488.2 GPIB.

Copyright (C) 2020  Steven Lowery

This program is free software: you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation, either version 3 of the License, or
(at your option) any later version.

This program is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU General Public License for more details.
"""

try:
    import visa
except ImportError:
    pass

class PressureController:
    def __init__(self, address_string):
        self.Address = address_string
        rm = visa.ResourceManager()
        self.instrument = rm.open_resource(self.Address)
    
    def ping(self):
        '''Check communication with pressure controller. Returns 'True' or 'Error:' '''
        response = self.instrument.query('*IDN?\r')
        if "MENSOR, 600,610189,0.1.5" not in response:
            return "Error: Pressure Controller did not respond!"
        else:
            return True 
        
        
    def setActiveChannel(self, channel):
        '''Sets active channel'''
        self.instrument.write('Chan ' + channel + '\r')
        return self.instrument.last_status
    
    def setActiveChannelDifferential(self):
        '''Sets active channel as differential channel'''
        self.instrument.write('Chan D\r') # sets the active channel as differential channel
        return self.instrument.last_status
            
    def setUnit(self, unitCode):
        '''Sets unit of the active channel
        Code Description 							Output Format
            1   pounds per square inch ..................psi
            2   inches of mercury @0C ...................inHg @0C
            3   inches of mercury @60F ..................inHg @60F
            4   inches of water @4C .....................inH2O @4C
            5   inches of water @20C.....................inH2O @20C
            6   inches of water @60F.....................inH2O @60F
            7   feet of water @4C .......................ftH2O @4C
            8   feet of water @20C ......................ftH2O @20C
            9   feet of water @60F.......................ftH2O @60F
            10  millitorr ...............................mTorr
            11  inches of seawater @0C 3.5% salinity.....inSW @0C
            12  feet of seawater @0C 3.5% salinity ......ftSW @0C
            13  atmospheres .............................atm
            14  bars ....................................bar
            15  millibars ...............................mbar
            16  millimeters of water @4C ................mmH2O @4C
            17  centimeters of water @4C ................cmH2O @4C
            18  meters of water @4C .....................mH2O @4C
            19  millimeters of mercury @0C ..............mmHg @0C
            20  centimeters of mercury @0C ..............cmHg @0C
            21  torr ....................................Torr
            22  kilopascals .............................kPa
            23  pascals .................................Pa
            24  dyne per square centimeter ..............dyn/sq cm
            25  grams per square centimeter .............g/sq cm
            26  kilograms per square centimeter .........kg/sq cm
            27  meters of seawater @0C 3.5% salinity ....mSW @0C
            28  ounce per square inch ...................oz/si
            29  pounds per square foot ..................psf
            30  tons per square foot ....................tons/sq ft
            31  percent of full scale ...................%FS
            32  micron Hg @0C ...........................micronHg @0C
            33  ton per square inch .....................tons/sq in
            34  n/a .....................................n/a'''
        # To Do: Implement unit format instead of code?
        self.instrument.write('Units ' + str(unitCode) + '\r')
        return self.instrument.last_status
        
    def setMode(self, mode):
        '''Sets mode to : Standby, Measure, Control or Vent'''
        self.instrument.write('Mode '+ mode + '\r')
        return self.instrument.last_status
        
    def setMeasType(self, mtype):
        '''Sets the measurement type: Absolute, Gauge or Differential'''
        if mtype is 'Absolute' or 'A':
            self.instrument.write('Ptype A\r')
        elif mtype is 'Gauge' or 'G':
            self.instrument.write('Ptype G\r')
        elif mtype is 'Differential' or 'D':
            self.instrument.write('Chan D\r')
        else:
            return 'Error: Enter correct measurement type'
        return self.instrument.last_status
    
    def setLimit(self, upper, lower):
        ''''Sets upper and lower control limit for the active channel'''
        self.instrument.write('UpperLimit'+ str(upper))
        self.instrument.write('LowerLimit'+ str(lower))
        return self.instrument.last_status
    
    def setPoint(self,setpt):
        ''' Set the setpoint on current channel on current units'''
        self.instrument.write('Setpt ' + setpt + '\r')
        return self.instrument.last_status
    
    def is_stable(self):
        '''Returns TRUE if instrument is stable or FALSE if not'''
        response = self.instrument.query('Stable?\r').strip('\n').strip('\r').strip('').lstrip('E').lstrip(' ')
        if response == 'YES':
            return True
        elif response == 'NO':
            return False
        else:
            return "Error!No response from the instruemnt :" + response
        
    def readPressure(self, units = False):
        '''Returns current pressure reading on active channel. units = True returns the unit of measurement
        separated by comma '''
        curr_reading = 0
        curr_chan = self.instrument.query('Chan?\r').rstrip('\r').strip('\n').lstrip('E').strip('').rstrip('\r').lstrip(' ')
        #print(curr_chan)
        if curr_chan == 'A':
            strValue = self.instrument.query('A?\r')
            curr_reading = float(strValue.strip('\n').rstrip('\r').lstrip('E').lstrip('E').lstrip(' '))
        elif curr_chan == 'B':
            strValue = self.instrument.query('B?\r')
            curr_reading = float(strValue.strip('\n').rstrip('\r').lstrip('E').lstrip(' '))
            
        if units is True:
            strValue = self.instrument.query('Units?\r')
            unit = strValue.strip('\n').strip('\r').lstrip('E').lstrip(' ')
            return str(curr_reading) + ',' + str(unit)
        return curr_reading
