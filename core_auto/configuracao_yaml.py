import yaml

class Configuracao_yaml:
    def __init__(self, arquivo_de_configuracao='config.yaml'):
        self.config = self._load_config(arquivo_de_configuracao)
        configuracao_camera = self.config['hardware']['camera']
        self.resolucao = tuple(configuracao_camera['resolution'])
        self.fps = configuracao_camera['fps']
        self.flip_horizontal = configuracao_camera['flip_horizontal']

    def _load_config(self, path):
        try:
            with open(path, 'r') as file:
                return yaml.safe_load(file)
        except Exception as e:
            print(f"Erro ao carregar configuracao: {e}")
            return {}