# -*- coding: utf-8 -*-

__author__ = 'daining.chen@cygia.com'
__version__ = '0.1'

import pytest
from mock import patch, Mock
from mix.driver.cyg.common.ic.mcp4725 import MCP4725Def, MCP4725Exception, MCP4725


@pytest.fixture(scope="module")
def TESTMCP4725():
    i2c = Mock()
    attrs = {'write.return_value': None}
    i2c.configure_mock(**attrs)
    TESTMCP4725 = MCP4725(i2c, 0x60, 5500)
    return TESTMCP4725


def test_output_volt_dc(TESTMCP4725):
    TESTMCP4725._i2c_bus.read.return_value = [0x80]
    TESTMCP4725.output_volt_dc(3300)
    with pytest.raises(MCP4725Exception, match='Wait eeprom write completed timeout.'):
        TESTMCP4725._i2c_bus.read.return_value = [~0x80]
        TESTMCP4725.output_volt_dc(3300)


def test_fast_output_volt_dc(TESTMCP4725):
    TESTMCP4725.fast_output_volt_dc(3300)
