import os, tempfile

with tempfile.TemporaryDirectory() as tmp:
    print("Nowy katalog:", tmp)
    open(os.path.join(tmp, "plik1.txt"), "w").close()
    open(os.path.join(tmp, "plik2.md"), "w").close()
    print("Zawartość:", os.listdir(tmp))
    print("---")


    for name in os.listdir(tmp):
        full_path = os.path.join(tmp, name)
        print(name, "→ pełna ścieżka:", full_path)
        print("Czy to plik?", os.path.isfile(full_path))
        print("splitext:", os.path.splitext(name))
        print("---")
