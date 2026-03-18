# SFZC Website: Current Structure and Recommended Architecture

**Prepared:** February 27, 2026

---

## Part 1: The Current Website

### Overview

The current sfzc.org runs on **Drupal**, a content management system hosted on Pantheon. The site has grown organically over many years, resulting in a large but somewhat disorganized structure. Through a systematic crawl of the site, we identified approximately **150 unique page paths** on the main sfzc.org domain, plus eight separate sub-sites on their own subdomains.

The planned migration will move the site to **WordPress** on WP Engine, targeted for launch in **June 2026**.

### Current Site Sections

The main navigation has **eight top-level items**: About, Calendar, Locations, Dharma Talks, SFZC Online, Giving, News, and Store. Here is what each contains:

| Section | Nav label | What it covers |
|---------|-----------|---------------|
| **About** | About | Mission, lineage, board, governance, DEIA, affiliations, contact (~12 pages) |
| **Practice Centers** | Locations | City Center, Green Gulch Farm, Tassajara, and Online, each with 10-20 sub-pages (~50 pages total) |
| **Calendar** | Calendar | Events across all centers, plus per-center calendar pages and daily schedules |
| **Offerings** | Dharma Talks | Practice pathways (entering, establishing, deepening), livestream, dharma talk archive (~10 pages) |
| **Online** | SFZC Online | Online Zendo, live and on-demand courses, practice sessions (~5 pages) |
| **Giving** | Giving | Donations, membership, legacy giving, volunteering (~5 pages) |
| **News** | News | Links to the external Sangha News blog |
| **Store** | Store | Links to the external online bookstore |

Additional content lives outside the main navigation: approximately 285 teacher profiles, hundreds of individual dharma talk pages, chants and sutras (30+ PDFs), and various standalone pages for topics like residential practice, visa information, and family sangha.

### The Practice Center Pages

The three physical practice centers (plus Online) form the largest section of the site. Each center has its own landing page with a set of six tiles linking to sub-sections. However, the tile topics differ from center to center:

**City Center** tiles: Zen Meditation & Practice, Rooms & Rentals, Calendar, Residential Opportunities, About City Center, Bookstore

**Green Gulch Farm** tiles: About, Calendar, Zen Meditation & Practice, Visits & Stays, Conference Center, Getting to Green Gulch

**Tassajara** tiles: Summer Practice, Guest Season Retreats, Practice Periods, Work Periods, About Tassajara, Contact

This means a visitor who learns one center's page layout cannot carry that understanding to another center's page. Common topics like "Beginners" or "Teachers" appear at different levels and under different labels depending on the center.

Beneath the tiles, each center has a deep tree of sub-pages. For example, City Center's meditation and practice section alone contains pages for beginners, daily schedule, teachers, classes and courses, sesshins, practice periods, practice groups, and Saturday sangha. These pages sit three to five levels deep in the URL hierarchy.

### Separate Sub-sites

SFZC operates **eight separate websites** on different subdomains, each running its own platform:

| Sub-site | Purpose |
|----------|---------|
| **store.sfzc.org** | Online bookstore |
| **app.sfzc.org** | Dharma Talk streaming archive |
| **learn.sfzc.org** | On-demand courses |
| **giving.sfzc.org** | Donation and membership portal |
| **blogs.sfzc.org** | Sangha News Journal |
| **memorials.sfzc.org** | Great Leap Memorial Blog (In Memoriam) |
| **branchingstreams.sfzc.org** | Directory of affiliated sanghas |
| **sfzc.org** | The main site itself |

For a visitor, clicking through the site means jumping between these separate platforms without warning. The "News" menu item takes you off the main site entirely. The "Dharma Talk Archive" link in the navigation goes to app.sfzc.org, but the same-labeled link in the Offerings sidebar goes to an internal page. "Donate" goes to giving.sfzc.org. "Store" goes to store.sfzc.org. The fragmentation makes the experience feel disjointed and can be disorienting.

### What We Found: Problems in Detail

#### 1. The navigation does not match the site

Several navigation labels are misleading or inconsistent:

- The nav item labeled **"Dharma Talks"** does not go to dharma talks. It goes to the **Offerings** page, which contains the entering/establishing/deepening practice pathways alongside dharma talk resources. A visitor clicking "Dharma Talks" expecting recorded talks lands on a much broader page. The actual Offerings section has no nav item under its own name.

