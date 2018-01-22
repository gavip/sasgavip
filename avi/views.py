import os
import json

from django.shortcuts import render, redirect, resolve_url, get_object_or_404
from django.views.decorators.http import require_http_methods

from avi.models import EuclidJob
from avi.forms import QueryForm
#Lib not needed
#from . import eas_qry, vos_handler

import logging
logger = logging.getLogger(__name__)


@require_http_methods(["GET"])
def index(request):
    """
    This view is the first view that the user sees
    """
    form_context = {
        'query_form': QueryForm()
    }
    return render(request, 'avi/index.html', context=form_context)


@require_http_methods(["POST"])
def run_query(request):
    """
    This is called when the user submits their job parameters in
    their interface.
    We pull the parameters from the request POST parameters.
    """

    adql_query = request.POST.get("query")

    job = EuclidJob.objects.create(
        query=adql_query,
    )

    return redirect(resolve_url('avi:index'))


@require_http_methods(["GET"])
def job_result(request, job_id):
    """
    This view is called to view a result given a particular job ID
    We retrieve the Job model from Django, and find the result path

    Once the result is found, we load it, then add it to the view 
    context so it can be rendered in a Django template (job_result.html)
    """
    job = get_object_or_404(EuclidJob, request_id=job_id)
    file_path = job.request.result_path
    context = {'job_id': job.id}
    with open(file_path, 'r') as out_file:
        context.update(json.load(out_file))
    return render(request, 'avi/job_result.html', context=context)
