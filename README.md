# Vigorys Nuclear Edition

Advanced Business Logic Vulnerability Scanner - CLI-only, Multi-Agent System, LLM-powered

## Features

✨ **7 Nuclear Features:**
1. **Multi-Agent System** (ReAct + Chain-of-Thought)
2. **Stateful Multi-User Simulation** (parallel role sessions)
3. **Dynamic LLM-guided Fuzzing** (intelligent mutations)
4. **Custom Business Rule Engine** (YAML/natural language)
5. **Executable Attack Graphs** (PoC generation)
6. **Self-Improvement Loop** (learning from findings)
7. **Terminal Output** (real-time progress, ASCII art)

🚀 **Integrated Bases:**
- **bizlogic** - Fast heuristic-based detection
- **strix** - Autonomous AI agents with ReAct
- **seclab-taskflow** - Agentic orchestration

📊 **Scan Modes:**
- `quick` - Fast heuristic-based scan
- `normal` - Balanced scan with LLM reasoning
- `ultra` - Deep analysis with all features
- `nuclear` - Maximum power (all agents + fuzzing)

## Installation

```bash
# Clone repository
git clone https://github.com/shamanORc/Vygoris.git
cd Vygoris/vygoris-nuclear-core

# Install dependencies
pip install -r requirements.txt

# Download Playwright browsers
playwright install

# Configure environment
cp .env.example .env
# Edit .env with your LLM API key
```

## Quick Start

### Basic Nuclear Scan
```bash
python vigorys.py scan --url https://example.com --mode nuclear --llm grok
```

### With Custom Business Rules
```bash
python vigorys.py scan --url https://example.com --mode nuclear --rules business_rules.yaml
```

### Quick Scan (Fast)
```bash
python vigorys.py scan --url https://example.com --mode quick
```

### Demo Mode
```bash
python vigorys.py demo
```

### Generate Rules Template
```bash
python vigorys.py generate-rules --output my_rules.yaml
```

## Usage Examples

### Example 1: Scan with Export
```bash
python vigorys.py scan \
  --url https://myapp.com \
  --mode nuclear \
  --llm grok \
  --export report.json \
  --format json
```

### Example 2: Parallel Scanning
```bash
python vigorys.py scan \
  --url https://myapp.com \
  --mode ultra \
  --workers 8 \
  --timeout 600
```

### Example 3: Custom Rules
```bash
python vigorys.py scan \
  --url https://myapp.com \
  --mode nuclear \
  --rules business_rules.yaml
```

## Business Rules Format

Create a `business_rules.yaml` file:

```yaml
rules:
  - name: "Payment Approval Limit"
    description: "Regular users cannot approve payments > R$ 1000"
    condition: "user_role == 'user' AND payment_amount > 1000"
    expected_result: "DENY"
    severity: "HIGH"
  
  - name: "Order Status Flow"
    description: "Orders must follow specific status transitions"
    condition: "order_status_transition"
    expected_flow:
      - "PENDING"
      - "PROCESSING"
      - "SHIPPED"
      - "DELIVERED"
    severity: "MEDIUM"
  
  - name: "Admin-Only Actions"
    description: "Only admins can delete users"
    condition: "action == 'delete_user' AND user_role != 'admin'"
    expected_result: "DENY"
    severity: "CRITICAL"
```

## Output Format

### Terminal Output
- Real-time progress with spinners
- Colored severity indicators (🔴 Critical, 🟠 High, 🟡 Medium, 🔵 Low)
- Organized findings table
- ASCII art attack flow visualization

### Report Export (JSON)
```json
{
  "scan_id": "scan_001",
  "target": "https://example.com",
  "mode": "nuclear",
  "status": "completed",
  "findings": [
    {
      "id": "finding_001",
      "type": "authorization_bypass",
      "severity": "CRITICAL",
      "confidence": "HIGH",
      "description": "...",
      "steps_to_reproduce": [...],
      "poc": "...",
      "fix_suggestion": "..."
    }
  ],
  "attack_graph": {...},
  "summary": {...}
}
```

## Architecture

```
vigorys-nuclear-core/
├── vigorys.py                 # Main CLI entry point
├── requirements.txt           # Python dependencies
├── .env.example               # Configuration template
│
├── core/
│   ├── cli.py                 # CLI handler
│   ├── config.py              # Configuration
│   └── logger.py              # Logging
│
├── agents/
│   ├── orchestrator.py        # Multi-Agent coordinator
│   ├── recon_agent.py         # Crawling
│   ├── role_simulator.py      # Multi-user sessions
│   ├── logic_reasoner.py      # LLM reasoning
│   ├── validator_exploiter.py # PoC generation
│   └── triage_reporter.py     # Finding deduplication
│
├── engines/
│   ├── bizlogic_engine.py     # bizlogic integration
│   ├── strix_engine.py        # strix integration
│   ├── seclab_engine.py       # seclab-taskflow integration
│   ├── llm_reasoner.py        # LLM reasoning
│   └── fuzzer.py              # Dynamic fuzzing
│
├── modules/
│   ├── advanced_analyzer.py   # 12 detection mechanisms
│   ├── jwt_analyzer.py        # JWT analysis
│   ├── api_key_detector.py    # API key detection
│   ├── compliance_checker.py  # OWASP/CWE/CVSS
│   ├── attack_flow.py         # Attack visualization
│   ├── parallel_scanner.py    # Multi-threading
│   ├── business_rules.py      # Custom rules engine
│   └── executable_graphs.py   # Attack chain execution
│
├── output/
│   ├── formatter.py           # Terminal formatting
│   ├── reporter.py            # Report generation
│   └── ascii_art.py           # ASCII visualizations
│
└── tests/
    ├── test_agents.py
    ├── test_engines.py
    └── test_cli.py
```

## Scan Workflow

```
Input URL
  ↓
[ReconAgent] Crawl target
  ↓
[RoleSimulator] Create isolated sessions (User/Admin/Guest)
  ↓
[LogicReasoner] LLM-powered business logic analysis
  ↓
[ValidatorExploiter] Generate and validate PoCs
  ↓
[TriageReporter] Deduplicate, calculate CVSS, map OWASP/CWE
  ↓
[Output] Terminal display + Report export
```

## Ethical Notice

⚠️ **IMPORTANT**: This tool is designed for authorized security testing ONLY.

- You must have explicit written permission from the system owner
- Unauthorized access to computer systems is ILLEGAL
- Violations may result in criminal charges
- The developers assume no liability for misuse

## Requirements

- Python 3.9+
- Playwright (for browser automation)
- LLM API access (Grok, Claude, or OpenAI)
- 4+ GB RAM recommended
- Internet connection

## Troubleshooting

### "Connection refused" error
- Ensure target URL is accessible
- Check firewall/proxy settings
- Try with `--timeout 600` for slow targets

### "LLM API error"
- Verify LLM_API_KEY in .env
- Check API quota and rate limits
- Try different LLM provider

### "Playwright error"
- Run `playwright install` to download browsers
- Check for browser compatibility

## Support

For issues, questions, or feature requests:
1. Check the documentation
2. Review example configurations
3. Run with `--verbose` for debugging
4. Check logs in `vigorys.log`

## License

MIT License - See LICENSE file for details

---

**Vigorys Nuclear Edition v2.0** - The most powerful CLI tool for Business Logic Vulnerability detection
