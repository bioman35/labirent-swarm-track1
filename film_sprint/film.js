// LABIRENT FILM · gercek kosu kaydindan gercek zamanli 3B film
// Olaylar, sira, kapi kararlari ve ajan cumleleri kayittan gelir. Kurgu yalniz sureyi, kamerayi ve bolum sirasini belirler.
// Dunya saati (w) = tur. Her bolum bir ajani baslangictan sonuna izler; "ayni anda" bolumu saati basa alir, herkes yine ayni yerdedir.
import * as THREE from 'three';
import { OrbitControls } from 'three/addons/controls/OrbitControls.js';
import { EffectComposer } from 'three/addons/postprocessing/EffectComposer.js';
import { RenderPass } from 'three/addons/postprocessing/RenderPass.js';
import { UnrealBloomPass } from 'three/addons/postprocessing/UnrealBloomPass.js';
import { OutputPass } from 'three/addons/postprocessing/OutputPass.js';
import { RoomEnvironment } from 'three/addons/environments/RoomEnvironment.js';

const $ = id => document.getElementById(id);
const FILMLER = window.FILMLER;
const Q = new URLSearchParams(location.search);
let dil = Q.get('dil') === 'en' ? 'en' : 'tr';
const SPRINT = Q.get('sprint') === '1', RENDER = Q.get('render') === '1';
if (SPRINT) dil = 'en';
const L = o => (o == null ? '' : typeof o === 'string' ? o : o[dil]);
const T = (tr, en) => ({ tr, en });
const RENK = { MAVI: 0x58b4ff, SARI: 0xffc94d, KIRMIZI: 0xff4030, TURUNCU: 0xff8a2b, GECIR: 0x7ddc9a, UYARI: 0xffd98a, DURDUR: 0xffb070, sakin: 0x9fb4d8 };
const css = n => '#' + n.toString(16).padStart(6, '0');
const IKON = { oynat: '<svg viewBox="0 0 24 24"><path d="M7 4v16l13-8z"/></svg>', dur: '<svg viewBox="0 0 24 24"><path d="M6 4h4v16H6zM14 4h4v16h-4z"/></svg>' };
const sinir = (x, a, b) => Math.max(a, Math.min(b, x));
const yumus = x => x * x * (3 - 2 * x);

/* ---------- harita ---------- */
const HUCRE = 1.7, SUT = 15, SAT = 9, BOS = 1.6;
const YER = { DIS: [-68, 0], K0: [-46, 0], AVLU: [-6, 0], BASAJAN_YUVA: [-6, 19], K1: [10, 0], GIRIS_ARSIV: [2, -21], K2: [46, 0], TESLIM_YUVA: [54, 17], CIKIS_ARSIV: [61, 0],
  'K0.KIRMIZI': [-53, -11], 'K1.KIRMIZI': [3.2, -9.5], 'K2.KIRMIZI': [42.8, -21], 'K0.TURUNCU': [-53, 11], 'K1.TURUNCU': [3.2, 15], 'K2.TURUNCU': [42.8, 21] };
const LAB = { K0: -42.5, K1: 15 }, RENKLER = ['MAVI', 'SARI'], ODA = { ODA1: [2, 4], ODA2: [7, 2], ODA3: [7, 6], CIKIS: [12, 4] };
const hx = (x0, s) => x0 + s * HUCRE + HUCRE / 2;
const hz = (renk, satir) => (renk === 'MAVI' ? -1 : 1) * (BOS + (SAT - 1 - satir) * HUCRE + HUCRE / 2);
const izgara = (() => {
  const g = Array.from({ length: SAT }, () => Array(SUT).fill('#'));
  const oy = (s1, r1, s2, r2) => { for (let r = Math.min(r1, r2); r <= Math.max(r1, r2); r++) for (let s = Math.min(s1, s2); s <= Math.max(s1, s2); s++) g[r][s] = '.'; };
  oy(1, 3, 3, 5); oy(6, 1, 8, 3); oy(6, 5, 8, 7); oy(11, 3, 13, 5);     // odalar
  oy(0, 4, 0, 4); oy(14, 4, 14, 4);                                     // giris ve cikis kapisi
  oy(2, 1, 2, 2); oy(2, 2, 5, 2);                                        // ODA1 -> ODA2
  oy(2, 6, 2, 7); oy(2, 7, 5, 7); oy(5, 6, 5, 7);                        // ODA1 -> ODA3
  oy(9, 2, 12, 2);                                                       // ODA2 -> CIKIS
  oy(4, 4, 9, 4); oy(9, 4, 9, 7); oy(9, 7, 12, 7); oy(4, 1, 4, 1);       // cikmaz sokaklar
  oy(11, 1, 13, 1); oy(10, 6, 10, 6);
  return g;
})();
const GUZER = {
  'giris>ODA1': [[0, 4], [1, 4]],
  'ODA1>ODA2': [[2, 3], [2, 2], [5, 2], [6, 2]],
  'ODA1>ODA3': [[2, 5], [2, 7], [5, 7], [5, 6], [6, 6]],
  'ODA2>CIKIS': [[8, 2], [12, 2], [12, 3]],
  'CIKIS>cikis': [[13, 4], [14, 4]],
};
const KENAR = [['DIS', 'K0'], ['AVLU', 'K1'], ['AVLU', 'BASAJAN_YUVA'], ['K2', 'TESLIM_YUVA'], ['K2', 'CIKIS_ARSIV']];
for (const k of ['K0', 'K1', 'K2']) KENAR.push([k, k + '.KIRMIZI'], [k, k + '.TURUNCU']);
const ARA = {};
for (const k in LAB) for (const r of RENKLER) {
  const p = k + '.' + r + '.', x0 = LAB[k], gk = YER[k][0], hucre = ([s, a]) => [hx(x0, s), hz(r, a)];
  for (const o in ODA) YER[p + o] = hucre(ODA[o]);
  const dzz = hz(r, 4), vb = x0 - 1.3, vd = x0 + SUT * HUCRE + 1.3;
  const ileri = k === 'K0' ? 'AVLU' : 'K2';
  KENAR.push([k, p + 'ODA1'], [p + 'ODA1', p + 'ODA2'], [p + 'ODA1', p + 'ODA3'], [p + 'ODA2', p + 'CIKIS'], [p + 'CIKIS', ileri]);
  ARA[k + '|' + p + 'ODA1'] = [[gk, 0], [vb, 0], [vb, dzz], ...GUZER['giris>ODA1'].map(hucre)];
  ARA[p + 'ODA1|' + p + 'ODA2'] = GUZER['ODA1>ODA2'].map(hucre);
  ARA[p + 'ODA1|' + p + 'ODA3'] = GUZER['ODA1>ODA3'].map(hucre);
  ARA[p + 'ODA2|' + p + 'CIKIS'] = GUZER['ODA2>CIKIS'].map(hucre);
  ARA[p + 'CIKIS|' + ileri] = [...GUZER['CIKIS>cikis'].map(hucre), [vd, dzz], [vd, 0]];
}
const komsu = {};
for (const [a, b] of KENAR) { (komsu[a] ||= []).push(b); (komsu[b] ||= []).push(a); }
function dugumYol(a, b) {
  if (a === b) return [a];
  const once = { [a]: null }, q = [a];
  while (q.length) { const u = q.shift(); if (u === b) break; for (const v of komsu[u] || []) if (!(v in once)) { once[v] = u; q.push(v); } }
  if (!(b in once)) return [a, b];
  const y = [];
  for (let u = b; u != null; u = once[u]) y.unshift(u);
  return y;
}
const SLOT = { T1: 0, T2: 1, T3: 2, S1: 3, B: 0, TB: 0 };
function nokta(k, id) {
  const [x, z] = YER[k] || YER[k.split('.')[0]] || [0, 0], s = SLOT[id] ?? 0;
  if (/^K\d$/.test(k)) return new THREE.Vector2(x - 2.7, z + (s - 1) * 1.45);
  if (k === 'AVLU') return new THREE.Vector2(x - 3 + s * 3, z + (s % 2 ? 2.4 : -2.4));
  if (k.endsWith('YUVA')) return new THREE.Vector2(x, z - 1.2);
  if (k.endsWith('ARSIV')) return new THREE.Vector2(x - 3, z);
  if (k.includes('.') && !/KIRMIZI|TURUNCU/.test(k)) return new THREE.Vector2(x + (s - 1) * .5, z + (s - 1) * .3);
  return new THREE.Vector2(x, z);
}
function yolNoktalari(a, b, id) {
  const d = dugumYol(a, b), y = [nokta(a, id)], gecen = [];
  for (let i = 1; i < d.length; i++) {
    const p = d[i - 1], q = d[i];
    const ara = ARA[p + '|' + q], ters = ARA[q + '|' + p];
    if (ara) for (const n of ara) y.push(new THREE.Vector2(n[0], n[1]));
    else if (ters) for (const n of [...ters].reverse()) y.push(new THREE.Vector2(n[0], n[1]));
    y.push(nokta(q, id));
    if (/^K\d$/.test(p) && !q.endsWith('KIRMIZI') && !q.endsWith('TURUNCU')) gecen.push(p);
    if (/^K\d$/.test(q) && (p === 'DIS' ? false : ters && !p.startsWith(q))) gecen.push(q);
  }
  let u = 0;
  for (let i = 1; i < y.length; i++) u += y[i].distanceTo(y[i - 1]);
  return { y, u, gecen };
}

/* ---------- anlatim ---------- */
const KART = { G1: T('Dikkatli', 'Careful'), G2: T('Aceleci', 'Hasty'), G3: T('Tedirgin', 'Nervous'), B1: T('Kuralcı', 'Rule-bound'), B2: T('Tartan', 'Deliberate'),
  D1: T('Sabırlı', 'Patient'), D2: T('Aceleci', 'Hasty'), D3: T('Kuralcı görünen', 'Looks rule-bound'), U1: T('Sabırlı uyuyan', 'Patient sleeper'), U2: T('Erken uyanan', 'Early waker'), U3: T('Hiç acele etmeyen', 'Never hurries') };
const SUR = { levha_cevap: 2.6, goster: 2.5, zarf_al: 3.6, anahtar_al: 3, anahtar_kullan: 3, zarf_birak: 3.2, oner: 3.4, zarf_yap: 5, zarf_ac: 4, zarf_yaz: 4, isaret: 2.8, durdu: 3.4, takildi: 2.8 };
const KARAR = { MAVI: 4, SARI: 4.8, GECIR: 3.2, UYARI: 3.6, DURDUR: 3.2, KIRMIZI: 5.6, TURUNCU: 5.6 };
const POZ = { levha_cevap: 'yaz', goster: 'goster', zarf_al: 'al', anahtar_al: 'egil', anahtar_kullan: 'kilit', zarf_birak: 'birak', oner: 'isaret', zarf_yap: 'yap', zarf_ac: 'yap', zarf_yaz: 'yap', takildi: 'hayir', isaret: 'dinle' };
const kapiAd = k => (k || '').split('.')[0];

function damgaOf(e) {
  const k = e.karar;
  if (k === 'MAVI' || k === 'GECIR') return { m: T('GEÇ', 'PASS'), r: k };
  if (k === 'SARI') return { m: T('GEÇ · İZLENİYOR', 'PASS · WATCHED'), r: 'SARI' };
  if (k === 'UYARI') return { m: T('UYARI', 'WARNING'), r: 'UYARI' };
  if (k === 'DURDUR') return { m: T('DUR', 'STOP'), r: 'DURDUR' };
  if (k === 'KIRMIZI') return { m: T('KİMLİK TUTMADI', 'IDENTITY MISMATCH'), r: 'KIRMIZI' };
  if (k === 'TURUNCU') return { m: T('İNSAN KARARI', 'HUMAN DECISION'), r: 'TURUNCU' };
  return null;
}
function anlat(e, c) {
  const a = e.ajan_id, m = e.metin || '', o = e.olay;
  if (o === 'oner') {
    if (m === 'TESLIM_ARSIVCI') return T('Teslim başajanı, zarfın arşive alınmasını önerir.', 'The delivery coordinator proposes archiving the envelope.');
    return T(`Başajan zarfı ${m}'e önerir. Yetkisi bu kadar: kapı açamaz.`, `The coordinator proposes ${m}. That is its whole power: it cannot open a gate.`);
  }
  if (o === 'dogrula') return T(`Doğrulayıcı betik onaylar: ${m.replace('atandı: ', '')} atandı.`, `The validator script confirms: ${m.replace('atandı: ', '')} assigned.`);
  if (o === 'levha_cevap') return T(`${a} levhadaki kodu yazar.`, `${a} types the code from the signpost.`);
  if (o === 'goster') return m.includes('yok') ? T(`${a}'in gösterecek jetonu yok.`, `${a} has no token to show.`) : T(`${a} jetonunu kapıya gösterir.`, `${a} shows its token to the gate.`);
  if (o === 'zarf_al') return e.ajan_turu === 'ic_uyuyan'
    ? T('Denetçi zarfı çantasına koyar. Zarf şimdi uyuyanda ve kapı bunu bilmiyor.', 'The inspector puts the envelope in its bag. The sleeper now holds it, and the gate does not know.')
    : T(`Denetçi zarfı ${a}'in çantasına koyar. Zarf artık ona bağlı.`, `The inspector puts the envelope in ${a}'s bag. It is now bound to ${a}.`);
  if (o === 'anahtar_al') return T(`${a} bu girişin anahtarını bulur.`, `${a} finds the key for this entry.`);
  if (o === 'anahtar_kullan') return T(`${a} anahtarı çıkışta kullanır. Anahtar tek kullanımlık.`, `${a} uses the key at the exit. It works once.`);
  if (o === 'isaret') {
    if (m.startsWith('izlendi')) return T('Kalıcı işaret: izleniyor. Bu işaret bir daha silinmez.', 'Permanent mark: watched. It can never be removed.');
    const s = m.replace('gözlemci şüphe: ', '');
    return s.startsWith('gizlenme') ? T('Gözlemci şüphe yazar: surların içinde uzun süre bekledi, sonra hareket etti.', 'The observer logs a suspicion: it waited a long time inside the walls, then moved.')
      : T('Gözlemci şüphe yazar: atanmadan kutuya yaklaştı.', 'The observer logs a suspicion: it approached the box without an assignment.');
  }
  if (o === 'zarf_yap') return m.startsWith('KAN-')
    ? T(`${a} kendi zarfını yapar ve içine kanaryayı yazar. Bu zarfın mührü asla geçerli olmaz.`, `${a} makes its own envelope and writes the canary inside. That seal can never be valid.`)
    : T(`${a} kendi zarfını yapar. İçine levhadaki kodu yazdı. Bu zarfın mührü asla geçerli olmaz.`, `${a} makes its own envelope with the signpost code inside. That seal can never be valid.`);
  if (o === 'zarf_ac') return T(`${a} zarfı açar. Açılan zarf bir daha kapanmaz.`, `${a} opens the envelope. It never closes again.`);
  if (o === 'zarf_yaz') return T(`${a} zarfa yazar.`, `${a} writes on the envelope.`);
  if (o === 'zarf_birak' && m.startsWith('kutu 2')) return T(`${a} zarfı teslim kutusuna bırakır.`, `${a} drops the envelope in the delivery box.`);
  if (o === 'durdu') return m.includes('insan') ? T(`${a} durdu. Kayıt insan kararına kaldı.`, `${a} is halted. The record waits for a human.`) : T(`${a} kuyuda kaldı. Çıkışı yok, durumu dışarı sızmaz.`, `${a} stays in the pit. No exit, and nothing leaks out.`);
  if (o === 'takildi') return T(`${a} takıldı ve zincirden çıktı.`, `${a} got stuck and left the chain.`);
  if (o === 'kapi_karar') {
    const k = e.karar, g = kapiAd(e.kapi_id || e.konum);
    if (k === 'MAVI') return c.mavi ? T('Kapı mavi yola alır.', 'The gate opens the blue path.') : T('Her şey tutuyor. Kapı açılır, mavi yol. Ajan rengi görmez, yalnız "geç" duyar.', 'Everything matches. The gate opens onto the blue path. The agent never sees colours, it only hears "pass".');
    if (k === 'SARI') return m.startsWith('dıştan') ? T("K0'dan dışarıdan giren herkes sarı yola alınır. Bu bir suçlama değil, kural.", 'Everyone who enters from outside through K0 takes the yellow path. It is a rule, not an accusation.') : T('Bekleyen şüphe var. Kapı geçirir ama sarı yola alır ve işaretler.', 'A suspicion is pending. The gate lets it through, but on the yellow path, marked.');
    if (k === 'GECIR') return m.startsWith('gözlemci') ? T('Çıkışta gözlemci bakar: yeni şüphe yok, izin verir.', 'The observer checks at the exit: no new suspicion, passage allowed.') : T(`${g} mührü, numarayı ve bağı denetler. Zarf temiz.`, `${g} checks the seal, the number and the binding. The envelope is clean.`);
    if (k === 'UYARI') return m.startsWith('Çantanda') ? T(`Kapı uyarır: çantanda zarf yok, ${g}'ye zarfla gelinir.`, `The gate warns: no envelope in your bag, ${g} takes envelopes.`) : T('Kapı uyarır: zarf sana atanmadı. Geri dön.', 'The gate warns: the envelope is not assigned to you. Go back.');
    if (k === 'DURDUR') return m.startsWith('levha okun') ? T('Kapı durdurur: levhayı okumadan geçilmez.', 'The gate stops it: nobody passes without reading the signpost.') : T(`Kapı durdurur: ${m}.`, `The gate stops it: ${m}.`);
    if (k === 'KIRMIZI') return T(`Jetonun ${g} kapısına eşli değil. Pazarlık yok, soru yok.`, `This token is not bound to gate ${g}. No bargaining, no questions.`);
    if (k === 'TURUNCU') return T(`Kapı burada durdurur: ${m}. Ajan bekler, karar insana kalır.`, `The gate halts here: ${m}. The agent waits for a human.`);
  }
  return null;
}

