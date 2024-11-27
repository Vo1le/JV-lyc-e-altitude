localsettings = {}

def get_variables_from_txt(file_path):
    variables = {}
    try:
        with open(file_path, 'r') as file:
            for line in file:
                line = line.strip()
                if "=" in line and not line.startswith("#"): 
                    key, value = line.split("=", 1)
                    key, value = key.strip(), value.strip()
                    try:
                        if "." in value:
                            value = float(value)
                        else:
                            value = int(value)
                    except ValueError:
                        pass
                    variables[key] = value
    except FileNotFoundError:
        print(f"fichier introuvable{file_path} ")
    except Exception as e:
        print(f"Erreur: {e}")
    return variables

def update_variable_in_txt(file_path, key, value):
    variables = get_variables_from_txt(file_path)

    variables[key] = value

    try:
        with open(file_path, 'w') as file:
            for var_key, var_value in variables.items():
                file.write(f"{var_key}={var_value}\n")
    except Exception as e:
        print(f"erreur: {e}")

localsettings= get_variables_from_txt('settings.txt')
class screensize:
    localsettings = localsettings
    @classmethod
    def setWidth(cls, val):
        cls.localsettings["width"] = val
    @classmethod
    def setHeight(cls, val):
        cls.localsettings["height"] = val
    @classmethod
    def getWidth(cls):
        return int(cls.localsettings["width"])
    @classmethod
    def getHeight(cls):
        return int(cls.localsettings["height"])
