# Kaburgalı Soğutma Kanalı — Proje Klasörü

Rau ve ark. (1996), 96-GT-541 — $p/e = 9$, tek duvar kaburgalı, $Re_{D_h} = 30\,000$
vakasının 2B periyodik CFD doğrulaması.

## Klasör haritası

```
00_Screenshots/    ANSYS / Fluent ekran görüntüleri (ham)
01_Data/
  cfd/             ribbed_bottomwall.csv            Fluent ASCII export (taban duvarı)
                   ribbed_bottomwall_processed.csv  script çıktısı
                   FFF_raw_fluent_export            export'un ham hâli (yedek)
  experimental/    (boş) → rau_fig15_pe9_1s.csv buraya
02_Scripts/        postprocess_ribbed.py
03_Report/         ribchannel_validation.tex + figures/
RibChannel_Gun2_Geometri_Ag.md   geometri ve ağ kararlarının gerekçeli kaydı
rau_1996_96-GT-541.pdf           referans deney makalesi
```

Çalıştırma:
```bash
python 02_Scripts/postprocess_ribbed.py     # pandas, matplotlib, numpy gerekir
cd 03_Report && pdflatex ribchannel_validation.tex   # iki kez
```

---

# 1. Aşama 1 — kesinleşen sonuçlar

| Büyüklük | Değer | Not |
|---|---|---|
| Ağ | 27 100 eleman / 27 501 düğüm | tamamı yapılandırılmış dörtgen |
| Orthogonal quality (min) | ≈ 1,00 | Element Quality ≈ 0,03 **normaldir** |
| $y^+_{\max}$ (taban) | 0,257 | ölçüm yüzeyi tam çözümlü |
| $y^+_{\max}$ (kaburga) | 2,699 | köşe tekilliği, yerel |
| $\Delta p/L$ | 37,4 Pa/m | |
| Form direnci payı | %81,3 | kalan %18,7 duvar sürtünmesi |
| Momentum dengesi | %0,05 hata | $F_x / V_{akışkan}$, $V = 2{,}225\times10^{-3}$ m³ |
| Enerji dengesi | %0,03 hata | $\Delta T_b$: ölçülen 0,07402 / teorik 0,07400 K |
| $T_w$ ortalama (taban / kaburga) | 326,2 / 312,8 K | |

---

# 2. ⚠️ Rau'nun tanımları — makaleden çıkarıldı, bunlara uyulacak

Bunlar okunmadan önce hesaplanan bazı sayılar **yanlış normalize edilmişti.**

### $Nu_0$ — Dittus-Boelter (Denklem 1)

$$Nu_0 = 0.023\,Re^{0.8} Pr^{0.4} = 78{,}01$$

Rau kendi düz kanal ölçümünü değil, korelasyonu kullanıyor. **Aşama 0'ın
$(T_w-T_b)_0$ değerine karşılaştırma için ihtiyaç yok.** Script'teki
`DT_SMOOTH` sadece ikincil, iç referans olarak duruyor.

### $f_0$ — Blasius (Denklem 4)

$$f_0 = 0.046\,Re^{-0.2} = 0.00585$$

| Normalizasyon | $f/f_0$ | Durum |
|---|---|---|
| **Blasius (Rau)** | **1,635** | ✅ karşılaştırılabilir |
| Aşama 0 düz kanal koşumuz | 3,659 | ❌ karşılaştırılamaz |

Sebep: 2B kanalımızın gerçek hidrolik çapı $2H = 0{,}1$ m, ama normalizasyonda
Rau'nun kare kanalının $D_h = 0{,}05$ m'si kullanılıyor. Düz kanal koşumuz
Blasius'un %44,7'sini veriyor, dolayısıyla referans olamaz.

### $X_r$ — duvarda değil, $Y/e = 0{,}05$'te (s.6, D.2)

> *"...measured with the LDV system at a distance of **Y/e = 0.05** in the
> symmetry plane; it was defined by the interval in which the U velocity
> remained negative."*

Yani tabandan **0,25 mm** yukarıda $U < 0$ olan aralık. Biz $\tau_w$ işaret
değişimi kullandık — aynı şey değil, **aynı tanımla yeniden çıkarılacak.**

Rau'nun değerleri: $p/e = 8 \to 3{,}75$–$4{,}00$ · **$p/e = 9,10,12 \to 4{,}00$–$4{,}25$** · $p/e = 14,16 \to 4{,}25$–$4{,}50$

### Diğer

