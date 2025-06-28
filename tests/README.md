# 🔄 Update und Test Anleitung - PrestaShop MCP Server

## Schnelle Update-Anleitung für bestehende Installationen

### Voraussetzungen
- Bestehende PrestaShop MCP Installation 
- Aktive virtuelle Python-Umgebung
- Zugriff auf das GitHub Repository

### 1. Server stoppen und Updates laden

```powershell
# 1. Aktuellen MCP Server stoppen
# -> Schließe Claude Desktop oder stoppe den Server dort

# 2. Repository mit neuen Bugfixes aktualisieren
git pull origin main

# 3. Aktualisierte Version installieren
pip install -e .

# 4. Installation verifizieren
python -c "import prestashop_mcp; print('✅ Neue Version erfolgreich installiert')"
```

### 2. API-Verbindung testen

```powershell
# Direkte API-Verbindung testen
python -c "
import asyncio
from prestashop_mcp.config import Config
from prestashop_mcp.prestashop_client import PrestaShopClient

async def test():
    config = Config()
    async with PrestaShopClient(config) as client:
        result = await client.get_shop_info()
        print('✅ API-Verbindung erfolgreich:', result.get('shop_info', {}))

asyncio.run(test())
"
```

### 3. Claude Desktop Konfiguration

Deine bestehende `~/.claude_desktop_config.json` bleibt unverändert:

```json
{
  "mcpServers": {
    "prestashop": {
      "command": "C:\\Users\\{Username}\\GitHub\\prestashop-mcp\\venv_prestashop\\Scripts\\python.exe",
      "args": ["-m", "prestashop_mcp.prestashop_mcp_server"],
      "cwd": "C:\\Users\\{Username}\\GitHub\\prestashop-mcp",
      "env": {
        "PRESTASHOP_SHOP_URL": "https://shop.ginos.cloud",
        "PRESTASHOP_API_KEY": "XVM6ZNX6IQI42ILGXRXFF62FZCGE3X7N"
      }
    }
  }
}
```

**Wichtig**: Starte Claude Desktop neu, um die neue Version zu aktivieren.

## 🧪 Funktionalitätstests

### Test 1: Produkterstellung mit Backend-Sichtbarkeit

```
Frage in Claude Desktop:
"Erstelle ein Testprodukt 'Test Widget 2025' für 29.99€ in Kategorie 2"

Erwartetes Ergebnis:
✅ Produkt wird erfolgreich erstellt
✅ Produkt ist sofort im PrestaShop Backend sichtbar
✅ Alle Felder sind korrekt initialisiert
```

### Test 2: Stock-Update ohne XML-Parsing-Fehler

```
Frage in Claude Desktop:
"Aktualisiere die Lagermenge des letzten Produkts auf 50 Stück"

Erwartetes Ergebnis:
✅ Stock-Update erfolgt ohne Fehler
✅ Keine XML-Parsing-Warnungen in den Logs
✅ Neue Lagermenge ist korrekt gesetzt
```

### Test 3: Kategorie-Erstellung ohne PHP-Warnungen

```
Frage in Claude Desktop:
"Erstelle eine neue Kategorie 'Test Kategorie 2025' mit Beschreibung"

Erwartetes Ergebnis:
✅ Kategorie wird erfolgreich erstellt
✅ Keine PHP-Warnungen bezüglich undefined array keys
✅ Alle mehrsprachigen Felder korrekt initialisiert
```

### Test 4: API-Authentifizierung direkt

```bash
# Direkte API-Abfrage mit curl
curl -u "XVM6ZNX6IQI42ILGXRXFF62FZCGE3X7N:" https://shop.ginos.cloud/api/configurations?output_format=JSON

# Erwartetes Ergebnis:
# ✅ JSON-Response ohne Authentifizierungsfehler
# ✅ Konfigurationsdaten werden korrekt zurückgegeben
```

## 🔧 Behobene Kritische Probleme

### ✅ Fehlende Backend-Sichtbarkeit
- **Problem**: Produkte waren mit `state: 0` als Entwurf gespeichert
- **Fix**: Automatische `state: 1` Initialisierung für sofortige Backend-Sichtbarkeit

### ✅ XML-Parsing Fehler
- **Problem**: JSON wurde statt XML gesendet, falsche Content-Type Header
- **Fix**: Korrekte `application/xml; charset=UTF-8` Header und XML-Struktur

### ✅ Stock-Update Operationen
- **Problem**: Fehlerhafte XML-Generierung für `stock_available` Updates
- **Fix**: Vollständige und korrekte XML-Struktur für alle Stock-Operationen

### ✅ Mehrsprachige Feldinitialisierung  
- **Problem**: Undefined array key Warnungen bei mehrsprachigen Feldern
- **Fix**: Systematische Initialisierung aller verfügbaren Sprachen

## 🚀 Performance Verbesserungen

- **Robuste Error-Behandlung**: Verbesserte Fehlerbehandlung bei API-Requests
- **Debug-Logging**: Erweiterte XML-Request-Protokollierung für besseres Debugging
- **Vollständige Feldabdeckung**: Alle erforderlichen PrestaShop-Felder werden korrekt initialisiert
- **Optimierte Performance**: Effizientere mehrsprachige Feldbehandlung

## 📞 Support

Bei Problemen:
1. Überprüfe die API-Konfiguration in den Umgebungsvariablen
2. Teste die direkte API-Verbindung mit curl
3. Kontrolliere die Logs für detaillierte Fehlermeldungen
4. Stelle sicher, dass die PrestaShop API-Berechtigungen korrekt sind

---

**Version**: Bugfixes vom 28.06.2025  
**Status**: Production Ready ✅
