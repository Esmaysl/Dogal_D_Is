import time
import csv
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager

# WebDriver ayarları
service = Service(ChromeDriverManager().install())
driver = webdriver.Chrome(service=service)

# Trendyol ürün yorumları URL'si
url = "https://www.trendyol.com/nisantasi-shoes/mini-taba-suet-yarim-bot-ici-tuylu-duz-taban-kadin-ayakkabi-p-86852674/yorumlar?boutiqueId=61&merchantId=208337&sav=true"

# WebDriver ile sayfayı aç
driver.get(url)
time.sleep(5)  # Sayfanın yüklenmesi için bekleme

# "Daha Fazla Yorum" butonuna tıklamaya devam et
while True:
    try:
        # Sayfanın sonuna kaydır
        driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
        time.sleep(2)

        # "Daha Fazla Yorum" butonunun yüklenmesini ve tıklanabilir olmasını bekleyin
        load_more_button = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.XPATH, '//button[contains(text(), "Daha Fazla Yorum")]'))
        )
        load_more_button.click()
        time.sleep(2)  # Yorumların yüklenmesi için bekleme
    except Exception as e:
        # Eğer "Daha Fazla Yorum" butonu bulunamazsa veya daha fazla tıklanamazsa döngüden çık
        print("Tüm yorumlar yüklendi veya buton bulunamadı:", e)
        break

# Yorumları çekme
yorumlar = driver.find_elements(By.CLASS_NAME, "comment-text")  # class="comment-text" olan yorumları çek
print(f"{len(yorumlar)} adet yorum bulundu.")

# Yorumları CSV dosyasına kaydetme
csv_file_path = r"C:\Users\Pc\Desktop\ESMA_DOGAL_DİL İSLEME\yorumlar.csv"  # Dosya yolunu uygun şekilde belirtin
try:
    with open(csv_file_path, mode="w", newline="", encoding="utf-8") as file:
        writer = csv.writer(file)
        writer.writerow(["Yorum"])  # CSV başlık satırı

        for yorum in yorumlar:
            writer.writerow([yorum.text])  # Yorumları dosyaya yaz
    print(f"Yorumlar başarılı bir şekilde {csv_file_path} dosyasına kaydedildi.")
except PermissionError:
    print(f"Dosyaya yazma izni reddedildi: {csv_file_path}")
except Exception as e:
    print(f"Dosyaya yazarken bir hata oluştu: {e}")

# Tarayıcıyı kapatma
driver.quit()
