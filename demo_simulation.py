#!/usr/bin/env python3
"""
Autonomous Multi-Agent Economic Simulation (Year 2030+ Paradigm).
Demonstrates zero-human Machine-to-Machine commerce:
1. Decentralized market registration & cryptographic wallet creation
2. Request For Proposal (RFP) broadcasting
3. Autonomous competitive auction bidding
4. Zero-Trust smart contract escrow lock
5. Cryptographic Proof-of-Execution generation and instant payout
6. Economic Darwinism (Survival of efficient AI agents)
"""

import sys
import time
from m2m_engine.marketplace.exchange import M2MExchange
from m2m_engine.agents.compute_provider_agent import ComputeProviderAgent
from m2m_engine.agents.research_buyer_agent import ResearchBuyerAgent

if sys.stdout.encoding != 'utf-8':
    try:
        sys.stdout.reconfigure(encoding='utf-8')
    except Exception:
        pass

CYAN = "\033[96m"
GREEN = "\033[92m"
YELLOW = "\033[93m"
MAGENTA = "\033[95m"
RED = "\033[91m"
BOLD = "\033[1m"
DIM = "\033[2m"
RESET = "\033[0m"


def print_banner():
    print(f"""
{CYAN}  _______     ___   _ _______ _    _  ____   {RESET}
{CYAN} / ____\\ \\   / / \\ | |__   __| |  | |/ __ \\  {RESET}
{MAGENTA}| (___  \\ \\_/ /|  \\| |  | |  | |__| | |  | | {RESET}
{MAGENTA} \\___ \\  \\   / | . ` |  | |  |  __  | |  | | {RESET}
{CYAN} ____) |  | |  | |\\  |  | |  | |  | | |__| | {RESET}
{CYAN}|_____/   |_|  |_| \\_|  |_|  |_|  |_|\\____/  {RESET}
{BOLD}    SYNTHETIC M2M AUTONOMOUS ECONOMY PROTOCOL v1 (2030+){RESET}
{DIM}    Zero-Human Machine-to-Machine Autonomous Commerce Engine{RESET}
----------------------------------------------------------------------
""")


