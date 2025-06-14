from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponseRedirect
from django.urls import reverse
from .models import Contact
from .forms import ContactFormfrom django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponseRedirect
from django.urls import reverse
from .models import Contact
from .forms import ContactForm

def contact_list(request):
    contacts = Contact.objects.all()
    return render(request, 'app_contacts/contact_list.html', {'contacts': contacts})

def contact_detail(request, pk):
    contact = Contact.objects.get(pk=pk)
    return render(request, 'app_contacts/contact_detail.html', {'contact': contact})

def contact_create(request):
    form = ContactForm(request.POST or None)
    if form.is_valid():
        form.save()
        return redirect('contact_list')
    return render(request, 'app_contacts/contact_form.html', {'form': form})

def contact_update(request, pk):
    contact    = get_object_or_404(Contact, pk=pk)
    form = ContactForm(request.POST or None, instance=contact)  
    if form.is_valid():
        form.save()
        return redirect('contact_detail', pk=pk)
    return render(request, 'app_contacts/contact_form.html', {'form': form, 'contact': contact})

def contact_delete(request, pk):
    contact = get_object_or_404(Contact, pk=pk)
    if request.method == 'POST':
        contact.delete()
        return redirect('contact_list')
    return render(request, 'app_contacts/contact_confirm_delete.html', {'contact': contact})

def contact_search(request):
    query = request.GET.get('q', '')
    contacts = Contact.objects.filter(name__icontains=query) if query else Contact.objects.all()
    return render(request, 'app_contacts/contact_list.html', {'contacts': contacts, 'query': query})





def contact_list(request):
    contacts = Contact.objects.all()
    return render(request, 'app_contacts/contact_list.html', {'contacts': contacts})

def contact_detail(request, pk):
    contact = Contact.objects.get(pk=pk)
    return render(request, 'app_contacts/contact_detail.html', {'contact': contact})

def contact_create(request):
    form = ContactForm(request.POST or None)
    if form.is_valid():
        form.save()
        return redirect('contact_list')
    return render(request, 'app_contacts/contact_form.html', {'form': form})

def contact_update(request, pk):
    contact    = get_object_or_404(Contact, pk=pk)
    form = ContactForm(request.POST or None, instance=contact)  
    if form.is_valid():
        form.save()
        return redirect('contact_detail', pk=pk)
    return render(request, 'app_contacts/contact_form.html', {'form': form, 'contact': contact})
def contact_delete(request, pk):
    contact = get_object_or_404(Contact, pk=pk)
    if request.method == 'POST':
        contact.delete()
        return redirect('contact_list')
    return render(request, 'app_contacts/contact_confirm_delete.html', {'contact': contact})
def contact_search(request):
    query = request.GET.get('q', '')
    contacts = Contact.objects.filter(name__icontains=query) if query else Contact.objects.all()
    return render(request, 'app_contacts/contact_list.html', {'contacts': contacts, 'query': query})



