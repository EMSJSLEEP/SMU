from mix.driver.core.bus.axi4_lite_bus import AXI4LiteBus

class AD5522RegDef:
    PMU_REG_RD = 0x01 << 28

    PMU_MODE_SYSREG = 0x00
    PMU_MODE_GAINREG = 0x01 << 22
    PMU_MODE_OFFSETREG = 0x02 << 22
    PMU_MODE_DATAREG = 0x03 << 22
    PMU_MODE_ALARMREG = 0x03 << 22

    PMU_CH_0 = 0x01 << 24
    PMU_CH_1 = 0x01 << 25
    PMU_CH_2 = 0x01 << 26
    PMU_CH_3 = 0x01 << 27

    #--------PMU SYS REG--------#
    PMU_SYSREG_CL0 = 0x01 << 18
    PMU_SYSREG_CL1 = 0x01 << 19
    PMU_SYSREG_CL2 = 0x01 << 20
    PMU_SYSREG_CL3 = 0x01 << 21

    PMU_SYSREG_CPOLH0 = 0x01 << 14
    PMU_SYSREG_CPOLH1 = 0x01 << 15
    PMU_SYSREG_CPOLH2 = 0x01 << 16
    PMU_SYSREG_CPOLH3 = 0x01 << 17

    PMU_SYSREG_CPBIAS = 0x01 << 13

    PMU_SYSREG_DUTGND = 0x01 << 12
    PMU_SYSREG_GUARDALM = 0x01 << 11
    PMU_SYSREG_CLAMPALM = 0x01 << 10
    PMU_SYSREG_INT10K = 0x01 << 9
    PMU_SYSREG_GUARDEN = 0x01 << 8
    PMU_SYSREG_GAIN1 = 0x01 << 7
    PMU_SYSREG_GAIN0 = 0x01 << 6
    PMU_SYSREG_TMPEN = 0x01 << 5
    PMU_SYSREG_TMP1 = 0x01 << 4
    PMU_SYSREG_TMP0 = 0x01 << 3
    PMU_SYSREG_LATCH = 0x01 << 2

    #--------PMU self REG--------#
    PMU_PMUREG_CH_EN = 0x01 << 21
    PMU_PMUREG_CH_DIS = 0x00 << 21
    PMU_PMUREG_FVCI = 0x00 << 19
    PMU_PMUREG_FICV = 0x01 << 19
    PMU_PMUREG_HZV = 0x02 << 19
    PMU_PMUREG_HZI = 0x03 << 19
    PMU_PMUREG_C2 = 0x01 << 17
    PMU_PMUREG_C1 = 0x01 << 16
    PMU_PMUREG_C0 = 0x01 << 15
    PMU_PMUREG_MEAS_I = 0x00 << 13
    PMU_PMUREG_MEAS_V = 0x01 << 13
    PMU_PMUREG_MEAS_TEMP = 0x02 << 13
    PMU_PMUREG_MEAS_HZ = 0x03 << 13
    PMU_PMUREG_FIN = 0x01 << 12
    PMU_PMUREG_FIN_DIS = 0x00 << 12
    PMU_PMUREG_SF0 = 0x01 << 11
    PMU_PMUREG_SS0 = 0x01 << 10
    PMU_PMUREG_CL = 0x01 << 9
    PMU_PMUREG_CPOLH = 0x01 << 8
    PMU_PMUREG_COMPV = 0x01 << 7
    PMU_PMUREG_CLEAR = 0x01 << 6

    #--------PMU DAC REG--------#
    PMU_DACREG_ADDR_OFFSET = 0x00 << 16 | PMU_MODE_DATAREG
    PMU_DACREG_ADDR_FIN_5UA_M = 0x08 << 16 | PMU_MODE_GAINREG
    PMU_DACREG_ADDR_FIN_5UA_C = 0x08 << 16 | PMU_MODE_OFFSETREG
    PMU_DACREG_ADDR_FIN_5UA_X1 = 0x08 << 16 | PMU_MODE_DATAREG
    PMU_DACREG_ADDR_FIN_20UA_M = 0x09 << 16 | PMU_MODE_GAINREG
    PMU_DACREG_ADDR_FIN_20UA_C = 0x09 << 16 | PMU_MODE_OFFSETREG
    PMU_DACREG_ADDR_FIN_20UA_X1 = 0x09 << 16 | PMU_MODE_DATAREG
    PMU_DACREG_ADDR_FIN_200UA_M = 0x0A << 16 | PMU_MODE_GAINREG
    PMU_DACREG_ADDR_FIN_200UA_C = 0x0A << 16 | PMU_MODE_OFFSETREG
    PMU_DACREG_ADDR_FIN_200UA_X1 = 0x0A << 16 | PMU_MODE_DATAREG
    PMU_DACREG_ADDR_FIN_2MA_M = 0x0B << 16 | PMU_MODE_GAINREG
    PMU_DACREG_ADDR_FIN_2MA_C = 0x0B << 16 | PMU_MODE_OFFSETREG
    PMU_DACREG_ADDR_FIN_2MA_X1 = 0x0B << 16 | PMU_MODE_DATAREG
    PMU_DACREG_ADDR_FIN_EXTC_M = 0x0C << 16 | PMU_MODE_GAINREG
    PMU_DACREG_ADDR_FIN_EXTC_C = 0x0C << 16 | PMU_MODE_OFFSETREG
    PMU_DACREG_ADDR_FIN_EXTC_X1 = 0x0C << 16 | PMU_MODE_DATAREG
    PMU_DACREG_ADDR_FIN_VOL_M = 0x0D << 16 | PMU_MODE_GAINREG
    PMU_DACREG_ADDR_FIN_VOL_C = 0x0D << 16 | PMU_MODE_OFFSETREG
    PMU_DACREG_ADDR_FIN_VOL_X1 = 0x0D << 16 | PMU_MODE_DATAREG
    PMU_DACREG_ADDR_CLL_I_M = 0x14 << 16 | PMU_MODE_GAINREG
    PMU_DACREG_ADDR_CLL_I_C = 0x14 << 16 | PMU_MODE_OFFSETREG
    PMU_DACREG_ADDR_CLL_I_X1 = 0x14 << 16 | PMU_MODE_DATAREG
    PMU_DACREG_ADDR_CLL_V_M = 0x15 << 16 | PMU_MODE_GAINREG
    PMU_DACREG_ADDR_CLL_V_C = 0x15 << 16 | PMU_MODE_OFFSETREG
    PMU_DACREG_ADDR_CLL_V_X1 = 0x15 << 16 | PMU_MODE_DATAREG
    PMU_DACREG_ADDR_CLH_I_M = 0x1C << 16 | PMU_MODE_GAINREG
    PMU_DACREG_ADDR_CLH_I_C = 0x1C << 16 | PMU_MODE_OFFSETREG
    PMU_DACREG_ADDR_CLH_I_X1 = 0x1C << 16 | PMU_MODE_DATAREG
    PMU_DACREG_ADDR_CLH_V_M = 0x1D << 16 | PMU_MODE_GAINREG
    PMU_DACREG_ADDR_CLH_V_C = 0x1D << 16 | PMU_MODE_OFFSETREG
    PMU_DACREG_ADDR_CLH_V_X1 = 0x1D << 16 | PMU_MODE_DATAREG
    PMU_DACREG_ADDR_CPL_5UA_M = 0x20 << 16 | PMU_MODE_GAINREG
    PMU_DACREG_ADDR_CPL_5UA_C = 0x20 << 16 | PMU_MODE_OFFSETREG
    PMU_DACREG_ADDR_CPL_5UA_X1 = 0x20 << 16 | PMU_MODE_DATAREG
    PMU_DACREG_ADDR_CPL_20UA_M = 0x21 << 16 | PMU_MODE_GAINREG
    PMU_DACREG_ADDR_CPL_20UA_C = 0x21 << 16 | PMU_MODE_OFFSETREG
    PMU_DACREG_ADDR_CPL_20UA_X1 = 0x21 << 16 | PMU_MODE_DATAREG
    PMU_DACREG_ADDR_CPL_200UA_M = 0x22 << 16 | PMU_MODE_GAINREG
    PMU_DACREG_ADDR_CPL_200UA_C = 0x22 << 16 | PMU_MODE_OFFSETREG
    PMU_DACREG_ADDR_CPL_200UA_X1 = 0x22 << 16 | PMU_MODE_DATAREG
    PMU_DACREG_ADDR_CPL_2MA_M = 0x23 << 16 | PMU_MODE_GAINREG
    PMU_DACREG_ADDR_CPL_2MA_C = 0x23 << 16 | PMU_MODE_OFFSETREG
    PMU_DACREG_ADDR_CPL_2MA_X1 = 0x23 << 16 | PMU_MODE_DATAREG
    PMU_DACREG_ADDR_CPL_EXTC_M = 0x24 << 16 | PMU_MODE_GAINREG
    PMU_DACREG_ADDR_CPL_EXTC_C = 0x24 << 16 | PMU_MODE_OFFSETREG
    PMU_DACREG_ADDR_CPL_EXTC_X1 = 0x24 << 16 | PMU_MODE_DATAREG
    PMU_DACREG_ADDR_CPL_VOL_M = 0x25 << 16 | PMU_MODE_GAINREG
    PMU_DACREG_ADDR_CPL_VOL_C = 0x25 << 16 | PMU_MODE_OFFSETREG
    PMU_DACREG_ADDR_CPL_VOL_X1 = 0x25 << 16 | PMU_MODE_DATAREG
    PMU_DACREG_ADDR_CPH_5UA_M = 0x28 << 16 | PMU_MODE_GAINREG
    PMU_DACREG_ADDR_CPH_5UA_C = 0x28 << 16 | PMU_MODE_OFFSETREG
    PMU_DACREG_ADDR_CPH_5UA_X1 = 0x28 << 16 | PMU_MODE_DATAREG
    PMU_DACREG_ADDR_CPH_20UA_M = 0x29 << 16 | PMU_MODE_GAINREG
    PMU_DACREG_ADDR_CPH_20UA_C = 0x29 << 16 | PMU_MODE_OFFSETREG
    PMU_DACREG_ADDR_CPH_20UA_X1 = 0x29 << 16 | PMU_MODE_DATAREG
    PMU_DACREG_ADDR_CPH_200UA_M = 0x2A << 16 | PMU_MODE_GAINREG
    PMU_DACREG_ADDR_CPH_200UA_C = 0x2A << 16 | PMU_MODE_OFFSETREG
    PMU_DACREG_ADDR_CPH_200UA_X1 = 0x2A << 16 | PMU_MODE_DATAREG
    PMU_DACREG_ADDR_CPH_2MA_M = 0x2B << 16 | PMU_MODE_GAINREG
    PMU_DACREG_ADDR_CPH_2MA_C = 0x2B << 16 | PMU_MODE_OFFSETREG
    PMU_DACREG_ADDR_CPH_2MA_X1 = 0x2B << 16 | PMU_MODE_DATAREG
    PMU_DACREG_ADDR_CPH_EXTC_M = 0x2C << 16 | PMU_MODE_GAINREG
    PMU_DACREG_ADDR_CPH_EXTC_C = 0x2C << 16 | PMU_MODE_OFFSETREG
    PMU_DACREG_ADDR_CPH_EXTC_X1 = 0x2C << 16 | PMU_MODE_DATAREG
    PMU_DACREG_ADDR_CPH_VOL_M = 0x2D << 16 | PMU_MODE_GAINREG
    PMU_DACREG_ADDR_CPH_VOL_C = 0x2D << 16 | PMU_MODE_OFFSETREG
    PMU_DACREG_ADDR_CPH_VOL_X1 = 0x2D << 16 | PMU_MODE_DATAREG

    AD5522_DAC_REG_M = 0x00
    AD5522_DAC_REG_C = 0x01
    AD5522_DAC_REG_X1 = 0x02

    PMU_DAC_SCALEID_5UA = 0x00
    PMU_DAC_SCALEID_20UA = 0x01
    PMU_DAC_SCALEID_200UA = 0x02
    PMU_DAC_SCALEID_2MA = 0x03
    PMU_DAC_SCALEID_EXT = 0x04
    PMU_DAC_VOL = 0x05

    AD5522_STATE_IDLE = 0x01
    AD5522_STATE_FVMI = 0x02
    AD5522_STATE_FIMV = 0x04
    AD5522_STATE_CLL_ARM = 0x08
    AD5522_STATE_CLH_ARM = 0x10
    AD5522_STATE_CPL_ARM = 0x20
    AD5522_STATE_CPH_ARM = 0x40

    DAC_MODE_REG_X = {
    "FIN_5uA": PMU_DACREG_ADDR_FIN_5UA_X1,
    "FIN_20uA": PMU_DACREG_ADDR_FIN_20UA_X1,
    "FIN_200uA": PMU_DACREG_ADDR_FIN_200UA_X1,
    "FIN_2mA": PMU_DACREG_ADDR_FIN_2MA_X1,
    "FIN_external": PMU_DACREG_ADDR_FIN_EXTC_X1,
    "FIN_Vol": PMU_DACREG_ADDR_FIN_VOL_X1,
    "CLL_Curr": PMU_DACREG_ADDR_CLL_I_X1,
    "CLH_Curr": PMU_DACREG_ADDR_CLH_I_X1,
    "CLL_Vol": PMU_DACREG_ADDR_CLL_V_X1,
    "CLH_Vol": PMU_DACREG_ADDR_CLH_V_X1
    }

    DAC_MODE_REG_M = {
    "FIN_5uA": PMU_DACREG_ADDR_FIN_5UA_M,
    "FIN_20uA": PMU_DACREG_ADDR_FIN_20UA_M,
    "FIN_200uA": PMU_DACREG_ADDR_FIN_200UA_M,
    "FIN_2mA": PMU_DACREG_ADDR_FIN_2MA_M,
    "FIN_external": PMU_DACREG_ADDR_FIN_EXTC_M,
    "FIN_Vol": PMU_DACREG_ADDR_FIN_VOL_M,
    "CLL_Curr": PMU_DACREG_ADDR_CLL_I_M,
    "CLH_Curr": PMU_DACREG_ADDR_CLH_I_M,
    "CLL_Vol": PMU_DACREG_ADDR_CLL_V_M,
    "CLH_Vol": PMU_DACREG_ADDR_CLH_V_M
    }

    DAC_MODE_REG_C = {
    "FIN_5uA": PMU_DACREG_ADDR_FIN_5UA_C,
    "FIN_20uA": PMU_DACREG_ADDR_FIN_20UA_C,
    "FIN_200uA": PMU_DACREG_ADDR_FIN_200UA_C,
    "FIN_2mA": PMU_DACREG_ADDR_FIN_2MA_C,
    "FIN_external": PMU_DACREG_ADDR_FIN_EXTC_C,
    "FIN_Vol": PMU_DACREG_ADDR_FIN_VOL_C,
    "CLL_Curr": PMU_DACREG_ADDR_CLL_I_C,
    "CLH_Curr": PMU_DACREG_ADDR_CLH_I_C,
    "CLL_Vol": PMU_DACREG_ADDR_CLL_V_C,
    "CLH_Vol": PMU_DACREG_ADDR_CLH_V_C
    }

    CURREMT_RANGE = {
        "5uA": PMU_DAC_SCALEID_5UA,
        "20uA": PMU_DAC_SCALEID_20UA,
        "200uA": PMU_DAC_SCALEID_200UA,
        "2mA": PMU_DAC_SCALEID_2MA,
        "external": PMU_DAC_SCALEID_EXT
    }