- $f$ tanımı Fanning (Denklem 3): $f = \Delta p \, D_h / (2 L \rho U^2)$ ✅ bizimkiyle aynı
- Kaburgalar **pleksiglas** → adyabatik. Aşama 1 modellememiz deneyle birebir ✅
- Isı transferi test kesiti 50×50 mm / 5 mm kaburga; aerodinamik kesit 100×100 mm / 10 mm kaburga (ikisinde de $e/D_h = 0{,}1$)
- Rau'nun önerisi (s.3): periyodik segment yerine **beş kaburgalı** hesap, Şekil 4 profilleri $1 D_h$ yukarı akımdan giriş koşulu

---

# 3. Ana bulgu — ve statüsü

$$
X_r/e \big|_{\text{CFD}} = 7{,}95 \qquad X_r/e \big|_{\text{deney}} = 4{,}00 - 4{,}25
$$

Ayrılma balonu bir sonraki kaburgaya kadar uzanıyor, yeniden yapışma yok.
**Üç bağımsız gösterge uyuşuyor:** duvar kayma gerilmesi işareti, kuvvet
raporundaki negatif viskoz bileşen, kırpılmış $u_x$ konturu.

$Nu/Nu_0$: min 0,391 ($X/e = 0{,}65$) · maks **1,463** ($X/e \approx 4{,}7$) · periyot ort. 1,171
Rau Şekil 15'te $p/e=9$ için tepe $\approx 2{,}5$ → **%40 eksik tahmin.**

### Yakalanan yapılar (Rau s.3'teki üç girdap)

| Rau'nun tarifi | Bizde |
|---|---|
| Kaburga arkası ayrılma bölgesi | ✅ |
| Sonraki kaburga önünde ikinci küçük girdap | ✅ (ana balonla birleşmiş) |
| Kaburga üstünde üçüncü küçük girdap | ✅ |

> Önden kaydedilen hipotez ($X_r/e = 3{,}6$–$4{,}0$, yani **eksik** tahmin)
> yanlış çıkmıştır. Raporda böyle kayda geçirilecek.

## 3.1 Eleme zinciri — nedenin daraltılması

| Aday sebep | Durum | Kanıt |
|---|---|---|
| Ölçüm tanımı farkı | **elendi** | Rau'nun tanımıyla ($y=0{,}25$ mm) $X_r/e \approx 8{,}0$ — daha da uzun |
| Türbülans modeli | **elendi** | İki farklı model, $X_r/e$ farkı %0,5 (aşağıdaki tablo) |
| Ağ çözünürlüğü | test bekliyor | İki modelin aynı sonucu vermesi ağın da masum olduğuna işaret |
| **Sürekli rejim varsayımı** | **açık** | Girdap dökülmesi temsil edilemiyor |
| **2B kısıtı** | **açık** | İkincil akışlar yok |

Son iki adayın ortak yanı: ikisi de "zaman ortalamalı, düzlemsel" olmanın sonucu.

### Türbülans modeli karşılaştırması (aynı ağ, aynı sınır koşulları)

| | $k$-$\omega$ SST | Realizable $k$-$\varepsilon$ | Deney |
|---|---|---|---|
| $X_r/e$ | 7,95 | **7,91** | 4,00 – 4,25 |
| $\tau_x$ min [Pa] | −0,181 ($X/e$=3,04) | −0,229 ($X/e$=2,04) | |
| $Nu/Nu_0$ min | 0,391 | 0,558 | |
| $Nu/Nu_0$ maks | 1,463 ($X/e$=5,50) | 1,485 ($X/e$=7,73) | ~2,5 |
| $Nu/Nu_0$ periyot ort. | 1,171 | 1,043 | ~2,2 |
| $T_w$ maks [K] | 367,7 | 347,4 | |
| $\Delta p/L$ [Pa/m] | 37,4 | 42,6 | |
| $f/f_0$ (Blasius) | 1,634 | 1,860 | |

SST ve Realizable $k$-$\varepsilon$ yapısal olarak çok farklı modeller (kayma
gerilmesi sınırlayıcısı + $\omega$ tabanlı duvar formülasyonu vs. tamamen
başka bir girdap viskozitesi tanımı + $\varepsilon$ denklemi). Ayrılma
uzunluğunda binde beş içinde buluşmaları, sapmanın türbülans kapanışından
gelmediğini gösterir.

Modeller yalnızca basınç kaybında ayrışıyor (%14). Rau'nun $f/f_0$ değeri
bulununca hangisinin yakın olduğu görülecek.

**k-epsilon koşusu:** 1392 iterasyon, tw-rib = 309,99 K (düz), $F_x$ = 0,09467 N.
Veri: `01_Data/cfd/ribbed_bottomwall_kepsilon.csv`

### 2B kısıtı hipotezini destekleyen makale alıntıları

- s.1: *"Most of the present efforts in numerical flow modeling are **limited to two-dimensional approaches** on the channel centerline..."*
- s.4: *"...for the smallest p/e ratio (p/e=6) the flow clearly **reattaches around $Z/D_h=0.4$ while remaining separated in the symmetry plane**."* → balon uzunluğu açıklık yönünde ciddi değişiyor
- Şekil 9: kesitte **Prandtl'ın ikinci tür ikincil akışları** (türbülans kaynaklı). 2B modelde var olamaz.

