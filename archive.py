import os
from tempfile import mkdtemp
from shutil import copy, rmtree, make_archive, unpack_archive


FORMAT = "zip"

class Archive(object):
    def __init__(self, source, is_tmpdir=False):
        if os.path.isdir(source):
            self.dirname = os.path.abspath(source)
            self.is_tmpdir = is_tmpdir  # trust caller
        else:
            base = mkdtemp(dir=os.environ.get("TMPDIR", None))
            sourcePath=os.getcwd()+'/'+source
            unpack_archive(sourcePath, base)
            (head, tail, _) = next(os.walk(base))
            if not tail:
                raise ValueError("'{}' is empty.".format(source))
            if len(tail) > 1:
                raise ValueError("'{}' is a bomb.".format(source))
            self.dirname = os.path.join(head, tail[0])
            self.is_tmpdir = True  # ignore caller