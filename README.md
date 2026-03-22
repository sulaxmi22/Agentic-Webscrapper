# Agentic Web Scraper

Web scrapers are dumb — they return raw HTML and leave the thinking to you. I wanted something that could take a URL, figure out what's relevant on the page, summarize it, and decide whether it needs to follow any links to get a complete answer. This is that.

It's built as a LangGraph agent loop rather than a linear chain because the decisions are genuinely conditional — sometimes the first page has everything, sometimes it needs to go deeper, and a static chain can't make that call.

---

## What it does

Give it a URL and an objective (e.g. "summarize the pricing page" or "extract all team members and their roles"). The agent:

1. Fetches and parses the page
2. Asks the LLM whether the content satisfies the objective
3. If yes — formats and returns a structured output
4. If no — identifies the most relevant link on the page and follows it, then repeats

The loop runs until the objective is satisfied or a max-depth limit is hit.

## Stack

- **LangGraph** — stateful agent graph, handles the conditional routing between scrape/reason/follow
- **OpenAI GPT-4** — reasoning, relevance judgment, output formatting
- **BeautifulSoup + requests** — HTML parsing and link extraction
- **LangChain** — tool definitions, prompt templates

The main reason for LangGraph over a simple LangChain chain: I needed the agent to loop back to the scrape node after following a link. You can't easily do that with LCEL — the graph model made this straightforward.

## Run it

```bash
git clone https://github.com/sulaxmi22/Agentic-Webscrapper.git
cd Agentic-Webscrapper

pip install -r requirements.txt

# set your key
export OPENAI_API_KEY=your_key_here

python main.py
```

## Limitations worth knowing

- Doesn't handle JavaScript-rendered pages (SPAs) — the scraper uses requests, not a headless browser. Adding Playwright is on the roadmap.
- Behind-auth pages return a 403 and the agent reports it cleanly rather than crashing, but obviously can't scrape them
- Rate limiting on aggressive multi-link traversal — added a small delay between requests but it's not configurable yet

## Things I want to add

- Playwright integration for JS-heavy sites
- Async multi-URL parallel scraping
- A `/research` FastAPI endpoint so this can be called from other services
