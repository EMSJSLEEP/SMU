# -*- coding: utf-8 -*-
from mix.driver.core.bus.axi4_lite_bus import AXI4LiteBus
import time

__author__ = 'daining.chen@cygia.com'
__version__ = '0.2'


class MIXAD7768CYGDef:
    '''
    Here shows the IP core register.

    '''
    AD7768_CONFIG_REG = 0x28
    AD7768_STATUS_REG = 0x2C
    AD7768_SPI_CMD_REG = 0x30
    AD7768_SPI_RES_REG = 0x34
    AD7768_ONESHOT_PERIOD_REG = 0x38
    AD7768_LITE_DATA_NUMBER_REG = 0x3C
    AD7768_DATA_REG = {0: 0x40, 1: 0x44, 2: 0x48, 3: 0x4C}
    AD7768_STREAM_DATA_TIME_REG = 0x50

    # Mask
    AD7768_CONFIG_MASK = 0x3F
    AD7768_LITE_SWITCH_MASK = 0x20
    AD7768_STREAM_SWITCH_MASK = 0x10
    AD7768_CONVERSION_MODE_MASK = 0x8
    AD7768_RESET_MASK = 0x4
    AD7768_SYNC_MASK = 0x3
    AD7768_CONTROL_MODE_MASK = 0x1
    AD7768_RESET_STATUS_MASK = 0x200
    AD7768_AXI_LITE_BUSY_MASK = 0x100
    AD7768_AXI_STREAM_BUSY_MASK = 0x80
    AD7768_SPI_BUSY_MASK = 0x40
    AD7768_RESET_SEND_MASK = 0x4
    AD7768_SYNC_SEND_MASK = 0x2
    AD7768_SPI_ADDR_MASK = 0x7F00
    AD7768_SPI_DATA_MASK = 0xFF

    # Parameter definition
    AD7768_CONTROL_MODE = {'pin': 0, 'spi': 1, 0: 'pin', 1: 'spi'}
    AD7768_CONVERSION_MODE = {'standard': 0, 'oneshot': 1, 0: 'standard', 1: 'oneshot'}
    AD7768_MAX_DATA_NUMBER = 8192
    AD7768_CAHNNEL_NUM = 4
    FPGA_WORK_FREQUENCE = 125000000
    REG_SIZE = 0x10000

    '''
    Here shows the registers address of AD7768

    '''
    MODEA_REG = 0x1
    MODEB_REG = 0x2
    AB_MODE_SELECT_REG = 0x3
    POWER_MODE_SELECT_REG = 0x4
    INTERFACE_CONFIGURATION_REG = 0x7
    REVISION_IDENTIFICATION_REG = 0xA
    GAIN_CHANNEL_REG = {4: {0: 0x36, 1: 0x39, 2: 0x42, 3: 0x45},
                        8: {0: 0x36, 1: 0x39, 2: 0x3C, 3: 0x3F, 4: 0x42, 5: 0x45, 6: 0x48, 7: 0x4B}}
    OFFSET_CHANNEL_REG = {4: {0: 0x1E, 1: 0x21, 2: 0x2A, 3: 0x2D},
                          8: {0: 0x1E, 1: 0x21, 2: 0x24, 3: 0x27, 4: 0x2A, 5: 0x2D, 6: 0x30, 7: 0x33}}

    # Mask
    PER_CHANNEL_MODE_MASK = 0x1
    FILETER_MASK = 0x8
    DECIMATION_MASK = 0x7
    POWER_MODE_MASK = 0x30
    MCLK_DIV_MASK = 0x3
    DCLK_DIV_MASK = 0x3
    GAIN_OR_OFFSET_MASK = 0XFFFFFF
    GAIN_OR_OFFSET_MSB_MASK = 0XFF0000
    GAIN_OR_OFFSET_MID_MASK = 0X00FF00
    GAIN_OR_OFFSET_LSB_MASK = 0X0000FF
    ERROR_FLAGGED_MASK = 0x80000000
    FILTER_NOT_SETTLED_MASK = 0x40000000
    REPEATED_DATA_MASK = 0x20000000
    FILTER_TYPE_MASK = 0x10000000
    FILTER_SATURATED_MASK = 0x8000000
    CHANNEL_ID_MASK = 0x7000000
    DATA_MASK = 0xFFFFFF
    DATA_MASK = (1 << 24) - 1

    # Parameter definition
    GAIN_OR_OFFSET_BYTES = 3
    DATA_WIDTH = 24
    CHANNEL_NUM = 4
    CONTROL_MODE = ('pin', 'spi')
    CONVERSION_MODE = ('standard', 'oneshot')
    CLOCKSEL = ("external", "crystal")
    POWER_MODE = {
        'low': (0, 32),
        'media': (2, 8),
        'fast': (3, 4)
    }  # power mode value and its typical mclk div(fMOD)
    POWER_MODE_RE = {
        0: 'low',
        2: 'media',
        3: 'fast'
    }
    MCLK_DIV = {32: 0, 8: 2, 4: 3}  # DIV VALUE: CONFIG VALUE
    MCLK_DIV_RE = {0: 32, 2: 8, 3: 4}  # CONFIG VALUE: DIV VALUE
    DCLK_DIV = {8: 0, 4: 1, 2: 2, 1: 3}  # DIV: CONFIG VALUE
    DCLK_DIV_RE = {0: 8, 1: 4, 2: 2, 3: 1}  # CONFIG VALUE: DIV
    SAMPLING_CONFIG_TABLE = {
        'low': [1, 2, 4, 8, 16, 32],
        'media': [4, 8, 16, 32, 64, 128],
        'fast': [8, 16, 32, 64, 128, 256]
    }  # sampling speed unit: kSPS

    # independent: each channel use a dout line
    # tdm_single: only use dout0
    # tdm_double: dout0 for ch0~3 and dout1 for ch4~7(cannot be used for AD7768-4)
    DOUT_CONFIG = ('independent', 'tdm_single', 'tdm_double')
    FILTER = {'sinc5': 1, 'wideband': 0}
    FILTER_RE = {1: 'sinc5', 0: 'wideband'}
    DECIMATION = {32: 0, 64: 1, 128: 2, 256: 3, 512: 4, 1024: 5}  # DECIMATION VALUE: CONFIG VALUE
    DECIMATION_RE = {0: 32, 1: 64, 2: 128, 3: 256, 4: 512, 5: 1024}  # CONFIG VALUE: DECIMATION VALUE
    CHANNEL_MODE = {'A': 0, 'B': 1}  # MODE: VALUE
    CHANNEL_MODE_RE = {0: 'A', 1: 'B'}  # VALUE: MODE
    DEFAULT_GAIN = 0x555555
    DEFAULT_OFFSET = 0
    REVISION_ID = 0x06
    MAX_LOGGER_TIME = 125  # ms


