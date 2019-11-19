# Copyright (C) 2013 Garrett Brown
# See Copyright Notice in rominfo.py

from .rominfo import RomInfoParser

class GenericDiscParser(RomInfoParser):
    """
    Parse generic disc image or cuesheets. Valid extensions are iso mdf img bin cue gdi.
    * https://wiki.osdev.org/ISO_9660
    """

    def getValidExtensions(self):
        return ["iso", "mdf", "img", "bin", "cue", "gdi"]

    def parse(self, filename):
        props = {}
        
        tracks = self._getDiscTracks(filename)

        if tracks:
            filename = tracks[0]["filename"]

        with open(filename, "rb") as f:
            # read first 17 sectors of disc image and convert it if neccessary
            f.seek(tracks[0]["offset"])
            data = bytearray(f.read(17 * 2352))

            # Try to convert raw CD images
            if tracks != None and tracks[0]["sector_size"] != 2048:
                data = self._convertRawToUser(data, tracks[0]["sector_size"], tracks[0]["mode"])

            if self.isValidData(data):
                props = self.parseBuffer(data)
                if tracks != None:
                    props["tracks"] = tracks
        return props

    def isValidData(self, data):
        if data[0x8001 : 0x8001 + 5] in [ b"CD001", b"BEA01", b"CD-I "]:
            return True
        return False

    def parseBuffer(self, data):
        props = {}
        props["platform"] = "Generic Disc"
        props["pvg_standard_id"] =  self._sanitize(data[0x8001 : 0x8001 + 5])
        props["pvg_system_id"] =  self._sanitize(data[0x8008 : 0x8008 + 32])
        props["pvg_volume_id"] =  self._sanitize(data[0x8028 : 0x8028 + 32])
        props["pvg_volume_set_id"] =  self._sanitize(data[0x80be : 0x80be + 128])
        props["pvg_publisher_id"] =  self._sanitize(data[0x813e : 0x813e + 128])
        props["pvg_preparer_id"] =  self._sanitize(data[0x81be : 0x81be + 128])
        props["pvg_application_id"] =  self._sanitize(data[0x823e : 0x823e + 128])
        props["pvg_copyright_file_id"] =  self._sanitize(data[0x82be : 0x82be + 37])
        props["pvg_abstract_file_id"] =  self._sanitize(data[0x82e3 : 0x82e3 + 37])
        props["pvg_bibliographic_file_id"] =  self._sanitize(data[0x8308 : 0x8308 + 37])
        props["pvg_creation_date_code"] =  self._sanitize(data[0x832d : 0x832d + 17])
        props["pvg_modification_date_code"] =  self._sanitize(data[0x833e : 0x833e + 17])
        props["pvg_expiration_date_code"] =  self._sanitize(data[0x834f : 0x834f + 17])
        props["pvg_effective_date_code"] =  self._sanitize(data[0x8360 : 0x8360 + 17])

        return props

RomInfoParser.registerParser(GenericDiscParser())
