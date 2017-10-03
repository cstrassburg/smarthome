#!/usr/bin/env python3
# vim: set encoding=utf-8 tabstop=4 softtabstop=4 shiftwidth=4 expandtab
#########################################################################
# Copyright 2017-       Martin Sinn                         m.sinn@gmx.de
#########################################################################
#  This file is part of SmartHomeNG
#  https://github.com/smarthomeNG/smarthome
#  http://knx-user-forum.de/
#
#  SmartHomeNG is free software: you can redistribute it and/or modify
#  it under the terms of the GNU General Public License as published by
#  the Free Software Foundation, either version 3 of the License, or
#  (at your option) any later version.
#
#  SmartHomeNG is distributed in the hope that it will be useful,
#  but WITHOUT ANY WARRANTY; without even the implied warranty of
#  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#  GNU General Public License for more details.
#
#  You should have received a copy of the GNU General Public License
#  along with SmartHomeNG If not, see <http://www.gnu.org/licenses/>.
#########################################################################

import common
import unittest
import logging
import shutil

from lib.model.smartplugin import SmartPlugin
#from lib.logic import Logics          # für update der /etc/logic.yaml
import lib.logic

from tests.mock.core import MockSmartHome


logger = logging.getLogger(__name__)

class TestLogics(unittest.TestCase):

    def test_00_begin(self):
        logger.warning('')
        logger.warning('=== Begin Logic Tests:')
        shutil.copy2(self.sh._logic_conf_basename+'.yaml.orig', self.sh._logic_conf_basename+'.yaml')


    def test_99_end(self):    
        logger.warning('')
        logger.warning('=== End Logic Tests')


    def setUp(self):
        logger.warning('')
        self.sh = MockSmartHome()


    def test_01_defined_logics(self):
        
        logger.warning('----- Logic Test: test_01_defined_logics')
        self._logics = lib.logic.Logics(self.sh, self.sh._logic_conf_basename, self.sh._env_logic_conf_basename)
        logger.warning("Defined logics = {}".format( str(lib.logic.Logics.return_defined_logics()) ))
        
        # Trest defined logics
        self.assertTrue('logic1' in lib.logic.Logics.return_defined_logics())
        self.assertTrue('logic2' in lib.logic.Logics.return_defined_logics())
        self.assertTrue('logic3' in lib.logic.Logics.return_defined_logics())


    def test_02_loaded_logics(self):
        
        logger.warning('----- Logic Test: test_02_loaded_logics')
        self._logics = lib.logic.Logics(self.sh, self.sh._logic_conf_basename, self.sh._env_logic_conf_basename)
        logger.warning("Loaded logics = {}".format( str(lib.logic.Logics.return_loaded_logics()) ))
        
        # Test loaded logics
        self.assertFalse('logic1' in lib.logic.Logics.return_loaded_logics())
        self.assertTrue('logic2' in lib.logic.Logics.return_loaded_logics())
        self.assertTrue('logic3' in lib.logic.Logics.return_loaded_logics())
        # test loaded system logics
        self.assertTrue('env_init' in lib.logic.Logics.return_loaded_logics())
        self.assertTrue('env_daily' in lib.logic.Logics.return_loaded_logics())
        self.assertTrue('env_loc' in lib.logic.Logics.return_loaded_logics())
        self.assertTrue('env_stat' in lib.logic.Logics.return_loaded_logics())


    def test_03_return_logictype(self):
    
        logger.warning('----- Logic Test: test_03_return_logictype')
        self._logics = lib.logic.Logics(self.sh, self.sh._logic_conf_basename, self.sh._env_logic_conf_basename)
        
        self.assertEqual(lib.logic.Logics.return_logictype('logic1'),'None')
        self.assertEqual(lib.logic.Logics.return_logictype('logic2'),'Python')
        self.assertEqual(lib.logic.Logics.return_logictype('logic3'),'Blockly')


    def test_04_unload_logic(self):

        logger.warning('----- Logic Test: 04_test_unload_logic')
        self.assertTrue('logic2' in lib.logic.Logics.return_loaded_logics())
        self.assertTrue(lib.logic.Logics.unload_logic('logic2'))
        self.assertFalse(lib.logic.Logics.unload_logic('logic2'))     # trying to unload a not loaded logic shoul return false
        

    def test_05_load_logic(self):

        logger.warning('----- Logic Test: 05_test_load_logic')
        self.assertFalse('logic2' in lib.logic.Logics.return_loaded_logics())
        self.assertTrue(lib.logic.Logics.load_logic('logic2'))
        self.assertTrue(lib.logic.Logics.load_logic('logic2'))   # A loaded Logic can be reloaded this way (it is unloaded first)
        

    def test_06_update_and_read_section(self):

        logger.warning('----- Logic Test: test_06_update_and_read_section')
        fn = ['filename','logic_up.py','Test for section update']
        ct = ['crontab','init = Init','Execute at initialization']
        wi = ['watchitem', ['beleuchtung.automatik_wuerfel.onoff', 'fenster.bad.fenster_nord'], ['Ausführen wenn sich der Würfel ändert', 'Ausführen wenn das Fenster sich ändert']] 
        lib.logic.Logics.update_config_section(True, 'logic_up', [ fn, ct, wi ])
        readback = lib.logic.Logics.read_config_section('logic_up')
#        logger.warning("read_config_section('logic_up') = {}".format(str(readback) ))
        fnb = readback[0]
        ctb = readback[1]
        wib = readback[2]
        self.assertEqual(fn,fnb)
        self.assertEqual(ct,ctb)
        self.assertEqual(wi,wib)
        self.assertEqual(len(readback),3)

        logger.info('----- Logic Test: test_06_update_and_read_section - test2')
        # Test: hand lists as strings to update function
        fn = ['filename','logic_up2.py','Test for section update']
        ct = ['crontab','init = Init','Execute at initialization']
        wi = ['watchitem', ['beleuchtung.automatik_wuerfel.offon', 'fenster.bad.fenster_sued'], ['Ausführen wenn sich der Würfel ändert', 'Ausführen wenn das Fenster sich ändert']] 
        wis = [wi[0], str(wi[1]), str(wi[2])] 
        lib.logic.Logics.update_config_section(True, 'logic_up2', [ fn, ct, wis ])
        readback = lib.logic.Logics.read_config_section('logic_up2')
#        logger.warning("read_config_section('logic_up2') = {}".format(str(readback) ))
        fnb = readback[0]
        ctb = readback[1]
        wib = readback[2]
        self.assertEqual(fn,fnb)
        self.assertEqual(ct,ctb)
        self.assertEqual(wi,wib)
        self.assertEqual(len(readback),3)

        logger.info('----- Logic Test: test_06_update_and_read_section - test3')
        # Test: read non-existing section
        readback = lib.logic.Logics.read_config_section('logic_up3')
#        logger.warning("read_config_section('logic_up3') = {}".format(str(readback) ))
        self.assertEqual(len(readback),0)


if __name__ == '__main__':
    unittest.main(verbosity=2)
