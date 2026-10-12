---
doc_id: "SEC-15C3-5"
title: "SEC Rule 15c3-5: Risk Management Controls for Brokers or Dealers with Market Access"
jurisdiction: "SEC"
citation_prefix: "17 CFR § 240.15c3-5"
effective_date: "2011-07-14"
last_amended: "2024-03-15"
category: "Market Access & Pre-Trade Risk Controls"
---

# 17 CFR § 240.15c3-5 — Risk Management Controls for Brokers or Dealers with Market Access

## § 240.15c3-5(a) Definitions

For the purposes of this section:

1. **Market Access** (`17 CFR § 240.15c3-5(a)(1)`): The term *market access* shall mean:
   - (i) Access to trading in securities on an exchange or alternative trading system (ATS) as a result of being a member or subscriber of the exchange or alternative trading system, respectively; or
   - (ii) Access to trading in securities on an alternative trading system provided by a broker-dealer operator of an alternative trading system to a non-broker-dealer.

2. **Regulatory Requirements** (`17 CFR § 240.15c3-5(a)(2)`): The term *regulatory requirements* shall mean all federal securities laws, rules and regulations of the Securities and Exchange Commission (SEC), and rules of self-regulatory organizations (SROs) including Nasdaq Stock Market LLC and FINRA, that are applicable in connection with market access.

## § 240.15c3-5(b) General Requirement for Risk Management Controls and Supervisory Procedures

A broker or dealer with market access, or that provides a customer or any other person with access to trading securities through use of its market participant identifier (MPID) or otherwise, shall establish, document, and maintain a system of risk management controls and supervisory procedures reasonably designed to manage the financial, regulatory, and other risks of this business activity.

- **Prohibition on Unfiltered or "Naked" Sponsored Access**: Any arrangement where a customer routes orders directly to an exchange (such as Nasdaq) or ATS using the broker-dealer's MPID without passing through pre-trade risk management controls administered prior to order entry is strictly prohibited under `17 CFR § 240.15c3-5(b)` and `17 CFR § 240.15c3-5(c)`.
- Cross-references: `17 CFR § 242.611`, `Nasdaq Rule 4611`, `17 CFR § 242.200`.

## § 240.15c3-5(c) Elements of Risk Management Controls and Supervisory Procedures

The risk management controls and supervisory procedures required by paragraph (b) of this section shall include the following elements:

### § 240.15c3-5(c)(1) Financial Risk Management Controls

The risk management controls and supervisory procedures shall be reasonably designed to systematically limit the financial exposure of the broker or dealer that could arise as a result of market access, including being reasonably designed to:

1. **Pre-Trade Credit and Capital Thresholds (`17 CFR § 240.15c3-5(c)(1)(i)`)**:
   Prevent the entry of orders that exceed appropriate pre-set credit or capital thresholds in the aggregate for each customer and the broker or dealer and, where appropriate, more finely-tuned by sector, security, or otherwise, by rejecting orders if such orders would exceed the applicable credit or capital thresholds.
   - Controls MUST be applied **pre-trade** (before the order reaches the exchange matching engine). Post-trade alerts or end-of-day reconciliations alone are **non-compliant**.
   - Credit thresholds must account for both open unexecuted orders on the order book and executed positions.

2. **Erroneous Order & Price/Size Collar Controls (`17 CFR § 240.15c3-5(c)(1)(ii)`)**:
   Prevent the entry of erroneous orders, by rejecting orders that exceed appropriate price or size parameters, on an order-by-order basis or over a short period of time, or that indicate duplicative orders.
   - Mandatory controls include:
     - **Maximum Single Order Notional Value Limit** (e.g., hard block on orders exceeding pre-set notional dollar limits).
     - **Maximum Single Order Share Quantity Limit** ("fat-finger" quantity check).
     - **Price Reasonableness / Collar Check**: Rejecting limit orders priced more than a specified percentage (e.g., 5% to 10% depending on price tier and Limit Up-Limit Down (LULD) bands) away from the National Best Bid and Offer (NBBO) or last sale price.
     - **Duplicate Order / Message Rate Throttling**: Blocking runaway algorithmic loops that submit rapid, identical orders within millisecond windows.

### § 240.15c3-5(c)(2) Regulatory Risk Management Controls

The risk management controls and supervisory procedures shall be reasonably designed to ensure compliance with all regulatory requirements, including being reasonably designed to:

