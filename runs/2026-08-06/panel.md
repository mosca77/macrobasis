# Weekly Indicator Panel — run 2026-08-06 (window 30 Jul → 6 Aug 2026)

Pulled per `MacroBasis_Indicator_Panel.md`. **Tier 1 rates and credit series lag one to three business days**, so several "6 Aug" cells are the latest published print, not same-day. Every such cell carries its actual as-of date. Where Tier 1 and Tier 2 disagree materially, both are shown rather than reconciled silently.

## Rates and policy pricing

| Indicator | Latest | 30 Jul | Change | Driver | Source |
|---|---|---|---|---|---|
| 2-year UST | 4.25% (3 Aug) | 4.23% | +2bp | Front end did NOT rally on the ADP miss | FRED H.15, T1 |
| 10-year UST | 4.63% (5 Aug) | 4.67% (29 Jul) | -4bp | Spiked to 4.75% on 31 Jul, an 18-month peak, then round-tripped on Hormuz de-escalation and the steady refunding | US Treasury par curve, T1 |
| 30-year UST | 5.17% (5 Aug) | 5.20% (29 Jul) | -3bp | Held near its highest since 2007 through the week | US Treasury par curve, T1 |
| 2s10s | 0.43 (4 Aug) | 0.45 | -2bp | Marginal flattening, not a growth signal | FRED, T1 |
| 10-year TIPS real yield | 2.41% (5 Aug) | 2.41% | flat | Peaked 2.47% on 31 Jul | US Treasury real curve, T1 |
| **10-year breakeven** | **2.22% (5 Aug)** | **2.26% (29 Jul)** | **-4bp** | The decisive read: inflation compensation came OUT while the real yield held | Computed from Treasury nominal minus real, T1 |
| 5y5y forward inflation | 2.26% (5 Aug) | 2.30% | -4bp | Same | FRED, T1 |
| SOFR | 3.66% (4 Aug) | 3.65% | +1bp | Flat | NY Fed, T1 |
| 30-year mortgage | 6.66% (30 Jul) | 6.58% (23 Jul) | +8bp w/w | **Stale** — the 6 Aug print had not released at pull time | Freddie Mac, T1 |
| Sept FOMC odds, **CME FedWatch** | 54.1% hike / 45.9% hold (5 Aug) | ~61.4% hike (30 Jul) | hike odds -7pp | Peaked ~82% on 23-27 Jul on the oil spike, then faded | CME, T2 read |
| Sept FOMC odds, **Polymarket** | 50.5% hold / 47.5% hike / ~1.7% cut (6 Aug) | ~45.5% hold / ~51.5% hike | hold +5pp | Same direction | Polymarket, T2 |
| Sept FOMC odds, **Kalshi** | 56.5% hike (5 Aug) | not verified | — | — | T2 |

**Adjudication of the source-file contradiction.** Three daily files carried three incompatible readings of September pricing. The 5 Aug file's claim of "~57% hold / ~43% cut, zero hike priced" is **wrong and is discarded**: no venue prices a meaningful cut, and a direct Investing.com Fed Rate Monitor pull returned 65.9% hike / 34.1% hold with no cut visible. The correct read is that September is close to a **coin flip between a hold and a hike, with a cut essentially unpriced**, and that hike conviction has cooled from roughly 82% at the pre-FOMC oil peak to the mid-50s. Separately, the "82.4% today" figure circulating in aggregator results is stale, traceable to 23-27 Jul, and must not be used. Prior anchor from the 30 Jul report was "roughly 55%", so on CME the number **held**.

## FX

| Indicator | Latest | 30 Jul | Change | Driver |
|---|---|---|---|---|
| DXY | ~99.7 (6 Aug), a seven-week low | 100.06 close | ~-0.4% | Joint intervention aftermath plus cooler hike odds |
| USD/JPY | 157.6 (5-6 Aug) | pre-intervention high 163.9 (late Jul) | yen +~4% from the low | Intervention low 155.20; 155 now treated as the floor |
| EUR/USD | 1.1555 (6 Aug) | 1.1529 | +0.2% | Softer dollar |
| USD/CAD | ~1.401 (6 Aug) | 1.4012 | flat | No Canadian repricing despite the tariff track |
| GBP/USD | 1.3468 (6 Aug) | 1.3463 | flat | — |

## Commodities

