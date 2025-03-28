from mix.driver.core.ic.cat24cxx import CAT24C64, CAT24C32
from mix.driver.cyg.common.ic.ad5522 import AD5522, AD5522RegDef
from mix.driver.cyg.common.ic.mcp4725 import MCP4725
from mix.driver.cyg.common.ipcore.mix_ad4134_cyg import MIXAD4134CYG
from mix.driver.core.bus.axi4_lite_bus import AXI4LiteBus
from mix.driver.cyg.common.module.cyg_module_driver import CYGModuleDriver, CalCell
from mix.driver.core.ic.cat9555 import CAT9555
from mix.rpc.services.streamservice import StreamServiceBuffered, StreamFilter
from mix.driver.cyg.common.ipcore.mix_smu_lite_cyg import MIX_SMU_Lite_CYG
import struct
import time

__version__ = '0.1'

class CYGHERMESDef:
    LOW_LIMIT_VOL=-1250
    DMA_MAX_READ_SIZE = 16
    DMA_TIME_OUT = 1
    BASE_CLOCK_TIME = 1.0 / 125e6
    EEPROM_DEV_ADDR = 0x20
    AMP_EEPROM_DEV_ADDR = 0x21
    P_DAC_POWER_ADDR = 0x60
    N_DAC_POWER_ADDR = 0x61
    IO_EXPAND_ADDR = 0x22
    AMP_IO_EXPAND_ADDR = 0x24
    CAT9555_RELAY_BANK = 0
    CAT9555_COMP_BANK = 1
    FV_MODE = 0x00
    FI_MODE = 0x01
    PMU_REG_DEFAULT = 1 << 6 | 0xF << 13 | 1 << 20
    OVERLOAD_COFFI = 1.125
    OUTPUT_RANGE_ADDRESS = 0x1ffc
    AD5522_CHANNEL = {
        "ch0": AD5522RegDef.PMU_CH_0,
        "ch1": AD5522RegDef.PMU_CH_1,
        "ch2": AD5522RegDef.PMU_CH_2,
        "ch3": AD5522RegDef.PMU_CH_3,
    }
    CAP_SPEC = {
        "default": 0x00,
        "lte_1nf": 0x01,
        "lte_10nf": 0x02,
        "lte_100nf": 0x03
    }
    CURREMT_RANGE = {
        "5uA": AD5522RegDef.PMU_DAC_SCALEID_5UA,
        "20uA": AD5522RegDef.PMU_DAC_SCALEID_20UA,
        "200uA": AD5522RegDef.PMU_DAC_SCALEID_200UA,
        "2mA": AD5522RegDef.PMU_DAC_SCALEID_2MA,
        "external": AD5522RegDef.PMU_DAC_SCALEID_EXT
    }
    RSENSE_I_RANGE = {
        "5uA": 200000,
        "20uA": 50000,
        "200uA": 5000,
        "2mA": 500,
        "external": 0.2 * 10,
        "external_150mA": 5
    }
    TEMP_RANGE = [130, 120, 110, 100]

    SYS_CONTROL_REG_DEF = [
        "Latched", "TMP0", "TMP1", "TMP_ENABLE", "GAIN0", "GAIN1", "Guard_EN",
        "INT10K", "CLAMP_ALM", "GUARD_ALM", "DUTGND/CH", "CPBIASEN", "CPOLH0",
        "CPOLH1", "CPOLH2", "CPOLH3", "CL0", "CL1", "CL2", "CL3", "MODE0",
        "MODE1", "PMU0", "PMU1", "PMU2", "PMU3", "RD/WR"
    ]
    PMU_CONTROL_REG_DEF = [
        "TMPALM", "LTMPALM", "Compare_V/I", "CPOLH", "CL", "SS0", "SF0", "FIN",
        "MEAS0", "MEAS1", "C0", "C1", "C2", "Reserved", "FORCE0", "FORCE1",
        "CH_EN", "MODE0", "MODE1", "PMU0", "PMU1", "PMU2", "PMU3", "RD/WR"
    ]
    PMU_ALARM_REG_DEF = [
        "C3", "LC3", "C2", "LC2", "C1", "LC1", "C0", "LC0", "G3", "LG3", "G2",
        "LG2", "G1", "LG1", "G0", "LG0", "TMPALM", "LTMPALM"
    ]
    DAC_CONTROL_REG_DEF = ["M(k)", "C(b)", "X1"]

    DAC_TYPE_IN_USER = [
        "FIN_5uA", "FIN_20uA", "FIN_200uA", "FIN_2mA", "FIN_external",
        "FIN_Vol", "CLL_Curr", "CLL_Vol", "CLH_Curr", "CLH_Vol"
    ]

    RANGE_LIMITS = {
        "5uA": 5 * OVERLOAD_COFFI,
        "20uA": 20 * OVERLOAD_COFFI,
        "200uA": 200 * OVERLOAD_COFFI,
        "2mA": 2 * OVERLOAD_COFFI,
        "external": 500 * OVERLOAD_COFFI
    }

    cyg_hercules_func_info = {
        'FI_CH0_5uA': {
            'cali_segment': [{
                'threshold': 5.625,
                'limit': (-5.625, 5.625)
            }]
        },
        'FI_CH0_20uA': {
            'cali_segment': [{
                'threshold': 22.5,
                'limit': (-22.5, 22.5)
            }]
        },
        'FI_CH0_200uA': {
            'cali_segment': [{
                'threshold': 225.0,
                'limit': (-225.0, 225.0)
            }]
        },
        'FI_CH0_2mA': {
            'cali_segment': [{
                'threshold': 2.25,
                'limit': (-2.25, 2.25)
            }]
        },
        'FI_CH0_external': {
            'cali_segment': [{
                'threshold':250,
                'limit': (-562.5, 250)
            },{
                'threshold':562.5,
                'limit': (250, 562.5)
            }]
        },
        'FI_CH1_5uA': {
            'cali_segment': [{
                'threshold': 5.625,
                'limit': (-5.625, 5.625)
            }]
        },
        'FI_CH1_20uA': {
            'cali_segment': [{
                'threshold': 22.5,
                'limit': (-22.5, 22.5)
            }]
        },
        'FI_CH1_200uA': {
            'cali_segment': [{
                'threshold': 225.0,
                'limit': (-225.0, 225.0)
            }]
        },
        'FI_CH1_2mA': {
            'cali_segment': [{
                'threshold': 2.25,
                'limit': (-2.25, 2.25)
            }]
        },
        'FI_CH1_external': {
            'cali_segment': [{
                'threshold':250,
                'limit': (-562.5, 250)
            },{
                'threshold':562.5,
                'limit': (250, 562.5)
            }]
        },
        'FI_CH2_5uA': {
            'cali_segment': [{
                'threshold': 5.625,
                'limit': (-5.625, 5.625)
            }]
        },
        'FI_CH2_20uA': {
            'cali_segment': [{
                'threshold': 22.5,
                'limit': (-22.5, 22.5)
            }]
        },
        'FI_CH2_200uA': {
            'cali_segment': [{
                'threshold': 225.0,
                'limit': (-225.0, 225.0)
            }]
        },
        'FI_CH2_2mA': {
            'cali_segment': [{
                'threshold': 2.25,
                'limit': (-2.25, 2.25)
            }]
        },
        'FI_CH2_external': {
            'cali_segment': [{
                'threshold':250,
                'limit': (-562.5, 250)
            },{
                'threshold':562.5,
                'limit': (250, 562.5)
            }]
        },
        'FI_CH3_5uA': {
            'cali_segment': [{
                'threshold': 5.625,
                'limit': (-5.625, 5.625)
            }]
        },
        'FI_CH3_20uA': {
            'cali_segment': [{
                'threshold': 22.5,
                'limit': (-22.5, 22.5)
            }]
        },
        'FI_CH3_200uA': {
            'cali_segment': [{
                'threshold': 225.0,
                'limit': (-225.0, 225.0)
            }]
        },
        'FI_CH3_2mA': {
            'cali_segment': [{
                'threshold': 2.25,
                'limit': (-2.25, 2.25)
            }]
        },
        'FI_CH3_external': {
            'cali_segment': [{
                'threshold':250,
                'limit': (-562.5, 250)
            },{
                'threshold':562.5,
                'limit': (250, 562.5)
            }]
        },
        'FV_CH0': {
            'cali_segment': [{
                'threshold': 0.0,
                'limit': (-10000, 0.0)
            },{
                'threshold': 10000.0,
                'limit': (0, 10000.0)
            }]
        },
        'FV_CH1': {
            'cali_segment': [{
                'threshold': 10000.0,
                'limit': (-10000, 10000.0)
            }]
        },
        'FV_CH2': {
            'cali_segment': [{
                'threshold': 10000.0,
                'limit': (-10000, 10000.0)
            }]
        },
        'FV_CH3': {
            'cali_segment': [{
                'threshold': 10000.0,
                'limit': (-10000, 10000.0)
            }]
        },
        'MV_CH0': {
            'cali_segment': [{
                'threshold': 0.0,
                'limit': (-10000, 0.0)
            },{
                'threshold': 10000.0,
                'limit': (0, 10000.0)
            }]
        },
        'MV_CH1': {
            'cali_segment': [{
                'threshold': 0.0,
                'limit': (-10000, 0.0)
            },{
                'threshold': 10000.0,
                'limit': (0, 10000.0)
            }]
        },
        'MV_CH2': {
            'cali_segment': [{
                'threshold': 0.0,
                'limit': (-10000, 0.0)
            },{
                'threshold': 10000.0,
                'limit': (0, 10000.0)
            }]
        },
        'MV_CH3': {
            'cali_segment': [{
                'threshold': 0.0,
                'limit': (-10000, 0.0)
            },{
                'threshold': 10000.0,
                'limit': (0, 10000.0)
            }]
        },
        'MI_CH0_5uA': {
            'cali_segment': [{
                'threshold': 5.625,
                'limit': (-5.625, 5.625)
            }]
        },
        'MI_CH0_20uA': {
            'cali_segment': [{
                'threshold': 22.5,
                'limit': (-22.5, 22.5)
            }]
        },
        'MI_CH0_200uA': {
            'cali_segment': [{
                'threshold': -4.0,
                'limit': (-225, -4.0)
            },{
                'threshold': 225.0,
                'limit': (-4.0, 225)
            }]
        },
        'MI_CH0_2mA': {
            'cali_segment': [{
                'threshold': 0.0,
                'limit': (-2.25, 0.0)
            },{
                'threshold': 2.25,
                'limit': (0.0, 2.25)
            }]
        },
        'MI_CH0_external': {
            'cali_segment': [{
                'threshold': -4.5,
                'limit': (-90.0, -4.5)
            },{
                'threshold': 90.0,
                'limit': (-4.5, 90.0)
            }]
        },
        'MI_CH1_5uA': {
            'cali_segment': [{
                'threshold': 5.625,
                'limit': (-5.625, 5.625)
            }]
        },
        'MI_CH1_20uA': {
            'cali_segment': [{
                'threshold': 22.5,
                'limit': (-22.5, 22.5)
            }]
        },
        'MI_CH1_200uA': {
            'cali_segment': [{
                'threshold': -4.0,
                'limit': (-225, -4.0)
            },{
                'threshold': 225.0,
                'limit': (-4.0, 225)
            }]
        },
        'MI_CH1_2mA': {
            'cali_segment': [{
                'threshold': 0.0,
                'limit': (-2.25, 0.0)
            },{
                'threshold': 2.25,
                'limit': (0.0, 2.25)
            }]
        },
        'MI_CH1_external': {
            'cali_segment': [{
                'threshold':120,
                'limit': (-562.5, 120)
            },{
                'threshold':320,
                'limit': (120, 320)
            },{
                'threshold':562.5,
                'limit': (320, 562.5)
            }]
        },
        'MI_CH2_5uA': {
            'cali_segment': [{
                'threshold': 5.625,
                'limit': (-5.625, 5.625)
            }]
        },
        'MI_CH2_20uA': {
            'cali_segment': [{
                'threshold': 22.5,
                'limit': (-22.5, 22.5)
            }]
        },
        'MI_CH2_200uA': {
            'cali_segment': [{
                'threshold': -4.0,
                'limit': (-225, -4.0)
            },{
                'threshold': 225.0,
                'limit': (-4.0, 225)
            }]
        },
        'MI_CH2_2mA': {
            'cali_segment': [{
                'threshold': 0.0,
                'limit': (-2.25, 0.0)
            },{
                'threshold': 2.25,
                'limit': (0.0, 2.25)
            }]
        },
        'MI_CH2_external': {
            'cali_segment': [{
                'threshold':120,
                'limit': (-562.5, 120)
            },{
                'threshold':320,
                'limit': (120, 320)
            },{
                'threshold':562.5,
                'limit': (320, 562.5)
            }]
        },
        'MI_CH3_5uA': {
            'cali_segment': [{
                'threshold': 5.625,
                'limit': (-5.625, 5.625)
            }]
        },
        'MI_CH3_20uA': {
            'cali_segment': [{
                'threshold': 22.5,
                'limit': (-22.5, 22.5)
            }]
        },
        'MI_CH3_200uA': {
            'cali_segment': [{
                'threshold': -4.0,
                'limit': (-225, -4.0)
            },{
                'threshold': 225.0,
                'limit': (-4.0, 225)
            }]
        },
        'MI_CH3_2mA': {
            'cali_segment': [{
                'threshold': 0.0,
                'limit': (-2.25, 0.0)
            },{
                'threshold': 2.25,
                'limit': (0.0, 2.25)
            }]
        },
        'MI_CH3_external': {
            'cali_segment': [{
                'threshold':120,
                'limit': (-562.5, 120)
            },{
                'threshold':320,
                'limit': (120, 320)
            },{
                'threshold':562.5,
                'limit': (320, 562.5)
            }]
        },
        'SINGLE_FI_CH0_5uA': {
            'cali_segment': [{
                'threshold': 5.625,
                'limit': (0, 5.625)
            }]
        },
        'SINGLE_FI_CH0_20uA': {
            'cali_segment': [{
                'threshold': 22.5,
                'limit': (0, 22.5)
            }]
        },
        'SINGLE_FI_CH0_200uA': {
            'cali_segment': [{
                'threshold': 225.0,
                'limit': (0.0, 225.0)
            }]
        },
        'SINGLE_FI_CH0_2mA': {
            'cali_segment': [{
                'threshold': 2.25,
                'limit': (0, 2.25)
            }]
        },
        'SINGLE_FI_CH0_external': {
            'cali_segment': [{
                'threshold':90,
                'limit': (0.0, 90)
            }]
        },
        'SINGLE_MI_CH0_5uA': {
            'cali_segment': [{
                'threshold': 5.625,
                'limit': (-1, 5.625)
            }]
        },
        'SINGLE_MI_CH0_20uA': {
            'cali_segment': [{
                'threshold': 22.5,
                'limit': (-2, 22.5)
            }]
        },
        'SINGLE_MI_CH0_200uA': {
            'cali_segment': [{
                'threshold': 225,
                'limit': (-10, 225)
            }]
        },
        'SINGLE_MI_CH0_2mA': {
            'cali_segment': [{
                'threshold': 2.25,
                'limit': (-0.2, 2.25)
            }]
        },
        'SINGLE_MI_CH0_external': {
            'cali_segment': [{
                'threshold': 562.5,
                'limit': (-30, 562.5)
            }]
        },
        'SINGLE_FI_CH1_5uA': {
            'cali_segment': [{
                'threshold': 5.625,
                'limit': (0, 5.625)
            }]
        },
        'SINGLE_FI_CH1_20uA': {
            'cali_segment': [{
                'threshold': 22.5,
                'limit': (0, 22.5)
            }]
        },
        'SINGLE_FI_CH1_200uA': {
            'cali_segment': [{
                'threshold': 225.0,
                'limit': (0.0, 225.0)
            }]
        },
        'SINGLE_FI_CH1_2mA': {
            'cali_segment': [{
                'threshold': 2.25,
                'limit': (0, 2.25)
            }]
        },
        'SINGLE_FI_CH1_external': {
            'cali_segment': [{
                'threshold':90,
                'limit': (0.0, 90)
            }]
        },
        'SINGLE_MI_CH1_5uA': {
            'cali_segment': [{
                'threshold': 5.625,
                'limit': (-1, 5.625)
            }]
        },
        'SINGLE_MI_CH1_20uA': {
            'cali_segment': [{
                'threshold': 22.5,
                'limit': (-2, 22.5)
            }]
        },
        'SINGLE_MI_CH1_200uA': {
            'cali_segment': [{
                'threshold': 225,
                'limit': (-10, 225)
            }]
        },
        'SINGLE_MI_CH1_2mA': {
            'cali_segment': [{
                'threshold': 2.25,
                'limit': (0, 2.25)
            }]
        },
        'SINGLE_MI_CH1_external': {
            'cali_segment': [{
                'threshold': 562.5,
                'limit': (-30, 562.5)
            }]
        },
        'SINGLE_FI_CH2_5uA': {
            'cali_segment': [{
                'threshold': 5.625,
                'limit': (0, 5.625)
            }]
        },
        'SINGLE_FI_CH2_20uA': {
            'cali_segment': [{
                'threshold': 22.5,
                'limit': (0, 22.5)
            }]
        },
        'SINGLE_FI_CH2_200uA': {
            'cali_segment': [{
                'threshold': 225.0,
                'limit': (0.0, 225.0)
            }]
        },
        'SINGLE_FI_CH2_2mA': {
            'cali_segment': [{
                'threshold': 2.25,
                'limit': (0, 2.25)
            }]
        },
        'SINGLE_FI_CH2_external': {
            'cali_segment': [{
                'threshold': 562.5,
                'limit': (-30, 562.5)
            }]
        },
        'SINGLE_MI_CH2_5uA': {
            'cali_segment': [{
                'threshold': 5.625,
                'limit': (-1, 5.625)
            }]
        },
        'SINGLE_MI_CH2_20uA': {
            'cali_segment': [{
                'threshold': 22.5,
                'limit': (-2, 22.5)
            }]
        },
        'SINGLE_MI_CH2_200uA': {
            'cali_segment': [{
                'threshold': 225,
                'limit': (-10, 225)
            }]
        },
        'SINGLE_MI_CH2_2mA': {
            'cali_segment': [{
                'threshold': 2.25,
                'limit': (-0.2, 2.25)
            }]
        },
        'SINGLE_MI_CH2_external': {
            'cali_segment': [{
                'threshold': 562.5,
                'limit': (-30, 562.5)
            }]
        },
        'SINGLE_FI_CH3_5uA': {
            'cali_segment': [{
                'threshold': 5.625,
                'limit': (0, 5.625)
            }]
        },
        'SINGLE_FI_CH3_20uA': {
            'cali_segment': [{
                'threshold': 22.5,
                'limit': (0, 22.5)
            }]
        },
        'SINGLE_FI_CH3_200uA': {
            'cali_segment': [{
                'threshold': 225.0,
                'limit': (0.0, 225.0)
            }]
        },
        'SINGLE_FI_CH3_2mA': {
            'cali_segment': [{
                'threshold': 2.25,
                'limit': (0, 2.25)
            }]
        },
        'SINGLE_FI_CH3_external': {
            'cali_segment': [{
                'threshold': 562.5,
                'limit': (-30, 562.5)
            }]
        },
        'SINGLE_MI_CH3_5uA': {
            'cali_segment': [{
                'threshold': 5.625,
                'limit': (-1, 5.625)
            }]
        },
        'SINGLE_MI_CH3_20uA': {
            'cali_segment': [{
                'threshold': 22.5,
                'limit': (0, 22.5)
            }]
        },
        'SINGLE_MI_CH3_200uA': {
            'cali_segment': [{
                'threshold': 225,
                'limit': (-10, 225)
            }]
        },
        'SINGLE_MI_CH3_2mA': {
            'cali_segment': [{
                'threshold': 2.25,
                'limit': (-0.2, 2.25)
            }]
        },
        'SINGLE_MI_CH3_external': {
            'cali_segment': [{
                'threshold': 562.5,
                'limit': (-30, 562.5)
            }]
        },
        'SINGLE_FV_CH0': {
            'cali_segment': [{
                'threshold': 22500.0,
                'limit': (0.0, 22500.0)
            }]
        },
        'SINGLE_FV_CH1': {
            'cali_segment': [{
                'threshold': 22500.0,
                'limit': (0.0, 22500.0)
            }]
        },
        'SINGLE_FV_CH2': {
            'cali_segment': [{
                'threshold': 22500.0,
                'limit': (0.0, 22500.0)
            }]
        },
        'SINGLE_FV_CH3': {
            'cali_segment': [{
                'threshold': 22500.0,
                'limit': (0.0, 22500.0)
            }]
        },
        'SINGLE_MV_CH0': {
            'cali_segment': [{
                'threshold': 22500.0,
                'limit': (0.0, 22500.0)
            }]
        },
        'SINGLE_MV_CH1': {
            'cali_segment': [{
                'threshold': 22500.0,
                'limit': (0.0, 22500.0)
            }]
        },
        'SINGLE_MV_CH2': {
            'cali_segment': [{
                'threshold': 22500.0,
                'limit': (0.0, 22500.0)
            }]
        },
        'SINGLE_MV_CH3': {
            'cali_segment': [{
                'threshold': 22500.0,
                'limit': (0.0, 22500.0)
            }]
        },
    }

