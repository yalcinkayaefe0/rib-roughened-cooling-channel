# Kaburgalı Soğutma Kanalı — Gün 2 | Geometri ve Ağ Kararları

> **Bu dosya, ana durum dosyasının (`RibChannel_CHT_Durum.md`) Bölüm 8 "Adım 1" kısmının
> yerine geçer.** Gün 1 (pürüzsüz kanal referans koşusu) sonuçları değişmedi, ana dosyada
> geçerli.
>
> Proje sahibi: Efe Yalçınkaya — Makine Mühendisliği, ESOGÜ (4. sınıf)
> Son güncelleme: Gün 2 sonu + sayısal denetim düzeltmeleri.
> **Durum: sketch SpaceClaim'e girildi, Share Topology bekleniyor.**

---

## 0. Bu dosyada ne var

Gün 2'de tek satır CFD koşulmadı. Yapılan iş, kaburgalı vakanın geometri ve ağ
tasarımını **kurmadan önce** sonuna kadar düşünmekti. Aşağıdaki her sayı gerekçesiyle
birlikte kayıtta; hiçbiri "öyle denk geldi" değil.

**Denetim notu:** Bölüm 7'deki bias tablosu, Bölüm 9'daki eleman sayısı ve Bölüm 2.2'deki
$X/e$ dikişi bağımsız olarak yeniden türetildi ve doğrulandı. Dört düzeltme yapıldı;
hepsi metinde 🔧 ile işaretli.

---

## 1. Vaka tanımı (değişmedi)

| Parametre | Değer |
|---|---|
| Vaka | $p/e = 9$, tek duvar (1s), $e/D_h = 0.1$ |
| $Re_{D_h}$ | 30 000 ($D_h = 0.05$ m, Rau tanımı) |
| Periyodik segment uzunluğu | $p = 9 \times 5 = 45$ mm |
| Kanal yüksekliği | $H = 50$ mm |
| Kaburga kesiti | 5 × 5 mm kare, 90° dik |
| Debi | $\dot m = 0.537$ kg/s (birim derinlik) |
| Türbülans modeli | $k$-$\omega$ SST, $y^+ < 1$ |

**Doğrulama:** $Re = \dot m D_h / (A \mu) = 0.537 \times 0.05 / (0.05 \times 1.7894{\times}10^{-5}) = 30\,010$ ✓

> 🔧 **Yoğunluk tutarlılığı.** $Re$, kütle debisiyle sabitlenir ve $\rho$'dan bağımsızdır;
> ama **yığın hız değildir**:
>
> | $\rho$ [kg/m³] | $U_b = \dot m/(\rho A)$ |
> |---|---|
> | 1.18 (T ≈ 300 K) | **9.10 m/s** |
> | 1.225 (Fluent varsayılanı) | 8.77 m/s |
>
> Dokümandaki 9.1 m/s, $\rho = 1.18$ varsayımına dayanır. Fluent'te malzeme panelinde
> hangi $\rho$ duruyorsa, $f = (\Delta p/L) D_h / (2\rho U_b^2)$ hesabında **aynısı**
> kullanılacak. Karıştırılırsa $f$'te %8 hata olur.

---

## 2. ✅ KESİN: Kaburga konumu — $x = 12.5$ ile $17.5$ mm arası

### 2.1 Sketch tanımı

XY düzleminde, **orijin domenin sol alt köşesi** (taban duvarı ile sol periyodik kenarın
kesişimi). Birim: **mm**.

| Nesne | Başlangıç | Bitiş |
|---|---|---|
| Dikdörtgen | $(0,\ 0)$ | $(45,\ 50)$ |
| Dikey çizgi 1 | $(12.5,\ 0)$ | $(12.5,\ 50)$ |
| Dikey çizgi 2 | $(17.5,\ 0)$ | $(17.5,\ 50)$ |
| Yatay çizgi | $(0,\ 5)$ | $(45,\ 5)$ |

```
 y=50 ┌──────┬──┬────────────────┐
      │      │  │                │
      │  A2  │B │      C2        │
  y=5 ├──────┼──┼────────────────┤
      │  A1  │R │      C1        │
      ●──────┴──┴────────────────┘  y=0
   (0,0)   12.5  17.5           45
```

> ⚠️ Kaburga karesini **ayrıca çizme.** Üç çizgi zaten altı kapalı alan üretiyor;
> kaburga karesi bunlardan biri olarak kendiliğinden oluşuyor. Ayrıca çizersen üst üste
> binen kenarlar çıkar.
>
> ⚠️ Çizgiler uçtan uca olmalı (dikeyler $y{=}0 \to 50$, yatay $x{=}0 \to 45$).
> Kısa kalırsa alan kapanmaz, yüzey bölünmez.
>
> ⚠️ **Orijin ankrajı.** Dikdörtgenin sol alt köşesi tam $(0,0)$'da olmalı. Sketch ekranda
> rastgele bir yere oturursa fizik değişmez ama Bölüm 15'teki $X/e$ formülünün sabitleri
> ($17.5$ ve $45$) geçersiz olur. Koordinatları klavyeden gir (değer → **Tab** → değer →
> **Enter**), fareyle tıklayarak konumlandırma.