| Indicator | Latest (6 Aug) | 30 Jul | Change | Driver |
|---|---|---|---|---|
| **Brent** | **$79.10 close** | **$89.03 close** | **-11.2%** | Hormuz corridor deal in final drafting; bounced intraday above $80 on the Wafa strike then gave it back |
| **WTI** | **$75.15 close** | **$83.59 close** | **-10.1%** | Same |
| Gold | ~$4,252-4,280 | ~$4,071-4,082 | +4.2 to +5.0% | Biggest one-day gain since February on the ADP miss and falling real yields; seven-week high; +26% y/y |
| Silver | ~$62.20 | ~$58.0 | +7% | +61% y/y |
| Copper | $6.72/lb, at or near a record | ~$6.44/lb | +4.3% | Chile supply risk, thin LME on-warrant stock, tariff front-running, grid and AI demand |
| Henry Hub | ~$2.67-2.70 (5 Aug), a three-month low, per futures; FRED spot +6% to $2.81 (3 Aug) | $2.65 spot | **conflicted** | Record Lower-48 dry gas output ~110.7 Bcf/d; storage 3,084 Bcf, 6.4% above the five-year average |
| TTF | €53-55/MWh | ~€58 | ~-8% | Same de-escalation; EU storage 57.15% on 2 Aug, the lowest early-August reading on record, vs a relaxed 80% target |
| Uranium | $86.35/lb (5 Aug) | ~$86.30 | flat | — |
| Urea | $390/t (5 Aug) | ~$439 implied | ~-11%, **low confidence** | Not independently verified |

## Equities and factor rotation

| Indicator | Latest | 30 Jul | Change | Driver |
|---|---|---|---|---|
| S&P 500 | 7,723.55 (5 Aug), after a record 7,736.52 on 4 Aug | 7,437.63 | +3.8% | Hormuz de-escalation plus an 87% earnings beat rate |
| Nasdaq Composite | 26,705.30 (5 Aug) | 25,122.18 | +6.3% | AI-led early week, chip weakness late |
| Dow | 54,592.81 record (5 Aug), fifth straight winning session | 52,208.06 | +4.6% | Rotation into industrials and value |
| Russell 2000 (IWM proxy) | $299.77 (5 Aug) | $292.59 | +2.5% | Small caps participating |
| Equal weight vs cap weight | RSP +2.0% vs SPY +3.8% | — | cap weight led by 1.8pp | The rally is **narrower** than the index level implies |
| SOX / SOXX | SOXX $530.70 (5 Aug), in bear-market territory, >20% off its June high | — | — | Memory and AI-hardware dispersion |
| Single names inside semis | Nvidia +14.7% (5 Aug vs 29 Jul); Micron +18.8%; AMD -7 to -9% on a beat; SanDisk -10%; Western Digital -14.5% | — | — | Suppliers with pricing power rewarded, spenders punished |
| Nikkei 225 | 65,655 (6 Aug) | 61,867 | +6.1% | Yen intervention plus AI |
| KOSPI | 6,314 (6 Aug), -4.3% on the day | not verified | — | Late-week chip selloff, SK Hynix -5%, Samsung -8% |
| Euro Stoxx 50 | 6,491.80 (6 Aug), near a record | not verified | — | Records on de-escalation |
| TSX | 36,146 record (5 Aug) | not verified | — | Gold miners and Shopify +16.5% |
| Defence | Northrop +1.8% trailing month; Lockheed and RTX prints stale | — | — | **No defence conclusion this week** |
| Utilities and grid | Duke ~flat; NextEra unusable | — | — | Insufficient |

## Credit

| Indicator | Latest (4 Aug) | 30 Jul | Change | Note |
|---|---|---|---|---|
| ICE BofA US IG OAS | 0.78% | 0.80% | -2bp | Tightened |
| ICE BofA US HY OAS | 2.73% | 2.84% | -11bp | Tightened; historically tight |
| Oracle CDS-implied default risk | Record high, above its 2008 peak; 2046 bond 7.50%, 2056 bond 7.60% | — | rising | **The one place credit is stressed**, and it is AI-specific |
| Nvidia and Meta CDS | not verified this run | 82bp Nvidia (27 Jul), Meta 95bp claimed | — | Named gap |
| Leveraged loan index, new-issue reception | not verified | — | — | Named gap |

## Volatility, flows and crypto

| Indicator | Latest | 30 Jul | Change | Note |
|---|---|---|---|---|
| VIX | 16.50 (4 Aug), ~15.9 on 6 Aug | 17.09 | -0.6pt | Intraweek spike to 20.66 on 29 Jul, so the delta understates the round trip |
| OVX (oil vol) | 53.45 (4 Aug) | 63.44 | -16% | Still above 50 in absolute terms |
| MOVE | not verified | — | — | Named gap |
| Bitcoin | ~$64,500-64,800 | ~$65,300 (27 Jul, nearest print) | ~-1% | -44% y/y |
| Spot BTC ETF flows | +$626m net over 4-6 Aug, fourth consecutive weekly inflow | — | — | Institutional channel positive, price flat |
| Gold ETF flows | +$3bn in July, reversing two months of outflows; holdings +23t to 4,068t | — | — | WGC Goldhub, T1 |

