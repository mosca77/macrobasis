# MacroBasis Weekly Indicator Panel — the market-confirmation layer

**Purpose.** News tells you what happened; the tape tells you whether markets believe it. Every weekly run pulls this panel and uses it two ways: the **generator** (Run Prompt, Phase 3) drafts claims only with their confirming indicators attached, and the **evaluator** (Phase 7) audits that every macro claim in the report is confirmed, contradicted-and-explained, or flagged. A claim like "markets are pricing moderating inflation" is never carried by one asset: gold, yes, but also breakevens, ISM prices paid, oil, fertilizer, the front end, and the dollar. The panel is the checklist that makes that reflex systematic.

---

## A. The Weekly Panel (pull EVERY run: level, weekly change, driver)

| Bucket | Indicators (core) | What it reads on |
|---|---|---|
| **Rates & policy pricing** | 2-year UST; 10-year UST; 2s10s slope; 10-year TIPS real yield; 10-year breakeven (5y5y when findable); Fed hike/cut odds into the next 2 meetings | Policy pricing, growth expectations, **market-implied inflation** (the cleanest inflation-expectations gauge; compare breakevens to spot CPI/PCE to separate level from direction) |
| **FX** | DXY; USD/JPY; EUR/USD; USD/CAD | Dollar prop (rates vs reserve behaviour), carry stress, Canada read |
| **Commodities** | WTI & Brent (+ curve shape when notable); gold; copper; natural gas (EU TTF when Europe is in the story); urea/fertilizer complex | War/supply premium, disinflation impulse, **global growth (copper)**, debasement bid, food-channel inflation |
| **Equities & factors** | S&P 500, Nasdaq-100, Dow, TSX; and the factor reads: semis (SOX), memory/storage names, hyperscalers, defence (SXPARO, US primes), utilities/grid, cyclicals vs defensives, small caps | Risk appetite, AI-theme internals (rotation = who holds pricing power), defence-fiscal confirmation, growth breadth |
| **Credit** | IG OAS; HY OAS; the week's big new-issue receptions (oversubscription, concession) | Financing stress: the first place an AI-capex or fiscal-supply problem shows up |
| **Volatility** | VIX (MOVE when rates are the story) | Whether the market is trading the news as shock or as repricing |
| **Flows & crypto** | Notable ETF flows (GRID, ICLN/IXC, defence, gold ETFs), fund-flow stories, bitcoin | Positioning: where capital is actually voting; the speculative wing of debasement |

Slow-moving structural gauges stay on their release cadence, not weekly: COFER (quarterly), TIC (monthly), WGC gold purchases, term premium estimates, auction tails/bid-to-cover as auctions occur.

## B. Regime-axis confirmation sets (the Weekly Direction test)

The Weekly Direction is a two-axis call (inflation up/down, growth faster/slower). Each side of the call must clear the Evaluator's minimum (≥3 confirming indicators from ≥2 asset classes; the Evaluator owns that threshold), and divergences must be named. The sets below say WHICH indicators speak to which axis:

- **Inflation direction:** 10y breakeven and 5y5y (anchored vs drifting); ISM/PMI prices-paid; oil and natgas; fertilizer/food complex; wage growth (AHE); gold (rates-sensitive part); the prints themselves (CPI/PCE, euro flash); import prices. *Distinguish LEVEL (spot prints) from DIRECTION (market-implied): both belong in the text when they disagree.*
- **Growth direction:** payrolls/claims/JOLTS as a set (hiring vs firing); ISM/PMIs (US, China, euro); copper; 2s10s and the front end; cyclicals vs defensives, small caps; earnings-revision tone; Canada monthly GDP/LFS for the domestic read.
- **Policy pricing:** 2-year; meeting-dated odds; real yields; DXY; central-bank rhetoric against what the curve did.

## C. Theme confirmation map (what "the market agrees" looks like per theme)

