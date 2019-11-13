# Copyright (C) 2013 Garrett Brown
# See Copyright Notice in rominfo.py

from .rominfo import RomInfoParser

class NESParser(RomInfoParser):
    """
    Parse a NES image. Valid extensions are nes, nez, unf, unif.
    NES file format documentation and related source code:
    * http://nesdev.com/neshdr20.txt
    * http://wiki.nesdev.com/w/index.php/INES
    * http://codef00.com/unif_cur.txt
    * nes_slot.c of the MAME project:
    * http://git.redump.net/mame/tree/src/mess/machine/nes_slot.c
    * https://github.com/TASVideos/fceux
    """

    def getValidExtensions(self):
        return ["nes", "nez", "unf", "unif"]

    def parse(self, filename):
        props = {}
        with open(filename, "rb") as f:
            ext = self._getExtension(filename)
            if ext in ["unf", "unif"]:
                data = bytearray(f.read())
            else:
                data = bytearray(f.read(16))
            if self.isValidData(data):
                props = self.parseBuffer(data)
        return props

    def isValidData(self, data):
        """
        Test for a valid NES image by checking the first 4 bytes for a UNIF or
        iNES header ("NES" followed by MS-DOS end-of-file). FDS headers
        ("FDS\x1a") are not supported, as they contain no useful information.
        """
        return data[:4] == b"NES\x1a" or data[:4] == b"UNIF"

    def parseBuffer(self, data):
        props = {}

        props["platform"] = "Nintendo Entertainment System"

        if data[:4] == b"NES\x1a":
            # 04 - PRG ROM size
            props["prg_size"] = "%dKB" % (data[0x04] * 16)

            # 05 - CHR ROM size
            props["chr_size"] = "%dKB" % (data[0x05] * 8)
            
            # 06 - First ROM option byte
            # 76543210
            # |||||||+- Mirroring: 0: horizontal / 1: vertical
            # ||||||+-- 1: Cartridge contains battery
            # |||||+--- 1: ROM contains trainer
            # ||||+---- 1: ROM provide four-screen VRAM
            # ++++----- Lower nybble of mapper number
            props["mirroring"] = "vertical" if data[0x06] & 0x01 else "horizontal"
            props["battery"] = "yes" if data[0x06] & 0x02 else ""
            props["trainer"] = "yes" if data[0x06] & 0x04 else ""
            props["four_screen_vram"] = "yes" if data[0x06] & 0x08 else ""

            # 07 - Second ROM option byte
            # 76543210
            # |||||||+- VS System
            # ||||||+-- PlayChoice-10
            # ||||++--- If equal to 2, flags 8-15 are in NES 2.0 format
            # ++++----- Upper nybble of mapper number
            props["vs_system"] = "yes" if data[0x07] & 0x01 else ""
            props["playchoice_10"] = "yes" if data[0x07] & 0x02 else ""
            ines2 = (data[0x07] & 0x0c == 0x8)
            props["header"] = "NES 2.0" if ines2 else "iNES"
            #props["mapper_id"] = (data[0x07] & 0xf0) + (data[0x06] >> 4)
            mapper = (data[0x07] & 0xf0) + (data[0x06] >> 4)
            props["mapper"] = ines_mappers.get(mapper, "")
            props["mapper_code"] = ("%03d" % mapper) if mapper != -1 else ""


            # 0C - iNES 2.0 headers can specify TV system. If the second bit is set
            #      (data[0x0c] & 0x2) then the ROM works with both PAL and NTSC machines.
            #
            # iNES 1.0 doesn't store video information. FCEU-Next compensates by matching
            # the following PAL country tags in filenames:
            #     (E), (F), (G), (I), (Europe), (Australia), (France), (Germany),
            #     (Sweden), (En, Fr, De), (Italy)
            # See https://github.com/libretro/fceu-next/blob/master/src-fceux/ines.cpp
            props["video_output"] = ("PAL" if data[0x0c] & 0x1 else "NTSC") if ines2 else ""

        elif data[:4] == b"UNIF":
            props["header"] = "UNIF"

            # Set defaults to be overridden in our chunked reads later
            props["prg_size"] = ""
            props["chr_size"] = ""
            props["mirroring"] = ""
            props["battery"] = ""
            props["trainer"] = ""
            props["four_screen_vram"] = ""
            props["mapper"] = ""
            props["video_output"] = ""
            props["title"] = ""

            # Skip the UNIF header (0x20 / 32 bytes) and continue with chunked reads
            data = data[0x20 : ]
            while len(data) > 8:
                size = 0
                sizestr = data[4:8]
                if len(sizestr) == 4:
                    size = sizestr[0] | (sizestr[1] << 8) | (sizestr[2] << 16) | (sizestr[3] << 24)
                if size == 0:
                    continue

                ID = self._sanitize(data[ : 4])
                chunk = data[8 : 8 + size]
                data = data[8 + size : ] # Fast-forward past chunk's data

                if ID == "MAPR":
                    props["mapper"] = self._sanitize(chunk)
                elif ID == "PRG0":
                    props["prg_size"] = "%dKB" % (len(chunk) / 1024)
                elif ID == "CHR0":
                    props["chr_size"] = "%dKB" % (len(chunk) / 1024)
                elif ID == "NAME":
                    props["title"] = self._sanitize(chunk)
                elif ID == "TVCI":
                    props["video_output"] = "NTSC" if chunk[0] == 0x00 else "PAL" if chunk[0] == 0x01 else ""
                elif ID == "BATR":
                    props["battery"] = "yes"
                elif ID == "MIRR":
                    if chunk[0] == 0x01:
                        props["mirroring"] = "vertical"
                    elif chunk[0] == 0x02:
                        props["mirroring"] = "horizontal"
                    elif chunk[0] == 0x04:
                        props["four_screen_vram"] = "yes"

        return props