### 2.2 Neden bu konum — $X/e$ dikişi

Post-processing'de Rau'nun eksenine geçiş:

$$
X/e = \frac{\left( x_{[\text{mm}]} - 17.5 \right) \bmod 45}{5}
$$

`mod` işlemi eğriyi bir yerden böler ("dikiş"). Dikişin konumu kaburganın konumuna bağlı:

$$
x = 45 \ \text{mm} \ \rightarrow \ X/e = 5.5
$$

$$
x = 0 \ \text{mm} \ \rightarrow \ X/e = 5.5
$$

Kaburga ön yüzü ($x = 12.5$) ise $X/e = 8.0$'a düşer. Yani **taban duvarı verisi
$X/e \in [0,\ 8]$ aralığını kaplar** ($p/e = 9$'un 1'ini kaburganın kendisi yiyor) ve
dikiş bu aralığın içinde, 5.5'te.

Taban boyunca ilgi bölgeleri:

| $X/e$ | Ne oluyor |
|---|---|
| 0 – 1.5 | Kaburga arkası resirkülasyon balonu, $Nu$ minimum |
| **4.0 – 4.25** | **Yeniden yapışma — en keskin doğrulama metriği** |
| 6.5 – 8.0 | Bir sonraki kaburga önündeki ikincil ayrılma (1–1.5$e$) |
| **5.0 – 6.3** | **Sessiz bölge — dikiş buraya konuldu** |

Dikiş $X/e = 5.5$'te, yani hiçbir olayın olmadığı yerde. Hem yeniden yapışma hem de
kaburga önü ayrılma bölgesi **tek parça, kesintisiz veri** içinde kalıyor.

### 2.3 Reddedilen alternatifler (kayıtta tutuluyor)

| Konum | Dikiş | Neden reddedildi |
|---|---|---|
| $x = 0 \to 5$ | — | Sol periyodik kenar 45 mm, sağ kenar 50 mm olur. `make-periodic` iki yüzü eşleştiremez, **reddeder** |
| Ortada ($x = 20 \to 25$) | $X/e = 4.0$ | Dikiş **tam yeniden yapışma noktasında**. $X_r$ verisi domenin iki ucuna bölünür |
| $x = 5 \to 10$ | $X/e = 7.0$ | Dikiş kaburga önü ikincil ayrılma bölgesinin ($6.5-8.0$) içinde |
| **$x = 12.5 \to 17.5$** | **$X/e = 5.5$** | **SEÇİLDİ** — dikiş sessiz bölgede |

> **Not:** Translational periyodik domende kaburganın konumu **fiziği hiç değiştirmez** —
> çözüm bit bit aynı çıkar, sadece ötelenir. Bu tamamen post-processing kolaylığı kararıdır.
> Raporda: *"Periyodik sınır, ilgi bölgelerinin dışına yerleştirilmiştir."*

---

## 3. ✅ Altı yüzey

Sketch'ten çıkınca oluşan kapalı alanlar:

| Yüz | $x$ [mm] | $y$ [mm] | Boyut | Durum |
|---|---|---|---|---|
| A1 | 0 – 12.5 | 0 – 5 | 12.5 × 5 | akışkan |
| A2 | 0 – 12.5 | 5 – 50 | 12.5 × 45 | akışkan |
| B | 12.5 – 17.5 | 5 – 50 | 5 × 45 | akışkan |
| **R** | 12.5 – 17.5 | 0 – 5 | 5 × 5 | **SİL** |
| C1 | 17.5 – 45 | 0 – 5 | 27.5 × 5 | akışkan |
| C2 | 17.5 – 45 | 5 – 50 | 27.5 × 45 | akışkan |

R silinince beş akışkan bloğu kalır.

$$
A_{\text{akışkan}} = 45 \times 50 - 5 \times 5 = 2225 \ \text{mm}^2
$$

### 3.1 Neden beş blok

Face Meshing (mapped) **sadece dört kenarlı yüzlerde** çalışır. Kaburga çıkarılınca
kalan tek parça alan altı kenarlı "L" benzeri bir şekildir → mapped olmaz.

Bölme çizgileri keyfi değil, **kaburga kenarlarının uzantıları**:
- $x = 12.5$ → kaburga ön yüzünün uzantısı
- $x = 17.5$ → kaburga arka yüzünün uzantısı
- $y = 5$ → kaburga üst yüzünün uzantısı

### 3.2 Share Topology — atlanırsa çözüm sessizce bozulur

SpaceClaim'de: Structure ağacında en üstteki **Component**'i seç → sağ panel →
**Share Topology = Share** → Share butonu.

Yapılmazsa beş yüz komşu ama **bağlı değil** kalır. Meshing hata vermez, ağ üretir,
ama blok sınırlarında düğümler eşleşmez ve **Fluent'te bloklar arası akış geçmez.**

**Meshing içinden doğrulama:** ağaçta `Geometry` dalını aç. Beş `Surface Body`,
**tek bir `Part` altında** olmalı. Beş ayrı Part görünüyorsa: beşini Ctrl ile seç →
sağ tık → **Form New Part**.

---

## 4. ⚠️ Kenar topolojisi — R silinince bir kenar da siliniyor

Sketch'te R karesinin 4 kenarı vardı. R silinince:

