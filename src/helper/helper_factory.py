from helper.slides_helper import SlidesHelper

class HelperFactory:

    def __init__(self, data_retriever):
        self._slides_helper = SlidesHelper(data_retriever)

    def get_slides_helper(self):
        return self._slides_helper

helper_factory = None

def init_helper_factory(data_retriever):
    global helper_factory
    if helper_factory is None:
        helper_factory = HelperFactory(data_retriever)

def get_helper_factory():
    return helper_factory
