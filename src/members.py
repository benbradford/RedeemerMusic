from member import Member
import json

class Members:
    def __init__(self, file_name):
        mem = open(file_name, "r").read()
        all_members = json.loads(mem)
        self._members = {}
        for member in all_members['members']:
            self._members[member['id']] = Member(member)

    def get_by_id(self, id):
        val = self._members.get(id)
        if val is None:
            raise Exception("invalid member id {}".format(id))
        return val
