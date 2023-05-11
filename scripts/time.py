from datetime import datetime
import time
while True:
    print("Этот цикл продолжится бесконечно!"+datetime.now().strftime("%H:%M:%S"))
    time.sleep(2)