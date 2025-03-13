import pytest
import mock
from mock import call
from mock import patch
from unittest.mock import Mock
from mix.driver.core.ic.cat24cxx import CAT24C64
from mix.driver.cyg.common.ic.ad5522 import AD5522, AD5522RegDef
from mix.driver.core.bus.axi4_lite_bus import AXI4LiteBus
from mix.driver.cyg.common.ipcore.mix_smu_lite_cyg import MIX_SMU_Lite_CYG
from mix.driver.cyg.common.module.cyg_module_driver import CYGModuleDriver, CalCell
from mix.driver.core.ic.cat9555 import CAT9555
from mix.rpc.services.streamservice import StreamServiceBuffered, StreamFilter
from mix.driver.cyg.hercules_lite_v2.module.cyg_hercules_lite_v2 import CYG_HERCULES_LITE_V2, \
    CYGHERCULESLITEException, CYGHERCULESLITEDef

@pytest.fixture(scope="module")
def CYG_HERCULES():
    i2c_1 = mock.Mock()
    i2c_2 = mock.Mock()
    ipcore = "/dev/MIX_HERCULES_CY"
    smu_path = "mix.driver.cyg.hercules_lite_v2.module.cyg_hercules_lite_v2."
    with mock.patch(smu_path + "CAT9555"):
        with mock.patch(smu_path + "CAT24C64"):
            with mock.patch(smu_path + "AXI4LiteBus"):
                with mock.patch(smu_path + "AD5522"):
                    with mock.patch(smu_path + "MCP4725"):
                        with mock.patch(smu_path + "MIXAD4134CYG"):
                            with patch.object(CYGModuleDriver, '__init__') as mock_init:
                                with patch.object(CYGModuleDriver, "load_calibration") as mock_set_mode:
                                    with patch.object(CYGModuleDriver, "calibrate") as mock_set_mode:
                                        with patch.object(CYGModuleDriver, "calibrate") as mock_set_mode:
                                            CYG_HERCULES_LITE_V2.low_limit = -1250
                                            with mock.patch.object(CYG_HERCULES_LITE_V2, "set_dac_range",
                                                                   return_value=[-11250, 11250]):
                                                with mock.patch(smu_path + "MIX_SMU_Lite_CYG"):
                                                    with mock.patch.object(CYG_HERCULES_LITE_V2, "reset"):
                                                        CYG_HERCULES_LITE_V2(i2c_1, i2c_2)
                                                        with pytest.raises(ValueError, match='No valid i2c bus input'):
                                                            CYG_HERCULES_LITE_V2(None, None)
                                                        smu = CYG_HERCULES_LITE_V2(i2c_1, i2c_2, ipcore)
                                                        smu.eeprom = mock.Mock()
                                                        smu.cat9555 = mock.Mock()
                                                        smu.ad5522 = mock.Mock()
                                                        smu.mcp4725_P = mock.Mock()
                                                        smu.mcp4725_N = mock.Mock()
                                                        smu.ad4134 = mock.Mock()
                                                        smu.ip_control = mock.Mock()
            return smu


def test_error_condition():
    error_message = CYGHERCULESLITEException
    print(error_message("error"))


def test_get_driver_version(CYG_HERCULES):
    CYG_HERCULES.get_driver_version()


def test_reset(CYG_HERCULES):
    with mock.patch.object(CYG_HERCULES.ad5522, 'set_pmu_control'):
        with mock.patch.object(CYG_HERCULES.ad5522, 'set_output_vol'):
            with mock.patch.object(CYG_HERCULES, 'power_on_init'):
                with mock.patch.object(CYG_HERCULES.cat9555, 'write_dir', return_value=0):
                    with mock.patch.object(CYG_HERCULES.cat9555, 'write_output'):
                        with mock.patch.object(CYG_HERCULES, 'set_single_pmu_curr_range'):
                            with mock.patch.object(CYG_HERCULES, 'set_single_comp_cap'):
                                with mock.patch.object(CYG_HERCULES, 'set_single_pmu_vol'):
                                    with mock.patch.object(CYG_HERCULES, 'set_dac_range'):
                                        with patch.object(CYGModuleDriver, "calibrate") as mock_set_mode:
                                            with mock.patch.object(CYG_HERCULES, 'single_pmu_enable'):
                                                with mock.patch.object(CYG_HERCULES, 'update_dac_and_pmu_reg'):
                                                    with mock.patch.object(CYG_HERCULES, 'single_pmu_disable'):
                                                        CYG_HERCULES.reset()

