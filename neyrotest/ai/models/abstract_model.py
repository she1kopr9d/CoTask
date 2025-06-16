import abc


class AbstractModel(abc.ABC):

    @abc.abstractmethod
    def send_request(
        self,
        token: str,
        history: list,
    ) -> str:
        pass