- The nav says **"Locations"** but the URLs say `/practice-centers`. The homepage calls them "Practice Centers." The footer uses individual center names without a grouping label. Three different terms for the same concept.

- **"SFZC Online" appears in two places** in the navigation: as the fourth item under "Locations" and as its own top-level menu item. The same concept takes up two of eight navigation slots.

- The **"Dharma Talk Archive"** sub-nav item links to app.sfzc.org (an external site), but the sidebar link with the same label on the Offerings page links to an internal archive page. Same label, different destinations.

- **"News"** and **"Store"** both take visitors off the main site entirely, with no internal landing pages.

#### 2. Duplicate and inconsistent page paths

Many pages can be reached through two or more different URLs:

- The City Center page exists at both `/locations/city-center` and `/practice-centers/city-center`.
- The volunteering page exists at both `/support/outreach-volunteering` and `/giving/outreach-volunteering`.
- Livestream events are at both `/offerings/livestream-media` and `/upcoming-livestream-events`.
- Online content uses three different URL prefixes: `/online-page`, `/online-programs/`, and `/sfzc-online/`.
- Legacy paths from earlier versions of the site (`/welcome/...`, `/about-us/...`, `/about-sfzc/...`) still work alongside the current paths.

This duplication confuses search engines (which cannot tell which version to show in results), makes analytics unreliable (traffic is split across duplicate URLs), and creates maintenance headaches (editors may not know which version to update).

#### 3. Deeply nested pages

Some content is buried four or five levels deep. Here are real examples from the current site:

> `/practice-centers/city-center/zen-meditation-practice-city-center/sitting-meditation-sesshins-at-city-center`

> `/practice-centers/green-gulch-farm/zen-meditation-practice-green-gulch/classes-courses-green-gulch/sewing-buddha's-robe`

> `/locations/green-gulch-farm/about-green-gulch/farm-garden-programs/farm-land-steward-apprenticeship`

> `/about/how-san-francisco-zen-center-operates/conflict-complaint-and-ethical-review-processes`

Pages this deep are hard to find, hard to share (imagine texting one of these URLs to a friend), and hard for search engines to index effectively. They also create unwieldy breadcrumb trails that are difficult to navigate on mobile devices.

#### 4. Repetitive content across centers

Each practice center has its own set of sub-pages covering the same topics: beginners, daily schedule, teachers, classes, sesshins, practice periods, guest stays, residential practice, and more. While the specific details differ by center (schedules, programs, teachers), the pages do not link to each other or to any shared overview.

For example, the City Center beginners page describes Saturday morning meditation at 9:25 AM and Thursday online sessions, while the Green Gulch beginners page describes Sunday zazen instruction at 8:15 AM and half-day introductory sittings. These are appropriately distinct. But neither page links to the other, and neither links to the general "Entering Practice" overview. A visitor who finds one center's beginners page has no pathway to discover the other center's equivalent or the organization-wide beginner resources.

The teacher listings show a similar problem. City Center's teachers page lists 18 people and mixes teaching roles with governance roles (President, Corporate Secretary, Governance Committee Chair). Green Gulch's teachers page lists 43 people, better categorized into core teachers and guest teachers. The two pages use different organizational approaches for the same type of content.

#### 5. The "Offerings" section tries to do too much

The Offerings section is doing double duty as both a dharma talks hub and a practice pathways guide. These serve fundamentally different needs:

- Someone looking for **dharma talks** wants to browse, search, and listen to recordings.
- Someone exploring **practice pathways** wants guidance on how to begin, deepen, or commit to practice.

Combining these under one roof (and then labeling it "Dharma Talks" in the navigation) means neither audience is well served.

The three practice pathways (Entering, Establishing, Deepening Practice) are themselves problematic. "Establishing Practice" and "Deepening Practice" are organized as two-column comparisons of City Center and Green Gulch offerings, essentially duplicating content that already exists on those centers' pages. Tassajara, despite being the most intensive practice environment SFZC offers, is mentioned only in passing. The "Entering Practice" page recommends the Online Zendo and books but does not link to the center-specific beginners pages where someone would find concrete program schedules.