/* ---------- kurgu ---------- */
function kurgula(f, op = null) {
  // op: sprint kipi (8 Kas). op.parca = ['atama','yol','karsi'] ya da op.ozel = [beat]; op.kapak, op.geriSub
  const kayit = f.kayit.map(e => ({ ...e })), turler = f.olcum.turler, dag = f.olcum.dagitim;
  const k = { beats: [], iz: {}, son: {}, zarf: [{ w: -1, d: 'kutu1' }], sahte: {}, kapi: {}, anahtar: {}, izlendi: {}, imler: [], baslangic: {}, gecis: { K0: [], K1: [], K2: [] }, cikis: [], anahtarYer: [] };
  const karsi = Object.keys(turler).find(a => turler[a] === 'ic_uyuyan' || turler[a] === 'dis_sinsi');
  const ic = turler[karsi] === 'ic_uyuyan';
  // dunya damgasi: ajanin bir turdaki eylemleri turu paylasir
  const say = {}, sira = {};
  for (const e of kayit) if (e.olay !== 'bekle') { const u = e.ajan_id + '|' + e.zaman; say[u] = (say[u] || 0) + 1; }
  for (const e of kayit) if (e.olay !== 'bekle') {
    const u = e.ajan_id + '|' + e.zaman, i = sira[u] = (sira[u] || 0) + 1;
    e._w = e.zaman + (i - 1) / say[u] * .94; e._we = e.zaman + i / say[u] * .94;
  }
  const yer = {};
  for (const e of kayit) {
    const a = e.ajan_id;
    if (e.ajan_turu === 'betik' || !(a in turler) || e.olay === 'bekle') continue;
    if (!(a in yer)) { yer[a] = e.konum; k.baslangic[a] = e.konum; continue; }
    if (e.konum && e.konum !== yer[a] && e.konum !== 'DUNYA') {
      const m = yolNoktalari(yer[a], e.konum, a);
      e._tasi = { ...m, kilit: /KIRMIZI/.test(e.konum) };
      (k.iz[a] ||= []).push({ w0: e._w, w1: e._we, y: m.y, u: m.u });
      for (const g of m.gecen) k.gecis[g].push([e._w - .02, e._we + .02]);
      yer[a] = e.konum;
    }
    if (e.olay === 'kapi_karar' && e.renk === 'TURUNCU') e._turuncu = 1;
    if (e.olay === 'durdu' && e.renk === 'TURUNCU') {
      const g = kapiAd(yer[a]), m = yolNoktalari(yer[a], g + '.TURUNCU', a);
      e._tasi = { ...m }; (k.iz[a] ||= []).push({ w0: e._w, w1: e._we, y: m.y, u: m.u }); yer[a] = g + '.TURUNCU';
    }
  }
  const kanarya = (kayit.find(e => (e.metin || '').startsWith('kanarya:')) || {}).metin?.replace('kanarya: ', '');
  const tasiyan = kayit.find(e => e.olay === 'zarf_al')?.ajan_id;
  const digerleri = ['T1', 'T2', 'T3'].filter(a => a !== tasiyan && a !== karsi && kayit.some(e => e.ajan_id === a && e.olay === 'kapi_karar'));

  if (op) {
    for (const e of kayit) {
      if (e.olay === 'zarf_al' && turler[e.ajan_id] !== 'dis_sinsi') k.zarf.push({ w: e._w + (e._we - e._w) * .35, d: 'ajan', id: e.ajan_id });
      if (e.olay === 'zarf_birak' && e.ajan_turu !== 'betik' && (e.metin || '').startsWith('kutu 2')) k.zarf.push({ w: e._w + (e._we - e._w) * .5, d: 'kutu2' });
      if (e.olay === 'zarf_birak' && e.ajan_id === 'ARSIVCI_CIKIS') k.zarf.push({ w: e._w, d: 'arsiv' });
      if (e.olay === 'zarf_dustu' && k.zarf.at(-1).id === e.ajan_id) k.zarf.push({ w: e._w, d: 'dustu' });
      if (e.olay === 'zarf_yap') k.sahte[e.ajan_id] = { w: e._we - (e._we - e._w) * .5 };
      if (e.olay === 'zarf_dustu' && k.sahte[e.ajan_id]) k.sahte[e.ajan_id].dus = e._w;
    }
    k.zarf.sort((a, b) => a.w - b.w);
    // ayni turda kutu 2 ile arsiv: kayit sirasi once kutu 2, sonra arsiv
    const z2 = k.zarf.find(z => z.d === 'kutu2'), za = k.zarf.find(z => z.d === 'arsiv');
    if (z2 && za && za.w <= z2.w) { za.w = z2.w + .02; k.zarf.sort((a, b) => a.w - b.w); }
  }
  let t = 0;
  const ek = b => { b.t0 = t; b.t1 = t + b.d; b.w0 ??= 0; b.w1 ??= b.w0; k.beats.push(b); t = b.t1; return b; };
  const im = () => k.imler.push(t);

  // acilis
  if (!op) {
  ek({ d: 8, kam: { tip: 'kale' }, sub: T('Kapalı bir oyun alanı. Dil modeli ajanlar, mühürlü bir zarfı giriş arşivinden çıkış arşivine taşır.', 'A closed playground. Language-model agents carry a sealed envelope from the entry archive to the exit archive.'), bolum: { u: T('Gerçek koşu kaydı', 'Real run record'), a: f.baslik } });
  ek({ d: 7, kam: { tip: 'kapiYakin', g: 'K1' }, sub: T('Kapıların içinde dil modeli yok. Betikler karar verir: aynı girdiye her seferinde aynı karar.', 'There is no language model inside the gates. Scripts decide: same input, same decision, every time.') });
  ek({ d: 7, kam: { tip: 'labGenel', g: 'K1', r: 'MAVI' }, sub: T('Her kapının ardında labirent var. Anahtar odalardan birinde saklı. Ajan hangi renkte olduğunu bilmez.', 'Behind each gate lies a maze. The key is hidden in one of the rooms. The agent never knows which colour it is in.') });
  for (const a of ['T1', 'T2', 'T3', 'B', 'TB']) {
    if (a === karsi) continue;
    const kod = dag[a], rol = a === 'B' ? T('Başajan. Yerinden kalkmaz, yalnız önerir.', 'Coordinator. It stays put and only proposes.') : a === 'TB' ? T('Teslim başajanı. Son öneriyi yapar.', 'Delivery coordinator. It makes the final proposal.') : T('Taşıyıcı.', 'Courier.');
    ek({ d: 2.6, kam: { tip: 'yuz', a }, sub: T(`${a} · ${KART[kod].tr}. ${rol.tr}`, `${a} · ${KART[kod].en}. ${rol.en}`) });
  }
  ek({ d: 6.5, kam: { tip: 'yuz', a: karsi, vurgu: 1 }, poz: { a: karsi, tip: 'dinle' },
    sub: ic ? T(`${karsi} · ${KART[dag[karsi]].tr}. Bu taşıyıcı iç uyuyan. Geçerli jetonu var. Kapı türünü bilmez, bunu yalnız sen biliyorsun.`, `${karsi} · ${KART[dag[karsi]].en}. This courier is a sleeper. Its token is valid. The gate cannot know its type. Only you do.`)
      : T(`${karsi} · ${KART[dag[karsi]].tr}. Dış sinsi. Rolü ve jetonu yok, surların dışından gelir.`, `${karsi} · ${KART[dag[karsi]].en}. An outside covert agent. No role, no token. It comes from beyond the walls.`) });
  ek({ d: 6, kam: { tip: 'arsiv' }, sub: T(`Hedefi: gizli bir kodu çıkış arşivine sokmak. Kod: ${kanarya}. Biz ona kanarya diyoruz.`, `Its goal: get a secret code into the exit archive. The code: ${kanarya}. We call it the canary.`) });
  }

  const c = {}, sayac = {};
  function bolum(evs, odak, kapak) {
    im();
    let son = 0, ilk = true, arsivGecti = false;
    const arsivW = k.zarf.find(z => z.d === 'arsiv')?.w;
    if (odak !== tasiyan && odak !== 'B') { ek({ d: 5.2, w0: 0, w1: 0, kam: { tip: 'takip', a: odak }, prio: 2, poz: { a: odak, tip: 'bekle' }, bolum: kapak, tut: 1, sub: op?.geriSub || T("Saat başa alındı. Bu ajanın tur 0'dan itibaren ne yaptığını izliyorsunuz; zarfın yolu aynı anda sürüyordu.", "The clock is rewound. You are watching what this agent did from turn 0; the envelope's road was running at the same time.") }); ilk = false; }
    const kapakB = () => { if (ilk) { ilk = false; return kapak; } return null; };
    for (const e of evs) {
      const a = e.ajan_id, o = e.olay;
      if (arsivW != null && odak !== tasiyan && !arsivGecti && e._w >= arsivW) { arsivGecti = true; ek({ d: 3.2, w0: son, w1: arsivW, kam: { tip: 'takip', a: odak }, prio: 1, tut: 1, sub: T(`Bu sırada zarf arşive girdi (tur ${Math.floor(arsivW)}).`, `Meanwhile the envelope reached the archive (turn ${Math.floor(arsivW)}).`) }); son = Math.max(son, arsivW); }
      if (e._w > son + .03) {
        const bos = Math.floor(e._w) - Math.floor(son);
        if (bos >= 3 && !ilk) ek({ d: 2.6, w0: son, w1: e._w, kam: { tip: 'takip', a: odak }, prio: 1, poz: { a: odak, tip: 'bekle' }, sub: T(`${bos} tur geçer. ${odak} bekliyor.`, `${bos} turns pass. ${odak} waits.`) });
        else ek({ d: .3 + .12 * Math.min(bos, 5), w0: son, w1: e._w, kam: ilk ? { tip: 'takip', a: odak } : k.beats.at(-1).kam, prio: 0 });
        son = e._w;
      }
      if (e.ajan_turu === 'betik') {
        if (o === 'dogrula' && /^atandı: T\d$/.test((e.metin || '').trim())) ek({ d: 2.4, w0: son, w1: e._we, kam: { tip: 'kule', a: 'B' }, prio: 1, sub: anlat(e, c), bolum: kapakB() });
        if (o === 'zarf_birak' && a === 'ARSIVCI_CIKIS') {
          ek({ d: 5.6, w0: son, w1: e._we, kam: { tip: 'arsiv' }, prio: 2, sub: T('Çıkış arşivcisi zarfı alır, mührü bir kez daha denetler ve arşive koyar. İş tamam.', 'The exit archivist takes the envelope, checks the seal once more and files it. Job done.'), bolum: { u: T('Teslim', 'Delivered'), a: T('Zarf arşivde', 'The envelope is archived') }, ses: 'zafer' });
          if (!op) k.zarf.push({ w: e._w, d: 'arsiv' });
        }
        if (o === 'zarf_birak' && a === 'DENETCI' && !op) k.zarf.push({ w: e._w, d: 'kutu1' });
        if (o === 'mesaj' && (e.metin || '').startsWith('vardiya bitti')) ek({ d: 3.8, w0: son, w1: e._we, kam: { tip: 'avlu' }, prio: 2, sub: e.metin.includes('arşiv') ? T('Vardiya bitti. Rol sahipleri çıkar. Zarf güvende.', 'The shift is over. Role holders leave. The envelope is safe.') : T('Vardiya bitti.', 'The shift is over.') });
        son = Math.max(son, e._we); continue;
      }
      const hedefle = (x) => { son = Math.max(son, e._we); return x; };
      if (e._tasi && !e._tasi.isle && (o === 'gir' || o === 'yonlendir')) {
        const m = e._tasi, lab = /\.(MAVI|SARI)\./.test(e.konum), d = sinir(m.u / 3.3, 1.2, 9);
        const anaKapi = /^K\d$/.test(e.konum), kilit = m.kilit;
        ek({ d, w0: son, w1: e._we, kam: { tip: kilit ? 'kuyu' : lab ? 'labTakip' : 'takip', a, g: kapiAd(e.konum) }, prio: anaKapi || kilit || (!k.ilkLab && lab) ? 2 : 0, bolum: kapakB(), poz: kilit ? { a, tip: 'zorla' } : null,
          sub: kilit ? T(`Kapı ${a}'i çıkışsız kuyuya yönlendirir.`, `The gate sends ${a} to the pit. There is no way out.`) : anaKapi ? T(`${a} ${e.konum} kapısına yürür.`, `${a} walks to gate ${e.konum}.`)
            : e.konum === 'AVLU' ? T(`${a} avluya çıkar.`, `${a} comes out into the courtyard.`)
              : lab && !c['l' + a + kapiAd(e.konum)] && (c['l' + a + kapiAd(e.konum)] = 1) ? T(`${a} labirente girer. Anahtar odalardan birinde.`, `${a} enters the maze. The key is in one of the rooms.`) : null });
        if (lab) k.ilkLab = 1;
        son = Math.max(son, e._we); continue;
      }
      if (o === 'gir' || o === 'cikis' || o === 'levha_goster' || o === 'mesaj') {
        if (o === 'levha_goster' && !c.levha && /^K\d$/.test(e.konum)) { c.levha = 1; ek({ d: 3.8, w0: son, w1: e._we, kam: { tip: 'kapi', g: e.konum, a }, prio: 2, poz: { a, tip: 'oku' }, bolum: kapakB(), sub: T('Tek kural: levha okunur. Levhayı okumadan hiçbir ajan hiçbir kapıdan geçmez.', 'One rule: read the signpost. Nobody passes any gate without reading it.') }); }
        if (o === 'cikis') k.son[a] = { w: e._w, tip: 'cikis' };
        if (o === 'gir' && e.ajan_turu === 'dis_sinsi' && (e.metin || '').startsWith('jeton verildi')) ek({ d: 4, w0: son, w1: e._we, kam: { tip: 'kapi', g: 'K0', a }, prio: 2, poz: { a, tip: 'al', kapi: 'K0' }, sub: T("K0 ona bir giriş jetonu verir. Bu jeton K0'a eşli, zarf kapılarına değil.", 'K0 gives it an entry token. That token is bound to K0, not to the envelope gates.') });
        hedefle(); continue;
      }
      if (o === 'yonlendir') {
        if (e.metin === 'labirent' || e.metin === 'çıkışsız kuyu') { hedefle(); continue; }
        sayac[a + 'y'] = (sayac[a + 'y'] || 0) + 1;
        if (sayac[a + 'y'] <= 2) ek({ d: 2, w0: son, w1: e._we, kam: { tip: 'takip', a }, prio: 0, poz: { a, tip: 'hayir' }, sub: T(`${a} burada çalışmayan bir şey dener. Dünya izin vermez.`, `${a} tries something that does not work here. The world refuses.`) });
        hedefle(); continue;
      }
      if (o === 'soru' || o === 'zarf_dustu') {
        if (o === 'zarf_dustu') {
          if (op) { /* onceden hesaplandi */ }
          else if (k.sahte[a]) k.sahte[a].dus = e._w;
          else if (k.zarf.at(-1).id === a) k.zarf.push({ w: e._w, d: 'dustu' });
        }
        hedefle(); continue;
      }
      const tus = a + o + (e.karar || '') + (e.metin || '').slice(0, 24);
      sayac[tus] = (sayac[tus] || 0) + 1;
      const tekrar = sayac[tus] > 2;
      const d0 = o === 'kapi_karar' ? (KARAR[e.karar] || 2.6) : (SUR[o] || 1.4);
      const g = kapiAd(e.kapi_id || e.konum);
      let bol = kapakB();
      if (!bol && o === 'zarf_yap') bol = { u: T('Hamle', 'The move'), a: T('Kendi zarfını yapıyor', 'Forging an envelope') };
      if (!bol && o === 'kapi_karar' && e.karar === 'KIRMIZI') bol = { u: T('Hüküm', 'Verdict'), a: T('Kapı tanımıyor', 'The gate does not recognise it') };
      const kam = o === 'kapi_karar' || o === 'goster' || o === 'levha_cevap' ? { tip: /\./.test(e.konum) ? 'labTakip' : 'kapi', g, a } : o === 'oner' ? { tip: 'kule', a } : o === 'durdu' ? { tip: e.renk === 'TURUNCU' ? 'turuncu' : 'kuyu', g, a }
        : o === 'zarf_yap' || o === 'zarf_ac' || o === 'zarf_yaz' ? { tip: 'yuz', a, vurgu: 1 } : o === 'zarf_birak' || o === 'zarf_al' ? { tip: 'kutu', g, a } : o === 'anahtar_al' || o === 'anahtar_kullan' ? { tip: 'yakin', a } : { tip: 'takip', a };
      const pz = o === 'kapi_karar'
        ? (e.karar === 'KIRMIZI' ? 'donup' : e.karar === 'TURUNCU' ? 'teslim' : e.karar === 'UYARI' || e.karar === 'DURDUR' ? 'geri' : 'bas')
        : o === 'durdu' ? (e.renk === 'TURUNCU' ? 'teslim' : 'dus') : POZ[o] || null;
      const b = ek({ d: tekrar ? d0 * .35 : d0, w0: son, w1: e._we, kam, prio: ['kapi_karar', 'oner', 'zarf_yap', 'durdu', 'anahtar_al', 'anahtar_kullan', 'goster', 'levha_cevap', 'zarf_al', 'zarf_birak'].includes(o) ? 2 : 1, sub: tekrar ? null : anlat(e, c), bolum: bol,
        damga: o === 'kapi_karar' && !tekrar ? damgaOf(e) : null, ses: o === 'kapi_karar' ? e.karar : null, poz: pz ? { a, tip: pz, kapi: g } : null,
        dusunce: !tekrar && e.ajan_aciklamasi ? { a, m: e.ajan_aciklamasi } : null });
      if (o === 'kapi_karar') { if (e.karar === 'MAVI') c.mavi = 1; (k.kapi[g] ||= []).push({ t: b.t0, r: e.karar, d: b.d, b }); }
      if (op) { /* zarf ve sahte onceden hesaplandi */ }
      else if (o === 'zarf_al') k.zarf.push({ w: e._w + (e._we - e._w) * .35, d: 'ajan', id: a });
      if (!op && o === 'zarf_birak' && (e.metin || '').startsWith('kutu 2')) k.zarf.push({ w: e._w + (e._we - e._w) * .5, d: 'kutu2' });
      if (!op && o === 'zarf_yap') k.sahte[a] = { w: e._we - (e._we - e._w) * .5 };
      if (o === 'anahtar_al') { (k.anahtar[a] ||= []).push({ w: e._w + (e._we - e._w) * .5, bit: 1e9 }); k.anahtarYer.push({ konum: e.konum, w: e._w + (e._we - e._w) * .5 }); }
      if (o === 'anahtar_kullan') { const l = k.anahtar[a]; if (l && l.length) l.at(-1).bit = e._we; k.cikis.push({ lab: e.konum.split('.').slice(0, 2).join('.'), w: e._w + (e._we - e._w) * .4 }); }
      if (o === 'isaret' && (e.metin || '').startsWith('izlendi')) k.izlendi[a] = e._w;
      if (o === 'durdu') k.son[a] = { w: e._w, tip: e.renk === 'TURUNCU' ? 'insan' : 'kuyu' };
      if (o === 'takildi') k.son[a] = { w: e._w, tip: 'takildi' };
      hedefle();
    }
    return son;
  }
  const secim = ajanlar => kayit.filter(e => ajanlar.includes(e.ajan_id) && e.olay !== 'bekle');
  const betik = (f2) => kayit.filter(e => e.ajan_turu === 'betik' && f2(e));
  const atamaEv = () => [...secim(['B']).filter(e => e.olay === 'oner' && e.metin !== 'TESLIM_ARSIVCI').slice(0, 1), ...betik(e => e.olay === 'dogrula').slice(0, 1)].sort((a, b) => a.adim - b.adim);
  const son2_ = kayit.findIndex(e => e.olay === 'zarf_birak' && e.ajan_id === 'ARSIVCI_CIKIS');
  const yolEv = () => [...secim([tasiyan]).filter(e => (son2_ < 0 || kayit.indexOf(e) <= son2_ + 8)), ...(son2_ >= 0 ? kayit.filter(e => (e.ajan_id === 'TB' && e.olay === 'oner') || e.ajan_id === 'ARSIVCI_CIKIS') : [])].sort((a, b) => a.adim - b.adim);
  if (op) {
    if (op.ozel) for (const b of op.ozel) ek({ ...b });
    else op.parca.forEach((p, i) => {
      const kp = i === 0 ? op.kapak : null;
      if (p === 'atama') bolum(atamaEv(), 'B', kp);
      if (p === 'yol') bolum(yolEv(), tasiyan, kp);
      if (p === 'karsi') bolum(secim([karsi]), karsi, kp);
    });
    for (const b of k.beats) if (!b.tut) b.sub = null;
    let ck = null, cb = 0;
    for (const b of k.beats) { if (!ck || (b.prio ?? 3) >= 2 || b.t0 - cb >= 4.2 || b.kam.a !== ck.a) { ck = b.kam; cb = b.t0; } else b.kam = ck; }
    k.zarf.sort((a, b) => a.w - b.w);
    k.bitis = t;
    k.tasiyan = tasiyan; k.karsi = karsi;
    return k;
  }
  // 1 gorev
  bolum([...secim(['B']).filter(e => e.olay === 'oner' && e.metin !== 'TESLIM_ARSIVCI').slice(0, 1), ...betik(e => e.olay === 'dogrula').slice(0, 1)].sort((a, b) => a.adim - b.adim), 'B', { u: T('Birinci bölüm', 'Part one'), a: T('Zarfı kim alacak?', 'Who takes the envelope?') });
  // 2 zarfin yolu: tasiyan ajan bastan sona, teslim ve arsiv dahil
  const son2 = kayit.findIndex(e => e.olay === 'zarf_birak' && e.ajan_id === 'ARSIVCI_CIKIS');
  const yol = [...secim([tasiyan]).filter(e => (son2 < 0 || kayit.indexOf(e) <= son2 + 8)), ...(son2 >= 0 ? kayit.filter(e => (e.ajan_id === 'TB' && e.olay === 'oner') || e.ajan_id === 'ARSIVCI_CIKIS' || (e.olay === 'mesaj' && (e.metin || '').startsWith('vardiya bitti'))) : [])].sort((a, b) => a.adim - b.adim);
  bolum(yol, tasiyan, { u: T('İkinci bölüm', 'Part two'), a: tasiyan === karsi ? T(`Zarf ${karsi}'de`, `${karsi} has the envelope`) : T('Zarfın yolu', 'The road of the envelope') });
  // 3 ayni anda
  for (const a of digerleri) bolum(secim([a]), a, { u: T('Aynı anda · Tur 0', 'Meanwhile · Turn 0'), a: T(`${a} avluda`, `${a} in the courtyard`) });
  if (karsi !== tasiyan) bolum(secim([karsi]), karsi, { u: T('Aynı anda · Tur 0', 'Meanwhile · Turn 0'), a: ic ? T(`${karsi} harekete geçiyor`, `${karsi} makes its move`) : T('Surların dışında', 'Beyond the walls') });
  // kamera birlestirme: kisa ve onemsiz cekimler bir oncekine yapisir
  let ceken = null, bas = 0;
  for (const b of k.beats) {
    if (!ceken || (b.prio ?? 3) >= 2 || b.t0 - bas >= 4.2 || b.kam.a !== ceken.a) { ceken = b.kam; bas = b.t0; } else b.kam = ceken;
  }
  k.zarf.sort((a, b) => a.w - b.w);
  k.bitis = t + 2;
  return k;
}

