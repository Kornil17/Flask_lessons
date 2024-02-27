import yaml
from dataclasses import dataclass

class Config:
    @classmethod
    def get_settings(cls) -> dict[str]:
        with open(f'/home/kornilov/PycharmProjects/Flask_lessons/config.yml', 'r', encoding='utf8') as file:
            return yaml.safe_load(file)






if __name__ == '__main__':
    print(Config.get_settings())
