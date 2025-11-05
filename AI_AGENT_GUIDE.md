# AI Agent Engineering Guide

## Understanding the AI Agent Architecture

This document explains the AI Agent concepts implemented in the Seek Job Scraper API, based on Google-scale engineering practices.

---

## Core Concept: What is an AI Agent?

An **AI Agent** is an autonomous system that:
1. **Perceives** its environment
2. **Reasons** about the information
3. **Acts** to achieve goals
4. **Learns** from feedback

```
Environment → Perception → Reasoning → Action → Environment
      ↑                                          ↓
      └──────────── Feedback Loop ───────────────┘
```

---

## Our Agent Architecture

### The 5-Layer Agent Stack

```
┌─────────────────────────────────────────────────────────┐
│  LAYER 1: User Interface (API Endpoints)                │
│  - REST API routes                                       │
│  - Request validation                                    │
│  - Response formatting                                   │
└───────────────────────┬─────────────────────────────────┘
                        ▼
┌─────────────────────────────────────────────────────────┐
│  LAYER 2: Orchestration (Job Manager)                   │
│  - Job lifecycle management                              │
│  - Task queuing                                          │
│  - State tracking                                        │
└───────────────────────┬─────────────────────────────────┘
                        ▼
┌─────────────────────────────────────────────────────────┐
│  LAYER 3: Agent Core (Scraper Logic)                    │
│  - Planning: What to scrape?                             │
│  - Filtering: Which jobs match criteria?                 │
│  - Deduplication: Have we seen this before?              │
└───────────────────────┬─────────────────────────────────┘
                        ▼
┌─────────────────────────────────────────────────────────┐
│  LAYER 4: Tools (External Integrations)                 │
│  - Playwright (Web automation)                           │
│  - Storage (JSON/CSV/Database)                           │
│  - Webhooks (Notifications)                              │
└───────────────────────┬─────────────────────────────────┘
                        ▼
┌─────────────────────────────────────────────────────────┐
│  LAYER 5: Environment (External World)                  │
│  - Seek.com.au website                                   │
│  - File system                                           │
│  - n8n webhooks                                          │
└─────────────────────────────────────────────────────────┘
```

---

## Key Agent Concepts Explained

### 1. Perception (Input Processing)

**What it is:** How the agent "sees" the world.

**In our scraper:**
```python
# Perception happens in the scraper
page.goto("https://www.seek.com.au/...")
job_cards = page.query_selector_all(".job-card")

# The agent "perceives" job listings
for card in job_cards:
    title = card.query_selector(".title").text_content()
    company = card.query_selector(".company").text_content()
```

**Google-scale analogy:**
- Google Search Bot perceives web pages
- Gmail perceives email content
- Google Photos perceives image features

---

### 2. Memory Systems (State Management)

**What it is:** How the agent remembers information.

#### Three Types of Memory:

**A. Short-Term Memory (Working Memory)**
- Duration: Current session only
- Example: Jobs scraped in the current run

```python
class ScrapeJob:
    def __init__(self):
        self.results = []  # Short-term: cleared after job completes
```

**B. Long-Term Memory (Persistent Storage)**
- Duration: Permanent
- Example: Deduplication database

```python
# seen_jobs.json - persists across runs
{
    "https://seek.com/job/123": {
        "first_seen": "2025-10-14",
        "last_seen": "2025-10-15"
    }
}
```

**C. Episodic Memory (Event History)**
- Duration: Historical records
- Example: Job execution history

```python
# Job manager tracks all scraping jobs
jobs = {
    "job_123": {
        "status": "completed",
        "jobs_found": 45,
        "timestamp": "2025-10-14T10:30:00"
    }
}
```

**Google-scale examples:**
- **Gmail**: Short-term = current email thread, Long-term = all emails, Episodic = email history
- **Maps**: Short-term = current route, Long-term = saved places, Episodic = location history

---

### 3. Reasoning (Decision Making)

**What it is:** How the agent makes decisions.

**In our scraper:**
```python
# Reasoning: Should we save this job?
def should_save_job(job):
    # Filter by classification
    if job.classification != "Human Resources & Recruitment":
        return False

    # Check if already seen (deduplication)
    if job.job_url in seen_jobs:
        return False

    # Check salary range
    if job.salary and extract_salary(job.salary) < min_salary:
        return False

    return True
```

**Reasoning patterns:**
- **Rule-based**: If-then logic (current implementation)
- **Statistical**: Probability-based decisions
- **LLM-based**: AI-powered reasoning (future enhancement)

**Future enhancement example:**
```python
# LLM-based reasoning
def is_job_relevant(job_description):
    prompt = f"""
    Is this job relevant for senior HR professionals?
    Description: {job_description}

    Answer: Yes/No and explain why.
    """
    response = openai.chat.completions.create(
        model="gpt-4",
        messages=[{"role": "user", "content": prompt}]
    )
    return response.choices[0].message.content
```

