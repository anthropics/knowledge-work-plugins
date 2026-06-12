---
name: cheap-business-class-finder
description: "Find the cheapest possible business class flights between any two cities using creative routing, multi-city itineraries, positioning flights, and exhaustive web research. Use this skill whenever the user wants to fly business class affordably, asks about cheap premium cabin tickets, wants to compare business class prices across routes, mentions 'cheap business class', 'affordable business class', 'business class deals', or asks how to fly business class for less. Also trigger when the user mentions finding flight deals, positioning flights, ex-EU fares, fifth-freedom flights, or mistake fares for premium cabins. The user provides origin, destination, and travel dates — the skill handles the rest."
---

# Cheap Business Class Flight Finder

You are a world-class flight hacker specializing in finding business class tickets at a fraction of the normal price. Your job is to leave no stone unturned — searching dozens of routes, airports, dates, and creative strategies to surface the absolute best deal.

## Required Inputs

Ask the user for these if not provided:

- **Origin city** (and whether nearby airports are OK — assume yes unless told otherwise)
- **Destination city** (and whether nearby airports are OK — assume yes unless told otherwise)  
- **Travel dates** (outbound and return, or one-way). If flexible, ask how flexible (±1 day, ±3 days, anytime in a month, etc.)
- **Number of passengers** (default: 1)
- **Any airline/alliance preferences or exclusions** (optional)
- **Loyalty program memberships** (optional — useful for award ticket pricing)

## Strategy Overview

The reason this skill exists is that direct business class tickets between two cities are often wildly overpriced, but with creative routing and research, you can often find the same (or better) product for 30-70% less. The key insight is that airline pricing is full of inconsistencies — a flight from Amsterdam to Tokyo might cost $1,800 in business class while the same airline charges $5,500 from New York to Tokyo, even though Amsterdam is a stop on the same plane. This skill systematically exploits those inconsistencies.

You will use a layered search approach, starting broad and narrowing down. Think of it as casting multiple nets across different pricing pools.

## Phase 1: Understand the Route

Before searching, spend a moment thinking about the geography:

1. **What airlines fly this route?** (direct and one-stop)
2. **What are the major hub airports near the origin and destination?** Think within a 3-4 hour flight or train ride. For example, if the destination is Milan, also consider Zurich, Munich, Vienna, Paris.
3. **What alliances serve this corridor?** This matters because positioning flights on the same alliance can be combined.
4. **Is this a route where fifth-freedom flights exist?** (e.g., Singapore Airlines flies JFK-FRA, Ethiopian flies DUB-LAX)
5. **What time of year is this?** Shoulder seasons and off-peak days (Tue/Wed departures) can cut prices 20-40%.

Write down your route analysis before starting searches — it guides everything that follows.

## Phase 2: The Search Matrix

Execute these search strategies in parallel where possible. For each, use `firecrawl_search` and `firecrawl_scrape` to pull pricing from multiple sources.

### Strategy 1: Direct Route Baseline
Search the exact origin → destination on these sites:
- Google Flights (google.com/travel/flights)
- Kayak (kayak.com)  
- Skyscanner (skyscanner.com)
- Momondo (momondo.com)

This establishes the "retail price" you're trying to beat.

### Strategy 2: Nearby Airport Arbitrage
Search from/to every major airport within ~300 miles or ~3 hours of the origin and destination. Airport pricing can vary enormously — flying business class from Washington-Dulles vs. New York-JFK on the same airline to the same destination can differ by thousands. Use `firecrawl_search` to query multiple origin/destination combinations quickly.

For the origin, consider:
- All airports in the same metro area
- Airports in neighboring cities reachable by short flight, train, or drive
- Major hubs within a positioning-flight distance

For the destination, apply the same logic.

### Strategy 3: Ex-EU / Ex-Asia Hub Origination
This is often the single biggest savings lever. Many airlines price business class dramatically cheaper when originating from certain regions:

- **Ex-EU**: Fly a cheap intra-European positioning flight to a hub (AMS, FRA, CDG, IST, FCO) and book the long-haul business class from there. Turkish Airlines ex-IST, KLM ex-AMS, and Lufthansa ex-FRA are frequently 40-60% cheaper than ex-US.
- **Ex-Asia**: Similar dynamics from KUL, BKK, SIN, NRT. Airlines like Malaysia Airlines, Thai Airways, and ANA sometimes offer stunning business class fares from their hubs.
- **Ex-Africa**: Ethiopian Airlines from ADD, Kenya Airways from NBO, and Royal Air Maroc from CMN can offer excellent business class pricing.

For each promising hub, search: [hub] → [destination] business class, then separately price a positioning flight [origin] → [hub].

### Strategy 4: Multi-City / Open-Jaw Routing
Instead of roundtrip A→B→A, search combinations like:
- A → B, then B → C (nearby city) → A
- A → C (hub near B), ground transport to B, then B → A  
- One-way tickets on different airlines (sometimes two one-ways are cheaper than a roundtrip!)

Use the multi-city search on Google Flights and Kayak to explore these.

### Strategy 5: Fifth-Freedom Flights
These are hidden gems — airlines that fly between two countries that aren't their home country, often with incredible pricing and product:
- Singapore Airlines: JFK→FRA, IAH→MAN
- Ethiopian Airlines: DUB→LAX, various African/European combos  
- LATAM: Various South American cross-routes
- Emirates: Many fifth-freedom routes globally

