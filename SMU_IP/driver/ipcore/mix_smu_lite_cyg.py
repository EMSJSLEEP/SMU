# -*- coding: utf-8 -*-
from mix.driver.core.bus.axi4_lite_bus import AXI4LiteBus
import time

__author__ = 'daining.chen@cygia.com'
__version__ = '0.1'


class MIXHERCULESIPREGDEF:
    IP_VER_REG = 0x00
    IP_TIME_REG = 0x04
    RESET_REG = 0x10
    SPI_CHOOSE_REG = 0x14
    SPI_STATUS_REG = 0x18
    SPI_WRITE_REG = 0x1C
    SPI_READ_REG = 0x20
    READ_BACK_REG = 0x24
    ENABLE_CMD_LIST_SEND_REG = 0x54
    CMD_LIST_STATUS_REG = 0x58
    CMD_STORE_LOAD_REG = 0x5C
    CMD_TIME_CONTROL = 0x60

class MIXHERCULESIPREGException(Exception):
    '''
    MIXHERCULESIPREGException shows the exception of MIXHERCULESIPREG.

    '''

    def __init__(self, err_str):
        Exception.__init__(self, '%s.' % (err_str))


class MIX_SMU_Lite_CYG(object):
    rpc_public_api = [
        'get_ip_time', 'enable_choose_spi', 'get_spi_status',
        'ad5522_spi_write', 'ad5522_spi_read', 'enable_cmd_list_send',
        'get_cmd_list_send_status','enable_loop_func'
    ]

    def __init__(self, axi4_bus):
        if isinstance(axi4_bus, str):
            self.axi4_bus = AXI4LiteBus(axi4_bus, 65536)
        else:
            self.axi4_bus = axi4_bus

    def get_ip_time(self):
        '''
        Get ip create time.

        Args:
            None.
        Return:
            value, string
        '''
        date = self.axi4_bus.read_32bit_fix(MIXHERCULESIPREGDEF.IP_TIME_REG,
                                            1)[0]
        date = hex(date)[2:]
        return date

    def reset(self):
        '''
        reset ip reg value to default.
        Args:
            None
        Return:
            str, "done"
        '''
        self.axi4_bus.write_32bit_fix(MIXHERCULESIPREGDEF.RESET_REG, [3])
        self.reset_ad5522()
        return "done"

    def enable_choose_spi(self, status):
        '''
        Enable ad5522 or ad7768 spi control.

        Args:
            status: int, [0, 1], 1 means "enable ad5522", 0 means "enable ad4134".
                    Once only one can be controlled.
        Return:
            "done"
        '''
        assert status in [0, 1]
        data = self.axi4_bus.read_32bit_fix(MIXHERCULESIPREGDEF.SPI_CHOOSE_REG,
                                            1)[0]
        data &= ~(1 << 0 | 1 << 1)
        data |= status
        self.axi4_bus.write_32bit_fix(MIXHERCULESIPREGDEF.SPI_CHOOSE_REG,
                                      [data])
        return 'done'

    def set_ADA4870_pin(self, status):
        '''
        Control GPIO named "ADA4870_PIN".
        Args:
            status: int, select in [0, 1]
        Return:
            str, "done"
        '''
        data = self.axi4_bus.read_32bit_fix(MIXHERCULESIPREGDEF.SPI_CHOOSE_REG, 1)[0]
        data &= ~(1 << 3 | 1 << 1)
        data |= status << 3
        self.axi4_bus.write_32bit_fix(MIXHERCULESIPREGDEF.SPI_CHOOSE_REG, [data])
        return "done"

    def reset_ad5522(self):
        '''
        reset ad5522
        '''
        reg = 0x1f
        self.axi4_bus.write_32bit_fix(MIXHERCULESIPREGDEF.SPI_CHOOSE_REG,
                                      [reg])
        return "done"

    def set_LOAD_pin(self, status):
        '''
        Control FPIO named "AD5522_LOAD"
        Args:
            status: int, select in [0, 1]
        Return:
            str, "done"
        '''
        data = self.axi4_bus.read_32bit_fix(MIXHERCULESIPREGDEF.SPI_CHOOSE_REG,
                                            1)[0]
        data &= ~(1 << 4 | 1 << 1)
        data |= status << 4
        self.axi4_bus.write_32bit_fix(MIXHERCULESIPREGDEF.SPI_CHOOSE_REG,
                                      [data])
        return "done"

    def get_spi_status(self):
        '''
        Get spi write and read busy status.

        Args:
            None.
        Return:
            [wirte_status, read_status]
        '''
        data = self.axi4_bus.read_32bit_fix(MIXHERCULESIPREGDEF.SPI_STATUS_REG,
                                            1)[0]
        wirte_status = data & 0x01
        read_status = (data & 0x02) >> 1

        return [wirte_status, read_status]

    def ad5522_spi_write(self, cmd):
        '''
        Control spi write for ad5522 reg.

        Args:
            cmd, int.
        Return:
            str, "done"
        '''
        self.axi4_bus.write_32bit_fix(MIXHERCULESIPREGDEF.SPI_WRITE_REG, [cmd])
        return 'done'

    def ad5522_spi_read(self, cmd):
        '''
        Control spi read for ad5522 reg.

        Args:
            cmd, int
        Return:
            reg_data, int
        '''
        self.axi4_bus.write_32bit_fix(MIXHERCULESIPREGDEF.SPI_READ_REG, [cmd])
        data = self.axi4_bus.read_32bit_fix(MIXHERCULESIPREGDEF.READ_BACK_REG,
                                            1)[0]
        return data

    def enable_cmd_list_send(self, is_loop):
        '''
        Enable ad5522 send cmd list
        
        Args:
            None
        Return:
            str, "done"
        '''
        cmd = 0x01 | is_loop << 1
        self.axi4_bus.write_32bit_fix(
            MIXHERCULESIPREGDEF.ENABLE_CMD_LIST_SEND_REG, [cmd])
        return "done"

    def enable_loop_func(self, is_loop):
        '''
        Enable ad5522 send cmd list
        
        Args:
            is_loop, int, [0, 1]
        Return:
            str, "done"
        '''
        cmd = 0x00 | int(is_loop) << 1
        self.axi4_bus.write_32bit_fix(
            MIXHERCULESIPREGDEF.ENABLE_CMD_LIST_SEND_REG, [cmd])
        return "done"

    def get_cmd_list_send_status(self):
        '''
        Get ad5522 cmd list send status.

        Args:
            None.
        Return:
            int, [0, 1], 0 means send success; 1 means sengding. 
        
        '''
        data = self.axi4_bus.read_32bit_fix(
            MIXHERCULESIPREGDEF.CMD_LIST_STATUS_REG, 1)[0]
        return data
    
    def write_cmd_list(self, cmd, if_load, delay_time):
        '''
        Write cmd to FIFO, max cmd count is 64.

        Args:
            cmd_list: int
            if_load: select in [0, 1]
            delay_time: int
        Return:
            "done"
        '''
        cmd_list_reg = cmd | (if_load << 31)
        cmd_delay_reg = delay_time
        self.axi4_bus.write_32bit_fix(MIXHERCULESIPREGDEF.CMD_STORE_LOAD_REG, [cmd_list_reg])
        self.axi4_bus.write_32bit_fix(MIXHERCULESIPREGDEF.CMD_TIME_CONTROL, [cmd_delay_reg])
        return 'done'         