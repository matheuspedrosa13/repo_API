import pymongo


class MongoDBInfra:

    __client = None

    @classmethod
    def get_client(cls):
        cls.__client = pymongo.MongoClient("mongodb+srv://Contas:Ma65451884@cluster0.ls20ooj.mongodb.net/test")
        return cls.__client
