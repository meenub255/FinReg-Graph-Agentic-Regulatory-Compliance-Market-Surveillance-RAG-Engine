---
doc_id: "FINRA-NASDAQ-SUPERVISION"
title: "FINRA Rules 3110, 3310, 5310 & Nasdaq Equity 9: Algorithmic Trading Supervision, Best Execution & AML Compliance"
jurisdiction: "FINRA_NASDAQ"
citation_prefix: "FINRA Rule"
effective_date: "2014-12-01"
last_amended: "2024-11-01"
category: "Algorithmic Trading Supervision, Best Execution & Anti-Money Laundering"
---

# FINRA Rules 3110, 3310, 5310 & Nasdaq Equity 9 — Algorithmic Supervision, Best Execution & AML

## FINRA Rule 3110 & Regulatory Notice 15-09 — Supervision of Algorithmic Trading Strategies

### Supervisory System & Written Supervisory Procedures (`FINRA Rule 3110(a)` & `(b)` / `Nasdaq General 9, Section 20`)
Each member firm must establish and maintain a system to supervise the activities of each associated person (including quantitative developers and algorithmic traders) that is reasonably designed to achieve compliance with applicable securities laws and regulations, and with applicable FINRA and **Nasdaq** rules.

1. **Pre-Deployment Testing & SDLC Governance (`FINRA RN 15-09` & `17 CFR § 240.15c3-5(c)`)**:
   Before deploying a new algorithmic trading strategy or a material code modification to production on Nasdaq or other exchanges, the member firm must:
   - Conduct rigorous **sandbox/simulation testing** under stressed market conditions (high volatility, widened spreads, LULD halts, and message bursts);
   - Verify that hard-coded or configurable **kill-switches**, **maximum order rate throttles**, and **fat-finger notional collars** (`17 CFR § 240.15c3-5(c)(1)(ii)`) are independent of the trading strategy logic itself;
   - Maintain an independent **Change Management Sign-Off** by Compliance, Risk Management, and Technology Supervision prior to production release.

2. **Associated Person Registration — Securities Traders (`FINRA Rule 1220(b)(4)` / `Series 57`)**:
   Each person associated with a member who is primarily responsible for the **design, development, or significant modification of an algorithmic trading strategy** relating to equity, preferred, or convertible debt securities, or who is responsible for the day-to-day supervision or direction of such activities, must register as a **Securities Trader (`Series 57`)**.

3. **Emergency Kill-Switch & Disconnection Controls**:
   Firms must maintain an automated and manual **"Kill-Switch"** capability able to immediately:
   - (i) Disable a malfunctioning algorithm or specific MPID/port; AND
   - (ii) **Mass-cancel all open, unexecuted resting orders** on Nasdaq (`OUCH` / `FIX` Cancel-On-Disconnect or Mass Cancel ports) and other trading venues.

## FINRA Rule 5310 — Best Execution and Interpositioning

### FINRA Rule 5310(a)(1) Reasonable Diligence for Best Execution
In any transaction for or with a customer or a customer of another broker-dealer, a member and persons associated with a member shall use **reasonable diligence** to ascertain the best market for the subject security, and buy or sell in such market so that the resultant price to the customer is as favorable as possible under prevailing market conditions.

1. **Factors Determining Reasonable Diligence (`FINRA Rule 5310(a)(1)(A)–(E)`)**:
   - (A) The character of the market for the security (e.g., price, volatility, relative liquidity, and pressure on available communications);
   - (B) The size and type of transaction;
   - (C) The number of markets checked;
   - (D) Accessibility of the quotation; and
   - (E) The terms and conditions of the order which result in the transaction.

2. **Regular and Rigorous Review of Execution Quality (`FINRA Rule 5310 Supplementary Material .09`)**:
   - A member that routes customer orders to other broker-dealers, market makers, or exchanges (including **Nasdaq**, NYSE, or wholesale internalizers) for execution on an automated, non-directed basis must conduct a **"regular and rigorous review"** of execution quality **at least quarterly** (and more frequently, such as monthly, where market conditions or routing changes warrant).
   - **Payment for Order Flow (PFOF) & Exchange Rebate Conflicts**: A member may **not** allow routing inducements, maker-taker rebates, or Payment for Order Flow (`PFOF`) to interfere with its duty of best execution (`FINRA Rule 5310.09(b)`). The review must compare price improvement, effective-over-quoted spread (`E/Q`), fill rates, and speed of execution across competing venues including Nasdaq.

## FINRA Rule 3310 — Anti-Money Laundering (AML) Compliance Program

### Mandatory Four Pillars + FinCEN CDD Rule (`FINRA Rule 3310(a)–(f)` & `31 CFR § 1023.210`)
Each member firm shall develop and implement a written **Anti-Money Laundering (AML) Program** reasonably designed to achieve and monitor the member's compliance with the requirements of the **Bank Secrecy Act (`31 U.S.C. 5311 et seq.`)** and the implementing regulations promulgated thereunder by the Department of the Treasury:

1. **Internal Policies, Procedures, and Controls (`FINRA Rule 3310(a)`)**:
   Policies reasonably designed to detect and cause the reporting of suspicious transactions under `31 U.S.C. 5318(g)`:
   - **Suspicious Activity Report (`SAR`) Filing Threshold (`31 CFR § 1023.320`)**: A broker-dealer must file a **SAR (`FinCEN Form 111`)** for any suspicious transaction (or pattern of transactions) conducted or attempted by, at, or through the broker-dealer involving or aggregating at least **$5,000 in funds or other assets** where the broker-dealer knows, suspects, or has reason to suspect illegal activity, money laundering, market manipulation (pump-and-dump, microcap wash trading, spoofing), or BSA evasion.
   - **SAR Filing Deadline**: Must be filed within **30 calendar days** after the date of initial detection by the broker-dealer of facts that may constitute a basis for filing a SAR (extended to 60 calendar days only if no suspect is identified on the date of detection).

2. **Independent AML Testing (`FINRA Rule 3310(c)`)**:
   Provide for **annual (on a calendar-year basis) independent testing** for compliance to be conducted by member personnel or by a qualified outside party, unless the member does not execute transactions for customers or otherwise hold customer accounts or act as an introducing broker with respect to customer accounts, in which case such "independent testing" is required **every two years** (on a calendar-year basis).

3. **Customer Due Diligence (CDD) & Beneficial Ownership (`FINRA Rule 3310(f)` / `31 CFR § 1010.230`)**:
   Identify and verify the identity of **beneficial owners** of legal entity customers owning **25% or more** of the equity interests of the legal entity, plus one individual with significant responsibility to control, manage, or direct the legal entity customer.
