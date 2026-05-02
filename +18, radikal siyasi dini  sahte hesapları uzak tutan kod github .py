from atproto import Client
import time

# --- GİRİŞ BİLGİLERİ ---
HANDLE = "becaecosystem.bsky.social"
PASSWORD = "2222-1111-0000-1111"

# Genişletilmiş Filtre Listesi
FORBIDDEN_KEYWORDS = [
    "+18", "politics", "siyaset", "din", "religious", "radical", 
    "muhalefet", "propaganda", "parti", "seçim", "troll", "ideoloji", 
    "reklam", "masaj", "massage", "gay", "lezbiyen", "lesbian", "lgbt",
    "atatürkçüyüz", "izindeyiz", "ataturk", "kemalist"
]

def get_wait_time(step):
    wait_times = [4, 5, 6]
    return wait_times[step % 3]

def main():
    client = Client()
    try:
        client.login(HANDLE, PASSWORD)
        print(f"--- BÜYÜK DETOKS VE ENGELLEME BAŞLADI: {HANDLE} ---")
        
        step = 0
        total_processed = 0 # Toplam işlenen kişi sayısı için sayaç

        # 1. TAKİP EDİLENLERİ (15.2B) TARAVE ENGELLE
        print("\n--- Takip edilenler taranıyor ve filtrelenenler ENGELLENİYOR ---")
        cursor = None
        
        while True:
            following = client.get_follows(actor=HANDLE, cursor=cursor)
            for user in following.follows:
                total_processed += 1
                bio = user.description.lower() if user.description else ""
                name = user.display_name.lower() if user.display_name else ""
                
                found_bad_word = False
                for word in FORBIDDEN_KEYWORDS:
                    if word in (bio + name):
                        try:
                            # Önce takipten çıkar, sonra engelle
                            client.unfollow(user.viewer.following)
                            client.block(user.did) 
                            print(f"[{total_processed}] 🚫 ENGELLENDİ: {user.handle}")
                            
                            wait = get_wait_time(step)
                            time.sleep(wait)
                            step += 1
                            found_bad_word = True
                            break
                        except Exception as e:
                            print(f"[{total_processed}] ⚠️ Hata: {e}")
                
                if not found_bad_word:
                    print(f"[{total_processed}] ✨ Temiz: {user.handle}")

            cursor = following.cursor
            if not cursor: break

        print(f"\n--- İŞLEM TAMAMLANDI ---")
        print(f"Toplam {total_processed} kişi kontrol edildi ve filtrelenenler sonsuza dek engellendi.")

    except Exception as e:
        print(f"❌ Kritik Hata: {e}")

if __name__ == "__main__":
    main()