Additionally, the "Featured Offerings" link in the sidebar navigation of this section **returns a 404 error**. This broken link is visible on every page in the Offerings section.

#### 6. Teacher profiles are dead ends

Teacher profiles contain valuable biographical information. For example, a profile might describe when a teacher began practice, their training history, dharma transmission lineage, publications, and current role. But the profiles do not connect visitors to anything actionable:

- **No links to their dharma talks.** A visitor reading about a teacher cannot click through to hear their teachings.
- **No links to upcoming events.** There is no "upcoming events with this teacher" section.
- **No links back to their center's page.** The biography mentions which center they serve, but there are no direct links.
- **No way to request a meeting.** For teachers who offer practice interviews, there is no scheduling or contact information.

A teacher profile is effectively a biographical page with no onward path. The visitor reads it and has nowhere to go.

#### 7. Dharma talks exist as descriptions without audio

Individual dharma talk pages on sfzc.org contain the talk title, speaker name, date, location, and a written description. But the actual audio or video is not embedded on the page. To listen, a visitor must go to the separate Dharma App (app.sfzc.org), or find the talk on a podcast platform or YouTube.

The on-site dharma talk archive can only be filtered by year. There is no filtering by teacher, practice center, topic, or keyword. There is no search. Pagination shows a "More Events" link with no indication of how many talks exist in total.

The result is that sfzc.org functions as a catalog of dharma talks that points elsewhere for the actual content. A visitor who arrives at a talk page from a search engine finds a description but no way to listen without navigating to a different website.

#### 8. The calendar lacks basic functionality

The calendar page displays events in a chronological table with columns for start time, location, and event title. Two dropdown filters are available: Event Type and Practice Center. Beyond these:

- **No text search.** A visitor looking for a specific teacher's events or a named retreat must scroll through results manually.
- **No date range selector.** There is no way to jump to a specific month or week. Visitors see events starting from today and must click "More Events" repeatedly to look ahead.
- **No distinction between the calendar and daily schedules.** Each center has separate daily schedule pages (linked under the Calendar nav dropdown), but the relationship between recurring daily events and calendar events is unclear. Are daily zazen periods on the calendar? Or only on the daily schedule page? The answer is not obvious.
- **Event titles carry metadata that belongs in structured fields.** Titles like "Monthly BIPOC Affinity Group, CC 2/27" include the location abbreviation and date even though those are already shown in separate columns.

#### 9. The beginner path is broken

A new visitor arriving at sfzc.org sees a homepage card labeled "New to Zen Center?" that links to the About page. But the About page is an organizational overview covering mission, lineage, governance, and history. It contains no practical guidance for a beginner looking to start practicing.

The actual beginner resources, which are well written and helpful, are scattered in at least three places:

- The **Entering Practice** page under Offerings (but hidden behind the "Dharma Talks" nav label)
- The **Beginners** page under each practice center (buried 3-4 levels deep)
- The **Online Zendo** page (under the separate Online section)

These pages do not link to each other. A visitor who finds one has no way to discover the others. The site has good beginner content; it simply has no coherent path for a beginner to follow.

#### 10. Important pages are hard to find

Several significant pages are reachable only from the footer, which contains 50+ links:

- **DEIA Feedback Form**: not in the main navigation
- **Conflict, Complaint, and Ethical Review Processes**: footer only
- **Conference Centers** for City Center and Green Gulch: footer and center landing page tiles, but not in the main nav
- **Great Leap Memorial Blog** (memorials.sfzc.org): footer only
- **Non-Profit Status**: footer only
- **Podcast links** (Apple Podcasts, Spotify, RSS): footer only
- **Greens Restaurant, Enso Village, Enso Verde**: footer logo area only

The footer essentially functions as a secondary sitemap, which suggests that the main navigation does not adequately represent the site's content.

#### 11. No XML sitemap for search engines

The site lacks an XML sitemap, which is a standard file that tells search engines like Google about every page on the site. Without one, search engines must discover pages by following links from other pages. Given the site's deep nesting and inconsistent navigation, it is likely that some pages are poorly indexed or not indexed at all. This means potential visitors searching for SFZC content on Google may not find the most relevant pages.

#### 12. Eight separate platforms with no unified experience

