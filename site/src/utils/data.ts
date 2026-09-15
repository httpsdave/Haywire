// Mock data for development — simulates what the Python scrapers will produce
// Each category has a featured article and sidebar articles

export interface Article {
  id: string;
  title: string;
  url: string;
  source: string;
  sourceType: 'reddit' | 'rss' | 'scrape';
  category: string;
  timestamp: string;
  score?: number;
  isFeatured: boolean;
}

export interface CategoryData {
  name: string;
  slug: string;
  articles: Article[];
}

function formatDate(hoursAgo: number): string {
  const d = new Date(Date.now() - hoursAgo * 3600000);
  const months = ['January','February','March','April','May','June','July','August','September','October','November','December'];
  const month = months[d.getMonth()];
  const day = d.getDate();
  const year = d.getFullYear();
  let hours = d.getHours();
  const ampm = hours >= 12 ? 'PM' : 'AM';
  hours = hours % 12 || 12;
  const mins = d.getMinutes().toString().padStart(2, '0');
  return `${month} ${day}, ${year} | ${hours}:${mins} ${ampm}`;
}

export const mockWorldNews: CategoryData = {
  name: 'World News',
  slug: 'world-news',
  articles: [
    { id: 'wn1', title: 'UN General Assembly Adopts Landmark AI Governance Framework After Months of Negotiations', url: 'https://reuters.com', source: 'Reuters', sourceType: 'rss', category: 'world', timestamp: formatDate(1), score: 4521, isFeatured: true },
    { id: 'wn2', title: 'European Central Bank Signals Further Rate Cuts Amid Slowing Growth', url: 'https://bbc.com', source: 'BBC World', sourceType: 'rss', category: 'world', timestamp: formatDate(2), score: 2103, isFeatured: false },
    { id: 'wn3', title: 'Japan Launches Next-Generation Semiconductor Fab in Kumamoto', url: 'https://reuters.com', source: 'r/worldnews', sourceType: 'reddit', category: 'world', timestamp: formatDate(3), score: 1876, isFeatured: false },
    { id: 'wn4', title: 'Climate Summit Reaches Agreement on Methane Reduction Targets for 2035', url: 'https://aljazeera.com', source: 'Al Jazeera', sourceType: 'rss', category: 'world', timestamp: formatDate(4), score: 1654, isFeatured: false },
    { id: 'wn5', title: 'India\'s GDP Growth Exceeds Expectations at 7.2% in Q2', url: 'https://reuters.com', source: 'r/NeutralNews', sourceType: 'reddit', category: 'world', timestamp: formatDate(5), score: 1432, isFeatured: false },
    { id: 'wn6', title: 'Ukraine and Russia Signal Willingness to Resume Grain Corridor Talks', url: 'https://apnews.com', source: 'AP News', sourceType: 'rss', category: 'world', timestamp: formatDate(6), score: 1210, isFeatured: false },
  ]
};

export const mockPhNews: CategoryData = {
  name: 'Philippine News',
  slug: 'ph-news',
  articles: [
    { id: 'ph1', title: 'Marcos Signs Executive Order Establishing National Digital Infrastructure Program', url: 'https://inquirer.net', source: 'Inquirer.net', sourceType: 'rss', category: 'philippines', timestamp: formatDate(1), score: 3210, isFeatured: true },
    { id: 'ph2', title: 'PAGASA: Southwest Monsoon to Bring Heavy Rains Over Western Luzon This Week', url: 'https://gmanetwork.com', source: 'GMA News', sourceType: 'rss', category: 'philippines', timestamp: formatDate(2), score: 2100, isFeatured: false },
    { id: 'ph3', title: 'BSP Maintains Key Interest Rate at 5.75% Amid Stable Inflation', url: 'https://mb.com.ph', source: 'Manila Bulletin', sourceType: 'rss', category: 'philippines', timestamp: formatDate(3), score: 1800, isFeatured: false },
    { id: 'ph4', title: 'Senate Approves New Public Transport Modernization Bill on Third Reading', url: 'https://rappler.com', source: 'Rappler', sourceType: 'rss', category: 'philippines', timestamp: formatDate(4), score: 1650, isFeatured: false },
    { id: 'ph5', title: 'DOH Reports Rise in Dengue Cases, Launches Nationwide Prevention Campaign', url: 'https://news.abs-cbn.com', source: 'ABS-CBN News', sourceType: 'rss', category: 'philippines', timestamp: formatDate(5), score: 1500, isFeatured: false },
    { id: 'ph6', title: 'Philippine Stock Exchange Index Closes at New 2026 High on Foreign Inflows', url: 'https://philstar.com', source: 'PhilStar', sourceType: 'rss', category: 'philippines', timestamp: formatDate(6), score: 1320, isFeatured: false },
  ]
};