def test_power_on_init(CYG_HERCULES):
    CYG_HERCULES.base_dac_offset = 100
    with mock.patch.object(CYG_HERCULES.ad5522, 'set_dac_offset_value'):
        with mock.patch.object(CYG_HERCULES.ad5522, 'set_system_control'):
            with mock.patch.object(CYG_HERCULES, 'select_range'):
                with mock.patch.object(CYG_HERCULES.cat9555, 'write_dir'):
                    with mock.patch.object(CYG_HERCULES.cat9555, 'write_output'):
                        with mock.patch.object(CYG_HERCULES, 'set_single_pmu_vol'):
                            with patch.object(CYGModuleDriver, "calibrate") as mock_set_mode:
                                with mock.patch.object(CYG_HERCULES, 'reset_ad4134'):
                                    with mock.patch.object(CYG_HERCULES.ad5522, 'set_system_control'):
                                        with mock.patch.object(CYG_HERCULES, 'set_calibration_mode'):
                                            CYG_HERCULES.power_on_init()


def test_set_single_comp_cap(CYG_HERCULES):
    with mock.patch.object(CYG_HERCULES.cat9555, 'write_dir'):
        with mock.patch.object(CYG_HERCULES.cat9555, 'read_output'):
            with mock.patch.object(CYG_HERCULES.cat9555, 'write_output'):
                CYG_HERCULES.set_single_comp_cap("ch0", "default")


def test_get_single_comp_cap(CYG_HERCULES):
    with mock.patch.object(CYG_HERCULES.cat9555, 'read_output', return_value=0):
        CYG_HERCULES.get_single_comp_cap("ch1")


def test_set_single_pmu_mode(CYG_HERCULES):
    with mock.patch.object(CYG_HERCULES.ad5522, 'set_2_FV'):
        with mock.patch.object(CYG_HERCULES.ad5522, 'set_2_FI'):
            CYG_HERCULES.set_single_pmu_mode("ch0", "FV")
            CYG_HERCULES.set_single_pmu_mode("ch0", "FI")


def test_get_single_pmu_mode(CYG_HERCULES):
    with mock.patch.object(CYG_HERCULES.ad5522, 'read_pmu_reg_back', return_value=1 << 19):
        CYG_HERCULES.get_single_pmu_mode("ch0")
    with mock.patch.object(CYG_HERCULES.ad5522, 'read_pmu_reg_back', return_value=0):
        CYG_HERCULES.get_single_pmu_mode("ch0")
    with mock.patch.object(CYG_HERCULES.ad5522, 'read_pmu_reg_back', return_value=3 << 19):
        with pytest.raises(CYGHERCULESLITEException, match='wrong mode get'):
            CYG_HERCULES.get_single_pmu_mode("ch0")


def test_set_single_pmu_vol(CYG_HERCULES):
    with mock.patch.object(CYG_HERCULES, 'select_ad_spi', return_value=1):
        with mock.patch.object(CYG_HERCULES, 'get_single_pmu_meas_mode', return_value="MI"):
            with mock.patch.object(CYG_HERCULES.ad5522, 'set_output_vol', return_value=1):
                with mock.patch.object(CYG_HERCULES, 'set_sys_meas_out_gain', return_value=1):
                    with mock.patch.object(CYG_HERCULES.ad5522, 'read_sys_reg_back', return_value=0x1):
                        with mock.patch.object(CYG_HERCULES, 'update_dac_and_pmu_reg', return_value=1):
                            with mock.patch.object(CYG_HERCULES.ad5522, 'set_dac_c_reg', return_value=1):
                                with patch.object(CYGModuleDriver, "get_calibration_mode", return_value="raw"):
                                    with patch.object(CYGModuleDriver, "set_calibration_mode", return_value=1):
                                        with patch.object(CYGModuleDriver, "calibrate", return_value=0):
                                            CYG_HERCULES.base_dac_offset = 1
                                            CYG_HERCULES.low_limit = -10000
                                            CYG_HERCULES.high_limit = 10000
                                            CYG_HERCULES.set_single_pmu_vol("ch3", 1000)


