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
    """Python driver for Mensor Pressure Controllers.

    [Reference](https://www.mensor.com/products_pressure_controllers_en_co.WIKA).

    This class communicates with the pressure controller over a GPIB connection using pyvisa.

    inheritance:
    none

    methods:
    ping()
    set_active_channel(channel)
    set_active_channel_differential()
    set_unit(unit_code)
    set_mode(mode)
    set_meas_type(mtype)
    set_limit(upper, lower)
    setpoint(setpt)
    is_stable()
    read_pressure()
    """
    def __init__(self, address_string):
        """Initialize a GPIB-connected pressure controller with an address string
        such as 'GPIB::1::INSTR' or other GPIB address.

        args:
        adress_string: (string) the GPIB address of the device

        return:
        PressureController object
        """
        self.address = address_string
        resource_manager = visa.ResourceManager()
        self.instrument = resource_manager.open_resource(self.address)

    def ping(self):
        """Check communication with pressure controller.

        args:
        none

        return:
        True if instrument responded
        """
        # TODO: validate if a Mensor instrument is connected
        response = self.instrument.query('*IDN?\r')
        if "MENSOR, 600,610189,0.1.5" not in response:
            raise RuntimeError("A Mensor pressure controller did not respond! \
                                Got response: {}".format(response))
        return True

    def set_active_channel(self, channel):
        """Sets active channel on modular pressure controllers.
        Must be 'A' or 'B'.

        args:
        channel: (char) 'A' or 'B'

        return:
        self.instrument.last_status
        """
        channel = channel.upper()
        if channel not in ('A', 'B'):
            raise ValueError("Input must be 'A' or 'B'")
        self.instrument.write('Chan ' + channel + '\r')
        return self.instrument.last_status

    def set_active_channel_differential(self):
        """Makes the active channel a differential channel.

        args:
        none

        return:
        self.instrument.last_status
        """
        self.instrument.write('Chan D\r') # sets the active channel as differential channel
        return self.instrument.last_status

    def set_unit(self, unit_code):
        """Sets unit of the active channel using unit_code described below.

        args:
        unit_code: (int) the integer unit code from the table below

        return:
        self.instrument.last_status

        Code    Description 							 Output Format
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
            34  n/a .....................................n/a
            """
        # TODO: Implement unit format instead of code?
        if unit_code not in range(1, 35):
            raise ValueError("Unit code not supported. See instrument's user's manual.")
        self.instrument.write('Units ' + str(unit_code) + '\r')
        return self.instrument.last_status

    def set_mode(self, mode):
        """Sets mode to : Standby, Measure, Control or Vent.

        args:
        mode: (string) "standby", "measure", "control", or "vent"

        return:
        self.instrument.last_status
        """
        self.instrument.write('Mode '+ mode + '\r')
        return self.instrument.last_status

    def set_meas_type(self, mtype):
        """Sets the measurement type: Absolute, Gauge or Differential.

        args:
        mtype: (string) "Absolute" (or 'A'), "Gauge" (or 'G'), or "Differential" (or 'D')

        return:
        self.instrument.last_status
        """
        mtype = mtype.upper()
        if mtype not in ('ABSOLUTE', 'A', 'GAUGE', 'G', 'DIFFERENTIAL', 'D'):
            raise ValueError("Input must be Absolute, Gauge, or Differential.")
        if mtype in ('ABSOLUTE', 'A'):
            self.instrument.write('Ptype A\r')
        elif mtype in ('GAUGE', 'G'):
            self.instrument.write('Ptype G\r')
        elif mtype in ('DIFFERENTIAL', 'D'):
            self.instrument.write('Chan D\r')
        return self.instrument.last_status

    def set_limit(self, upper, lower):
        """Sets upper and lower control limit for the active channel.

        args:
        upper: (string) upper control limit as a value
        lower: (string) lower control limit as a value

        return:
        self.instrument.last_status
        """
        # TODO: add option for setting just one of the limits
        if not isinstance(upper, (int, float)):
            raise TypeError("Input must be of type int or float.")
        if not isinstance(lower, (int, float)):
            raise TypeError("Input must be of type int or float.")
        self.instrument.write('UpperLimit'+ str(upper))
        self.instrument.write('LowerLimit'+ str(lower))
        return self.instrument.last_status

    def setpoint(self, setpt):
        """Set the setpoint on current channel on current units.

        args:
        setpt: (string) the desired setpoint as a value

        return:
        self.instrument.last_status
        """
        if not isinstance(setpt, (int, float)):
            raise TypeError("Input must be of type int or float.")
        self.instrument.write('Setpt ' + str(setpt) + '\r')
        return self.instrument.last_status

    def is_stable(self):
        """Check if the control value has stabilized.

        args:
        none

        return:
        True if stable
        False if not
        """
        # TODO: fix return formatting - should not return before else
        response = self.instrument.query('Stable?\r')
        response = response.strip('\n')
        response = response.strip('\r')
        response = response.strip('')
        response = response.lstrip('E')
        response = response.lstrip(' ')
        stable = None
        if response == 'YES':
            stable = True
        elif response == 'NO':
            stable = False
        else:
            raise RuntimeError("An unexpected response was received! \
                                Got response: {}".format(response))
        return stable

    def read_pressure(self, units=False):
        """Returns current pressure reading on active channel.
        If units=True then returns the unit of measurement separated by comma.

        args:
        (optional) units: (bool) set to True to return the units along with pressure reading.
        Default=False.

        return:
        curr_reading
        """
        # TODO: make return type same regardless. Choose to return units another way.
        curr_reading = 0
        curr_chan = self.instrument.query('Chan?\r')
        curr_chan = curr_chan.rstrip('\r')
        curr_chan = curr_chan.strip('\n')
        curr_chan = curr_chan.lstrip('E')
        curr_chan = curr_chan.strip('')
        curr_chan = curr_chan.rstrip('\r')
        curr_chan = curr_chan.lstrip(' ')

        if curr_chan == 'A':
            str_value = self.instrument.query('A?\r')
            str_value = str_value.strip('\n')
            str_value = str_value.rstrip('\r')
            str_value = str_value.lstrip('E')
            str_value = str_value.lstrip('E')
            str_value = str_value.lstrip(' ')
            curr_reading = float(str_value)
        elif curr_chan == 'B':
            str_value = self.instrument.query('B?\r')
            str_value = str_value.strip('\n')
            str_value = str_value.rstrip('\r')
            str_value = str_value.lstrip('E')
            str_value = str_value.lstrip(' ')
            curr_reading = float(str_value)

        return_val = curr_reading

        if units is True:
            str_value = self.instrument.query('Units?\r')
            str_value = str_value.strip('\n')
            str_value = str_value.strip('\r')
            str_value = str_value.lstrip('E')
            str_value = str_value.lstrip(' ')
            unit = str_value
            return_val = str(curr_reading) + ',' + str(unit)
        return return_val
    