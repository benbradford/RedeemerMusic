from view.manipulate_service_base_view import ManipulateServiceBaseView

class AddServiceView(ManipulateServiceBaseView):
    def __init__(self, data_retriever):
        ManipulateServiceBaseView.__init__(self, data_retriever)

    def title(self):
        return "Add"

    def method_name(self):
        return "add_service"

    def hidden_value(self, service):
        return '<input type="hidden" name="email_status" value="not sent test" />' +\
            '<input type="hidden" name="slides_email_status" value="not sent test" />'

    def cancel_action(self, service):
        return '<form action="http://localhost:5000/services" id="usrform">' +\
                    '<input type="submit" value="Cancel">' + \
                '</form>'
