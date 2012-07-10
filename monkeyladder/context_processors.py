from monkeyladder.settings.common import VERSION_NUMBER

def version_number(request):
    return {'version_number': VERSION_NUMBER}