| Kenar | Durum | Sebep |
|---|---|---|
| $x = 12.5$, $y{:}\ 0 \to 5$ | **kalır** | aynı zamanda A1'in sağ kenarı |
| $x = 17.5$, $y{:}\ 0 \to 5$ | **kalır** | aynı zamanda C1'in sol kenarı |
| $y = 5$, $x{:}\ 12.5 \to 17.5$ | **kalır** | aynı zamanda B'nin alt kenarı |
| $y = 0$, $x{:}\ 12.5 \to 17.5$ | **KAYBOLUR** | sadece R kullanıyordu, başka komşusu yoktu |

**Sonuç:** Kaburga boşluğunu çevreleyen kenar sayısı **3'tür, 4 değil.** Bu üçü `rib-wall`.
Ayrıca dış dikdörtgenin alt kenarı ikiye bölünmüş durumdadır — `bottom-wall`ın iki
kenardan oluşmasının sebebi budur.

### 4.1 Toplam kenar sayısı: 16

| Yön | Konum | Adet |
|---|---|---|
| Dikey | $x = 0,\ 12.5,\ 17.5,\ 45$ — her biri $y{=}5$ ile ikiye bölünmüş | 8 |
| Yatay | $y = 0$ (2 parça), $y = 5$ (3 parça), $y = 50$ (3 parça) | 8 |

**Çapraz kontrol:** 12 sınır kenarı (Bölüm 5) + 4 iç kenar ($y{=}5$ sol ve sağ parçaları,
$x{=}12.5$ ve $x{=}17.5$ üst parçaları) = 16 ✓
Edge sizing grupları: V1(4) + V2(4) + H1(3) + H2(2) + H3(3) = 16 ✓

### 4.2 Terminoloji

Akış $+x$ yönünde. Bir yüzeyin akışa göre konumunu **uzandığı yön değil, normali** belirler.

| Yüzey | Uzanım | Normal | Akış |
|---|---|---|---|
| `bottom-wall` ($y{=}0$) | $x$ | $y$ | teğet |
| Kaburga **ön yüzü** ($x{=}12.5$) | $y$ | $x$ | **dik çarpıyor** (yukarı akım) |
| Kaburga **üst yüzü** ($y{=}5$) | $x$ | $y$ | teğet, hızlanıyor |
| Kaburga **arka yüzü** ($x{=}17.5$) | $y$ | $x$ | dik, ayrılmış bölge (aşağı akım) |

Rau'nun $X/e$ ekseninin sıfırı **arka yüzdedir** (resirkülasyon oradan başlar).

### 4.3 Kaburga katısı ağda yok ama yüzeyleri gerçek duvar

Aşama 1'de kaburga boşluk olarak kalıyor; üç yüzeyi akışkan domeninin sınırı ve
**adyabatik duvar**. Deneyde arkasında pleksiglas var, iletken değil, dolayısıyla
akışkan açısından fark yok.

**Aşama 2'de bu boşluk metal katı bölge olarak doldurulacak** — geometri aynı kalır,
sadece boşluk mesh'lenir ve konjuge kuplaj devreye girer.

---

## 5. Named selections

Seçim filtresi **Edge** modunda yapılır.

| İsim | Kenarlar | Adet | Sınır koşulu |
|---|---|---|---|
| `periodic-1` | $x = 0$: A1 solu + A2 solu | 2 | periyodik |
| `periodic-2` | $x = 45$: C1 sağı + C2 sağı | 2 | periyodik (shadow) |
| `bottom-wall` | $y = 0$: $x \in [0, 12.5]$ ve $x \in [17.5, 45]$ | 2 | **sabit $q$ = 1000 W/m²** |
| `rib-wall` | $x{=}12.5$ ($y{:}0{\to}5$), $y{=}5$ ($x{:}12.5{\to}17.5$), $x{=}17.5$ ($y{:}0{\to}5$) | 3 | **ADYABATİK** |
| `top-wall` | $y = 50$: A2, B, C2 üstü | 3 | adyabatik |
| `fluid` | 5 yüz | 5 | akışkan bölge |

> `periodic-1` ve `periodic-2` artık **ikişer kenardan** oluşuyor ($y{=}5$ çizgisi yan
> kenarları da böldüğü için). Ctrl ile ikisini birden seç. Fluent tarafında tek zone
> olarak gelir, `make-periodic` sorunsuz eşleştirir.
>
> **Named selection ile edge sizing gruplaması farklı şeylerdir.** Aynı kenar ikisinde de
> yer alır, çakışma olmaz. Named selection sınır koşulu için, edge sizing ağ için.

---

## 6. ANSYS Meshing — global ayarlar (minimal)

Mapped yüzde iç düğümler **transfinite interpolasyonla**, yani tamamen kenar düğüm
dağılımından türetilir. Global sizing fonksiyonu bu hesaba girmez. 16 kenarın 16'sı da
`Behavior = Hard` sizing altında olduğu için global ayarların karar vereceği hiçbir şey
kalmıyor.

**Mesh dalının Details panelinde sadece:**

| Alan | Değer |
|---|---|
| Physics Preference | **CFD** |
| Element Order | **Linear** |

