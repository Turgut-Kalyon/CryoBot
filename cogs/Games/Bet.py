




class Bet:
    def __init__(self, amount: int, author_id: int):
        self.author_id = author_id
        self.m_amount = amount


    @property
    def author_id(self):
        return self.author_id

    @property
    def amount(self):
        return self.m_amount
