# -*- coding: utf-8 -*-
import pytest
import mock
from mock import patch, Mock
from mix.driver.cyg.common.ipcore.mix_smu_lite_cyg import MIX_SMU_Lite_CYG

__author__ = 'daining.chen@cygia.com'
__version__ = '0.1'


@pytest.fixture(scope="module")
def MIX_SMU_LITE_CYG():
    axi4_bus = "/dev/mix_hercules_cyg"
    ip_path = "mix.driver.cyg.common.ipcore.mix_smu_lite_cyg."
    with mock.patch(ip_path + "AXI4LiteBus"):
        ip = MIX_SMU_Lite_CYG(axi4_bus)
        ip.axi4_bus = mock.Mock()
    return ip


def test_get_ip_time(MIX_SMU_LITE_CYG):
    with mock.patch.object(MIX_SMU_LITE_CYG.axi4_bus, 'read_32bit_fix'):
        MIX_SMU_LITE_CYG.get_ip_time()


def test_reset(MIX_SMU_LITE_CYG):
    with mock.patch.object(MIX_SMU_LITE_CYG.axi4_bus, 'write_32bit_fix'):
        MIX_SMU_LITE_CYG.reset()


def test_enable_choose_spi(MIX_SMU_LITE_CYG):
    with mock.patch.object(MIX_SMU_LITE_CYG.axi4_bus, 'read_32bit_fix', return_value=[1]):
        with mock.patch.object(MIX_SMU_LITE_CYG.axi4_bus, 'write_32bit_fix'):
            MIX_SMU_LITE_CYG.enable_choose_spi(1)


def test_reset_ad5522(MIX_SMU_LITE_CYG):
    with mock.patch.object(MIX_SMU_LITE_CYG.axi4_bus, 'write_32bit_fix'):
        assert MIX_SMU_LITE_CYG.reset_ad5522() == 'done'


def test_set_ADA4870_pin(MIX_SMU_LITE_CYG):
    with mock.patch.object(MIX_SMU_LITE_CYG.axi4_bus, 'read_32bit_fix', return_value=[0x8]):
        assert MIX_SMU_LITE_CYG.set_ADA4870_pin(1) == 'done'


def test_set_LOAD_pin(MIX_SMU_LITE_CYG):
    with mock.patch.object(MIX_SMU_LITE_CYG.axi4_bus, 'read_32bit_fix', return_value=[0]):
        with mock.patch.object(MIX_SMU_LITE_CYG.axi4_bus, 'write_32bit_fix'):
            assert MIX_SMU_LITE_CYG.set_LOAD_pin(1) == 'done'


def test_get_spi_status(MIX_SMU_LITE_CYG):
    with mock.patch.object(MIX_SMU_LITE_CYG.axi4_bus, 'read_32bit_fix'):
        MIX_SMU_LITE_CYG.get_spi_status()


def test_ad5522_spi_write(MIX_SMU_LITE_CYG):
    with mock.patch.object(MIX_SMU_LITE_CYG.axi4_bus, 'write_32bit_fix'):
        MIX_SMU_LITE_CYG.ad5522_spi_write(0xffff)


def test_ad5522_spi_read(MIX_SMU_LITE_CYG):
    with mock.patch.object(MIX_SMU_LITE_CYG.axi4_bus, 'read_32bit_fix'):
        MIX_SMU_LITE_CYG.ad5522_spi_read(0xffff)


def test_enable_cmd_list_send(MIX_SMU_LITE_CYG):
    with mock.patch.object(MIX_SMU_LITE_CYG.axi4_bus, 'write_32bit_fix'):
        MIX_SMU_LITE_CYG.enable_cmd_list_send(1)


def test_get_cmd_list_send_status(MIX_SMU_LITE_CYG):
    with mock.patch.object(MIX_SMU_LITE_CYG.axi4_bus, 'read_32bit_fix'):
        MIX_SMU_LITE_CYG.get_cmd_list_send_status()


def test_write_cmd_list(MIX_SMU_LITE_CYG):
    with mock.patch.object(MIX_SMU_LITE_CYG.axi4_bus, 'write_32bit_fix'):
        MIX_SMU_LITE_CYG.write_cmd_list(0, 0, 0)
