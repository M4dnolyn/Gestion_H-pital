# config/views.py
# DEPRECATED: This file is no longer used.
# Logic has been moved to:
# - core/views.py (Dashboard, Index, Auth)
# - personnes/web_views.py (Patients, Personnel)
# - planning/web_views.py (Rendez-vous)
# - medical/web_views.py (Consultations)
# - billing/web_views.py (Facturation)

from django.shortcuts import render

def index(request):
    """
    Deprecated view kept only for emergency fallback if routing fails.
    Should not be reached with current config/urls.py
    """
    return render(request, 'index.html')