Taken together, a visitor to SFZC's web presence may encounter eight different websites: the main Drupal site, the Dharma App, the online course platform, the blog, the memorial blog, the bookstore, the donation portal, and the affiliated sanghas directory. Each has its own design, navigation, and login system. There is no shared header, no common search, and no way to move between them without knowing the specific subdomain. For an organization that presents itself as one community across three physical centers and an online program, the web experience tells a different story.

---

## Part 2: Recommended WordPress Architecture

### Design Principles

1. **One home for each piece of content.** Every teacher, dharma talk, event, and page lives at exactly one address. No more duplicate paths.

2. **Connected, not copied.** A teacher's profile is created once. When that teacher is linked to a City Center event or a dharma talk, their information appears automatically. Update the teacher's bio in one place and it updates everywhere.

3. **No more than three levels deep.** The deepest page on the new site would be something like `/practice-centers/green-gulch/farm-garden/`. Most content is one or two levels deep.

4. **Editors focus on content, not layout.** Templates control how pages look. Editors fill in structured fields (title, description, speaker, date, etc.) and the design is handled automatically.

5. **The calendar is the calendar.** Instead of manually maintained calendar pages per center, each center's calendar is simply a filtered view of the same event data. Add an event once with the right center and type, and it appears in all the right places.

### Content Types

The new site organizes content into four main types, each with its own structured format:

**Teachers** (approximately 285 profiles)

Each teacher has a profile with their photo, title, biography, role (e.g., Abbot, Senior Dharma Teacher, Practice Leader, Guest Teacher), which center(s) they're affiliated with, and whether they are currently active. Teacher profiles are linked from event pages, dharma talks, and center pages automatically.

> Example: `/teachers/eijun-linda-cutts/`

**Dharma Talks** (hundreds of recordings)

Each dharma talk has a speaker (linked to their teacher profile), date, audio or video, a summary, and optional transcript. Talks can be browsed by teacher, center, topic, or date.

> Example: `/dharma-talks/cultivating-intimacy-our-body/`

**Events** (approximately 5,700 historical and ongoing)

Events include sesshins, workshops, retreats, classes, practice periods, and guest season dates. Each event has a date and time, location (linked to a practice center), teacher or leader (linked to their profile), event type, and whether it's in-person, online, or hybrid. The Events Calendar plugin generates calendar views automatically, with filters for center, type, and date range.

> Example: `/events/one-day-sitting-march-2026/`

**Practice Centers** (4: City Center, Green Gulch Farm, Tassajara, Online)

Each practice center has its own hub page with an introduction, photo, contact information, daily schedule, and links to its sub-pages. Sub-pages for each center cover topics like how to visit, classes, guest stays, and programs specific to that location.

> Example: `/practice-centers/city-center/`

### Recommended Page Map

Below is the full proposed structure. Indentation shows parent-child relationships.

#### Home

The homepage introduces SFZC and highlights the three physical practice centers, upcoming events, recent dharma talks, and calls to action for new visitors and supporters.

#### About

- About SFZC (`/about/`)
    - Mission and Vision (`/about/mission-and-vision/`)
    - Lineage (`/about/lineage/`)
    - Board of Directors (`/about/board-of-directors/`)
    - How We Operate (`/about/how-we-operate/`)
    - DEIA (`/about/deia/`)
    - Ethics and Complaints (`/about/ethics-and-complaints/`)
    - Affiliations (`/about/affiliations/`)
    - Non-Profit Status (`/about/non-profit-status/`)
    - Contact (`/about/contact/`)

#### Practice Centers

