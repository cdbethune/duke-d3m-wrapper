import os.path
import numpy as np
import pandas
import pickle
import requests
import ast
import typing
import pkg_resources
from json import JSONDecoder
from typing import List

from Duke.agg_functions import *
from Duke.dataset_descriptor import DatasetDescriptor
from Duke.utils import mean_of_rows

from d3m.primitive_interfaces.base import PrimitiveBase, CallResult

from d3m import container, utils
from d3m.metadata import hyperparams, base as metadata_base, params

__author__ = 'Distil'
__version__ = '1.1.2'

Inputs = container.pandas.DataFrame
Outputs = container.pandas.DataFrame

class Params(params.Params):
    pass


class Hyperparams(hyperparams.Hyperparams):
    pass

class duke(PrimitiveBase[Inputs, Outputs, Params, Hyperparams]):
    metadata = metadata_base.PrimitiveMetadata({
        # Simply an UUID generated once and fixed forever. Generated using "uuid.uuid4()".
        'id': "46612a42-6120-3559-9db9-3aa9a76eb94f",
        'version': __version__,
        'name': "duke",
        # Keywords do not have a controlled vocabulary. Authors can put here whatever they find suitable.
        'keywords': ['Dataset Descriptor','Text', 'NLP','Abstractive Summarization'],
        'source': {
            'name': __author__,
            'uris': [
                # Unstructured URIs.
                "https://github.com/NewKnowledge/duke-d3m-wrapper",
            ],
        },
        # A list of dependencies in order. These can be Python packages, system packages, or Docker images.
        # Of course Python packages can also have their own dependencies, but sometimes it is necessary to
        # install a Python package first to be even able to run setup.py of another package. Or you have
        # a dependency which is not on PyPi.
         'installation': [{
            'type': metadata_base.PrimitiveInstallationType.PIP,
            'package_uri': 'git+https://github.com/NewKnowledge/duke-d3m-wrapper.git@{git_commit}#egg=DukeD3MWrapper'.format(
                git_commit=utils.current_git_commit(os.path.dirname(__file__)),
            ),
         },
            {
            "type": "TGZ",
            "key": "en.model",
            "file_uri": "http://public.datadrivendiscovery.org/en_1000_no_stem.tar.gz",
            "file_digest":"3b1238137bba14222ae7c718f535c68a3d7190f244296108c895f1abe8549861"
        },
        ],
        # The same path the primitive is registered with entry points in setup.py.
        'python_path': 'd3m.primitives.distil.duke',
        # Choose these from a controlled vocabulary in the schema. If anything is missing which would
        # best describe the primitive, make a merge request.
        'algorithm_types': [
            metadata_base.PrimitiveAlgorithmType.RECURRENT_NEURAL_NETWORK,
        ],
        'primitive_family': metadata_base.PrimitiveFamily.DATA_CLEANING,
    })

    def __init__(self, *, hyperparams: Hyperparams, random_seed: int = 0, volumes: typing.Dict[str,str]=None)-> None:
        super().__init__(hyperparams=hyperparams, random_seed=random_seed, volumes=volumes)

        self._decoder = JSONDecoder()
        self._params = {}
        self.volumes = volumes

    def fit(self) -> None:
        pass

    def get_params(self) -> Params:
        return self._params

    def set_params(self, *, params: Params) -> None:
        self.params = params

    def set_training_data(self, *, inputs: Inputs, outputs: Outputs) -> None:
        pass

    def produce(self, *, inputs: Inputs, timeout: float = None, iterations: int = None) -> CallResult[Outputs]:
        """
        Produce a summary for the tabular dataset input

        Parameters
        ----------
        inputs : Input pandas frame
        Returns
        -------
        Outputs
            The output is a string summary
        """

        """ Accept a pandas data frame, returns a string summary
        frame: a pandas data frame containing the data to be processed
        -> a string summary
        """

        frame = inputs

        # cast frame data type back to original, if numeric, to ensure
        # that duke can drop them, and not skew results (since d3m
        #  preprocessing prims turn everything into str/object)
        tmp = frame.value
        for i in range(frame.value.shape[1]):
            if (frame.value.metadata.query_column(i)['semantic_types'][0]=='http://schema.org/Integer'):
                tmp.ix[:,frame.value.columns[i]].replace('',0,inplace=True)
                tmp = tmp.astype({frame.value.columns[i]:int})
            elif (frame.value.metadata.query_column(i)['semantic_types'][0]=='http://schema.org/Float'):
                tmp.ix[:,frame.value.columns[i]].replace('',0,inplace=True)
                tmp = tmp.astype({frame.value.columns[i]:float})
            # not yet sure if dropping CategoticalData is ideal, but it appears to work...
            # some categorical data may contain useful information, but the d3m transformation is not reversible
            # and not aware of a way to distinguish numerical from non-numerical CategoricalData
            elif (frame.value.metadata.query_column(i)['semantic_types'][0]=='https://metadata.datadrivendiscovery.org/types/CategoricalData'):
                tmp = tmp.drop(columns=[frame.value.columns[i]])

        # print('beginning summarization... \n')

        # get the path to the ontology class tree
        resource_package = "Duke"
        resource_path = '/'.join(('ontologies', 'class-tree_dbpedia_2016-10.json'))
        tree_path = pkg_resources.resource_filename(resource_package, resource_path)

        embedding_path = self.volumes['en.model']+"/en_1000_no_stem/en.model"
        row_agg_func=mean_of_rows
        tree_agg_func=parent_children_funcs(np.mean, max)
        source_agg_func=mean_of_rows
        max_num_samples = 1e6
        verbose=True

        duke = DatasetDescriptor(
            dataset=tmp,
            tree=tree_path,
            embedding=embedding_path,
            row_agg_func=row_agg_func,
            tree_agg_func=tree_agg_func,
            source_agg_func=source_agg_func,
            max_num_samples=max_num_samples,
            verbose=verbose,
            )

        print('initialized duke dataset descriptor \n')

        N = 5
        out_tuple = duke.get_top_n_words(N)
        print('finished summarization \n')
        out_df = pandas.DataFrame.from_records(list(out_tuple)).T
        out_df.columns = ['subject tags','confidences']

        return CallResult(out_df)

if __name__ == '__main__':
    volumes = {} # d3m large primitive architecture dictionary of large files
    volumes["en.model"]='/home/wiki2vec'
    client = duke(hyperparams={},volumes=volumes)
    # frame = pandas.read_csv("https://query.data.world/s/10k6mmjmeeu0xlw5vt6ajry05",dtype=str)
    frame = pandas.read_csv("https://s3.amazonaws.com/d3m-data/merged_o_data/o_4550_merged.csv",dtype=str)
    result = client.produce(inputs = frame)
    print(result)