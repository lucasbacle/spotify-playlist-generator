class LoginViewController():
    def __init__(self, view):
        self.view = view

    def loginHandler(self):
        value = self.view.loginLineEdit.text()
        
        if (value != ""):
            # TODO : app.login
            print(value)
            pass

        