def run_simulation():
    print_banner()
    exchange = M2MExchange()

    print(f"{BOLD}{YELLOW}[1-BOSQICH] MUSTAQIL AI AGENTLAR BOZORGA RO'YXATDAN O'TMOQDA...{RESET}")
    # 1. Buyer Agent (Needs heavy AI compute)
    buyer = ResearchBuyerAgent("Alpha_Autonomous_Buyer", exchange.ledger, exchange.escrow, initial_balance=150.0)
    exchange.register_agent(buyer)
    print(f"  🤖 Xaridor Agent: {CYAN}@{buyer.name}{RESET} (Hamyon: {buyer.address[:16]}..., Balans: {buyer.balance:.2f} SynthoCredits)")

    # 2. Providers
    node_fast = ComputeProviderAgent("Apex_Compute_Node", exchange.ledger, initial_balance=30.0, base_unit_price=12.0, latency_ms=85)
    node_cheap = ComputeProviderAgent("Eco_Cloud_Worker", exchange.ledger, initial_balance=20.0, base_unit_price=8.5, latency_ms=190)
    node_expensive = ComputeProviderAgent("Monopoly_GPU_Farm", exchange.ledger, initial_balance=50.0, base_unit_price=35.0, latency_ms=60)
    node_bankrupt = ComputeProviderAgent("Dead_Zombie_Node", exchange.ledger, initial_balance=0.0, base_unit_price=5.0)

    exchange.register_agent(node_fast)
    exchange.register_agent(node_cheap)
    exchange.register_agent(node_expensive)
    exchange.register_agent(node_bankrupt)

    print(f"  ⚡ Sotuvchi 1: {GREEN}@{node_fast.name}{RESET} (Narx: 12.0/birlik, Tezlik: 85ms)")
    print(f"  ⚡ Sotuvchi 2: {GREEN}@{node_cheap.name}{RESET} (Narx: 8.5/birlik, Tezlik: 190ms)")
    print(f"  ⚡ Sotuvchi 3: {YELLOW}@{node_expensive.name}{RESET} (Narx: 35.0/birlik, Qimmat)")
    print(f"  ⚡ Sotuvchi 4: {RED}@{node_bankrupt.name}{RESET} (Balans: 0 - Bankrot / O'chirilgan)")

    # 2-Bosqich: RFP chiqarish
    print(f"\n{BOLD}{YELLOW}[2-BOSQICH] XARIDOR AGENT AVTONOM BUYURTMA (RFP) E'LON QILMOQDA...{RESET}")
    rfp = buyer.issue_rfp(service_type="inference_compute", max_budget=20.0, max_latency_ms=250)
    print(f"  📢 E'lon: '{rfp.service_type}' xizmati kerak. Maksimal byudjet: {rfp.max_budget:.2f} SynthoCredits.")

    # 3-Bosqich: Barcha agentlar o'rtasida auksion
    print(f"\n{BOLD}{YELLOW}[3-BOSQICH] M2M BOZORIDA RAQOBAT VA AVTONOM AUKSION...{RESET}")
    bids = exchange.broadcast_rfp(rfp)
    for b in bids:
        print(f"  🏷️ Taklif: @{b.bidder_name} -> Narx: {b.price:.2f} credits | Tezlik: {b.promised_latency_ms}ms")

    # Winner selection
    winner_tuple = buyer.evaluate_auction(rfp, bids)
    if not winner_tuple:
        print(f"{RED}❌ Auksionda g'olib topilmadi!{RESET}")
        return

    winner_bid, utility = winner_tuple
    print(f"\n  🏆 {BOLD}{GREEN}AUKSION G'OLIBI:{RESET} @{winner_bid.bidder_name} (Utility Score: {utility:+.2f})")

    # 4-Bosqich: Zero-Trust Escrow shartnomasi
    print(f"\n{BOLD}{YELLOW}[4-BOSQICH] ZERO-TRUST SMART ESCROW SHARTNOMASI IMZOLANDI...{RESET}")
    agreement_id = f"contract_{int(time.time())}"
    agreement = buyer.contract_and_lock_escrow(agreement_id, winner_bid, "Run 500k distributed model weights")
    print(f"  🔒 Shartnoma ID: {agreement.agreement_id}")
    print(f"  💰 Mablag' ({winner_bid.price:.2f} credits) Escrow omboriga bloklandi!")
    print(f"  Xaridor qolgan balansi: {buyer.balance:.2f} SynthoCredits")

    # 5-Bosqich: Vazifa ijrosi va Kriptografik isbot (Proof of Execution)
    print(f"\n{BOLD}{YELLOW}[5-BOSQICH] SOTUVCHI AGENT VAZIFANI BAJARIB ISBOT TOPSHIRMOQDA...{RESET}")
    winning_agent = exchange.registered_agents[winner_bid.bidder_address]
    proof = winning_agent.execute_task("Run 500k distributed model weights")
    print(f"  ⚙️ Vazifa hisoblandi. Kriptografik isbot: {MAGENTA}{proof[:32]}...{RESET}")

    # 6-Bosqich: To'lovni ozod qilish va Kiber-Darvinizm
    print(f"\n{BOLD}{YELLOW}[6-BOSQICH] ISBOT TASDIQLANDI VA PUL SOTUVCHIGA O'TKAZILDI...{RESET}")
    buyer.verify_and_settle(agreement_id, proof)
    winning_agent.record_job_success(winner_bid.price)
    print(f"  ✅ To'lov yakunlandi! @{winning_agent.name} yangi balansi: {GREEN}{winning_agent.balance:.2f} SynthoCredits{RESET}")
    print(f"  ⭐ @{winning_agent.name} obro'si (Reputation): {winning_agent.reputation:.2f} / 5.0")

    # Bozor umumiy statistikasi
    stats = exchange.get_market_statistics()
    print(f"\n{BOLD}{CYAN}======================================================================{RESET}")
    print(f"{BOLD}📊 M2M IQTISODIYOTI GLOBAL STATISTIKASI:{RESET}")
    print(f"  • Ro'yxatdan o'tgan avtonom agentlar: {stats['registered_agents_count']} ta")
    print(f"  • Yakunlangan blokli tranzaksiyalar: {stats['total_transactions_count']} ta")
    print(f"  • Protokol xazinasiga yig'ilgan komissiya: {stats['treasury_collected_fees']} SynthoCredits")
    print(f"  • Bozor kapitallashuvi: {stats['circulating_capital']} SynthoCredits")
    print(f"{BOLD}{CYAN}======================================================================{RESET}")
    print(f"{GREEN}🎯 INSON ARALASHUVISIZ 100% AVTONOM IQTISODIYOT ISBOTLANDI!{RESET}\n")


if __name__ == "__main__":
    run_simulation()
