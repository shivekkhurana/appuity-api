
class Response:
    @staticmethod
    def model(verb, model_instance):
        return {
            'msg': '{} {}'.format(type(model_instance).__name__, verb),
            'model': model_instance.to_dict()
        }

    @staticmethod
    def error(msg, status):
        return {
            'msg': msg,
            'status': status
        }

    @staticmethod
    def collection(msg, collection):
        return {
            'msg': msg,
            'collection': [m.to_dict() for m in collection.all()] 
        }

    @staticmethod
    def custom(msg, data):
        return {
            'msg': msg,
            'data': data
        }