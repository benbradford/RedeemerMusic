from view.manipulate_service_base_view import ManipulateServiceBaseView

class EditServiceView(ManipulateServiceBaseView):
    def __init__(self, data_retriever):
        ManipulateServiceBaseView.__init__(self, data_retriever)

    def title(self):
        return "Edit"

    def method_name(self):
        return "update_service"

    def hidden_value(self, service):
        return '<input type="hidden" name="id" value="' + service['id'] + '" />'\
                '<input type="hidden" name="email_status" value="' + service['email_status'] + '" />'

    def cancel_action(self, service):
        return '<form action="http://localhost:5000/service" id="usrform">' +\
                    '<input type="hidden" name="id" value="' + service['id'] + '" />' +\
                    '<input type="submit" value="Cancel">' + \
                '</form>'
