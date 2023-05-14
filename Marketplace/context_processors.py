def provincia(request):
    provincia_nombre = request.session.get('provincia', None)
    return {'provincia': provincia_nombre}