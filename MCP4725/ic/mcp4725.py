# -*- coding: utf-8 -*-
import time

__author__ = 'yuanle@SmartGiant'
__version__ = '0.1'


class MCP4725Def:
    FAST_MODE = 0x00
    WRITE_DAC_REGISTER = 0x02
    WRITE_DAC_AND_EEPROM = 0x03

    POWER_MODE_NORMAL = 0x00
    POWER_MODE_1KOHM = 0x01
    POWER_MODE_100KOHM = 0x02
    POWER_MODE_500KOHM = 0x03
    TIMEOUT = 0.1
    DELAY = 0.001


class MCP4725Exception(Exception):
    def __init__(self, err_str):
        self._err_reason = '%s.' % (err_str)

    def __str__(self):
        return self._err_reason


class MCP4725(object):
    '''
    MCP4725 function class

    ClassType = DAC

    Args:
        i2c:        Instance(I2C)/None, i2c bus instance if not using.
        dev_addr:   hexmial,            mcp4725 i2c bus device address.
        mvref:      float, [2700-5500], default 3300.0, reference voltage.

    Examples:
        i2c = I2C('/dev/i2c-0')
        mcp4725 = MCP4725(i2c, 0x60, 3300)

    '''

    def __init__(self, i2c, dev_addr, mvref=3300.0):
        assert dev_addr & (~0x01) == 0x60
        assert mvref >= 2700 and mvref <= 5500
        self._dev_addr = dev_addr
        self._mvref = float(mvref)
        self._i2c_bus = i2c

    def output_volt_dc(self, volt):
        '''
        MCP4725 output dc voltage function

        Args:
            volt: float, output voltage.

        Examples:
            mcp4725.output_volt_dc(1000)

        '''
        assert volt >= 0 and volt <= self._mvref
        dac_code = int(volt * float(4096) / self._mvref)
        dac_code = ((dac_code << 4) & 0xFFF0)
        wr_data = [(MCP4725Def.WRITE_DAC_AND_EEPROM << 5) | (MCP4725Def.POWER_MODE_NORMAL << 1)]
        wr_data.extend([(dac_code >> 8) & 0xFF, dac_code & 0xff])
        self._i2c_bus.write(self._dev_addr, wr_data)

        lasttime = time.time()
        while time.time() - lasttime <= MCP4725Def.TIMEOUT:
            rd_data = self._i2c_bus.read(self._dev_addr, 5)
            if (rd_data[0] & 0x80) == 0x80:
                break

        if time.time() - lasttime > MCP4725Def.TIMEOUT:
            raise MCP4725Exception('Wait eeprom write completed timeout.')
        time.sleep(MCP4725Def.DELAY)

    def fast_output_volt_dc(self, volt):
        '''
        MCP4725 output dc voltage and will not wait ready for next output

        Args:
            volt: float, output voltage

        Examples:
            mcp4725.fast_output_volt_dc(1000)

        '''
        assert volt >= 0 and volt <= self._mvref
        dac_code = int(volt * float(4096) / self._mvref)
        reg_value = ((MCP4725Def.POWER_MODE_NORMAL << 11) | (dac_code & 0xFFF))
        self._i2c_bus.write(self._dev_addr, [(reg_value >> 8) & 0xFF, reg_value & 0xFF])
