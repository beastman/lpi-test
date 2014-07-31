from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.decorators import login_required
from plupload.models import PluploadImage
from django.http import HttpResponse, Http404
from django.shortcuts import render_to_response, get_object_or_404
from django.template import RequestContext
# Create your views here.

@csrf_exempt
@login_required
def plupload_handler(request):
    if request.method == 'POST':
        f = request.FILES['file']
        file = PluploadImage(image=f)
        file.save()
        return HttpResponse(file.pk)
    return HttpResponse('Not OK')

@login_required
def admin_image_preview(request):
    image_id = request.GET.get('image_id')
    field_name = request.GET.get('field_name')
    if not image_id or not field_name:
        raise Http404
    image_id = int(image_id)
    image = get_object_or_404(PluploadImage, pk=image_id)
    context = RequestContext(request)
    context['image'] = image
    context['field_name'] = field_name
    return render_to_response('plupload/admin_image_preview.html', context)