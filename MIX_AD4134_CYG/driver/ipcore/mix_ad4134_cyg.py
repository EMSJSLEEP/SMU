# -*- coding: utf-8 -*-
from mix.driver.core.bus.axi4_lite_bus import AXI4LiteBus
import time

class MIXAD4134CYGDef:
    LOGIC_RESET = 0x10
    AD4134_CONFIG_REG = 0X28
    AD4134_STATUS_REG = 0X2C
    AD4134_SPI_CMD_REG = 0x30
    AD4134_SPI_RES_REG = 0x34
    AD4134_MEASURE_COUNT_REG = 0x3C
    AD4134_DATA_CHANNEL0_REG = 0x40
    AD4134_DATA_CHANNEL1_REG = 0x44
    AD4134_DATA_CHANNEL2_REG = 0x48
    AD4134_DATA_CHANNEL3_REG = 0x4C
    AD4134_DATA_REG = {0: 0x40, 1: 0x44, 2: 0x48, 3: 0x4C}
    AD4134_DMA_REG = 0x50
    AD4134_DEFALUT_MASK = (~(1 << 3))
    AD4134_SPI_ADDR_MASK = 0x7F00
    AD4134_SPI_DATA_MASK = 0xFF
    MCLK_RATE = 24e6
    CHANNEL_NUM = 4
    transfer_mode = {
        "stream": 1,
        "lite": 2,
        "all": 3
    }
    data_frame = {
        "16bit": 0,
        "16bit_CRC": 1,
        "24bit": 2,
        "24bit_CRC": 3
    }
    channel_format = {
        "Single-channel daisy-chain mode": 0,
        "Dual-channel daisy-chain mode": 1,
        "Quad-channel parallel output mode": 2,
        "Channel data averaging mode": 3
    }

    channel_dig_filter = {
        "Wideband filter": 0, 
        "Sinc6 filter": 1, 
        "Sinc3 filter": 2, 
        "Sinc3 filter with simultaneous 50 Hz and 60 Hz rejection": 3
    }

    POWER_MODE = {
        'low': (0, 32),
        'high': (3, 4)
    }
    REG_SIZE = 0x10000
    FLOAT_CONVERT_COFFEI = 2.3283064370807974e-10

    '''
    Here shows the registers address of AD4134
    '''
    POWER_MODE_SELECT_REG = 0x2
    TRANSFER_REG = 0xF
    DATA_PACKET_CONFIG = 0x11
    DIGITAL_INTERFACE_CONFIG = 0x12
    CHANNEL_DIG_FILTER_REG = 0x1E
    ODR_VAL_INT_LSB = 0x16
    ODR_VAL_INT_MID = 0x17
    ODR_VAL_INT_MSB = 0x18
    ODR_VAL_FLT_LSB = 0x19
    ODR_VAL_FLT_MID0 = 0x1A
    ODR_VAL_FLT_MID1 = 0x1B
    ODR_VAL_FLT_MSB = 0x1C

    

class MIXAD4134CYGException(Exception):
    '''
    MIXAD4134CYGException shows the exception of MIXAD4134CYG.

    '''
    def __init__(self, err_str):
        Exception.__init__(self, '%s.' % (err_str))

