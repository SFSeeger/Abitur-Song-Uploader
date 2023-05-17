import os


def generate_filename(self, filename):
    name = "%s/%s%s" % (self.user.id, self.user.id, os.path.splitext(filename)[1])
    return name
