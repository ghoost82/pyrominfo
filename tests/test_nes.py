#!/usr/bin/env python3
#
# Copyright (C) 2013 Garrett Brown
# See Copyright Notice in rominfo.py

import testutils

import unittest

nes = testutils.loadModule("nes")

class TestNESParser(unittest.TestCase):
    def setUp(self):
        self.nesParser = nes.NESParser()

    def test_nes(self):
        empty = self.nesParser.parse("data/empty")
        self.assertEqual(len(empty), 0)

        props = self.nesParser.parse("data/Metroid.nes")
        self.assertEqual(len(props), 13)
        self.assertEqual(props["platform"], "Nintendo Entertainment System")
        self.assertEqual(props["prg_size"], "128KB")
        self.assertEqual(props["chr_size"], "0KB")
        self.assertEqual(props["mirroring"], "horizontal")
        self.assertEqual(props["battery"], "")
        self.assertEqual(props["trainer"], "")
        self.assertEqual(props["four_screen_vram"], "")
        self.assertEqual(props["vs_system"], "")
        self.assertEqual(props["playchoice_10"], "")
        self.assertEqual(props["header"], "iNES")
        self.assertEqual(props["mapper"], "MMC1")
        self.assertEqual(props["mapper_code"], "001")
        self.assertEqual(props["video_output"], "")

        props = self.nesParser.parse("data/Dancing Blocks (1990)(Sachen)(AS)[p][!][SA-013][NES cart].unf")
        self.assertEqual(len(props), 11)
        self.assertEqual(props["platform"], "Nintendo Entertainment System")
        self.assertEqual(props["header"], "UNIF")
        self.assertEqual(props["prg_size"], "32KB")
        self.assertEqual(props["chr_size"], "8KB")
        self.assertEqual(props["mirroring"], "vertical")
        self.assertEqual(props["battery"], "")
        self.assertEqual(props["trainer"], "")
        self.assertEqual(props["four_screen_vram"], "")
        self.assertEqual(props["mapper"], "UNL-SA-NROM")
        self.assertEqual(props["video_output"], "")
        self.assertEqual(props["title"], "Dancing Blocks (72 pin cart)")

if __name__ == '__main__':
    unittest.main()