`Element Order` sizing'le değil eleman tipiyle ilgilidir; Program Controlled bırakılırsa
ara düğümlü (quadratic) eleman üretebilir, Fluent doğrusal hücre bekler.
`Physics Preference = CFD` zaten bunu otomatik Linear'a çeker — ikisinden biri yeterli.

**Ölü ayarlar (dokunma):** Capture Curvature (16 kenar da düz doğru), Capture Proximity
(mapped'de devreye girmez), Growth Rate (sizing'siz bölge yok), Smoothing (mapped quad'da
düzeltilecek bozukluk yok).

> ❌ **Max Size = 1 mm HATALIYDI, kullanılmayacak.** V2 grubunun kanal ortasındaki hücresi
> 2.66 mm. Uygulansaydı bias tasarımını kırardı. Uygulanmıyor olması işi kurtarıyor ama
> ayar yine de silinmeli.

### 6.1 Workbench ön koşulu

Geometry hücresi seçili → Properties → Advanced Geometry Options → **Analysis Type = 2D**.
**Mesh hücresi bir kez açıldıktan sonra yapılırsa geometri 3B olarak okunmuş olur** ve
düzeltmek için projeyi yeniden kurmak gerekir.

### 6.2 Face Meshing

Seçim filtresi **Face** modunda, beş yüzü de Ctrl ile seç →
Mesh dalına sağ tık → Insert → **Face Meshing**

| Alan | Değer |
|---|---|
| Geometry | 5 Faces |
| Method | **Quadrilaterals** |
| Constrain Boundary | No |

Tek Face Meshing yeterli, beş ayrı tane gerekmez.

---

## 7. Edge sizing — beş grup

Her grup için: seçim filtresi **Edge** modunda, kenarları Ctrl ile seç →
Mesh dalına sağ tık → Insert → **Sizing**

Her Edge Sizing'de doldurulacak alanlar:

```
Scoping Method       = Geometry Selection
Type                 = Number of Divisions
Number of Divisions  = (tablodan)
Behavior             = Hard
Bias Type            = iki uçta sık (dropdown'da çizgilerin iki uçta yoğun olduğu grafik)
Bias Option          = Bias Factor
Bias Factor          = (tablodan)
Reverse Bias         = None
```

### 7.1 ⚠️ Tüm gruplarda bias "iki uçta sık" — tek yönlü bias YOK

**Karar değişikliği (Gün 2).** İlk planda H1 ve H3 için tek yönlü bias düşünülmüştü,
**iptal edildi.**

Gerekçe: tek yönlü bias'ta "başlangıç" ve "bitiş" kenarın kendi iç yönüne bağlıdır.
Bu yön ekranda görünmez ve aynı gruptaki dört kenarda farklı olabilir → bazı kenarlar
ters biaslanır ve fark edilmez. **İki uçta sık bias simetriktir**, ters dönmesi hiçbir
şeyi değiştirmez. Sorun tamamen ortadan kalkar.

Ek fayda: V1'in üst ucundaki hücre (0.020 mm) ile V2'nin alt ucundaki hücre (0.021 mm)
eşleşir → $y = 5$ çizgisinde geçiş pürüzsüz olur.

### 7.2 Grup tanımları

Aşağıdaki ilk/son hücre boyları, ANSYS'in iki-uçta-bias tanımından türetildi
(her yarıda geometrik seri, $BF = $ en büyük / en küçük hücre):

$$
r = BF^{\,1/(N/2 - 1)}, \qquad
\Delta_1 = \frac{L}{2} \cdot \frac{r - 1}{r^{N/2} - 1}
$$

#### V1 — kaburga seviyesindeki dikey kenarlar (4 kenar, $y{:}\ 0 \to 5$ mm)

| # | Konum | Nerede |
|---|---|---|
| 1 | $x = 0$ | A1 sol kenarı (periyodik) |
| 2 | $x = 12.5$ | **kaburga ön yüzü** |
| 3 | $x = 17.5$ | **kaburga arka yüzü** |
| 4 | $x = 45$ | C1 sağ kenarı (periyodik) |

| Number of Divisions | Bias Factor | İlk hücre | En büyük hücre |
|---|---|---|---|
| **50** | **14** | 0.0199 mm | 0.278 mm |

`bottom-wall` üzerindeki $y^+$'yı bu grup belirler. **Kritik grup.**

#### V2 — üst bölgedeki dikey kenarlar (4 kenar, $y{:}\ 5 \to 50$ mm)

| # | Konum | Nerede |
|---|---|---|
| 1 | $x = 0$ | A2 sol kenarı (periyodik) |
| 2 | $x = 12.5$ | A2 / B blok sınırı |
| 3 | $x = 17.5$ | B / C2 blok sınırı |
| 4 | $x = 45$ | C2 sağ kenarı (periyodik) |

| Number of Divisions | Bias Factor | İlk hücre | En büyük hücre |
|---|---|---|---|
| **80** | **130** | 0.0204 mm | 2.658 mm |

İki iş birden: üstte `top-wall`, altta **kaburga üst yüzeyi** $y^+$'sı.

#### H1 — kaburga öncesi yatay kenarlar (3 kenar, $x{:}\ 0 \to 12.5$ mm)

