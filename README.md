# DevOps Portfolio – Bibliotheksverwaltung

Eine webbasierte Bibliotheksverwaltung zur Verwaltung von Büchern, Exemplaren, Mitgliedern sowie Ausleihen und Rückgaben.

Das Projekt entsteht im Rahmen meines Bachelorstudiums im Modul **CDS212: Versionsverwaltung, Container, CI/CD, Cloud und Monitoring**.

Als leitende Bibliothekarin habe ich einen persönlichen Bezug zum fachlichen Thema und verbinde mit diesem Projekt meinen beruflichen Alltag mit meinen aktuellen Erfahrungen in **Softwareentwicklung und DevOps**.

## Voraussetzungen

- Python 3.12
- Git
- Docker
- Docker Compose

Für die weiteren DevOps-Komponenten werden zusätzlich benötigt:

- Terraform
- kind
- kubectl
- Prometheus
- Grafana
- Trivy

## Installation

Repository klonen:

    git clone git@github.com:DST81/devops-portfolio.git
    cd devops-portfolio

Virtuelle Umgebung erstellen und aktivieren:

    python3.12 -m venv .venv
    source .venv/bin/activate

Abhängigkeiten installieren:

    pip install -r requirements.txt

## Nutzung

Die Anwendung kann während der Entwicklung lokal mit Flask gestartet werden:

    flask --app src.app run

Anschließend ist die Anwendung standardmäßig unter `http://127.0.0.1:5000` erreichbar.

### Mit Docker

Die Anwendung kann alternativ als Container gestartet werden:

    docker compose up --build

Dadurch werden die für die Anwendung benötigten Container erstellt und gestartet.

## Fachlicher Umfang

Die Bibliotheksverwaltung bildet zentrale Abläufe einer Bibliothek ab.

Geplant sind unter anderem:

- 📚 Verwaltung von Büchern
- 📖 Verwaltung einzelner Exemplare
- 👤 Verwaltung von Mitgliedern
- ↗️ Erfassung von Ausleihen
- ↩️ Bearbeitung von Rückgaben
- 🔎 Anzeige der Verfügbarkeit
- ⏰ Erkennung überfälliger Ausleihen

Ein besonderer Schwerpunkt liegt auf den **Beziehungen zwischen den verschiedenen Entitäten** und den Zuständen eines Exemplars:

    verfügbar → ausgeliehen → überfällig

## REST-API

Die Anwendung stellt eine REST-API zur Verfügung, über die die Daten der Bibliotheksverwaltung verarbeitet werden können.

Beispiele für geplante Ressourcen:

    /books
    /books/{id}

    /copies
    /copies/{id}

    /members
    /members/{id}

    /loans
    /loans/{id}

Die konkreten Endpunkte und verfügbaren HTTP-Methoden werden im Laufe der Entwicklung dokumentiert.

## Technologie-Stack

| Bereich | Technologie | Begründung |
| --- | --- | --- |
| Sprache | Python 3.12 / Flask |  kleine Lernkurve |
| Container | Docker / Docker Compose | Industriestandard |
| CI/CD | GitHub Actions | Kostenlos für öffentliche Repositories, keine zusätzliche Infrastruktur |
| Cloud | Render (Free Tier) | Ohne Kreditkarte nutzbar |
| IaC | Terraform + lokaler Docker-Provider | Echte Terraform-Konzepte ohne Cloud-Kosten |
| Kubernetes | kind | Läuft lokal auf dem Notebook, kein externes Cluster nötig |
| Monitoring | Prometheus / Grafana | Etablierter Monitoring-Stack |
| Sicherheit | Trivy | Image- und Dependency-Scanning mit einem Werkzeug |

## DevOps

Der Schwerpunkt des Projekts liegt nicht nur auf der Entwicklung der Anwendung, sondern auf der gesamten **DevOps-Kette**.

    Code
      ↓
    Git / GitHub
      ↓
    GitHub Actions
      ↓
    Tests & Security Scanning
      ↓
    Docker Image
      ↓
    Container / Cloud
      ↓
    Kubernetes (kind)
      ↓
    Monitoring
      ↓
    Prometheus + Grafana

