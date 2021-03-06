

import pandas as pd


class Condition:

    """
    A condition maps gene names to numbers
    which often represent expression levels.

        Parameters
    ----------
    condition_name: str
        A unique name identifying the condition.

    gene_mapping: pd.Series
        A pandas Series holding the gene to number mapping or an object that
        can be converted to a pandas Series.
    """

    META_DATA_HEADER = "\t".join(["isTs", "is1stLast",
        "prevCol", "del.t", "condName"]) + "\n"

    def __init__(self, condition_name, gene_mapping):
        self.name = condition_name
        self.gene_mapping = pd.Series(gene_mapping, name=condition_name)

    def __repr__(self):
        "printable representation for diagnostics."
        return "Condition" + repr((self.name, id(self)))

    def response_scalar(self, gene_name):
        "Return the gene 'response' for this conditon."
        return self.gene_mapping[gene_name]

    def design_vector(self, transcription_factors):
        "Return a 1d array of transcription factor coefficients for condition."
        return self.gene_mapping[transcription_factors]

    def meta_data_tsv_line(self, isTs=False,
            is1stLast="e", prevCol=None, delt=None):
        def f(s):
            if s is None:
                return "NA"
            else:
                return repr(s).replace("'", '"')
        data = [isTs, is1stLast, prevCol, delt, self.name]
        return "\t".join(map(f, data)) + "\n"
