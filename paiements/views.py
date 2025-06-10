from django.shortcuts import render, redirect, get_object_or_404
from django.core.paginator import Paginator
from django.http import HttpResponse
from django.template.loader import get_template
from django.db.models import Sum
from xhtml2pdf import pisa
import pandas as pd
from .models import ClientPaiement
from .forms import ClientPaiementForm
from .forms import InscriptionForm
from django.contrib import messages

from django.contrib.auth.decorators import login_required
from xhtml2pdf import pisa
import io


from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required

def connexion(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('liste_paiements')
        else:
            erreur = "Nom d'utilisateur ou mot de passe incorrect."
            return render(request, 'paiements/login.html', {'erreur': erreur})
    return render(request, 'paiements/login.html')

@login_required
def deconnexion(request):
    logout(request)
    return redirect('login')

@login_required
def liste_paiements(request):
    paiements_list = ClientPaiement.objects.all().order_by('-date_paiement')
    paginator = Paginator(paiements_list, 10)
    page_number = request.GET.get('page')
    paiements = paginator.get_page(page_number)

    totaux = ClientPaiement.objects.aggregate(
        total_demande=Sum('montant_demande'),
        total_verse=Sum('montant_verse'),
    )
    total_demande = totaux['total_demande'] or 0
    total_verse = totaux['total_verse'] or 0
    total_solde = total_demande - total_verse

    return render(request, 'paiements/liste.html', {
        'paiements': paiements,
        'total_demande': total_demande,
        'total_verse': total_verse,
        'total_solde': total_solde,
    })

@login_required
def ajouter_paiement(request):
    if request.method == 'POST':
        form = ClientPaiementForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('liste_paiements')
    else:
        form = ClientPaiementForm()
    return render(request, 'paiements/ajouter.html', {'form': form})

@login_required
def modifier_paiement(request, paiement_id):
    paiement = get_object_or_404(ClientPaiement, id=paiement_id)
    if request.method == 'POST':
        form = ClientPaiementForm(request.POST, instance=paiement)
        if form.is_valid():
            form.save()
            return redirect('liste_paiements')
    else:
        form = ClientPaiementForm(instance=paiement)
    return render(request, 'paiements/modifier.html', {'form': form})

@login_required
def supprimer_paiement(request, paiement_id):
    paiement = get_object_or_404(ClientPaiement, id=paiement_id)
    if request.method == 'POST':
        paiement.delete()
        return redirect('liste_paiements')
    return render(request, 'paiements/supprimer.html', {'paiement': paiement})

@login_required
def reinitialiser_paiements(request):
    if request.method == 'POST':
        ClientPaiement.objects.all().delete()
        return redirect('liste_paiements')
    return render(request, 'paiements/reinitialiser.html')

@login_required
def export_excel(request):
    paiements = ClientPaiement.objects.all().values()
    df = pd.DataFrame(paiements)
    response = HttpResponse(content_type='application/vnd.ms-excel')
    response['Content-Disposition'] = 'attachment; filename="paiements.xlsx"'
    df.to_excel(response, index=False)
    return response
@login_required
def export_pdf(request):
    paiements = ClientPaiement.objects.all().order_by('-date_paiement')
    totaux = ClientPaiement.objects.aggregate(
        total_demande=Sum('montant_demande'),
        total_verse=Sum('montant_verse'),
    )
    total_demande = totaux['total_demande'] or 0
    total_verse = totaux['total_verse'] or 0
    total_solde = total_demande - total_verse

    template = get_template('paiements/pdf_template.html')
    html = template.render({
        'paiements': paiements,
        'total_demande': total_demande,
        'total_verse': total_verse,
        'total_solde': total_solde,
    })

    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = 'attachment; filename="paiements.pdf"'
    pisa_status = pisa.CreatePDF(html, dest=response)
    if pisa_status.err:
        return HttpResponse('Erreur lors de la génération du PDF', status=500)
    return response

from .forms import InscriptionForm
from django.contrib import messages

def inscription(request):
    if request.method == 'POST':
        form = InscriptionForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "Inscription réussie ! Vous pouvez maintenant vous connecter.")
            return redirect('login')  # Redirige vers ta vue login
    else:
        form = InscriptionForm()
    return render(request, 'paiements/inscription.html', {'form': form})



