import pymongo


class MongoDBInfra:
    def __init__(self):
        self.__client = None

    def get_client(self):
        if self.__client is None:
            self.__client = pymongo.MongoClient(
                "mongodb+srv://pedrosa:1234@pedrosabanco.ashlzo8.mongodb.net/test"
            )

        return self.__client