class MIXAD7768CYGException(Exception):
    '''
    MIXAD7768CYGException shows the exception of MIXAD7768CYG.

    '''
    def __init__(self, err_str):
        Exception.__init__(self, '%s.' % (err_str))


class MIXAD7768CYG:
    rpc_public_api = ['reset', 'set_control_mode', 'get_control_mode', 'sync', 'spi_write',
                      'spi_read', 'set_conversion_mode', 'get_conversion_mode', 'set_mode',
                      'get_mode', 'set_channel_mode', 'get_channel_mode', 'set_dclk',
                      'get_dclk', 'set_power_mode', 'get_power_mode', 'set_gain',
                      'get_gain', 'set_offset', 'get_offset', 'filter_measurement',
                      'decode_measurement', 'set_lite', 'get_lite', 'set_stream',
                      'get_stream', 'start_lite', 'busy_lite', 'busy_stream', 'measure',
                      'set_oneshot_frequency', 'get_oneshot_frequency', 'get_revision_id']

    def __init__(self, axi4_bus, ref1, ref2):
        '''
        AD7768 ADC function class.

        Args:
            ref1, int, The Reference 1 voltage, mV.
            ref2, int. The Reference 2 voltage, mV.

        '''
        if isinstance(axi4_bus, str):
            self.axi4_bus = AXI4LiteBus(axi4_bus, MIXAD7768CYGDef.REG_SIZE)
        else:
            self.axi4_bus = axi4_bus
        self.channel_num = MIXAD7768CYGDef.CHANNEL_NUM
        self.reference_voltate = {'ref1': ref1, 'ref2': ref2}

    def reset(self, timeout=0.1):
        '''
        Reset AD7768.

        Args:
            timeout, float(unit: second, default 0.1s).

        Examples:
            mix_ad7768_cyg.reset()

        '''
        assert timeout > 0, 'timeout value should bigger than 0'
        self.axi4_bus.write_32bit_fix(MIXAD7768CYGDef.AD7768_CONFIG_REG, [MIXAD7768CYGDef.AD7768_RESET_MASK])
        reset_send_flag = False
        reset_finish_flag = False
        time_start = time.time()
        while time.time() - time_start < timeout:
            data = self.axi4_bus.read_32bit_fix(MIXAD7768CYGDef.AD7768_STATUS_REG, 1)[0]
            if data & MIXAD7768CYGDef.AD7768_RESET_SEND_MASK != 0:
                reset_send_flag = True
            if reset_send_flag and data & MIXAD7768CYGDef.AD7768_RESET_STATUS_MASK == 0:
                reset_finish_flag = True
                break
        assert reset_send_flag, 'time out for sending ad7768 reset signal.'
        assert reset_finish_flag, 'time out for ad7768 reseting.'

    def set_control_mode(self, control_mode):
        '''
        Set control mode(pin or spi).

        Args:
            control_mode, string, ['pin', 'spi']

        Examples:
            mix_ad7768_cyg.set_control_mode('spi')

        '''
        assert control_mode in MIXAD7768CYGDef.CONTROL_MODE, 'not supported control mode'
        data = self.axi4_bus.read_32bit_fix(MIXAD7768CYGDef.AD7768_CONFIG_REG, 1)[0] \
            & MIXAD7768CYGDef.AD7768_CONFIG_MASK
        if control_mode == 'spi':
            data = data | MIXAD7768CYGDef.AD7768_CONTROL_MODE_MASK
        elif control_mode == 'pin':
            data = data & ~MIXAD7768CYGDef.AD7768_CONTROL_MODE_MASK
        self.axi4_bus.write_32bit_fix(MIXAD7768CYGDef.AD7768_CONFIG_REG, [data])

    def get_control_mode(self):
        '''
        Get current control mode.

        Return, string, ['pin', 'spi']

        Examples:
            mix_ad7768_cyg.get_control_mode()

        '''
        control_mode = self.axi4_bus.read_32bit_fix(MIXAD7768CYGDef.AD7768_CONFIG_REG, 1)[0] \
            & MIXAD7768CYGDef.AD7768_CONTROL_MODE_MASK
        control_mode = MIXAD7768CYGDef.AD7768_CONTROL_MODE[control_mode]
        return control_mode

    def sync(self, timeout=0.1):
        '''
        After modifying the configuration, you need to use this api to
        synchronize the configuration for the modification to take effect

        Args:
            timeout, float(default 0.1s).

        Examples:
            mix_ad7768_cyg.sync()

        '''
        assert timeout > 0, 'invalid timeout value'
        self.axi4_bus.write_32bit_fix(MIXAD7768CYGDef.AD7768_CONFIG_REG, [MIXAD7768CYGDef.AD7768_SYNC_MASK])
        time_start = time.time()
        while time.time() - time_start < timeout:
            data = self.axi4_bus.read_32bit_fix(MIXAD7768CYGDef.AD7768_STATUS_REG, 1)[0]
            if data & MIXAD7768CYGDef.AD7768_SYNC_SEND_MASK != 0:
                return
        raise MIXAD7768CYGException('time out for sending ad7768 sync signal')

    def spi_write(self, addr, data, timeout=0.1):
        '''
        Spi write operation for AD7768.

        Args:
            addr, int, 7bit unsigned value.
            data, int, 8bit unsigned value.
            timeout, float(default 0.1s).

        Examples:
            mix_ad7768_cyg.spi_write(0x0, 0x12)

        '''
        assert isinstance(addr, int) and addr >= 0, 'invalid register address'
        assert isinstance(data, int) and data >= 0, 'invalid cmd data'
        assert timeout > 0, 'invalid timeout value'
        addr = addr & MIXAD7768CYGDef.AD7768_SPI_ADDR_MASK >> 8
        data = data & MIXAD7768CYGDef.AD7768_SPI_DATA_MASK
        self.axi4_bus.write_32bit_fix(MIXAD7768CYGDef.AD7768_SPI_CMD_REG, [addr << 8 | data])
        time_start = time.time()
        while time.time() - time_start < timeout:
            spi_busy_status = self.axi4_bus.read_32bit_fix(MIXAD7768CYGDef.AD7768_STATUS_REG, 1)[0] \
                    & MIXAD7768CYGDef.AD7768_SPI_BUSY_MASK
            if spi_busy_status == 0:
                return
        raise MIXAD7768CYGException('time out for spi write')

    def spi_read(self, addr, timeout=0.1):
        '''
        Spi read operation for AD7768.

        Args:
            addr, int, 7bit unsigned value.
            timeout, float(default 0.1s).

        Examples:
            mix_ad7768_cyg.spi_read(0x0)

        '''
        assert isinstance(addr, int) and addr >= 0, 'invalid register address'
        assert timeout > 0, 'invalid timeout value'
        addr = addr & MIXAD7768CYGDef.AD7768_SPI_ADDR_MASK >> 8
        self.axi4_bus.write_32bit_fix(MIXAD7768CYGDef.AD7768_SPI_CMD_REG, [1 << 15 | addr << 8])
        time_start = time.time()
        while time.time() - time_start < timeout:
            spi_busy_status = self.axi4_bus.read_32bit_fix(MIXAD7768CYGDef.AD7768_STATUS_REG, 1)[0] \
                    & MIXAD7768CYGDef.AD7768_SPI_BUSY_MASK
            if spi_busy_status == 0:
                data = self.axi4_bus.read_32bit_fix(MIXAD7768CYGDef.AD7768_SPI_RES_REG, 1)[0] \
                    & MIXAD7768CYGDef.AD7768_SPI_DATA_MASK
                return data
        raise MIXAD7768CYGException('time out while spi writing before read')

    def set_conversion_mode(self, conversion_mode):
        '''
        Set conversion mode(standard or oneshot).

        Args:
            conversion_mode, string, ['standard', 'oneshot']

        Examples:
            mix_ad7768_cyg.set_conersion_mode('standard')

        '''
        assert conversion_mode in MIXAD7768CYGDef.CONVERSION_MODE, 'not supported conversion mode'
        data = self.axi4_bus.read_32bit_fix(MIXAD7768CYGDef.AD7768_CONFIG_REG, 1)[0] \
            & MIXAD7768CYGDef.AD7768_CONFIG_MASK
        if conversion_mode == 'standard':
            data = data & ~MIXAD7768CYGDef.AD7768_CONVERSION_MODE_MASK
        else:
            data = data | MIXAD7768CYGDef.AD7768_CONVERSION_MODE_MASK
        self.axi4_bus.write_32bit_fix(MIXAD7768CYGDef.AD7768_CONFIG_REG, [data])
        self.sync()

    def get_conversion_mode(self):
        '''
        Get the current conversion mode.

        Return, string, ['standard', 'oneshot']

        Examples:
            mix_ad7768_cyg.get_conversion_mode()

        '''
        conversion_mode = (self.axi4_bus.read_32bit_fix(MIXAD7768CYGDef.AD7768_STATUS_REG, 1)[0]
                           & MIXAD7768CYGDef.AD7768_CONVERSION_MODE_MASK) >> 3
        conversion_mode = MIXAD7768CYGDef.AD7768_CONVERSION_MODE[conversion_mode]
        return conversion_mode

    def set_mode(self, mode, filter, decimation):
        '''
        Set the configuration of channel mode A or channel mode B.

        Args:
            mode, string, ['A', 'B']
            filter, string, ['sinc5', 'wideband']
            decimation, int, [32, 64, 128, 256, 512, 1024]

        Examples:
            mix_ad7768_cyg.set_mode('A', 'sinc5', 32)

        '''
        if self.get_control_mode() == 'spi':
            assert filter in MIXAD7768CYGDef.FILTER, 'not supported filter'
            assert decimation in MIXAD7768CYGDef.DECIMATION, 'not supported decimation'
            assert mode in MIXAD7768CYGDef.CHANNEL_MODE, 'wrong channel mode'
            data = MIXAD7768CYGDef.FILTER[filter] << 3 | MIXAD7768CYGDef.DECIMATION[decimation]
            if mode == 'A':
                self.spi_write(MIXAD7768CYGDef.MODEA_REG, data)
            else:
                self.spi_write(MIXAD7768CYGDef.MODEB_REG, data)
            self.sync()
        else:
            raise MIXAD7768CYGException('operation not implemented for pin mode')

    def get_mode(self, mode):
        '''
        Get channel mode A or channel mode B's configuration.

        Args:
            mode, string, ['A', 'B']

        Return, dict, {'filter': 'sinc5', 'decimation': 32}

        Examples:
            mix_ad7768_cyg.get_mode('A')

        '''
        if self.get_control_mode() == 'spi':
            assert mode in MIXAD7768CYGDef.CHANNEL_MODE, 'wrong channel mode'
            if mode == 'A':
                data = self.spi_read(MIXAD7768CYGDef.MODEA_REG)
            else:
                data = self.spi_read(MIXAD7768CYGDef.MODEB_REG)
            filter = MIXAD7768CYGDef.FILTER_RE[(data & MIXAD7768CYGDef.FILETER_MASK) >> 3]
            decimation = MIXAD7768CYGDef.DECIMATION_RE[data & MIXAD7768CYGDef.DECIMATION_MASK]
            return {'filter': filter, 'decimation': decimation}
        else:
            raise MIXAD7768CYGException('operation not implemented for pin mode')

    def set_channel_mode(self, channel_index, mode):
        '''
        Specilize channel's mode.

        Args:
            channel_index, int, 0~3
            mode: string, 'A' or 'B'

        Examples:
            mix_ad7768_cyg.set_channel_mode(0, 'A')

        '''
        if self.get_control_mode() == 'spi':
            assert isinstance(channel_index, int) and 0 <= channel_index and channel_index < self.channel_num, \
                'invalid channel index'
            assert mode in MIXAD7768CYGDef.CHANNEL_MODE, 'invalid channel mode'
            data = self.spi_read(MIXAD7768CYGDef.AB_MODE_SELECT_REG)
            if mode == 'A':
                data = data & ~(1 << channel_index)
            else:  # mode B
                data = data | 1 << channel_index
            if self.channel_num == 4 and channel_index > 1:
                if mode == 'A':
                    data = data & ~(1 << channel_index + 2)
                else:  # mode B
                    data = data | 1 << channel_index + 2
            self.spi_write(MIXAD7768CYGDef.AB_MODE_SELECT_REG, data)
            self.sync()
        else:
            raise MIXAD7768CYGException('operation not implemented for pin mode')

    def get_channel_mode(self, channel_index):
        '''
        Get channel's mode

        Args:
            channel_index, int, 0~3

        Return:
            string, 'A' or 'B'

        Examples:
            mix_ad7768_cyg.get_channel_mode(0)

        '''
        if self.get_control_mode() == 'spi':
            assert isinstance(channel_index, int) and 0 <= channel_index and channel_index < self.channel_num, \
                'invalid channel index'
            data = self.spi_read(MIXAD7768CYGDef.AB_MODE_SELECT_REG)
            channel_mode = MIXAD7768CYGDef.CHANNEL_MODE_RE[data >> channel_index & MIXAD7768CYGDef.PER_CHANNEL_MODE_MASK]
            return channel_mode
        else:
            raise MIXAD7768CYGException('operation not implemented for pin mode')

    def set_dclk(self, dclk_div):
        '''
        Set the DCLK division.

        Args:
            dclk_div, int, [8, 4, 2, 1]

        Examples:
            mix_ad7768_cyg.set_dclk(2)

        '''
        if self.get_control_mode() == 'spi':
            assert dclk_div in MIXAD7768CYGDef.DCLK_DIV, 'not supported dclk division'
            data = self.spi_read(MIXAD7768CYGDef.INTERFACE_CONFIGURATION_REG)
            data = data & ~MIXAD7768CYGDef.DCLK_DIV_MASK | MIXAD7768CYGDef.DCLK_DIV[dclk_div]
            self.spi_write(MIXAD7768CYGDef.INTERFACE_CONFIGURATION_REG, data)
            self.sync()
        else:
            raise MIXAD7768CYGException('operation not implemented for pin mode')

    def get_dclk(self):
        '''
        Get the current DCLK division value.

        Return, int, [8, 4, 2, 1]

        Examples:
            mix_ad7768_cyg.get_dclk()

        '''
        if self.get_control_mode() == 'spi':
            data = self.spi_read(MIXAD7768CYGDef.INTERFACE_CONFIGURATION_REG)
            dclk_div = MIXAD7768CYGDef.DCLK_DIV_RE[data & MIXAD7768CYGDef.DCLK_DIV_MASK]
            return dclk_div
        else:
            raise MIXAD7768CYGException('operation not implemented for pin mode')

    def set_power_mode(self, power_mode):
        '''
        Set power mode(fast, media or slow. See the datasheet).
        This function will change the MCLK division.

        Args:
            power_mode, string, ['fast', 'media', 'slow']

        Exmaples:
            mix_ad7768_cyg.set_power_mode('fast')

        '''
        if self.get_control_mode() == 'spi':
            assert power_mode in MIXAD7768CYGDef.POWER_MODE, 'not supported power mode'
            data = self.spi_read(MIXAD7768CYGDef.POWER_MODE_SELECT_REG)
            data = data & ~MIXAD7768CYGDef.POWER_MODE_MASK | MIXAD7768CYGDef.POWER_MODE[power_mode][0] << 4
            data = data & ~MIXAD7768CYGDef.MCLK_DIV_MASK | \
                MIXAD7768CYGDef.MCLK_DIV[MIXAD7768CYGDef.POWER_MODE[power_mode][1]]
            self.spi_write(MIXAD7768CYGDef.POWER_MODE_SELECT_REG, data)
            self.sync()
        else:
            raise MIXAD7768CYGException('operation not implemented for pin mode')

    def get_power_mode(self):
        '''
        Get power mode and it's MCLK division.

        Return, dic, {'power mode': 'fast', 'mclk division': 4}

        Examples:
            mix_ad7768_cyg.get_power_mode()

        '''
        if self.get_control_mode() == 'spi':
            data = self.spi_read(MIXAD7768CYGDef.POWER_MODE_SELECT_REG)
            power_mode = MIXAD7768CYGDef.POWER_MODE_RE[(data & MIXAD7768CYGDef.POWER_MODE_MASK) >> 4]
            mclk = MIXAD7768CYGDef.MCLK_DIV_RE[data & MIXAD7768CYGDef.MCLK_DIV_MASK]
            return {'power mode': power_mode, 'mclk division': mclk}
        else:
            raise MIXAD7768CYGException('operation not implemented for pin mode')

    def set_gain(self, channel_index, gain):
        '''
        Set gain coefficient used for calibration.

        Args:
            channel_index, int, 0~3
            gain, int, 24bit unsigned value

        Examples:
            mix_ad7768_cyg.set_gain(0, 0x555555)

        '''
        if self.get_control_mode() == 'spi':
            assert 0 <= channel_index and channel_index < self.channel_num, 'invalid channel index'
            assert 0 <= gain and gain < (1 << MIXAD7768CYGDef.GAIN_OR_OFFSET_BYTES * 8), 'invalid gain value'
            gain_bytes_addrs = [MIXAD7768CYGDef.GAIN_CHANNEL_REG[self.channel_num][channel_index] + index
                                for index in range(MIXAD7768CYGDef.GAIN_OR_OFFSET_BYTES)]
            gain_bytes_values = [(gain & MIXAD7768CYGDef.GAIN_OR_OFFSET_MSB_MASK) >> 16,
                                 (gain & MIXAD7768CYGDef.GAIN_OR_OFFSET_MID_MASK) >> 8,
                                 gain & MIXAD7768CYGDef.GAIN_OR_OFFSET_LSB_MASK]
            for index in range(MIXAD7768CYGDef.GAIN_OR_OFFSET_BYTES):
                self.spi_write(gain_bytes_addrs[index], gain_bytes_values[index])
            self.sync()
        else:
            raise MIXAD7768CYGException('operation not implemented for pin mode')

    def get_gain(self, channel_index):
        '''
        Get gain coefficient.

        Args:
            channel_index, int, 0~3

        Return, int, 24bit unsigned value

        Example:
            mix_ad7768_cyg.get_gain(0)

        '''
        if self.get_control_mode() == 'spi':
            assert 0 <= channel_index and channel_index < self.channel_num, 'invalid channel index'
            gain = 0
            gain_bytes_addrs = [MIXAD7768CYGDef.GAIN_CHANNEL_REG[self.channel_num][channel_index] + index
                                for index in range(MIXAD7768CYGDef.GAIN_OR_OFFSET_BYTES)]
            for item in gain_bytes_addrs:
                data = self.spi_read(item)
                gain = (gain << 8) | data
            return gain
        else:
            raise MIXAD7768CYGException('operation not implemented for pin mode')

    def set_offset(self, channel_index, offset):
        '''
        Set offset coefficient used for calibration.

        Args:
            channel_index, 0~3
            offset, int, 24bit unsigned value

        Examples:
            mix_ad7768_cyg.set_channel_offset(0, 0)

        '''
        if self.get_control_mode() == 'spi':
            assert 0 <= channel_index and channel_index < self.channel_num, 'invalid channel index'
            assert 0 <= offset and offset < (1 << MIXAD7768CYGDef.GAIN_OR_OFFSET_BYTES * 8), 'invalid offset value'
            offset_bytes_addrs = [MIXAD7768CYGDef.OFFSET_CHANNEL_REG[self.channel_num][channel_index] + index
                                  for index in range(MIXAD7768CYGDef.GAIN_OR_OFFSET_BYTES)]
            offset_bytes_values = [(offset & MIXAD7768CYGDef.GAIN_OR_OFFSET_MSB_MASK) >> 16,
                                   (offset & MIXAD7768CYGDef.GAIN_OR_OFFSET_MID_MASK) >> 8,
                                   offset & MIXAD7768CYGDef.GAIN_OR_OFFSET_LSB_MASK]
            for index in range(MIXAD7768CYGDef.GAIN_OR_OFFSET_BYTES):
                self.spi_write(offset_bytes_addrs[index], offset_bytes_values[index])
            self.sync()
        else:
            raise MIXAD7768CYGException('operation not implemented for pin mode')

    def get_offset(self, channel_index):
        '''
        Get offset coefficient.

        Args:
            channel_index, int, 0~3

        Return, int, 24bit unsigned value

        Example:
            mix_ad7768_cyg.get_channel_offset(0)

        '''
        if self.get_control_mode() == 'spi':
            assert 0 <= channel_index and channel_index < self.channel_num, 'invalid channel index'
            offset = 0
            offset_bytes_addrs = [MIXAD7768CYGDef.OFFSET_CHANNEL_REG[self.channel_num][channel_index] + index
                                  for index in range(MIXAD7768CYGDef.GAIN_OR_OFFSET_BYTES)]
            for item in offset_bytes_addrs:
                data = self.spi_read(item)
                offset = (offset << 8) | data
            return offset
        else:
            raise MIXAD7768CYGException('operation not implemented for pin mode')

    def filter_measurement(self, measurement):
        '''
        Filter out net settled data in one channel's measurements.

        Args:
            measurement, list, [0x40000000, 0x40FFFFFF, 0x00FFFFFF, ...]

        Return: list, settled data

        Examples:
            mix_ad7768_cyg.filter_measurement(measurement)

        '''
        data_list = []
        for item in measurement:
            # choose only settled data
            if item & MIXAD7768CYGDef.FILTER_NOT_SETTLED_MASK == 0:
                data_list.append(item)
        return data_list

    def decode_measurement(self, measurement, ref, gain=0x555555, offset=0):
        '''
        Decode adc data to voltages.

        Args:
            measurement, list. It is a data list such as [0x123, 0x234, 0x456].
                Each data contains a 8-bit header and a 24-bit adc data.
            ref, int. The reference voltage, unit: mv.
            gain, int. It is the gain coefficient.
            offset, int. It is the offset coefficient.

        Return, list. [1000, 1000. 1000, 1000, ...], unit: mv

        Examples:
            mix_ad7768_cyg.decode_measurement([0x123, 0x123, 0x123, ...], 5000, 0x555555, 0)

        '''
        data_list = []
        data_width = MIXAD7768CYGDef.GAIN_OR_OFFSET_BYTES * 8
        for item in measurement:
            # delete the header
            item = item & MIXAD7768CYGDef.DATA_MASK
            # change to signed data
            item = item - (1 << data_width) if item & (1 << data_width - 1) else item
            # The formula comes from the data book
            data_calculated = (item * 2**44 / (gain * 4194300) + offset) * ref / (3 * 2**21)
            data_list.append(data_calculated)
        return data_list

    def set_lite(self, flag):
        '''
        Enable or disable axi-lite data bus for transfer data.

        Args:
            flag, string, ['on', 'off']

        Exmaples:
            mix_ad7768_cyg.set_lite('on')

        '''
        assert flag in ['on', 'off'], 'not supported switch flag'
        data = self.axi4_bus.read_32bit_fix(MIXAD7768CYGDef.AD7768_CONFIG_REG, 1)[0]
        if flag == 'on':
            data = data | MIXAD7768CYGDef.AD7768_LITE_SWITCH_MASK
        else:
            data = data & ~MIXAD7768CYGDef.AD7768_LITE_SWITCH_MASK
        self.axi4_bus.write_32bit_fix(MIXAD7768CYGDef.AD7768_CONFIG_REG, [data])

    def get_lite(self):
        '''
        Get axi-lite data bus status.

        Return: string, ['on', 'off']

        Exmaples:
            mix_ad7768_cyg.get_lite()

        '''
        data = self.axi4_bus.read_32bit_fix(MIXAD7768CYGDef.AD7768_CONFIG_REG, 1)[0]
        if data & MIXAD7768CYGDef.AD7768_LITE_SWITCH_MASK != 0:
            return 'on'
        else:
            return 'off'

    def set_stream(self, flag):
        '''
        Enable or disable axi-stream data bus for transfer data.

        Args:
            flag, string, ['on', 'off']

        Exmaples:
            mix_ad7768_cyg.set_stream('on')

        '''
        assert flag in ['on', 'off'], 'not supported switch flag'
        data = self.axi4_bus.read_32bit_fix(MIXAD7768CYGDef.AD7768_CONFIG_REG, 1)[0]
        if flag == 'on':
            data = data | MIXAD7768CYGDef.AD7768_STREAM_SWITCH_MASK
        else:
            data = data & ~MIXAD7768CYGDef.AD7768_STREAM_SWITCH_MASK
        self.axi4_bus.write_32bit_fix(MIXAD7768CYGDef.AD7768_CONFIG_REG, [data])

    def get_stream(self):
        '''
        Get axi-stream data bus status.

        Return: string, ['on', 'off']

        Exmaples:
            mix_ad7768_cyg.get_stream()

        '''
        data = self.axi4_bus.read_32bit_fix(MIXAD7768CYGDef.AD7768_CONFIG_REG, 1)[0]
        if data & MIXAD7768CYGDef.AD7768_STREAM_SWITCH_MASK != 0:
            return 'on'
        else:
            return 'off'

    def start_lite(self, number):
        '''
        Start transfer data to fifo. Invalid when axi-lite data bus is busy or disabled.

        Args:
            number, int, 1~8192

        Examples:
            mix_ad7768_cyg.start_lite(5000)

        '''
        assert isinstance(number, int) and 0 < number and number <= MIXAD7768CYGDef.AD7768_MAX_DATA_NUMBER, \
            'invalid transporting number'
        self.axi4_bus.write_32bit_fix(MIXAD7768CYGDef.AD7768_LITE_DATA_NUMBER_REG, [number])

    def start_stream(self, logger_time):
        '''
        Start axi-stream transfer.

        Args:
            logger_time, float, 0~125(ms), step by 8ns.

        '''
        assert logger_time > 0 and logger_time <= MIXAD7768CYGDef.MAX_LOGGER_TIME, 'invalid time'
        reg = round(logger_time*125000)
        assert reg > 0, 'time is too short'
        if self.get_stream() == 'off':
            self.set_stream('on')
        if self.busy_stream():
            self.set_stream('off')
            self.set_stream('on')
        self.axi4_bus.write_32bit_fix(MIXAD7768CYGDef.AD7768_STREAM_DATA_TIME_REG, [reg])

    def busy_lite(self):
        '''
        Show if axi-lite data bus is busy.

        Return, bool, True means busy.

        Examples:
            mix_ad7768_cyg.busy_lite()

        '''
        data = self.axi4_bus.read_32bit_fix(MIXAD7768CYGDef.AD7768_STATUS_REG, 1)[0]
        if data & MIXAD7768CYGDef.AD7768_AXI_LITE_BUSY_MASK != 0:
            return True
        else:
            return False

    def busy_stream(self):
        '''
        Show if axi-stream data bus is busy.

        Return, bool, True means busy.

        Examples:
            mix_ad7768_cyg.busy_stream()

        '''
        data = self.axi4_bus.read_32bit_fix(MIXAD7768CYGDef.AD7768_STATUS_REG, 1)[0]
        if data & MIXAD7768CYGDef.AD7768_AXI_STREAM_BUSY_MASK != 0:
            return True
        else:
            return False

    def set_oneshot_frequency(self, freq):
        '''
        Set sampling frequency under oneshot mode.

        Args:
            freq, float, unit: Hz

        Examples:
            mix_ad7768_cyg.set_oneshot_frequency()

        '''
        assert 0 < freq, 'invalid one shot sampling frequence'
        period = round(MIXAD7768CYGDef.FPGA_WORK_FREQUENCE / freq)
        self.axi4_bus.write_32bit_fix(MIXAD7768CYGDef.AD7768_ONESHOT_PERIOD_REG, [period])

    def get_oneshot_frequency(self):
        '''
        Get sampling frequency under oneshot mode.

        Return: float, Hz

        Examples:
            mix_ad7768_cyg.get_oneshot_frequency()

        '''
        period = self.axi4_bus.read_32bit_fix(MIXAD7768CYGDef.AD7768_ONESHOT_PERIOD_REG, 1)[0]
        assert period != 0, 'frequency has not been set'
        freq = MIXAD7768CYGDef.FPGA_WORK_FREQUENCE / period
        return freq

    def measure(self, channel_list, number, timeout=0.5):
        '''
        Measure all 4 channels and automatically filter out not settled data.

        Args:
            number, int, per channel's data amount you wanted.
            timeout, float, default 0.5s.

        Return, dict. {0: [1000.0, 1001.0, 1002.0, 1001.0, ...], 1: [1000.0, ...], ...}, unit: mv.

        Example:
            mix_ad7768_cyg.measure(100)

        '''
        assert False not in [item in ["ch0","ch1","ch2","ch3"] for item in channel_list]
        assert timeout > 0, 'invalid timeout value'
        if self.get_lite() == 'off':
            self.set_lite('on')
        self.start_lite(number)
        measurements = dict()
        time_start = time.time()
        while time.time() - time_start < timeout:
            if self.busy_lite() is False:
                for channel_name in channel_list:
                    ch = int(channel_name[2:])
                    measurements[ch] = self.axi4_bus.read_32bit_fix(MIXAD7768CYGDef.AD7768_DATA_REG[ch], number)
                for channel_index, data_list in measurements.items():
                    data_list = self.filter_measurement(data_list)
                    if channel_index < self.channel_num/2:
                        ref = self.reference_voltate['ref1']
                    else:
                        ref = self.reference_voltate['ref2']
                    measurements[channel_index] = self.decode_measurement(
                        data_list, ref)
                return measurements
        self.set_lite('off')
        raise MIXAD7768CYGException('time out while measuring')

    def get_revision_id(self):
        '''
        Get AD7768's revision id. It must be 0x06. Used for test spi.

        Return, string, '0x6'

        Examples:
            mix_ad7768_cyg.get_revision_id()

        '''
        if self.get_control_mode() == 'spi':
            revision_id = self.spi_read(MIXAD7768CYGDef.REVISION_IDENTIFICATION_REG)
            return hex(revision_id)
        else:
            raise MIXAD7768CYGException('invalid operation under pin mode')