#!/usr/bin/env python3
"""
Interactive Real-Time Terminal Monitor for Synthetic M2M Economy.
Allows manual injection of agent tasks, market inspection, and balance tracking.
"""

import sys
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


def main():
    exchange = M2MExchange()

    # Pre-seed network with agents
    buyer = ResearchBuyerAgent("Investor_Agent_Prime", exchange.ledger, exchange.escrow, initial_balance=250.0)
    gpu_cluster_1 = ComputeProviderAgent("H100_Supercluster", exchange.ledger, initial_balance=50.0, base_unit_price=15.0, latency_ms=45)
    gpu_cluster_2 = ComputeProviderAgent("A100_Budget_Grid", exchange.ledger, initial_balance=35.0, base_unit_price=9.0, latency_ms=110)

    exchange.register_agent(buyer)
    exchange.register_agent(gpu_cluster_1)
    exchange.register_agent(gpu_cluster_2)

    cycle_count = 0

    while True:
        print(f"\n{BOLD}{CYAN}======================================================================{RESET}")
        print(f"{BOLD}{MAGENTA}      🌐 SYNTHETIC M2M ECONOMY - REAL-TIME MARKET TICKER (2030+){RESET}")
        print(f"{BOLD}{CYAN}======================================================================{RESET}")

        stats = exchange.get_market_statistics()
        print(f"Jami aylanma kapital: {GREEN}{stats['circulating_capital']} SynthoCredits{RESET} | Protokol xazinasi: {YELLOW}{stats['treasury_collected_fees']} credits{RESET}")
        print(f"Blokdagi tranzaksiyalar: {stats['total_transactions_count']} ta | Aktiv agentlar: {stats['registered_agents_count']} ta\n")

        print(f"{BOLD}Faol Kiber-Agentlar va Ularning Hamyonlari:{RESET}")
        for addr, agent in exchange.registered_agents.items():
            status = f"{GREEN}SOLVENT{RESET}" if agent.is_solvent else f"{RED}BANKRUPT{RESET}"
            print(f"  • {BOLD}@{agent.name:<22}{RESET} | Balans: {GREEN}{agent.balance:>7.2f} credits{RESET} | Obro': {agent.reputation:.2f}⭐ | [{status}]")

        print(f"""
{BOLD}Buyruqlar:{RESET}
  {BOLD}[1]{RESET} yoki {BOLD}[Enter]{RESET} -> Yangi avtonom M2M savdo siklini boshlash (Auto-Trade Cycle)
  {BOLD}[2]{RESET}         -> Tranzaksiyalar o'zgarmas blok-tarixini ko'rish (Ledger Blocks)
  {BOLD}[q]{RESET}         -> Chiqish
""")
        choice = input(f"{BOLD}Tanlovingiz: {RESET}").strip().lower()

        if choice in ("q", "quit", "exit"):
            print(f"{YELLOW}Monitor to'xtatildi.{RESET}")
            break

        if choice == "2":
            print(f"\n{GREEN}--- 📜 O'ZGARMAS TRANZAKSIYALAR BLOKI (IMMUTABLE LEDGER) ---{RESET}")
            for idx, tx in enumerate(exchange.ledger.history, 1):
                print(f"  #{idx:<2} [{tx.tx_id[:12]}] {tx.sender_address[:14]}.. -> {tx.recipient_address[:14]}.. : {tx.amount:.2f} credits ({tx.memo})")
            print(f"{GREEN}------------------------------------------------------------{RESET}")
            input(f"{DIM}Davom etish uchun Enter bosing...{RESET}")
            continue

        # Execute automated M2M trade cycle
        cycle_count += 1
        print(f"\n{YELLOW}▶️ #{cycle_count}-Kiber-Savdo Sikli Bajarilmoqda...{RESET}")

        rfp = buyer.issue_rfp("inference_compute", max_budget=18.0, max_latency_ms=150)
        bids = exchange.broadcast_rfp(rfp)
        winner_tuple = buyer.evaluate_auction(rfp, bids)

        if winner_tuple:
            winner_bid, _ = winner_tuple
            agr_id = f"m2m_deal_{cycle_count}"
            buyer.contract_and_lock_escrow(agr_id, winner_bid, f"Inference task #{cycle_count}")
            winning_agent = exchange.registered_agents[winner_bid.bidder_address]
            proof = winning_agent.execute_task(f"Task #{cycle_count}")
            buyer.verify_and_settle(agr_id, proof)
            winning_agent.record_job_success(winner_bid.price)
            print(f"  ✅ @{buyer.name} @{winner_bid.bidder_name} dan {winner_bid.price:.2f} credits ga xizmat sotib oldi!")
        else:
            print(f"  ⚠️ Narx to'g'ri kelmadi, auksion bekor qilindi.")


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\nDastur to'xtatildi.")
