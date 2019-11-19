# Copyright (C) 2015 Jan Holthuis
# See Copyright Notice in rominfo.py

from .rominfo import RomInfoParser

# Regions are the same across SEGA Systems
from .genesis import sega_regions

class DreamcastParser(RomInfoParser):
    """
    Parse a Dreamcast image. Valid extensions are cdi, gdi, cue.
    This parser is derived from:
    * https://gist.github.com/Holzhaus/ae3dacf6a2e83dd00421
    * https://github.com/Nold360/mksdiso/tree/master/src/cdirip
    Other related documentation and source code:
    * GD-ROM Format Basic Specifications Ver. 2.14 by Sega Enterprises, Ltd.
    * http://thekickback.com/dreamcast/GD-ROM%20Format%20Basic%20Specifications%20v2.14.pdf
    * Image reader code of the reicast-emulator project:
    * https://github.com/reicast/reicast-emulator/tree/master/core/imgread
    * IP0000.BIN documentation:
    * https://www.dropbox.com/s/ithnw69wy3ciuzn/IP0000.BIN.txt
    """

    def getValidExtensions(self):
        # TODO: Add chd support
        return ["cdi", "gdi", "cue"]

    def parse(self, filename):
        props = {}

        ext = self._getExtension(filename)

        if ext == "cdi":
            binary_track = -1
        else:
            binary_track = 2

        tracks = self._getDiscTracks(filename)

        if tracks:
            filename = tracks[binary_track]["filename"]

        with open(filename, "rb") as f:
            # read first 17 sectors of disc image and convert it if neccessary
            f.seek(tracks[binary_track]["offset"])
            data = bytearray(f.read(17 * 2352))

            # Try to convert raw CD images
            if tracks != None and tracks[binary_track]["sector_size"] != 2048:
                data = self._convertRawToUser(data, tracks[binary_track]["sector_size"], tracks[binary_track]["mode"])

            if self.isValidData(data):
                props = self.parseBuffer(data)
                if tracks != None:
                    props["tracks"] = tracks
        return props

    def isValidData(self, data):
        if data[0x0 : 0x0 + 15] == b"SEGA SEGAKATANA":
            return True
        return False


    def parseBuffer(self, data):
        # See SEGA's GD-ROM Format Basic Specifications Ver. 2.13, p. 13 for
        # details.
        props = {}
        props["platform"] = "Dreamcast"

        props["hardware_id"] = self._sanitize(data[0x00 : 0x00 + 16])

        props["hardware_vendor_id"] = self._sanitize(data[0x10 : 0x10 + 16])

        props["media_id"] = self._sanitize(data[0x20 : 0x20 + 5])

        props["media_info_code"] = self._sanitize(data[0x25 : 0x25 + 11])
        props["media_info"] = "/".join( props["media_info_code"][6:].split("/"))

        props["region_code"] = self._sanitize(data[0x30 : 0x30 + 8])
        props["region"] = ", ".join([sega_regions.get(d) for d in props["region_code"] \
                                                             if d in sega_regions])

        props["compatible_peripherals_code"] = self._sanitize(data[0x38 : 0x38 + 8])
        peripherals = []
        for p_code, p_desc in list(dc_peripherals.items()):
            if int(props["compatible_peripherals_code"], 16) & p_code == p_code:
                peripherals.append(p_desc)
        props["compatible_peripherals"] = ", ".join(peripherals)

        props["product_id"] = self._sanitize(data[0x40 : 0x40 + 10])

        props["product_version"] = self._sanitize(data[0x4a : 0x4a + 6])

        props["release_date_code"] = self._sanitize(data[0x50 : 0x50 + 8])

        props["bootfile"] = self._sanitize(data[0x60 : 0x60 + 12])

        props["publisher"] = self._sanitize(data[0x70 : 0x70 + 16])

        props["game_title"] = self._sanitize(data[0x80 : 0x80 + 96])

        return props

RomInfoParser.registerParser(DreamcastParser())


dc_peripherals = {
    0b0000000000000000000000000001: "Uses Windows CE",
    0b0000000000000000000000010000: "VGA box support",
    # Expansion units
    0b0000000000000000000100000000: "Other expansions",
    0b0000000000000000001000000000: "Puru Puru pack",
    0b0000000000000000010000000000: "Mike device",
    0b0000000000000000100000000000: "Memory card",
    # Required peripherals
    0b0000000000000001000000000000: "Start/A/B/Directions",
    0b0000000000000010000000000000: "C button",
    0b0000000000000100000000000000: "D button",
    0b0000000000001000000000000000: "X button",
    0b0000000000010000000000000000: "Y button",
    0b0000000000100000000000000000: "Z button",
    0b0000000001000000000000000000: "Expanded direction buttons",
    0b0000000010000000000000000000: "Analog R trigger",
    0b0000000100000000000000000000: "Analog L trigger",
    0b0000001000000000000000000000: "Analog horizontal controller",
    0b0000010000000000000000000000: "Analog vertical controller",
    0b0000100000000000000000000000: "Expanded analog horizontal",
    0b0001000000000000000000000000: "Expanded analog vertical",
    # Optional peripherals
    0b0010000000000000000000000000: "Gun",
    0b0100000000000000000000000000: "Keyboard",
    0b1000000000000000000000000000: "Mouse",
}
