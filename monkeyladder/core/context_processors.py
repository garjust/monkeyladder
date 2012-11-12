from monkeyladder.version import VERSION_NUMBER


def version_number(request):
    return {'version_number': VERSION_NUMBER}


def global_announcments(request):
    return {'global_announcments': [
        ('Player vs player statistics now available in profiles', '(The calculations are slow and need to be cached)'),
    ]}
