import json


class Base:
    """
    Base class for the utiliuy functions.
    """
    @staticmethod
    def _json_str(**kwargs):
        """
        Generates an ordered string of the transaction being created for signing.
        :param transaction: transaction dict
        :ptype transaction: dict
        :return:
        """
        return json.dumps(kwargs, sort_keys=True)