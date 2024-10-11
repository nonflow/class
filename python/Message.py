from datetime import datetime


class Message:
    def __init__(self):
        self.messages = {}
        self.message_id = 0

    def create(self, sender, content, subject):
        self.message_id += 1
        self.messages[self.message_id] = {
            'sender': sender,
            'content': content,
            'subject': subject
        }
        print(f"Message created with ID: {self.message_id}")
        return self.message_id

    def read(self, id):
        id = int(id)
        if id in self.messages:
            message = self.messages[id]
            print(f"Message {id}:")
            print(f"From: {message['sender']}")
            print(f"Subject: {message['subject']}")
            print(f"Content: {message['content']}")
            return message
        else:
            print(f"No message found with ID: {id}")
            return None

    def list(self, from_date: str, to_date: str):
        datetime_from = datetime.strptime(from_date, "%Y-%m-%d")
        datetime_to = datetime.strptime(to_date, "%Y-%m-%d")
        print("Messages between", datetime_from, "and", datetime_to, ":")
        # Sortowanie po datach
        message_list = []
        for message_id, message in self.messages.items():
            datetime_message = datetime.strptime(message['created_at'], '%Y-%m-%d')
            if datetime_message >= datetime_from and datetime_message <= datetime_to:
                message_list.append(message)
        return message_list


    def delete(self, id):
        id = int(id)
        if id in self.messages:
            del self.messages[id]
            print(f"Message {id} deleted")
            return True
        else:
            print(f"No message found with ID: {id}")
            return False