- Practice Centers (`/practice-centers/`)
    - **City Center** (`/practice-centers/city-center/`)
        - About (`/practice-centers/city-center/about/`)
        - Daily Schedule (`/practice-centers/city-center/schedule/`)
        - Beginners (`/practice-centers/city-center/beginners/`)
        - Classes and Courses (`/practice-centers/city-center/classes/`)
        - Sesshins (`/practice-centers/city-center/sesshins/`)
        - Practice Periods (`/practice-centers/city-center/practice-periods/`)
        - Guest Stays (`/practice-centers/city-center/guest-stays/`)
        - Residential Practice (`/practice-centers/city-center/residential/`)
        - Conference Center (`/practice-centers/city-center/conference-center/`)
        - Calendar (`/practice-centers/city-center/calendar/`)
        - Directions (`/practice-centers/city-center/directions/`)
        - Contact (`/practice-centers/city-center/contact/`)
    - **Green Gulch Farm** (`/practice-centers/green-gulch/`)
        - About (`/practice-centers/green-gulch/about/`)
        - Daily Schedule (`/practice-centers/green-gulch/schedule/`)
        - Beginners (`/practice-centers/green-gulch/beginners/`)
        - Sunday Program (`/practice-centers/green-gulch/sunday-program/`)
        - Classes and Courses (`/practice-centers/green-gulch/classes/`)
        - Sesshins (`/practice-centers/green-gulch/sesshins/`)
        - Practice Periods (`/practice-centers/green-gulch/practice-periods/`)
        - Guest Stays (`/practice-centers/green-gulch/guest-stays/`)
        - Residential Practice (`/practice-centers/green-gulch/residential/`)
        - Farm and Garden (`/practice-centers/green-gulch/farm-garden/`)
        - Farmers Market (`/practice-centers/green-gulch/farmers-market/`)
        - Way of Tea (`/practice-centers/green-gulch/way-of-tea/`)
        - Volunteer Program (`/practice-centers/green-gulch/volunteer/`)
        - Conference Center (`/practice-centers/green-gulch/conference-center/`)
        - Calendar (`/practice-centers/green-gulch/calendar/`)
        - Directions (`/practice-centers/green-gulch/directions/`)
        - Contact (`/practice-centers/green-gulch/contact/`)
    - **Tassajara** (`/practice-centers/tassajara/`)
        - About (`/practice-centers/tassajara/about/`)
        - Hot Springs (`/practice-centers/tassajara/hot-springs/`)
        - Zen Monastery (`/practice-centers/tassajara/zen-monastery/`)
        - Practice Programs (`/practice-centers/tassajara/practice-programs/`)
        - Practice Periods (`/practice-centers/tassajara/practice-periods/`)
        - Guest Season (`/practice-centers/tassajara/guest-season/`)
        - Reservations (`/practice-centers/tassajara/reservations/`)
        - What to Expect (`/practice-centers/tassajara/what-to-expect/`)
        - Summer Practice (`/practice-centers/tassajara/summer-practice/`)
        - Calendar (`/practice-centers/tassajara/calendar/`)
        - Contact (`/practice-centers/tassajara/contact/`)
    - **Online** (`/practice-centers/online/`)
        - Online Zendo (`/practice-centers/online/zendo/`)
        - Live Courses (`/practice-centers/online/live-courses/`)
        - On-Demand Courses (`/practice-centers/online/on-demand/`)
        - Schedule (`/practice-centers/online/schedule/`)

#### Practice

Cross-center resources for practitioners at all levels.

- Practice (`/practice/`)
    - New to Zen (`/practice/new-to-zen/`)
    - Finding a Teacher (`/practice/finding-a-teacher/`)
    - Residential Practice (`/practice/residential/`)
    - Sewing Buddha's Robe (`/practice/sewing-buddhas-robe/`)
    - Chants and Texts (`/practice/chants-and-texts/`)
    - Family Sangha (`/practice/family-sangha/`)
    - Visa Information (`/practice/visa-information/`)

#### Dharma Talks

Browsable archive with filters for teacher, center, topic, and date.

- Dharma Talks (`/dharma-talks/`)
    - Individual talks (`/dharma-talks/{title}/`)
    - Suzuki Roshi Archive (`/dharma-talks/suzuki-roshi/`)
    - Livestream (`/dharma-talks/livestream/`)

#### Teachers

Browsable directory with filters for center, role, and active status.

- Teachers (`/teachers/`)
    - Individual profiles (`/teachers/{name}/`)

#### Events

Calendar views with filters for center, event type, date range, and level.

- Events (`/events/`)
    - Individual events (`/events/{title}/`)

#### Giving

- Giving (`/giving/`)
    - Donate (`/giving/donate/`)
    - Membership (`/giving/membership/`)
    - Legacy Giving (`/giving/legacy/`)
    - Volunteer (`/giving/volunteer/`)

#### News

