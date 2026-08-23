import pandas as pd
import numpy as np
from scipy.signal import savgol_filter
import matplotlib.pyplot as plt
import logging

# --- 1. KULLANICI AYARLARI (USER SETTINGS) ---
# Filtre parametreleri: TiO2 Tauc plot analizinde absorpsiyon kenarını (absorption edge) 
# bozmamak için pencere boyutu ve polinom derecesi dikkatle seçilmelidir.
WINDOW_LENGTH = 5  # Tek sayı olmalı. Cihazın spektral aralığına göre değiştirilebilir.
POLY_ORDER = 3      # Ana trendi korumak için 3. derece polinom.

DOSYA_YOLU = 'ham_veri.csv' # Cihazdan alınacak ham veri
CIKTI_YOLU = 'temizlenmis_spektro_verisi.csv'
GRAFIK_YOLU = 'spektro_sonucu.png'

# Loglama Sistemi Kurulumu
logging.basicConfig(level=logging.INFO, format='%(levelname)s: %(message)s')

def veri_temizle_ve_filtrele():
    try:
        # 1. Veriyi Oku
        df = pd.read_csv(DOSYA_YOLU)
        
        # 2. Fiziksel Sınır Kontrolü ve Loglama (Hataları Halı Altına Süpürmemek)
        anormal_alt = df[df['Gecirgenlik'] < 0]
        anormal_ust = df[df['Gecirgenlik'] > 100]
        
        if not anormal_alt.empty:
            logging.warning(f"Fiziksel olmayan değer: %0'ın altında {len(anormal_alt)} veri noktası bulundu. Cihazın karanlık referansını (baseline) kontrol ediniz.")
        if not anormal_ust.empty:
            logging.warning(f"Fiziksel olmayan değer: %100'ün üzerinde {len(anormal_ust)} veri noktası bulundu. Sensör doygunluğu olabilir.")

        # Değerleri mantıklı sınırlar içine al (Clip)
        df['Gecirgenlik'] = np.clip(df['Gecirgenlik'], 0, 100)

        # Eksik (NaN) verileri lineer interpolasyon ile doldur ve kullanıcıya haber ver
        eksik_sayisi = df['Gecirgenlik'].isna().sum()
        if eksik_sayisi > 0:
            logging.info(f"{eksik_sayisi} adet eksik/okunamayan veri interpolasyon ile dolduruldu.")
            df['Gecirgenlik'] = df['Gecirgenlik'].interpolate(method='linear')

        # 3. Savitzky-Golay Filtresi Uygulama
        logging.info(f"Savitzky-Golay filtresi uygulanıyor (Pencere: {WINDOW_LENGTH}, Polinom: {POLY_ORDER}).")
        df['Filtrelenmis_Gecirgenlik'] = savgol_filter(df['Gecirgenlik'], WINDOW_LENGTH, POLY_ORDER)

        # 4. Temiz Veriyi Dışa Aktar
        df.to_csv(CIKTI_YOLU, index=False)
        logging.info(f"Temizlenmiş veri arşive eklendi: {CIKTI_YOLU}")

        # 5. Görselleştirme (Makale Formatında Grafik Çizimi)
        plt.figure(figsize=(10, 6))
        plt.plot(df['Dalga_Boyu'], df['Gecirgenlik'], label='Ham Veri (Raw)', color='gray', alpha=0.5, linewidth=1)
        plt.plot(df['Dalga_Boyu'], df['Filtrelenmis_Gecirgenlik'], label='Filtrelenmiş Veri (Filtered)', color='blue', linewidth=2)
        
        plt.title('UV-Vis Spektrofotometre Veri Analizi (TiO2/PDMS)')
        plt.xlabel('Dalga Boyu (nm)')
        plt.ylabel('Geçirgenlik (%)')
        plt.legend()
        plt.grid(True, linestyle='--', alpha=0.7)
        plt.tight_layout()
        
        plt.savefig(GRAFIK_YOLU, dpi=300)
        logging.info(f"Yüksek çözünürlüklü analiz grafiği oluşturuldu: {GRAFIK_YOLU}")
        plt.show()

    except FileNotFoundError:
        logging.error(f"HATA: '{DOSYA_YOLU}' bulunamadı. Lütfen cihaz verisini klasöre ekleyin.")
    except Exception as e:
        logging.error(f"Sistem Hatası: {e}")

if __name__ == "__main__":
    veri_temizle_ve_filtrele()