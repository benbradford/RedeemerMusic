from client.client_factory import get_client_factory
from data.data_factory import get_data_factory, init_data_factory

init_data_factory(
    get_client_factory().get_drive_client(),
    get_client_factory().get_sheets_client()
)