---

## Claim-to-indicator sets

**1. Inflation expectations moderated.** Confirm: 10y breakeven -4bp [rates]; 5y5y forward -4bp [rates]; Brent -11.2% and WTI -10.1% [commodities]; TTF ~-8% [commodities]; urea ~-11% [commodities, low confidence]. Diverge: Henry Hub spot +6% on FRED against a three-month low on futures — a genuine spot-versus-futures conflict, carried not dropped; core PCE at 3.3% y/y and CPI expected 3.4-3.5% are **levels** far above the 2.22% market-implied rate, a level-versus-direction gap that belongs in the text. Null: ISM prices paid for July was 71.1 (3 Aug) and is a **diverging** confirm, still deep in inflationary territory. **Bar met: 5 confirms, 2 asset classes.**

**2. Growth was resilient, not softening.** Confirm: copper +4.3% to a record [commodities]; Russell 2000 +2.5% [equities]; S&P, Dow, Nasdaq, Nikkei, TSX, Euro Stoxx at or near records [equities]; HY OAS -11bp [credit]; VIX -0.6pt [volatility]; the 2-year yield ROSE 2bp, so the front end priced no growth scare [rates]; ISM manufacturing 55.6, a four-year high [survey]; initial claims 199,000, a third straight week below 200,000, four-week average lowest since September 2022 [labour]. Diverge: ADP +44,000 against ~70,000 expected, a six-month low, with June revised to 95,000; continuing claims +24,000 to 1.801m; Conference Board jobs-plentiful lowest since February 2021; Q2 GDP 1.5% annualised (pre-window print). **Bar met for resilient: 6 confirms, 4 asset classes. The bar is NOT met for softening — one weak market-priced indicator (2s10s -2bp) against six diverging ones.**

**3. Fiscal — the impulse is unchanged and its funding cost is what moves markets.** Confirm: Q3 borrowing estimate raised to $739B [primary]; TGA peak raised to ~$1.05T [primary]; 30-year at 5.17%, still near its highest since 2007 [rates, level]. **Diverge, and it is the week's cleanest one: the borrowing number went up $68B and the long end went DOWN 3bp**, with the breakeven falling 4bp and IG and HY both tightening. The market absorbed a bigger fiscal number without a concession. Null: auction tails and term-premium decomposition not pulled.

**4. Currency — dollar confidence weakened and the official sector is setting the yen's price.** Confirm: DXY at a seven-week low [FX]; USD/JPY roughly 4% off its 40-year low with the move authored by intervention, not the market [FX]; gold +4.2 to 5.0% to a seven-week high [commodities]; gold ETF inflows reversing two months of outflows [flows]. Diverge: bitcoin roughly flat and -44% y/y, so the speculative wing is not confirming [crypto]; the 10y breakeven fell, so the market is not expressing debasement through inflation compensation [rates]; the NY Fed funded its leg by selling **euros**, not dollars, which is the opposite of a dollar-weakening operation. **Bar met, with two named offsets.**

**5. Energy — the war premium deflated while the physical Gulf market stayed tight.** Confirm: Brent -11.2%, WTI -10.1% [commodities]; OVX -16% [volatility]. Confirm on the tightness leg: Gulf oil exports at ~36% of pre-conflict levels on a seven-day average, down from ~80% in early July [shipping data]; 84 tanker transits in the week to 2 Aug against a 130-140 per day pre-war baseline; 65 ships stranded in the Gulf on top of 70-plus since the conflict began; EU gas storage 57.15%, the lowest early-August reading on record. **Bar met on both legs. The gap between the two IS the theme's finding.**

**6. AI — the market punishes capex acceleration on beats and rewards capital-light AI.** Confirm: SpaceX -13.6% to an all-time low on a revenue beat with AI capex doubled to $15.8B; AMD -7 to -9% on a beat and raise; Western Digital -14.5% and SanDisk -10% on beats; Palantir +25-30% on a beat and raise; Caterpillar +11% [equities]; Oracle's CDS-implied default risk at a record [credit]. **Diverge, and it reframes the claim: Nvidia +14.7% and Micron +18.8%** — both hardware, both rallying. The honest formulation is therefore **not** capex-heavy versus capital-light but **buyer versus seller of the scarce input**: the market is paying for pricing power in supply and charging for the spend that funds it. Rewrite the claim to that form.