| # | Konum | Nerede |
|---|---|---|
| 1 | $y = 0$ | `bottom-wall` sol parçası |
| 2 | $y = 5$ | A1 / A2 blok sınırı |
| 3 | $y = 50$ | `top-wall` sol parçası |

| Number of Divisions | Bias Factor | İlk hücre | En büyük hücre |
|---|---|---|---|
| **50** | **14** | 0.0497 mm | 0.695 mm |

$x = 12.5$'teki sıklaşma **kaburga ön yüzünün $y^+$'sı** içindir.

#### H2 — kaburga üstündeki yatay kenarlar (2 kenar, $x{:}\ 12.5 \to 17.5$ mm)

| # | Konum | Nerede |
|---|---|---|
| 1 | $y = 5$ | **kaburga üst yüzeyi** (`rib-wall`ın parçası) |
| 2 | $y = 50$ | `top-wall` orta parçası |

| Number of Divisions | Bias Factor | İlk hücre | En büyük hücre |
|---|---|---|---|
| **30** | **10** | 0.0414 mm | 0.414 mm |

İki uçtaki sıklaşma kaburganın **iki üst köşesi** içindir — kayma tabakası oradan kopuyor.

#### H3 — kaburga sonrası yatay kenarlar (3 kenar, $x{:}\ 17.5 \to 45$ mm)

| # | Konum | Nerede |
|---|---|---|
| 1 | $y = 0$ | `bottom-wall` sağ parçası — **BİRİNCİL ÖLÇÜM YÜZEYİ** |
| 2 | $y = 5$ | C1 / C2 blok sınırı |
| 3 | $y = 50$ | `top-wall` sağ parçası |

| Number of Divisions | Bias Factor | İlk hücre | En büyük hücre |
|---|---|---|---|
| **140** | **10** | 0.0500 mm | 0.500 mm |

Bölme sayısı bilinçli olarak yüksek: $Nu/Nu_0$ dağılımı Şekil 15 ile burada karşılaştırılacak
ve yeniden yapışma noktası ($x \approx 37.5$ mm) burada. O civarda hücre boyu
(doğrulandı — 54. hücre, $x{=}45$ ucundan 7.5 mm içeride):

$$
\Delta x_{\text{yeniden yapışma}} = 0.295 \ \text{mm} = 0.059 \, e
$$

$\tau_w$'nin işaret değiştirdiği yer doğrusal enterpolasyonla bulunduğunda $X_r/e$
hassasiyeti 0.02'nin altına iner.

**Periyodik uyum kontrolü:** H1'in $x{=}0$'daki hücresi 0.0497 mm, H3'ün $x{=}45$'teki
hücresi 0.0500 mm → periyodik yüzeyin iki tarafında hücre boyu pratik olarak aynı.

---

## 8. Gruplamanın mantığı — kısıt zinciri

Gruplar fiziksel benzerliğe göre değil, **mapped ağın dayattığı zincire** göre kuruldu.

$y{:}\ 0 \to 5$ katındaki dört dikey kenar için:

**1. A1 bloğu** ($x \in [0,\ 12.5]$, $y \in [0,\ 5]$) dikdörtgen ve mapped:

$$
N_{x=0} = N_{x=12.5}
$$

**2. C1 bloğu** ($x \in [17.5,\ 45]$, $y \in [0,\ 5]$):

$$
N_{x=17.5} = N_{x=45}
$$

**3. Periyodiklik.** `make-periodic` iki yüzü düğüm düğüm eşleştirir:

$$
N_{x=0} = N_{x=45}
$$

Üçü birleşince:

$$
N_{x=0} = N_{x=12.5} = N_{x=17.5} = N_{x=45} = 50
$$

Yani **kaburganın iki yüzünün aynı bölme sayısına sahip olması tercih değil, zorunluluk.**
V2, H1, H2, H3 için de aynı mantık işler.

### 8.1 Hangi grup hangi duvarın $y^+$'sını belirliyor

$y^+$ her zaman **duvara dik yönde** ölçülür.

| Yüzey | Duvara dik yön | Belirleyen grup | İlk hücre | Beklenen $y^+$ |
|---|---|---|---|---|
| `bottom-wall` | $y$ | **V1** | 0.020 mm | 0.22 |
| `top-wall` | $y$ | **V2** | 0.021 mm | 0.23 |
| Kaburga üst yüzü | $y$ | **V2** | 0.021 mm | 0.23 |
| Kaburga **ön** yüzü | $x$ | **H1** | 0.050 mm | 0.54 |
| Kaburga **arka** yüzü | $x$ | **H3** | 0.050 mm | 0.54 |

> $y^+$ tahminleri Gün 1'in düz kanal değeriyle ($\Delta p/L = 10.22$ Pa/m →
> $\tau_w = 0.128$ Pa → $u_\tau = 0.329$ m/s) ve ilk hücre **merkezine** göre hesaplandı.
> Kaburgalı vakada yerel $\tau_w$ yeniden yapışma civarında birkaç kat artacağı için
> gerçek değerler bunun 1.5–2 katı olabilir; yine de $y^+ < 1$ korunur.

> Kaburganın ön/arka yüzlerinde $y^+$'yı V1 **değil**, yatay gruplar (H1, H3) belirler.
> V1 o yüzeylerde sadece yüzey boyunca kaç düğüm olacağını belirler.

