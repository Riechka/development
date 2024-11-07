class User:
    #это черновой набросок кода,он скорее всего будет изменен,если можно,хотела бы усталашать парочку советов) 
    def __init__(self, user_id, name, email, password, phone_number):
        self.user_id = user_id
        self.name = name
        self.email = email
        self.password = password
        self.phone_number = phone_number
        self.pets = []

    def register(self):
        print(f"Пользователь {self.name} зарегистрирован.")

    def login(self):
        print(f"Пользователь {self.name} вошел в систему.")

    def logout(self):
        print(f"Пользователь {self.name} вышел из системы.")

    def create_profile(self, pet):
        self.pets.append(pet)
        print(f"Профиль питомца {pet.name} создан.")

    def view_profile(self):
        for pet in self.pets:
            print(f"Питомец: {pet.name}, Возраст: {pet.age}, Порода: {pet.breed}")


class Pet:
    def __init__(self, pet_id, name, age, breed, description, owner_id):
        self.pet_id = pet_id
        self.name = name
        self.age = age
        self.breed = breed
        self.description = description
        self.owner_id = owner_id
        self.likes = []

    def create_pet_profile(self):
        print(f"Профиль питомца {self.name} создан.")

    def update_pet_profile(self, name=None, age=None, breed=None, description=None):
        if name:
            self.name = name
        if age:
            self.age = age
        if breed:
            self.breed = breed
        if description:
            self.description = description
        print(f"Профиль питомца {self.name} обновлен.")

    def delete_pet_profile(self):
        print(f"Профиль питомца {self.name} удален.")

    def like_pet(self, other_pet):
        if other_pet not in self.likes:
            self.likes.append(other_pet)
            print(f"{self.name} лайкнул питомца {other_pet.name}.")

    def dislike_pet(self, other_pet):
        if other_pet in self.likes:
            self.likes.remove(other_pet)
            print(f"{self.name} дизлайкнул питомца {other_pet.name}.")


class Message:
    def __init__(self, message_id, sender_id, receiver_id, content):
        self.message_id = message_id
        self.sender_id = sender_id
        self.receiver_id = receiver_id
        self.content = content

    def send_message(self):
        print(f"Сообщение от {self.sender_id} к {self.receiver_id}: {self.content}")

    def receive_message(self):
        print(f"Получено сообщение от {self.sender_id}: {self.content}")


def main():
    user1 = User(1, "Иван", "ivan@example.com", "password", "+71234567890")
    user1.register()
    user1.login()

    pet1 = Pet(1, "Барсик", 3, "Шотландская веслоухая", "Добрый котик", user1.user_id)
    pet1.create_pet_profile()
    user1.create_profile(pet1)

    pet2 = Pet(2, "Шарик", 5, "Немецкая овчарка", "Смешной песик", user1.user_id)
    pet2.create_pet_profile()
    user1.create_profile(pet2)

    user1.view_profile()

    pet1.like_pet(pet2)

    message = Message(1, user1.user_id, 2, "Привет! Интересный питомец!")
    message.send_message()

if __name__ == "__main__":
    main()