---

# 4. Sıradaki adımlar

## YARIN İLK İŞ — ağı da ele, zincir kapansın

**İnce ağ koşusu.** Hem GCI için gerekli hem de eleme zincirinin son halkası.
Ağ da elenince geriye sadece "sürekli rejim + 2B" kalır ve rapor yazılabilir
hâle gelir. Yaklaşık 40 dakika.

| Grup | Orta (koşuldu) | İnce | Kaba |
|---|---|---|---|
| V1 | 50 | **70** | 35 |
| V2 | 80 | **113** | 57 |
| H1 | 50 | **70** | 35 |
| H2 | 30 | **42** | 21 |
| H3 | 140 | **198** | 99 |

Adımlar: Workbench → sistemi **Duplicate** → beş sizing'in `Number of Divisions`
değerini değiştir (bias faktörlerine **dokunma**) → Generate → Update → Fluent →
`/mesh/modify-zones/make-periodic` **yeniden** (eşleşmesi gereken: $70+113 = 183$ yüz)
→ sınır koşullarını kontrol → 1500 iterasyon → `bottom-wall` export.

- $X_r/e$ ince ağda 4–5'e düşerse → sebep ağdı (beklenmiyor)
- Değişmezse → sebep sürekli rejim / 2B, bkz. Bölüm 5

> **Export tuzakları** (ikisine de düşüldü):
> - Export penceresinde **File Type = ASCII** olmalı, CGNS'te kalabiliyor.
>   (CGNS de okunabiliyor, `h5py` ile — `Base/Zone/FlowSolution.N:1` altında.)
> - `Quantities` listesinde **Static Temperature** seçili olduğunu gözle
>   doğrula; `Pressure` seçili kalabiliyor.
> - Türbülans modeli değişince yakınsama ölçütü **kendini sıfırlıyor**.
>   Solution → Monitors → Residual → `Convergence Criterion = none` yapmadan
>   koşma, yoksa 40 iterasyonda durup "converged" der.

## Sonra

- [ ] Rau Şekil 15 dijitalleştirme → `01_Data/experimental/rau_fig15_pe9_1s.csv`
      (iki sütun, başlıksız: `X/e`, `Nu/Nu0`; **1s** eğrisi, 2s değil)
- [ ] Makalenin 7–8. sayfalarından Rau'nun $f/f_0$ değeri (grafikler orada olmalı)
- [ ] Kaba ağ koşusu (GCI'ın üçüncü seviyesi)
- [ ] Artık grafiği ekran görüntüsü (1070 iterasyonluk hâli)
- [ ] Kaburga üst köşesi ağ yakınlaştırması
- [ ] `air` → Thermal Conductivity teyidi (raporda 0,0242 varsayıldı)
- [ ] Rapor: sonuçlar + sonuç bölümü, `\renewcommand{\todo}[1]{}` ile taslak işaretlerini sustur

---

# 5. İnce ağ da değiştirmezse — karar

**(a) 3B'ye geç.** Aynı periyodik segment, açıklık yönünde de çözülür.
Simetri düzlemi kullanılırsa 25 mm yarım açıklık, ~1,5–2 M hücre, birkaç saatlik
steady RANS. Proje şuna dönüşür:
*"Kaburgalı kanalda 2B idealleştirmenin sınırları: ikincil akışların yeniden
yapışma ve ısı transferi üzerindeki etkisinin nicelenmesi."*
Düz bir doğrulamadan daha güçlü bir çalışma olur.

**(b) 2B kalıp sınırı belgele.** Mevcut işi bitir, sapmayı kanıtlarıyla raporla.
Daha az iş, daha az iddia.

**(c) Rau'nun önerdiği beş kaburgalı gelişen akış kurulumunu dene.** (a)'dan
daha az kazandırır.

Öneri: **ince ağ → sonuca göre (a) veya (b).**

---

# 6. Aşama 2 — CHT

Kaburga boşluğu metal katı bölge olarak doldurulacak; geometri ve ağ topolojisi
değişmiyor.

> ⚠️ Rau'nun kaburgaları pleksiglas. Metal kaburgayla yapılacak CHT'nin
> **deneysel karşılığı yok.** Aşama 2 bir doğrulama değil, doğrulanmış modelin
> **genişletilmesi** olarak konumlandırılmalı.

> ⚠️ Kaburga yüzeyindeki $y^+ = 2{,}7$ kararı Aşama 2'den önce yeniden
> değerlendirilmeli — o aşamada aktif ısı transferi yüzeyi olacak.