def test_get_single_pmu_vol(CYG_HERCULES):
    with mock.patch.object(CYG_HERCULES.ad5522, 'read_dac_reg_x_back'):
        CYG_HERCULES.get_single_pmu_vol("ch0")


def test_set_single_pmu_curr_range(CYG_HERCULES):
    with mock.patch.object(CYG_HERCULES.ad5522, 'set_current_range'):
        with patch.object(CYGModuleDriver, "calibrate", return_value=20):
            with mock.patch.object(CYG_HERCULES, 'select_ad_spi'):
                CYG_HERCULES.set_single_pmu_curr_range("ch0", "5uA")


def test_get_single_pmu_curr_range(CYG_HERCULES):
    with mock.patch.object(CYG_HERCULES.ad5522, 'read_pmu_reg_back', return_value=1):
        CYG_HERCULES.get_single_pmu_curr_range("ch0")


def test_set_single_pmu_curr(CYG_HERCULES):
    with mock.patch.object(CYG_HERCULES.ad5522, 'set_output_curr', return_value=1):
        with mock.patch.object(CYG_HERCULES.ad5522, 'read_sys_reg_back', return_value=0x1):
            with mock.patch.object(CYG_HERCULES, 'set_sys_meas_out_gain'):
                with mock.patch.object(CYG_HERCULES, 'select_ad_spi'):
                    with mock.patch.object(CYG_HERCULES, 'update_dac_and_pmu_reg'):
                        with mock.patch.object(CYG_HERCULES.ad5522, 'set_dac_c_reg'):
                            with patch.object(CYGModuleDriver, "get_calibration_mode", return_value="raw"):
                                with patch.object(CYGModuleDriver, "set_calibration_mode"):
                                    with patch.object(CYGModuleDriver, "calibrate", return_value=0):
                                        CYG_HERCULES.set_single_pmu_curr("ch0", 10)
                                        CYG_HERCULES.set_single_pmu_curr("ch0", 1000)
                                        CYG_HERCULES.set_single_pmu_curr("ch1", 10)


def test_get_single_pmu_curr(CYG_HERCULES):
    with mock.patch.object(CYG_HERCULES.ad5522, 'read_dac_reg_x_back', return_value=10):
        CYG_HERCULES.get_single_pmu_curr("ch0")
        CYG_HERCULES.get_single_pmu_curr("ch1")


# def test_set_single_pmu_clamp_vol(CYG_HERCULES):
#     with mock.patch.object(CYG_HERCULES.ad5522, 'set_clamp_vol'):
#         CYG_HERCULES.set_single_pmu_clamp_vol("ch0", 10, 6543)
#         CYG_HERCULES.set_single_pmu_clamp_vol("ch1", 10, 6543)


# def test_get_single_pmu_clamp_vol(CYG_HERCULES):
#     with mock.patch.object(CYG_HERCULES.ad5522, 'read_dac_reg_x_back', return_value=10):
#         CYG_HERCULES.get_single_pmu_clamp_vol("ch0")


# def test_set_single_pmu_clamp_curr(CYG_HERCULES):
#     with mock.patch.object(CYG_HERCULES.ad5522, 'set_clamp_curr', return_value=10):
#         CYG_HERCULES.set_single_pmu_clamp_curr("ch0", 10, 6534)
#         with mock.patch.object(CYG_HERCULES, 'select_range', ['-', 'external']):
#             CYG_HERCULES.set_single_pmu_clamp_curr("ch1", 10, 6534)


# def test_get_single_pmu_clamp_curr(CYG_HERCULES):
#     with mock.patch.object(CYG_HERCULES.ad5522, 'read_dac_reg_x_back', return_value=10):
#         CYG_HERCULES.get_single_pmu_clamp_curr("ch0")


