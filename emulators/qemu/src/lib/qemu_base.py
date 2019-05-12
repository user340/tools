#!/usr/bin/env python

import os


class QemuBase:
    def __init__(self, qmdir=os.path.expanduser('~/.qm')):
        self.qmdir = qmdir
        self.supported_formats = [
            'blkdebug',
            'blklogwrites',
            'blkreplay',
            'blkverify',
            'bochs',
            'cloop',
            'copy-on-read',
            'dmg',
            'file',
            'ftp',
            'ftps',
            'host_device',
            'http',
            'https',
            'luks',
            'nbd',
            'null-aio',
            'null-co',
            'parallels',
            'qcow',
            'qcow2',
            'qed',
            'quorum',
            'raw',
            'replication',
            'sheepdog',
            'throttle',
            'vdi',
            'vhdx',
            'vmdk',
            'vpc',
            'vvfat'
        ]
        self.supported_suffixes = [
            'G', 'g', 'GB', 'Gb', 'gB', 'gb',
            'K', 'k', 'KB', 'Kb', 'kB', 'kb',
            'T', 't', 'TB', 'Tb', 'tB', 'tb',
            'P', 'p', 'PB', 'Pb', 'pB', 'pb',
            'E', 'e', 'EB', 'Eb', 'eB', 'eb'
        ]