export const mockTechnology: CategoryData = {
  name: 'Technology',
  slug: 'technology',
  articles: [
    { id: 'tech1', title: 'Apple Unveils M5 Chip at iPhone 18 Launch Event, Claims 40% Performance Leap', url: 'https://theverge.com', source: 'r/technology', sourceType: 'reddit', category: 'technology', timestamp: formatDate(2), score: 5600, isFeatured: true },
    { id: 'tech2', title: 'OpenAI Announces GPT-6 with Real-Time Multimodal Reasoning Capabilities', url: 'https://techcrunch.com', source: 'r/technology', sourceType: 'reddit', category: 'technology', timestamp: formatDate(3), score: 4200, isFeatured: false },
    { id: 'tech3', title: 'SpaceX Starship Completes First Operational Mars Cargo Mission', url: 'https://spacenews.com', source: 'r/technology', sourceType: 'reddit', category: 'technology', timestamp: formatDate(4), score: 3800, isFeatured: false },
    { id: 'tech4', title: 'EU Digital Markets Act Forces Meta to Open WhatsApp Interoperability', url: 'https://reuters.com', source: 'Reuters', sourceType: 'rss', category: 'technology', timestamp: formatDate(5), score: 2900, isFeatured: false },
    { id: 'tech5', title: 'Samsung Begins Mass Production of 2nm GAA Process Node', url: 'https://anandtech.com', source: 'r/tech_philippines', sourceType: 'reddit', category: 'technology', timestamp: formatDate(6), score: 2100, isFeatured: false },
    { id: 'tech6', title: 'GitHub Copilot Now Handles Full Project Architecture, Not Just Code Completion', url: 'https://github.blog', source: 'r/pinoyprogrammer', sourceType: 'reddit', category: 'technology', timestamp: formatDate(7), score: 1800, isFeatured: false },
  ]
};

export const mockSports: CategoryData = {
  name: 'Sports',
  slug: 'sports',
  articles: [
    { id: 'sp1', title: 'Gilas Pilipinas Stuns Australia in FIBA Asia Cup Semifinals Behind Sotto\'s 28 Points', url: 'https://inquirer.net', source: 'r/gilasbasketball', sourceType: 'reddit', category: 'sports', timestamp: formatDate(1), score: 3400, isFeatured: true },
    { id: 'sp2', title: 'Azkals Qualify for 2027 Asian Cup After Historic Win Over Thailand', url: 'https://rappler.com', source: 'r/azkals', sourceType: 'reddit', category: 'sports', timestamp: formatDate(3), score: 2800, isFeatured: false },
    { id: 'sp3', title: 'PBA Philippine Cup Finals Set: San Miguel vs Ginebra in Best-of-Seven Series', url: 'https://gmanetwork.com', source: 'r/pba', sourceType: 'reddit', category: 'sports', timestamp: formatDate(4), score: 2200, isFeatured: false },
    { id: 'sp4', title: 'Carlos Yulo Wins Gold in World Gymnastics Championships Floor Exercise', url: 'https://philstar.com', source: 'PhilStar', sourceType: 'rss', category: 'sports', timestamp: formatDate(5), score: 1900, isFeatured: false },
    { id: 'sp5', title: 'Philippine Women\'s Volleyball Team Reaches FIVB Challenger Cup Final Four', url: 'https://rappler.com', source: 'r/philippinevolleyball', sourceType: 'reddit', category: 'sports', timestamp: formatDate(6), score: 1600, isFeatured: false },
    { id: 'sp6', title: 'Manchester City Completes Record Transfer for Argentine Midfielder', url: 'https://bbc.com', source: 'BBC Sport', sourceType: 'rss', category: 'sports', timestamp: formatDate(7), score: 1400, isFeatured: false },
  ]
};

