📄 Funktion
Zur direkten Verwendung der finalen XML-Dateien wurde ein n8n Workflow implementiert, der alle XML-Dateien empfängt und sie an Connectoren der gewünschten Zielsysteme wie Enventa ERP o.ä. weitergibt.

🚀 Verwendung
Nach dem Klick auf „Send XML“ werden die XML-Dateien per POST an einen dedizierten API-Endpunkt gesendet, der in n8n eingerichtet wurde:

POST http://localhost:5678/webhook-test/708d4bf7-7a85-4e34-b6d9-973a8086721c

Der Webhook-Endpunkt lauscht (wenn der n8n-Workflow deployed ist) auf eingehende XML-Dateien im Request Body.

✅ Voraussetzungen
- Docker installiert (Unter Windows ist WSL erforderlich)
- n8n installiert (siehe offizielle Doku):
  https://docs.n8n.io/hosting/installation/docker/#prerequisites
- Laufwerk ist im Docker verfügbar (gemountet)

🐳 Docker-Befehl mit Mount
Zum Starten von n8n mit eingebundenem lokalen Ordner:

docker run -it --rm --name n8n -p 5678:5678 \
  -v n8n_data:/home/node/.n8n \
  -v "C:\examplestruct\examplefolder:/data/example" \
  docker.n8n.io/n8nio/n8n

📂 Verzeichnisstruktur
- Lokaler Ordner: C:\examplestruct\examplefolder
- Im Container verfügbar unter: /data/example