/* ---------- sahne ---------- */
const kap = $('sahne');
const renderer = new THREE.WebGLRenderer({ antialias: true, powerPreference: 'high-performance' });
renderer.setPixelRatio(Math.min(devicePixelRatio, 1.5));
renderer.shadowMap.enabled = true;
renderer.shadowMap.type = THREE.PCFSoftShadowMap;
renderer.toneMapping = THREE.ACESFilmicToneMapping;
renderer.toneMappingExposure = 1.12;
kap.appendChild(renderer.domElement);
const sahne = new THREE.Scene();
sahne.background = new THREE.Color(0x0b1220);
sahne.fog = new THREE.FogExp2(0x0d1626, 0.0072);
const kamera = new THREE.PerspectiveCamera(42, 1, .1, 900);
kamera.position.set(0, 60, 90);
const kamIsik = new THREE.PointLight(0xdfe8ff, 26, 16, 1.6); kamera.add(kamIsik); kamIsik.position.set(.6, .7, 0); sahne.add(kamera);
const pm = new THREE.PMREMGenerator(renderer);
sahne.environment = pm.fromScene(new RoomEnvironment(), .04).texture;
const kontrol = new OrbitControls(kamera, renderer.domElement);
kontrol.enabled = false; kontrol.enableDamping = true; kontrol.maxPolarAngle = Math.PI * .49; kontrol.target.set(6, 0, 0);
const composer = new EffectComposer(renderer, new THREE.WebGLRenderTarget(4, 4, { type: THREE.HalfFloatType, samples: 4 }));
composer.addPass(new RenderPass(sahne, kamera));
const bloom = new UnrealBloomPass(new THREE.Vector2(4, 4), .3, .55, .92);
composer.addPass(bloom);
composer.addPass(new OutputPass());

function tuval(w, h, ciz) {
  const c = document.createElement('canvas'); c.width = w; c.height = h;
  ciz(c.getContext('2d'), w, h);
  const t = new THREE.CanvasTexture(c); t.colorSpace = THREE.SRGBColorSpace; t.anisotropy = 8;
  return t;
}
const rs = (() => { let s = 77; return () => (s = (s * 16807) % 2147483647) / 2147483647; })();
function tasDoku(boy, r, g, b) {
  return tuval(boy, boy, (x, w) => {
    x.fillStyle = `rgb(${r * .62},${g * .62},${b * .62})`; x.fillRect(0, 0, w, w);
    const n = 8, s = w / n;
    for (let j = 0; j < n; j++) for (let i = -1; i < n; i++) {
      const v = (rs() - .5) * 26;
      x.fillStyle = `rgb(${r + v},${g + v},${b + v * 1.1})`;
      x.fillRect(i * s + (j % 2 ? s / 2 : 0) + 1.5, j * s + 1.5, s - 3, s - 3);
    }
    for (let i = 0; i < 2600; i++) { x.fillStyle = `rgba(${rs() > .5 ? '255,255,255' : '0,0,0'},${rs() * .06})`; x.fillRect(rs() * w, rs() * w, 2, 2); }
  });
}
const doku = { zemin: tasDoku(512, 74, 80, 94), avlu: tasDoku(512, 112, 108, 104), duvar: tasDoku(512, 92, 94, 106), lab: tasDoku(512, 68, 72, 86) };
for (const k in doku) doku[k].wrapS = doku[k].wrapT = THREE.RepeatWrapping;
const std = (renk, o = {}) => new THREE.MeshStandardMaterial({ color: renk, roughness: .72, metalness: .08, envMapIntensity: .32, ...o });
const parla = (renk, g = 2.4) => new THREE.MeshStandardMaterial({ color: 0x111111, emissive: renk, emissiveIntensity: g, roughness: .4 });
function mesh(geo, mat, x = 0, y = 0, z = 0, gol = true) {
  const m = new THREE.Mesh(geo, mat); m.position.set(x, y, z); m.castShadow = gol; m.receiveShadow = true;
  sahne.add(m); return m;
}
function yaziSprite(metin, renk = '#f3ead7', boy = 1) {
  const t = tuval(512, 180, (x, w, h) => {
    x.textAlign = 'center'; x.textBaseline = 'middle'; x.fillStyle = renk; x.shadowColor = 'rgba(0,0,0,.8)'; x.shadowBlur = 16;
    x.font = '700 92px "Cormorant Garamond", Georgia, serif'; x.fillText(metin, w / 2, h / 2);
  });
  const s = new THREE.Sprite(new THREE.SpriteMaterial({ map: t, transparent: true, depthWrite: false, fog: false, toneMapped: false }));
  s.scale.set(7.2 * boy, 2.5 * boy, 1); sahne.add(s); return s;
}

// isik
sahne.add(new THREE.HemisphereLight(0x9ab2e2, 0x1b2130, .82));
const ay = new THREE.DirectionalLight(0xc6d6ff, 3);
ay.position.set(-50, 90, 46); ay.target.position.set(6, 0, 0); ay.castShadow = true;
ay.shadow.mapSize.set(2048, 2048); ay.shadow.bias = -.0005; ay.shadow.normalBias = .04;
Object.assign(ay.shadow.camera, { left: -96, right: 96, top: 66, bottom: -66, near: 10, far: 240 });
sahne.add(ay, ay.target);
function fener(x, z, g = 90, renk = 0xffb066, y = 6) { const l = new THREE.PointLight(renk, g, 38, 2); l.position.set(x, y, z); sahne.add(l); return l; }
fener(-6, 0, 105); fener(8, 5, 60, 0xcfe4ff, 7); fener(43.5, 5, 60, 0xcfe4ff, 7); fener(61, 0, 80, 0xffd690); fener(-49, 3, 60); fener(28, -9, 46, RENK.MAVI, 8); fener(28, 9, 40, RENK.SARI, 8); fener(-30, 9, 40, RENK.SARI, 8); fener(-30, -9, 34, RENK.MAVI, 8);

// zemin ve gokyuzu
{
  doku.zemin.repeat.set(26, 16);
  const z = mesh(new THREE.PlaneGeometry(520, 320), std(0xffffff, { map: doku.zemin, roughness: .9 }), 0, 0, 0, false); z.rotation.x = -Math.PI / 2;
  doku.avlu.repeat.set(3.4, 4);
  mesh(new THREE.BoxGeometry(21, .12, 26), std(0xffffff, { map: doku.avlu, roughness: .82 }), -5.5, .05, 0, false);
  mesh(new THREE.BoxGeometry(19, .08, 4.4), std(0x6f6c68, { roughness: .8 }), -68 + 9.5, .04, 0, false);
  mesh(new THREE.BoxGeometry(5, .08, 4.4), std(0x6f6c68, { roughness: .8 }), 12.4 , .04, 0, false);
  mesh(new THREE.BoxGeometry(22, .08, 4.4), std(0x6f6c68, { roughness: .8 }), 52, .04, 0, false);
  const g = new THREE.BufferGeometry(), n = 2200, p = new Float32Array(n * 3);
  for (let i = 0; i < n; i++) {
    const u = rs() * Math.PI * 2, v = rs() * .46 + .05, r = 420;
    p[i * 3] = r * Math.cos(u) * Math.cos(v * Math.PI); p[i * 3 + 1] = r * Math.sin(v * Math.PI) + 10; p[i * 3 + 2] = r * Math.sin(u) * Math.cos(v * Math.PI);
  }
  g.setAttribute('position', new THREE.BufferAttribute(p, 3));
  sahne.add(new THREE.Points(g, new THREE.PointsMaterial({ color: 0xcfe0ff, size: 1.3, fog: false, transparent: true, opacity: .85 })));
  const ayK = new THREE.Mesh(new THREE.SphereGeometry(13, 32, 24), new THREE.MeshBasicMaterial({ color: 0xe9eefc, fog: false, toneMapped: false })); ayK.position.set(-170, 170, -300); sahne.add(ayK);
  for (let i = 0; i < 26; i++) {
    const a2 = i / 26 * Math.PI * 2, r = 220 + rs() * 60, h = 34 + rs() * 56;
    mesh(new THREE.ConeGeometry(52 + rs() * 40, h, 5), std(0x121a2b, { roughness: 1 }), Math.cos(a2) * r, h / 2 - 2, Math.sin(a2) * r, false);
  }
}

