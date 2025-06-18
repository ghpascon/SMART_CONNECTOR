class AddDevice:
    def __init__(self):
        self.devices = {}

    def add_device(self, data, name="default"):
        reader = data.get("READER")

        # Garante nome único
        unique_name = self._generate_unique_name(name)

        print(f"🔍 Adicionando dispositivo: {unique_name}")
        print(f"📡 Tipo de leitor: {reader}")

        if reader == "R700_IOT":
            from ..readers.R700_IOT import R700_IOT

            self.devices[unique_name] = R700_IOT(data, name)
        elif reader == "UR4":
            from ..readers.UR4 import UR4

            self.devices[unique_name] = UR4(data, name)
        elif reader == "X714":
            from ..readers.X714 import X714

            self.devices[unique_name] = X714(data, name)
        else:
            print(
                f"⚠️ Leitor '{reader}' não reconhecido. Dispositivo '{unique_name}' não adicionado."
            )

        print(f"✅ Dispositivo '{unique_name}' adicionado com sucesso.")

    def get_device_list(self):
        return [device for device in self.devices]