def test_clear_multi_pmu_alarm(CYG_HERCULES):
    with mock.patch.object(CYG_HERCULES.ad5522, 'read_pmu_reg_back', return_value=0):
        CYG_HERCULES.clear_multi_pmu_alarm()


def test_set_single_pmu_meas_mode(CYG_HERCULES):
    with mock.patch.object(CYG_HERCULES.ad5522, 'set_2_MV'):
        with mock.patch.object(CYG_HERCULES, 'set_sys_meas_out_gain'):
            CYG_HERCULES.set_single_pmu_meas_mode("ch0", "MV")
    with mock.patch.object(CYG_HERCULES.ad5522, 'set_2_MI'):
        with mock.patch.object(CYG_HERCULES, 'set_sys_meas_out_gain'):
            CYG_HERCULES.set_single_pmu_meas_mode("ch0", "MI")


def test_get_single_pmu_meas_mode(CYG_HERCULES):
    with mock.patch.object(CYG_HERCULES.ad5522, 'read_pmu_reg_back', return_value=1 << 13):
        CYG_HERCULES.get_single_pmu_meas_mode("ch0")
    with mock.patch.object(CYG_HERCULES.ad5522, 'read_pmu_reg_back', return_value=0):
        CYG_HERCULES.get_single_pmu_meas_mode("ch0")


def test_single_pmu_enable(CYG_HERCULES):
    with mock.patch.object(CYG_HERCULES.ad5522, 'enable_pmu'):
        with mock.patch.object(CYG_HERCULES.cat9555, 'read_output', return_value=0):
            CYG_HERCULES.single_pmu_enable("ch0")


def test_single_pmu_disable(CYG_HERCULES):
    with mock.patch.object(CYG_HERCULES.ad5522, 'disable_pmu'):
        with mock.patch.object(CYG_HERCULES.cat9555, 'read_output', return_value=0):
            CYG_HERCULES.single_pmu_disable("ch0")


def test_set_multi_pmu_mode(CYG_HERCULES):
    with mock.patch.object(CYG_HERCULES.ad5522, 'set_2_FV'):
        with mock.patch.object(CYG_HERCULES.ad5522, 'set_2_FI'):
            CYG_HERCULES.set_multi_pmu_mode(["ch0", "ch1"], "FV")
            CYG_HERCULES.set_multi_pmu_mode(["ch0", "ch1"], "FI")


def test_set_multi_pmu_curr_range(CYG_HERCULES):
    with mock.patch.object(CYG_HERCULES.ad5522, 'set_current_range'):
        CYG_HERCULES.set_multi_pmu_curr_range(["ch0", "ch1"], "5uA")


def test_set_multi_pmu_meas_mode(CYG_HERCULES):
    with mock.patch.object(CYG_HERCULES.ad5522, 'set_2_MV'):
        CYG_HERCULES.set_multi_pmu_meas_mode(["ch0", "ch1"], "MV")
    with mock.patch.object(CYG_HERCULES.ad5522, 'set_2_MI'):
        CYG_HERCULES.set_multi_pmu_meas_mode(["ch0", "ch1"], "MI")


def test_multi_pmu_enable(CYG_HERCULES):
    with mock.patch.object(CYG_HERCULES.ad5522, 'enable_pmu'):
        with mock.patch.object(CYG_HERCULES.cat9555, 'read_output', return_value=0):
            CYG_HERCULES.multi_pmu_enable(["ch0", "ch1"])


def test_multi_pmu_disable(CYG_HERCULES):
    with mock.patch.object(CYG_HERCULES.ad5522, 'disable_pmu'):
        with mock.patch.object(CYG_HERCULES.cat9555, 'read_output', return_value=0):
            CYG_HERCULES.multi_pmu_disable(["ch0", "ch1"])


def test_set_sys_meas_out_gain(CYG_HERCULES):
    with mock.patch.object(CYG_HERCULES.ad5522, 'set_system_control'):
        with mock.patch.object(CYG_HERCULES.ad5522, 'read_sys_reg_back', return_value=0):
            CYG_HERCULES.set_sys_meas_out_gain(0, 1)