RomInfoParser.registerParser(NESParser())

# Source FCEUX
ines_mappers = {
    0: "NROM",
    1: "MMC1",
    2: "UNROM",
    3: "CNROM",
    4: "MMC3",
    5: "MMC5",
    6: "FFE Rev. A",
    7: "ANROM",
    9: "MMC2",
    10: "MMC4",
    11: "Color Dreams",
    12: "REX DBZ 5",
    13: "CPROM",
    14: "REX SL-1632",
    15: "100-in-1",
    16: "BANDAI 24C02",
    17: "FFE Rev. B",
    18: "JALECO SS880006",
    19: "Namcot 106",
    21: "Konami VRC2/VRC4 A",
    22: "Konami VRC2/VRC4 B",
    23: "Konami VRC2/VRC4 C",
    24: "Konami VRC6 Rev. A",
    25: "Konami VRC2/VRC4 D",
    26: "Konami VRC6 Rev. B",
    27: "CC-21 MI HUN CHE",
    29: "RET-CUFROM",
    30: "UNROM 512",
    31: "infiniteneslives-NSF",
    32: "IREM G-101",
    33: "TC0190FMC/TC0350FMR",
    34: "IREM I-IM/BNROM",
    35: "Wario Land 2",
    36: "TXC Policeman",
    37: "PAL-ZZ SMB/TETRIS/NWC",
    38: "Bit Corp.",
    40: "SMB2j FDS",
    41: "CALTRON 6-in-1",
    42: "BIO MIRACLE FDS",
    43: "FDS SMB2j LF36",
    44: "MMC3 BMC PIRATE A",
    45: "MMC3 BMC PIRATE B",
    46: "RUMBLESTATION 15-in-1",
    47: "NES-QJ SSVB/NWC",
    48: "TAITO TCxxx",
    49: "MMC3 BMC PIRATE C",
    50: "SMB2j FDS Rev. A",
    51: "11-in-1 BALL SERIES",
    52: "MMC3 BMC PIRATE D",
    53: "SUPERVISION 16-in-1",
    57: "SIMBPLE BMC PIRATE A",
    58: "SIMBPLE BMC PIRATE B",
    60: "SIMBPLE BMC PIRATE C",
    61: "20-in-1 KAISER Rev. A",
    62: "700-in-1",
    64: "TENGEN RAMBO1",
    65: "IREM-H3001",
    66: "MHROM",
    67: "SUNSOFT-FZII",
    68: "Sunsoft Mapper #4",
    69: "SUNSOFT-5/FME-7",
    70: "BA KAMEN DISCRETE",
    71: "CAMERICA BF9093",
    72: "JALECO JF-17",
    73: "KONAMI VRC3",
    74: "TW MMC3+VRAM Rev. A",
    75: "KONAMI VRC1",
    76: "NAMCOT 108 Rev. A",
    77: "IREM LROG017",
    78: "Irem 74HC161/32",
    79: "AVE/C&E/TXC BOARD",
    80: "TAITO X1-005 Rev. A",
    82: "TAITO X1-017",
    83: "YOKO VRC Rev. B",
    85: "KONAMI VRC7",
    86: "JALECO JF-13",
    87: "74*139/74 DISCRETE",
    88: "NAMCO 3433",
    89: "SUNSOFT-3",
    90: "HUMMER/JY BOARD",
    91: "EARLY HUMMER/JY BOARD",
    92: "JALECO JF-19",
    93: "SUNSOFT-3R",
    94: "HVC-UN1ROM",
    95: "NAMCOT 108 Rev. B",
    96: "BANDAI OEKAKIDS",
    97: "IREM TAM-S1",
    99: "VS Uni/Dual- system",
    103: "FDS DOKIDOKI FULL",
    105: "NES-EVENT NWC1990",
    106: "SMB3 PIRATE A",
    107: "MAGIC CORP A",
    108: "FDS UNROM BOARD",
    111: "Cheapocabra",
    112: "ASDER/NTDEC BOARD",
    113: "HACKER/SACHEN BOARD",
    114: "MMC3 SG PROT. A",
    115: "MMC3 PIRATE A",
    116: "MMC1/MMC3/VRC PIRATE",
    117: "FUTURE MEDIA BOARD",
    118: "TSKROM",
    119: "NES-TQROM",
    120: "FDS TOBIDASE",
    121: "MMC3 PIRATE PROT. A",
    123: "MMC3 PIRATE H2288",
    125: "FDS LH32",
    132: "TXC/MGENIUS 22111",
    133: "SA72008",
    134: "MMC3 BMC PIRATE",
    136: "TCU02",
    137: "S8259D",
    138: "S8259B",
    139: "S8259C",
    140: "JALECO JF-11/14",
    141: "S8259A",
    142: "UNLKS7032",
    143: "TCA01",
    144: "AGCI 50282",
    145: "SA72007",
    146: "SA0161M",
    147: "TCU01",
    148: "SA0037",
    149: "SA0036",
    150: "S74LS374N",
    153: "BANDAI SRAM",
    157: "BANDAI BARCODE",
    159: "BANDAI 24C01",
    160: "SA009",
    166: "SUBOR Rev. A",
    167: "SUBOR Rev. B",
    176: "BMCFK23C",
    192: "TW MMC3+VRAM Rev. B",
    193: "NTDEC TC-112",
    194: "TW MMC3+VRAM Rev. C",
    195: "TW MMC3+VRAM Rev. D",
    198: "TW MMC3+VRAM Rev. E",
    206: "NAMCOT 108 Rev. C",
    207: "TAITO X1-005 Rev. B",
    219: "UNLA9746",
    220: "Debug Mapper",
    221: "UNLN625092",
    226: "BMC 22+20-in-1",
    230: "BMC Contra+22-in-1",
    232: "BMC QUATTRO",
    233: "BMC 22+20-in-1 RST",
    234: "BMC MAXI",
    238: "UNL6035052",
    243: "S74LS374NA",
    244: "DECATHLON",
    246: "FONG SHEN BANG",
    252: "SAN GUO ZHI PIRATE",
    253: "DRAGON BALL PIRATE",
}