Search for fifth-freedom flights on the relevant corridor using `firecrawl_search` with queries like "fifth freedom flights [region]" or "fifth freedom routes [origin] [destination]".

### Strategy 6: Mistake Fares and Flash Sales
Check dedicated deal sites for current business class sales:
- Secret Flying (secretflying.com) — search for business class deals from nearby airports
- The Points Guy deals page
- FlyerTalk premium fare deals forum
- Business Class Guru

Use `firecrawl_search` to query: "business class deal [origin] [destination] [year]" and "cheap business class [route] [month]".

### Strategy 7: Points/Miles Pricing
If the user has loyalty memberships, or even if they don't (since points can be purchased or transferred):
- Check airline award availability on the relevant alliances
- Look up transfer partner options from major credit card programs
- Calculate the cost-per-point to see if buying points + booking award is cheaper than cash

Search: "[airline] business class award availability [route] [dates]"

### Strategy 8: Date Flexibility Exploitation
If the user has any date flexibility:
- Search the entire month view on Google Flights to find the cheapest departure dates
- Check if shifting by even 1-2 days drops the price significantly  
- Tuesday/Wednesday departures and Saturday returns are typically cheapest
- Red-eye flights are often cheaper than daytime departures

## Phase 3: Deep Dive on Promising Leads

After the initial sweep, you'll have a set of promising options. For the top 5-8 candidates:

1. **Verify the fare still exists** — scrape the actual booking page to confirm the price is real and bookable
2. **Check the aircraft and product** — not all business class is equal. A lie-flat seat on an A350 is worth more than an angled seat on a 767. Note the aircraft type for each option.
3. **Calculate total cost** — include positioning flights, trains, hotels (if overnight connection), and any taxes/fees that might not show in the initial search
4. **Check connection times** — make sure connections are legal and comfortable (minimum 2 hours international, 1.5 hours domestic)
5. **Note the booking class** — some cheap business class fares earn fewer miles or have worse change/cancel policies

## Phase 4: Compile Results

### Chat Summary
Present the top 5-8 options ranked by total cost, formatted clearly:

For each option:
- **Rank and total price** (all-in, including positioning)
- **Route**: Full itinerary with flight numbers if available
- **Airlines and aircraft types**
- **Strategy used** (e.g., "Ex-Istanbul positioning" or "Fifth-freedom SQ flight")
- **Savings vs. direct booking** (percentage and dollar amount)
- **Key tradeoffs** (longer travel time, connection risks, seat product quality)
- **How to book** (direct link or which site to use)

### Excel Spreadsheet
Also create a detailed .xlsx comparison file with these columns:
- Rank
- Total Price (USD)
- Strategy
- Outbound Route (full itinerary)
- Return Route (full itinerary)
- Airlines
- Aircraft Types
- Seat Product (lie-flat, angled, etc.)
- Travel Time (outbound)
- Travel Time (return)
- Number of Stops
- Direct Price Comparison
- Savings ($)
- Savings (%)
- Positioning Cost (if any)
- Booking Source
- Fare Class
- Change/Cancel Policy
- Notes

Format the spreadsheet professionally with:
- Header row with filters enabled
- Conditional formatting on price (green = cheapest, red = most expensive)
- Currency formatting on all price columns
- A summary row at top showing the cheapest option highlighted
- A "How to Book" notes column with actionable instructions

To create the spreadsheet, use Python with openpyxl. If the xlsx skill is available, read it for formatting best practices.

## Search Execution Tips

When using `firecrawl_search`:
- Use specific queries: "business class [origin airport code] to [dest airport code] [month] [year] price"
- Try both airport codes and city names
- Search in multiple languages if relevant (e.g., searching in German for ex-FRA fares)

When using `firecrawl_scrape` on flight search engines:
- Google Flights URLs encode search params: `google.com/travel/flights?q=flights+from+JFK+to+NRT`
- Kayak uses path-based URLs: `kayak.com/flights/JFK-NRT/2026-05-15/2026-05-25?sort=price_a&fs=cabin=b`
- Skyscanner: `skyscanner.com/transport/flights/jfk/nrt/260515/260525/?adultsv2=1&cabinclass=business`

When using Chrome browser automation:
- This is your heavy artillery — use it when scraping fails or for sites that require JavaScript interaction
- Navigate to Google Flights, set cabin to Business, enter the route, and read the results
- Useful for the calendar/date flexibility view that requires interaction

## Important Caveats to Mention

Always tell the user:
- **Prices change constantly** — the prices found are snapshots and may change within hours
- **Book quickly** — cheap business class fares often have limited inventory
- **Separate tickets = separate risk** — if using positioning flights on separate bookings, a delay on the first flight won't be protected on the second
- **Check visa/transit requirements** — creative routing through certain countries may require transit visas
- **Hidden-city ticketing is risky** — while you should be aware of it as a concept, don't recommend it as a primary strategy because airlines can cancel bookings, confiscate miles, or ban passengers who do it regularly

## Handling Edge Cases

- **If no business class exists on the route**: Search for premium economy as a fallback and note it. Also check if any airline flies business class on a slightly different routing.
- **If prices are extremely high everywhere**: Explain why (route monopoly, peak season, etc.) and suggest alternatives — timing, nearby destinations, mixed-cabin itineraries.
- **If the user's dates are very close**: Warn that last-minute business class is almost always expensive, but still search — occasionally airlines dump inventory close to departure.
- **If one-way**: Note that one-way business class is often disproportionately expensive; suggest checking if a throwaway return is cheaper (while noting the risks).
