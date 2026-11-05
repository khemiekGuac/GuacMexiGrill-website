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
