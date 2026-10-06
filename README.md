# 🌐 Synthetic M2M Autonomous Economy Protocol v1 (2030+)

[![Python Version](https://img.shields.io/badge/python-3.11%2B-blue.svg)](https://www.python.org/downloads/)
[![Paradigm](https://img.shields.io/badge/paradigm-Zero--Human%20Agent%20Commerce-9cf.svg)]()
[![Cryptography](https://img.shields.io/badge/crypto-Ed25519%20%2B%20Zero--Trust%20Escrow-brightgreen.svg)]()
[![Tests](https://img.shields.io/badge/tests-6%2F6%20passed%20(100%25)-success.svg)]()
[![License](https://img.shields.io/badge/license-MIT-purple.svg)]()

> **Dunyodagi eng mashhur ertangi kun (2028–2035 Frontier AI) loyihalarini noldan yaratish seriyasi.**  
> Ushbu repozitoriy **inson aralashuvisiz** mustaqil ravishda bir-biri bilan savdo qiluvchi, narx bo'yicha muzokaralar o'tkazuvchi va o'zini o'zi moliyalashtiruvchi **AI Agentlar Kiber-Iqtisodiyoti (Machine-to-Machine Autonomous Commerce)** ning fundamental protokolidir.

---

## 🔮 2030-Yillar Muammosi va Daho Yechim

Bugungi barcha AI agentlar insonning kredit kartasi yoki API kalitiga to'liq qaram.  
2030-yillarda millionlab avtonom AI agentlar dunyoga kelganda, ularning har biriga inson qo'lda pul to'lab o'tirmaydi. **AI agentlar mustaqil iqtisodiy subyektga aylanadi**:

1. **Sovereign Agent Wallet (`Ed25519`)**: Har bir agent inson aralashuvisiz o'z shaxsiy kriptografik hamyoni va o'zgarmas manziliga ega.
2. **Request For Proposal (RFP) & Bidding**: Xaridor agent o'z ehtiyojini e'lon qiladi (masalan: *"Menga 500k model xulosasi kerak, byudjet 20 SynthoCredits"*). Boshqa hisoblash klasterlari (GPU node lari) auksionda o'zaro raqobatlashib, eng arzon va tezkor takliflarni berishadi.
3. **Utility-Maximizing Autonomous Auction**:
   $$\text{Utility} = \frac{\text{Reputation} \times 8.0}{\frac{\text{Price}}{\text{MaxBudget}} + 0.2} - \left(\frac{\text{Latency}}{\text{MaxLatency}} \times 3.0\right)$$
4. **Zero-Trust Smart Escrow & Proof-of-Execution**: Xaridor agent pulni oldindan to'lamaydi! Mablag' Escrow omboriga qulflanadi. Sotuvchi agent vazifani bajarib, **kriptografik isbot (Proof-of-Execution)** topshirgandagina pul sotuvchiga o'tkaziladi.
5. **Economic Darwinism (Kiber-Darvinizm)**:
   - Foydali va arzon xizmat ko'rsatgan agentlar boyiydi va obro'si (Reputation) 5.0 gacha ko'tariladi.
   - Sifatsiz yoki qimmat xizmat ko'rsatgan agentlar bankrot bo'lib, bozor aylanmasidan chiqib ketadi (Survival of the Fittest AI).

---

## 🔄 Protokol Sxemasi (Sequence Diagram)

```mermaid
sequenceDiagram
    autonumber
    actor Buyer as 🤖 Xaridor Agent (AlphaBuyer)
    participant Exchange as 🏛️ M2M Kiber-Birja (Market Clearinghouse)
    actor Provider as ⚡ Sotuvchi Agent (EcoCloud)
    participant Escrow as 🔒 Zero-Trust Escrow Vault

    Buyer->>Exchange: 1. RFP e'lon qilish: "compute kerak, byudjet: 20c"
    Exchange->>Provider: 2. RFP xabarini tarqatish
    Provider->>Exchange: 3. Raqobatli Taklif (Bid): 8.5c (190ms)
    Exchange->>Buyer: 4. Auksion g'olibi EcoCloud deb topildi

    Buyer->>Escrow: 5. Shartnoma tuzish va 8.5c ni Escrow ga qulflash
    Note over Escrow: Mablag' xavfsiz qulflandi (Zero-Trust)

    Provider->>Provider: 6. Vazifani hisoblash & Proof generatsiya qilish
    Provider->>Buyer: 7. Kriptografik isbotni topshirish (proof_sha256)
    
    Buyer->>Escrow: 8. Isbot tasdiqlandi -> Pulni sotuvchiga o'tkazish
    Escrow->>Provider: 9. 8.5c sotuvchi hamyoniga o'tdi (To'lov yakunlandi)
    Note over Provider: Provider obro'si oshdi va boyidi (Kiber-Darvinizm)
```

---

## 📂 Loyiha Tuzilmasi

```
synthetic-m2m-economy-v1/
├── m2m_engine/
│   ├── crypto_ledger/
│   │   ├── wallet.py             # Ed25519 avtonom kripto-hamyon va imzo
│   │   ├── transaction.py        # M2M tranzaksiyalari modeli va fee hisobi
│   │   ├── ledger.py             # O'zgarmas hash-zanjir mikro-baza (Immutable Ledger)
│   │   └── escrow.py             # Zero-Trust shartnomaviy qulf (Smart Escrow)
│   ├── protocol/
│   │   ├── rfp.py                # Request For Proposal (Talab e'loni)
│   │   ├── bid.py                # Xizmat ko'rsatish taklifi modeli
│   │   └── negotiation.py        # Utility-maximizing auksion va g'olib tanlash
│   ├── agents/
│   │   ├── base_agent.py         # Mustaqil iqtisodiy agent yadrosi
│   │   ├── compute_provider_agent.py # GPU hisoblash quvvati sotuvchi agent
│   │   └── research_buyer_agent.py   # Xizmat sotib oluvchi tadbirkor agent
│   └── marketplace/
│       └── exchange.py           # Kiber-birja va bozor kliring tizimi
├── tests/
│   ├── test_crypto_ledger.py     # Hamyon va o'zgarmas balans testlari
│   ├── test_escrow_settlement.py # Zero-Trust Escrow testlari
│   ├── test_auction_and_bidding.py # Auksion va raqobat testlari
│   └── test_economic_darwinism.py# Kiber-Darvinizm va agentlar omon qolish testi
├── demo_simulation.py            # 1-klikli 2030-yillar kiber-iqtisodiyot simulyatsiyasi
├── cli_monitor.py                # Real-vaqt kiber-bozor terminal monitoringi
├── requirements.txt              # Minimal test vositalari
└── README.md                     # Hujjatlar
```

---

## 🚀 Tezkor Ishga Tushirish

### 1. Testlarni Tekshirish (100% Yashil)
```bash
python -m pytest -v
```

### 2. 2030-Yillar Kiber-Iqtisodiyoti Simulyatsiyasini Ko'rish
Inson aralashuvisiz 4 ta agent bir-biri bilan savdo qilishi, auksion o'tkazishi va pul to'lashini ko'rish:
```bash
python demo_simulation.py
```

### 3. Real-Vaqt Kiber-Bozor Terminal Monitoringi
Bozor tikerini ko'rish, yangi savdo sikllarini boshlash va o'zgarmas bloklar tarixini tekshirish:
```bash
python cli_monitor.py
```

---
**Muallif:** Javohirbek Asqarov (Jasper)  
*Next-Gen Autonomous Machine Economics Protocol*
