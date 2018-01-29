from django.db import models
from pipeline.models import AviJob


class EuclidJob(AviJob):
    """
    This model is used to store the parameters for the AVI pipeline.
    Notice that it contains identical field names here as is the variables in
    the pipeline itself.

    An AviJob model must contain all fields required by the intended
    pipeline class (ProcessData) in this case.
    """

    query = models.CharField(max_length=1000, 
        default="""SELECT objectid, rightascension, declination, flagh, flagj, flagvis, flagy, fluxhaper, fluxjaper, fluxvisaper, fluxyaper,
                      DISTANCE(POINT('ICRS', rightascension, declination), 
                              POINT('ICRS', 8.62, -19.93)) AS dist
                      FROM sc3_mer_cat_10 
              WHERE 1=CONTAINS(POINT('ICRS', rightascension, declination), 
                               CIRCLE('ICRS', 8.62, -19.93, 0.1)) 
              ORDER BY dist ASC""")
    
    pipeline_task = "ProcessData"
