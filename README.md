# 🔐 Vygoris Production - Real Security Scanner for Bug Bounty

**Vygoris Production** é uma ferramenta CLI de segurança de classe empresarial para Bug Bounty, desenvolvida para realizar exploração real, gerar Proof of Concepts verificados e integrar com Burp Suite.

## ✨ Características

### 🎯 Exploração Real
- ✅ HTTP requests reais com Playwright
- ✅ Payloads reais para SQL Injection, XSS, IDOR, Auth Bypass
- ✅ Captura de evidências e dados
- ✅ Screenshots e análise de DOM

### 🛡️ Zero False Positives
- ✅ Validação multi-check para cada vulnerabilidade
- ✅ Confirmação de exploração real
- ✅ Análise de resposta e timing
- ✅ Detecção de estado inconsistente

### 📊 Relatórios Profissionais
- ✅ Burp Suite XML export
- ✅ HackerOne format
- ✅ Bugcrowd format
- ✅ Intigriti format
- ✅ Markdown reports

### 🔗 Integração
- ✅ Burp Suite API integration
- ✅ Multi-platform export
- ✅ CVSS scoring
- ✅ Remediation suggestions

## 🚀 Instalação

```bash
# Clone o repositório
git clone https://github.com/shamanORc/Vygoris.git
cd Vygoris

# Instale as dependências
pip install -r requirements.txt

# Instale browsers Playwright
playwright install
```

## 📖 Uso

### Scan básico
```bash
python vygoris_cli.py https://example.com
```

### Exportar para HackerOne
```bash
python vygoris_cli.py https://example.com --format hackerone
```

### Exportar para Burp Suite
```bash
python vygoris_cli.py https://example.com --format burp
```

### Exportar todos os formatos
```bash
python vygoris_cli.py https://example.com --format all
```

## 🔍 Detecções Suportadas

| Vulnerabilidade | Tipo | CVSS | Status |
|---|---|---|---|
| SQL Injection | CRITICAL | 9.8 | ✅ |
| Cross-Site Scripting (XSS) | HIGH | 7.1 | ✅ |
| Insecure Direct Object Reference (IDOR) | HIGH | 7.5 | ✅ |
| Authentication Bypass | CRITICAL | 9.9 | ✅ |
| Race Condition | MEDIUM | 5.3 | ✅ |
| Business Logic Bypass | HIGH | 7.3 | ✅ |

## 📁 Estrutura do Projeto

```
vygoris-production/
├── real_http_client.py      # Cliente HTTP real com Playwright
├── payload_injector.py      # Payloads reais de exploração
├── poc_generator.py         # Gerador de PoC com evidências
├── burp_integration.py      # Integração com Burp Suite
├── bug_bounty_formats.py    # Formatos de plataformas
├── validation_engine.py     # Validação e zero false positives
├── vygoris_cli.py          # CLI principal
├── requirements.txt         # Dependências Python
└── README.md               # Este arquivo
```

## 🔧 Configuração

### Variáveis de Ambiente

```bash
# Burp Suite API
export BURP_URL=http://localhost:8080

# Timeout de requisição
export REQUEST_TIMEOUT=30

# Modo debug
export DEBUG=1
```

## 🧪 Exemplos

### Exemplo 1: Scan completo com export
```bash
python vygoris_cli.py https://pagardasmei.com.br --format all
```

Gera:
- `vygoris_report_*.json` - Relatório JSON
- `vygoris_burp_*.xml` - Burp Suite XML
- `vygoris_h1_*.json` - HackerOne format
- `vygoris_bugcrowd_*.json` - Bugcrowd format
- `vygoris_intigriti_*.json` - Intigriti format
- `vygoris_report_*.md` - Markdown report

## 🛠️ Desenvolvimento

### Adicionar novo tipo de validação

```python
from validation_engine import ValidationEngine

# Adicione método estático
@staticmethod
def validate_custom_vuln(data: str) -> Tuple[bool, Dict]:
    evidence = {"checks_passed": 0}
    # Implementar lógica
    return is_valid, evidence
```

### Adicionar novo payload

```python
from payload_injector import PayloadInjector

# Adicione ao dicionário de payloads
CUSTOM_PAYLOADS = [
    "payload1",
    "payload2"
]
```

## 📋 Checklist de Segurança

- [ ] Testar em ambiente autorizado
- [ ] Obter permissão escrita do proprietário
- [ ] Usar VPN/proxy se necessário
- [ ] Documentar todas as descobertas
- [ ] Seguir responsabilidade disclosure
- [ ] Respeitar rate limits

## 🐛 Troubleshooting

### Erro: "Playwright browser not found"
```bash
playwright install
```

### Erro: "Connection timeout"
```bash
python vygoris_cli.py https://example.com --timeout 60
```

### Erro: "Invalid URL"
```bash
# Use URL completa com protocolo
python vygoris_cli.py https://example.com
```

## 📝 Licença

Proprietary - Uso exclusivo para Bug Bounty autorizado

## 👨‍💻 Autor

Vygoris Team - Security Research

## 🤝 Contribuições

Para contribuições, abra uma issue ou pull request.

## 📞 Suporte

Para suporte, abra uma issue no repositório.

---

**⚠️ AVISO LEGAL:** Esta ferramenta é destinada apenas para testes de segurança autorizados. Uso não autorizado é ilegal.
