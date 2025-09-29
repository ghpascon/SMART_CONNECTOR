import asyncio
import time
from typing import Optional

from bleak import BleakClient, BleakScanner

# ---------------- BLE Settings ----------------
SERVICE_UUID = "6E400001-B5A3-F393-E0A9-E50E24DCCA9E"
CHARACTERISTIC_RX = "6E400002-B5A3-F393-E0A9-E50E24DCCA9E"
CHARACTERISTIC_TX = "6E400003-B5A3-F393-E0A9-E50E24DCCA9E"


# ---------------- BLE Manager Class ----------------
class BLEProtocol:
    def init_ble_vars(self):
        self.client_ble: Optional[BleakClient] = None
        self.client_ble_lock = asyncio.Lock()
        self.connected_ble_event = asyncio.Event()
        self.ble_stop = False

    def default_receive_func(self, data: str):
        print(f"[ESP32] {data}")

    async def scan_for_device(self):
        while not self.ble_stop:
            print("🔍 Scanning BLE devices...")
            devices = await BleakScanner.discover(timeout=5.0)
            for d in devices:
                if d.name and self.ble_name in d.name:
                    print(f"✅ Device found: {d.address}")
                    return d.address
            print("❌ Device not found, retrying in 5s...")
            await asyncio.sleep(5)

    async def connect_and_run(self):
        while not self.ble_stop:
            try:
                address = await self.scan_for_device()
                async with BleakClient(address) as client:
                    self.client_ble = client
                    print("🔗 Connected to device")
                    self.connected_ble_event.set()

                    last_ping = 0
                    while client.is_connected and not self.ble_stop:
                        now = time.time()
                        if now - last_ping >= 5:
                            await self.write(b"#ping")
                            last_ping = now

                        # Read TX characteristic
                        try:
                            data = await client.read_gatt_char(CHARACTERISTIC_TX)
                            if data:
                                decoded = data.decode(errors='ignore')
                                # Call user-defined handler or default
                                if self.on_receive_func:
                                    self.on_receive_func(decoded)
                                else:
                                    self.default_receive_func(decoded)
                        except Exception as e:
                            print(f"[Error reading TX] {e}")

                        await asyncio.sleep(0.5)

            except Exception as e:
                print(f"[Connection error] {e}")
                self.connected_ble_event.clear()
                await asyncio.sleep(5)

    async def write_ble(self, data: bytes, verbose: bool = False) -> bool:
        if not self.client_ble or not self.client_ble.is_connected:
            if verbose:
                print("⚠️ BLE client not connected")
            return False
        async with self.client_ble_lock:
            try:
                await self.client_ble.write_gatt_char(CHARACTERISTIC_RX, data)
                return True
            except Exception as e:
                if verbose:
                    print(f"[Error writing data] {e}")
                return False

    async def connect_ble(self):
        asyncio.create_task(self.connect_and_run())

    def stop(self):
        self.ble_stop = True
