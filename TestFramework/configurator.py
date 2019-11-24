class Configurator:
    def __init__(self, environment):
        with open('config.json') as file:
            self.config = eval(file.read())
        self.config = self.config[environment]

    def get_database_url(self):
        return self.config['database']

    def get_test_data_folder(self):
        return self.config['test_data_folder']
