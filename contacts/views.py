from django.shortcuts import render
from django.http import JsonResponse, Http404
from .models import Contact
import re
from .forms import FeadbackForm
from django.views.decorators.http import require_POST
from django.core.mail import EmailMessage


def page_detail(request):
    page = Contact.objects.first()
    if not page:
        raise Http404
    phone_link = 'tel+' + re.sub(r'\D', '', page.phone_1)
    form = FeadbackForm()
    breadcrumbs = [{
        'label': 'Контакты',
        'url': '',
        'type': 'text'
    }]

    context = {
        'page': page,
        'phone_link': phone_link,
        'form': form,
        'breadcrumbs': breadcrumbs
    }

    return render(request, 'contacts/page.html', context)


@require_POST
def send_message(request):
    page = Contact.objects.first()
    form = FeadbackForm(request.POST)
    if form.is_valid():
        cd = form.cleaned_data
        name = cd['name']
        tel = cd['tel']
        message = f'Имя: {name} \nНомер телефона: {tel}'
        em = EmailMessage(subject='Новое сообщение с сайта',
                          body=message,
                          to=[page.email],
                          headers={'content-type': 'text/html'}
                          )
        try:
            em.send()
            return JsonResponse({'status': 'ok'})
        except:
            return JsonResponse({'status': 'bad'})