export const mockScience: CategoryData = {
  name: 'Science',
  slug: 'science',
  articles: [
    { id: 'sc1', title: 'James Webb Telescope Discovers New Class of Exoplanets with Potential Biosignatures', url: 'https://nasa.gov', source: 'r/science', sourceType: 'reddit', category: 'science', timestamp: formatDate(2), score: 6100, isFeatured: true },
    { id: 'sc2', title: 'CRISPR Gene Therapy Shows 90% Efficacy in Sickle Cell Disease Trial', url: 'https://nature.com', source: 'r/science', sourceType: 'reddit', category: 'science', timestamp: formatDate(3), score: 4500, isFeatured: false },
    { id: 'sc3', title: 'Nuclear Fusion Reactor Achieves Net Energy Gain for 60 Continuous Seconds', url: 'https://reuters.com', source: 'Reuters', sourceType: 'rss', category: 'science', timestamp: formatDate(4), score: 3800, isFeatured: false },
    { id: 'sc4', title: 'Marine Biologists Discover New Deep-Sea Species in Philippine Trench', url: 'https://rappler.com', source: 'r/science', sourceType: 'reddit', category: 'science', timestamp: formatDate(5), score: 2900, isFeatured: false },
    { id: 'sc5', title: 'AI Model Predicts Earthquake Patterns with 72% Accuracy in Pacific Ring of Fire', url: 'https://sciencedaily.com', source: 'r/science', sourceType: 'reddit', category: 'science', timestamp: formatDate(7), score: 2100, isFeatured: false },
  ]
};

export const mockHealth: CategoryData = {
  name: 'Health',
  slug: 'health',
  articles: [
    { id: 'hl1', title: 'WHO Declares End of Latest Mpox Emergency as Vaccination Campaign Succeeds', url: 'https://who.int', source: 'r/health', sourceType: 'reddit', category: 'health', timestamp: formatDate(2), score: 3200, isFeatured: true },
    { id: 'hl2', title: 'New mRNA Vaccine Shows Promise Against Multiple Cancer Types in Phase 3 Trial', url: 'https://nature.com', source: 'r/health', sourceType: 'reddit', category: 'health', timestamp: formatDate(3), score: 2800, isFeatured: false },
    { id: 'hl3', title: 'DOH Launches Free Mental Health Hotline Available 24/7 Nationwide', url: 'https://gmanetwork.com', source: 'GMA News', sourceType: 'rss', category: 'health', timestamp: formatDate(4), score: 2100, isFeatured: false },
    { id: 'hl4', title: 'Study Links Ultra-Processed Foods to 30% Higher Risk of Depression', url: 'https://bbc.com', source: 'BBC Health', sourceType: 'rss', category: 'health', timestamp: formatDate(5), score: 1800, isFeatured: false },
    { id: 'hl5', title: 'Philippines Reports First Locally-Developed Dengue Rapid Test Kit', url: 'https://news.abs-cbn.com', source: 'ABS-CBN News', sourceType: 'rss', category: 'health', timestamp: formatDate(6), score: 1500, isFeatured: false },
  ]
};

