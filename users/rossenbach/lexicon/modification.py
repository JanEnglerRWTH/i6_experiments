from sisyphus import Job, Task, tk

from i6_core.lib.lexicon import Lexicon, Lemma
from i6_core.util import write_xml


class AddBoundaryMarkerToLexiconJob(Job):

    def __init__(self, bliss_lexicon, add_eow=False, add_sow=False):
        """

        :param tk.Path bliss_lexicon:
        :param bool add_eow:
        :param bool add_sow:
        """
        assert add_eow or add_eow
        self.bliss_lexicon = bliss_lexicon
        self.add_eow = add_eow
        self.add_sow = add_sow

        self.out_lexicon = self.output_path("lexicon.xml")

    def tasks(self):
        yield Task("run", mini_task=True)

    def modify_phon(self, phon):
        if phon.startswith('[') and phon.endswith(']'):
            return phon
        if self.add_eow:
            phon += '#'
        if self.add_sow and (not self.add_eow or len(phon.split()) > 1):
            phon = '#' + phon
        return phon

    def run(self):

        in_lexicon = Lexicon()
        in_lexicon.load(self.bliss_lexicon.get_path())

        out_lexicon = Lexicon()

        for phoneme, variation in in_lexicon.phonemes.items():
            out_lexicon.add_phoneme(phoneme, variation)
            if not (phoneme.startswith("[") or phoneme.endswith("]")):
                out_lexicon.add_phoneme(phoneme + "#", variation)

        for lemma in in_lexicon.lemmata:
            lemma.phon = map(self.modify_phon, lemma.phon)
            out_lexicon.add_lemma(lemma)

        write_xml(self.out_lexicon.get_path(), out_lexicon.to_xml())