| Theme | Primary market gauges | MORE of the theme looks like |
|---|---|---|
| **1 Fiscal & Dereg** | Defence stocks (SXPARO, primes); sovereign yields/term premium; auction demand; bank stocks (dereg); infrastructure names | Defence outperformance, term premium creep, heavier issuance absorbed |
| **Monetary (appendix)** | Front end, breakevens, real yields, meeting odds; cross-CB spreads (UST-JGB, UST-GoC) | Curve repricing around data/speakers; divergence trades widening or closing |
| **2 Currency Debasement** | Gold (and silver); DXY; USD/JPY; bitcoin; real yields; auction tails; (slow: COFER, TIC, CB gold buying) | Gold up with dollar down **for reserve/fiscal reasons, not just rate moves**; weak auctions; foreign selling |
| **3 Energy & Transition** | GRID/ICLN/IXC levels AND flows; utilities/grid equipment names; copper; natgas; uranium; PPA/curtailment datapoints | Grid-enabler outperformance and inflows; tightening power markets |
| **4 AI** | SOX/semis vs hyperscalers (rotation tells you which layer holds pricing power); memory contract prices; AI credit (new-issue reception, spreads on AI issuers); data-centre REITs; copper | Raises oversubscribed, memory prices firm, enablers outperforming; stress = spreads widening, deals repricing |
| **5 Geopolitics & Trade** | Oil level and curve; tanker/freight rates; gold war-bid; defence stocks; FX of exposed economies (CAD, MXN, EUR); fertilizer/sulphur; tariff-exposed sectors (autos, steel) | War premium rebuilding, freight spiking, exposed-FX weakening on trade headlines |
| **6 Domestic (Canada)** | USD/CAD; TSX vs S&P relative; GoC-UST spread; BoC odds; Canadian banks; housing prints | CAD and relative TSX moves on policy/trade news; domestic-sector bid |

## D. Claim→indicator protocol (generator discipline)

For **every** market-direction claim you intend to write (the Weekly Direction, each Status line, each keydev):
1. Enumerate its confirming set from B/C, aiming for the full set. The binding minimums live in the Evaluator and differ by claim type: each Weekly Direction axis needs ≥3 confirming indicators from ≥2 asset classes; a theme's 🟢/🔴 light needs at least one market-price confirmation (plus its news score); keydev and body claims carry whatever confirmations exist, with divergences named.
2. Check each in-window: **confirm / diverge / null (not checkable this week)**.
3. Confirmations get woven into the text as the cross-asset thread ("the 2-year fell, the dollar slipped, gold reclaimed $4,000").
4. **Divergences are findings, not noise**: either explain them in the text (e.g., "JOLTS at a two-year high argues stall, not break") or send them to triage. An unexplained divergence must never be silently dropped.
5. Nulls are recorded in triage as checked-null.

## E. How to pull it (query patterns)

Prefer data pages over headlines: FRED (breakevens T10YIE, real yields, HY OAS BAMLH0A0HYM2, VIX VIXCLS), Trading Economics (commodities, DXY, currencies), exchange/index pages, fund pages for AUM/flows. Patterns: "<indicator> level <date/week>", "<indicator> weekly change <month year>", "10-year breakeven inflation rate <month year>", "high yield OAS spread <month year>", "copper price <date>", "VIX <date>", "USD CAD <date>", "<ETF> assets flows <month year>". Every value lands with its as-of date and carries prior/trend context into the text (no standalone numbers).

---

## F. Worked example — week of 2 July 2026 (the payrolls-repricing week)

Panel pulled: 2y 4.108% (-5bp on the jobs miss); 10y ~4.47% (little changed); **10y breakeven 2.21-2.22% and 10y real yield ~2.2%** (market-implied inflation anchored while spot PCE runs 4.1%: direction vs level in one line); DXY 101.6 15-month high Wednesday → ~100.75 after payrolls; USD/JPY ~160 (no intervention); **USD/CAD 1.4216, CAD's one-year low**; WTI $67.59 (lowest since late Feb), Brent $70.60; gold $4,018 → $4,135 intraday ($4,079 futures); **copper ~$6.10/lb (~$13,400/t), easing off May's ~$14,800/t record**; urea $368/t (-21% m/m); S&P +1.2% Monday and +0.3% Thursday with the **Dow above 52,000 for the first time**; Nasdaq-100 +2% Monday with rotation into memory/storage; **VIX 16.59** (calm); **IG OAS ~80bp (multi-decade tights), HY ~280-285bp (17th percentile, drifting wider)**; new-issue reception strong (SKHY +5.5% on pricing, SpaceX 3.5x covered last week); GRID $11.2B AUM on $3.1B YTD inflows; bitcoin ~$58,500 (-18% June).

Confirmation read: **moderating inflation** confirmed by breakevens ≤2.2%, ISM prices paid -9.1pts, oil and urea falling, euro flash 2.8% (5 indicators, 4 asset classes); offset named: spot PCE 4.1%, DRAM +51-89%. **Slower growth** confirmed by payrolls/revisions/participation, copper off its record, CAD at a one-year low; tension named: JOLTS 7.6M, claims 215K, ISM 53.3 still expanding, VIX 16.6 and credit at tights (stall, not break). **Policy** confirmed by the 2-year, hike odds leaving the curve, and the dollar giving back its high. Divergences worth carrying forward: HY drifting wider off tights while IG sits at extremes (early financing-stress watch against the AI supply calendar), and gold's monthly drawdown against its weekly pop (rates-driven, not structural).