def test_get_sys_meas_out_gain(CYG_HERCULES):
    with mock.patch.object(CYG_HERCULES.ip_control, 'ad5522_spi_read', return_value=0xff):
        CYG_HERCULES.get_sys_meas_out_gain()


def test_set_sys_thermal_shutdown_temp(CYG_HERCULES):
    with mock.patch.object(CYG_HERCULES.ad5522, 'set_system_control'):
        with mock.patch.object(CYG_HERCULES.ad5522, 'read_sys_reg_back', return_value=0):
            CYG_HERCULES.set_sys_thermal_shutdown_temp(110)


def test_get_sys_thermal_shutdown_temp(CYG_HERCULES):
    with mock.patch.object(CYG_HERCULES.ip_control, 'ad5522_spi_read', return_value=1 << 13):
        CYG_HERCULES.get_sys_thermal_shutdown_temp()


def test_read_all_control_reg(CYG_HERCULES):
    with mock.patch.object(CYG_HERCULES.ad5522, 'read_sys_reg_back', return_value=1 << 28):
        with mock.patch.object(CYG_HERCULES.ad5522, 'read_pmu_reg_back', return_value=1 << 28):
            with mock.patch.object(CYG_HERCULES.ad5522, 'read_dac_reg_m_back', return_value=1 << 28):
                with mock.patch.object(CYG_HERCULES.ad5522, 'read_dac_reg_c_back', return_value=1 << 28):
                    with mock.patch.object(CYG_HERCULES.ad5522, 'read_dac_reg_x_back', return_value=1 << 28):
                        CYG_HERCULES.read_all_control_reg()


def test_get_single_meas_result(CYG_HERCULES):
    with mock.patch.object(CYG_HERCULES, 'get_multi_meas_result', return_value={'ch0_volt': 0}):
        CYG_HERCULES.get_single_meas_result('ch0')


def test_get_multi_meas_result(CYG_HERCULES):
    CYG_HERCULES.ad4134.measure.return_value = {0: [], 1: [], 2: [], 3: []}
    with pytest.raises(AssertionError, match='Some data not settled in channels, please try again.'):
        CYG_HERCULES.get_multi_meas_result(['ch0'])
    CYG_HERCULES.ad4134.measure.return_value = {0: [1000], 1: [1000], 2: [], 3: []}
    with mock.patch.object(CYG_HERCULES, 'get_sys_meas_out_gain', return_value=(0, 1)):
        with mock.patch.object(CYG_HERCULES, 'get_single_pmu_meas_mode', return_value='MV'):
            with mock.patch.object(CYG_HERCULES, 'calibrate', return_value=1000):
                CYG_HERCULES.get_multi_meas_result(['ch1'], 1)
        with mock.patch.object(CYG_HERCULES, 'get_single_pmu_meas_mode', return_value='MI'):
            with mock.patch.object(CYG_HERCULES, 'select_range', ['_', 'external']):
                with mock.patch.object(CYG_HERCULES, 'calibrate', return_value=1000):
                    CYG_HERCULES.get_multi_meas_result(['ch1'], 1)


def test_set_register_data(CYG_HERCULES):
    with mock.patch.object(CYG_HERCULES.ad5522, 'set_system_control'):
        with mock.patch.object(CYG_HERCULES.ad5522, 'set_pmu_control'):
            with mock.patch.object(CYG_HERCULES.ad5522, 'set_output_vol'):
                CYG_HERCULES.set_register_data("ch0", "SYS_CTRL", 1)
                CYG_HERCULES.set_register_data("ch0", "PMU", 1)
                CYG_HERCULES.set_register_data("ch0", "DAC", 1)


def test_get_alarm_status(CYG_HERCULES):
    with mock.patch.object(CYG_HERCULES.ad5522, 'read_alarm_reg_back'):
        CYG_HERCULES.get_alarm_status()


def test_set_dut_positive_volt(CYG_HERCULES):
    with mock.patch.object(CYG_HERCULES.mcp4725_P, 'output_volt_dc'):
        CYG_HERCULES.set_dut_positive_volt(2800)

