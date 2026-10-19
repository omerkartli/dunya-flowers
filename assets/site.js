const PHONE = "905334222994";

// İstatistik (Umami, çerezsiz). Kişisel veri (ad, telefon, adres) gönderilmez.
const UMAMI_ID = "f18cc63d-43e2-44fb-b65c-728dedc0f216";
if (UMAMI_ID) {
  const sc = document.createElement("script");
  sc.defer = true; sc.src = "https://cloud.umami.is/script.js"; sc.dataset.websiteId = UMAMI_ID;
  document.head.appendChild(sc);
}
const track = (name, data) => { try { window.umami && window.umami.track(name, data); } catch (e) {} };
document.addEventListener("click", e => {
  const a = e.target.closest("a[href]"); if (!a) return;
  const yer = a.id === "fab" ? "yuzen-buton" : a.closest(".mbar") ? "alt-bar"
    : (a.closest("header") ? "ust-menu" : a.closest("footer") ? "alt-bilgi" : a.closest("section[id]")?.id) || "sayfa";
  const href = a.getAttribute("href");
  if (href.startsWith("tel:")) track("ara", { yer });
  else if (href.includes("wa.me")) track("whatsapp", { yer });
  else if (href.includes("instagram.com")) track("instagram", { yer });
  else if (href.includes("google.com/maps")) track("yol-tarifi", { yer });
  else if (a.classList.contains("btn-review")) track("yorum-yap", { yer });
});

// Özel gün sayfalarında <body data-gun="..." data-gun-adi="..."> bulunur
const GUN = document.body.dataset.gun || "", GUN_ADI = document.body.dataset.gunAdi || "";
const imgSrc = v => /^(https?:)?\//.test(v) ? v : "/" + v;
let PRODUCTS = [];

const CATS = [
  { id:"all",   label:"Tümü" },
  { id:"buket", label:"Buketler" },
  { id:"gul",   label:"Güller" },
  { id:"vazo",  label:"Vazo & Saksı" },
  { id:"ozel",  label:"Özel Tasarım" }
];

