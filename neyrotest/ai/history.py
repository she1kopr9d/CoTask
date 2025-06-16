class History:
    def __init__(self, history=None):
        if not history:
            self.__history = []
        else:
            self.__history = history

    def add_user_message(self, message):
        self.__history.append(
            {
                "role": "user",
                "content": message,
            }
        )

    def add_ai_message(self, message):
        self.__history.append(
            {
                "role": "assistant",
                "content": message,
            }
        )

    def add_context_message(self, message):
        self.__history.append(
            {
                "role": "context",
                "content": message,
            }
        )

    def get_last_message(self):
        return self.__history[-1]["content"]

    def get_history(self):
        return self.__history