export const mockPolitics: CategoryData = {
  name: 'Politics',
  slug: 'politics',
  articles: [
    { id: 'pol1', title: 'Supreme Court Rules on Landmark Case Expanding Freedom of Information Coverage', url: 'https://inquirer.net', source: 'Inquirer.net', sourceType: 'rss', category: 'politics', timestamp: formatDate(1), score: 4100, isFeatured: true },
    { id: 'pol2', title: 'House Passes Anti-Political Dynasty Bill on Final Reading After Decades of Debate', url: 'https://rappler.com', source: 'r/ph_politics', sourceType: 'reddit', category: 'politics', timestamp: formatDate(2), score: 3500, isFeatured: false },
    { id: 'pol3', title: 'COMELEC Announces Full Automation of 2028 National Elections', url: 'https://mb.com.ph', source: 'Manila Bulletin', sourceType: 'rss', category: 'politics', timestamp: formatDate(4), score: 2800, isFeatured: false },
    { id: 'pol4', title: 'US Congress Passes Bipartisan AI Regulation Act, Sends to President', url: 'https://apnews.com', source: 'r/NeutralPolitics', sourceType: 'reddit', category: 'politics', timestamp: formatDate(5), score: 2200, isFeatured: false },
    { id: 'pol5', title: 'EU Parliament Elects New Commission President After Lengthy Negotiations', url: 'https://reuters.com', source: 'r/geopolitics', sourceType: 'reddit', category: 'politics', timestamp: formatDate(6), score: 1900, isFeatured: false },
  ]
};

export const mockEntertainment: CategoryData = {
  name: 'Entertainment',
  slug: 'entertainment',
  articles: [
    { id: 'ent1', title: 'Filipino Film "Hugot sa Dagat" Wins Palme d\'Or at Cannes, First for Philippine Cinema', url: 'https://rappler.com', source: 'r/pinoycinema', sourceType: 'reddit', category: 'entertainment', timestamp: formatDate(2), score: 5200, isFeatured: true },
    { id: 'ent2', title: 'SB19 Announces World Tour with Stops in 30 Countries', url: 'https://gmanetwork.com', source: 'r/sb19', sourceType: 'reddit', category: 'entertainment', timestamp: formatDate(3), score: 4100, isFeatured: false },
    { id: 'ent3', title: 'Marvel Studios Unveils Phase 7 Slate Including First Filipino Superhero Film', url: 'https://variety.com', source: 'r/entertainment', sourceType: 'reddit', category: 'entertainment', timestamp: formatDate(4), score: 3200, isFeatured: false },
    { id: 'ent4', title: 'Eraserheads Reunion Concert at Philippine Arena Sells Out in 12 Minutes', url: 'https://news.abs-cbn.com', source: 'r/eraserheads', sourceType: 'reddit', category: 'entertainment', timestamp: formatDate(5), score: 2800, isFeatured: false },
    { id: 'ent5', title: 'Netflix\'s New Filipino Series "Aswang" Becomes Most-Watched Asian Title', url: 'https://variety.com', source: 'r/animeph', sourceType: 'reddit', category: 'entertainment', timestamp: formatDate(7), score: 2100, isFeatured: false },
  ]
};

export const mockEsports: CategoryData = {
  name: 'E-Sports',
  slug: 'esports',
  articles: [
    { id: 'es1', title: 'Filipino Team Blacklist International Wins M6 World Championship in Jakarta', url: 'https://oneesports.com', source: 'r/mobilelegendspinas', sourceType: 'reddit', category: 'esports', timestamp: formatDate(1), score: 4800, isFeatured: true },
    { id: 'es2', title: 'Valorant Champions Tour 2026 Finals to Be Held in Manila, Riot Games Announces', url: 'https://valorantesports.com', source: 'r/valorantph', sourceType: 'reddit', category: 'esports', timestamp: formatDate(3), score: 3600, isFeatured: false },
    { id: 'es3', title: 'League of Legends Worlds 2026 Group Stage Draws Released', url: 'https://lolesports.com', source: 'r/lolph', sourceType: 'reddit', category: 'esports', timestamp: formatDate(4), score: 2900, isFeatured: false },
    { id: 'es4', title: 'SEA Games 2027 Adds 5 New E-Sports Titles to Medal Events', url: 'https://rappler.com', source: 'r/phgaming', sourceType: 'reddit', category: 'esports', timestamp: formatDate(5), score: 2200, isFeatured: false },
    { id: 'es5', title: 'Wild Rift Asian League: PH Team Advances to Grand Finals', url: 'https://oneesports.com', source: 'r/wildriftph', sourceType: 'reddit', category: 'esports', timestamp: formatDate(6), score: 1800, isFeatured: false },
  ]
};