const fmt = n => n.toLocaleString("tr-TR") + " ₺";
const $ = s => document.querySelector(s);
const esc = v => String(v ?? "").replace(/[&<>"']/g, c => ({"&":"&amp;","<":"&lt;",">":"&gt;",'"':"&quot;","'":"&#39;"})[c]);

const grid = $("#grid"), filters = $("#filters");
let current = null;
const yr = $("#yr"); if (yr) yr.textContent = new Date().getFullYear();
if (grid) {

function renderFilters(active){
  if (!filters) return;
  filters.innerHTML = CATS.map(c =>
    `<button class="chip${c.id===active?" on":""}" data-cat="${c.id}">${c.label}</button>`).join("");
}
function renderGrid(cat){
  const list = PRODUCTS.map((p, i) => ({...p, i})).filter(p => cat==="all" || p.cat===cat);
  grid.innerHTML = list.map(p => `
    <article class="card">
      <div class="ph">
        <img loading="lazy" decoding="async" src="${esc(imgSrc(p.img))}" alt="${esc(p.name)} çiçek buketi">
        ${p.tag ? `<span class="tag">${esc(p.tag)}</span>` : ""}
      </div>
      <div class="body">
        <h3>${esc(p.name)}</h3>
        <p class="desc">${esc(p.desc)}</p>
        <div class="row">
          <span class="price">${p.price.toLocaleString("tr-TR")}<small>₺</small></span>
          <button class="btn btn-primary" data-order="${p.i}">Sipariş Ver</button>
        </div>
      </div>
    </article>`).join("");
}
if (filters) filters.addEventListener("click", e => {
  const b = e.target.closest("[data-cat]"); if(!b) return;
  renderFilters(b.dataset.cat); renderGrid(b.dataset.cat);
});
grid.addEventListener("click", e => {
  const b = e.target.closest("[data-order]"); if(!b) return;
  openOrder(PRODUCTS[b.dataset.order]);
});

// Modal
const overlay = $("#overlay"), form = $("#orderForm"), delivFields = $("#delivFields");
const today = new Date(); today.setMinutes(today.getMinutes() - today.getTimezoneOffset());
const todayStr = today.toISOString().slice(0,10);
$("#fDate").min = todayStr;

function openOrder(p){
  current = p;
  track("siparis-formu-acildi", { urun: p.name, fiyat: p.price, gun: GUN || "yok" });
  $("#mImg").src = imgSrc(p.img); $("#mImg").alt = p.name;
  $("#mName").textContent = p.name;
  $("#mPrice").textContent = fmt(p.price);
  $("#sumPrice").textContent = fmt(p.price);
  if(!$("#fDate").value) $("#fDate").value = todayStr;
  overlay.classList.add("open"); overlay.setAttribute("aria-hidden","false");
  document.body.style.overflow = "hidden";
  setTimeout(() => $("#fName").focus(), 50);
}
function closeOrder(){
  overlay.classList.remove("open"); overlay.setAttribute("aria-hidden","true");
  document.body.style.overflow = "";
}
$("#closeBtn").addEventListener("click", closeOrder);
overlay.addEventListener("click", e => { if(e.target===overlay) closeOrder(); });
document.addEventListener("keydown", e => { if(e.key==="Escape") closeOrder(); });

function syncMethod(){
  const delivery = form.method.value === "delivery";
  delivFields.hidden = !delivery;
  ["#fRName","#fRPhone","#fAddr"].forEach(s => $(s).required = delivery);
  $("#lDate").textContent = delivery ? "Teslimat tarihi" : "Teslim alma tarihi";
  $("#sumLabel").textContent = delivery ? "Ürün tutarı (+ teslimat)" : "Ürün tutarı";
  $("#note").textContent = delivery
    ? "Teslimat ücreti adrese göre sipariş onayında bildirilir."
    : "Siparişiniz hazır olduğunda size haber veririz.";
}
form.addEventListener("change", e => { if(e.target.name==="method") syncMethod(); });

form.addEventListener("submit", e => {
  e.preventDefault();
  const req = [...form.querySelectorAll("[required]")];
  const bad = req.find(el => !el.value.trim());
  req.forEach(el => el.style.borderColor = el.value.trim() ? "" : "#d64545");
  if(bad){ bad.focus(); return; }

  const delivery = form.method.value === "delivery";
  const d = new Date($("#fDate").value + "T00:00").toLocaleDateString("tr-TR",{day:"numeric",month:"long",weekday:"long"});
  const lines = [
    "🌸 *Yeni Sipariş – Dünya Flowers*",
    "",
    `*Ürün:* ${current.name} (${fmt(current.price)})`,
    ...(GUN_ADI ? [`*Özel gün:* ${GUN_ADI}`] : []),
    `*Teslim şekli:* ${delivery ? "Adrese gönderim" : "Gelip alacağım"}`,
    `*Tarih:* ${d}, ${$("#fTime").value}`,
    "",
    `*Sipariş veren:* ${$("#fName").value.trim()}`,
    `*Telefon:* ${$("#fPhone").value.trim()}`
  ];
  if(delivery){
    lines.push("", `*Alıcı:* ${$("#fRName").value.trim()}`, `*Alıcı tel:* ${$("#fRPhone").value.trim()}`, `*Adres:* ${$("#fAddr").value.trim()}`);
  }
  const note = $("#fNote").value.trim();
  if(note) lines.push("", `*Kart notu:* ${note}`);

  track("siparis-gonderildi", { urun: current.name, fiyat: current.price, teslim: delivery ? "adrese" : "gelip-alma", kart_notu: note ? "var" : "yok", gun: GUN || "yok" });
  window.open(`https://wa.me/${PHONE}?text=${encodeURIComponent(lines.join("\n"))}`, "_blank");
});

renderFilters("all"); syncMethod();
// Ürünler yönetim panelinden (Pages CMS) düzenlenen products.json dosyasından gelir
fetch("/products.json", {cache:"no-cache"})
  .then(r => r.json())
  .then(data => {
    const list = Array.isArray(data) ? data : (data.urunler || []);
    PRODUCTS = list.filter(p => p.active !== false && p.name && p.img && Number(p.price) > 0)
      .map(p => ({...p, price: Number(p.price)}));
    // Özel gün sayfası: panelde o güne işaretlenen ürünler; hiç işaretli yoksa tüm ürünler
    if (GUN) {
      const sec = PRODUCTS.filter(p => Array.isArray(p.gunler) && p.gunler.includes(GUN));
      if (sec.length) PRODUCTS = sec;
    }
    renderGrid("all");
    const prices = PRODUCTS.map(p => p.price);
    if (prices.length && $("#priceRange")) $("#priceRange").textContent =
      `${Math.min(...prices).toLocaleString("tr-TR")} – ${Math.max(...prices).toLocaleString("tr-TR")} ₺`;
  })
  .catch(() => { grid.innerHTML = `<p>Ürünler yüklenemedi. Lütfen sayfayı yenileyin ya da WhatsApp'tan yazın.</p>`; });
}
