from service_retriever import get_songs, get_service_from_args
from powerpoint_creator import PowerpointCreator

if __name__ == '__main__':
    service = get_service_from_args('create_power_point.py -s <service_file>')
    ppt_file = service['ppt_file']

    PowerpointCreator(get_songs(service), ppt_file).create()

    print('created power point in {}'.format(ppt_file))
