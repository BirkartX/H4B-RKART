# H4B-RKART
# BIRKARTX v2.4 - Ultra Pentest Suite

**Güclü SQLi Data Dumper + Full Pentest Aləti**

BIRKARTX, sənin istədiyin kimi tam yenidən qurulmuş, güclü və gözəl dizaynlı pentest alətidir.  
Xüsusilə SQL Injection zafiyyətlərindən maksimum data (email, password, hash və s.) çıxarmaq üçün optimallaşdırılıb.

### Xüsusiyyətlər

- **Ultra SQLi Data Dumper** – Error-based, Union, Blind, Time-based dəstəyi
- Sənin verdiyin error tiplərinə xüsusi dəstək (`parent_id=`, `hidden=0`, `mysqli_fetch_object`)
- Güclü WAF Bypass (15+ tamper script)
- SQLMap ilə avtomatik data dump + hassas məlumatların ayrı CSV-yə çıxarılması
- Doxbin stilində qara-neon dizayn
- 20+ pentest modulu (Port Scan, Subdomain, Admin Finder, XSS, LFI, SSRF və s.)
- Avtomatik SQLMap quraşdırma

### Quraşdırma

#### Linux / Termux / Kali

```bash
# 1. Reponu klonla (və ya faylları əl ilə qoy)
git clone https://github.com/seninusername/birkartx.git
cd birkartx

# 2. Lazımi paketləri quraşdır
pip install customtkinter requests beautifulsoup4 dnspython websocket-client pyjwt cryptography

# 3. run.sh faylını icazə ver
chmod +x run.sh

# 4. İşə sal
./run.sh
