def save_processed_skus(skus, file_path="files/processed_skus.txt"):
    with open(file_path, "a") as file:
        for sku in skus:
            file.write(f"{sku}\n")


def load_processed_skus(file_path="files/processed_skus.txt"):
    try:
        with open(file_path, "r") as file:
            return set(file.read().splitlines())
    except FileNotFoundError:
        return set()