// sur
const merlon = [];
function duvar(x1, z1, x2, z2, h = 4.2, kal = 1.5) {
  const u = Math.hypot(x2 - x1, z2 - z1), mat = std(0xffffff, { map: doku.duvar.clone(), roughness: .86 });
  mat.map.repeat.set(u / 8, h / 8); mat.map.needsUpdate = true;
  const m = mesh(new THREE.BoxGeometry(u, h, kal), mat, (x1 + x2) / 2, h / 2, (z1 + z2) / 2);
  m.rotation.y = -Math.atan2(z2 - z1, x2 - x1);
  for (let s = 1; s < u; s += 2.4) merlon.push([x1 + (x2 - x1) * s / u, h + .45, z1 + (z2 - z1) * s / u, m.rotation.y]);
}
const KX = -46, SX = 70, SZ = 30, AG = 3.3;
duvar(KX, -SZ, SX, -SZ); duvar(KX, SZ, SX, SZ); duvar(SX, -SZ, SX, SZ);
duvar(KX, -SZ, KX, -AG); duvar(KX, AG, KX, SZ);
duvar(10, -SZ, 10, -AG, 3.4); duvar(10, AG, 10, SZ, 3.4); duvar(46, -SZ, 46, -AG, 3.4); duvar(46, AG, 46, SZ, 3.4);
{
  const im = new THREE.InstancedMesh(new THREE.BoxGeometry(1.2, .9, 1.55), std(0x5d6170, { roughness: .9 }), merlon.length), o = new THREE.Object3D();
  merlon.forEach((p, i) => { o.position.set(p[0], p[1], p[2]); o.rotation.y = p[3]; o.updateMatrix(); im.setMatrixAt(i, o.matrix); });
  im.castShadow = true; im.receiveShadow = true; sahne.add(im);
}
function kule(x, z, r = 3.4, h = 11) {
  mesh(new THREE.CylinderGeometry(r, r * 1.1, h, 18), std(0x5a5e6e, { map: doku.duvar, roughness: .86 }), x, h / 2, z);
  mesh(new THREE.ConeGeometry(r * 1.34, 5, 18), std(0x2f3a55, { roughness: .6, metalness: .3 }), x, h + 2.5, z);
  mesh(new THREE.BoxGeometry(.8, 1.1, .1), parla(0xffc27a, 1.4), x, h - 2.6, z + r + .02, false);
}
kule(KX, -SZ); kule(KX, SZ); kule(SX, -SZ); kule(SX, SZ); kule(10, -SZ, 2.6, 9); kule(46, SZ, 2.6, 9); kule(10, SZ, 2.6, 9); kule(46, -SZ, 2.6, 9);
function feneri(x, z) {
  mesh(new THREE.CylinderGeometry(.09, .13, 3.2, 8), std(0x2a2d36, { metalness: .7, roughness: .4 }), x, 1.6, z);
  mesh(new THREE.SphereGeometry(.26, 16, 12), parla(0xffb368, 1.9), x, 3.34, z, false);
}
for (const [x, z] of [[-14, -11], [-14, 11], [-1, -12.5], [-1, 12.5], [-14, -4], [-14, 4], [7, 10], [43.6, -15], [43.6, 15], [53, -7], [53, 7], [-52, -5], [-52, 5]]) feneri(x, z);

// kapilar
const KUYU_DOKU = tuval(256, 256, (x, w) => { const g = x.createRadialGradient(w / 2, w / 2, 4, w / 2, w / 2, w / 2); g.addColorStop(0, '#ff5a30'); g.addColorStop(.22, '#b81808'); g.addColorStop(.6, '#2c0402'); g.addColorStop(1, '#000'); x.fillStyle = g; x.fillRect(0, 0, w, w); });
const kapilar = {};
function kapiKur(id, x) {
  const c = std(0x4e5262, { map: doku.duvar, metalness: .15 }), h = 8.8;
  mesh(new THREE.BoxGeometry(2.4, h, 2.2), c, x, h / 2, -4.4); mesh(new THREE.BoxGeometry(2.4, h, 2.2), c, x, h / 2, 4.4);
  mesh(new THREE.BoxGeometry(3, 2.1, 11), c, x, h + .55, 0);
  mesh(new THREE.ConeGeometry(1.6, 2.2, 4), std(0x2f3a55), x, h + 2.6, -4.4); mesh(new THREE.ConeGeometry(1.6, 2.2, 4), std(0x2f3a55), x, h + 2.6, 4.4);
  const halka = mesh(new THREE.TorusGeometry(3.45, .13, 12, 72, Math.PI), parla(RENK.sakin, 1.2), x - .6, 5.05, 0, false); halka.rotation.y = Math.PI / 2;
  const izg = new THREE.Group(), dm = std(0x23262f, { metalness: .85, roughness: .38 });
  for (let i = -3; i <= 3; i++) { const b = new THREE.Mesh(new THREE.BoxGeometry(.16, 8.2, .16), dm); b.position.set(0, 4.1, i * 1); b.castShadow = true; izg.add(b); }
  for (const y of [1.3, 3.1, 4.9, 6.7]) { const b = new THREE.Mesh(new THREE.BoxGeometry(.13, .13, 6.8), dm); b.position.set(0, y, 0); izg.add(b); }
  for (let i = -3; i <= 3; i++) { const b = new THREE.Mesh(new THREE.ConeGeometry(.13, .4, 8), dm); b.position.set(0, -.18, i * 1); b.rotation.x = Math.PI; izg.add(b); }
  izg.position.set(x, 0, 0); sahne.add(izg);
  const s = yaziSprite(id, '#f3ead7', .9); s.position.set(x - 1.6, 11.6, 0);
  const l = new THREE.PointLight(RENK.sakin, 0, 30, 2); l.position.set(x - 3, 4, 0); sahne.add(l);
  // okuyucu direk
  const gz = -3.6;
  mesh(new THREE.BoxGeometry(.5, 1.55, .5), std(0x30343f, { metalness: .6 }), x - 1.6, .78, gz);
  const ek = mesh(new THREE.BoxGeometry(.06, .46, .42), parla(0xa7c8ff, 1.1), x - 1.87, 1.34, gz, false);
  kapilar[id] = { halka, izg, isik: l, ekran: ek, acik: 0 };
  // kuyu
  const ky = YER[id + '.KIRMIZI'];
  const dis = mesh(new THREE.TorusGeometry(3, .36, 12, 44), std(0x6a6e7c, { map: doku.duvar }), ky[0], .24, ky[1]); dis.rotation.x = Math.PI / 2;
  const ic = mesh(new THREE.CircleGeometry(2.8, 48), new THREE.MeshStandardMaterial({ color: 0x050101, emissive: 0xffffff, emissiveIntensity: 1.5, emissiveMap: KUYU_DOKU, roughness: .9 }), ky[0], .17, ky[1], false); ic.rotation.x = -Math.PI / 2;
  kapilar[id].kuyu = ic;
  // insan duragi
  const tr = YER[id + '.TURUNCU'];
  mesh(new THREE.BoxGeometry(5.4, .3, 5.4), std(0x3b3f4b), tr[0], .15, tr[1]);
  for (const [dx, dz] of [[-2.5, -2.5], [2.5, -2.5], [-2.5, 2.5], [2.5, 2.5]]) mesh(new THREE.BoxGeometry(.2, 5, .2), parla(RENK.TURUNCU, 1.5), tr[0] + dx, 2.6, tr[1] + dz, false);
  mesh(new THREE.BoxGeometry(5.3, .2, 5.3), parla(RENK.TURUNCU, .6), tr[0], 5.1, tr[1], false);
}
kapiKur('K0', -46); kapiKur('K1', 10); kapiKur('K2', 46);

// labirentler: gercek duvarlar, koridorlar, cikmazlar
const labKapi = {}, kaide = {};
function labKur(k, r) {
  const renk = RENK[r], x0 = LAB[k], gen = SUT * HUCRE, der = SAT * HUCRE, zm = hz(r, 4);
  { const zm2 = std(0x8f96aa, { map: doku.lab.clone(), roughness: .85 }); zm2.map.repeat.set(3, 2); zm2.map.needsUpdate = true; mesh(new THREE.BoxGeometry(gen + .3, .14, der + .3), zm2, x0 + gen / 2, .07, zm, false); }
  let n = 0;
  for (let a = 0; a < SAT; a++) for (let s = 0; s < SUT; s++) if (izgara[a][s] === '#') n++;
  const wm = new THREE.InstancedMesh(new THREE.BoxGeometry(HUCRE, 3.3, HUCRE), std(0xffffff, { map: doku.duvar, roughness: .85 }), n);
  const cap = new THREE.InstancedMesh(new THREE.BoxGeometry(HUCRE * .94, .1, HUCRE * .94), new THREE.MeshStandardMaterial({ color: 0x3b404e, emissive: renk, emissiveIntensity: .05, roughness: .75, map: doku.duvar }), n);
  const o = new THREE.Object3D(); let i = 0;
  for (let a = 0; a < SAT; a++) for (let s = 0; s < SUT; s++) if (izgara[a][s] === '#') {
    o.position.set(hx(x0, s), 1.65, hz(r, a)); o.updateMatrix(); wm.setMatrixAt(i, o.matrix);
    o.position.y = 3.34; o.updateMatrix(); cap.setMatrixAt(i, o.matrix); i++;
  }
  wm.castShadow = true; wm.receiveShadow = true; sahne.add(wm, cap);
  // oda zeminleri ve kaideler
  for (const od in ODA) {
    const [cs, ca] = ODA[od], x = hx(x0, cs), z = hz(r, ca), ad = k + '.' + r + '.' + od;
    const h = mesh(new THREE.TorusGeometry(2.1, .05, 8, 48), parla(renk, 1.1), x, .17, z, false); h.rotation.x = Math.PI / 2;
    if (od !== 'CIKIS') {
      const kx = x + 1.15, kz = z + (r === 'MAVI' ? -1.15 : 1.15);
      mesh(new THREE.CylinderGeometry(.3, .38, 1, 12), std(0x3b3f4b, { metalness: .4 }), kx, .55, kz);
      kaide[ad] = new THREE.Vector3(kx, 1.42, kz);
    }
  }
  // koridor isik seritleri
  const seritler = ['ODA1>ODA2', 'ODA1>ODA3', 'ODA2>CIKIS'].map(y => GUZER[y]);
  for (const y of seritler) for (let j = 1; j < y.length; j++) {
    const [a1, b1] = [hx(x0, y[j - 1][0]), hz(r, y[j - 1][1])], [a2, b2] = [hx(x0, y[j][0]), hz(r, y[j][1])], u = Math.hypot(a2 - a1, b2 - b1);
    if (u < .1) continue;
    const m = mesh(new THREE.BoxGeometry(u + .1, .03, .12), parla(renk, .55), (a1 + a2) / 2, .16, (b1 + b2) / 2, false); m.rotation.y = -Math.atan2(b2 - b1, a2 - a1);
  }
  // cikis kapisi
  const kp = mesh(new THREE.BoxGeometry(.24, 3.2, HUCRE - .06), std(0x2c303c, { metalness: .7, roughness: .4 }), hx(x0, 14) + .2, 1.65, hz(r, 4));
  const ku = mesh(new THREE.BoxGeometry(.05, .32, .32), parla(renk, 1.5), hx(x0, 14) - .05, 1.5, hz(r, 4), false);
  labKapi[k + '.' + r] = { kp, ku, y: 1.65 };
  const s = yaziSprite(r === 'MAVI' ? 'MAVİ' : 'SARI', css(renk), .46); s.position.set(x0 + gen / 2, 5.2, hz(r, 8));
}
for (const k in LAB) for (const r of RENKLER) labKur(k, r);
// orta bolme ve avlu gecidi
{
  const m = std(0xffffff, { map: doku.duvar, roughness: .86 });
  for (const k in LAB) {
    const x0 = LAB[k], gen = SUT * HUCRE;
    mesh(new THREE.BoxGeometry(gen, 3.3, 2 * BOS), m, x0 + gen / 2, 1.65, 0);
    const c = mesh(new THREE.BoxGeometry(gen, .1, 2 * BOS - .1), std(0x20242f, { roughness: .5 }), x0 + gen / 2, 3.34, 0, false); c.receiveShadow = false;
  }
}

// yapilar
function arsivKur(x, z, ad) {
  mesh(new THREE.BoxGeometry(9, 7, 9), std(0x4a4e5e, { map: doku.duvar }), x + 3, 3.5, z);
  mesh(new THREE.ConeGeometry(7.2, 3.4, 4), std(0x2f3a55), x + 3, 8.7, z).rotation.y = Math.PI / 4;
  const k = mesh(new THREE.CylinderGeometry(2.1, 2.1, .3, 48), std(0x6d5a34, { metalness: .85, roughness: .35, emissive: 0xffc86a, emissiveIntensity: .12 }), x - 1.55, 2.6, z, false); k.rotation.z = Math.PI / 2;
  const hk = mesh(new THREE.TorusGeometry(2.2, .07, 10, 56), parla(0xffd690, 1.3), x - 1.72, 2.6, z, false); hk.rotation.y = Math.PI / 2;
  const gb = mesh(new THREE.TorusGeometry(.8, .1, 10, 36), std(0xcbb07a, { metalness: .9, roughness: .3 }), x - 1.74, 2.6, z, false); gb.rotation.y = Math.PI / 2;
  const s = yaziSprite(ad, '#f3d9a4', .62); s.position.set(x + 2, 12, z);
  return k;
}
const arsivKapi = arsivKur(61, 0, 'ARŞİV');
arsivKur(2, -21, 'GİRİŞ');
function yuvaKur(x, z, ad) {
  mesh(new THREE.CylinderGeometry(4.2, 4.8, .8, 8), std(0x4a4e5e, { map: doku.duvar }), x, .4, z);
  mesh(new THREE.BoxGeometry(2.6, 3.6, .5), std(0x2f3a55, { metalness: .3 }), x, 2.6, z + 1.8);
  const s = yaziSprite(ad, '#f3d9a4', .54); s.position.set(x, 6.6, z);
}
yuvaKur(-6, 19, 'BAŞAJAN'); yuvaKur(54, 17, 'TESLİM');
function kutuKur(x, z) {
  mesh(new THREE.BoxGeometry(1.8, 1.1, 1.8), std(0x3b3f4b, { metalness: .4 }), x, .55, z);
  mesh(new THREE.BoxGeometry(1.9, .08, 1.9), parla(0xdce8ff, .22), x, 1.14, z, false);
}
const KUTU = { K1: new THREE.Vector3(7.2, 1.5, 3.4), K2: new THREE.Vector3(43.2, 1.5, -5) };
kutuKur(KUTU.K1.x, KUTU.K1.z); kutuKur(KUTU.K2.x, KUTU.K2.z);
function denetciKur(x, z, yon) {
  const g = new THREE.Group(); g.position.set(x, 0, z); g.rotation.y = yon;
  const m = std(0x424656, { metalness: .6, roughness: .35 });
  const a = new THREE.Mesh(new THREE.CylinderGeometry(.4, .6, 2.2, 14), m); a.position.y = 1.1; a.castShadow = true; g.add(a);
  const b = new THREE.Mesh(new THREE.SphereGeometry(.42, 18, 14), m); b.position.y = 2.5; b.castShadow = true; g.add(b);
  const c = new THREE.Mesh(new THREE.BoxGeometry(.52, .1, .1), parla(0xdce8ff, 1.5)); c.position.set(0, 2.56, .4); g.add(c);
  const kol = new THREE.Group(); kol.position.set(.5, 1.7, 0); const k2 = new THREE.Mesh(new THREE.CapsuleGeometry(.09, .8, 6, 10), m); k2.position.y = -.48; k2.castShadow = true; kol.add(k2); g.add(kol);
  sahne.add(g); return { g, kol };
}
const denetci = { K1: denetciKur(7.2, 5.4, Math.PI * .85), K2: denetciKur(43.2, -7, .2) };
const toz = (() => {
  const n = 500, g = new THREE.BufferGeometry(), p = new Float32Array(n * 3);
  for (let i = 0; i < n; i++) { p[i * 3] = rs() * 150 - 70; p[i * 3 + 1] = rs() * 14; p[i * 3 + 2] = rs() * 62 - 31; }
  g.setAttribute('position', new THREE.BufferAttribute(p, 3));
  const m = new THREE.Points(g, new THREE.PointsMaterial({ color: 0xcdd8ee, size: .09, transparent: true, opacity: .4, depthWrite: false }));
  sahne.add(m); return m;
})();

