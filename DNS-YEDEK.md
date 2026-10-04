# DNS yedeği — eski site (4 Ekim 2026 itibarıyla)

GitHub'a geçmeden önce Natro'daki kayıtların aynısı. Eski siteye geri dönmek
gerekirse bu tablo birebir geri girilir.

Nerede: Natro → Hosting Yönetimi → Web Hosting Hesapları → Sınırsız Pro Hosting
(dunyaflowers.com) → Yönet → Web Alanı Yönetimi → dunyaflowers.com satırı
"Web Sitesi" menüsü → **DNS Yönetimi**.

## DNS sunucuları (Alan Adı Yönetimi → dunyaflowers.com → DNS simgesi)

| 1.DNS | 2.DNS |
|---|---|
| NS1.NATROHOST.COM | NS2.NATROHOST.COM |

## Kayıtlar

| Tür | Zone | Adres / Data |
|---|---|---|
| A | dunyaflowers.com | 94.73.149.62 |
| CNAME | www.dunyaflowers.com | dunyaflowers.com. |
| CNAME | ftp.dunyaflowers.com | dunyaflowers.com. |
| TXT | dunyaflowers.com | "v=spf1 include:_spfcls.natrohost.com include:_netblockshalon.natrohost.com ~all" |
| MX | — | Kayıt yok (domainde mail kullanılmıyor) |
| SRV | — | Kayıt yok |

Eski site Natro'da Windows 2019 / Plesk hostingde (94.73.149.62) duruyor;
hosting 14 Kasım 2026'da bitiyor. Ondan sonra eskiye dönüş mümkün olmaz.

## Eskiye dönüş

1. GitHub için eklenen 4 A kaydını (185.199.108–111.153) sil.
2. A kaydı ekle: `dunyaflowers.com` → `94.73.149.62`
3. `www` CNAME'ini (`omerkartli.github.io`) sil, yerine
   `www.dunyaflowers.com` → `dunyaflowers.com.` ekle.
4. ftp CNAME ve TXT kaydına dokunulmadı; olduğu gibi kalır.

## GitHub'a geçiş (4 Ekim 2026'da girildi)

| Tür | Zone | Adres |
|---|---|---|
| A | dunyaflowers.com | 185.199.108.153 |
| A | dunyaflowers.com | 185.199.109.153 |
| A | dunyaflowers.com | 185.199.110.153 |
| A | dunyaflowers.com | 185.199.111.153 |
| CNAME | www.dunyaflowers.com | omerkartli.github.io. |

ftp CNAME ve TXT (spf) kaydı değiştirilmedi.

Natro paneli notu: CNAME eklerken "Alt Alan Adı" = `www`, "Server" =
`omerkartli.github.io.` (sonunda nokta). A kaydında "Alt Alan Adı" boş bırakılır.
