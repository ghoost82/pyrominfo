#!/usr/bin/env python3
#
# Copyright (C) 2013 Garrett Brown
# See Copyright Notice in rominfo.py

import testutils

import unittest

genesis = testutils.loadModule("genesis")

class TestGenesisParser(unittest.TestCase):
    def setUp(self):
        self.genesisParser = genesis.GensisParser()

    def test_genesis(self):
        empty = self.genesisParser.parse("data/empty")
        self.assertEqual(len(empty), 0)

        props = self.genesisParser.parse("data/Sonic the Hedgehog.bin")
        self.assertEqual(len(props), 14)
        self.assertEqual(props["format"], "")
        self.assertEqual(props["console"], "SEGA MEGA DRIVE")
        self.assertEqual(props["copyright"], "(C)SEGA 1991.APR")
        self.assertEqual(props["publisher"], "SEGA")
        self.assertEqual(props["foreign_title"], "SONIC THE               HEDGEHOG")
        self.assertEqual(props["title"], "SONIC THE               HEDGEHOG")
        self.assertEqual(props["classification"], "Game")
        self.assertEqual(props["code"], "00001009")
        self.assertEqual(props["version"], "00")
        self.assertEqual(props["checksum"], "264A")
        self.assertEqual(props["device_codes"], "J")
        self.assertEqual(props["devices"], "3B Joypad")
        self.assertEqual(props["memo"], "")
        self.assertEqual(props["country_codes"], "JUE")

if __name__ == '__main__':
    unittest.main()
