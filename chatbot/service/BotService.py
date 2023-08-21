from chatbot.Exceptions.InternalServiceException import InternalServiceException
from chatbot.accessor.DatabaseAccessor import DatabaseAccessor
from chatbot.accessor.OpenAIAccessor import OpenAIAccessor


class BotService:

    def __init__(self):
        self.openAI_accessor = OpenAIAccessor()
        self.database_accessor = DatabaseAccessor()

    def prompt_and_respond(self, question):
        try:
            context = self.database_accessor.get_context_from_db(question)

        except InternalServiceException:
            context = "Error: Unable to reach database"
        return self.openAI_accessor.get_response(context, question)








