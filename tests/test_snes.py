#!/usr/bin/env python3
#
# Copyright (C) 2013 Garrett Brown
# See Copyright Notice in rominfo.py

import testutils

import unittest

snes = testutils.loadModule("snes")

class TestSNESParser(unittest.TestCase):
    def setUp(self):
        self.snesParser = snes.SNESParser()

    def test_snes(self):
        empty = self.snesParser.parse("data/empty")
        self.assertEqual(len(empty), 0)

        props = self.snesParser.parse("data/Super Mario World.smc")
        self.assertEqual(len(props), 15)
        self.assertEqual(props["header"], "")
        self.assertEqual(props["title"], "SUPER MARIOWORLD")
        self.assertEqual(props["code"], "")
        self.assertEqual(props["memory_layout"], "LoROM")
        self.assertEqual(props["rom_speed"], "SlowROM")
        self.assertEqual(props["cartridge_type"], "ROM+RAM+BATT")
        self.assertEqual(props["rom_size"], "4 Mbit")
        self.assertEqual(props["ram_size"], "16 Kbit")
        self.assertEqual(props["region"], "USA/Canada")
        self.assertEqual(props["video_output"], "NTSC")
        self.assertEqual(props["publisher"], "Nintendo")
        self.assertEqual(props["publisher_code"], "0001")
        self.assertEqual(props["version"], "00")
        self.assertEqual(props["checksum"], "A0DA")
        self.assertEqual(props["checksum_complement"], "5F25")
        

if __name__ == '__main__':
    unittest.main()