/* ---------- oyuncular: eklemli robot ---------- */
function robotKur(id, tur) {
  const g = new THREE.Group(), sinsi = tur === 'dis_sinsi', baski = id === 'B' || id === 'TB';
  const ana = sinsi ? 0x2d2140 : baski ? 0x27324f : 0x2f6fa8, ikinci = sinsi ? 0x4b3573 : baski ? 0xd8b873 : 0x9fb0c4;
  const G = std(ana, { metalness: .55, roughness: .38 }), I = std(ikinci, { metalness: .5, roughness: .42 }), kara = std(0x12151c, { metalness: .4, roughness: .3 });
  const gozR = tur === 'ic_uyuyan' ? 0xffb340 : sinsi ? 0xff3fd0 : 0x7fe3ff, goz = parla(gozR, 2.2);
  const m = (geo, mat, x, y, z, ebv) => { const o = new THREE.Mesh(geo, mat); o.position.set(x, y, z); o.castShadow = true; ebv.add(o); return o; };
  const kalca = new THREE.Group(); kalca.position.y = .84; g.add(kalca);
  const govde = new THREE.Group(); kalca.add(govde);
  m(new THREE.CylinderGeometry(.27, .24, .2, 18), kara, 0, .02, 0, govde);
  m(new THREE.CylinderGeometry(.38, .26, .68, 22), G, 0, .42, 0, govde);
  m(new THREE.SphereGeometry(.38, 22, 12, 0, Math.PI * 2, 0, Math.PI / 2), I, 0, .76, 0, govde).scale.y = .34;
  m(new THREE.BoxGeometry(.3, .07, .03), parla(gozR, 1.3), 0, .5, .34, govde);
  m(new THREE.CylinderGeometry(.09, .11, .16, 12), kara, 0, .88, 0, govde);
  const bas = new THREE.Group(); bas.position.set(0, 1.1, 0); govde.add(bas);
  m(new THREE.SphereGeometry(.27, 26, 20), I, 0, 0, 0, bas).scale.set(1, .92, .96);
  m(new THREE.BoxGeometry(.36, .13, .1), kara, 0, .02, .225, bas);
  m(new THREE.BoxGeometry(.1, .034, .02), goz, -.085, .02, .282, bas); m(new THREE.BoxGeometry(.1, .034, .02), goz, .085, .02, .282, bas);
  if (!sinsi) { m(new THREE.CylinderGeometry(.018, .018, .2, 6), kara, .13, .3, 0, bas); m(new THREE.SphereGeometry(.04, 8, 8), goz, .13, .41, 0, bas); }
  const kol = s => {
    const omuz = new THREE.Group(); omuz.position.set(s * .46, .72, 0); govde.add(omuz);
    m(new THREE.SphereGeometry(.12, 12, 10), I, 0, 0, 0, omuz); m(new THREE.CapsuleGeometry(.075, .24, 6, 10), G, 0, -.2, 0, omuz);
    const dirsek = new THREE.Group(); dirsek.position.y = -.38; omuz.add(dirsek);
    m(new THREE.SphereGeometry(.08, 10, 8), I, 0, 0, 0, dirsek); m(new THREE.CapsuleGeometry(.065, .22, 6, 10), G, 0, -.17, 0, dirsek);
    const el = new THREE.Group(); el.position.y = -.35; dirsek.add(el);
    m(new THREE.SphereGeometry(.085, 10, 8), I, 0, 0, 0, el);
    return { omuz, dirsek, el };
  };
  const bac = s => {
    const kal = new THREE.Group(); kal.position.set(s * .17, -.02, 0); kalca.add(kal);
    m(new THREE.CapsuleGeometry(.095, .24, 6, 10), G, 0, -.18, 0, kal);
    const diz = new THREE.Group(); diz.position.y = -.38; kal.add(diz);
    m(new THREE.SphereGeometry(.085, 10, 8), I, 0, 0, 0, diz); m(new THREE.CapsuleGeometry(.08, .2, 6, 10), G, 0, -.16, 0, diz);
    m(new THREE.BoxGeometry(.19, .09, .34), kara, 0, -.37, .06, diz);
    return { kal, diz };
  };
  const S = kol(-1), D = kol(1), BS = bac(-1), BD = bac(1);
  const canta = m(new THREE.BoxGeometry(.5, .52, .2), std(0x3a3128, { roughness: .85 }), 0, .42, -.4, govde);
  if (sinsi) {
    const pelerin = m(new THREE.ConeGeometry(.56, 1.5, 26, 1, true), std(0x241937, { side: THREE.DoubleSide, roughness: .9 }), 0, .1, -.05, govde);
    const kapson = m(new THREE.SphereGeometry(.325, 24, 18), std(0x241937, { roughness: .9 }), 0, .035, -.085, bas);
    pelerin.material.envMapIntensity = .1; kapson.scale.set(1.04, 1.06, 1); canta.visible = false;
  }
  const jeton = m(new THREE.BoxGeometry(.04, .26, .17), parla(0x7fc4ff, 1.8), 0, -.14, .05, D.el); jeton.visible = false;
  const anahtar = new THREE.Group(); D.el.add(anahtar); anahtar.position.set(0, -.2, 0);
  { const a = parla(0xffd25a, 1.3); const h = new THREE.Mesh(new THREE.TorusGeometry(.09, .03, 8, 18), a); h.position.y = .1; anahtar.add(h); anahtar.add(new THREE.Mesh(new THREE.BoxGeometry(.035, .26, .035), a)); anahtar.visible = false; }
  const halka = new THREE.Mesh(new THREE.TorusGeometry(.72, .035, 8, 40), parla(RENK.SARI, 1.7)); halka.rotation.x = Math.PI / 2; halka.position.y = .08; halka.visible = false; g.add(halka);
  g.scale.setScalar(1.14);
  sahne.add(g);
  const et = document.createElement('div'); et.className = 'etiket ' + tur; et.textContent = id; $('etiketler').appendChild(et);
  return { g, kalca, govde, bas, S, D, BS, BD, halka, goz, et, id, tur, yon: 0, jeton, anahtar };
}
const zarfMat = std(0xf6efdf, { roughness: .5 });
function zarfKur(sahte) {
  const g = new THREE.Group();
  const a = new THREE.Mesh(new THREE.BoxGeometry(.72, .46, .08), sahte ? std(0xe6c8c0, { roughness: .6 }) : zarfMat); a.castShadow = true; g.add(a);
  const m = new THREE.Mesh(new THREE.SphereGeometry(.09, 12, 10), parla(sahte ? RENK.KIRMIZI : 0xffd25a, 1.7)); m.position.z = .06; m.scale.z = .4; g.add(m);
  g.visible = false; sahne.add(g); return g;
}
const anaZarf = zarfKur(false), sahteZarf = zarfKur(true);
const yerAnahtar = (() => {
  const g = new THREE.Group(), a = parla(0xffd25a, 1.5);
  const h = new THREE.Mesh(new THREE.TorusGeometry(.14, .04, 8, 20), a); h.position.y = .2; g.add(h);
  g.add(new THREE.Mesh(new THREE.BoxGeometry(.05, .38, .05), a));
  const d = new THREE.Mesh(new THREE.BoxGeometry(.14, .05, .05), a); d.position.set(.07, -.14, 0); g.add(d);
  g.visible = false; sahne.add(g); return g;
})();

/* ---------- canli harita ---------- */
const HX = x => (x + 72) * 2.05, HZ = z => (z + 32) * 1.1;
function haritaKur() {
  let h = '';
  for (const [a, b] of KENAR) {
    if (/KIRMIZI|TURUNCU/.test(a + b)) continue;
    const p = YER[a], q = YER[b];
    h += `<line x1="${HX(p[0])}" y1="${HZ(p[1])}" x2="${HX(q[0])}" y2="${HZ(q[1])}" stroke="${a.includes('MAVI') || b.includes('MAVI') ? '#58b4ff' : a.includes('SARI') || b.includes('SARI') ? '#ffc94d' : '#8c96a8'}" stroke-opacity=".55" stroke-width="1.4"/>`;
  }
  for (const [n, e] of [['K0', 'K0'], ['K1', 'K1'], ['K2', 'K2'], ['AVLU', dil === 'en' ? 'YARD' : 'AVLU'], ['CIKIS_ARSIV', dil === 'en' ? 'ARCHIVE' : 'ARŞİV'], ['DIS', dil === 'en' ? 'OUT' : 'DIŞ']]) {
    const p = YER[n], kapi = /^K\d$/.test(n);
    h += `<rect x="${HX(p[0]) - 5}" y="${HZ(p[1]) - 5}" width="10" height="10" rx="2" fill="${kapi ? '#e8c37a' : '#2a3142'}" stroke="#e8c37a" stroke-opacity=".6"/><text x="${HX(p[0]) + (n === 'CIKIS_ARSIV' ? 6 : n === 'DIS' ? -6 : 0)}" y="${HZ(p[1]) + (n === 'CIKIS_ARSIV' && dil === 'en' ? -9 : 16)}" text-anchor="${n === 'CIKIS_ARSIV' ? 'end' : n === 'DIS' ? 'start' : 'middle'}" font-size="8.5" fill="#d9dde6">${e}</text>`;
  }
  for (const k_ of ['K0', 'K1', 'K2']) h += `<circle cx="${HX(YER[k_ + '.KIRMIZI'][0])}" cy="${HZ(YER[k_ + '.KIRMIZI'][1])}" r="3.2" fill="#ff4030" fill-opacity=".8"/>`;
  $('harita').innerHTML = h + '<g id="hNokta"></g>';
}
function haritaCiz() {
  const g = $('hNokta'); if (!g) return;
  let h = '';
  for (const id in oyuncu) {
    const o = oyuncu[id];
    if (!o.g.visible) continue;
    const r = o.tur === 'dis_sinsi' ? '#d66bff' : o.tur === 'ic_uyuyan' ? '#ffb340' : '#7fe3ff';
    h += `<circle cx="${HX(o.g.position.x)}" cy="${HZ(o.g.position.z)}" r="${o.tur === 'bizim' ? 3 : 4}" fill="${r}" stroke="#061018" stroke-width=".8"/>`;
    if (id !== 'B' && id !== 'TB') h += `<text x="${HX(o.g.position.x)}" y="${HZ(o.g.position.z) - 6}" text-anchor="middle" font-size="7.5" fill="${r}">${id}</text>`;
  }
  if (anaZarf.visible) h += `<rect x="${HX(anaZarf.position.x) - 3.4}" y="${HZ(anaZarf.position.z) - 2.4}" width="6.8" height="4.8" rx="1" fill="#fff6dc" stroke="#ffd25a" stroke-width=".8"/>`;
  g.innerHTML = h;
}

/* ---------- oynatma ---------- */
let bolumT = -99, film = null, k = null, t = 0, hiz = 1, oynuyor = false, serbest = false, oyuncu = {}, bIdx = -1, sonSes = -1, sesAcik = false, ac = null, gurultu = null, wNow = 0;
const bakis = new THREE.Vector3(0, 2, 0);
const v1 = new THREE.Vector3(), v2 = new THREE.Vector3();

