from .models import Analysis
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib.auth.views import LoginView, LogoutView
from django.urls import reverse_lazy
from .forms import AnalysisForm, RegisterForm
from django.contrib.auth import login

@login_required
def analysis_list(request):
    if request.user.role == 'admin':
        analyses = Analysis.objects.all()
    else:
        analyses = Analysis.objects.filter(user=request.user)
    return render(request, 'analysis_list.html', {'analyses': analyses})

@login_required
def analysis_create(request):
    if request.method == 'POST':
        form = AnalysisForm(request.POST)
        if form.is_valid():
            analysis = form.save(commit=False)
            analysis.user = request.user
            analysis.save()
            return redirect('analysis_list')
        
    else: 
        form = AnalysisForm()
    return render(request, 'analysis_form.html', {'form': form})


class UserLoginView(LoginView):
    template_name = 'login.html'
    redirect_authenticated_user = True
    success_url = reverse_lazy('analysis_list')
    
    
class UserLogoutView(LogoutView):
    next_page = 'login'
    

@login_required    
def analysis_detail(request, pk):
    analysis = get_object_or_404(Analysis, pk=pk)
    
    if request.user != analysis.user and request.user.role != 'admin':
        return redirect('analysis_list')
    
    return render(request, 'analysis_detail.html', {'analysis': analysis})


@login_required
def analysis_update(request, pk):
    analysis = get_object_or_404(Analysis, pk=pk)
    
    if request.user != analysis.user and request.user.role != 'admin':
        return redirect('analysis_list')
    
    if request.method == 'POST':
        form = AnalysisForm(request.POST, instance=analysis)
        if form.is_valid():
            form.save()
            return redirect('analysis_detail', pk=analysis.pk)
    else:
        form = AnalysisForm(instance=analysis)
        
    return render(request, 'analysis_form.html', {'form': form})

@login_required
def analysis_delete(request, pk):
    analysis = get_object_or_404(Analysis, pk=pk)
    
    if request.user != analysis.user and request.user.role != 'admin':
            return redirect('analysis_list') 
    
    if request.method == 'POST':
        analysis.delete()
        return redirect('analysis_list')
    else:
        return render(request, 'analysis_confirm_delete.html', {'analysis': analysis})


def register(request):
    if request.method == 'POST':
        form = RegisterForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('analysis_list')
    else:    
        form = RegisterForm()
        
    return render(request, 'register.html', {'form': form})
    



