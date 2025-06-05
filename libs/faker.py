from faker import Faker


class Fake:
    def __init__(self, faker: Faker):
        self.faker = faker

    def card_pin(self) -> str:
        return self.faker.numerify("####")

    def card_cvv(self) -> str:
        return self.faker.credit_card_security_code()

    def card_number(self) -> str:
        return self.faker.credit_card_number()

    def sentence(self) -> str:
        return self.faker.sentence()


fake = Fake(faker=Faker())