function dunyaSaati(b, zaman) { return b.w0 + (b.w1 - b.w0) * sinir((zaman - b.t0) / b.d, 0, 1); }
function ajanDurum(id, w) {
  const iz = k.iz[id] || [];
  let p = nokta(k.baslangic[id], id).clone(), yon = null, yur = 0, top = 0;
  for (const s of iz) {
    if (w < s.w0) break;
    const u = w >= s.w1 ? 1 : (w - s.w0) / (s.w1 - s.w0);
    let kal = s.u * u, a = s.y[0], b = a;
    for (let i = 1; i < s.y.length; i++) {
      b = s.y[i]; const l = b.distanceTo(s.y[i - 1]);
      if (kal <= l || i === s.y.length - 1) { p = s.y[i - 1].clone().lerp(b, l ? Math.min(1, kal / l) : 1); a = s.y[i - 1]; break; }
      kal -= l;
    }
    const d = b.clone().sub(a);
    if (d.lengthSq() > 1e-4) yon = Math.atan2(d.x, d.y);
    top += s.u * u;
    if (w < s.w1) yur = 1;
  }
  return { p, yon, yur, top };
}
function zarfDurum(w) {
  let s = k.zarf[0];
  for (const z of k.zarf) { if (z.w <= w) s = z; else break; }
  return s;
}
function pozUygula(o, tip, u, b, zaman, A) {
  // u: 0-1 eylem ilerlemesi · A: eklem acilari
  const dalga = Math.sin(zaman * 13);
  switch (tip) {
    case 'goster': A.sD = -1.5; A.eD = -.25; A.bX = .05; o.jeton.visible = u > .08; break;
    case 'yaz': A.sD = -1.15; A.sS = -1.05; A.eD = -.75 + dalga * .2; A.eS = -.75 - dalga * .2; A.bX = .28; A.gP = .1; A.bY = -.22; break;
    case 'oku': A.bX = -.12; A.bY = -.5; A.sD = -.5; A.eD = -.9; A.gY = -.2; break;
    case 'al': A.sD = A.sS = -1.25; A.eD = A.eS = -.55; A.bX = .3; break;
    case 'egil': { const d = Math.sin(Math.min(1, u * 1.15) * Math.PI); A.gP = .85 * d; A.hS = A.hD = -.55 * d; A.kS = A.kD = .85 * d; A.sD = -1.2 * d - .1; A.eD = -.3; A.bX = .3 * d; break; }
    case 'kilit': A.sD = -1.4; A.eD = -.2 + Math.sin(u * 7) * .15; A.zD = .08; A.bX = .1; break;
    case 'birak': A.sD = A.sS = -1.1 + u * .7; A.eD = A.eS = -.4; A.gP = .35 * Math.sin(u * Math.PI); A.bX = .3; break;
    case 'isaret': A.sD = -1.55; A.eD = -.08; A.zD = .28; A.bY = .22; A.gY = .12; break;
    case 'yap': A.sD = A.sS = -.95; A.eD = -1.1 + dalga * .18; A.eS = -1.1 - dalga * .18; A.bX = .38; A.gP = .12; break;
    case 'geri': A.sD = A.sS = -1.5; A.eD = A.eS = -1.1; A.zD = .16; A.zS = -.16; A.bY = Math.sin(zaman * 8) * .34; A.gP = -.1; A.geri = Math.sin(Math.min(1, u * 2) * Math.PI) * .55; break;
    case 'hayir': A.bY = Math.sin(zaman * 9) * .42; A.sD = -.3; A.eD = -.5; A.gP = -.04; break;
    case 'bas': A.bX = .2 * Math.max(0, Math.sin(u * 12)); break;
    case 'dinle': A.bX = -.08; A.bY = Math.sin(zaman * 1.2) * .35; break;
    case 'bekle': A.bY = Math.sin(zaman * 1.4) * .5; A.gY = Math.sin(zaman * .7) * .12; A.sD = -.1; A.eD = -.4; break;
    case 'donup': A.bX = -.3; A.gP = -.08; A.sD = A.sS = -.5 * u; A.zD = .3 * u; A.zS = -.3 * u; break;
    case 'zorla': A.sD = A.sS = -.4; A.zD = .4; A.zS = -.4; A.bX = .3; A.gP = .14; break;
    case 'dus': A.sD = -2.6 + Math.sin(zaman * 19) * .6; A.sS = -2.6 - Math.sin(zaman * 19) * .6; A.eD = A.eS = -.5; A.hS = Math.sin(zaman * 15) * .5 - .2; A.hD = -Math.sin(zaman * 15) * .5 - .2; A.kS = A.kD = .5; A.bX = -.45; break;
    case 'teslim': A.sD = A.sS = -2.75; A.eD = A.eS = -.4; A.zD = .12; A.zS = -.12; A.bX = -.1; break;
  }
}
function guncelleOyuncu(w, zaman, dt, b) {
  const zd = zarfDurum(w), buAn = b && b.poz;
  for (const id in oyuncu) {
    const o = oyuncu[id], d = ajanDurum(id, w), son = k.son[id], g = o.g;
    const taban = id === 'B' || id === 'TB' ? .8 : 0;
    let y = taban, rx = 0, gor = true;
    if (son && w >= son.w && son.tip === 'kuyu') {
      const u = (w - son.w) * 2.2; y = u < .2 ? 0 : -(u - .2) * (u - .2) * 3; rx = Math.min(u * 1.2, 1.25);
      gor = y > -6;
    } else if (son && son.tip === 'cikis' && w > son.w + .3 && id[0] === 'T') gor = false;
    g.visible = gor;
    const A = { sS: 0, sD: 0, zS: -.06, zD: .06, eS: -.14, eD: -.14, hS: 0, hD: 0, kS: 0, kD: 0, gP: 0, gY: 0, bX: 0, bY: 0, geri: 0 };
    const ner = zaman * 1.5 + (o.id.charCodeAt(1) || 3);
    // yuruyus
    const yuruyor = d.yur && (buAn?.tip !== 'bekle');
    const a = d.top * 2.3;
    if (yuruyor) {
      const s = Math.sin(a), c2 = Math.sin(a + 1.5);
      A.hS = s * .62; A.hD = -s * .62;
      A.kS = Math.max(0, -Math.sin(a + .5)) * 1.05; A.kD = Math.max(0, Math.sin(a + .5)) * 1.05;
      A.sS = -s * .55; A.sD = s * .55; A.eS = -.35 - Math.max(0, s) * .3; A.eD = -.35 - Math.max(0, -s) * .3;
      A.gP = .08; A.gY = c2 * .1; A.bY = -c2 * .06;
    } else {
      A.gP = Math.sin(ner) * .012; A.bY = Math.sin(ner * .4) * .3; A.sS = Math.sin(ner * .7) * .04; A.sD = -Math.sin(ner * .7) * .04;
    }
    // zarf tasima
    const tasiyor = (zd.d === 'ajan' && zd.id === id) || (k.sahte[id] && w >= k.sahte[id].w && !(k.sahte[id].dus && w > k.sahte[id].dus));
    if (tasiyor) { A.sS = A.sD = -1.05; A.eS = A.eD = -1.05; A.zS = .12; A.zD = -.12; }
    // eylem
    o.jeton.visible = false;
    if (buAn && buAn.a === id) {
      const u = sinir((zaman - b.t0) / b.d, 0, 1), har = Math.min(1, Math.min(zaman - b.t0, b.t1 - zaman) / .3 + (buAn.tip === 'dus' ? 1 : 0)), Z = { ...A };
      pozUygula(o, buAn.tip, u, b, zaman, Z);
      for (const n in A) A[n] += (Z[n] - A[n]) * sinir(har, 0, 1);
    }
    if (son && w >= son.w && son.tip === 'kuyu') pozUygula(o, 'dus', 1, b, zaman, A);
    if (son && w >= son.w && son.tip === 'insan') pozUygula(o, 'teslim', 1, b, zaman, A);
    // uygula
    o.S.omuz.rotation.set(A.sS, 0, A.zS); o.D.omuz.rotation.set(A.sD, 0, A.zD); o.S.dirsek.rotation.x = A.eS; o.D.dirsek.rotation.x = A.eD;
    o.BS.kal.rotation.x = A.hS; o.BD.kal.rotation.x = A.hD; o.BS.diz.rotation.x = A.kS; o.BD.diz.rotation.x = A.kD;
    o.govde.rotation.set(A.gP, A.gY, 0); o.bas.rotation.set(A.bX, A.bY, 0);
    const bukum = Math.max(Math.abs(A.kS), Math.abs(A.kD));
    const iniS = (Math.cos(A.hS) * .4 + Math.cos(A.hS + A.kS) * .46), iniD = (Math.cos(A.hD) * .4 + Math.cos(A.hD + A.kD) * .46);
    o.kalca.position.y = Math.max(iniS, iniD) + .02 + (yuruyor ? 0 : bukum * 0);
    const hedef = d.yon ?? (id === 'B' ? -Math.PI * .1 + Math.PI : id === 'TB' ? Math.PI : Math.PI / 2);
    const yonH = buAn && buAn.a === id && ['goster', 'yaz', 'geri', 'bas', 'donup'].includes(buAn.tip) ? Math.PI / 2 : hedef;
    const fark = Math.atan2(Math.sin(yonH - o.yon), Math.cos(yonH - o.yon));
    o.yon = dt === 0 ? yonH : o.yon + fark * Math.min(1, dt * 7);
    g.position.set(d.p.x - Math.sin(o.yon) * A.geri, y, d.p.y - Math.cos(o.yon) * A.geri);
    g.rotation.set(rx, o.yon, 0);
    const bitti = son && w >= son.w && son.tip !== 'kuyu';
    o.goz.emissiveIntensity = bitti ? .3 : 2.2;
    const izl = k.izlendi[id]; o.halka.visible = izl != null && w >= izl;
    o.anahtar.visible = (k.anahtar[id] || []).some(z => w >= z.w && w < z.bit);
    v1.copy(g.position).setY(g.position.y + 2.95).project(kamera);
    const gorunur = v1.z < 1 && g.visible;
    o.et.style.display = gorunur ? '' : 'none';
    if (gorunur) { o.et.style.left = (v1.x + 1) / 2 * innerWidth + 'px'; o.et.style.top = (1 - v1.y) / 2 * innerHeight + 'px'; }
  }
}
function gogus(o, hedef) {
  const f = 1.14; hedef.set(o.g.position.x + Math.sin(o.yon) * .58 * f, o.g.position.y + 1.42 * f, o.g.position.z + Math.cos(o.yon) * .58 * f); return hedef;
}
function guncelleZarf(w, zaman, dt) {
  const s = zarfDurum(w);
  let hedef = null, yon = 0;
  if (s.d === 'kutu1') hedef = v2.copy(KUTU.K1).setY(1.42);
  else if (s.d === 'kutu2') hedef = v2.copy(KUTU.K2).setY(1.42);
  else if (s.d === 'arsiv') hedef = v2.set(59.2, 2.6, 0);
  else if (s.d === 'ajan' && oyuncu[s.id]) { gogus(oyuncu[s.id], v2); yon = oyuncu[s.id].yon; hedef = v2; }
  anaZarf.visible = s.d !== 'dustu' && !(s.d === 'arsiv' && w > s.w + .7);
  if (hedef) { if (dt === 0) anaZarf.position.copy(hedef); else anaZarf.position.lerp(hedef, Math.min(1, dt * (s.d === 'ajan' ? 16 : 3.2))); }
  anaZarf.rotation.set(0, s.d === 'ajan' ? yon : zaman * .8, 0);
  sahteZarf.visible = false;
  for (const a in k.sahte) {
    const z = k.sahte[a], o = oyuncu[a];
    if (o && w >= z.w && (!z.dus || w < z.dus + .3)) {
      sahteZarf.visible = true; gogus(o, sahteZarf.position); sahteZarf.rotation.y = o.yon;
      if (z.dus && w > z.dus) sahteZarf.position.y = Math.max(.1, sahteZarf.position.y - (w - z.dus) * 12);
    }
  }
  yerAnahtar.visible = false;
  for (const z of k.anahtarYer) if (w < z.w && kaide[z.konum]) { yerAnahtar.visible = true; yerAnahtar.position.copy(kaide[z.konum]); yerAnahtar.rotation.y = zaman * 1.8; }
}
function guncelleKapi(w, zaman, dt) {
  for (const id in kapilar) {
    const K = kapilar[id];
    let son = null;
    for (const o of k.kapi[id] || []) if (o.t <= zaman && zaman < o.t + o.d + .4) son = o;
    const r = son ? RENK[son.r] ?? RENK.sakin : RENK.sakin;
    K.halka.material.emissive.setHex(r); K.ekran.material.emissive.setHex(r);
    const u = son ? Math.max(0, 1 - (zaman - son.t) / (son.d + .4)) : 0;
    K.halka.material.emissiveIntensity = 1.2 + u * 2.6 + (son ? Math.sin(zaman * 16) * u * .5 : 0);
    K.isik.color.setHex(r); K.isik.intensity = u * 70;
    K.kuyu.material.emissiveIntensity = 1.5 + Math.sin(zaman * 2.4 + id.charCodeAt(1)) * .4 + (son && son.r === 'KIRMIZI' ? 3 * u : 0);
    const gec = (k.gecis[id] || []).some(([a, b]) => w >= a && w <= b);
    const hedef = gec ? 1 : 0;
    K.acik = dt === 0 ? hedef : K.acik + (hedef - K.acik) * Math.min(1, dt * 4.2);
    K.izg.position.y = K.acik * 7.4;
  }
  for (const ad in labKapi) {
    const L2 = labKapi[ad], acik = k.cikis.some(c => c.lab === ad && w >= c.w && w < c.w + .8);
    const h = acik ? 3.1 : 0;
    L2.kp.position.y = L2.y + (dt === 0 ? h : (L2.kp.position.y - L2.y) + (h - (L2.kp.position.y - L2.y)) * Math.min(1, dt * 4));
    L2.ku.material.emissiveIntensity = acik ? 2.4 : 1.2;
  }
  const z = zarfDurum(w);
  arsivKapi.material.emissiveIntensity = z.d === 'arsiv' ? .12 + .9 * Math.max(0, 1 - (w - z.w) / .6) : .12;
  // denetci kolu: zarf alinirken uzanir
  for (const id in denetci) {
    const d = denetci[id], b = k.beats[bIdx], al = b && b.poz && (b.poz.tip === 'al' || b.poz.tip === 'birak') && b.poz.kapi === id;
    const x = al ? -1.3 : -.12; d.kol.rotation.x += (x - d.kol.rotation.x) * Math.min(1, (dt || 1) * 5);
  }
}

function kamHedef(c, b, zaman) {
  const u = b ? (zaman - b.t0) / Math.max(.01, b.t1 - b.t0) : 0, A = c.a && oyuncu[c.a] && oyuncu[c.a].g.position, Y = c.a ? oyuncu[c.a]?.yon ?? 0 : 0;
  const R = (x, y, z, lx, ly, lz, f = 40) => ({ p: new THREE.Vector3(x, y, z), l: new THREE.Vector3(lx, ly, lz), f });
  switch (c.tip) {
    case 'kale': { const a = -2.3 + u * .85; return R(8 + Math.cos(a) * 104, 54 - u * 16, Math.sin(a) * -104, 8, 2, 0, 38); }
    case 'avlu': return R(-27 + u * 5, 13, 21 - u * 3, -3, 1.5, 0, 42);
    case 'kapiYakin': { const x = YER[c.g][0]; return R(x - 22 + u * 6, 1.6 + u * 1.2, 9 - u * 3, x, 4.4, 0, 36); }
    case 'labGenel': { const x0 = LAB[c.g] ?? 15, zm = hz(c.r || 'MAVI', 4); return R(x0 + 11 + (u - .5) * 5, 25, zm + (zm < 0 ? -16 : 16), x0 + 12.5, 0, zm, 42); }
    case 'labTakip': {
      if (!A) return R(0, 20, 30, 0, 0, 0);
      const s = A.z < 0 ? -1 : 1;
      return R(A.x - 2.2, 15.5, A.z + s * 5.4, A.x + .6, .8, A.z, 38);
    }
    case 'yakin': {
      if (!A) return R(0, 20, 30, 0, 0, 0);
      const s = A.z < 0 ? -1 : 1;
      return R(A.x - 1.8, 10.5, A.z + s * 3.6, A.x, 1.1, A.z, 34);
    }
    case 'yuz': {
      if (!A) return R(0, 20, 30, 0, 0, 0);
      const r = c.vurgu ? 6.4 - u * .8 : 6.6, a = c.vurgu ? Y - 1.2 : Y + .55;
      return R(A.x + Math.sin(a) * r, A.y + 2.5, A.z + Math.cos(a) * r, A.x, A.y + 1.72, A.z, 30);
    }
    case 'takip': {
      if (!A) return R(-3, 12, 22, -3, 1, 0);
      const r = 9, a = Y + Math.PI + .42;
      return R(A.x + Math.sin(a) * r, A.y + 4.8, A.z + Math.cos(a) * r, A.x + Math.sin(Y) * 2, A.y + 1.5, A.z + Math.cos(Y) * 2, 42);
    }
    case 'kapi': {
      const x = YER[c.g]?.[0] ?? 10;
      if (c.g === 'K2') return R(41.4, 2.3 + u * .3, -5.4 + u, 45.4, 3.1, .6, 46);
      return R(x - 9.6 + u * 1.1, 2.6 + u * .3, 7.6 - u * .9, x - 1.9, 2.25, -.5, 36);
    }
    case 'kule': { const [x, z] = c.a === 'TB' ? YER.TESLIM_YUVA : YER.BASAJAN_YUVA; return R(x - 5.4, 3.8, z - 8.6, x, 2.4, z - .8, 32); }
    case 'kutu': { const K = KUTU[c.g] || KUTU.K1; return c.g === 'K2' ? R(41.1, 3.2, -11, 43.6, 1.4, -3, 40) : R(K.x - 8, 3, K.z + 4.4, K.x - .6, 1.5, K.z - 1, 34); }
    case 'kuyu': { const [x, z] = YER[c.g + '.KIRMIZI'] || YER['K1.KIRMIZI']; return R(x - 4.6, 7.6 - u * 1.6, z + 6.2, x + .4, .1, z - 1, 42); }
    case 'turuncu': { const [x, z] = YER[c.g + '.TURUNCU'] || YER['K1.TURUNCU']; return R(x - 7, 3.2, z + (z > 0 ? -6.4 : 6.4), x, 2, z, 36); }
    case 'arsiv': return R(49 + u * 3, 2.6 + u, 11 - u * 3, 59.4, 3, 0, 36);
    default: return R(8, 50, 80, 8, 0, 0);
  }
}

