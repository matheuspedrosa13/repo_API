class PokeAPIInfra:
    __url = "https://pokeapi.co/api/v2/pokemon"

    @classmethod
    def get_url(cls):
        return cls.__url
