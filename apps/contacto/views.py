from django.views.generic import CreateView
from .models import Contact
from .forms import ContactForm
from django.urls import reverse_lazy
from django.contrib import messages

class ContactView(CreateView):
    model = Contact
    template_name = 'contact/contact.html'
    form_class = ContactForm
    success_url = reverse_lazy('contacts:contact')  

    def form_valid(self, form):
        messages.success(self.request, '¡Muchas gracias, estaremos en contacto contigo! ¡Excelente trabajo!')
        return super().form_valid(form)