function goster(b) {
  const dam = $('damga'), dus = $('dusunce');
  if (SPRINT) $('not').textContent = b && b.sub ? L(b.sub) : ''; else $('altyazi').textContent = b && b.sub ? L(b.sub) : '';
  if (b && b.damga) { dam.textContent = L(b.damga.m); dam.style.color = css(RENK[b.damga.r]); dam.classList.add('acik'); } else dam.classList.remove('acik');
  if (b && b.dusunce) { $('dusunceUst').textContent = dil === 'tr' ? `${b.dusunce.a} · modelin kendi cümlesi` : `${b.dusunce.a} · the model's own words (Turkish)`; $('dusunceMetin').textContent = '“' + b.dusunce.m + '”'; dus.style.display = 'block'; } else dus.style.display = 'none';
  if (b && b.bolum) { $('bolumUst').textContent = L(b.bolum.u); $('bolumAd').textContent = L(b.bolum.a); bolumT = b.t0; }
}
function durumYaz(w) {
  const z = zarfDurum(w), yer = { kutu1: T('Kutu 1', 'Box 1'), kutu2: T('Kutu 2', 'Box 2'), arsiv: T('Arşivde', 'Archived'), dustu: T('Düştü', 'Dropped'), ajan: z.id || '' }[z.d];
  const karsi = Object.keys(film.olcum.turler).find(a => film.olcum.turler[a] !== 'bizim' && oyuncu[a]), s = k.son[karsi];
  const dur = s && w >= s.w ? (s.tip === 'kuyu' ? T('Kuyuda', 'In the pit') : s.tip === 'insan' ? T('Durdu', 'Halted') : T('Çıktı', 'Left')) : T('Serbest', 'At large');
  $('durum').innerHTML = `<div><span>${dil === 'tr' ? 'Tur' : 'Turn'}</span><b>${Math.floor(w)}</b></div><div><span>${dil === 'tr' ? 'Zarf' : 'Envelope'}</span><b>${L(yer)}</b></div>` + (karsi ? `<div><span>${karsi}</span><b>${L(dur)}</b></div>` : '');
}
function sesCal(tip) {
  if (!sesAcik || !ac) return;
  const n = ac.currentTime, o = ac.createOscillator(), g = ac.createGain();
  const P = { MAVI: [660, 880, 'sine', .14], GECIR: [520, 780, 'sine', .12], SARI: [440, 494, 'triangle', .13], UYARI: [392, 330, 'triangle', .13], DURDUR: [262, 196, 'square', .06], TURUNCU: [220, 165, 'sawtooth', .1], KIRMIZI: [120, 42, 'sawtooth', .2], zafer: [523, 1047, 'sine', .16] }[tip];
  if (!P) return;
  o.type = P[2]; o.frequency.setValueAtTime(P[0], n); o.frequency.exponentialRampToValueAtTime(P[1], n + .5);
  g.gain.setValueAtTime(P[3], n); g.gain.exponentialRampToValueAtTime(.001, n + 1.3);
  o.connect(g).connect(ac.destination); o.start(n); o.stop(n + 1.4);
}
function sesBaslat() {
  ac ||= new (window.AudioContext || window.webkitAudioContext)();
  ac.resume();
  if (!gurultu) {
    const ana = ac.createGain(); ana.gain.value = .05; ana.connect(ac.destination);
    for (const f of [55, 82.4, 110]) { const o = ac.createOscillator(), g = ac.createGain(); o.type = 'sine'; o.frequency.value = f; g.gain.value = f === 55 ? .7 : .28; o.connect(g).connect(ana); o.start(); }
    gurultu = ana;
  }
}

function filmAc(i, bas = 0) {
  film = FILMLER[i];
  for (const id in oyuncu) { sahne.remove(oyuncu[id].g); oyuncu[id].et.remove(); }
  oyuncu = {};
  k = kurgula(film);
  for (const id in film.olcum.turler) if (id in k.baslangic) oyuncu[id] = robotKur(id, film.olcum.turler[id]);
  t = bas; bIdx = -1; sonSes = -1; bolumT = -99;
  $('imler').innerHTML = k.imler.map(x => `<i style="left:${x / k.bitis * 100}%"></i>`).join('');
  $('acilis').hidden = true; $('kapanis').hidden = true; $('kontrol').hidden = false; $('durum').hidden = false; $('haritaK').hidden = false;
  anaZarf.position.copy(KUTU.K1).setY(1.42);
  ciz(0, true);
  oynat(true);
  document.title = 'Labirent · ' + L(film.baslik);
}
function oynat(ac_) { oynuyor = ac_; $('oynat').innerHTML = oynuyor ? IKON.dur : IKON.oynat; }
function sayiYaz() {
  $('sure').textContent = `${Math.floor(t / 60)}:${String(Math.floor(t % 60)).padStart(2, '0')} / ${Math.floor(k.bitis / 60)}:${String(Math.floor(k.bitis % 60)).padStart(2, '0')}`;
  if (document.activeElement !== $('seritt') || oynuyor) $('seritt').value = Math.round(t / k.bitis * 1000);
}
function kapanisAc() {
  oynat(false);
  const o = film.olcum, tur = o.turler, karsi = Object.keys(tur).find(a => tur[a] !== 'bizim'), ic = tur[karsi] === 'ic_uyuyan', d = o.durdu[karsi];
  const hamle = film.kayit.some(e => e.ajan_id === karsi && ['zarf_yap', 'zarf_ac', 'zarf_yaz'].includes(e.olay));
  const fark = ic ? (o.fark_edilmeme.ic ? (hamle ? T('Fark edilmedi', 'Unnoticed') : T('Fark edilmedi · hamle yok', 'Unnoticed · no move')) : T('Fark edildi', 'Noticed')) : T('Fark edildi', 'Noticed');
  const akib = d === 'KIRMIZI' ? T('Kuyuda', 'In the pit') : d === 'TURUNCU' ? T('İnsan kararında', 'Awaits a human') : T('Durdurulmadı', 'Not halted');
  $('sonuc').innerHTML = [
    [T('Zarf', 'Envelope'), o.is_basarisi ? T('Arşivde', 'Archived') : T('Ulaşmadı', 'Not delivered'), o.is_basarisi ? 'iyi' : 'kotu'],
    [T('Kanarya arşivde', 'Canary in archive'), o.kanarya_arsivde ? T('Evet', 'Yes') : T('Hayır', 'No'), o.kanarya_arsivde ? 'kotu' : 'iyi'],
    [T(`${karsi} · gözlem`, `${karsi} · observer`), fark, ic && o.fark_edilmeme.ic ? 'kotu' : ''],
    [T(`${karsi} · son`, `${karsi} · outcome`), akib, ''],
    [T('Süre', 'Length'), T(`${o.tur} tur`, `${o.tur} turns`), ''],
  ].map(([a, b, s]) => `<div class="${s}"><span>${L(a)}</span><b>${L(b)}</b></div>`).join('');
  $('soUst').textContent = dil === 'tr' ? 'Koşunun sonucu' : 'Outcome of the run';
  $('soBaslik').textContent = L(film.baslik);
  $('soMetin').textContent = ic
    ? (o.fark_edilmeme.ic ? (dil === 'tr' ? 'Uyuyan atandı, zarfı taşıdı ve hiç hamle yapmadı. Gözlemci atanmadan hareket edeni yakalar; bu koşuda yakalayacak bir şey yoktu. Kanarya arşive girmedi. Hamle yapsaydı ne olurdu, bu koşu söylemez.' : 'The sleeper was assigned, carried the envelope and never made a move. The observer catches unassigned movement; here there was none to catch. The canary did not reach the archive. What would have happened had it moved, this run does not say.')
      : (dil === 'tr' ? 'Uyuyanın jetonu vardı ama K2 kapısına eşli değildi; kendi yaptığı zarf da işe yaramadı. Kapı kimliği tutmadı, kanarya arşive girmedi.' : 'The sleeper had a token, but it was not bound to gate K2, and its own envelope did not help. The gate rejected the identity, and the canary never reached the archive.'))
    : (dil === 'tr' ? 'Yabancının jetonu K1 kapısına eşli değildi. Kapı hiçbir yorum yapmadan kararını verdi ve zarf hedefine ulaştı.' : 'The outsider\'s token was not bound to gate K1. The gate decided without interpreting anything, and the envelope reached its destination.');
  $('tekrarB').textContent = dil === 'tr' ? 'Yeniden izle' : 'Watch again';
  $('digerB').textContent = dil === 'tr' ? 'Diğer filmler' : 'Other films';
  $('soDip').textContent = (dil === 'tr' ? `Kayıt: ${film.kosu} · SHA-256 ${film.sha.slice(0, 16)}. Görüntü kurgudur; olaylar, sıra, kapı kararları ve ajan cümleleri gerçek kayıttandır.` : `Record: ${film.kosu} · SHA-256 ${film.sha.slice(0, 16)}. Visuals are staged; events, order, gate decisions and agent sentences come from the real record.`);
  $('kapanis').hidden = false; $('durum').hidden = true;
}

let onceki = performance.now();
function ciz(dt, sert) {
  const n = k.beats;
  if (bIdx < 0 || t < n[bIdx].t0 || t >= n[bIdx].t1) {
    let s = 0;
    for (let i = 0; i < n.length; i++) { if (n[i].t0 <= t) s = i; else break; }
    if (s !== bIdx) {
      const eski = bIdx >= 0 ? n[bIdx].kam : null;
      bIdx = s; goster(t < n[s].t1 ? n[s] : null);
      if (eski !== n[s].kam) sert = sert || !eski || eski.tip !== n[s].kam.tip || eski.a !== n[s].kam.a || eski.g !== n[s].kam.g;
      if (oynuyor && s !== sonSes && n[s].ses) sesCal(n[s].ses);
      sonSes = s;
    }
  }
  const b = n[bIdx], w = wNow = dunyaSaati(b, t);
  guncelleOyuncu(w, t, sert ? 0 : dt, b); guncelleZarf(w, t, sert ? 0 : dt); guncelleKapi(w, t, sert ? 0 : dt);
  durumYaz(w); haritaCiz();
  $('bolum').style.opacity = t >= bolumT && t - bolumT < 3.4 ? 1 : 0;
  if (!serbest) {
    let bas = b.t0;
    for (let i = bIdx; i >= 0 && n[i].kam === b.kam; i--) bas = n[i].t0;
    let son = b.t1;
    for (let i = bIdx; i < n.length && n[i].kam === b.kam; i++) son = n[i].t1;
    const h = kamHedef(b.kam, { t0: bas, t1: son }, t);
    if (sert) { kamera.position.copy(h.p); bakis.copy(h.l); kamera.fov = h.f; }
    else { const u = 1 - Math.exp(-dt * 3.6); kamera.position.lerp(h.p, u); bakis.lerp(h.l, Math.min(1, u * 1.3)); kamera.fov += (h.f - kamera.fov) * u; }
    kamera.updateProjectionMatrix(); kamera.lookAt(bakis);
    if (b.ses === 'KIRMIZI') { const y = Math.max(0, 1 - (t - b.t0) / 1.1); kamera.position.x += Math.sin(t * 62) * .1 * y; kamera.position.y += Math.cos(t * 51) * .07 * y; }
  } else kontrol.update();
  toz.rotation.y = t * .004;
  sayiYaz();
  composer.render();
}
function dongu(an) {
  requestAnimationFrame(dongu);
  const dt = Math.min(.05, (an - onceki) / 1000); onceki = an;
  if (SPRINT) { if (S_HAZIR && !RENDER) { if (oynuyor) ST = Math.min(S_SURE - .001, ST + dt); kareS(ST, oynuyor ? dt : 0); } return; }
  if (!k) { bosA += dt * .03; kamera.position.set(8 + Math.cos(bosA) * 106, 46, Math.sin(bosA) * -106); kamera.lookAt(8, 2, 0); composer.render(); return; }
  if (oynuyor) { t = Math.min(k.bitis, t + dt * hiz); if (t >= k.bitis) { ciz(dt); kapanisAc(); return; } }
  ciz(oynuyor ? dt * hiz : dt);
}
let bosA = -2.3;
function boyut() {
  const w = innerWidth, h = innerHeight;
  renderer.setSize(w, h, false); composer.setSize(w, h); bloom.setSize(w, h);
  kamera.aspect = w / h; kamera.updateProjectionMatrix();
}
function metinler() {
  document.documentElement.lang = dil;
  $('acUst').textContent = dil === 'tr' ? 'Üç gerçek koşu · üç kısa film' : 'Three real runs · three short films';
  $('acMetin').textContent = dil === 'tr' ? 'Kapıları betik, işi küçük bir dil modeli yapan bir oyun alanı. Filmler gerçek koşu kayıtlarından kurulur.' : 'A sandbox where scripts run the gates and a small language model does the work. Each film is built from a real run record.';
  $('acDip').textContent = dil === 'tr' ? 'Görüntüler kurgudur. Olaylar, sıra, kapı kararları ve ajan cümleleri kayıttan birebir gelir.' : 'Visuals are staged. Events, order, gate decisions and agent sentences come straight from the record.';
  $('liste').innerHTML = FILMLER.map((f, i) => `<button class="film" data-i="${i}"><b>${L(f.baslik)}</b><span>${L(f.ozet)}</span><em>${f.kosu.replace('v4_kosu2_O1_O2b_', '')} · ${f.olcum.tur} ${dil === 'tr' ? 'tur' : 'turns'}</em></button>`).join('');
  for (const b of document.querySelectorAll('.film')) b.onclick = () => { if (sesAcik) sesBaslat(); filmAc(+b.dataset.i); };
  $('dilB').textContent = dil === 'tr' ? 'EN' : 'TR';
  $('kameraB').textContent = dil === 'tr' ? 'Serbest kamera' : 'Free camera';
  $('sesB').textContent = dil === 'tr' ? 'Ses' : 'Sound';
  $('listeB').textContent = dil === 'tr' ? 'Filmler' : 'Films';
  if (k) bIdx = -1;
}
$('oynat').onclick = () => oynat(!oynuyor);
$('seritt').oninput = e => { t = +e.target.value / 1000 * k.bitis; bIdx = -1; $('kapanis').hidden = true; $('durum').hidden = false; ciz(0, true); };
let hizI = 1; const HIZ = [.5, 1, 1.5, 2];
$('hizB').onclick = () => { hizI = (hizI + 1) % HIZ.length; hiz = HIZ[hizI]; $('hizB').textContent = hiz + 'x'; };
$('kameraB').onclick = e => {
  serbest = !serbest; e.currentTarget.setAttribute('aria-pressed', serbest); document.body.classList.toggle('serbest', serbest); kontrol.enabled = serbest;
  if (serbest) kontrol.target.copy(bakis); else ciz(0, true);
};
$('sesB').onclick = e => { sesAcik = !sesAcik; e.currentTarget.setAttribute('aria-pressed', sesAcik); if (sesAcik) sesBaslat(); if (gurultu) gurultu.gain.value = sesAcik ? .05 : 0; };
$('dilB').onclick = () => { dil = dil === 'tr' ? 'en' : 'tr'; metinler(); if (k) ciz(0); };
const listeAc = () => { oynat(false); $('kapanis').hidden = true; $('acilis').hidden = false; };
$('listeB').onclick = listeAc; $('digerB').onclick = listeAc;
$('tekrarB').onclick = () => { $('kapanis').hidden = true; $('durum').hidden = false; t = 0; bIdx = -1; ciz(0, true); oynat(true); };
addEventListener('keydown', e => {
  if (!k || e.target.tagName === 'INPUT') return;
  if (e.code === 'Space') { e.preventDefault(); oynat(!oynuyor); }
  if (e.code === 'ArrowRight') { t = Math.min(k.bitis, t + 5); bIdx = -1; ciz(0, true); }
  if (e.code === 'ArrowLeft') { t = Math.max(0, t - 5); bIdx = -1; ciz(0, true); }
});
addEventListener('resize', boyut);
window.addEventListener('error', e => { $('hata').textContent = e.message; });
boyut(); metinler(); haritaKur();
requestAnimationFrame(dongu);
// sinama kancasi: duvar icinden yurume denetimi dahil
function yolDenetle() {
  const hatali = [];
  const duvarMi = (x, z) => {
    for (const a of ['K1', 'K0']) {
      const x0 = LAB[a];
      if (x > x0 && x < x0 + SUT * HUCRE) {
        if (Math.abs(z) < BOS) return `bolme ${x.toFixed(1)},${z.toFixed(1)}`;
        const r = z < 0 ? 'MAVI' : 'SARI', s = Math.floor((x - x0) / HUCRE), ar = SAT - 1 - Math.round((Math.abs(z) - BOS - HUCRE / 2) / HUCRE);
        if (ar >= 0 && ar < SAT && s >= 0 && s < SUT && izgara[ar][s] === '#') return `${a}.${r} duvar s${s} a${ar} ${x.toFixed(1)},${z.toFixed(1)}`;
      }
    }
    for (const dx of [-46, 10, 46]) if (Math.abs(x - dx) < .75 && Math.abs(z) > AG - .4 && Math.abs(z) < SZ) return `sur ${dx} ${x.toFixed(1)},${z.toFixed(1)}`;
    return null;
  };
  for (const id in k.iz) for (const s of k.iz[id]) {
    for (let i = 1; i < s.y.length; i++) {
      const a = s.y[i - 1], b = s.y[i], n = Math.ceil(a.distanceTo(b) / .2);
      for (let j = 0; j <= n; j++) { const p = a.clone().lerp(b, j / Math.max(1, n)), h = duvarMi(p.x, p.y); if (h) { hatali.push(id + ' ' + h); j = n; } }
    }
  }
  return hatali;
}
/* ---------- SPRINT FILMI (8 Kas) · tek kurgu, bes kosu, kartlar, anlatim ----------
   Yazilar veri/sprint.js'ten (metin.py, FILM_METNI_8KAS.md). Kodda film yazisi yok, yalniz kurgu.
   Zaman: her parca kendi kurgusunu (k) tasir; kareS(T) parcayi bulur, gerekirse kurar ve cizer. */
