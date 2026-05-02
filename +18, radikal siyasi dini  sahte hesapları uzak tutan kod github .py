from atproto import Client
import time

# --- GİRİŞ BİLGİLERİ ---
HANDLE = "becaecosystem.bsky.social"
PASSWORD = "2222-1111-0000-1111"

# Filtre Listesi
FORBIDDEN_KEYWORDS = [
    "+18", "politics", "siyaset", "din", "religious", "radical", 
    "muhalefet", "propaganda", "parti", "seçim", "troll", "ideoloji", 
    "reklam", "masaj", "massage", "gay", "lezbiyen", "lesbian", "lgbt",
    "atatürkçüyüz", "izindeyiz", "ataturk", "kemalist"
]

def get_wait_time(step):
    # 4, 5, 6 saniye döngüsünü ayarlar
    wait_times = [4, 5, 6]
    return wait_times[step % 3]

def main():
    client = Client()
    try:
        client.login(HANDLE, PASSWORD)
        print(f"--- BÜYÜK DETOKS BAŞLADI: {HANDLE} ---")
        
        step = 0

        # 1. TAKİP EDİLENLERİ (15.2B) TEMİZLE
        print("\n--- Takip edilenler taranıyor (Unfollow süreci) ---")
        cursor = None
        unfollow_count = 0
        
        while True:
            following = client.get_follows(actor=HANDLE, cursor=cursor)
            for user in following.follows:
                bio = user.description.lower() if user.description else ""
                name = user.display_name.lower() if user.display_name else ""
                
                for word in FORBIDDEN_KEYWORDS:
                    if word in (bio + name):
                        try:
                            client.unfollow(user.viewer.following)
                            print(f"❌ Takipten Çıkarıldı: {user.handle}")
                            unfollow_count += 1
                            
                            # Dinamik Bekleme Süresi Uygula
                            wait = get_wait_time(step)
                            print(f"⏳ Hız Sınırı Koruması: {wait} saniye bekleniyor...")
                            time.sleep(wait)
                            step += 1
                            break
                        except Exception as e:
                            print(f"⚠️ Hata ({user.handle}): {e}")
            
            cursor = following.cursor
            if not cursor: break

        # 2. TAKİPÇİLERİ (2.9B) KONTROL ET VE GERİ TAKİP ET
        print("\n--- Takipçiler taranıyor (Geri Takip süreci) ---")
        cursor = None
        follow_count = 0
        
        while True:
            followers = client.get_followers(actor=HANDLE, cursor=cursor)
            for user in followers.followers:
                bio = user.description.lower() if user.description else ""
                name = user.display_name.lower() if user.display_name else ""
                
                is_clean = all(word not in (bio + name) for word in FORBIDDEN_KEYWORDS)
                
                if is_clean:
                    try:
                        client.follow(user.did)
                        print(f"✅ Geri Takip Edildi: {user.handle}")
                        follow_count += 1
                        
                        # Dinamik Bekleme Süresi Uygula
                        wait = get_wait_time(step)
                        print(f"⏳ {wait} saniye mola...")
                        time.sleep(wait)
                        step += 1
                    except:
                        continue
            
            cursor = followers.cursor
            if not cursor: break

        print(f"\n--- İŞLEM TAMAMLANDI ---")
        print(f"Elenen: {unfollow_count} | Yeni Takip: {follow_count}")

    except Exception as e:
        print(f"❌ Kritik Hata: {e}")

if __name__ == "__main__":
    main()