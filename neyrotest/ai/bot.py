import ai.models.abstract_model
import ai.history


class Bot:
    __token: str
    __model: ai.models.abstract_model.AbstractModel
    __history: ai.history.History

    def __init__(
        self,
        token: str,
        model: ai.models.abstract_model.AbstractModel,
        history: ai.history.History,
    ):
        self.__token = token
        self.__model = model
        self.__history = history

    def send(
        self,
        message: str,
    ) -> str:
        self.__history.add_user_message(
            message=message,
        )
        answer = self.__model.send_request(
            token=self.__token,
            history=self.__history.get_history(),
        )
        self.__history.add_ai_message(
            message=answer,
        )
        return answer