def test_set_dut_negative_volt(CYG_HERCULES):
    with mock.patch.object(CYG_HERCULES.mcp4725_N, 'output_volt_dc'):
        CYG_HERCULES.set_dut_negative_volt(-2800)

def test_get_register_data(CYG_HERCULES):
    with mock.patch.object(CYG_HERCULES.ad5522, 'read_dac_reg_m_back'):
        with mock.patch.object(CYG_HERCULES.ad5522, 'read_dac_reg_c_back'):
            with mock.patch.object(CYG_HERCULES.ad5522, 'read_dac_reg_x_back'):
                with mock.patch.object(CYG_HERCULES.ad5522, 'read_sys_reg_back'):
                    with mock.patch.object(CYG_HERCULES.ad5522, 'read_pmu_reg_back'):
                        CYG_HERCULES.get_register_data("DAC", "ch0")
                        CYG_HERCULES.get_register_data("SYS_CTRL", "ch0")
                        CYG_HERCULES.get_register_data("PMU", "ch0")


def test_linear_regress(CYG_HERCULES):
    CYG_HERCULES.linear_regress([[1, 1], [2, 2]])


def test_write_module_calibration(CYG_HERCULES):
    with mock.patch.object(CYG_HERCULES, 'linear_regress', return_value=(1, 0.5)):
        with mock.patch.object(CYG_HERCULES, 'write_calibration_cell'):
            with mock.patch.object(CYG_HERCULES, 'load_calibration'):
                with mock.patch.object(CYG_HERCULES, 'get_cell_size', return_value=1):
                    CYG_HERCULES.write_module_calibration("FI_CH0_2mA", [(100, 101), (110, 115)])

def test_sequence_set_single_pmu_vol(CYG_HERCULES):
    with mock.patch.object(CYG_HERCULES, 'select_ad_spi', return_value=1):
        with mock.patch.object(CYG_HERCULES, 'get_single_pmu_meas_mode', return_value="MI"):
            with mock.patch.object(CYG_HERCULES.ip_control, 'write_cmd_list', return_value=1):
                with mock.patch.object(CYG_HERCULES, 'set_sys_meas_out_gain', return_value=1):
                    with mock.patch.object(CYG_HERCULES.ad5522, 'read_sys_reg_back', return_value=0x1):
                        with mock.patch.object(CYG_HERCULES, 'update_dac_and_pmu_reg', return_value=1):
                            with mock.patch.object(CYG_HERCULES.ad5522, 'set_dac_c_reg', return_value=1):
                                with patch.object(CYGModuleDriver, "get_calibration_mode", return_value="raw"):
                                    with patch.object(CYGModuleDriver, "set_calibration_mode", return_value=1):
                                        with patch.object(CYGModuleDriver, "calibrate", return_value=0):
                                            CYG_HERCULES.sequence_set_single_pmu_vol("ch3", 1000, 0)


def test_sequence_set_single_pmu_curr(CYG_HERCULES):
    with mock.patch.object(CYG_HERCULES.ad5522, 'sequence_set_output_curr', return_value=1):
        with mock.patch.object(CYG_HERCULES.ad5522, 'read_sys_reg_back', return_value=0x1):
            with mock.patch.object(CYG_HERCULES, 'select_ad_spi'):
                with mock.patch.object(CYG_HERCULES, 'update_dac_and_pmu_reg'):
                    with mock.patch.object(CYG_HERCULES.ad5522, 'set_dac_c_reg'):
                        with patch.object(CYGModuleDriver, "get_calibration_mode", return_value="raw"):
                            with patch.object(CYGModuleDriver, "set_calibration_mode"):
                                with patch.object(CYGModuleDriver, "calibrate", return_value=0):
                                    CYG_HERCULES.sequence_set_single_pmu_curr("ch0", 10, 0)
                                    CYG_HERCULES.sequence_set_single_pmu_curr("ch1", 10, 0)


