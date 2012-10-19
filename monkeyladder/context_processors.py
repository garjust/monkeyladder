from monkeyladder.version import VERSION_NUMBER


def version_number(request):
    return {'version_number': VERSION_NUMBER}