cyg_hercules_range_table = {
    "FI_CH0_5uA" : 0,
    "FI_CH0_20uA" : 1,
    "FI_CH0_200uA": 2,
    "FI_CH0_2mA": 3,
    "FI_CH0_external": 4,
    "FI_CH1_5uA": 5,
    "FI_CH1_20uA": 6,
    "FI_CH1_200uA": 7,
    "FI_CH1_2mA": 8,
    "FI_CH1_external": 9,
    "FI_CH2_5uA": 10,
    "FI_CH2_20uA": 11,
    "FI_CH2_200uA": 12,
    "FI_CH2_2mA": 13,
    "FI_CH2_external": 14,
    "FI_CH3_5uA": 15,
    "FI_CH3_20uA": 16,
    "FI_CH3_200uA": 17,
    "FI_CH3_2mA": 18,
    "FI_CH3_external": 19,
    "FV_CH0": 20,
    "FV_CH1": 21,
    "FV_CH2": 22,
    "FV_CH3": 23,
    "MV_CH0": 24,
    "MV_CH1": 25,
    "MV_CH2": 26,
    "MV_CH3": 27,
    "MI_CH0_5uA": 28,
    "MI_CH0_20uA": 29,
    "MI_CH0_200uA": 30,
    "MI_CH0_2mA": 31,
    "MI_CH0_external": 32,
    "MI_CH1_5uA": 33,
    "MI_CH1_20uA": 34,
    "MI_CH1_200uA": 35,
    "MI_CH1_2mA": 36,
    "MI_CH1_external": 37,
    "MI_CH2_5uA": 38,
    "MI_CH2_20uA": 39,
    "MI_CH2_200uA": 40,
    "MI_CH2_2mA": 41,
    "MI_CH2_external": 42,
    "MI_CH3_5uA": 43,
    "MI_CH3_20uA": 44,
    "MI_CH3_200uA": 45,
    "MI_CH3_2mA": 46,
    "MI_CH3_external": 47}