Die einzelnen Schritte sollen möglichst **automatisiert, reproduzierbar und nachvollziehbar** umgesetzt werden.

### CI/CD

GitHub Actions übernimmt die Automatisierung der Entwicklungs- und Bereitstellungsprozesse.

Geplante Schritte der Pipeline:

- Code prüfen
- Tests ausführen
- Abhängigkeiten prüfen
- Docker Image bauen
- Security Scan mit Trivy durchführen
- Anwendung bzw. Container bereitstellen

## Infrastructure as Code

Für die Infrastruktur wird **Terraform** eingesetzt.

Da für das Projekt keine kostenpflichtige Cloud-Infrastruktur notwendig sein soll, wird Terraform mit einem **lokalen Docker-Provider** verwendet.

So können Infrastructure-as-Code-Konzepte praktisch umgesetzt werden, ohne zusätzliche Cloud-Kosten zu verursachen.

## Kubernetes

Für die lokale Arbeit mit Kubernetes wird **kind (Kubernetes in Docker)** verwendet.

Dadurch kann ein Kubernetes-Cluster direkt auf dem eigenen Notebook betrieben werden, ohne einen externen Cluster bereitstellen zu müssen.

## Monitoring

Die Anwendung soll mit **Prometheus** und **Grafana** überwacht werden.

Prometheus übernimmt dabei die Sammlung von Metriken, während Grafana zur Visualisierung und Auswertung verwendet wird.

Geplant sind unter anderem Metriken zur Verfügbarkeit und zum Verhalten der Anwendung.

## Sicherheit

Für das Security Scanning wird **Trivy** eingesetzt.

Dabei sollen sowohl Container-Images als auch Python-Abhängigkeiten auf bekannte Schwachstellen überprüft werden.

Die Security-Prüfungen sollen in die CI/CD-Pipeline integriert werden.

## Cloud

Für das Deployment wird **Render** im Free Tier verwendet.

Ziel ist es, die Anwendung ohne zusätzliche kostenpflichtige Infrastruktur öffentlich bereitzustellen und dabei die zuvor aufgebaute CI/CD-Pipeline zu nutzen.

## Projektstruktur

Die Projektstruktur wird im Laufe der Entwicklung erweitert.

Geplant ist beispielsweise:

    devops-portfolio/
    ├── README.md
    ├── .gitignore
    ├── LICENSE
    ├── requirements.txt
    ├── Dockerfile
    ├── compose.yaml
    │
    ├── src/
    │   ├── app.py
    │   ├── routes/
    │   ├── models/
    │   └── ...
    │
    ├── tests/
    │   └── ...
    │
    ├── terraform/
    │   └── ...
    │
    ├── kubernetes/
    │   └── ...
    │
    └── .github/
        └── workflows/
            └── ...

## Lernziele

Mit diesem Projekt möchte ich praktische Erfahrungen in folgenden Bereichen sammeln:

- Versionsverwaltung mit Git und GitHub
- Entwicklung einer REST-API mit Python und Flask
- Containerisierung mit Docker
- Automatisierung mit GitHub Actions
- Deployment in einer Cloud-Umgebung
- Infrastructure as Code mit Terraform
- Kubernetes mit kind
- Monitoring mit Prometheus und Grafana
- Security Scanning mit Trivy

Dabei steht nicht nur das fertige Produkt im Mittelpunkt, sondern auch der **Lernprozess und das Verständnis der einzelnen DevOps-Komponenten**.

## Über das Projekt

Dieses Projekt verbindet meine beiden aktuellen Schwerpunkte:

**Bibliothek × IT / DevOps**

Durch meinen beruflichen Hintergrund als leitende Bibliothekarin kann ich die fachlichen Anforderungen aus einer praktischen Perspektive betrachten. Gleichzeitig nutze ich das Projekt, um neue Technologien kennenzulernen und die verschiedenen Bausteine einer modernen DevOps-Kette praktisch anzuwenden.

## Lizenz

Veröffentlicht unter der MIT-Lizenz.

Siehe [LICENSE](LICENSE) für weitere Informationen.
