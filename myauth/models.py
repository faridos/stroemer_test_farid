class FakeUser:
    """
    a placeholder class for our fake user, just to make it easier to t authenticate
    since we don't implement the a real User model
    """
    def __init__(self, id):
        self.id = id