class AD5522(object):
    rpc_public_api = [
        'read_pmu_reg_back',
        'read_dac_reg_x_back',
        'read_dac_reg_m_back',
        'read_dac_reg_c_back',
        'read_sys_reg_back',
        'set_system_control',
        'set_pmu_control',
        'set_clamp_vol',
        'set_clamp_curr',
        'set_output_vol',
        'set_2_MV',
        'set_2_MI',
        'set_2_FV',
        'set_2_FI',
        'set_dac_offset_value',
        'set_current_range',
        'enable_pmu',
        'disable_pmu',
        'set_dac_c_reg',
        'sequnece_disable_pmu',
        'sequence_enable_pmu'
    ]

    def __init__(self, spi, vref=5000):
        self.spi_ad5522 = spi
        self.pmu_reg = [0, 0, 0, 0]
        self.range_I = AD5522RegDef.PMU_DAC_SCALEID_2MA

    def read_alarm_reg_back(self):
        '''
        Read pmu alarm reg back.

        Args:
            None.
        Return:
            reg_data, int.
        '''
        cmd = 0
        cmd |= AD5522RegDef.PMU_REG_RD | AD5522RegDef.PMU_MODE_ALARMREG
        reg_data = self.spi_ad5522.ad5522_spi_read(cmd)
        return reg_data

    def read_pmu_reg_back(self, channel):
        '''
        Read pmu register back.

        Args:
            channel, int, select in [0x01 << 24, 0x01 << 25, 0x01 << 26, 0x01 << 27]
        Return:
            reg_value, int
        '''
        assert channel in [
            AD5522RegDef.PMU_CH_0, AD5522RegDef.PMU_CH_1,
            AD5522RegDef.PMU_CH_2, AD5522RegDef.PMU_CH_3
            ]
        cmd = 0
        for i in range(4):
            if (channel == (AD5522RegDef.PMU_CH_0 << i)):
                cmd |= (AD5522RegDef.PMU_REG_RD | channel)
                value = self.spi_ad5522.ad5522_spi_read(cmd)
        return value

    def read_dac_reg_x_back(self, channel, dac_mode):
        '''
        Read dac reg of x data.

        Args:
            channel: int, select in [0x01 << 24, 0x01 << 25, 0x01 << 26, 0x01 << 27]
            dac_mode: int, select in ["FIN_5uA", "FIN_20uA", "FIN_200uA", "FIN_2mA", 
                                    "FIN_external", "FIN_Vol", "CLL_Curr", "CLL_Vol",
                                    "CLH_Curr", "CLH_Vol"]

        Return:
            int, dac_code
        '''
        assert channel in [
            AD5522RegDef.PMU_CH_0, AD5522RegDef.PMU_CH_1,
            AD5522RegDef.PMU_CH_2, AD5522RegDef.PMU_CH_3
        ]
        assert dac_mode in AD5522RegDef.DAC_MODE_REG_X.keys()
        cmd = 0
        for i in range(4):
            if (channel == (AD5522RegDef.PMU_CH_0 << i)):
                cmd |= (AD5522RegDef.DAC_MODE_REG_X[dac_mode] | channel | AD5522RegDef.PMU_REG_RD)
                value = self.spi_ad5522.ad5522_spi_read(cmd) & 0xffff
        return value

    def read_dac_reg_m_back(self, channel, dac_mode):
        '''
        Read dac reg of M data.

        Args:
            channel: int, select in [0x01 << 24, 0x01 << 25, 0x01 << 26, 0x01 << 27]
            dac_mode: int, select in ["FIN_5uA", "FIN_20uA", "FIN_200uA", "FIN_2mA", 
                                    "FIN_external", "FIN_Vol", "CLL_Curr", "CLL_Vol",
                                    "CLH_Curr", "CLH_Vol"]

        Return:
            int, dac_code
        '''

        assert channel in [
            AD5522RegDef.PMU_CH_0, AD5522RegDef.PMU_CH_1,
            AD5522RegDef.PMU_CH_2, AD5522RegDef.PMU_CH_3
        ]
        assert dac_mode in AD5522RegDef.DAC_MODE_REG_M.keys()

        cmd = 0
        for i in range(4):
            if (channel == (AD5522RegDef.PMU_CH_0 << i)):
                cmd |= (AD5522RegDef.DAC_MODE_REG_M[dac_mode] | channel
                        | AD5522RegDef.PMU_REG_RD)
                value = self.spi_ad5522.ad5522_spi_read(cmd)
        return value

    def read_dac_reg_c_back(self, channel, dac_mode):
        '''
        Read dac reg of C data.

        Args:
            channel: int, select in [0x01 << 24, 0x01 << 25, 0x01 << 26, 0x01 << 27]
            dac_mode: int, select in ["FIN_5uA", "FIN_20uA", "FIN_200uA", "FIN_2mA", 
                                    "FIN_external", "FIN_Vol", "CLL_Curr", "CLL_Vol",
                                    "CLH_Curr", "CLH_Vol"]

        Return:
            int, dac_code
        '''

        assert channel in [
            AD5522RegDef.PMU_CH_0, AD5522RegDef.PMU_CH_1,
            AD5522RegDef.PMU_CH_2, AD5522RegDef.PMU_CH_3
        ]
        assert dac_mode in AD5522RegDef.DAC_MODE_REG_C.keys()

        cmd = 0
        for i in range(4):
            if (channel == (AD5522RegDef.PMU_CH_0 << i)):
                cmd |= (AD5522RegDef.DAC_MODE_REG_C[dac_mode] | channel
                        | AD5522RegDef.PMU_REG_RD)
                value = self.spi_ad5522.ad5522_spi_read(cmd) & 0xffff
        return value

    def read_sys_reg_back(self):
        '''
        Read system register value back.
        
        Args:
            None.
        Return:
            int, value.
        '''
        cmd = 1 << 28
        value = self.spi_ad5522.ad5522_spi_read(cmd)
        return value

    def set_system_control(self, cmd):
        '''
        Write cmd to system register.

        Args:
            cmd, int.

        Return:
            str, "done"
        '''
        _write = (AD5522RegDef.PMU_MODE_SYSREG << 22) | cmd
        self.spi_ad5522.ad5522_spi_write(_write)
        return 'done'

    def set_pmu_control(self, channel, cmd):
        '''
        Write cmd to pmu register.

        Args:
            channel: int, select in [0x01 << 24, 0x01 << 25, 0x01 << 26, 0x01 << 27]
            cmd, int.

        Return:
            str, "done"
        '''
        self.spi_ad5522.ad5522_spi_write(channel | cmd)
        for i in range(4):
            if (channel == (AD5522RegDef.PMU_CH_0 << i)):
                self.pmu_reg[i] = cmd
        return 'done'

    def set_clamp_vol(self, channel, vol_low, vol_high):
        '''
        set clamp_voltage.

        Args:
            channel: int, select in [0x01 << 24, 0x01 << 25, 0x01 << 26, 0x01 << 27]
            vol_low, int, low limit vol.
            vol_high, int, high limit vol.

        Return:
            str, "done"
        '''
        assert channel in [
            AD5522RegDef.PMU_CH_0, AD5522RegDef.PMU_CH_1,
            AD5522RegDef.PMU_CH_2, AD5522RegDef.PMU_CH_3
        ]

        vol_low = 0 if vol_low < 0 else vol_low
        vol_low = 65535 if vol_low > 65535 else vol_low
        vol_high = 0 if vol_high < 0 else vol_high
        vol_high = 65535 if vol_high > 65535 else vol_high

        self.spi_ad5522.ad5522_spi_write(
            channel | vol_low | AD5522RegDef.PMU_DACREG_ADDR_CLL_V_X1)
        self.spi_ad5522.ad5522_spi_write(
            channel | vol_high | AD5522RegDef.PMU_DACREG_ADDR_CLH_V_X1)

        for i in range(4):
            if (channel == (AD5522RegDef.PMU_CH_0 << i)):
                cmd = self.pmu_reg[i]
                cmd &= ~(AD5522RegDef.PMU_CH_0 | AD5522RegDef.PMU_CH_1
                         | AD5522RegDef.PMU_CH_2 | AD5522RegDef.PMU_CH_3)
                cmd |= AD5522RegDef.PMU_PMUREG_CL
                self.set_pmu_control(channel, cmd)

        return 'done'

    def set_clamp_curr(self, channel, curr_low, curr_high):
        '''
        set clamp current value.

        Args:
            channel: int, select in [0x01 << 24, 0x01 << 25, 0x01 << 26, 0x01 << 27]
            clamp_low_curr:  int
            clamp_high_curr: int
        Returns:
            str, "done"
        '''
        assert channel in [
            AD5522RegDef.PMU_CH_0, AD5522RegDef.PMU_CH_1,
            AD5522RegDef.PMU_CH_2, AD5522RegDef.PMU_CH_3
        ]
        curr_low = 0 if curr_low < 0 else curr_low
        curr_low = 65535 if curr_low > 65535 else curr_low
        curr_high = 0 if curr_high < 0 else curr_high
        curr_high = 65535 if curr_high > 65535 else curr_high
        self.spi_ad5522.ad5522_spi_write(
            channel | curr_low | AD5522RegDef.PMU_DACREG_ADDR_CLL_I_X1)
        self.spi_ad5522.ad5522_spi_write(
            channel | curr_high | AD5522RegDef.PMU_DACREG_ADDR_CLH_I_X1)

        for i in range(4):
            if (channel == (AD5522RegDef.PMU_CH_0 << i)):
                cmd = self.pmu_reg[i]
                cmd &= ~(AD5522RegDef.PMU_CH_0 | AD5522RegDef.PMU_CH_1
                         | AD5522RegDef.PMU_CH_2 | AD5522RegDef.PMU_CH_3)
                cmd |= AD5522RegDef.PMU_PMUREG_CL
                self.set_pmu_control(channel, cmd)

        return 'done'

    def set_dac_c_reg(self, channel, c_reg, dac_code):
        assert channel in [
            AD5522RegDef.PMU_CH_0, AD5522RegDef.PMU_CH_1,
            AD5522RegDef.PMU_CH_2, AD5522RegDef.PMU_CH_3
        ]
        assert c_reg in AD5522RegDef.DAC_MODE_REG_C.keys()
       
        dac_code = 0 if dac_code < 0 else dac_code
        dac_code = 65535 if dac_code > 65535 else dac_code
        self.spi_ad5522.ad5522_spi_write(
            channel | dac_code |  AD5522RegDef.DAC_MODE_REG_C[c_reg])

        return 'done'
    
    def set_output_vol(self, channel, dac_code):
        '''
        set voltage value, 0 ~ 18000 mV.

        Args:
            channel: int, select in [0x01 << 24, 0x01 << 25, 0x01 << 26, 0x01 << 27]
            vol:  int, 0 ~ 18000 mV, step 10mV
        Returns:
            str, "done"
        '''
        assert channel in [
            AD5522RegDef.PMU_CH_0, AD5522RegDef.PMU_CH_1,
            AD5522RegDef.PMU_CH_2, AD5522RegDef.PMU_CH_3
        ]
        dac_code = 0 if dac_code < 0 else dac_code
        dac_code = 65535 if dac_code > 65535 else dac_code
        self.spi_ad5522.ad5522_spi_write(
            channel | dac_code | AD5522RegDef.PMU_DACREG_ADDR_FIN_VOL_X1)

        return 'done'

    def set_output_curr(self, channel, dac_code):
        '''
        set current value, 0 ~ 150 mA, step is 1mA.

        Args:
            channel: int, select in [0x01 << 24, 0x01 << 25, 0x01 << 26, 0x01 << 27]
            curr:  int, 0 ~ 150 mA, step 1mA
        Returns:
            str, "done"

        '''
        reg_data = self.read_pmu_reg_back(channel)
        curr_range = (reg_data >> 15) & 0x07
        I_range_base = 0x08
        I_range_base = ((I_range_base + curr_range) << 16) | AD5522RegDef.PMU_MODE_DATAREG
        dac_code = 0 if dac_code < 0 else dac_code
        dac_code = 65535 if dac_code > 65535 else dac_code
        self.spi_ad5522.ad5522_spi_write(channel | I_range_base | dac_code)

        return 'done'

    def sequence_set_output_curr(self, channel, dac_code, continue_time):
        '''
        set current value, 0 ~ 150 mA, step is 1mA.

        Args:
            channel: int, select in [0x01 << 24, 0x01 << 25, 0x01 << 26, 0x01 << 27]
            curr:  int, 0 ~ 150 mA, step 1mA
        Returns:
            str, "done"

        '''
        reg_data = self.read_pmu_reg_back(channel)
        curr_range = (reg_data >> 15) & 0x07
        I_range_base = 0x08
        I_range_base = ((I_range_base + curr_range) << 16) | AD5522RegDef.PMU_MODE_DATAREG
        dac_code = 0 if dac_code < 0 else dac_code
        dac_code = 65535 if dac_code > 65535 else dac_code
        self.spi_ad5522.write_cmd_list(channel | I_range_base | dac_code, 0, continue_time)

        return 'done'

    def set_2_MV(self, channel_list):
        '''
        set ic to measure voltage mode.

        Args:
            channel_list: list, [0x01 << 24, 0x01 << 25, 0x01 << 26, 0x01 << 27]
        Return:
            str, "done"
        '''
        if len(channel_list) == 1:
            channel_bit = 0
            channel_bit = channel_list[0]
            _temp = channel_bit >> 24
            _pos = 0 if _temp == 1 else _temp.bit_length() - 1
            cmd = self.pmu_reg[_pos] & ~0x6000
            cmd |= channel_bit | AD5522RegDef.PMU_PMUREG_MEAS_V
            self.set_pmu_control(channel_bit, cmd)
            self.pmu_reg[_pos] = cmd
        else:
            channel_bit = 0
            for bit in channel_list:
                _temp = bit >> 24
                _pos = 0 if _temp == 1 else _temp.bit_length() - 1
                channel_bit |= bit
                cmd = self.pmu_reg[_pos] & ~0x6000
                cmd |= AD5522RegDef.PMU_PMUREG_MEAS_V
                self.pmu_reg[_pos] = cmd
            self.set_pmu_control(channel_bit, cmd)

        return "done"

    def set_2_MI(self, channel_list):
        '''
        set ic to measure current mode.

        Args:
            channel_list: list, [0x01 << 24, 0x01 << 25, 0x01 << 26, 0x01 << 27]
        Return:
            str, "done"
        '''
        if len(channel_list) == 1:
            channel_bit = 0
            channel_bit = channel_list[0]
            _temp = channel_bit >> 24
            _pos = 0 if _temp == 1 else _temp.bit_length() - 1
            cmd = self.pmu_reg[_pos] & ~0x6000
            cmd |= AD5522RegDef.PMU_PMUREG_MEAS_I
            self.set_pmu_control(channel_bit, cmd)
            self.pmu_reg[_pos] = cmd
        else:
            channel_bit = 0
            cmd = 0
            for bit in channel_list:
                _temp = bit >> 24
                _pos = 0 if _temp == 1 else _temp.bit_length() - 1
                channel_bit |= bit
                cmd = self.pmu_reg[_pos] & ~0x6000
                cmd |= AD5522RegDef.PMU_PMUREG_MEAS_I 
                self.pmu_reg[_pos] = cmd
            self.set_pmu_control(channel_bit, cmd)

        return "done"

    def set_2_FV(self, channel_list):
        '''
        set ic to force voltage.

        Args:
            channel_list: list, [0x01 << 24, 0x01 << 25, 0x01 << 26, 0x01 << 27]
        Return:
            str, "done"
        '''
        if len(channel_list) == 1:
            channel_bit = 0
            channel_bit |= channel_list[0]
            _temp = channel_bit >> 24
            _pos = 0 if _temp == 1 else _temp.bit_length() - 1
            cmd = self.pmu_reg[_pos] & ~0x180000
            cmd |= AD5522RegDef.PMU_PMUREG_FVCI
            self.set_pmu_control(channel_bit, cmd)
            self.pmu_reg[_pos] = cmd
        else:
            channel_bit = 0
            cmd = 0
            for bit in channel_list:
                _temp = bit >> 24
                _pos = 0 if _temp == 1 else _temp.bit_length() - 1
                channel_bit |= bit
                cmd = self.pmu_reg[_pos] & ~0x180000
                cmd |= AD5522RegDef.PMU_PMUREG_FVCI
                self.pmu_reg[_pos] = cmd
            self.set_pmu_control(channel_bit, cmd)

        return "done"

    def set_2_FI(self, channel_list):
        '''
        set ic to force current.

        Args:
            channel_list: list, [0x01 << 24, 0x01 << 25, 0x01 << 26, 0x01 << 27]
        Return:
            str, "done"
        '''
        if len(channel_list) == 1:
            channel_bit = 0
            channel_bit = channel_list[0]
            _temp = channel_bit >> 24
            _pos = 0 if _temp == 1 else _temp.bit_length() - 1
            cmd = self.pmu_reg[_pos] & ~0x180000
            cmd |= AD5522RegDef.PMU_PMUREG_FICV
            self.set_pmu_control(channel_bit, cmd)
            self.pmu_reg[_pos] = cmd
        else:
            channel_bit = 0
            cmd = 0
            for bit in channel_list:
                _temp = bit >> 24
                _pos = 0 if _temp == 1 else _temp.bit_length() - 1
                channel_bit |= bit
                cmd = self.pmu_reg[_pos] & ~0x180000
                cmd |= AD5522RegDef.PMU_PMUREG_FICV
                self.pmu_reg[_pos] = cmd
            self.set_pmu_control(channel_bit, cmd)

        return 'done'

    def set_dac_offset_value(self, dac_offset):
        '''
        set ic offset dac value.

        Args:
            dac_offset: int, select in [0, 0x8000, 0xA492, 0xEDb7]
                             0: 0 ~ 22.5 V
                             0x8000: -8.75 ~ 13.75V
                             0xA492: -11.25 ~ 11.25V
                             0xEDb7: -16.25 ~ 6.25V
        Return:
            str, "done"
        '''
        for ch in [0, 1, 2, 3]:
            cmd = AD5522RegDef.PMU_CH_0 << ch | AD5522RegDef.PMU_DACREG_ADDR_OFFSET | dac_offset
            self.spi_ad5522.ad5522_spi_write(cmd)

        return "done"

    def set_current_range(self, channel_list, I_range):
        '''
        set multi pmu's output current range

        Args:
            channel_list: list, [0x01 << 24, 0x01 << 25, 0x01 << 26, 0x01 << 27]
            I_range:  int, [0, 1, 2, 3, 4]
        Returns:
            str, "done"

        '''
        assert I_range in [
            AD5522RegDef.PMU_DAC_SCALEID_5UA,
            AD5522RegDef.PMU_DAC_SCALEID_20UA,
            AD5522RegDef.PMU_DAC_SCALEID_200UA,
            AD5522RegDef.PMU_DAC_SCALEID_2MA, 
            AD5522RegDef.PMU_DAC_SCALEID_EXT
        ]
        if len(channel_list) == 1:
            channel_bit = 0
            channel_bit = channel_list[0]
            _temp = channel_bit >> 24
            _pos = 0 if _temp == 1 else _temp.bit_length() - 1
            cmd = self.pmu_reg[_pos] & ~0x38000
            cmd |= I_range << 15
            self.set_pmu_control(channel_bit, cmd)
            self.pmu_reg[_pos] = cmd
        else:
            channel_bit = 0
            cmd = 0
            for bit in channel_list:
                _temp = bit >> 24
                _pos = 0 if _temp == 1 else _temp.bit_length() - 1
                channel_bit |= bit
                cmd = self.pmu_reg[_pos] & ~0x38000
                cmd |= I_range << 15
                self.pmu_reg[_pos] = cmd
            self.set_pmu_control(channel_bit, cmd)

        return 'done'

    def enable_pmu(self, channel_list):
        '''
        enable pmu channel.

        Args:
            channel_list: list, [0x01 << 24, 0x01 << 25, 0x01 << 26, 0x01 << 27]
           
        Returns:
            str, "done"
        '''
        if len(channel_list) == 1:
            channel_bit = 0
            channel_bit = channel_list[0]
            _temp = channel_bit >> 24
            _pos = 0 if _temp == 1 else _temp.bit_length() - 1
            cmd = self.pmu_reg[_pos] & ~0x201000
            cmd |= AD5522RegDef.PMU_PMUREG_CH_EN | AD5522RegDef.PMU_PMUREG_FIN
            self.set_pmu_control(channel_bit, cmd)
            self.pmu_reg[_pos] = cmd
        else:
            channel_bit = 0
            cmd = 0
            for bit in channel_list:
                _temp = bit >> 24
                _pos = 0 if _temp == 1 else _temp.bit_length() - 1
                channel_bit |= bit
                cmd = self.pmu_reg[_pos] & ~0x201000
                cmd |= AD5522RegDef.PMU_PMUREG_CH_EN | AD5522RegDef.PMU_PMUREG_FIN
                self.pmu_reg[_pos] = cmd
            self.set_pmu_control(channel_bit, cmd)
        return "done"

    def sequence_enable_pmu(self, channel, channel_change_time):
        '''
        enable pmu channel.

        Args:
            channel_list: list, [0x01 << 24, 0x01 << 25, 0x01 << 26, 0x01 << 27]
           
        Returns:
            str, "done"
        '''
        _temp = channel >> 24
        _pos = 0 if _temp == 1 else _temp.bit_length() - 1
        cmd = self.pmu_reg[_pos] & ~0x201000
        cmd |= AD5522RegDef.PMU_PMUREG_CH_EN | AD5522RegDef.PMU_PMUREG_FIN
        self.spi_ad5522.write_cmd_list(channel | cmd, 1, channel_change_time)
        self.pmu_reg[_pos] = cmd
        return "done"

    def disable_pmu(self, channel_list):
        '''
        disable pmu channel.

        Args:
            channel_list: list, [0x01 << 24, 0x01 << 25, 0x01 << 26, 0x01 << 27]
           
        Returns:
            str, "done"
        '''
        if len(channel_list) == 1:
            channel_bit = 0
            channel_bit = channel_list[0]
            _temp = channel_bit >> 24
            _pos = 0 if _temp == 1 else _temp.bit_length() - 1
            cmd = self.pmu_reg[_pos] & ~0x1000
            self.set_pmu_control(channel_bit, cmd)
            self.pmu_reg[_pos] = cmd
        else:
            channel_bit = 0
            cmd = 0
            for bit in channel_list:
                _temp = bit >> 24
                _pos = 0 if _temp == 1 else _temp.bit_length() - 1
                channel_bit |= bit
                cmd = self.pmu_reg[_pos] & ~0x1000
                self.pmu_reg[_pos] = cmd
            self.set_pmu_control(channel_bit, cmd)
        return 'done'
    
    def sequnece_disable_pmu(self, channel, channel_change_time):
        '''
        disable pmu channel.

        Args:
            channel_list: list, [0x01 << 24, 0x01 << 25, 0x01 << 26, 0x01 << 27]
           
        Returns:
            str, "done"
        '''
        _temp = channel >> 24
        _pos = 0 if _temp == 1 else _temp.bit_length() - 1
        cmd = self.pmu_reg[_pos] & ~0x1000
        self.spi_ad5522.write_cmd_list(channel | cmd, 1, channel_change_time)
        self.pmu_reg[_pos] = cmd
        return 'done'        