**7. Geopolitics — conflict risk stayed high but the tape priced de-escalation.** Confirm on the de-escalation leg: Brent -11.2% on dated Hormuz headlines [commodities]; equity records across the US, Japan, Canada, Europe and the UK [equities]; OVX -16% [volatility]; HY OAS -11bp [credit]. Confirm on the risk-stayed-high leg: OVX still above 50 in absolute terms; Gulf exports at ~36% of baseline. **Russia-Ukraine leg: NULL.** No equity, credit or FX move in the window is attributable to it, which corroborates the daily files. Rheinmetall's 6 Aug guidance cut is procurement-driven, from Germany's F126 frigate cancellation, and must **not** be coded as war transmission.

**8. Domestic — Canadian policy pressure is building without moving prices.** Confirm: USD/CAD flat at ~1.401 [FX]. Diverge: the TSX hit a record, though on gold miners and Shopify rather than anything domestic-policy driven. Null: Government of Canada versus US Treasury spread, BoC odds, Canadian bank equities, housing prints — none pulled.

**9. Illiquids — public markets at records against long rates near multi-decade highs.** Confirm on the public leg: S&P, Dow, Nasdaq, Nikkei, TSX, Euro Stoxx at or near records [equities, multi-geography]. Confirm on the rates leg: 30-year 5.17%, 10-year 4.63%, 30-year mortgage 6.66%, all elevated in **level** even though this week's deltas were slightly lower [rates]. **Both legs confirmed as levels. State the level-versus-direction nuance explicitly: the discount-rate pressure on unlisted assets is a level story, not a this-week-direction story.** Supporting primary evidence rather than tape: BDC non-accruals 0.8-3.8% at fair value, improving at three of four; the TCPC continuation vehicle priced at 95% of December book yet forcing a 10.4% NAV markdown.

---

## Divergence list (findings, not noise)

1. **Credit is not confirming the fiscal-stress narrative, and this week it actively contradicted it.** Borrowing guidance rose $68B; the 30-year fell 3bp, IG tightened 2bp and HY tightened 11bp. The mechanism is that Treasury held coupon sizes flat and pushed the increment into bills.
2. **Bitcoin is not confirming the debasement trade.** Gold +4.2 to 5.0% and DXY at a seven-week low, against bitcoin roughly flat and -44% y/y. Gold's institutional channel (ETF inflows reversing) is doing the work the speculative wing is not.
3. **The breakeven fell while the real yield held.** Inflation compensation came out of the curve without real growth expectations following it down. That is a growth-positive, inflation-negative combination, and it is the single most important number in this panel.
4. **Equities priced the removal of geopolitical risk, not the risk.** Records across six geographies in a week that included a Russian missile on NATO soil, 17 killed in Kyiv with zero of 24 missiles intercepted, and an Iranian threat to Gulf energy infrastructure.
5. **Nvidia and Micron rallied hard while AMD, SanDisk and Western Digital sold off on beats.** This breaks the simple "capex punished" framing and forces the buyer-versus-seller reformulation.
6. **Cap weight beat equal weight by 1.8pp.** The record is narrower than it looks.
7. **Henry Hub spot rose 6% on FRED while futures hit a three-month low.** Spot versus futures, stated rather than reconciled.
8. **Gold rose while oil fell.** Not a war-hedge move; it is the real-yield trade. Say so rather than letting the reader infer war fear.
9. **The soft ADP print was read as fewer hikes, not less growth.** Copper made a record and small caps rose the same week.

## Weekly Direction confirmation test

- **Inflation axis: bar MET** (≥3 confirms, ≥2 asset classes). 10y breakeven -4bp, 5y5y -4bp [rates]; Brent -11.2%, TTF ~-8% [commodities]. Direction: **moderating expectations against an elevated level**. Named tension: ISM prices paid 71.1 and core PCE 3.3% are levels that have not moved.
- **Growth axis: bar MET for RESILIENT, NOT met for softening.** Copper record, Russell +2.5%, six index records, HY -11bp, VIX lower, the 2-year not rallying. Six confirms across four asset classes. The single soft market-priced indicator is a 2bp flattening.
- **Consequence:** the growth sign flips from **-** to **+** and the quadrant moves from Stagflation to **Inflation**. The falsification test is the 7 August payrolls print, one day past the window.

## Not verified / named gaps

CME FedWatch and Kalshi live dashboards (JS-rendered); MOVE index; leveraged-loan index; new-issue reception; Nvidia and Meta CDS levels; DRAM and NAND contract prices; defence-sector index; Lockheed and RTX (stale prints); NextEra (stale); 30 Jul levels for TSX, KOSPI, Euro Stoxx and FTSE; ether at 30 Jul; equity fund flows; auction tails and term premium; Government of Canada versus Treasury spread; NCREIF ODCE queues; Green Street CPPI; Trepp CMBS delinquency (403). **All Tier 1 rates and credit prints are dated 3-5 August, not 6 August.**
