from Storage import Storage
class TestUnitStorage:

    @staticmethod
    def test_set_and_get(tmp_path):
        file = tmp_path / "test_storage.yaml"
        storage = Storage("test_key", str(file))

        storage.set("test_user", 100)
        assert storage.get("test_user") == 100, "Set and Get failed"

    @staticmethod
    def test_exists(tmp_path):
        file = tmp_path / "test_exists.yaml"
        storage = Storage("test_exists_key", str(file))
        storage.set("test_exists", 110)
        assert storage.exists("test_exists") is True, "Exists check failed"
        assert storage.exists("non_existent_user") is False, "Exists check failed for non-existent user"

    @staticmethod
    def test_delete(tmp_path):
        file = tmp_path / "test_delete.yaml"
        storage = Storage("test_delete_key", str(file))
        storage.set("test_delete", 120)
        storage.delete("test_delete")
        assert storage.exists("test_delete") is False, "Delete operation failed"

    @staticmethod
    def test_adjust_decrease(tmp_path):
        file = tmp_path / "test_adjust_decrease.yaml"
        storage = Storage("test_adjust_key", str(file))
        storage.set("test_adjust", 200)
        storage.adjust("test_adjust", -50)
        assert storage.get("test_adjust") == 150, "Adjust operation failed"

    @staticmethod
    def test_adjust_negative_sets_zero(tmp_path):
        file = tmp_path / "test_adjust_negative.yaml"
        storage = Storage("test_adjust_negative_key", str(file))
        storage.set("test_adjust2", 100)
        storage.adjust("test_adjust2", -200)
        assert storage.get("test_adjust2") == 0, "Negative adjustment did not set to zero"

    @staticmethod
    def test_adjust_increase(tmp_path):
        file = tmp_path / "test_adjust_increase.yaml"
        storage = Storage("test_adjust_increase_key", str(file))
        storage.set("test_adjust", 300)
        storage.adjust("test_adjust", 100)
        assert storage.get("test_adjust") == 400, "Adjust operation failed for increase"

    @staticmethod
    def test_clear(tmp_path):
        file = tmp_path / "test_clear.yaml"
        storage = Storage("test_clear_key", str(file))
        storage.set("test_clear", 500)
        storage.clear()
        assert storage.get("test_clear") is None, "Clear operation failed"

    @staticmethod
    def test_file_creation(tmp_path):
        file = tmp_path / "test_file_creation.yaml"
        storage = Storage("test_file_creation_key", str(file))
        storage.set("test_file_creation_user", 600)
        assert file.exists(), "YAML file was not created"

    @staticmethod
    def test_save_and_load(tmp_path):
        file = tmp_path / "test_save_load.yaml"
        storage = Storage("test_save_load_key", str(file))
        loaded_storage = storage
        print(file)
        storage.set("test_save_load_user", 700)
        print("Before " + loaded_storage.get("test_save_load_user"))
        loaded_storage.load()
        print(loaded_storage.get("test_save_load_user"))
        assert loaded_storage.get("test_save_load_user") == 600, "Save and Load failed"