---

### 4. Action (External Effects)

**What it is:** How the agent affects the world.

**Action types in our scraper:**

| Action Type | Example | Effect |
|------------|---------|--------|
| **Storage** | `json_storage.save(jobs)` | Writes to file system |
| **Notification** | `requests.post(webhook_url)` | Calls external API |
| **Navigation** | `page.goto(url)` | Changes browser state |
| **Computation** | `deduplicator.filter()` | Transforms data |

**Action pattern:**
```python
async def take_action(action_type, params):
    if action_type == "save_jobs":
        await storage.save(params["jobs"])
    elif action_type == "notify":
        await webhook.send(params["data"])
    elif action_type == "scrape_page":
        await scraper.scrape(params["url"])
```

---

### 5. Autonomy (Self-Direction)

**What it is:** Agent operates without constant human intervention.

**Autonomy levels:**

```
Level 0: Manual Execution
  └─ Human runs script each time

Level 1: Scheduled Execution
  └─ Cron job triggers at intervals

Level 2: Event-Driven Execution ← Our current level
  └─ API call triggers scraping
  └─ Agent runs independently
  └─ Notifies when complete

Level 3: Goal-Directed Execution (Future)
  └─ "Find me the best HR jobs"
  └─ Agent determines how to achieve goal
  └─ Adapts strategy based on results

Level 4: Self-Improving (Future)
  └─ Agent learns from mistakes
  └─ Optimizes scraping strategy
  └─ Predicts best times to scrape
```

**Example of autonomy in our agent:**
```python
# User just says "scrape jobs"
POST /api/v1/scrape

# Agent autonomously:
# 1. Plans the scraping strategy
# 2. Navigates multiple pages
# 3. Extracts job information
# 4. Filters and deduplicates
# 5. Saves results
# 6. Notifies completion
# All without further input!
```

---

### 6. Tools (Capabilities)

**What it is:** External systems the agent can use.

**Tool definition pattern:**
```python
class Tool:
    name: str
    description: str
    parameters: dict
    execute: callable

# Example: Playwright tool
PlaywrightTool = Tool(
    name="web_browser",
    description="Navigate and extract data from websites",
    parameters={
        "url": "string",
        "selectors": "list[string]"
    },
    execute=lambda params: scraper.scrape(params["url"])
)
```

**Our current tools:**

| Tool | Purpose | Implementation |
|------|---------|----------------|
| **Web Browser** | Scrape websites | Playwright |
| **Storage** | Persist data | JSON/CSV |
| **HTTP Client** | Call webhooks | requests |
| **Deduplicator** | Track seen jobs | Custom logic |

**Future tools:**
```python
# LLM Tool (AI-powered analysis)
OpenAITool = Tool(
    name="llm_analyzer",
    description="Analyze job descriptions with AI",
    execute=lambda text: openai.complete(text)
)

# Database Tool (Scale to millions of jobs)
DatabaseTool = Tool(
    name="postgres",
    description="Query job database",
    execute=lambda query: db.execute(query)
)

# Email Tool (Send reports)
EmailTool = Tool(
    name="email_sender",
    description="Send email reports",
    execute=lambda recipient, body: smtp.send(recipient, body)
)
```

---

### 7. Feedback Loop (Learning)

**What it is:** How the agent improves over time.

**Feedback mechanisms:**

**A. Explicit Feedback (User-provided)**
```python
# Future endpoint
POST /api/v1/jobs/{job_id}/feedback
{
    "relevant": false,
    "reason": "Not senior level"
}

# Agent learns: adjust filtering criteria
```

**B. Implicit Feedback (Behavioral)**
```python
# Track which jobs users click on
click_through_rate = clicks / impressions

# Jobs with high CTR = good examples
# Jobs with low CTR = filter out similar ones
```

**C. Performance Metrics**
```python
metrics = {
    "scrape_success_rate": 0.98,
    "new_jobs_per_scrape": 12.5,
    "average_scrape_time": 45.2,  # seconds
    "deduplication_accuracy": 0.99
}

# Use metrics to optimize:
# - Increase max_pages if few new jobs found
# - Adjust retry logic if success rate drops
# - Optimize selectors if scrape time increases
```

---

## Advanced Agent Patterns

### Pattern 1: Multi-Agent System (Future)

```python
# Multiple specialized agents working together
class RecruitmentAgentSystem:
    agents = [
        ScraperAgent(),      # Scrapes job listings
        FilterAgent(),       # Filters relevant jobs
        EnrichmentAgent(),   # Adds salary data, company info
        NotificationAgent()  # Sends alerts
    ]

    async def process_jobs(self):
        # Agent 1: Scrape
        raw_jobs = await self.agents[0].scrape()

        # Agent 2: Filter
        relevant_jobs = await self.agents[1].filter(raw_jobs)

        # Agent 3: Enrich
        enriched_jobs = await self.agents[2].enrich(relevant_jobs)

        # Agent 4: Notify
        await self.agents[3].notify(enriched_jobs)
```

