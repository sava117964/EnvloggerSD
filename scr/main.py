import machine
import time
import sdcard
import uos
from machine import I2C, SPI, Pin

# ドライバ読み込み (出典元のAPIに準拠)
import bme280
import ds3231 

# --- ピン設定 ---
i2c = I2C(0, sda=Pin(0), scl=Pin(1), freq=400000)
spi = SPI(1, baudrate=1000000, polarity=0, phase=0, sck=Pin(10), mosi=Pin(11), miso=Pin(12))
cs_pin = Pin(13, Pin.OUT)
led = Pin("LED", Pin.OUT)

# --- 関数群 ---
def blink(times, interval=0.1):
    for _ in range(times):
        led.on()
        time.sleep(interval)
        led.off()
        time.sleep(interval)

def get_time_tuple():
    try:
        ds = ds3231.DS3231(i2c)
        return ds.get_time() 
    except Exception:
        return None

def get_env():
    try:
        bme = bme280.BME280(i2c=i2c)
        raw_t, raw_p, raw_h = bme.read_compensated_data()
        temp = raw_t / 100
        pres = raw_p / 25600 
        hum = raw_h / 1024
        return temp, hum, pres
    except Exception:
        return None, None, None

def write_log(filename, line):
    try:
        sd = sdcard.SDCard(spi, cs_pin)
        vfs = uos.VfsFat(sd)
        uos.mount(vfs, "/sd")
        full_path = "/sd/" + filename
        file_exists = False
        try:
            uos.stat(full_path)
            file_exists = True
        except OSError:
            file_exists = False
        
        with open(full_path, "a") as f:
            if not file_exists:
                f.write("Date,Temperature,Humidity,Pressure\n")
            f.write(line + "\n")
        uos.umount("/sd")
        return True
    except Exception as e:
        try: uos.umount("/sd")
        except: pass
        return False

# --- メイン処理 ---
blink(1)
time.sleep(1)

try:
    t = get_time_tuple()
    temp, hum, pres = get_env()
    
    if t is not None and temp is not None:
        now_str = "{:04d}-{:02d}-{:02d} {:02d}:{:02d}:{:02d}".format(t[0], t[1], t[2], t[3], t[4], t[5])
        filename = "{:04d}-{:02d}.csv".format(t[0], t[1])
        log_str = f"{now_str},{temp:.2f},{hum:.2f},{pres:.2f}"
        
        if write_log(filename, log_str):
            blink(3)
        else:
            blink(10, 0.05)
    else:
        blink(2, 0.5)

except Exception:
    blink(10)

time.sleep(0.1)
machine.deepsleep(3600 * 1000) # 1時間スリープ