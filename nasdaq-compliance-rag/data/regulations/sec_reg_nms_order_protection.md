---
doc_id: "SEC-REG-NMS"
title: "SEC Regulation NMS (17 CFR §§ 242.600–613): National Market System, Order Protection, Access Fees & Sub-Penny Rule"
jurisdiction: "SEC"
citation_prefix: "17 CFR § 242.611"
effective_date: "2005-08-29"
last_amended: "2024-09-18"
category: "Market Structure, Order Routing & Best Execution"
---

# SEC Regulation NMS (17 CFR §§ 242.600–613) — National Market System Rules

## § 242.611 (Rule 611) Order Protection Rule ("Trade-Through Rule")

### § 242.611(a)(1) Requirement to Prevent Trade-Throughs of Protected Quotations
A trading center (including any national securities exchange such as **Nasdaq**, any alternative trading system (ATS), exchange market maker, OTC market maker, or any other broker or dealer that executes orders internally) shall establish, maintain, and enforce written policies and procedures that are reasonably designed to prevent **trade-throughs** on that trading center of **protected quotations** in NMS stocks that do not fall within an exception set forth in paragraph (b) of this section and, if relying on such an exception, that are reasonably designed to assure compliance with the terms of the exception.

- **Definition of Trade-Through (`17 CFR § 242.600(b)(95)`)**: The purchase or sale of an NMS stock during regular trading hours (`9:30 a.m. to 4:00 p.m. ET`), either as principal or agent, at a price that is lower than a Protected Bid or higher than a Protected Offer.
- **Definition of Protected Quotation (`17 CFR § 242.600(b)(70)`)**: An automated quotation that is the best bid or best offer (top-of-book) of a national securities exchange (such as Nasdaq Stock Market LLC) or national securities association. Depth-of-book quotations below the top-of-book are not Protected Quotations under federal Rule 611 unless protected by exchange-specific routing logic.

### § 242.611(b) Exceptions to the Order Protection Rule

1. **System Failure / Self-Help Exception (`17 CFR § 242.611(b)(1)`)**:
   The transaction that constituted the trade-through was effected when the trading center displaying the protected quotation that was traded through was experiencing a failure, material delay, or malfunction of its systems or equipment (`> 1 second` response latency thresholds), and the routing trading center documented objective latency telemetry and declared "Self-Help" in accordance with written procedures.

2. **Intermarket Sweep Order (ISO) Exception (`17 CFR § 242.611(b)(5)` & `(b)(6)`)**:
   - **Inbound ISO Exception (`Rule 611(b)(5)`)**: The transaction that constituted the trade-through was the execution of an order identified as an **Intermarket Sweep Order (ISO)**.
   - **Outbound ISO Routing Obligation (`Rule 611(b)(6)` & `Rule 600(b)(38)`)**: A broker-dealer or trading center may mark an order as an **Intermarket Sweep Order (ISO)** **ONLY IF**, simultaneously with the routing of the limit order identified as an ISO, one or more additional limit orders, as necessary, are routed to execute against the **full displayed size** of any protected bid, in the case of a limit order to sell, or the **full displayed size** of any protected offer, in the case of a limit order to buy, for the NMS stock with a price that is **superior** to the limit price of the limit order identified as an ISO.
   - **Critical Compliance Requirement (Cross-Reference `17 CFR § 240.15c3-5(c)(2)(i)`)**: Broker-dealers granting customers permission to send ISO-marked orders must maintain pre-trade verification controls confirming that the simultaneous sweep orders were actually transmitted, and retain low-latency market data snapshot records (`SIP` or direct exchange feeds) proving the state of the NBBO at the exact microsecond of ISO generation.

3. **Benchmark / VWAP / Stopped Order Exceptions (`17 CFR § 242.611(b)(7)` & `(b)(9)`)**:
   - The transaction was the execution of an order at a price that was not based, directly or indirectly, on the quoted price of the NMS stock at the time of execution and for which the material terms were not reasonably determinable at the time the commitment to execute the order was made (e.g., qualified **Volume-Weighted Average Price (VWAP)** or **Time-Weighted Average Price (TWAP)** orders).

4. **Flickering Quotation Exception (`17 CFR § 242.611(b)(8)`)**:
   The trading center displaying the protected quotation that was traded through had displayed, within **one second** prior to the execution of the transaction that constituted the trade-through, a best bid or best offer, as applicable, for the NMS stock with a price that was equal or inferior to the price of the trade-through transaction.

## § 242.610 (Rule 610) Access to Quotations and Fee Caps

### § 242.610(c) Limitation on Access Fees
A trading center shall not impose, nor permit to be imposed, any fee or fees for the execution of an order against a protected quotation of the trading center or of any other trading center that exceed or accumulate to more than:
- **$0.0030 per share (30 mils)** for NMS stocks priced at **$1.00 or more** (note: subject to SEC 2024 Market Structure amendments reducing the access fee cap to **$0.0010 per share (10 mils)** for round-lot tick-constrained securities).
- **0.3% of the quotation price per share** if the price of a protected quotation is **less than $1.00**.

### § 242.610(d) Locking or Crossing Quotations
Each national securities exchange (including Nasdaq under `Nasdaq Equity 4, Rule 4756`) and national securities association shall establish, maintain, and enforce written rules that:
- Require its members reasonably to avoid displaying quotations that **lock** (bid equals another market's protected offer) or **cross** (bid exceeds another market's protected offer) any protected quotation in an NMS stock; and
- Prohibit its members from engaging in a pattern or practice of displaying quotations that lock or cross any protected quotation.

## § 242.612 (Rule 612) Minimum Pricing Increment ("Sub-Penny Rule")

### § 242.612(a) Prohibition on Sub-Penny Quotations for Stocks >= $1.00
No national securities exchange, national securities association, alternative trading system, vendor, or broker or dealer shall display, rank, or accept from any person a bid or offer, an order, or an indication of interest in any NMS stock priced in an increment **smaller than $0.01** (or updated $0.005 half-penny tick-constrained increment under 2024 SEC Rule 612 amendments) if that bid or offer, order, or indication of interest is priced equal to or greater than **$1.00 per share**.
- *Note*: Sub-penny **executions** resulting from midpoint peg orders (`Midpoint Peg` at $0.005 midpoint of an odd-cent NBBO spread) or retail price improvement programs that do not display or rank sub-penny limit orders are permissible.

### § 242.612(b) Sub-Dollar Stocks (< $1.00)
If the bid or offer, order, or indication of interest is priced **less than $1.00 per share**, the minimum pricing increment shall not be smaller than **$0.0001 per share**.

## § 242.613 (Rule 613) Consolidated Audit Trail (CAT) Reporting

Every national securities exchange (including Nasdaq) and FINRA member broker-dealer must record and report to the **Consolidated Audit Trail (CAT)** Central Repository by **8:00 a.m. Eastern Time on the trading day following the order event (`T+1 8:00 a.m. ET`)**:
- Every order origination, receipt, routing, modification, cancellation, and execution event (`MENO`, `MEOR`, `MEOA`, `MEOM`, `MEOC`, `MEOT`).
- **Clock Synchronization Requirement (`17 CFR § 242.613(d)`)**: Industry members must synchronize business clocks at a minimum to within **50 milliseconds** of the National Institute of Standards and Technology (NIST) atomic clock, and **100 microseconds** for electronic order-handling systems.
- **Customer Account & FDID Linkage**: Every order must include the Firm Designated ID (`FDID`) mapping to the Customer and Account Information System (`CAIS`).