1. **Pre-Order Regulatory Requirements (`17 CFR § 240.15c3-5(c)(2)(i)`)**:
   Prevent the entry of orders unless there has been compliance with all regulatory requirements that must be satisfied on a pre-order entry basis, including:
   - Compliance with **Regulation SHO (`17 CFR § 242.200` and `17 CFR § 242.203`)** order marking (`LONG`, `SHORT`, `SHORT EXEMPT`) and locate verification prior to short sale order submission.
   - Compliance with **Regulation NMS (`17 CFR § 242.611`)** requirements for Intermarket Sweep Orders (ISOs), ensuring that when a broker-dealer marks an order as an ISO, simultaneous routings are sent to execute against all protected quotations with a superior price.
   - Trading halt and Limit Up-Limit Down (LULD) pause blocks pursuant to `Nasdaq Rule 4120`.

2. **Restricted Securities & Wash Sale Prevention (`17 CFR § 240.15c3-5(c)(2)(ii)`)**:
   Prevent the entry of orders for securities that the broker or dealer, customer, or other person, as applicable, is restricted from trading (e.g., Restricted List securities, Regulation SHO Rule 201 circuit breaker short sale price test restrictions, or self-trade/wash-trade prevention).

3. **Surveillance Personnel Access (`17 CFR § 240.15c3-5(c)(2)(iii)`)**:
   Restrict access to trading systems and technology that provide market access to persons and accounts pre-approved and authorized by the broker or dealer.

4. **Immediate Post-Trade Surveillance Reporting (`17 CFR § 240.15c3-5(c)(2)(iv)`)**:
   Assure that appropriate surveillance personnel receive immediate post-trade execution reports resulting from market access, including position data, potential manipulation flags (spoofing, layering, marking the close), and credit utilization metrics.

## § 240.15c3-5(d) Direct and Exclusive Control of Risk Management Controls

The financial and regulatory risk management controls and supervisory procedures described in paragraph (c) of this section shall be under the **direct and exclusive control** of the broker or dealer that is subject to paragraph (b) of this section.

1. **Prohibition on Third-Party or Customer Control (`17 CFR § 240.15c3-5(d)(1)`)**:
   A broker-dealer may NOT delegate control of pre-trade risk parameters to a customer, hedge fund client, or non-broker-dealer affiliate. If the customer can modify, bypass, or disable credit limits or erroneous order checks without broker-dealer intervention, the system is in direct violation of `17 CFR § 240.15c3-5(d)`.

2. **Permissible Allocation to Another Registered Broker-Dealer (`17 CFR § 240.15c3-5(d)(2)`)**:
   A broker or dealer that provides market access may reasonably allocate, by written contract,after a thorough due diligence review, control over specific regulatory risk management controls under `§ 240.15c3-5(c)(2)` to a customer that is a **registered broker or dealer**, provided that the allocating broker-dealer has a reasonable basis for determining that such customer, based on its position in the transaction and relationship with an ultimate customer, has better access to that ultimate customer and its trading information such that it can more effectively implement the specified controls.

## § 240.15c3-5(e) Regular Review of Risk Management Controls and CEO Certification

A broker or dealer that is subject to paragraph (b) of this section shall establish, document, and maintain a system for regularly reviewing the effectiveness of the risk management controls and supervisory procedures required by paragraphs (b) and (c) of this section and for promptly addressing any issues.

1. **Annual Review Requirement (`17 CFR § 240.15c3-5(e)(1)`)**:
   The broker or dealer shall review, **no less frequently than annually**, the business activity of the broker or dealer in connection with market access to assure the overall effectiveness of such risk management controls and supervisory procedures. Such review shall be conducted in accordance with written procedures and shall be documented.

2. **Annual Chief Executive Officer (CEO) Certification (`17 CFR § 240.15c3-5(e)(2)`)**:
   The Chief Executive Officer (or equivalent officer) of the broker or dealer shall, on an **annual basis**, certify that such risk management controls and supervisory procedures comply with paragraphs (b) and (c) of this section, and that the broker or dealer conducted the regular review described in paragraph (e)(1) of this section.
   - Record Retention: All written procedures, review documentation, and CEO certifications must be preserved in accordance with `17 CFR § 240.17a-4(b)` for a period of not less than **three years**, the first two years in an easily accessible place.
