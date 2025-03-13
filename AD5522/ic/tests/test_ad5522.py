import pytest
import mock
import math
import time
from mix.driver.cyg.common.ic.ad5522 import AD5522, AD5522RegDef


__author__ = "dongsheng.yang@cygia.com"
__version__ = "1.0"


@pytest.fixture(scope="module")
def ad5522():
    AD5522(mock.Mock())
    AD5522(None)
    ad5522 = AD5522("/mix/pmu")
    ad5522.spi_ad5522 = mock.Mock()

    return ad5522


@pytest.fixture(params=[AD5522RegDef.PMU_CH_0, AD5522RegDef.PMU_CH_1, AD5522RegDef.PMU_CH_2, AD5522RegDef.PMU_CH_3],
                scope="module")
def channel(request):
    return request.param


def test_read_alarm_reg_back(ad5522):
    with mock.patch.object(ad5522.spi_ad5522, 'ad5522_spi_read') as read:
        ad5522.read_alarm_reg_back()


def test_read_pmu_reg_back(ad5522, channel):
    with mock.patch.object(ad5522.spi_ad5522, 'ad5522_spi_read') as read:
        ad5522.read_pmu_reg_back(channel)
        assert read.call_count == 1


def test_read_dac_reg_x_back(ad5522):
    with mock.patch.object(ad5522.spi_ad5522, 'ad5522_spi_read') as read:
        ad5522.read_dac_reg_x_back(0x01 << 24, "FIN_5uA")
        assert read.call_count == 1


def test_read_dac_reg_m_back(ad5522):
    with mock.patch.object(ad5522.spi_ad5522, 'ad5522_spi_read') as read:
        ad5522.read_dac_reg_m_back(0x01 << 24, "FIN_5uA")
        assert read.call_count == 1


def test_read_dac_reg_c_back(ad5522):
    with mock.patch.object(ad5522.spi_ad5522, 'ad5522_spi_read') as read:
        ad5522.read_dac_reg_c_back(0x01 << 24, "FIN_5uA")
        assert read.call_count == 1


def test_read_sys_reg_back(ad5522):
    with mock.patch.object(ad5522.spi_ad5522, 'ad5522_spi_read') as read:
        ad5522.read_sys_reg_back()
        assert read.call_count == 1


def test_set_system_control(ad5522):
    with mock.patch.object(ad5522.spi_ad5522, 'ad5522_spi_write') as write:
        ad5522.set_system_control(0x123)
        assert write.call_count == 1


def test_set_pmu_control(ad5522):
    with mock.patch.object(ad5522.spi_ad5522, 'ad5522_spi_write') as write:
        ad5522.set_pmu_control(0x01 << 24, 0x123)
        assert write.call_count == 1


# def test_clear_alarm(ad5522):
#     with mock.patch.object(ad5522.spi_ad5522, 'ad5522_spi_write') as write:
#         ad5522.clear_alarm()
#         assert write.call_count == 1


def test_set_clamp_vol(ad5522):
    with mock.patch.object(ad5522.spi_ad5522, 'ad5522_spi_write') as write:
        with mock.patch.object(ad5522, 'set_pmu_control') as write2:
            ad5522.set_clamp_vol(0x01 << 24, 0x123, 0x124)
            assert write.call_count == 2
            assert write2.call_count == 1


def test_set_clamp_curr(ad5522):
    with mock.patch.object(ad5522.spi_ad5522, 'ad5522_spi_write') as write:
        with mock.patch.object(ad5522, 'set_pmu_control') as write2:
            ad5522.set_clamp_curr(0x01 << 24, 0x123, 0x124)
            assert write.call_count == 2
            assert write2.call_count == 1


def test_set_output_vol(ad5522):
    with mock.patch.object(ad5522.spi_ad5522, 'ad5522_spi_write') as write:
        ad5522.set_output_vol(1 << 24, 0x123)
        assert write.call_count == 1


def test_set_output_curr(ad5522):
    with mock.patch.object(ad5522.spi_ad5522, 'ad5522_spi_write') as write:
        with mock.patch.object(ad5522, 'read_pmu_reg_back', return_value=0x7 << 15):
            ad5522.set_output_curr(1 << 24, 0x123)
            assert write.call_count == 1


def test_set_2_MV(ad5522):
    with mock.patch.object(ad5522, 'set_pmu_control'):
        ad5522.set_2_MV([0x01 << 24, 0x01 << 25])
        ad5522.set_2_MV([0x01 << 25])


def test_set_2_MI(ad5522):
    with mock.patch.object(ad5522, 'set_pmu_control'):
        ad5522.set_2_MI([0x01 << 24, 0x01 << 25])
        ad5522.set_2_MI([0x01 << 25])


def test_set_2_FI(ad5522):
    with mock.patch.object(ad5522, 'set_pmu_control'):
        ad5522.set_2_FI([0x01 << 24, 0x01 << 25])
        ad5522.set_2_FI([0x01 << 25])


def test_set_2_FV(ad5522):
    with mock.patch.object(ad5522, 'set_pmu_control'):
        ad5522.set_2_FV([0x01 << 24, 0x01 << 25])
        ad5522.set_2_FV([0x01 << 25])


def test_set_dac_offset_value(ad5522):
    with mock.patch.object(ad5522.spi_ad5522, 'ad5522_spi_write') as write:
        ad5522.set_dac_offset_value(0x8000)


def test_set_current_range(ad5522):
    with mock.patch.object(ad5522, 'set_pmu_control'):
        ad5522.set_current_range([0x01 << 24, 0x01 << 25], 0)
        ad5522.set_current_range([0x01 << 24], 1)


def test_enable_pmu(ad5522):
    with mock.patch.object(ad5522, 'set_pmu_control'):
        ad5522.enable_pmu([0x01 << 24, 0x01 << 25])
        ad5522.enable_pmu([0x01 << 25])


def test_disable_pmu(ad5522):
    with mock.patch.object(ad5522, 'set_pmu_control'):
        ad5522.disable_pmu([0x01 << 24, 0x01 << 25])
        ad5522.disable_pmu([0x01 << 25])


def test_sequence_enable_pmu(ad5522):
    with mock.patch.object(ad5522.spi_ad5522, 'write_cmd_list'):
        ad5522.sequence_enable_pmu(1 << 24, 0)


def test_sequence_disable_pmu(ad5522):
    with mock.patch.object(ad5522.spi_ad5522, 'write_cmd_list'):
        ad5522.sequence_enable_pmu(1 << 24, 0)


def test_disable_chen(ad5522):
    with mock.patch.object(ad5522, 'set_pmu_control'):
        ad5522.enable_pmu([0x01 << 24, 0x01 << 25])
        ad5522.enable_pmu([0x01 << 25])
