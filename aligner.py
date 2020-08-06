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