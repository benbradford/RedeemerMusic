from helper.slides_helper import SlidesHelper

class HelperFactory:

    def __init__(self, service_factory):
        self._slides_helper = SlidesHelper(service_factory.get_drive_service())

    def get_slides_helper(self):
        return self._slides_helper

helper_factory = None

def init_helper_factory(service_factory):
    global helper_factory
    if helper_factory is None:
        helper_factory = HelperFactory(service_factory)

def get_helper_factory():
    return helper_factory
