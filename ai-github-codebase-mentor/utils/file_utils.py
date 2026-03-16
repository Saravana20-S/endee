def read_file(path):

    try:
        with open(path, "r", encoding="utf-8", errors="ignore") as f:
            content = f.read()

        return content

    except Exception as e:
        print("Error reading:", path, e)
        return ""