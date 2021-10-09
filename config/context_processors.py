from pages.models import Page
from contacts.models import Contact
import re


def main_processor(request):
    contacts = Contact.objects.first()
    phone_link = ''
    if contacts:
        phone_link = 'tel+' + re.sub(r'\D', '', contacts.phone_1)
    pages = Page.objects.all()
    return {
        'contacts': contacts,
        'phone_link': phone_link,
        'pages': pages
    }