**0.050 mm neden yeterli:** her iki yüz de düşük kayma gerilmesi bölgesinde. Ön yüz,
kaburganın $1{-}1.5e$ önünde başlayan ikincil ayrılma balonunun içinde; arka yüz ana
resirkülasyon balonunun içinde. En yüksek $\tau_w$ kaburga üstünde ve yeniden yapışma
civarında — ikisi de 0.02 mm'lik gruplarla korunuyor.

**Koşu sonrası kontrol:** `rib-wall` üzerinde $y^+$ konturuna ayrıca bak. 2'yi aşıyorsa
H1 ve H3'ün bias faktörlerini 14 → 25 civarına çıkar, **bölme sayısına dokunma**
(dokunursan kısıt zinciri bozulur).

---

## 9. Beklenen ağ istatistikleri

$$
N_{\text{alt şerit}} = 50 \times (50 + 140) = 9500
$$

$$
N_{\text{üst bölge}} = 80 \times (50 + 30 + 140) = 17\,600
$$

$$
N_{\text{toplam}} = 27\,100 \ \text{eleman}
$$

🔧 **Düğüm sayısı 27 501** (doküman v1'deki ~27 400 yanlıştı):

$$
N_{\text{düğüm}} = \underbrace{51 \times 51 + 141 \times 51}_{\text{alt: A1 + C1}}
+ \underbrace{221 \times 81}_{\text{üst}}
- \underbrace{192}_{y=5 \ \text{ortak satırı}} = 27\,501
$$

Çıkan sayı buna yakın değilse **bir Edge Sizing tutmamıştır.**

Mesh → Details → Statistics / Quality → Mesh Metric:

| Metrik | Beklenen | Not |
|---|---|---|
| Elements | ~27 100 | |
| Nodes | ~27 500 | |
| Orthogonal Quality (min) | **> 0.95** (pratikte ≈ 1.0) | tüm hücreler dikdörtgen |
| Skewness (max) | **< 0.05** (pratikte ≈ 0) | |
| 🔧 Element Quality (min) | **≈ 0.03** | **>0.30 değil** — aşağıya bak |
| 🔧 Aspect Ratio (max) | **≈ 64** | **100–400 değil** |

> 🔧 **Element Quality ve Aspect Ratio eşikleri düzeltildi.** ANSYS'in quad Element
> Quality tanımı $EQ = 4A/\sum L_i^2$'dir; $a \times b$ dikdörtgen için
>
> $$
> EQ = \frac{2\,AR}{AR^2 + 1}, \qquad AR = \max(a/b,\ b/a)
> $$
>
> En kötü hücre kanal ortasında, kaburga hizasındaki dar sütunda:
>
> $$
> AR_{\max} = \frac{2.658}{0.0414} \approx 64 \ \Rightarrow \ EQ_{\min} \approx 0.031
> $$
>
> Yani **EQ ≈ 0.03 tamamen normaldir ve sınır tabaka ağının doğal sonucudur.**
> v1'deki "> 0.30" eşiği kusursuz bir ağı hatalı diye eletirdi.
> Ağın gerçekten yapılandırılmış olup olmadığının göstergesi **Orthogonal Quality**'dir,
> Element Quality değil.

**Orthogonal Quality 0.95'in altına düşerse** mapped ağ tam yapılandırılmış değildir —
muhtemelen bir yüz mapped yapılamamış ve serbest ağla dolmuştur. Face Meshing'in yanında
uyarı simgesi var mı bak.

**Aspect Ratio 64 normaldir ve sorun değildir.** Raporda: *"Yüksek en-boy oranlı hücreler,
duvara dik yönde sınır tabakayı çözmek amacıyla bilinçli olarak kullanılmıştır."*

### 9.1 Gözle doğrulama — ATLAMA

1. Alt duvara zoom → hücreler duvara doğru **incelmeli**. Kalınlaşıyorsa bias tipi yanlış.
2. Kaburganın iki üst köşesine zoom → orada da sıklaşma olmalı.
3. Kanal orta yüksekliği → hücreler en kalın orada.
4. Blok sınırları ($x{=}12.5$, $x{=}17.5$, $y{=}5$) → çizgiler **kesintisiz** geçmeli.
   Kırılma veya kayma varsa Share Topology tutmamıştır.

---

## 10. GCI için üç ağ seviyesi (Celik 2008)

Bias faktörleri **aynı kalır**, sadece bölme sayıları $\sqrt{2}$ ile ölçeklenir.

| Grup | Kaba | Orta | İnce |
|---|---|---|---|
| V1 | 35 | **50** | 70 |
| V2 | 57 | **80** | 113 |
| H1 | 35 | **50** | 70 |
| H2 | 21 | **30** | 42 |
| H3 | 99 | **140** | 198 |
| **Eleman** | ~13 500 | **~27 100** | ~53 800 |

$$
r_{21} = \left( \frac{N_{\text{ince}}}{N_{\text{orta}}} \right)^{1/2} = \left( \frac{53\,800}{27\,100} \right)^{1/2} \approx 1.41
$$

Celik'in $r > 1.3$ koşulu sağlanıyor. `scripts/mesh_independence.py` (Ahmed body'den)
bu üç sonuçla doğrudan çalışır.

