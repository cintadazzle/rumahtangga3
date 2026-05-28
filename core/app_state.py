class AppState:
    _instance = None

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(AppState, cls).__new__(cls)
            cls._instance.current_user = None
            cls._instance.current_keluarga = None
        return cls._instance

    def set_user(self, user_data):
        self.current_user = user_data

    def set_keluarga(self, keluarga_data):
        self.current_keluarga = keluarga_data

    def clear(self):
        self.current_user = None
        self.current_keluarga = None

app_state = AppState()
