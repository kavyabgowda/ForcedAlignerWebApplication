####Author: Kavya Bhadre Gowda######

# Copyright (c) 2011-2014 Kyle Gorman and Michael Wagner
#
# Permission is hereby granted, free of charge, to any person obtaining a
# copy of this software and associated documentation files (the
# "Software"), to deal in the Software without restriction, including
# without limitation the rights to use, copy, modify, merge, publish,
# distribute, sublicense, and/or sell copies of the Software, and to
# permit persons to whom the Software is furnished to do so, subject to
# the following conditions:
#
# The above copyright notice and this permission notice shall be included
# in all copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS
# OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF
# MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT.
# IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY
# CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT,
# TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE
# SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.



import os

from re import match
from tempfile import mkdtemp
from shutil import copyfile, rmtree
from subprocess import check_call, Popen, CalledProcessError, PIPE

from .utilities import opts2cfg, mkdir_p, \
                       HMMDEFS, MACROS, PROTO, SP, SIL, TEMP, VFLOORS
# regexp for parsing the HVite trace
HVITE_SCORE = r".+==  \[\d+ frames\] (-\d+\.\d+)"

class Aligner(object):
    def __init__(self, opts):
        # make temporary directories to stash everything
        hmmdir = os.environ["TMPDIR"] if "TMPDIR" in os.environ else None
        self.hmmdir = mkdtemp(dir=hmmdir)
        # config options
        self.HCompV_opts = opts["HCompV"]
        self.HERest_cfg = os.path.join(self.hmmdir, "HERest.cfg")
        opts2cfg(self.HERest_cfg, opts["HERest"])
        self.HVite_opts = opts["HVite"]
        self.pruning = [str(i) for i in opts["pruning"]]
        # initialize directories
        self.epochs = 0
        self.curdir = os.path.join(self.hmmdir, str(self.epochs).zfill(3))
        mkdir_p(self.curdir)
        self.epochs += 1
        self.nxtdir = os.path.join(self.hmmdir, str(self.epochs).zfill(3))
        mkdir_p(self.nxtdir)

    def align_and_score(self, corpus, mlf, scores):
        """
        The same as `self.align`, but also generates a text file `score`
        with -log likelihood confidence scores for each audio file
        """
        proc = Popen(["HVite", "-a", "-m",
                               "-T", "1",
                               "-o", "SM",
                               "-y", "lab",
                               "-b", SIL,
                               "-i", mlf,
                               "-L", corpus.labdir,
                               "-C", self.HERest_cfg,
                               "-S", corpus.feature_scp,
                               "-H", os.path.join(self.curdir, MACROS),
                               "-H", os.path.join(self.curdir, HMMDEFS),
                               "-I", corpus.word_mlf,] +
                               #FIXME(kg) do we want this?
                               #"-s", str(self.HVite_opts["SFAC"]),
                               #"-t"] + self.pruning +
                     [corpus.taskdict, corpus.phons],
                     stdout=PIPE)
        with open(scores, "w") as sink:
            i = 0
            for line in proc.stdout:
                m = match(HVITE_SCORE, line.decode("UTF-8"))
                if m:
                    print('"{!s}",{!s}'.format(corpus.audiofiles[i],
                                               m.group(1)), file=sink)
                    i += 1
        # Popen equivalent to check_call...
        retcode = proc.wait()
        if retcode != 0:
            raise CalledProcessError(retcode, proc.args)