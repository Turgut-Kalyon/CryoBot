from CurrencySystem.CoinTransfer import CoinTransfer
from Storage import Storage

class TestUnitCoinTransfer:
    def test_add_coins(self, tmp_path):
        file = tmp_path / "test_add_coins.yaml"
        storage = Storage("test_add_coins_key", str(file))
        coin_transfer = CoinTransfer(storage)
        coin_transfer.add_coins("test_user", 100)
        assert storage.get("test_user") is None, "User should not exist before adding coins"

        # Simulate user existing with 50 coins
        storage.set("test_user", 50)  # Simulate user existing with 50
        coin_transfer.add_coins("test_user", 50)
        assert storage.get("test_user") == 100, "Coins should be added correctly"

    def test_remove_coins(self, tmp_path):
        file = tmp_path / "test_remove_coins.yaml"
        storage = Storage("test_remove_coins_key", str(file))
        coin_transfer = CoinTransfer(storage)

        # Simulate user existing with 100 coins
        storage.set("test_user", 100)
        coin_transfer.remove_coins("test_user", 50)
        assert storage.get("test_user") == 50, "Coins should be removed correctly"

        # Test removing more coins than available
        coin_transfer.remove_coins("test_user", 100)
        assert storage.get("test_user") == 0, "Should not go below zero"

        coin_transfer.remove_coins("NOT_test_user", 50)
        assert storage.get("NOT_test_user") is None, "Should not raise error for non-existent user"

    def test_get_coins(self, tmp_path):
        file = tmp_path / "test_get_coins.yaml"
        storage = Storage("test_get_coins_key", str(file))
        coin_transfer = CoinTransfer(storage)

        # Simulate user existing with 100 coins
        storage.set("test_user", 100)
        assert coin_transfer.get_coins("test_user") == 100, "Should return correct coin amount"

        # Test non-existent user
        assert coin_transfer.get_coins("NOT_test_user") is None, "Should return None for non-existent user"