class CYGHERMESException(Exception):
    def __init__(self, err_str):
        Exception.__init__(self, '%s.' % (err_str))


class CYG_HERMES(CYGModuleDriver, StreamServiceBuffered):
    rpc_public_api = [
        "reset", "get_driver_version", "power_on_init", "select_ad_spi",
        "set_single_comp_cap", "get_single_comp_cap", "set_single_pmu_mode",
        "get_single_pmu_mode", "set_single_pmu_vol", "get_single_pmu_vol",
        "set_single_pmu_curr_range", "get_single_pmu_curr_range",
        "enable_cmd_list", "set_single_pmu_curr", 'get_single_pmu_curr',
        'multi_pmu_enable', "control_loop", 'sequence_set_single_pmu_curr',
        'sequence_enable_single_pmu', 'get_dac_range', 'set_single_pmu_meas_mode',
        'clear_multi_pmu_alarm',  'sequence_disable_single_pmu','reset_ad4134',
        'get_single_pmu_meas_mode', 'single_pmu_enable', 'pre_thread_launch',
        'single_pmu_disable', 'set_sys_meas_out_gain', 'get_sys_meas_out_gain',
        "read_all_control_reg", 'set_sys_thermal_shutdown_temp', 'open_stream', 
        'get_sys_thermal_shutdown_temp', 'get_register_data', 'post_thread_shutdown',
        'get_multi_meas_result', 'set_register_data', 'get_single_meas_result',
        'set_multi_pmu_meas_mode', 'hercules_enable_relay', 'streaming_read',
        'control_FI_sequence', 'write_module_calibration', 'set_dac_range',
        'update_dac_and_pmu_reg', 'control_FV_sequence', 'get_alarm_status',
        'set_multi_pmu_curr_range', 'set_multi_pmu_mode', "set_dut_negative_volt",
        'multi_pmu_disable', "set_dut_positive_volt", 'sequence_set_single_pmu_vol',
        'reset_power_amp_board_relay', 'set_power_amp_board_relay', 'get_bottom_sn'
    ] + CYGModuleDriver.rpc_public_api + StreamServiceBuffered.streamservice_api

    def __init__(self, i2c_eeprom, i2c_dac_and_io, dma=None, ipcore=None):
        if i2c_eeprom and i2c_dac_and_io:
            self.eeprom = CAT24C64(i2c_eeprom,
                                   CYGHERMESDef.EEPROM_DEV_ADDR)
            self.eeprom_amp = CAT24C32(i2c_eeprom,
                                   CYGHERMESDef.AMP_EEPROM_DEV_ADDR)
            self.cat9555 = CAT9555(i2c_dac_and_io,
                                   CYGHERMESDef.IO_EXPAND_ADDR)
            self.cat9555_amp = CAT9555(i2c_dac_and_io,
                                   CYGHERMESDef.AMP_IO_EXPAND_ADDR)
            self.mcp4725_P = MCP4725(i2c_dac_and_io,
                                   CYGHERMESDef.P_DAC_POWER_ADDR)
            self.mcp4725_N = MCP4725(i2c_dac_and_io,
                                   CYGHERMESDef.N_DAC_POWER_ADDR)
        else:
            raise ValueError('No valid i2c bus input')
        if isinstance(ipcore, str):
            self.axi4_bus = AXI4LiteBus(ipcore, 65536)
        elif ipcore:
            self.axi4_bus = ipcore
        else:
            self.axi4_bus = AXI4LiteBus('/dev/MIX_SMU_Lite_CYG_v2_0', 65536)

        self.up0 = None
        self.stream = None
        self.dma = dma
        StreamServiceBuffered.__init__(self, CYGHERMESDef.DMA_MAX_READ_SIZE,
                                       CYGHERMESDef.DMA_TIME_OUT)
        self.select_range = ["2mA", "2mA", "2mA", "2mA"]
        self.ip_control = MIX_SMU_Lite_CYG(self.axi4_bus)
        self.ad5522 = AD5522(self.ip_control, 5000)
        self.ad4134 = MIXAD4134CYG(self.axi4_bus)
        volt_range = self.set_dac_range()
        self.low_limit = volt_range[0]
        self.high_limit = volt_range[1]
        
        if self.low_limit>=CYGHERMESDef.LOW_LIMIT_VOL:
            self.cal_table = cyg_hercules_range_table
        else:
            self.cal_table = cyg_hercules_range_table
        super(CYG_HERMES, self).__init__(self.eeprom,
                                    temperature_device=None,
                                    channel_table=self.cal_table)
        hermes_sn_in_bottom = self.eeprom_amp.read(17, 17)
        ascii_str = ''.join(chr(i) for i in hermes_sn_in_bottom)
        hermes_sn = self.read_serial_number()
        if hermes_sn != ascii_str:
            raise CYGHERMESException(f"Please check whether the baseplate and hercules are compatible")
        self.load_calibration()
        self.reset()
    
    def __del__(self):
        if hasattr(self, 'streams'):
            self.streams.clear()

    def get_driver_version(self):
        return __version__
    
    def get_bottom_sn(self):
        bottom_sn = self.eeprom_amp.read(0, 16)
        ascii_str = ''.join(chr(i) for i in bottom_sn)
        return ascii_str

    def reset(self):
        '''
        reset ad5522, ad4134, mcp4725 and cat9555.
        '''
        self.ip_control.reset()
        time.sleep(0.002)
        self.power_on_init()
        self.reset_power_amp_board_relay()
        for channel in ["ch0", "ch1", "ch2", "ch3"]:
            self.set_single_comp_cap(channel, "default")
            self.ad5522.set_pmu_control(
                CYGHERMESDef.AD5522_CHANNEL[channel],
                CYGHERMESDef.PMU_REG_DEFAULT)
            self.single_pmu_enable(channel)
            self.single_pmu_disable(channel)
        self.update_dac_and_pmu_reg()
        return "done"

    def select_ad_spi(self, choice):
        '''
        Select spi bus to control ad5522 or ad7768.
        Args:
            choice: int, select in [0, 1], "0" means choose ad7768.
        Return:
            "done"
        '''
        self.ip_control.enable_choose_spi(choice)
        return "done"

    def power_on_init(self):
        '''
        set sys reg to start default function.
            MEASOUTx=0.2
            measure_curr_gain=10
            DAC_OFFSET=0
            INT10K=enable=DUTGND_CH
        '''
        cmd_sys = 0
        gain0_bit = 0 << 6
        gain1_bit = 1 << 7
        INT_10K = 1 << 9
        DUTGND_CH = 1 << 12
        ALARM_BIT = 1 << 10 | 1 << 11
        LATCH_BIT = 1 << 2
        cmd_sys |= gain0_bit | gain1_bit | AD5522RegDef.PMU_SYSREG_TMPEN | INT_10K | DUTGND_CH | ALARM_BIT | LATCH_BIT
        self.cat9555.write_dir(CYGHERMESDef.CAT9555_RELAY_BANK, 0x00)
        self.cat9555.write_output(CYGHERMESDef.CAT9555_RELAY_BANK, 0x00)
        self.cat9555.write_dir(CYGHERMESDef.CAT9555_COMP_BANK, 0x00)
        self.cat9555.write_output(CYGHERMESDef.CAT9555_COMP_BANK, 0x00)
        self.select_range = ["2mA", "2mA", "2mA", "2mA"]
        self.reset_ad4134()
        self.select_ad_spi(1)
        self.ad5522.set_system_control(cmd_sys)
        self.ad5522.set_dac_offset_value(int(self.base_dac_offset))
        self.update_dac_and_pmu_reg()
        return "done"

    def reset_ad4134(self):
        self.select_ad_spi(0)
        self.ad4134.reset()
        time.sleep(0.5)
        self.ad4134.set_data_frame(2)
        self.ad4134.set_ip_channel_format(2)
        self.ad4134.set_channels_packet_config(2, 0, 1, 0)
        self.ad4134.set_channels_dig_filter([2, 2, 2, 2])
        self.ad4134.set_ad4134_power_mode("fast")
        self.ad4134.set_transfer_mode('all')
        self.ad4134.set_ad4134_parallel_output()
        time.sleep(0.2)
        self.ad4134.set_ad4134_odr(1)

    def set_single_comp_cap(self, channel, cap_type):
        '''
        Configure single pmu's compensation capacitor.

        Args:
            channel: str, select in ["ch0", "ch1", "ch2", "ch3"]
            cap_type: str, select capacitor's specifications in ["default", "lte_1nf", "lte_10nf", "lte_100nf"]
        Returns:
            str, "done"

        Examples:
            cyg_smu.set_single_comp_cap("ch0", "default")
        '''
        assert channel in CYGHERMESDef.AD5522_CHANNEL.keys()
        assert cap_type in CYGHERMESDef.CAP_SPEC.keys()
        self.cat9555.write_dir(CYGHERMESDef.CAT9555_COMP_BANK, 0x00)
        move_position = int(channel[2:]) * 2
        pin_status = self.cat9555.read_output(
            CYGHERMESDef.CAT9555_COMP_BANK) & ~(1 << move_position
                                                      | 1 << move_position + 1)
        pin_status |= (CYGHERMESDef.CAP_SPEC[cap_type]) << move_position

        self.cat9555.write_output(CYGHERMESDef.CAT9555_COMP_BANK,
                                  pin_status)
        return "done"

    def get_single_comp_cap(self, channel):
        '''
        get now single pmu's compensation capacitor specifications.

        Args:
            channel: str, select in ["ch0", "ch1", "ch2", "ch3"]
        Returns:
            str, compensation capacitor specifications, one of ["default", "lte_1nf", "lte_10nf", "lte_100nf"]

        Examples:
            cyg_smu.get_single_comp_cap("ch0")
        '''
        assert channel in CYGHERMESDef.AD5522_CHANNEL.keys()

        move_position = int(channel[2:]) * 2
        pin_status = ((self.cat9555.read_output(
            CYGHERMESDef.CAT9555_COMP_BANK)) >> move_position) & 0x03

        return next(key for key, value in CYGHERMESDef.CAP_SPEC.items()
                    if value == pin_status)

    def set_single_pmu_mode(self, channel, mode):
        '''
        set single pmu's mode, "FV" or "FI.

        Args:
            channel: str, select in ["ch0", "ch1", "ch2", "ch3"]
            mode:  str, one of ["FV", "FI"]
        Returns:
            str, "done"

        Examples:
            cyg_smu.set_single_pmu_mode("ch0", "FV)
        '''
        assert channel in CYGHERMESDef.AD5522_CHANNEL.keys()
        assert mode in ["FV", "FI"]
        self.select_ad_spi(1)

        if mode == "FV":
            self.ad5522.set_2_FV([CYGHERMESDef.AD5522_CHANNEL[channel]])
        elif mode == "FI":
            self.ad5522.set_2_FI([CYGHERMESDef.AD5522_CHANNEL[channel]])

        else:
            raise CYGHERMESException("wrong param for mode")
        return "done"

    def get_single_pmu_mode(self, channel):
        '''
        get now single pmu's mode, "FV" or "FI.

        Args:
            channel: str, select in ["ch0", "ch1", "ch2", "ch3"]
        Returns:
            str, mode, one of ["FV", "FI"]

        Examples:
            cyg_smu.get_single_pmu_mode("ch0")
        '''
        assert channel in CYGHERMESDef.AD5522_CHANNEL.keys()
        self.select_ad_spi(1)
        reg_data = self.ad5522.read_pmu_reg_back(
            CYGHERMESDef.AD5522_CHANNEL[channel])

        mode_bit = (reg_data >> 19) & 0x03

        if mode_bit == CYGHERMESDef.FV_MODE:
            return "FV"
        elif mode_bit == CYGHERMESDef.FI_MODE:
            return "FI"
        else:
            raise CYGHERMESException("wrong mode get")

    def set_single_pmu_vol(self, channel, vol):
        '''
        set single pmu's voltage value, -10000 ~ 10000 mV.

        Args:
            channel: str, select in ["ch0", "ch1", "ch2", "ch3"]
            vol:  int, -10000 ~ 10000 mV, step 10mV
        Returns:
            str, "done"

        Examples:
            cyg_smu.set_single_pmu_vol("ch0", 10)
        '''
        assert channel in CYGHERMESDef.AD5522_CHANNEL.keys()
        assert vol >= self.low_limit and vol <= self.high_limit
        self.select_ad_spi(1)
        dac_code = 0
        self.set_sys_meas_out_gain(0, 1)
        if self.low_limit >=CYGHERMESDef.LOW_LIMIT_VOL:
            cal_item = f"SINGLE_FV_{channel.upper()}"
        else:
            cal_item = f"FV_{channel.upper()}"
        vol = self.calibrate(cal_item, vol)
        dac_code = self.base_dac_offset * 0.7777 + (vol / 22500.0) * pow(2, 16)
        self.ad5522.set_output_vol(CYGHERMESDef.AD5522_CHANNEL[channel],
                                   int(dac_code))
        return "done"

    def get_single_pmu_vol(self, channel):
        '''
        get single pmu's voltage value

        Args:
            channel: str, select in ["ch0", "ch1", "ch2", "ch3"]
            
        Returns:
            vol:  int, -10000 ~ 10000 mV, step 10mV

        Examples:
            cyg_smu.get_single_pmu_vol("ch0")
        '''
        assert channel in CYGHERMESDef.AD5522_CHANNEL.keys()
        self.select_ad_spi(1)
        reg_data = self.ad5522.read_dac_reg_x_back(
            CYGHERMESDef.AD5522_CHANNEL[channel], "FIN_Vol")
        dac_code = reg_data & 0xffff
        vol = (dac_code - self.base_dac_offset * 0.7777) / pow(2, 16) * 22500.0
        return vol

    def set_single_pmu_curr_range(self, channel, curr_range):
        '''
        set single pmu's output current range

        Args:
            channel: str, select in ["ch0", "ch1", "ch2", "ch3"]
            curr_range:  str, ["5uA", "20uA", "200uA", "2mA", "external"]
        Returns:
            str, "done"

        Examples:
            cyg_smu.set_single_pmu_curr_range("ch0", "5uA")
        '''
        assert channel in CYGHERMESDef.AD5522_CHANNEL.keys()
        assert curr_range in CYGHERMESDef.CURREMT_RANGE.keys()
        self.select_ad_spi(1)
        self.ad5522.set_current_range(
            [CYGHERMESDef.AD5522_CHANNEL[channel]],
            CYGHERMESDef.CURREMT_RANGE[curr_range])
        self.select_range[int(channel[2:])] = curr_range
        return "done"

    def get_single_pmu_curr_range(self, channel):
        '''
        get single pmu's output current range

        Args:
            channel: str, select in ["ch0", "ch1", "ch2", "ch3"]
           
        Returns:
            curr_range:  str, ["5uA", "20uA", "200uA", "2mA", "external"]

        Examples:
            cyg_smu.get_single_pmu_curr_range("ch0")
        '''
        assert channel in CYGHERMESDef.AD5522_CHANNEL.keys()
        self.select_ad_spi(1)
        reg_data = self.ad5522.read_pmu_reg_back(
            CYGHERMESDef.AD5522_CHANNEL[channel])
        curr_range = (reg_data >> 15) & 0x07

        return next(key
                    for key, value in CYGHERMESDef.CURREMT_RANGE.items()
                    if value == curr_range)

    def set_single_pmu_curr(self, channel, curr):
        '''
        set single pmu's current value.

        Args:
            channel: str, select in ["ch0", "ch1", "ch2", "ch3"]
            curr: int,
                    -500 ~ 500mA for ch0, ch1, ch2, ch3 in external mode.
                    Step by 0.1uA for 5uA, 20uA, 200uA.
                    Step by 0.1mA for 2mA, external

        Returns:
            str, "done"

        Examples:
            cyg_smu.set_single_pmu_curr("ch0", 10)
        '''
        assert channel in CYGHERMESDef.AD5522_CHANNEL.keys()
        self.select_ad_spi(1)
        set_curr = 0
        self.set_sys_meas_out_gain(0, 1)
        I_range = self.select_range[int(channel[2:])]
        if self.low_limit >=CYGHERMESDef.LOW_LIMIT_VOL:
            cal_item = f"SINGLE_FI_{channel.upper()}_{I_range}"
        else:
            cal_item = f"FI_{channel.upper()}_{I_range}"
        curr = self.calibrate(cal_item, curr)
        Rsense = CYGHERMESDef.RSENSE_I_RANGE[I_range]
        I_range_gear = 1e-3 if Rsense > 500 else 1

        if I_range in CYGHERMESDef.RANGE_LIMITS.keys():
            set_curr = min(curr, CYGHERMESDef.RANGE_LIMITS[I_range])
        dac_code = (set_curr * I_range_gear * Rsense * 10 * pow(2, 16)) / (4.5 * 5000) + 32768

        self.ad5522.set_output_curr(CYGHERMESDef.AD5522_CHANNEL[channel],
                                    int(dac_code))
        return "done"

    def get_single_pmu_curr(self, channel):
        '''
        get single pmu's current value, 0 ~ 80 mA, step is 1mA.

        Args:
            channel: str, select in ["ch0", "ch1", "ch2", "ch3"]
            I_range:str, ["5uA", "20uA", "200uA", "2mA", "external"]
            
        Returns:
            curr:  int, 0 ~ 80 mA, step 1mA

        Examples:
            cyg_smu.set_single_pmu_curr("ch0", 10)
        '''
        assert channel in CYGHERMESDef.AD5522_CHANNEL.keys()
        self.select_ad_spi(1)
        res_range = self.select_range[int(channel[2:])]
        I_range = "FIN_" + res_range
        Rsense = CYGHERMESDef.RSENSE_I_RANGE[res_range]
        unit = " uA" if Rsense > 500 else " mA"
        dac_code = self.ad5522.read_dac_reg_x_back(
            CYGHERMESDef.AD5522_CHANNEL[channel], I_range) & 0xffff
        curr = ((dac_code - 32768) * (4.5 * 5000)) / (Rsense * 10 * pow(2, 16))
        if unit == " uA":
            curr_value = str(curr * 1000) + unit
        else:
            curr_value = str(curr) + unit
        return curr_value

    def clear_multi_pmu_alarm(self):
        '''
       clear alarm status of all PMU channels

       Args:
            None       
       Return:
            str, "done"
       '''
        self.select_ad_spi(1)
        for ch in ["ch0", "ch1", "ch2", "ch3"]:
            reg = self.ad5522.read_pmu_reg_back(
                CYGHERMESDef.AD5522_CHANNEL[ch])
            reg |= 1 << 6
            self.ad5522.set_pmu_control(CYGHERMESDef.AD5522_CHANNEL[ch],
                                        reg)
        return "done"

    def set_single_pmu_meas_mode(self, channel, mode):
        '''
        set single pmu's measure mode.

        Args:
            channel: str, select in ["ch0", "ch1", "ch2", "ch3"]
            mode:  str, select in ["MI", "MV"]
           
        Returns:
            str, "done"

        Examples:
            cyg_smu.set_single_pmu_meas_mode("ch0", "MV")
        '''
        assert channel in CYGHERMESDef.AD5522_CHANNEL.keys()
        assert mode in ["MV", "MI"]
        self.select_ad_spi(1)

        if mode == "MI":
            self.ad5522.set_2_MI([CYGHERMESDef.AD5522_CHANNEL[channel]])
            self.set_sys_meas_out_gain(0, 1)
        else:
            self.ad5522.set_2_MV([CYGHERMESDef.AD5522_CHANNEL[channel]])
        return "done"

    def get_single_pmu_meas_mode(self, channel):
        '''
        set single pmu's measure mode.

        Args:
            channel: str, select in ["ch0", "ch1", "ch2", "ch3"]

        Returns:
            mode:  str, select in ["MI", "MV"]

        Examples:
            cyg_smu.get_single_pmu_meas_mode("ch0")
        '''
        assert channel in CYGHERMESDef.AD5522_CHANNEL.keys()
        self.select_ad_spi(1)
        read_data = self.ad5522.read_pmu_reg_back(
            CYGHERMESDef.AD5522_CHANNEL[channel])

        mode_bit = (read_data >> 13) & 0x01

        if mode_bit == 1:
            return "MV"
        else:
            return "MI"

    def single_pmu_enable(self, channel):
        '''
        enable single pmu channel.

        Args:
            channel: str, select in ["ch0", "ch1", "ch2", "ch3"]
           
        Returns:
            str, "done"

        Examples:
            cyg_smu.single_pmu_enable("ch0")
        '''
        assert channel in CYGHERMESDef.AD5522_CHANNEL.keys()
        self.select_ad_spi(1)
        status_bit = self.cat9555.read_output(
            CYGHERMESDef.CAT9555_RELAY_BANK)
        status_bit |= 1 << int(channel[2:])
        self.cat9555.write_output(CYGHERMESDef.CAT9555_RELAY_BANK,
                                  status_bit)
        self.ad5522.enable_pmu([CYGHERMESDef.AD5522_CHANNEL[channel]])
        curr_range = self.get_single_pmu_curr_range(channel)
        if curr_range == "external":
            self.set_power_amp_board_relay(channel, 0)
        else:
            self.set_power_amp_board_relay(channel, 1)
        return "done"

    def single_pmu_disable(self, channel):
        '''
        disable single pmu channel.

        Args:
            channel: str, select in ["ch0", "ch1", "ch2", "ch3"]
           
        Returns:
            str, "done"

        Examples:
            cyg_smu.single_pmu_disable("ch0")
        '''
        assert channel in CYGHERMESDef.AD5522_CHANNEL.keys()
        self.select_ad_spi(1)
        status_bit = self.cat9555.read_output(
            CYGHERMESDef.CAT9555_RELAY_BANK)
        status_bit &= ~(1 << int(channel[2:]))
        self.cat9555.write_output(CYGHERMESDef.CAT9555_RELAY_BANK,
                                  status_bit)
        self.ad5522.disable_pmu([CYGHERMESDef.AD5522_CHANNEL[channel]])

        return "done"

    def set_multi_pmu_mode(self, channel, mode):
        '''
        set multi pmu's mode, "FV" or "FI.

        Args:
            channel: list, select in ["ch0", "ch1", "ch2", "ch3"]
            mode:  str, one of ["FV", "FI"]
        Returns:
            str, "done"

        Examples:
            cyg_smu.set_multi_pmu_mode(["ch0", "ch1]", "FV)
        '''
        assert isinstance(channel, list)
        assert mode in ["FV", "FI"]
        self.select_ad_spi(1)

        if mode == "FV":
            self.ad5522.set_2_FV(
                [CYGHERMESDef.AD5522_CHANNEL[ch] for ch in channel])
        elif mode == "FI":
            self.ad5522.set_2_FI(
                [CYGHERMESDef.AD5522_CHANNEL[ch] for ch in channel])
        else:
            raise CYGHERMESException("wrong param for mode")
        return "done"

    def set_multi_pmu_curr_range(self, channel, curr_range):
        '''
        set multi pmu's output current range

        Args:
            channel: list, select in ["ch0", "ch1", "ch2", "ch3"]
            curr_range:  str, ["5uA", "20uA", "200uA", "2mA", "external"]
        Returns:
            str, "done"

        Examples:
            cyg_smu.set_multi_pmu_curr_range(["ch0", "ch1"], "5uA")
        '''
        assert isinstance(channel, list)
        assert curr_range in CYGHERMESDef.CURREMT_RANGE.keys()
        self.select_ad_spi(1)
        for ch in channel:
            self.select_range[int(ch[2:])] = curr_range
        self.ad5522.set_current_range(
            [CYGHERMESDef.AD5522_CHANNEL[ch] for ch in channel],
            CYGHERMESDef.CURREMT_RANGE[curr_range])
        return "done"

    def set_multi_pmu_meas_mode(self, channel, mode):
        '''
        set multi pmu's measure mode.

        Args:
            channel: str, select in ["ch0", "ch1", "ch2", "ch3"]
            mode:  str, select in ["MI", "MV"]
           
        Returns:
            str, "done"

        Examples:
            cyg_smu.set_multi_pmu_meas_mode(["ch0", "ch1"], "MV")
        '''
        assert isinstance(channel, list)
        assert mode in ["MI", "MV"]
        self.select_ad_spi(1)

        if mode == "MI":
            self.ad5522.set_2_MI(
                [CYGHERMESDef.AD5522_CHANNEL[ch] for ch in channel])
        else:
            self.ad5522.set_2_MV(
                [CYGHERMESDef.AD5522_CHANNEL[ch] for ch in channel])
        return "done"

    def multi_pmu_enable(self, channel):
        '''
        enable multi pmu channel.

        Args:
            channel: list, select in ["ch0", "ch1", "ch2", "ch3"]
           
        Returns:
            str, "done"

        Examples:
            cyg_smu.multi_pmu_enable(["ch0", "ch1"])
        '''
        assert isinstance(channel, list)
        self.select_ad_spi(1)

        status_bit = self.cat9555.read_output(
            CYGHERMESDef.CAT9555_RELAY_BANK) & ~(1 << 0 | 1 << 1 | 1 << 2
                                                       | 1 << 3)
        for ch in channel:
            status_bit |= 1 << int(ch[2:])
        self.cat9555.write_output(CYGHERMESDef.CAT9555_RELAY_BANK,
                                  status_bit)
        self.ad5522.enable_pmu(
            [CYGHERMESDef.AD5522_CHANNEL[ch] for ch in channel])

        return "done"

    def multi_pmu_disable(self, channel):
        '''
        disable single pmu channel.

        Args:
            channel: str, select in ["ch0", "ch1", "ch2", "ch3"]
           
        Returns:
            str, "done"

        Examples:
            cyg_smu.multi_pmu_disable(["ch0", "ch1"])
        '''
        assert isinstance(channel, list)
        self.select_ad_spi(1)
        status_bit = self.cat9555.read_output(
            CYGHERMESDef.CAT9555_RELAY_BANK)
        for ch in channel:
            status_bit &= ~(1 << int(ch[2:]))
        self.cat9555.write_output(CYGHERMESDef.CAT9555_RELAY_BANK,
                                  status_bit)
        self.ad5522.disable_pmu(
            [CYGHERMESDef.AD5522_CHANNEL[ch] for ch in channel])

        return "done"

    def set_sys_meas_out_gain(self, gain0, gain1):
        '''
        set measure out gain.

        Args:
            gain0: int, select in [0, 1]
            gain1: int, select in [0, 1]

        Return:
            "done"
        '''
        assert gain0 in [0, 1]
        assert gain1 in [0, 1]
        gain0_bit = gain0 << 6
        gain1_bit = gain1 << 7
        cmd_sys = self.ad5522.read_sys_reg_back() & ~0xC0
        cmd_sys |= gain0_bit | gain1_bit
        self.select_ad_spi(1)
        self.ad5522.set_system_control(cmd_sys)
        return "done"

    def get_sys_meas_out_gain(self):
        '''
        get measure out gain.

        Args:
            None

        Return:
            gain0: int, select in [0, 1]
            gain1: int, select in [0, 1]
        '''
        cmd_sys = 1 << 28
        self.select_ad_spi(1)
        reg_sys = self.ip_control.ad5522_spi_read(cmd_sys)
        gain0 = reg_sys >> 6 & 0x01
        gain1 = reg_sys >> 7 & 0x01

        return [gain0, gain1]

    def set_sys_thermal_shutdown_temp(self, shutdown_temp):
        '''
        set device shutdown temperature.

        Args:
            shutdown_temp: int
        
        Return:
            str, "done"
        '''
        assert shutdown_temp in [100, 110, 120, 130]
        self.select_ad_spi(1)
        cmd_sys = (self.ad5522.read_sys_reg_back()) & ~0x38
        tmp_bit = (3 - int(str(shutdown_temp)[1:2])) << 3
        tmp_enable_bit = 1 << 5
        cmd_sys |= tmp_bit | tmp_enable_bit
        self.ad5522.set_system_control(cmd_sys)

        return "done"

    def get_sys_thermal_shutdown_temp(self):
        '''
        get device shutdown temperature.

        Args:
            None
        
        Return:
            int, shutdown_temp
        '''
        self.select_ad_spi(1)
        cmd_sys = 1 << 28
        reg_sys = self.ip_control.ad5522_spi_read(cmd_sys)
        temp_code = (reg_sys >> 3) & 0x03

        return CYGHERMESDef.TEMP_RANGE[temp_code]

    def get_single_meas_result(self, channel, mean_num=10, retry_times=5):
        '''
        Get measured result of one channel.

        Args:
            channel, string, ['ch0', 'ch1', 'ch2', 'ch3']

        Return: dict, {'chx_volt': xxx} or {'chx_curr':xxx}

        '''
        meas_result = self.get_multi_meas_result([channel], mean_num,
                                                 retry_times)
        return meas_result

    def get_multi_meas_result(self, channel_list, mean_num=10, retry_times=5):
        '''
            Get measured result of one channel.

            Args:
                channel_list, list of string, ['ch0', 'ch1', 'ch2', 'ch3']

            Return: dict, {'chx_volt': xxx} or {'chx_curr': xxx}

        '''
        channel_dict = {'ch0': 0, 'ch1': 1, 'ch2': 2, 'ch3': 3}
        for channel in channel_list:
            assert channel in channel_dict, 'invalid channel: %s' % channel
        assert isinstance(
            mean_num,
            int) and mean_num > 0, 'average number should greater than 0'
        meas_result = {}
        self.select_ad_spi(0)
        for _ in range(retry_times):
            mv_result = self.ad4134.measure(channel_list, mean_num, 5)
            mv_result = {
                channel: mv_result[int(channel[2:])] for channel in channel_list
            }
            if False not in [len(data) == mean_num for _, data in mv_result.items()]:
                settled = True
                break
            else:
                settled = False
                time.sleep(0.2)
        assert settled, 'Some data not settled in channels, please try again.'
        self.select_ad_spi(1)
        _, gain1 = self.get_sys_meas_out_gain()
        gain_select = 1 if gain1 == 0 else 0.2
        for channel, data in mv_result.items():
            data = sum(data) / mean_num
            meas_mode = self.get_single_pmu_meas_mode(channel)
            if meas_mode == 'MV':
                if self.low_limit >= CYGHERMESDef.LOW_LIMIT_VOL:
                    calibrate_item = f"SINGLE_{meas_mode}_{channel.upper()}"
                else:
                     calibrate_item = f"{meas_mode}_{channel.upper()}"
                if gain_select == 0.2:
                    volt = self.calibrate(calibrate_item, (1 / gain_select) * data + self.low_limit)
                else:
                    volt = self.calibrate(calibrate_item, (1 / gain_select) * data)
                meas_result['%s_volt' % channel] = {
                    'value': volt,
                    'unit': 'mV'
                }
            else:
                I_range = self.select_range[int(channel[2:])]
                if self.low_limit >= CYGHERMESDef.LOW_LIMIT_VOL:
                    calibrate_item = f"SINGLE_{meas_mode}_{channel.upper()}_{I_range}"
                else:
                    calibrate_item = f"{meas_mode}_{channel.upper()}_{I_range}"
                Rsense = CYGHERMESDef.RSENSE_I_RANGE[I_range]
                I_range_gear = 1e3 if Rsense > 500 else 1
                i_unit = " uA" if Rsense > 500 else " mA"
                curr = self.calibrate(calibrate_item, (data - (11250 * 0.2)) / (2 * Rsense) * I_range_gear)
                meas_result['%s_curr' % channel] = {
                    'value': curr,
                    'unit': i_unit
                }
        return meas_result

    def set_register_data(self, channel, reg_type, reg_data):
        '''
        Set add5522 reg, select in ["SYS_CTRL", 'PMU', 'DAC']

        Args:
            channel: ["ch0", "ch1", "ch2", "ch3"]
            ret_type: str, select in ["SYS_CTRL", 'PMU', 'DAC']
            reg_data: int, 32bit
        Return:
            str, "done"
        '''
        assert channel in CYGHERMESDef.AD5522_CHANNEL.keys()
        assert reg_type in ["SYS_CTRL", "PMU", "DAC"]

        if reg_type == "SYS_CTRL":
            self.ad5522.set_system_control(reg_data)
        elif reg_type == "PMU":
            self.ad5522.set_pmu_control(
                CYGHERMESDef.AD5522_CHANNEL[channel], reg_data)
        elif reg_type == "DAC":
            self.ad5522.set_output_vol(
                CYGHERMESDef.AD5522_CHANNEL[channel], reg_data)
        else:
            raise CYGHERMESException("error param for reg_type")
        return "done"

    def get_alarm_status(self):
        '''
        Get alarm status.
        
        Args:
            None.
        Return:
            dict.
        '''
        alarm_reg_dict = {}
        reg_data = self.ad5522.read_alarm_reg_back() >> 4
        alarm_reg_dict = {
            name: (reg_data >> _pos) & 0x01
            for _pos, name in enumerate(CYGHERMESDef.PMU_ALARM_REG_DEF)
        }
        return alarm_reg_dict

    def get_register_data(self, reg_type, channel="ch0", dac_type="FIN_Vol"):
        '''
        Get select register data.

        Args:
            ret_type: str, select in ["SYS_CTRL", 'PMU', 'DAC', 'ALARM']
            channel: ["ch0", "ch1", "ch2", "ch3"]
            dac_type: str, ["FIN_5uA", "FIN_20uA", "FIN_200uA", "FIN_2mA", 
                            "FIN_external", "FIN_Vol", "CLL_Curr", "CLL_Vol",
                            "CLH_Curr", "CLH_Vol"]
        Return:
            dict.
        '''
        assert channel in CYGHERMESDef.AD5522_CHANNEL.keys()
        assert reg_type in ["SYS_CTRL", "PMU", "DAC", "ALARM"]
        assert dac_type in CYGHERMESDef.DAC_TYPE_IN_USER
        dac_reg_dicts = {}
        pmu_reg_dicts = {}
        channel_dict = {}
        sys_reg_dict = {}
        if reg_type == "DAC":
            dac_reg_value_m = (self.ad5522.read_dac_reg_m_back(
                CYGHERMESDef.AD5522_CHANNEL[channel], dac_type)
                               & 0xffff)
            dac_reg_value_c = self.ad5522.read_dac_reg_c_back(
                CYGHERMESDef.AD5522_CHANNEL[channel], dac_type) & 0xffff
            dac_reg_value_x = self.ad5522.read_dac_reg_x_back(
                CYGHERMESDef.AD5522_CHANNEL[channel], dac_type) & 0xffff
            channel_dict[dac_type] = {
                "M_C_X1": [dac_reg_value_m, dac_reg_value_c, dac_reg_value_x]
            }
            dac_reg_dicts[f"PMU{channel[2:]}"] = channel_dict
            return dac_reg_dicts
        elif reg_type == "SYS_CTRL":
            sys_reg_value = (self.ad5522.read_sys_reg_back()) >> 2
            sys_reg_dict = {
                name: (sys_reg_value >> _pos) & 0x01
                for _pos, name in enumerate(
                    CYGHERMESDef.SYS_CONTROL_REG_DEF)
            }
            return sys_reg_dict
        elif reg_type == "PMU":
            pmu_reg_value = self.ad5522.read_pmu_reg_back(
                CYGHERMESDef.AD5522_CHANNEL[channel]) >> 5
            pmu_reg_dict = {
                name: (pmu_reg_value >> _pos) & 0x01
                for _pos, name in enumerate(
                    CYGHERMESDef.PMU_CONTROL_REG_DEF)
            }
            pmu_reg_dicts[f"PMU{channel[2:]}"] = pmu_reg_dict
            return pmu_reg_dicts
        else:
            return self.get_alarm_status()

    def set_dut_positive_volt(self, volt):
        '''
        Set mcp4725 amp positive voltatge.

        Args:
            volt, int, Vamp value.
        Return:
            "done"
        '''
        volt = 8000 if volt < 8000 else volt
        volt = 26000 if volt > 26000 else volt
        Vmcp_set = (25600 - volt) / 5.0
        self.mcp4725_P.output_volt_dc(Vmcp_set)
        self.Vmcp4725_Vamp = volt
        return "done"

    def set_dut_negative_volt(self, volt):
        '''
        Set mcp4725 amp nagative voltatge.

        Args:
            volt, int, Vamp value.
        Return:
            "done"
        '''
        volt = -6000 if volt > -6000 else volt
        volt = -16000 if volt < -16000 else volt
        
        Vmcp_set = (5500 + volt) / (-3.33)
        self.mcp4725_N.output_volt_dc(Vmcp_set)
        self.Vmcp4725_Vamp = volt
        return volt

    def read_all_control_reg(self):
        '''
        Get all control reg value.

        Args:
            None
        Return:
            dict.
        '''
        pmu_reg_dicts = {}
        sys_reg_dict = {}

        sys_reg_value = (self.ad5522.read_sys_reg_back()) >> 2
        sys_reg_dict = {
            name: (sys_reg_value >> _pos) & 0x01
            for _pos, name in enumerate(CYGHERMESDef.SYS_CONTROL_REG_DEF)
        }
        for channel in ["ch0", "ch1", "ch2", "ch3"]:
            pmu_reg_value = self.ad5522.read_pmu_reg_back(
                CYGHERMESDef.AD5522_CHANNEL[channel]) >> 5
            pmu_reg_dict = {
                name: (pmu_reg_value >> _pos) & 0x01
                for _pos, name in enumerate(
                    CYGHERMESDef.PMU_CONTROL_REG_DEF)
            }
            pmu_reg_dicts[f"PMU{channel[2:]}"] = pmu_reg_dict

        pmu_reg_list = self.ad5522.pmu_reg
        return [sys_reg_dict, pmu_reg_dicts, pmu_reg_list]

    def update_dac_and_pmu_reg(self):
        '''
        Update DAC and PMU regisetr value.

        Args:
            None
        Return:
            "done"
        '''
        self.ip_control.set_LOAD_pin(0)
        self.ip_control.set_LOAD_pin(1)
        return "done"

    def write_module_calibration(self, channel, calibration_vectors=None):
        '''
         This module function write module level calibration parameters into EEPROM.

         Args:
             channel: string, 

             calibration_vectors:   list, [[module_raw1, benchmark1], [module_raw2, benchmark2], ...
                                     [module_rawN, benchmarkN]].

         Returns:
             string, "done".

         Examples:
             result = write_module_calibration('BATT_VOL_SET', vectors)

         '''
        assert calibration_vectors is not None
        assert channel in list(self.cal_table.keys())

        cal_index = self.cal_table[channel]

        segments = CYGHERMESDef.cyg_hercules_func_info[channel][
            'cali_segment']
        assert len(segments) < 16

        count = len(segments)

        cell = CalCell(self.get_cell_size(cal_index))
        cell.set_count(count)
        for index in range(count):
            seg_conf = segments[index]
            seg_start, seg_end = seg_conf.get("limit")
            seg_threshold = seg_conf.get("threshold")
            seg_vectors = [
                benchmark for benchmark in calibration_vectors
                if benchmark[1] >= seg_start and benchmark[1] <= seg_end
            ]
            if len(seg_vectors) < 2:
                err_str = "no enough data for calibration. ({}, {})".format(
                    seg_start, seg_end)
            gain, offset = self.linear_regress(seg_vectors)
            cell.add_calibration_item(gain, offset, seg_threshold, index)

        self.write_calibration_cell(cal_index, cell.to_bytearray())
        return 'done'

    def linear_regress(self, vectors):
        '''
        calculte the gain and offset value for the calibration.

        Args:
            vectors:  list, [[module_raw1,benchmark1], [module_raw2,benchmark2], ... [module_rawN,benchmarkN]]

        Returns:
            k:  float, gain value.
            b:  float, offset value.

        Examples:
            (k, b) = cyg_odin.linear_regress([[1, 2], [4, 2], [23.1, 81.23]])

        '''
        N = len(vectors)
        sigma_x = 0
        sigma_y = 0
        sigma_x2 = 0
        sigma_xy = 0
        for i in range(N):
            sigma_x += vectors[i][0]
            sigma_x2 += vectors[i][0] * vectors[i][0]
            sigma_y += vectors[i][1]
            sigma_xy += vectors[i][0] * vectors[i][1]

        k = (N * sigma_xy - sigma_x * sigma_y) / \
            (N * sigma_x2 - sigma_x * sigma_x)
        b = (sigma_x2 * sigma_y - sigma_xy * sigma_x) / \
            (N * sigma_x2 - sigma_x * sigma_x)
        return round(k, 6), round(b, 6)

    def sequence_set_single_pmu_vol(self, channel, vol, continue_time):
        '''
        set single pmu's voltage value, -10000 ~ 10000 mV.

        Args:
            channel: str, select in ["ch0", "ch1", "ch2", "ch3"]
            vol:  int, -10000 ~ 10000 mV, step 10mV
        Returns:
            str, "done"

        Examples:
            cyg_smu.set_single_pmu_vol("ch0", 10)
        '''
        assert channel in CYGHERMESDef.AD5522_CHANNEL.keys()
        self.select_ad_spi(1)
        dac_code = 0
        self.set_sys_meas_out_gain(0, 1)
        vol = self.calibrate(f"FV_{channel.upper()}", vol)
        dac_code = self.base_dac_offset * 0.7777 + (vol / 22500.0) * pow(2, 16)
        _convert_cmd = 1 << (24 + int(channel[2:])) | int(
            dac_code) | 0x0D << 16 | 0x03 << 22
        self.ip_control.write_cmd_list(_convert_cmd, 1, continue_time)
        return "done"

    def sequence_set_single_pmu_curr(self, channel, curr, continue_time):
        '''
        set single pmu's current value.

        Args:
            channel: str, select in ["ch0", "ch1", "ch2", "ch3"]
            curr: int,
                    0 ~ 80 mA for ch0, ch1, ch2, ch3 in external mode.
                    Step by 0.1uA for 5uA, 20uA, 200uA.
                    Step by 0.1mA for 2mA, external

        Returns:
            str, "done"

        Examples:
            cyg_smu.set_single_pmu_curr("ch0", 10)
        '''
        assert channel in CYGHERMESDef.AD5522_CHANNEL.keys()
        self.select_ad_spi(1)
        set_curr = 0
        self.set_sys_meas_out_gain(0, 1)
        I_range = self.select_range[int(channel[2:])]
        cal_item = f"FI_{channel.upper()}_{I_range}"
        Rsense = CYGHERMESDef.RSENSE_I_RANGE[I_range]
        curr = self.calibrate(cal_item, curr)
        I_range_gear = 1e-3 if Rsense > 500 else 1

        if I_range in CYGHERMESDef.RANGE_LIMITS.keys():
            set_curr = min(curr, CYGHERMESDef.RANGE_LIMITS[I_range])
        dac_code = (set_curr * I_range_gear * Rsense * 10 *
                    pow(2, 16)) / (4.5 * 5000) + 32768

        self.ad5522.sequence_set_output_curr(
            CYGHERMESDef.AD5522_CHANNEL[channel], int(dac_code),
            0)
        self.ad5522.sequence_enable_pmu(
            CYGHERMESDef.AD5522_CHANNEL[channel], continue_time)
        return "done"

    def sequence_disable_single_pmu(self, channel, channel_change_time):
        '''
        disable single pmu channel.

        Args:
            channel: str, select in ["ch0", "ch1", "ch2", "ch3"]
           
        Returns:
            str, "done"

        Examples:
            cyg_smu.single_pmu_disable("ch0")
        '''
        assert channel in CYGHERMESDef.AD5522_CHANNEL.keys()
        self.select_ad_spi(1)
        self.ad5522.sequnece_disable_pmu(
            CYGHERMESDef.AD5522_CHANNEL[channel], channel_change_time)
        return "done"

    def sequence_enable_single_pmu(self, channel, channel_change_time):
        '''
        disable single pmu channel.

        Args:
            channel: str, select in ["ch0", "ch1", "ch2", "ch3"]
           
        Returns:
            str, "done"

        Examples:
            cyg_smu.single_pmu_disable("ch0")
        '''
        assert channel in CYGHERMESDef.AD5522_CHANNEL.keys()
        self.select_ad_spi(1)
        self.ad5522.sequence_enable_pmu(
            CYGHERMESDef.AD5522_CHANNEL[channel], channel_change_time)
        return "done"

    def control_FV_sequence(self,
                            channel_list,
                            vol_list,
                            continue_time_list,
                            channel_change_time_list,
                            raise_time1,
                            raise_time2,
                            is_loop,
                            count):
        '''
        Control channels output different voltage by set time。

        Args:
            channel_list: list, ["ch0", "ch1", "ch2", "ch3"]
            vol_list: list, [1000, 2000, 3000, 4000]
            continue_time_list: [35, 35, 35, 35]
            channel_change_time_list: [10, 10, 10, 10]
            raise_time1: 0
            raise_time1: 2
            is_loop: bool, assert in ['False', 'True']
            count: 1
        Return:
            "done"
        '''
        for ch in channel_list:
            self.set_single_pmu_curr_range(ch, "external")
            self.set_single_pmu_mode(ch, "FV")
            self.set_single_pmu_vol(ch, 0)
            self.single_pmu_enable(ch)
            self.update_dac_and_pmu_reg()
        self.ip_control.enable_loop_func(is_loop)
        if is_loop:
            count = 1
        for i in range(count):
            for num, ch in enumerate(channel_list):
                self.sequence_set_single_pmu_vol(
                    ch, vol_list[num],
                    int(125 * (continue_time_list[num] - 9.4 + raise_time1)))
                self.sequence_set_single_pmu_vol(
                    ch, 0,
                    int(125 *
                        (channel_change_time_list[num] - 9.4 + raise_time2)))
        if (self.ip_control.get_cmd_list_send_status() == 0):
            self.ip_control.enable_cmd_list_send(is_loop)
        else:
            raise CYGHERMESException("Please wait for while")
        return "done"

    def control_FI_sequence(self, channel_list, curr_list, continue_time_list,
                            channel_change_time_list, raise_time1, raise_time2,
                            is_loop, count):
        '''
        Control channels output different current by set time。

        Args:
            channel_list: list, ["ch0", "ch1", "ch2", "ch3"]
            vol_list: list, [1000, 2000, 3000, 4000]
            continue_time_list: [35, 35, 35, 35]
            channel_change_time_list: [10, 10, 10, 10]
            raise_time1: 0
            raise_time1: 2
            is_loop: bool, assert in ['False', 'True']
            count: 1
        Return:
            "done"
        '''
        for ch in channel_list:
            self.set_single_pmu_curr_range(ch, "external")
            self.set_single_pmu_mode(ch, "FI")
            self.hercules_enable_relay(ch)
            self.update_dac_and_pmu_reg()

        self.ip_control.enable_loop_func(is_loop)
        if is_loop:
            count = 1
        for i in range(count):
            for num, ch in enumerate(channel_list):
                self.sequence_set_single_pmu_curr(
                    ch, curr_list[num], int(125 * (continue_time_list[num] - 9.4 + raise_time1)))
                self.sequence_disable_single_pmu(
                    ch, int(125 * (channel_change_time_list[num] - 9.4 + raise_time2)))
        if (self.ip_control.get_cmd_list_send_status() == 0):
            self.ip_control.enable_cmd_list_send(is_loop)
        else:
            raise CYGHERMESException("Please wait for while")
        return "done"

    def set_dac_range(self, low_vol=None):
        '''
        set ic output voltage range, unit mV

        Args:
            low_vol: int, make sure low_vol <= 0

        Return:
            str, "done"
        '''
        self.set_dut_negative_volt(-6000)
        self.set_dut_positive_volt(14000)
        coefficient = 3744.9143
        if low_vol == None:
            raw = bytes(self.eeprom.read(CYGHERMESDef.OUTPUT_RANGE_ADDRESS, 4))
            if raw == b'\xff\xff\xff\xff':
                low_vol = -11250
            else:
                low_vol = struct.unpack('!i', raw)[0]
        if low_vol >= CYGHERMESDef.LOW_LIMIT_VOL:
            low_vol = -1250
        self.set_dut_negative_volt(low_vol - 2750)
        self.set_dut_positive_volt(low_vol + 22500 + 2750)
        self.multi_pmu_disable(["ch0", "ch1", "ch2", "ch3"])
        self.base_dac_offset = coefficient * abs(low_vol) / 1000
        self.ad5522.set_dac_offset_value(int(self.base_dac_offset))
        self.update_dac_and_pmu_reg()
        self.low_limit = low_vol
        self.high_limit = low_vol + 22500
        byte_low_vol = struct.pack('!i', low_vol)
        list_low_vol = list(byte_low_vol)
        self.eeprom.write(CYGHERMESDef.OUTPUT_RANGE_ADDRESS, list_low_vol)
        return [low_vol, low_vol + 22500]
    
    def get_dac_range(self):
        '''
        Get AD5522 output range.
        '''
        return [self.low_limit, self.high_limit]

    def hercules_enable_relay(self, channel):
        '''
        Only control relay.
        Args:
            channel: str, assert in ['ch0', 'ch1', 'ch2', 'ch3']
        Return:
            "done"
        '''
        assert channel in CYGHERMESDef.AD5522_CHANNEL.keys()
        status_bit = self.cat9555.read_output(
            CYGHERMESDef.CAT9555_RELAY_BANK)
        status_bit |= 1 << int(channel[2:])
        self.cat9555.write_output(CYGHERMESDef.CAT9555_RELAY_BANK,
                                  status_bit)
        curr_range = self.get_single_pmu_curr_range(channel)
        if curr_range == "external":
            self.set_power_amp_board_relay(channel, 0)
        else:
            self.set_power_amp_board_relay(channel, 1)

        return "done"

    def enable_cmd_list(self, is_loop):
        '''
        enable cmd list.
        Args:
            is_loop, bool, assert in [True, False], if not need loop output, set it to False
        Returns:
            "done"
        '''
        assert is_loop in [True, False]
        self.ip_control.enable_cmd_list_send(is_loop)
        return "done"

    def control_loop(self, status):
        '''
        enable loop output function.
        Args:
            is_loop, bool, assert in [True, False], if not need loop output, set it to False
        Returns:
            "done"
        '''
        assert status in [True, False]
        self.ip_control.enable_loop_func(status)
        return "done"

    def open_stream(self,
                    id,
                    channels,
                    ds_factor=1,
                    ds_op='min',
                    autostart=False,
                    readraw=True):
        '''
        Opens a DataStream session to the module for performing continuous acquisitions

        Args:
            buffer_id: str, a unique string used to identify the buffer
            channels: list, channels length should be 1, channel can be [0], [1], [0, 1], ['all']
            ds_factor: int, the down sampling factor for the buffered read. For example, a value
                            of 2 would return data at 1/2 the rate of acquisition of the module.
            ds_op: str, the operation performed when decimating, whether it be ignoring values
                        vs taking the mean, max, etc
            sample_rate:    float, [5~250000], unit Hz, default 1000, set sampling rate of data acquisition in SPS.
                                            please refer to AD7175 data sheet for more.
            down_sample:    int, (>0), default 1, down sample rate for decimation.
            selection:      string, ['max', 'min'], default 'max'. This parameter takes effect as long as down_sample
                                    is higher than 1. Default 'max'

        Returns:
            A DataStream object for performing data stream operations
        '''
        assert isinstance(ds_factor, int) and ds_factor >= 1
        assert ds_op in ['max', 'min', 'avg']

        if channels not in [[0], [1]]:
            raise ValueError("Invalid channels '{}'".format(channels))

        config = {}
        config.update({
            'channels': channels,
            'ds_factor': ds_factor,
            'ds_op': ds_op
        })
        self.stream = super().open_stream('B' if readraw else 'd', id, config,
                                          autostart)

        class FilterRawData(StreamFilter):

            def __init__(self):
                pass

            def filter(self, data):
                return data

        if readraw:
            self.stream.add_data_filter(FilterRawData())

        return self.stream

    def pre_thread_launch(self):
        '''
        Initialize anything in the module to prepare for streaming
        Anything that should be reset if all streams were stopped, then started again
        
        Args:
            None
        Returns:
            None
        '''
        self.up0 = self.dma.open()

    def post_thread_shutdown(self):
        '''
        Handle anything that should be done when all streams are closed, and the read loop stops
        
        Args:
            None

        Returns:
            None
        '''
        self.up0.close()

    def streaming_read(self, size, timeout):
        '''
        Read from DMA
        Args:
            size: int, representative read count, suggest size >= 48000

        Returns:
            data_list, list, raw data in list
        '''
        data_list = []
        data = self.up0.read(size, timeout)
        data_list = [byte for byte in data]
        return data_list
    
    def reset_power_amp_board_relay(self):
        '''
        Reset amp board relay.        
        '''
        for id in range(0, 16):
            self.cat9555_amp.set_pin_dir(id, 0)
            self.cat9555_amp.set_pin_val(id, 1)
        return "done"
    
    def set_power_amp_board_relay(self, channel, status):
        '''
        Set amp board relay.

        Args:
            channel: str, ["ch0", "ch1", "ch2", "ch3"]
            status: int, [0, 1]
        Return:
            "done"
        '''

        assert channel in ["ch0", "ch1", "ch2", "ch3"]
        assert status in [0, 1]

        pin_num = int(channel[2:]) + 4
        self.cat9555_amp.set_pin_val(pin_num, status)
        return "done"
