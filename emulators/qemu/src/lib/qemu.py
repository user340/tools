#!/usr/bin/env python

import re
from lib import qemu_base


class QemuImg(qemu_base.QemuBase):
    def parse_size(self, size):
        """Parse given size to strings that can understood by qemu-img.

        Arguments:
            size (str) or (int): size of virtual disk.

        Returns:
            int or str: depends on argument. It returns same type as argument.

        Memo:
            qemu-img's help says:
                'size' is the disk image size in bytes. Optional suffixes
                  'k' or 'K' (kilobyte, 1024), 'M' (megabyte, 1024k),
                  'G' (gigabyte, 1024M), 'T' (terabyte, 1024G),
                  'P' (petabyte, 1024T) and 'E' (exabyte, 1024P) are supported.
                  'b' is ignored.
        """
        if type(size) is str:
            for supported_suffix in self.supported_suffixes:
                if size.endswith(supported_suffix):
                    return re.sub(r'B$', '', size.upper())
            raise ValueError(size + ': Given suffix is not supported')
        elif type(size) is int:
            if size < 1:
                raise ValueError('Too small value')
            return size
        else:
            raise TypeError

    def create(self, name, format, size):
        """Create virtual disk image using qemu-img.

        Arguments:
            name (str): disk name.
            format (str): disk format. Maybe qcow2 is most.
            size (str) or (int): disk size

        Returns:
            str: absolete path to created virtual disk image.
        """
        for arg in name, format:
            if type(arg) is not str:
                raise TypeError
        if type(size) is not int or type(size) is not str:
            raise TypeError
        if format not in self.supported_formats:
            raise ValueError
        pass