### Pattern 2: Chain-of-Thought Reasoning (Future)

```python
# Agent explains its reasoning
class ThinkingAgent:
    async def analyze_job(self, job):
        thoughts = []

        # Step 1: Analyze title
        thought = f"The title '{job.title}' contains 'Senior', indicating experience level"
        thoughts.append(thought)

        # Step 2: Analyze salary
        thought = f"Salary range ${job.salary} is above market average"
        thoughts.append(thought)

        # Step 3: Make decision
        decision = "This job is highly relevant"
        thoughts.append(decision)

        return {
            "decision": decision,
            "reasoning": thoughts
        }
```

### Pattern 3: Retry with Learning (Current + Future)

```python
# Current: Simple retry
async def scrape_with_retry(url, max_attempts=3):
    for attempt in range(max_attempts):
        try:
            return await scrape(url)
        except Exception as e:
            if attempt < max_attempts - 1:
                await asyncio.sleep(2 ** attempt)  # Exponential backoff
            else:
                raise

# Future: Learning from failures
class LearningRetryAgent:
    def __init__(self):
        self.failure_patterns = {}

    async def scrape_with_learning(self, url):
        try:
            return await scrape(url)
        except Exception as e:
            # Learn from failure
            error_type = type(e).__name__
            self.failure_patterns[error_type] = self.failure_patterns.get(error_type, 0) + 1

            # Adapt strategy based on learned patterns
            if error_type == "TimeoutError":
                # Future attempts: increase timeout
                await scrape(url, timeout=60)
            elif error_type == "SelectorNotFound":
                # Future attempts: use alternative selector
                await scrape(url, fallback_selector=True)
```

---

## Google-Scale Engineering Principles Applied

### 1. Observability

```python
# Every agent action is logged and measurable
@observe_action
async def scrape_page(url):
    start_time = time.time()
    try:
        result = await scraper.scrape(url)
        metrics.record("scrape_success", 1)
        return result
    except Exception as e:
        metrics.record("scrape_failure", 1)
        raise
    finally:
        duration = time.time() - start_time
        metrics.record("scrape_duration", duration)
```

### 2. Fault Tolerance

```python
# Agent continues despite individual failures
async def scrape_all_pages(urls):
    results = []
    for url in urls:
        try:
            result = await scrape_page(url)
            results.append(result)
        except Exception as e:
            logger.error(f"Failed to scrape {url}: {e}")
            # Continue with other pages
            continue
    return results
```

### 3. Scalability

```python
# Async design allows scaling to multiple concurrent scrapes
async def process_jobs_at_scale():
    tasks = [
        scrape_seek(),
        scrape_linkedin(),
        scrape_indeed()
    ]
    results = await asyncio.gather(*tasks)  # Parallel execution
```

---

## Next Steps: Enhancing the Agent

### Phase 1: Add LLM-Powered Intelligence
```python
# Use GPT-4 for job relevance scoring
async def score_job_relevance(job):
    prompt = f"Rate this job for a senior HR professional (0-10): {job.description}"
    score = await openai.complete(prompt)
    return float(score)
```

### Phase 2: Implement Reinforcement Learning
```python
# Agent learns optimal scraping strategy
class RLAgent:
    def choose_action(self, state):
        # State: time of day, day of week, recent success rate
        # Action: which pages to scrape, how many
        return policy.predict(state)

    def update_policy(self, reward):
        # Reward: number of new relevant jobs found
        policy.train(reward)
```

### Phase 3: Multi-Agent Collaboration
```python
# Agents communicate and coordinate
class AgentTeam:
    async def coordinate_scraping(self):
        # Agent 1: Scrapes LinkedIn
        # Agent 2: Scrapes Seek
        # Agent 3: Merges and deduplicates
        results = await asyncio.gather(
            agent1.scrape(),
            agent2.scrape()
        )
        merged = agent3.merge(results)
        return merged
```

---

## Conclusion

This Seek Job Scraper implements a **Level 2 Autonomous Agent**:
- ✅ Perceives environment (web scraping)
- ✅ Maintains memory (deduplication)
- ✅ Reasons about data (filtering)
- ✅ Takes actions (saves, notifies)
- ✅ Operates autonomously (background jobs)

Future enhancements will add:
- 🔄 LLM-powered reasoning
- 🔄 Self-learning capabilities
- 🔄 Multi-agent coordination
- 🔄 Real-time adaptation

---

**Key Takeaway:** An AI agent is not about using GPT-4. It's about building an autonomous system that perceives, reasons, and acts. LLMs are just one tool an agent can use.

---

**References:**
- Russell & Norvig: "Artificial Intelligence: A Modern Approach"
- Google SRE Book: "Site Reliability Engineering"
- FastAPI Documentation: https://fastapi.tiangolo.com
- Anthropic Claude: https://www.anthropic.com