> Bölme sayıları $\sqrt{2}$ ile ölçeklenirken bias faktörü sabit tutulduğu için
> **ilk hücre boyu da değişir** (kaba ağda daha kalın). Kaba ağda $y^+ > 1$ çıkarsa bu
> beklenen bir durumdur; GCI hesabında sorun değil, ama raporda belirtilmeli.

**Önce orta seviye kurulacak.** Diğer ikisi Aşama 1 doğrulaması tamamlandıktan sonra.

---

## 11. Fluent tarafında Gün 1'den değişenler

Ana dosya Bölüm 4'teki tarif geçerli, dört istisna:

**a) Debi değişmez.** $\dot m = 0.537$ kg/s. Periyodik düzlem ($x{=}0$) tam 50 mm açık,
kaburga oraya değmiyor → $Re = 30\,010$ ✓, yığın hız $\rho$'ya bağlı (Bölüm 1 notu).

**b) Basınç gradyanı ilk tahmini yukarı.** Düz kanalda 10.22 Pa/m'de oturmuştu;
$p/e{=}9$, 1s için $f/f_0 \approx 4{-}5$ bekleniyor:

$$
\left. \frac{\Delta p}{L} \right|_{\text{ilk tahmin}} \approx 40 \ \text{Pa/m}
$$

Relaxation factor **0.5 → 0.3**. Form direnci devreye girince gradyan ayarı salınımlı olur.

**c) ⚠️ Sürtünme faktörü artık kayma gerilmesinden hesaplanamaz.** Ana dosya Bölüm 5.3'teki
kuvvet dengesi kaburganın ön/arka yüzündeki **basınç kuvvetini** içermiyor.

> 🔧 **Birincil yol: Fluent'in kendi raporladığı gradyanı oku.** Kütle debisi verilmiş
> translational periyodik akışta Fluent $\Delta p/L$'yi zaten çözümün bir parçası olarak
> hesaplar ve Periodic Conditions panelinde / TUI'de raporlar. Elle hesap yapmaya gerek yok.

**İkincil yol (çapraz kontrol):** Reports → Forces → Force Vector $(1, 0, 0)$ →
**tüm duvar zone'ları** (`bottom-wall`, `rib-wall`, `top-wall`).

> 🔧 **Payda düzeltildi.** Periyodik momentum kaynağı **akışkan hacmine** etki eder,
> kaburgayı da içeren blok hacmine değil. Domen üzerinde momentum dengesi:
>
> $$
> \sum F_{x,\text{duvar}} = \frac{\Delta p}{L} \cdot V_{\text{akışkan}}
> $$
>
> $$
> \frac{\Delta p}{L} = \frac{F_x}{V_{\text{akışkan}}} = \frac{F_x}{2.225 \times 10^{-3}} \ \left[ \text{m}^3 \right]
> $$
>
> v1'deki $A_{\text{kesit}} \cdot L = 0.05 \times 0.045 = 2.25 \times 10^{-3}$ **yanlıştı**
> — kaburganın kapladığı 25 mm²'yi düşmüyordu. %1.1 hata, $f/f_0$'ı %1 mertebesinde
> karşılaştıracağımız için önemli. (2B Fluent kuvvetleri birim derinlik için raporlar,
> yani $V_{\text{akışkan}} = 2225\ \text{mm}^2 \times 1\ \text{m}$.)

$$
f = \frac{(\Delta p / L) \cdot D_h}{2 \rho U_b^2} \qquad \text{(Fanning)}
$$

**Bonus:** Fluent viskoz ve basınç bileşenlerini ayrı sütunlarda verir → Rau Şekil 20'deki
"form direnci / duvar sürtünmesi" ayrıştırmasıyla doğrudan karşılaştırılabilir.
Düz kanalda olmayan ekstra bir doğrulama noktası. İki yolun sonucu %1 içinde uyuşmalı;
uyuşmuyorsa yakınsama tamamlanmamıştır.

**d) Yakınsama kriteri gevşer.** Ayrılmalı akışta steady RANS rezidüelleri 1e-5 civarında
takılır ve küçük genlikli salınır. **1e-6 kovalanmayacak.** Bunun yerine üç report definition:

1. `bottom-wall` alan-ağırlıklı $T_w$
2. `rib-wall` alan-ağırlıklı $T_w$
3. Toplam $F_x$

Üçü de 200 iterasyon boyunca düz gidiyorsa yakınsamıştır. Diverjans olursa Coupled'da
pseudo-transient aç.

---

## 12. 📌 ÖNDEN KAYDEDİLEN HİPOTEZ (sonuç gelmeden yazıldı)

$k$-$\omega$ SST, ayrılmalı akışlarda yeniden yapışma mesafesini **eksik tahmin etme**
eğilimindedir.

- Rau deneysel bandı: $4.00 < X_r/e < 4.25$
- **Beklenti: 3.6 – 4.0 arası çıkması şaşırtıcı olmayacak**

