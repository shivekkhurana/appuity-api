
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
    def pagination(msg, query, page_num, per_page=10):
        total = query.count()
        return {
            'msg': msg,
            'total': total,
            'current_page': page_num,
            'per_page': per_page,
            'last_page': int(total//per_page),
            'collection': query.paginate(per_page, page_num).serialize()
        }