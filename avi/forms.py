"""
This module contains all ``django.forms.ModelForm`` implementations associated with AVI pipeline jobs (``gavip_avi.pipeline.models.AviJob``). 
The model subclasses of ``AviJob`` themselves are implemented in :mod:`avi.models`.
"""
from django.forms import ModelForm, Textarea
from avi.models import EuclidJob


class QueryForm(ModelForm):
    """
    ModelForm for Query
    """
    class Meta:
        model = EuclidJob
        # Exclude some of the fields included in the AviJob model 
        # See http://avi-framework.docs.gavip.science/pipeline.html
        exclude = [
            'expected_runtime',
            'output_path',
            'request',
            'resources_ram_mb',
            'resources_cpu_cores'
        ]
        
        widgets = {
            'query': Textarea(attrs={'rows':5, 'style':'width:100%'}),
        }