Bu, sonuç geldikten sonra uydurulmuş bir açıklama değil, **önden kurulmuş bir hipotezdir.**
Raporda bu şekilde konumlandırılacak. (Ahmed body'de öğrenilen ders.)

---

## 13. ⏭️ SIRA

1. ✅ **SpaceClaim:** sketch girildi, orijin sol alt köşeye ankrajlandı
2. **SpaceClaim:** 6 yüz kontrolü → R'yi sil → Share Topology
3. **Meshing:** Analysis Type 2D kontrolü → Part kontrolü → Face Meshing → 5 edge sizing
4. **Generate** → eleman sayısı ve kalite metrikleri kontrolü (Bölüm 9)
5. **Gözle doğrulama** (Bölüm 9.1) — dört maddenin dördü de
6. Named selections (Bölüm 5)
7. Fluent kurulumu (ana dosya Bölüm 4 + bu dosya Bölüm 11)

**Paralel iş (bilgisayar başında düşünmeden yapılır):**
Şekil 15'i WebPlotDigitizer ile sayısallaştır → `01_Data/experimental/rau_fig15_pe9_1s.csv`
($p/e{=}9$, **1s** eğrisi; 2s ile karıştırma)

---

## 14. Gün 2'de öğrenilen tuzaklar (ana dosya Bölüm 10'a eklenecek)

| Tuzak | Doğrusu |
|---|---|
| Kaburgayı periyodik kenara oturtmak | İki periyodik kenar farklı uzunlukta olur, `make-periodic` reddeder |
| Kaburga konumunu rastgele seçmek | $X/e$ dikişinin nereye düştüğünü hesapla; sessiz bölgeye koy |
| **Sketch'i orijine ankrajlamamak** | Fizik değişmez ama $X/e$ formülünün sabitleri geçersiz olur. Sol alt köşe = $(0,0)$, koordinatları klavyeden gir |
| Kaburga boşluğunun 4 kenarı var sanmak | **3 kenar.** Alttaki kenar R ile birlikte silinir |
| Kaburgayı sketch'te ayrı kare olarak çizmek | Gerekmez, üç çizgi altı alanı kendiliğinden üretir |
| Tek yönlü (one-side) bias | Kenar iç yönü görünmez, ters dönebilir. **Hep iki uçta sık kullan** |
| Global Max Size vermek | Bias tasarımını kırar. Mapped ağda global sizing gereksiz |
| Capture Curvature / Proximity açık bırakmak | Edge sizing'in üstüne otomatik sıklaştırma ekler, bölme sayıları tutmaz |
| `Behavior = Soft` | ANSYS bölme sayısını global ayarlar uğruna değiştirebilir. **Hard** kullan |
| Share Topology'yi atlamak | Ağ üretilir, hata vermez, ama bloklar arası akış geçmez |
| Kaburgalı vakada $f$'i kayma gerilmesinden hesaplamak | Form direncini kaçırır. Fluent'in periyodik $\Delta p/L$ raporunu kullan |
| **Kuvvet dengesinde blok hacmini kullanmak** | Kaynak terimi **akışkan hacmine** etki eder: $V = 2225$ mm², $2250$ değil |
| **Element Quality < 0.30 diye ağı elemek** | Sınır tabaka ağında $EQ \approx 0.03$ normaldir. Ölçüt **Orthogonal Quality** |
| Ayrılmalı akışta 1e-6 rezidüel beklemek | 1e-5'te takılması normaldir; report definition'ların düzleşmesine bak |
| $U_b$ ile $\rho$'yu karıştırmak | $Re$ debiyle sabit ama $U_b$ değil. $f$ hesabında Fluent'teki $\rho$'yu kullan |

---

## 15. Claude / Claude Code için notlar

- Matematiksel ifadeler `$$ $$` blokları içinde, her adım ayrı satırda
- Bu dosyadaki hiçbir sayı "yaklaşık uygun" değil; hepsi Bölüm 7-8'deki kısıt zincirinden
  türetilmiş. Bir bölme sayısı değişecekse **zincirin tamamı yeniden kontrol edilmeli**
- Bölme sayısı değiştirmeden önce sor: bu kenar hangi bloğun karşı kenarıyla eşleşmek
  zorunda? Periyodik eşleşmeyi bozuyor mu?
- Reddedilen alternatifler (Bölüm 2.3) silinmez — aynı tartışmanın tekrar açılmasını önler
- Post-processing'de $X/e$ dönüşümü (**sketch orijine ankrajlıysa geçerli**):

```python
Xe = ((x_mm - 17.5) % 45.0) / 5.0
```

  Domen başka bir yere ankrajlıysa `17.5` yerine **kaburga arka yüzünün gerçek $x$'i**
  yazılır; `% 45` ve `/ 5` değişmez. (Örn. merkezlenmiş sketch'te sabit `-5.0` olurdu.)

- Bias hücre boyu kontrolü (ANSYS iki-uçta-bias):

```python
def two_end(L, N, BF):
    n = N // 2
    r = BF ** (1.0 / (n - 1))
    a = (L / 2) * (r - 1) / (r**n - 1)
    return a, a * r**(n - 1)     # ilk hücre, en büyük hücre
```

- Doğrulama işinin altın kuralı: deney hangi tanımı kullandıysa aynısı kullanılır
  ($Nu_0$ korelasyonu, $f$ tanımı Fanning, $D_h = 0.05$ m)
