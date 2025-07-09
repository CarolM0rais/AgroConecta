from django.shortcuts import redirect
from django.core.exceptions import PermissionDenied

def cliente_required(view_func):
    def _wrapped_view(request, *args, **kwargs):
        if request.user.is_authenticated and hasattr(request.user, 'pessoa'):
            if request.user.pessoa.tipo == 'cliente':
                return view_func(request, *args, **kwargs)
        raise PermissionDenied  # Ou: return redirect('index')
    return _wrapped_view