def test_sequence_disable_single_pmu(CYG_HERCULES):
    with mock.patch.object(CYG_HERCULES.ad5522, 'sequnece_disable_pmu', return_value=0x1):
        with mock.patch.object(CYG_HERCULES, 'select_ad_spi'):
            CYG_HERCULES.sequence_disable_single_pmu("ch0", 0)


def test_sequence_enable_single_pmu(CYG_HERCULES):
    with mock.patch.object(CYG_HERCULES.ad5522, 'sequnece_enable_pmu', return_value=0x1):
        with mock.patch.object(CYG_HERCULES, 'select_ad_spi'):
            CYG_HERCULES.sequence_enable_single_pmu("ch0", 0)


def test_control_FV_sequence(CYG_HERCULES):
    with mock.patch.object(CYG_HERCULES, 'set_single_pmu_curr_range', return_value=0x1):
        with mock.patch.object(CYG_HERCULES, 'set_single_pmu_mode', return_value=0x1):
            with mock.patch.object(CYG_HERCULES, 'set_single_pmu_vol', return_value=0x1):
                with mock.patch.object(CYG_HERCULES, 'single_pmu_enable', return_value=0x1):
                    with mock.patch.object(CYG_HERCULES, 'update_dac_and_pmu_reg', return_value=0x1):
                        with mock.patch.object(CYG_HERCULES, 'sequence_set_single_pmu_vol', return_value=0x1):
                            with mock.patch.object(CYG_HERCULES.ip_control, 'get_cmd_list_send_status', return_value=0):
                                with mock.patch.object(CYG_HERCULES.ip_control, 'enable_cmd_list_send', return_value=0):
                                    CYG_HERCULES.control_FV_sequence(["ch0", "ch1"], [10, 10], [35, 35],
                                                                     [70, 70], 0, 0, True, 1)


def test_control_FI_sequence(CYG_HERCULES):
    with mock.patch.object(CYG_HERCULES, 'set_single_pmu_curr_range', return_value=0x1):
        with mock.patch.object(CYG_HERCULES, 'set_single_pmu_mode', return_value=0x1):
            with mock.patch.object(CYG_HERCULES, 'set_single_pmu_curr', return_value=0x1):
                with mock.patch.object(CYG_HERCULES, 'single_pmu_enable', return_value=0x1):
                    with mock.patch.object(CYG_HERCULES, 'update_dac_and_pmu_reg', return_value=0x1):
                        with mock.patch.object(CYG_HERCULES.ip_control, 'enable_loop_func', return_value=0x1):
                            with mock.patch.object(CYG_HERCULES, 'sequence_set_single_pmu_curr', return_value=0x1):
                                with mock.patch.object(CYG_HERCULES.ip_control, 'get_cmd_list_send_status',
                                                       return_value=0):
                                    with mock.patch.object(CYG_HERCULES.ip_control, 'enable_cmd_list_send',
                                                           return_value=0):
                                        with mock.patch.object(CYG_HERCULES.cat9555, 'read_output', return_value=1):
                                            with mock.patch.object(CYG_HERCULES.cat9555, 'write_output',
                                                                   return_value=1):
                                                CYG_HERCULES.control_FI_sequence(["ch0", "ch1"], [10, 10], [35, 35],
                                                                                 [70, 70], 0, 0, True, 1)

def test_set_dac_range(CYG_HERCULES):
    with mock.patch.object(CYG_HERCULES, 'set_dut_negative_volt', return_value=0x1):
        with mock.patch.object(CYG_HERCULES, 'set_dut_positive_volt', return_value=0x1):
            with mock.patch.object(CYG_HERCULES.eeprom, 'read', return_value=[255, 255, 255, 255]):
                with mock.patch.object(CYG_HERCULES, 'multi_pmu_disable', return_value=0x1):
                    with mock.patch.object(CYG_HERCULES.ad5522, 'set_dac_offset_value', return_value=0x1):
                        with mock.patch.object(CYG_HERCULES, 'update_dac_and_pmu_reg', return_value=0x1):
                            with mock.patch.object(CYG_HERCULES.eeprom, 'write', return_value=0x1):
                                CYG_HERCULES.set_dac_range()
