# Create your views here.
from django.http import HttpResponse
from EventManager.models import PurplePoster


def homepage(request):
    latest_posters_list = PurplePoster.objects.order_by('startTime')[:5]
    template = loader.get_template('EventManager/index.html')
    context = Context({
        'latest_posters_list': latest_posters_list,
    })
    return HttpResponse(template.render(context))

def purpleposterpage(request, PurplePoster):
    return HttpResponse("You're looking at the PurplePoster %s." % PurplePoster.alias + "<->" + PurplePoster.movie)