class MIXAD4134CYG(object):
    rpc_public_api = ['reset', 'get_reset_status', 'get_transfer_mode', 'set_transfer_mode', 'control_datalogger',
                      'set_data_frame', 'get_data_frame_format', 'set_ip_channel_format', 'measure',
                      'get_channel_format', 'get_spi_transfer_status', 'spi_write', 'spi_read',
                      'set_channels_dig_filter', 'get_channels_dig_filter', 'set_channels_packet_config',
                      'get_channels_packet_config', 'set_ad4134_power_mode', 'set_ad4134_parallel_output',
                      'set_ad4134_odr', 'set_measure_count', 'read_data', 'axi_write', 'axi_read']
    def __init__(self, axi4_bus):
        self.channel_num = MIXAD4134CYGDef.CHANNEL_NUM
        if isinstance(axi4_bus, str):
            self.axi4_bus = AXI4LiteBus(axi4_bus, MIXAD4134CYGDef.REG_SIZE)
        else:
            self.axi4_bus = axi4_bus

    def reset(self, timeout=0.1):
        '''
        Reset AD4134.

        Args:
            timeout, double, unit is second(default 0.1s).

        Examples:
            mix_ad4134_cyg.reset()
        '''
        self.axi4_bus.write_32bit_fix(MIXAD4134CYGDef.LOGIC_RESET, [0x2])
        used_data = self.axi4_bus.read_16bit_fix(MIXAD4134CYGDef.AD4134_CONFIG_REG, 1)[0]
        used_data = used_data & (~(1 << 3)) | 1
        change_data = used_data | (1 << 3)
        self.axi4_bus.write_16bit_fix(MIXAD4134CYGDef.AD4134_CONFIG_REG, [change_data])
        self.axi4_bus.write_16bit_fix(MIXAD4134CYGDef.AD4134_CONFIG_REG, [used_data])
        reset_finish_flag = False
        time_start = time.time()
        while time.time() - time_start < timeout:
            if self.get_reset_status() == True:
                reset_finish_flag = True
            else:
                reset_finish_flag = False
        assert reset_finish_flag, 'time out for ad4134 reseting.'
    
    def get_reset_status(self):
        '''
        Get chip reset status.

        Return:
            bool, Ture or False
        '''
        used_data = self.axi4_bus.read_16bit_fix(MIXAD4134CYGDef.AD4134_STATUS_REG, 1)[0]
        status = ((used_data & 0x4) >> 2) & ~((used_data & 0x200) >> 9) & ~((used_data & 0x400) >> 10)

        if status == 1:
            return False
        else:
            return True
    
    def get_transfer_mode(self):
        '''
        Get data transfer mode.

        Return:
            str, assert in ['lite', 'stream', 'all']
        '''
        used_data = self.axi4_bus.read_16bit_fix(MIXAD4134CYGDef.AD4134_STATUS_REG, 1)[0]
    
        transfer_status = used_data >> 4 & 0x3
       
        return [key for key, value in MIXAD4134CYGDef.transfer_mode.items() if value == transfer_status]
        
        
    def set_transfer_mode(self, mode):
        '''
        Set transfer mode to 'lite', 'stream', or 'all'

        Args:
            mode, str, assert in ['lite', 'stream', 'all']
        
        Return:
            str, "done"
        '''
        assert mode in ['lite', 'stream', 'all']
        used_data = self.axi4_bus.read_16bit_fix(MIXAD4134CYGDef.AD4134_CONFIG_REG, 1)[0]
        used_data &= ~0x30
        if mode == 'lite':
            change_data = used_data | 0x20 & MIXAD4134CYGDef.AD4134_DEFALUT_MASK | 1
        elif mode == 'stream':
            change_data = used_data | 0x10 & MIXAD4134CYGDef.AD4134_DEFALUT_MASK | 1
        else:
            change_data = used_data | 0x30 & MIXAD4134CYGDef.AD4134_DEFALUT_MASK | 1
        self.axi4_bus.write_16bit_fix(MIXAD4134CYGDef.AD4134_CONFIG_REG, [change_data])
        return "done"

    def set_data_frame(self, mode):
        '''
        Set fpga IP send data format.

        Args:
            mode, int, assert in [0, 1, 2, 3]
                "16bit": 0,
                "16bit_CRC": 1,
                "24bit": 2,
                "24bit_CRC": 3
        Return:
            str, "done"
        
        '''
        assert mode in [0, 1, 2, 3]
        used_data = self.axi4_bus.read_16bit_fix(MIXAD4134CYGDef.AD4134_CONFIG_REG, 1)[0]
        used_data &= ~0x300
        change_data = used_data | (mode << 8) & MIXAD4134CYGDef.AD4134_DEFALUT_MASK | 1
        self.axi4_bus.write_16bit_fix(MIXAD4134CYGDef.AD4134_CONFIG_REG, [change_data])
        return "done"
    
    def get_data_frame_format(self):
        '''
        Get data frame format from fpga IP.

        Return:
            frame, str, assert in ["16bit", "16bit_CRC", "24bit", "24bit_CRC"]
        '''
        used_data = self.axi4_bus.read_16bit_fix(MIXAD4134CYGDef.AD4134_CONFIG_REG, 1)[0]
        _bit = (used_data >> 8) & 0x3
        frame = [key for key, value in MIXAD4134CYGDef.data_frame.items() if value == _bit]
        return frame
    
    def set_ip_channel_format(self, mode):
        '''
        Set channel format of fpga ip.

        Args:
            mode, int, select in [0, 1, 2, 3]
                "Single-channel daisy-chain mode": 0,
                "Dual-channel daisy-chain mode": 1,
                "Quad-channel parallel output mode": 2,
                "Channel data averaging mode": 3
        Return:
            "done"    
        '''
        assert mode in [0, 1, 2, 3]
        used_data = self.axi4_bus.read_16bit_fix(MIXAD4134CYGDef.AD4134_CONFIG_REG, 1)[0]
        used_data &= ~0x0C0
        change_data = used_data | (mode << 6) & MIXAD4134CYGDef.AD4134_DEFALUT_MASK | 1
        self.axi4_bus.write_16bit_fix(MIXAD4134CYGDef.AD4134_CONFIG_REG, [change_data])
        return "done"
    
    def get_channel_format(self):
        '''
        Get channel format from IP.

        Return:
            format: str, "Single-channel daisy-chain mode",
                        "Dual-channel daisy-chain mode",
                        "Quad-channel parallel output mode",
                        "Channel data averaging mode"
        
        '''
        used_data = self.axi4_bus.read_16bit_fix(MIXAD4134CYGDef.AD4134_CONFIG_REG, 1)[0]
        _bit = (used_data >> 6) & 0x3
        format = [key for key, value in MIXAD4134CYGDef.channel_format.items() if value == _bit]
        return format

    def get_spi_transfer_status(self):
        '''
        Get spi transfer status.

        Return:
            True or "spi is busy"
        
        '''
        used_data = self.axi4_bus.read_16bit_fix(MIXAD4134CYGDef.AD4134_STATUS_REG, 1)[0]
        _bit = (used_data >> 7) & 0x7

        if _bit == 0:
            return True
        else:
            return "spi is busy"
    
    def spi_write(self, addr, data, timeout=0.1):
        '''
        Spi write operation for AD4134.

        Args:
            addr, int, 7bit unsigned value.
            data, int, 8bit unsigned value.
            timeout, double, unit is second(default 0.1s).

        Examples:
            mix_AD4134_cyg.spi_write(0x0, 0x12)

        '''
        assert isinstance(addr, int) and addr >= 0, 'invalid register address'
        assert isinstance(data, int) and data >= 0, 'invalid cmd data'
        assert timeout > 0, 'invalid timeout value'
        addr = addr & MIXAD4134CYGDef.AD4134_SPI_ADDR_MASK >> 8
        data = data & MIXAD4134CYGDef.AD4134_SPI_DATA_MASK
        self.axi4_bus.write_32bit_fix(MIXAD4134CYGDef.AD4134_SPI_CMD_REG, [addr << 8 | data])
        time_start = time.time()
        while time.time() - time_start < timeout:
           if self.get_spi_transfer_status() == True:
                return
        raise MIXAD4134CYGException('time out for spi write')

    def spi_read(self, addr, timeout=0.1):
        '''
        Spi read operation for AD4134.

        Args:
            addr, int, 7bit unsigned value.
            timeout, double, unit is second(default 0.1s).

        Examples:
            mix_AD4134_cyg.spi_read(0x0)

        '''
        assert isinstance(addr, int) and addr >= 0, 'invalid register address'
        assert timeout > 0, 'invalid timeout value'
        addr = addr & MIXAD4134CYGDef.AD4134_SPI_ADDR_MASK >> 8
        self.axi4_bus.write_32bit_fix(MIXAD4134CYGDef.AD4134_SPI_CMD_REG, [1 << 15 | addr << 8])
        time_start = time.time()
        while time.time() - time_start < timeout:
            if self.get_spi_transfer_status() == True:
                data = self.axi4_bus.read_32bit_fix(MIXAD4134CYGDef.AD4134_SPI_RES_REG, 1)[0] \
                    & MIXAD4134CYGDef.AD4134_SPI_DATA_MASK
                return data
        raise MIXAD4134CYGException('time out while spi writing before read')
    
    def set_channels_dig_filter(self, filter_mode_list):
        '''
        Set AD4134 channels digital filter format.

        Args:
            filter_mod_list: list, length of filter_mod_list should be 4, such as [0, 1, 2, 3] \
                 or [0, 0, 0, 0], each channel can be set to different filter format, there are 
                 4 types of filter: ["Wideband filter", "Sinc6 filter", "Sinc3 filter", 
                                    "Sinc3 filter with simultaneous 50 Hz and 60 Hz rejection"].
                channel_dig_filter = {
                    "Wideband filter": 0, 
                    "Sinc6 filter": 1, 
                    "Sinc3 filter": 2, 
                    "Sinc3 filter with simultaneous 50 Hz and 60 Hz rejection": 3
                    }
        Return:
            str, "done"
        '''
        w_data = 0
        for count, mode in enumerate(filter_mode_list):
            w_data |= (mode << 2 * count)
        self.spi_write(MIXAD4134CYGDef.CHANNEL_DIG_FILTER_REG, w_data)
        return "done"
    
    def get_channels_dig_filter(self):
        '''
        Get all channels digital filter.

        Returns:
            filter_list: list.
        '''
        filter_list = []
        r_data = self.spi_read(MIXAD4134CYGDef.CHANNEL_DIG_FILTER_REG)
        for count in range(4):
            _filter_bit = r_data >> (count * 2) & 0x3
            filter_format = [key for key, value in MIXAD4134CYGDef.channel_dig_filter.items() if _filter_bit == value]
            filter_list.append(filter_format[0])
        return filter_list
    
    def set_channels_packet_config(self, data_format, dclk_coeffi, dclk_status, dclk_mode):
        '''
        Set AD4134 channels data packet config.

        Args:
            data_format, int, assert in [0, 1, 2, 3]
                                        "16bit": 0,
                                        "16bit_CRC": 1,
                                        "24bit": 2,
                                        "24bit_CRC": 3
            dclk_coeffi, int, base_clock is 48MHz. set dclk to 12MHz, this param should be 2.
                         dclk = float(basc_clock / dclk_coeffi * 2)
            dclk_status, int, set dclk to output or input status.
                         0 is 'input', 1 is 'output' 
            dclk_mode, int, set dclk mode to free running or gated
                         0 is 'gate', 1 is 'free running'
        
        Return:
            str, "done"
        '''
        assert dclk_status in [0, 1]
        assert dclk_mode in [0, 1]
        used_data = self.axi4_bus.read_16bit_fix(MIXAD4134CYGDef.AD4134_CONFIG_REG, 1)[0]
        _bit = used_data & ~0xE
        change_data = _bit | (dclk_status << 1) | (dclk_mode << 2)
        self.axi4_bus.write_16bit_fix(MIXAD4134CYGDef.AD4134_CONFIG_REG, [change_data])
        w_data = dclk_coeffi | data_format << 4
        self.spi_write(MIXAD4134CYGDef.DATA_PACKET_CONFIG, w_data)
        return "done"
    
    def get_channels_packet_config(self):
        '''
        Get AD4134 channels data packet config.

        Returns:
            dict.
        '''
        info_dict = {"dclk_freq": "48MHz", "data_packt_frame": "16bit"}
        r_data = self.spi_read(MIXAD4134CYGDef.DATA_PACKET_CONFIG)
        dclk_freq_bit = r_data & 0xf
        if dclk_freq_bit == 0:
            info_dict["dclk_freq"] = "48MHz"
        else:
            info_dict["data_freq"] = f"{48.0 / dclk_freq_bit}MHz"
        data_format_bit = r_data >> 4 & 0x3
        data_format = [key for key, value in MIXAD4134CYGDef.data_frame.items() if data_format_bit == value]
        info_dict["data_packt_frame"] = data_format[0]

        return info_dict
    
    def set_ad4134_power_mode(self, power_mode):
        '''
        Set ad4134 power mode to fast or slow(Definition seeing the datasheet).
        This function will change the MCLK division at the same time.

        Args:
            power_mode, string, ['fast', 'slow']

        Exmaples:
            mix_ad4134_cyg.set_power_mode('fast')

        '''
        assert power_mode in ["fast", "slow"]
        use_data = self.spi_read(MIXAD4134CYGDef.POWER_MODE_SELECT_REG)
        if power_mode == 'fast':
            change_data = (use_data & ~0x1) | 1 
            self.spi_write(MIXAD4134CYGDef.POWER_MODE_SELECT_REG, change_data)
        else:
            change_data = (use_data & ~0x1)
            self.spi_write(MIXAD4134CYGDef.POWER_MODE_SELECT_REG, change_data)
            change_data = (use_data & ~0x1) | 1
            self.spi_write(MIXAD4134CYGDef.POWER_MODE_SELECT_REG, change_data)
            time.sleep(0.01)
            change_data &= ~0x1 
            self.spi_write(MIXAD4134CYGDef.POWER_MODE_SELECT_REG, change_data)
        return "done"
    
    def set_ad4134_parallel_output(self):
        '''
        Set AD4134 four channel parallel output data. each adc channel has a data pin.
        '''

        use_data = self.spi_read(MIXAD4134CYGDef.DIGITAL_INTERFACE_CONFIG)
        change_data = (use_data & ~0x3) | 0x02
        self.spi_write(MIXAD4134CYGDef.DIGITAL_INTERFACE_CONFIG, change_data)
        return "done"

    def set_ad4134_odr(self, odr):
        '''
        Set ad4134 output data rate.

        Args:
            odr, float, unit /ksps.
        Return:
            str, "done" 
        '''
        assert 0 < odr <= 1500
        if odr == 1500:
            odr == 1496
        f_base_addr = MIXAD4134CYGDef.ODR_VAL_FLT_LSB
        i_base_addr = MIXAD4134CYGDef.ODR_VAL_INT_LSB
        decimation_rate = MIXAD4134CYGDef.MCLK_RATE / (odr * 1e3)

        w_data = int(decimation_rate / MIXAD4134CYGDef.FLOAT_CONVERT_COFFEI)
        for count in range(4):
            f_bit = ((w_data >> (8 * count)) & 0xff)
            self.spi_write(f_base_addr + count, f_bit)
        for count in range(3):
            i_bit = (w_data >> (32 + 8 * count)) & 0xff
            self.spi_write(i_base_addr + count, i_bit)
        self.spi_write(MIXAD4134CYGDef.TRANSFER_REG, 1)
        return "done"
    
    def set_measure_count(self, num):
        '''
        Enable axi-lite bus and set measure count, move data to fifo.
        
        Args:
            num, int, num<=512.
        
        Return:
            str, "done".
        '''
        assert num <= 512
        self.axi4_bus.write_32bit_fix(MIXAD4134CYGDef.LOGIC_RESET, [0x2])
        time.sleep(0.01)
        self.axi4_bus.write_32bit_fix(MIXAD4134CYGDef.AD4134_MEASURE_COUNT_REG, [num])
        self.measure_count = num
        return "done"
    
    def read_data(self, count, timeout=5):
        '''
        Read data from fifo.

        Args:
            count, data numbers.
        Return:
            channels_data, list, data.
        '''
        channels_data = [[],[],[],[]]
        channel_data_base_addr = MIXAD4134CYGDef.AD4134_DATA_CHANNEL0_REG
        self.set_measure_count(count)
        time_start = time.time()
        while time.time() - time_start < timeout:
            if self.get_spi_transfer_status() == True:
                for count in range(self.measure_count):
                    for num in range(4):
                        channels_data[num].append(self.axi4_bus.read_32bit_fix(channel_data_base_addr + (4*num), 1)[0])
        return channels_data

    def decode_measurement(self, measurement):
        '''
        Decode MIXAD4134CYG values to voltages.

        Args:
            measurement, list. It is the adc data list from a channel such as [0x123, 0x234, 0x456].
                Each data contains 24-bit adc data.
    
        Return, list. [1000, 1000. 1000, 1000, ...], unit: mv

        Examples:
            mix_ad4134_cyg.decode_measurement([0x123, 0x123, 0x123, ...])

        '''
        data_list = []
        for item in measurement:
            vol = 5000 * (item & 0xffffff) / 0x7fffff
            data_list.append(vol)
        return data_list
 
    def measure(self, channel_list, number, timeout=0.5):
        '''
        Start a measure on all channels and automatically filter out not settled data.

        Args:
            number, int, The number of data than you want to get from one channel.
            timeout, float, default 0.5s.

        Return, dict. {0: [1000.0, 1001.0, 1002.0, 1001.0, ...], 1: [1000.0, ...], ...}, unit: mv.

        Example:
            mix_ad7768_cyg.measure()

        '''
        assert False not in [item in ["ch0","ch1","ch2","ch3"] for item in channel_list]
        assert timeout > 0, 'invalid timeout value'
        measurements = dict()
        time_start = time.time()
        self.set_measure_count(number)
        while time.time() - time_start < timeout:
            if self.get_spi_transfer_status() == True:
                for channel_name in channel_list:
                    ch = int(channel_name[2:])
                    measurements[ch] = self.axi4_bus.read_32bit_fix(MIXAD4134CYGDef.AD4134_DATA_REG[ch], number)
                for channel_index, data_list in measurements.items():
                    measurements[channel_index] = self.decode_measurement(data_list)
                return measurements
        raise MIXAD4134CYGException('time out while measuring')
    
    def axi_read(self, reg):
        '''
        Test func for axi-lite read.
        '''
        return self.axi4_bus.read_32bit_fix(reg, 1)[0]

    def axi_write(self, reg, data):
        '''
        Test func for axi-lite read.
        '''
        return self.axi4_bus.write_32bit_fix(reg, [data])
    
    def control_datalogger(self, status):
        '''
        Set datalogger time, measure time should <125ms and >0

        Args:
            time_ms: time to datalogger.
        Return:
            "done"
        '''
        self.axi4_bus.write_32bit_fix(MIXAD4134CYGDef.AD4134_DMA_REG, [status])
        return "done"