export const mockMemes: CategoryData = {
  name: 'Memes',
  slug: 'memes',
  articles: [
    { id: 'mm1', title: '"Nanay\'s WiFi Password" Format Takes Over as Most Viral Philippine Meme of 2026', url: 'https://reddit.com/r/pinoymemes', source: 'r/pinoymemes', sourceType: 'reddit', category: 'memes', timestamp: formatDate(1), score: 8200, isFeatured: true },
    { id: 'mm2', title: 'Senator\'s "May I Proceed" Clip Spawns Thousands of Edits Across Social Media', url: 'https://reddit.com/r/2philippines4u', source: 'r/2philippines4u', sourceType: 'reddit', category: 'memes', timestamp: formatDate(2), score: 6100, isFeatured: false },
    { id: 'mm3', title: '"Corporate Wants You to Find the Difference" Template Hits PH Government Context', url: 'https://reddit.com/r/philippinememes', source: 'r/philippinememes', sourceType: 'reddit', category: 'memes', timestamp: formatDate(3), score: 4500, isFeatured: false },
    { id: 'mm4', title: 'AI-Generated Memes of Historical Figures Eating Jollibee Go Viral', url: 'https://reddit.com/r/insanepinoyfacebook', source: 'r/insanepinoyfacebook', sourceType: 'reddit', category: 'memes', timestamp: formatDate(5), score: 3800, isFeatured: false },
    { id: 'mm5', title: '"Bakit Ganito Yung Traffic" Starter Pack Has Manila Commuters Feeling Seen', url: 'https://reddit.com/r/nanikposting', source: 'r/nanikposting', sourceType: 'reddit', category: 'memes', timestamp: formatDate(6), score: 3200, isFeatured: false },
  ]
};

export const allCategories: CategoryData[] = [
  mockWorldNews,
  mockPhNews,
  mockTechnology,
  mockSports,
  mockScience,
  mockHealth,
  mockPolitics,
  mockEntertainment,
  mockEsports,
  mockMemes,
];

// Helper: get the current formatted date for the masthead
export function getCurrentDate(): string {
  const d = new Date();
  const days = ['Sunday','Monday','Tuesday','Wednesday','Thursday','Friday','Saturday'];
  const months = ['January','February','March','April','May','June','July','August','September','October','November','December'];
  return `${days[d.getDay()]}, ${months[d.getMonth()]} ${d.getDate()}, ${d.getFullYear()}`;
}

export function getCurrentTime(): string {
  const d = new Date();
  let h = d.getHours();
  const ampm = h >= 12 ? 'PM' : 'AM';
  h = h % 12 || 12;
  const m = d.getMinutes().toString().padStart(2, '0');
  return `${h}:${m} ${ampm}`;
}

// Helper: get date labels for the date selector
export function getDateLabels(): { label: string; slug: string; isToday: boolean }[] {
  const labels = [];
  for (let i = 0; i <= 7; i++) {
    const d = new Date(Date.now() - i * 86400000);
    const slug = d.toISOString().split('T')[0];
    let label: string;
    if (i === 0) label = 'Today';
    else if (i === 1) label = 'Yesterday';
    else {
      const months = ['Jan','Feb','Mar','Apr','May','Jun','Jul','Aug','Sep','Oct','Nov','Dec'];
      label = `${months[d.getMonth()]} ${d.getDate()}`;
    }
    labels.push({ label, slug, isToday: i === 0 });
  }
  return labels;
}
