---
doc_id: "SEC-REG-SHO"
title: "SEC Regulation SHO (17 CFR §§ 242.200–204): Regulation of Short Sales, Locate & Close-Out Requirements"
jurisdiction: "SEC"
citation_prefix: "17 CFR § 242.200"
effective_date: "2005-01-03"
last_amended: "2024-05-28"
category: "Short Selling, Clearing & Settlement"
---

# SEC Regulation SHO (17 CFR §§ 242.200–204) — Regulation of Short Sales

## § 242.200 (Rule 200) Definition of "Short Sale" and Order Marking Requirements

### § 242.200(a) Definition of Short Sale
The term *short sale* shall mean any sale of a security which the seller does not own or any sale which is consummated by the delivery of a security borrowed by, or for the account of, the seller.

### § 242.200(g) Order Marking Requirements (`LONG`, `SHORT`, `SHORT EXEMPT`)
A broker or dealer must mark all sell orders of any equity security as **"long"**, **"short"**, or **"short exempt"**.

1. **When an Order May Be Marked "Long" (`17 CFR § 242.200(g)(1)`)**:
   A sell order may be marked `"long"` **only if**:
   - (i) The seller is deemed to own the security being sold pursuant to paragraphs (a) through (f) of `17 CFR § 242.200` (net long across all accounts of the legal entity after aggregation under `Rule 200(f)`); and
   - (ii) Either: (a) the security to be delivered is in the physical possession or control of the broker or dealer; or (b) it is reasonably expected that the security will be in the physical possession or control of the broker or dealer no later than the settlement of the transaction (`T+1`).
   - **Violation Warning**: Marking a sell order as `"long"` when the seller has an unexercised option, convertible bond not yet tendered, or holds a net short position across aggregated aggregation units violates `17 CFR § 242.200(g)(1)` and `17 CFR § 240.15c3-5(c)(2)(i)`.

2. **When an Order May Be Marked "Short Exempt" (`17 CFR § 242.200(g)(2)`)**:
   A sell order may be marked `"short exempt"` only if the provisions of `17 CFR § 242.201(c)` (Broker-Dealer Provision for Short Sale Price Test above the National Best Bid) or `17 CFR § 242.201(d)` (Exemptions for Riskless Principal, Odd-Lot, Domestic/International Arbitrage, or Volume-Weighted Average Price (VWAP)) are satisfied.

## § 242.201 (Rule 201) Circuit Breaker / Alternative Uptick Rule

### § 242.201(b) Short Sale Price Test Restriction Trigger (`10% Intraday Decline`)
1. **Trigger Threshold (`17 CFR § 242.201(b)(1)(i)`)**:
   If the price of a covered security decreases by **10% or more** from the covered security's closing price as determined by the listing market (e.g., Nasdaq Stock Market LLC) as of the end of regular trading hours on the prior day, the Short Sale Price Test Restriction (also known as the **Alternative Uptick Rule** or **SSR**) is immediately triggered.
2. **Duration of Restriction (`17 CFR § 242.201(b)(1)(ii)`)**:
   Once triggered, the short sale price restriction remains in effect for the **remainder of the trading day** on which it is triggered **and the entire following trading day**.
3. **Price Execution Restriction (`17 CFR § 242.201(b)(1)`)**:
   While the Rule 201 circuit breaker is in effect, no trading center (including Nasdaq, ATSs, and broker-dealer internalizers) may execute or display a short sale order (unless marked `"short exempt"`) at a price that is **less than or equal to the current National Best Bid (NBB)**. All short sale orders must be priced at least one minimum pricing increment above the current NBB.

## § 242.203 (Rule 203) Borrowing and Delivery Requirements ("Locate" Rule)

