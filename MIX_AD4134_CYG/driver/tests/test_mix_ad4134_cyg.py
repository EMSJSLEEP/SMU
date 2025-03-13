# -*- coding: utf-8 -*-
import pytest
import mock
from mix.driver.cyg.common.ipcore.mix_ad4134_cyg import MIXAD4134CYGDef, MIXAD4134CYGException, MIXAD4134CYG

@pytest.fixture(scope="module")
def MIX_AD4134_CYG():
    axi4_bus = "/dev/mix_hercules_cyg"
    ip_path = "mix.driver.cyg.common.ipcore.mix_ad4134_cyg."
    with mock.patch(ip_path + "AXI4LiteBus"):
        ip = MIXAD4134CYG(axi4_bus)
        ip.axi4_bus = mock.Mock()
    return ip

def test_reset(MIX_AD4134_CYG):
    with mock.patch.object(MIX_AD4134_CYG.axi4_bus, 'read_16bit_fix'):
        with mock.patch.object(MIX_AD4134_CYG.axi4_bus, 'write_16bit_fix'):
            MIX_AD4134_CYG.reset()

def test_get_reset_status(MIX_AD4134_CYG):
    with mock.patch.object(MIX_AD4134_CYG.axi4_bus, 'read_16bit_fix'):
        MIX_AD4134_CYG.get_reset_status()

def test_get_transfer_mode(MIX_AD4134_CYG):
    with mock.patch.object(MIX_AD4134_CYG.axi4_bus, 'read_16bit_fix'):
        with mock.patch.object(MIX_AD4134_CYG.axi4_bus, 'write_16bit_fix'):
            MIX_AD4134_CYG.get_transfer_mode()

def test_set_transfer_mode(MIX_AD4134_CYG):
    with mock.patch.object(MIX_AD4134_CYG.axi4_bus, 'read_16bit_fix'):
        with mock.patch.object(MIX_AD4134_CYG.axi4_bus, 'write_16bit_fix'):
            MIX_AD4134_CYG.set_transfer_mode('lite')
            MIX_AD4134_CYG.set_transfer_mode('stream')
            MIX_AD4134_CYG.set_transfer_mode('all')

def test_set_data_frame(MIX_AD4134_CYG):
    with mock.patch.object(MIX_AD4134_CYG.axi4_bus, 'read_16bit_fix'):
        with mock.patch.object(MIX_AD4134_CYG.axi4_bus, 'write_16bit_fix'):
            MIX_AD4134_CYG.set_data_frame(0)

def test_get_data_frame_format(MIX_AD4134_CYG):
    with mock.patch.object(MIX_AD4134_CYG.axi4_bus, 'read_16bit_fix'):
        with mock.patch.object(MIX_AD4134_CYG.axi4_bus, 'write_16bit_fix'):
            MIX_AD4134_CYG.get_data_frame_format()

def test_set_ip_channel_format(MIX_AD4134_CYG):
    with mock.patch.object(MIX_AD4134_CYG.axi4_bus, 'read_16bit_fix'):
        with mock.patch.object(MIX_AD4134_CYG.axi4_bus, 'write_16bit_fix'):
            MIX_AD4134_CYG.set_ip_channel_format(1)

def test_get_channel_format(MIX_AD4134_CYG):
    with mock.patch.object(MIX_AD4134_CYG.axi4_bus, 'read_16bit_fix'):
        with mock.patch.object(MIX_AD4134_CYG.axi4_bus, 'write_16bit_fix'):
            MIX_AD4134_CYG.get_channel_format()

def test_get_spi_transfer_status(MIX_AD4134_CYG):
    with mock.patch.object(MIX_AD4134_CYG.axi4_bus, 'read_16bit_fix'):
        with mock.patch.object(MIX_AD4134_CYG.axi4_bus, 'write_16bit_fix'):
            MIX_AD4134_CYG.get_spi_transfer_status()

def test_spi_write(MIX_AD4134_CYG):
    with mock.patch.object(MIX_AD4134_CYG.axi4_bus, 'write_32bit_fix'):
        with mock.patch.object(MIX_AD4134_CYG, 'get_spi_transfer_status', return_value=False):
            with pytest.raises(MIXAD4134CYGException, match='time out for spi write'):
                MIX_AD4134_CYG.spi_write(0, 0xff)