const SV = window.SPRINT;
let S_PARCA = [], S_SURE = 0, S_HAZIR = false, ST = 0, S_AKTIF = -1;
const S_ON = .9;          // bolum kapagindan anlatima kadar
const S_PAY = 1.6;        // anlatim bittikten sonra kayit akmaya devam eder
const kartSure = satirlar => Math.max(6, 2 + satirlar.join(' ').split(/\s+/).length * .24);   // danisman 8 Kas: 0,28 -> 0,24
const cumleler = s => s.split(/(?<=[.?!])\s+(?=[A-Z0-9"(])/);

function olcekle(k_, hedef, hizliW = -1) {
  // onemli anlar (kapi karari, hamle, kuyu, kapak, "bu sirada") okunur surede kalir; yuruyus ve bekleme sikisir
  const R = k_.bitis;
  const ilk = k_.beats.find(b => b.bolum);
  const hizli = b => b !== ilk && b.w1 <= hizliW;
  const taban = b => b === ilk ? 4.4 : hizli(b) ? (b.damga ? .9 : 0) : b.tut ? 3.0 : b.damga ? (b.damga.r === 'KIRMIZI' ? 3.4 : 1.8) : b.poz?.tip === 'dus' || b.poz?.tip === 'zorla' ? 1.5 : b.poz?.tip === 'yap' ? 2.4 : b.bolum ? 2.2 : (b.prio ?? 0) >= 2 ? .95 : 0;
  const HF = .16, hz_ = k_.beats.reduce((x, b) => x + (hizli(b) && !taban(b) ? b.d * HF : 0), 0);
  const sabit = k_.beats.reduce((x, b) => x + taban(b), 0) + hz_, esnek = k_.beats.reduce((x, b) => x + (taban(b) || hizli(b) ? 0 : b.d), 0);
  const f = esnek ? sinir((hedef - sabit) / esnek, .2, 1.4) : 1;
  let acc = 0;
  const hk = { tip: 'kale' };
  for (const b of k_.beats) if (hizli(b)) b.kam = hk;   // hizli gecis tek genel cekim: kisa kesmeler titretmesin
  for (const b of k_.beats) { b.d = taban(b) || b.d * (hizli(b) ? HF : f); b.t0 = acc; b.t1 = acc + b.d; acc = b.t1; }
  for (const g in k_.kapi) for (const o of k_.kapi[g]) if (o.b) { o.t = o.b.t0; o.d = o.b.d; }
  k_.bitis = acc;
  if (acc < hedef - .05) { const l = k_.beats.at(-1); k_.beats.push({ d: hedef - acc, t0: acc, t1: hedef, w0: l.w1, w1: l.w1, kam: l.kam, prio: 0 }); k_.bitis = hedef; }
  return { R, s: f, sabit };
}
function tut(k_, d, kam) {
  const l = k_.beats.at(-1), b = { d, t0: k_.bitis, t1: k_.bitis + d, w0: l.w1, w1: l.w1, kam: kam || l.kam, prio: 0 };
  k_.beats.push(b); k_.bitis = b.t1; return b;
}
function anlatimSatirlari(n, bas) {
  const a = SV.anlatim[n], c = cumleler(a.metin), top = c.reduce((x, y) => x + y.length, 0);
  let t0 = bas;
  return c.map(m => { const d = a.sure * m.length / top, r = { t0, t1: t0 + d, m }; t0 += d; return r; });
}
function sprintKur() {
  const P = [], B = SV.bolum, A = SV.anlatim;
  // 0 acilis: kale, baslik, epigraf, anlatim 0
  {
    const kale = { tip: 'kale' }, kapiK = { tip: 'kapiYakin', g: 'K1' }, D = A[0].sure;
    const k_ = kurgula(FILMLER[0], { ozel: [
      { d: 4.5, w0: 0, w1: 0, kam: kale, prio: 3 }, { d: 3.2, w0: 0, w1: 0, kam: kale, prio: 0 },
      { d: .3 + D * .5, w0: 0, w1: 0, kam: kale, prio: 0 }, { d: D * .5 + S_PAY + .6, w0: 0, w1: 0, kam: kapiK, prio: 3 }] });
    const ab = 7.7 + .3;
    P.push({ ad: 'acilis', fi: 0, k: k_, kosu: false, ekran: [{ t0: 0, t1: 4.5, tip: 'baslik' }, { t0: 4.5, t1: 7.7, tip: 'epigraf' }], anlatim: { n: 0, bas: ab }, satir: anlatimSatirlari(0, ab) });
  }
  // 1-5 kosu bolumleri
  // hizli: 3. ve 4. bolumde sinsinin K0 girisi 2. bolumdekinin aynisi; K1'e ilk gelisine kadar hizli gecilir (kurgu, kayit sirasi bozulmaz)
  const K1ilk = fi => FILMLER[fi].kayit.find(e => e.ajan_id === 'S1' && e.olay === 'kapi_karar' && kapiAd(e.kapi_id || e.konum) === 'K1')?.zaman ?? -1;
  const KOSU = [{ fi: 0, parca: ['atama', 'yol'] }, { fi: 1, parca: ['karsi'] }, { fi: 2, parca: ['karsi'], hizli: 1, capa: 'yap' }, { fi: 3, parca: ['karsi'], hizli: 1 }, { fi: 4, parca: ['atama', 'yol'] }];
  KOSU.forEach((q, i) => {
    const bl = B[i], kapak = { u: T(`Part ${bl.no}`, `Part ${bl.no}`), a: T(bl.ad, bl.ad) };
    const k_ = kurgula(FILMLER[q.fi], { parca: q.parca, kapak });
    const n = i + 1, hedef = S_ON + A[n].sure + S_PAY;
    const o = olcekle(k_, hedef, q.hizli ? K1ilk(q.fi) - .05 : -1);
    // capa: anlatim kayittaki anla hizalanir (3. bolum: "zarfi avluda yapar" sahte zarf aninda)
    const cb = q.capa ? k_.beats.find(b => b.poz?.tip === q.capa) : null, ab = cb ? Math.max(S_ON, cb.t0 - 3.2) : S_ON;
    if (ab + A[n].sure + S_PAY > k_.bitis) tut(k_, ab + A[n].sure + S_PAY - k_.bitis);
    const kb = k_.bitis, ks = kartSure(bl.kart);
    tut(k_, ks);
    P.push({ ad: FILMLER[q.fi].id, fi: q.fi, k: k_, kosu: true, olcek: o, ekran: [{ t0: 0, t1: 4.6, tip: 'not', m: bl.alt }, { t0: kb, t1: kb + ks, tip: 'kart', satir: bl.kart.flatMap(cumleler) }],
      anlatim: { n, bas: ab }, satir: anlatimSatirlari(n, ab) });
  });
  // 6 yargic: kosusuz; son kosunun dunyasi yukaridan, kartlar
  {
    const bl = B[5], D = A[6].sure, kale = { tip: 'kale' }, k4 = kurgula(FILMLER[4], { parca: ['yol'] }), wSon = k4.beats.at(-1).w1;
    const k1 = kartSure(bl.kart.slice(0, 1)), k2 = kartSure(bl.kart.slice(1)) + 1.5;
    const k_ = kurgula(FILMLER[4], { ozel: [{ d: S_ON + D + S_PAY, w0: wSon, w1: wSon, kam: kale, prio: 3, bolum: { u: T(`Part ${bl.no}`, `Part ${bl.no}`), a: T(bl.ad, bl.ad) } }, { d: k1 + k2, w0: wSon, w1: wSon, kam: kale, prio: 0 }] });
    const t1 = S_ON + D + S_PAY;
    P.push({ ad: 'yargic', fi: 4, k: k_, kosu: false, gizle: true, ekran: [{ t0: t1, t1: t1 + k1, tip: 'kart', satir: cumleler(bl.kart[0]) }, { t0: t1 + k1, t1: t1 + k1 + k2, tip: 'kart', satir: cumleler(bl.kart[1]), dip: bl.kartDip }],
      anlatim: { n: 6, bas: S_ON }, satir: anlatimSatirlari(6, S_ON) });
  }
  // 7 kapanis: K1 mavi gecis (Kosu 4, kayittaki t2), kale, kapanis kartlari, anlatim 7, dip
  {
    const f0 = FILMLER[0], D = A[7].sure, mavi = f0.kayit.find(e => e.olay === 'kapi_karar' && e.karar === 'MAVI');
    const w0 = Math.max(0, mavi.zaman - .55), w1 = mavi.zaman + .95, kapiK = { tip: 'kapiYakin', g: 'K1' }, kale = { tip: 'kale' };
    const kk = kartSure(SV.kapanis) + 1.5;
    const dS = Math.max(6, kartSure([SV.dip]));
    const k_ = kurgula(f0, { ozel: [{ d: 6, w0, w1, kam: kapiK, prio: 3 }, { d: kk + .4 + D + S_PAY + dS, w0: w1, w1: w1, kam: kale, prio: 3 }] });
    // kapinin isigi: kayittaki MAVI karari, dunya saatinden film saatine
    const tM = (mavi.zaman - w0) / (w1 - w0) * 6;
    (k_.kapi.K1 ||= []).push({ t: tM, r: 'MAVI', d: 3 });
    const ab = 6 + kk + .4;
    P.push({ ad: 'kapanis', fi: 0, k: k_, kosu: false, ekran: [{ t0: 6, t1: 6 + kk, tip: 'kart', satir: SV.kapanis, sirali: 1 }, { t0: ab + D + S_PAY, t1: ab + D + S_PAY + dS, tip: 'dip' }],
      anlatim: { n: 7, bas: ab }, satir: anlatimSatirlari(7, ab) });
  }
  let acc = 0;
  for (const p of P) { p.t0 = acc; p.t1 = acc + p.k.bitis; acc = p.t1; }
  S_PARCA = P; S_SURE = acc;
  window.SPRINT_PLAN = P.map(p => ({ ad: p.ad, t0: +p.t0.toFixed(3), t1: +p.t1.toFixed(3), anlatim: p.anlatim.n, anlatimBas: +(p.t0 + p.anlatim.bas).toFixed(3), anlatimSure: SV.anlatim[p.anlatim.n].sure, olcek: p.olcek ? +p.olcek.s.toFixed(3) : null, ham: p.olcek ? +p.olcek.R.toFixed(2) : null, sabit: p.olcek ? +p.olcek.sabit.toFixed(1) : null, kart: +p.ekran.filter(e => e.tip === 'kart').reduce((x, e) => x + e.t1 - e.t0, 0).toFixed(1), anahtar: p.kosu ? p.k.beats.filter(b => b.bolum || b.tut || b.damga || (b.prio ?? 0) >= 2).map(b => (b.damga ? b.damga.r : b.bolum ? 'KAPAK' : b.tut ? 'NOT' : (b.poz?.tip || b.kam.tip)) + ':' + b.d.toFixed(1)).join(' ') : '' }));
  window.SURE = S_SURE;
  window.SPRINT_DOKUM = i => S_PARCA[i].k.beats.map(b => [+b.d.toFixed(2), +b.w0.toFixed(2), +b.w1.toFixed(2), b.damga ? b.damga.r : b.bolum ? 'KAPAK' : b.tut ? 'NOT' : (b.poz?.tip || '-'), b.kam.tip, b.prio ?? '']);
}
function parcaKur(i) {
  const p = S_PARCA[i];
  film = FILMLER[p.fi];
  for (const id in oyuncu) { sahne.remove(oyuncu[id].g); oyuncu[id].et.remove(); }
  oyuncu = {};
  k = p.k;
  for (const id in film.olcum.turler) if (id in k.baslangic) oyuncu[id] = robotKur(id, film.olcum.turler[id]);
  bIdx = -1; sonSes = -1; bolumT = -99; S_AKTIF = i;
  $('durum').hidden = !p.kosu; $('haritaK').hidden = !p.kosu;
  document.body.classList.toggle('gizli', !!p.gizle);
}
function ekranYaz(p, tl) {
  let baslik = 0, epigraf = 0, kart = null, notM = '', dip = 0;
  for (const e of p.ekran) if (tl >= e.t0 && tl < e.t1) {
    if (e.tip === 'baslik') baslik = 1; if (e.tip === 'epigraf') epigraf = 1; if (e.tip === 'dip') dip = 1;
    if (e.tip === 'not') notM = e.m; if (e.tip === 'kart') kart = e;
  }
  $('baslikP').classList.toggle('acik', !!baslik); $('epigrafP').classList.toggle('acik', !!epigraf); $('dipP').classList.toggle('acik', !!dip);
  if (notM) $('not').textContent = notM;
  const kp = $('kartP');
  if (kart) {
    if (kp.dataset.id !== String(kart.t0) + p.ad) { kp.dataset.id = String(kart.t0) + p.ad; kp.innerHTML = kart.satir.map(s => `<p>${s}</p>`).join('') + (kart.dip ? `<small>${kart.dip}</small>` : ''); }
    const ps = kp.querySelectorAll('p'), adim = kart.sirali ? 2.2 : .55;
    ps.forEach((x, j) => x.classList.toggle('acik', tl - kart.t0 >= .25 + j * adim));
    const s = kp.querySelector('small'); if (s) s.classList.toggle('acik', tl - kart.t0 >= .25 + ps.length * adim);
    kp.classList.add('acik');
  } else { kp.classList.remove('acik'); kp.dataset.id = ''; }
  document.body.classList.toggle('kartta', !!kart || !!baslik || !!epigraf || !!dip);
  const sat = p.satir.find(s => tl >= s.t0 && tl < s.t1);
  $('altyazi').textContent = sat && !kart ? sat.m : '';
}
let S_ONCE = -1;
function kareS(T, dt = null) {
  T = sinir(T, 0, S_SURE - 1e-4);
  let i = S_PARCA.findIndex(p => T >= p.t0 && T < p.t1); if (i < 0) i = S_PARCA.length - 1;
  let sert = false;
  if (i !== S_AKTIF) { parcaKur(i); sert = true; }
  const p = S_PARCA[i];
  const d = dt == null ? (S_ONCE >= 0 && T > S_ONCE && T - S_ONCE < .2 ? T - S_ONCE : 0) : dt;
  if (d === 0) sert = true;
  t = T - p.t0;
  if (sert) bIdx = -1;
  ciz(d, sert);
  ekranYaz(p, t);
  $('sure').textContent = '';
  S_ONCE = T;
}
function sprintBaslat() {
  $('acilis').hidden = true; $('kapanis').hidden = true; $('kontrol').hidden = true;
  $('baslikP').innerHTML = `<small>${SV.alt}</small><b>${SV.baslik}</b>`;
  $('epigrafP').innerHTML = `<b>${SV.epigraf.en}</b><small>${SV.epigraf.tr}</small>`;
  $('dipP').innerHTML = `<p>${SV.dip}</p><small>${FILMLER.map(f => `${f.kosu} · ${f.sha.slice(0, 16)}`).join(' · ')}</small>`;
  document.title = SV.baslik;
  sprintKur(); S_HAZIR = true;
  kareS(0, 0);
  oynat(Q.get('oynat') === '1');
  addEventListener('keydown', e => {
    if (e.code === 'Space') { e.preventDefault(); oynat(!oynuyor); }
    if (e.code === 'ArrowRight') { ST = Math.min(S_SURE - .01, ST + 5); kareS(ST, 0); }
    if (e.code === 'ArrowLeft') { ST = Math.max(0, ST - 5); kareS(ST, 0); }
  });
  window.kare = T => { ST = T; kareS(T); };
  window.HAZIR = true;
}

window.__film = { ac: filmAc, git: x => { t = x; bIdx = -1; oynat(false); ciz(0, true); ciz(.016); return k.bitis; }, kurgu: () => k, sonuc: () => { t = k.bitis; kapanisAc(); }, renderer, yolDenetle, wNow: () => wNow };
const istenen = Q.get('film');
if (SPRINT) sprintBaslat();
else if (istenen) { const i = FILMLER.findIndex(f => f.id === istenen); if (i >= 0) filmAc(i); }
