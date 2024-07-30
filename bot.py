from variable import variable


class Bot(object):
    status = True

    def set_status(self, status):
        self.status = status

    def get_status(self):
        return self.status

    def get_id(self):
        return variable.bot_id