def test_spi_read(MIX_AD4134_CYG):
    with mock.patch.object(MIX_AD4134_CYG.axi4_bus, 'write_32bit_fix'):
        with mock.patch.object(MIX_AD4134_CYG.axi4_bus, 'read_32bit_fix'):
            with mock.patch.object(MIX_AD4134_CYG, 'get_spi_transfer_status', return_value=False):
                with pytest.raises(MIXAD4134CYGException, match='time out while spi writing before read'):
                    MIX_AD4134_CYG.spi_read(0xf)

def test_set_channels_dig_filter(MIX_AD4134_CYG):
    with mock.patch.object(MIX_AD4134_CYG, 'spi_write'):
        MIX_AD4134_CYG.set_channels_dig_filter([0, 0, 0, 0])

def test_get_channels_dig_filter(MIX_AD4134_CYG):
    with mock.patch.object(MIX_AD4134_CYG, 'spi_read', return_value=0):
        MIX_AD4134_CYG.get_channels_dig_filter()

def test_set_channels_packet_config(MIX_AD4134_CYG):
    with mock.patch.object(MIX_AD4134_CYG.axi4_bus, 'read_16bit_fix'):
        with mock.patch.object(MIX_AD4134_CYG.axi4_bus, 'write_16bit_fix'):
            with mock.patch.object(MIX_AD4134_CYG, 'spi_write'):
                MIX_AD4134_CYG.set_channels_packet_config(2, 0, 1, 0)

def test_get_channels_packet_config(MIX_AD4134_CYG):
    with mock.patch.object(MIX_AD4134_CYG, 'spi_read', return_value=0):
        MIX_AD4134_CYG.get_channels_packet_config()

def test_set_ad4134_power_mode(MIX_AD4134_CYG):
    with mock.patch.object(MIX_AD4134_CYG, 'spi_read', return_value=0):
        with mock.patch.object(MIX_AD4134_CYG, 'spi_write'):
            MIX_AD4134_CYG.set_ad4134_power_mode("fast")
            MIX_AD4134_CYG.set_ad4134_power_mode("slow")

def test_set_ad4134_parallel_output(MIX_AD4134_CYG):
    with mock.patch.object(MIX_AD4134_CYG, 'spi_read', return_value=0):
        with mock.patch.object(MIX_AD4134_CYG, 'spi_write'):
            MIX_AD4134_CYG.set_ad4134_parallel_output()
            MIX_AD4134_CYG.set_ad4134_parallel_output()

def test_set_ad4134_odr(MIX_AD4134_CYG):
    with mock.patch.object(MIX_AD4134_CYG, 'spi_read', return_value=0):
        with mock.patch.object(MIX_AD4134_CYG, 'spi_write'):
            MIX_AD4134_CYG.set_ad4134_odr(1496)
            MIX_AD4134_CYG.set_ad4134_odr(200)

def test_set_measure_count(MIX_AD4134_CYG):
    with mock.patch.object(MIX_AD4134_CYG, 'spi_read', return_value=0):
        with mock.patch.object(MIX_AD4134_CYG, 'spi_write'):
            MIX_AD4134_CYG.set_measure_count(10)
            MIX_AD4134_CYG.set_measure_count(200)

def test_measure(MIX_AD4134_CYG):
    with mock.patch.object(MIX_AD4134_CYG, 'set_measure_count', return_value=0):
        with mock.patch.object(MIX_AD4134_CYG, 'get_spi_transfer_status', return_value=True):
            with mock.patch.object(MIX_AD4134_CYG, 'decode_measurement', return_value=0):
                MIX_AD4134_CYG.measure(['ch0'], 10)

def test_axi_read(MIX_AD4134_CYG):
    with mock.patch.object(MIX_AD4134_CYG.axi4_bus, 'read_32bit_fix'):
        MIX_AD4134_CYG.axi_read(0xf)

def test_axi_write(MIX_AD4134_CYG):
    with mock.patch.object(MIX_AD4134_CYG.axi4_bus, 'write_32bit_fix'):
        MIX_AD4134_CYG.axi_write(0xf, 2)
