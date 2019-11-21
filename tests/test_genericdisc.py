#!/usr/bin/env python3
#
# Copyright (C) 2013 Garrett Brown
# See Copyright Notice in rominfo.py

import testutils

import unittest

genericdisc = testutils.loadModule("genericdisc")

class TestGenericdiscParser(unittest.TestCase):
    def setUp(self):
        self.genericdiscParser = genericdisc.GenericDiscParser()

    def test_invalid(self):
        empty = self.genericdiscParser.parse("data/empty")
        self.assertEqual(len(empty), 0)

    def test_genericdisc(self):
        props = self.genericdiscParser.parse("data/Dreamkey.gdi")
        self.assertEqual(len(props), 17)
        self.assertEqual(props["platform"], "Generic Disc")
        self.assertEqual(props["standard_id"], "CD001")
        self.assertEqual(props["system_id"], "SEGA SEGAKATANA")
        self.assertEqual(props["volume_id"], "DREAMKEY3")
        self.assertEqual(props["set_info"], "1/1")
        self.assertEqual(props["volume_set_id"], "DREAMKEY3")
        self.assertEqual(props["publisher_id"], "SEGA CORPORATION")
        self.assertEqual(props["data_preparer_id"], "CRI CD CRAFT VER.2.30")
        self.assertEqual(props["application_id"], "")
        self.assertEqual(props["copyright_file_id"], "COPYRIGH.TXT")
        self.assertEqual(props["abstract_file_id"], "ABSTRACT.TXT")
        self.assertEqual(props["bibliographic_file_id"], "BIBLIOGR.TXT")
        self.assertEqual(props["creation_date_code"], "2001122406043000")
        self.assertEqual(props["modification_date_code"], "2001122406043000")
        self.assertEqual(props["expiration_date_code"], "0000000000000000")
        self.assertEqual(props["effective_date_code"], "0000000000000000")
        self.assertEqual(props["tracks"], [{'index': 1, 'mode': 1, 'filename': 'data/Dreamkey-1.bin', 'sector_size': 2352, 'offset': 0}, {'index': 2, 'mode': 0, 'filename': 'data/Dreamkey-2.bin', 'sector_size': 2352, 'offset': 0}, {'index': 3, 'mode': 1, 'filename': 'data/Dreamkey-3.bin', 'sector_size': 2352, 'offset': 0}])

    def test_genericdisc_iso(self):
        props = self.genericdiscParser.parse("data/Road Avenger.iso")
        self.assertEqual(len(props), 17)
        self.assertEqual(props["platform"], "Generic Disc")
        self.assertEqual(props["standard_id"], "CD001")
        self.assertEqual(props["system_id"], "SEGA_CD")
        self.assertEqual(props["volume_id"], "ROAD_AVENGER_CD")
        self.assertEqual(props["set_info"], "1/1")
        self.assertEqual(props["volume_set_id"], "ROAD_AVENGER_CD")
        self.assertEqual(props["publisher_id"], "WOLF_TEAM")
        self.assertEqual(props["data_preparer_id"], "WOLF_TEAM")
        self.assertEqual(props["application_id"], "")
        self.assertEqual(props["copyright_file_id"], "CPY.TXT")
        self.assertEqual(props["abstract_file_id"], "ABS.TXT")
        self.assertEqual(props["bibliographic_file_id"], "BIB.TXT")
        self.assertEqual(props["creation_date_code"], "1993020101483200")
        self.assertEqual(props["modification_date_code"], "1993020101483200")
        self.assertEqual(props["expiration_date_code"], "0000000000000000")
        self.assertEqual(props["effective_date_code"], "0000000000000000")
        self.assertEqual(props["tracks"], [{'filename': 'data/Road Avenger.iso', 'mode': 1, 'sector_size': 2048, 'index': 0, 'offset': 0}])

    def test_genericdisc_raw(self):
        props = self.genericdiscParser.parse("data/metal_gear_solid_(v1.1)_(disc_1).bin")
        self.assertEqual(len(props), 17)
        self.assertEqual(props["platform"], "Generic Disc")
        self.assertEqual(props["standard_id"], "CD001")
        self.assertEqual(props["system_id"], "PLAYSTATION")
        self.assertEqual(props["volume_id"], "")
        self.assertEqual(props["set_info"], "1/1")
        self.assertEqual(props["volume_set_id"], "")
        self.assertEqual(props["publisher_id"], "")
        self.assertEqual(props["data_preparer_id"], "")
        self.assertEqual(props["application_id"], "PLAYSTATION")
        self.assertEqual(props["copyright_file_id"], "")
        self.assertEqual(props["abstract_file_id"], "")
        self.assertEqual(props["bibliographic_file_id"], "")
        self.assertEqual(props["creation_date_code"], "1998090914333600$")
        self.assertEqual(props["modification_date_code"], "0000000000000000")
        self.assertEqual(props["expiration_date_code"], "0000000000000000")
        self.assertEqual(props["effective_date_code"], "0000000000000000")
        self.assertEqual(props["tracks"], [{'filename': 'data/metal_gear_solid_(v1.1)_(disc_1).bin', 'mode': 2, 'sector_size': 2352, 'index': 0, 'offset': 0}])

        props = self.genericdiscParser.parse("data/Virtua Fighter CG Portrait Collection-1.bin")
        self.assertEqual(len(props), 17)
        self.assertEqual(props["platform"], "Generic Disc")
        self.assertEqual(props["standard_id"], "CD001")
        self.assertEqual(props["system_id"], "")
        self.assertEqual(props["volume_id"], "")
        self.assertEqual(props["set_info"], "1/1")
        self.assertEqual(props["volume_set_id"], "")
        self.assertEqual(props["publisher_id"], "")
        self.assertEqual(props["data_preparer_id"], "")
        self.assertEqual(props["application_id"], "")
        self.assertEqual(props["copyright_file_id"], "")
        self.assertEqual(props["abstract_file_id"], "")
        self.assertEqual(props["bibliographic_file_id"], "")
        self.assertEqual(props["creation_date_code"], "1995080414073800")
        self.assertEqual(props["modification_date_code"], "1995080414073800")
        self.assertEqual(props["expiration_date_code"], "0000000000000000")
        self.assertEqual(props["effective_date_code"], "0000000000000000")
        self.assertEqual(props["tracks"], [{'filename': 'data/Virtua Fighter CG Portrait Collection-1.bin', 'mode': 1, 'sector_size': 2352, 'index': 0, 'offset': 0}])

if __name__ == '__main__':
    unittest.main()