### § 242.203(b)(1) Pre-Trade Locate Requirement
A broker or dealer may **not** accept a short sale order in an equity security from another person, or effect a short sale in an equity security for its own account, unless the broker or dealer has:
- (i) **Borrowed** the security, or entered into a bona-fide arrangement to borrow the security; or
- (ii) **Reasonable grounds to believe** that the security can be borrowed so that it can be delivered on the date delivery is due (`T+1` under `17 CFR § 240.15c6-1`); and
- (iii) **Documented compliance** with this paragraph `17 CFR § 242.203(b)(1)` **prior to** effecting the short sale (including timestamp, locate source ID, and quantity located).
- **"Easy-to-Borrow" (ETB) List Requirements**: An Easy-to-Borrow list may provide reasonable grounds only if it is less than **24 hours old** and derived from verified, current inventory sources. Repeated fails-to-deliver in a security on an ETB list invalidate reliance on that list.

### § 242.203(b)(2) Exceptions to the Locate Requirement
The pre-trade locate requirement of `17 CFR § 242.203(b)(1)` shall not apply to:
- (i) A broker or dealer that has accepted a short sale order from another registered broker or dealer that is required to comply with `Rule 203(b)(1)` (unless the executing broker-dealer contractually assumed responsibility);
- (iii) **Bona-Fide Market Making Exception (`17 CFR § 242.203(b)(2)(iii)`)**: Short sales effected by a market maker in connection with **bona-fide market making activities** in the security for which this exception is claimed.
  - *Strict Limitation*: Speculative proprietary trading, directional hedge strategies, or trading where a market maker does not continuously post two-sided quotes near the NBBO does **NOT** qualify as bona-fide market making under `Rule 203(b)(2)(iii)`.

### § 242.203(c)(6) Threshold Securities Definition
A **Threshold Security** means any equity security of a reporting issuer for which there is an aggregate fail-to-deliver position for **five consecutive settlement days** at a registered clearing agency (NSCC/DTCC) totaling:
- **10,000 shares or more**, AND
- Equal to at least **0.5% (one-half of one percent)** of the issuer's total shares outstanding.
Lists of Threshold Securities are published daily by SROs including **Nasdaq** pursuant to `Nasdaq Equity Rule 4620` and `17 CFR § 242.203(c)(6)`.

## § 242.204 (Rule 204) Close-Out Requirement for Fails-to-Deliver

Under the `T+1` standard settlement cycle (`17 CFR § 240.15c6-1`, effective May 28, 2024):

1. **Short Sale Fail-to-Deliver Close-Out (`17 CFR § 242.204(a)`)**:
   A participant of a registered clearing agency (e.g., NSCC) must deliver securities to a registered clearing agency for clearance and settlement on a long or short sale in any equity security by settlement date (`T+1`). If a participant has a fail-to-deliver position at a registered clearing agency resulting from a **short sale**, the participant shall, by **no later than the beginning of regular trading hours on the settlement day following the settlement date (`T+2`, i.e., `S+1`)**, immediately close out the fail-to-deliver position by borrowing or purchasing securities of like kind and quantity.

2. **Long Sale or Bona-Fide Market Making Fail-to-Deliver Close-Out (`17 CFR § 242.204(a)(1)` & `(a)(3)`)**:
   If a participant has a fail-to-deliver position at a registered clearing agency that can be demonstrated on its books and records to have resulted from a **long sale** (`Rule 204(a)(1)`) or is attributable to **bona-fide market making activities** (`Rule 204(a)(3)`), the participant shall close out the fail-to-deliver position by purchasing or borrowing securities by **no later than the beginning of regular trading hours on the third consecutive settlement day following the settlement date (`T+4`, i.e., `S+3`)**.

3. **Penalty Box / Pre-Borrow Restriction (`17 CFR § 242.204(b)`)**:
   If a clearing participant fails to close out a fail-to-deliver position within the mandatory deadline (`T+2` for short sales, `T+4` for long sales / bona-fide market making), the participant and any broker-dealer from which it receives trades for clearance and settlement may **not** accept a short sale order from any person or effect a short sale in that equity security for its own account without **first borrowing the security or entering into a bona-fide arrangement to borrow the security** (the **"Penalty Box" Pre-Borrow Requirement**) until the fail-to-deliver position is closed out and that purchase has cleared and settled.
