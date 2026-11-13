# Holiday Gift Card email (Nov–Dec 2026)

Template: `holiday-gift-card-2026.html` (Constant Contact → Create → Email → **Custom Code**).
Images: `images/email/holiday-2026/` — live at `https://guacmexigrill.ca/images/email/holiday-2026/`
once this branch is merged and deployed. **Merge before sending a test**, or images will break.

## Offer (from the creative)
Buy a gift card valued at $25+ **in-store**, receive a free burrito. Valid through Dec 26, 2026.
Online gift card purchases do not qualify, so every CTA goes to Locations, not online checkout.

## Subject lines (A/B test the first two)
| | Subject | Preheader |
|---|---|---|
| A | Gift bold. Get a free burrito. 🎁 | Buy a $25+ GUAC gift card in-store and we'll hand you a free burrito. |
| B | One for them, one for you 🌯 | Every $25+ gift card comes with a free burrito, through Dec 26. |
| C | The easiest gift on your list | Never expires. Activated on the spot. Plus a free burrito for you. |
| Reminder (Dec 19–22) | Last call: your free burrito ends Dec 26 | There's still time. Gift cards are activated at the register. |

The preheader is hard-coded at the top of the HTML; update it to match the subject you send.

## Email flow
1. Hero: "GIFT BOLD." headline (live text) + creative photo, text removed so it reads on phones
2. Offer + primary CTA: Find Your Nearest GUAC
3. How it works (3 steps)
4. Gift guide: $25 / $50 / $100 tiers (anchors higher card values; all qualify)
5. Card benefits: never expires, $10–$500, coast to coast
6. "And one for you": the burrito as the buyer's reward
7. Urgency band (ends Dec 26) + second CTA
8. Footer + fine print. Constant Contact adds the address and unsubscribe block automatically.

## Tracking
All guacmexigrill.ca links carry
`utm_source=constant_contact&utm_medium=email&utm_campaign=holiday_giftcard_2026&utm_content=<slot>`
(`hero_image`, `primary_cta`, `gift_guide`, `urgency_cta`, `footer_*`), so GA shows which slot
drove the click. If Constant Contact's own UTM tagging is turned on, turn it off for this email
to avoid duplicate parameters.

## Before sending
- [ ] Confirm burrito redemption mechanics (on the spot vs. coupon) and update step 03 if needed
- [ ] Confirm all open locations participate (closed locations are flagged on /locations)
- [ ] Send tests to Gmail (web + app), Outlook desktop, and iPhone Mail
- [ ] Segment: exclude anyone who bought a gift card in the last 7 days, if possible
- [ ] Schedule a reminder send around Dec 19–22 to non-openers or non-clickers

`creative-full.jpg` is the original creative, resized, for social posts or a single-image fallback.

---

# Holiday Catering email (Nov–Dec 2026)

Template: `holiday-catering-2026.html` (Constant Contact → Create → Email → **Custom Code**).
Images: `images/email/holiday-catering-2026/`, live at `https://guacmexigrill.ca/images/email/holiday-catering-2026/`
once this branch is merged and deployed. **Merge before sending a test**, or images will break.
Source: Communication #108 (Holiday Catering Campaign) and the "Cater Your Holidays" / "Scan. Order. Enjoy." creative.

## Offer
Save up to 20% on catering orders **placed in-store** (not valid online or for delivery):
$250+ 10% off · $500+ 10% off + 20 cookies · $1,000+ 15% off + 40 churros · $1,500+ 20% off + 50 churros.
Tiers and fine print mirror `catering-offers.html` (unlisted page; the email is a direct link to it).
Action CTAs go to the deals page and to Locations, never to online checkout.

## Subject lines (A/B test the first two)
| | Subject | Preheader |
|---|---|---|
| A | Holiday party? We'll feed the whole crew 🎄 | Taco bars, burrito boxes & more for the whole crew. Order in-store and save up to 20%. |
| B | Save up to 20% on holiday catering 🌮 | Office lunch, team party or family feast. Order in-store and save. |
| C | The office party is handled. | Taco bars and burrito boxes for 10 to 100+. Up to 20% off in-store. |
| Reminder (Dec 8–12) | Still planning the holiday party? | Up to 20% off catering when you order in-store. Free churros on big orders. |

The preheader is hard-coded at the top of the HTML (matches A); update it to match the subject you send.

## Email flow
1. Hero: "Cater Your Holidays." headline (live text) + creative photo with the text cropped out
2. Offer: "Save up to 20% OFF" + primary CTA: See Catering Deals (catering-offers#deals)
3. Savings tiers (4 cards; $1,500+ flagged Best Value)
4. Packages: Taco & Bowl Bar, Burrito Boxes, each linking to its section
5. How to order (3 steps, step 02 = order in-store)
6. Urgency band + Find Your Nearest GUAC
7. Footer + fine print. Constant Contact adds the address and unsubscribe block automatically.

## Tracking
`utm_campaign=holiday_catering_2026`, `utm_content` = `hero_image`, `primary_cta`, `tiers`,
`taco_bowl_bar`, `burrito_boxes`, `urgency_cta`, `footer_*`. Turn off Constant Contact's own UTM
tagging for this email to avoid duplicate parameters.

## Before sending
- [ ] Send to the same lists as the Holiday Gift Card email
- [ ] Send tests to Gmail (web + app), Outlook desktop, and iPhone Mail
- [ ] Schedule the reminder to non-clickers around Dec 8–12 (office parties book early)
