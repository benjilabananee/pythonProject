class Person:
    def __init__(self, data: dict):
        self._id = data["_id"]
        self.index = data["index"]
        self.guid = data["guid"]
        self.is_active = data["isActive"]
        self.balance = data["balance"]
        self.picture = data["picture"]
        self.city = data["city"]
        self.zip_code = data["zip_code"]
        self.state = data["state"]
        self.address = data["address"] + f", {data['city']}, {data['state']}, {data['zip_code']}"
        self.age = data["age"]
        self.eye_color = data["eyeColor"]
        self.name = data["name"]
        self.gender = data["gender"]
        self.company = data["company"]
        self.email = data["email"]
        self.domain = self._extract_domain(data["email"])
        self.phone = data["phone"]
        self.about = data["about"]
        self.registered = data["registered"]
        self.latitude = data["latitude"]
        self.longitude = data["longitude"]
        self.tags = data["tags"]
        self.friends = data["friends"]
        self.greeting = data["greeting"]
        self.favorite_fruit = data["favoriteFruit"]

    def get_friends_count(self) -> int:
        return len(self.friends)

    @staticmethod
    def _extract_domain(email: str) -> str:
        return email.split('@')[-1]

    def is_adult(self) -> bool:
        return self.age >= 18


