from astropy.table import Table

import os
import json
import numpy as np

import pandas_profiling
import pandas as pd

# Class used for creating pipeline tasks
from pipeline.classes import AviTask, AviParameter, AviLocalTarget
# AVI Framework service which uses the TAP+ connector to run/monitor 
# and download the results from an ADQL query
# import services.gacs as svc_gacs
from . import sasquery

import logging
logger = logging.getLogger(__name__)


class DownloadData(sasquery.SASQuery):
    """
    This task uses an AVI service, to obtain a data product from SAS.
    Notice that we do not define a 'run' function. It is defined by the 
    service class which we extend.

    See :class:`SASQuery`
    """
    query = AviParameter()

    def output(self):
        # The AVI job object provides a directory based on a hash of job 
        #   parameters which can be used in the AVI
        # So we create the dir if it doesn't exist already
        job_dir = self.job_model.request.output_path
        if not os.path.exists(job_dir):
            os.makedirs(job_dir)

        return AviLocalTarget(
            os.path.join(job_dir, 'sas_data.vot')
        )


class ProcessData(AviTask):
    """
    This function requires a DownloadData class to be run. 
    We will obtain Euclid data in this way.

    Once we have this data, we parse the VOTable. Then we 
    present it using pandas.
    """
    query = AviParameter()

    def output(self):
        job_dir = self.job_model.request.output_path
        return AviLocalTarget(
            os.path.join(job_dir, "pandas_profile.json")
        )

    def requires(self):
        return self.task_dependency(DownloadData)

    def run(self):

        """
        Analyses the VOTable file containing the sas-dev query results
        """
        t = Table.read(self.input().path, format='votable')
        df = pd.DataFrame(np.ma.filled(t.as_array()), columns=t.colnames)

        sasmagcols=['objectid', 'rightascension', 'declination', 'dist', 'flagh', 'flagj', 'flagvis', 'flagy', 'fluxhaper', 'fluxjaper', 'fluxvisaper', 'fluxyaper']
        sasdf = df[sasmagcols]

        profile = pandas_profiling.ProfileReport(sasdf)
        analysis_json_object = {'pandas_profiling': profile.html}

        panda_str = json.dumps(analysis_json_object)
        encoded_panda_str = panda_str.encode('utf-8')
       
        with open(self.output().path, 'wb') as out:
            out.write(encoded_panda_str)
