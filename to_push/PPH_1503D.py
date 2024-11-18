# Version 0p3

import pyvisa
from pyvisa.errors import VisaIOError



class PPH_1503D:
    def __init__(self, address):
        try:
            self.rm = pyvisa.ResourceManager()
            self.ps = self.rm.open_resource(address)
        except VisaIOError:
            print('Could not connect to PSU. Please ensure it is connected and try again.')

    def __del__(self):
        # body of destructor
        try:
            self.ps.close()
        except (AttributeError, VisaIOError):
            print('Initialization failed. Is the PPH1503D connected? Try power cycle the PSU.')

    def set_source_voltage(self, source, voltage):
        try:
            command = ':SOUR{}:VOLT {:.3f}'.format(source, voltage)
            self.ps.write(command)
        except VisaIOError:
            print('Failed to set source voltage')

    def measure_voltage(self, source):
        try:
            command = ':MEAS{}:VOLT?'.format(source)
            result = float(self.ps.query(command).strip())
            return result
        except VisaIOError:
            print('Failed to measure voltage')
            return 'failed'
        except ValueError:
            return 'failed'

    def measure_current(self, source):
        try:
            command = ':MEAS{}:CURR?'.format(source)
            result = float(self.ps.query(command).strip())
            return result
        except VisaIOError:
            print('Failed to measure current')
            return 'failed'
        except ValueError:
            return 'failed'

    def set_source_ilim(self, source, ilimit):
        try:
            command = ':SOUR{}:CURR {:.3f}'.format(source, ilimit)
            self.ps.write(command)
        except VisaIOError:
            print('Failed to set source current limit')

    def output_state(self, output, state):
        try:
            command = ':OUTP{}:STAT {}'.format(output, state)
            self.ps.write(command)
        except VisaIOError:
            print('Failed to set output state')
        
    def read_DVM(self):
        try:
            command = ':MEAS2:DVM?'
            result = float(self.ps.query(command).strip())
            return result
        except VisaIOError:
            print('Failed to read DVM')
            return None

    def set_outp_ovp(self, source, voltage):
        try:
            command = ':OUTP{}:OVP {:.3f}'.format(source, voltage)
            self.ps.write(command)
        except VisaIOError:
            print('Failed to set output OVP')

    def set_outp_ovp_state(self, source, state):
        try:
            command = ':OUTP{}:OVP:STAT {}'.format(source, state)
            self.ps.write(command)
        except VisaIOError:
            print('Failed to set output OVP state')

    def set_data_format(self, dataformat):
        """
        :FORMat[:DATA] < type >
        <type > ASCii: ASCII format.
                SREal: IEEE754 single precision format.
                DREal: IEEE754 double precision format.
        """
        try:
            command = ':FORM:DATA{}'.format(dataformat)
            self.ps.write(command)
        except VisaIOError:
            print('Failed to set data format')

    def set_sense_func(self, source, func):
        try:
            command = ':SENS{}:FUNC {}'.format(source, func)
            self.ps.write(command)
        except VisaIOError:
            print('Failed to set sense function')

    def set_sense_period(self, source, NPLcycles):
        """measurement period has to be provides in terms of power line cycles 0.01-10.00 x NPLcycles"""
        try:
            command = ':SENS{}:NPLC {:.3f}'.format(source, NPLcycles)
            self.ps.write(command)
        except VisaIOError:
            print('Failed to set sense period')

    def set_sense_averaging(self, source, no_samples):
        """Accepts values in a range from 1-10"""
        try:
            command = ':SENS{}:AVER {}'.format(source, no_samples)
            self.ps.write(command)
        except VisaIOError:
            print('Failed to set sense averaging')
    
    def set_curr_range(self, source, max_current):
        """
        :SENSe[1]:CURRent[:DC]:RANGe[:UPPer] <n>
        :SENSe:CURRent:RANGe0.5
        Out 1
        Description <n> MIN(<=0.005)： 5mA range
                        MID(0.005<=?<=0.5): 500mA range
                        MAX(>0.5) : 5A range
        Out 2
        Description <n> MIN(<=0.005)： 5mA range
                        MAX(>0.005) : 1.5A range
        """
        try:
            command = ':SENS{}:CURR:RANG {:.3f}'.format(source, max_current)
            self.ps.write(command)
        except VisaIOError:
            print('Failed to set current range')
