# Workflow: Client Research → PDF

## Objective
Przeszukaj rynek w wybranej branży/lokalizacji i wygeneruj PDF z listą potencjalnych klientów, segmentami i priorytetami.

## Required Inputs
- Branża / nisze (np. beauty, fashion, home decor)
- Region startowy (np. Rzeszów, Kraków, Polska ogólnie)
- Typ usługi do sprzedania (np. fotografia produktowa, video, content)

## Required Tools
- `tools/generate_client_list_pdf.py`

## Steps

1. **Research rynku** – WebSearch dla każdego segmentu:
   - `[branża] sklepy internetowe ecommerce [miasto] [rok]`
   - `polskie marki [niszy] lista sklep online`
   - `firmy [branża] [miasto] producent`

2. **Zaktualizuj dane w toolie** – Edytuj `CLIENT_DATA` w `tools/generate_client_list_pdf.py`:
   - Dodaj/usuń segmenty (`segments[]`)
   - Zaktualizuj listę klientów (`clients[]`)
   - Ustaw priorytety: `WYSOKI / ŚREDNI / NISKI`
   - Zaktualizuj wskazówki strategiczne (`tips[]`)

3. **Wygeneruj PDF**:
   ```bash
   python3 tools/generate_client_list_pdf.py --output .tmp/potencjalni_klienci.pdf
   ```

4. **Otwórz i sprawdź**:
   ```bash
   open .tmp/potencjalni_klienci.pdf
   ```

## Expected Output
PDF z:
- Tabelą podsumowującą (łączna liczba klientów, priorytety)
- Segmentami rynku z kolorową nagłówkami
- Tabelami klientów z kolumnami: Firma, Kategoria, Lokalizacja, Dlaczego warto, Priorytet
- Wskazówkami strategicznymi na końcu

## Error Handling
- Jeśli `reportlab` nie jest zainstalowany: `pip3 install reportlab`
- Jeśli .tmp nie istnieje: `mkdir -p .tmp`
- Jeśli znaki polskie nie renderują się poprawnie → reportlab 4.x obsługuje UTF-8 natywnie, bez dodatkowych fontów

## Notes
- Dane klientów są hardcodowane w `CLIENT_DATA` w toolie – aktualizuj je ręcznie po researchu
- PDF trafia do `.tmp/` – jest plikiem tymczasowym, można regenerować w każdej chwili
- Priorytety: WYSOKI = kontaktuj się w pierwszej kolejności, ŚREDNI = drugi etap, NISKI = kiedy będzie portfelo
- W przyszłości można rozszerzyć tool o scraping Google Maps / LinkedIn dla automatycznego zbierania firm

## Wykonanie (2026-03-02)
- Zbadano 6 segmentów rynku: Rzeszów lokalne, Fashion PL, Beauty PL, Biżuteria PL, Home Decor PL, E-commerce PL
- Zidentyfikowano ~50 potencjalnych klientów
- Wygenerowano: `.tmp/potencjalni_klienci.pdf`