- News (`/news/`)
    - Sangha News (`/news/sangha-news/`)
    - In Memoriam (`/news/in-memoriam/`)

#### Store

Redirects to store.sfzc.org.

### Navigation

**Main menu (header):**

| Practice Centers | Events | Dharma Talks | Teachers | About | Giving |
|-----------------|--------|-------------|----------|-------|--------|
| City Center | | | | Mission | |
| Green Gulch | | | | Lineage | |
| Tassajara | | | | Board | |
| Online | | | | How We Operate | |
| | | | | Contact | |

**Utility bar (above or beside main menu):**

Store | News | Livestream | Search | **Donate**

**Footer (four columns):**

| Practice Centers | Practice | About | Connect |
|-----------------|----------|-------|---------|
| City Center | New to Zen | Mission and Vision | Newsletter Signup |
| Green Gulch Farm | Chants and Texts | Board of Directors | Sangha News |
| Tassajara | Find a Teacher | How We Operate | Social Media |
| Online | Residential Practice | Non-Profit Status | SFZC App |
| | Family Sangha | DEIA | Branching Streams |
| | | Contact | |

### How Content Connects

One of the biggest improvements in the new architecture is how content is linked together. Here are some examples:

**A teacher's profile page** automatically shows:

- Their biography, photo, and role
- Upcoming events where they are teaching
- Recent dharma talks they have given
- Which practice center(s) they are affiliated with

**A practice center page** automatically shows:

- Its daily schedule and contact information
- Upcoming events at that center (pulled from the events calendar)
- Teachers currently affiliated with that center
- Recent dharma talks from that center

**An event page** automatically shows:

- Date, time, and location details
- The teacher or leader (linked to their profile)
- Which center it belongs to
- Related events of the same type

All of this happens because the content is connected through relationships, not because someone has manually placed the information on each page. When a teacher's role changes or a new event is added, all the pages that reference that information update automatically.

### Sub-sites: What Stays Separate, What Comes In

| Sub-site | Recommendation | Reason |
|----------|---------------|--------|
| **store.sfzc.org** | Keep separate | The bookstore has its own ordering and inventory system |
| **app.sfzc.org** | Evaluate | If dharma talks move fully into WordPress, this could eventually be retired or serve as an embed source |
| **learn.sfzc.org** | Keep separate | Course platform with its own enrollment and payment system |
| **giving.sfzc.org** | Keep separate | Donation processing with its own forms and payment handling |
| **blogs.sfzc.org** | Bring into WordPress | Blog posts and news articles are exactly what WordPress does best; consolidating avoids maintaining a separate system |
| **branchingstreams.sfzc.org** | Keep separate | Community-maintained directory for affiliated sanghas |

### Redirects: Preserving Search Engine Rankings

Every page on the current Drupal site will need a redirect to its new WordPress address. This ensures that anyone who has bookmarked an old page, and any links from search engines, will still work. Key redirects include:

- All `/locations/...` paths redirect to `/practice-centers/...`
- All `/welcome/...`, `/about-us/...`, and `/about-sfzc/...` paths redirect to `/about/...`
- The deeply nested practice pages (e.g., `/practice-centers/city-center/zen-meditation-practice-city-center/beginners`) redirect to their shorter equivalents (e.g., `/practice-centers/city-center/beginners/`)
- `/offerings/...` pages redirect to their new homes under `/practice/` or specific center pages
- `/teachings/dharma-talks/...` redirects to `/dharma-talks/...`

A complete redirect map will be prepared before launch and implemented using the Redirection plugin in WordPress.

---

## Summary

The current sfzc.org has accumulated complexity over many years: duplicate paths, deeply nested pages, content scattered across overlapping sections, and six separate sub-sites. The recommended WordPress architecture addresses these issues by:

1. **Giving every piece of content one clear home** with short, readable addresses
2. **Connecting content through relationships** so that updating a teacher's profile or adding an event automatically appears in all the right places
3. **Limiting page depth to three levels** so visitors and search engines can find everything easily
4. **Consolidating the blog** into the main site while keeping specialized platforms (store, courses, donations) separate
5. **Preserving all existing links** through a comprehensive redirect plan

The result should be a site that is easier for visitors to navigate, easier for staff to maintain, and better positioned in search results.
