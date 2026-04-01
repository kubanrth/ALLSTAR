#!/usr/bin/env python3
"""
Tool: market_zestawy_prezentowe.py
Generates a PDF with Polish gift set market analysis (zestawy prezentowe).
Usage: python3 tools/market_zestawy_prezentowe.py --output .tmp/rynek_zestawy_prezentowe.pdf
"""

import argparse, os
from datetime import date
from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import cm
from reportlab.lib import colors
from reportlab.platypus import (
    SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle,
    HRFlowable, KeepTogether
)
from reportlab.lib.enums import TA_LEFT, TA_CENTER

# ─── DATA ─────────────────────────────────────────────────────────────────────

MARKET_DATA = {
    "meta": {
        "title": "Polski Rynek Zestawow Prezentowych",
        "subtitle": "Analiza firm sprzedajacych zestawy prezentowe — wlasne sklepy i Allegro",
        "date": str(date.today()),
    },
    "segments": [

        # ── 1. ZESTAWY SPOZYWCZE I DELIKATESOWE ───────────────────────────────
        {
            "name": "1. ZESTAWY SPOZYWCZE I DELIKATESOWE",
            "color": "#3B2A1A",
            "intro": (
                "Najszersza i najbardziej dojrzala kategoria rynku. Firmy oferuja kosze z polskimi "
                "przetworami, delikatesami, ekologicznymi produktami regionalnymi. Konkurencja wysoka, "
                "ale segmentacja (eko, premium, regionalne) pozwala sie wyrozniac. Sezonowosc: "
                "Swieta Bozego Narodzenia i Wielkanoc to szczyty sprzedazy."
            ),
            "clients": [
                ("Vivat",            "Kosze delikatesowe",     "Polska",   "vivat.pl",                    "30 lat na rynku. Ekskluzywne kosze z delikatesami, wlasna marka. Dostawa w 3 dni. Klienci VIP ze swiata polityki i kultury.", "OBA"),
                ("Fabryka Prezentow","Kosze / Boxy okolicz.",  "Polska",   "fabryka-prezentow.com",        "Kosze swiateczne, okolicznosciowe, firmowe i delikatesowe. Szeroka oferta B2C i B2B.", "OBA"),
                ("Polski Spichlerz", "Kosze polskie produkty", "Polska",   "polskispichlerz.pl",           "Ekologiczne polskie smakołyki, przetwory domowe. Estetyczne opakowania, personalizacja.", "WLASNA"),
                ("Kosz na Prezent",  "Kosze eko / regionalne", "Plock/PL", "kosznaprezent.pl",             "Ekologiczne, regionalne produkty. Tradycyjne metody, bez konserwantow. Kosze wiklinowe.", "WLASNA"),
                ("Lubelski Stol",    "Kosze regionalne",       "Lublin",   "lubelskistol.pl",              "Lokalne produkty od producentow z regionu lubelskiego. Reczne pakowanie w wikline i pudelka kraft.", "WLASNA"),
                ("Stolica Sliwki",   "Zestawy ze sliwka",      "Polska",   "stolicasliwki.pl",             "Specjalistyczne zestawy z produktami ze sliwki. Nisza regionalna.", "WLASNA"),
                ("Bacowka",          "Kosze gorskie produkty", "Polska",   "sklep.bacowkatowary.pl",        "Produkty gorskie i oscypki w eleganckich opakowaniach prezentowych.", "OBA"),
                ("Symbol Smaku",     "Przetwory / Zestawy",    "Polska",   "symbolsmaku.pl",               "Naturalny producent przetworow. Zestawy dla firm i klientow indywidualnych. B2B i B2C.", "WLASNA"),
                ("Prezentowapaka",   "Paczki upominkowe",      "Polska",   "prezentowapaka.pl",            "Paczki i zestawy upominkowe z szeroka oferta dla kazdej okazji.", "WLASNA"),
            ],
        },

        # ── 2. BOXY PREZENTOWE B2C ─────────────────────────────────────────────
        {
            "name": "2. BOXY PREZENTOWE — SPRZEDAZ DETALICZNA (B2C)",
            "color": "#1A3C5E",
            "intro": (
                "Segment boxow prezentowych — gotowych zestawow pakowanych w estetyczne pudelka. "
                "Rosnacy trend zwlaszcza wsrod mlodszych konsumentow kupujacych online. Firmy czesto "
                "oferuja kreatory boxow pozwalajace klientowi skomponowac wlasny zestaw. "
                "Duza aktywnosc na Allegro i Instagram."
            ),
            "clients": [
                ("NAPU",             "Gift boxy / szybka dost.", "Polska", "napu.pl",                     "Wyjatkowe prezenty z unikalnych produktow niedostepnych w sklepach. Dostawa w 24h. Gwarancja oryginalnosci.", "OBA"),
                ("kosze-prezentowe.pl","Boxy i kosze",           "Polska", "kosze-prezentowe.pl",          "Bogaty wybor boxow prezentowych — estetyczna i elegancka prezentacja prezentu.", "WLASNA"),
                ("Zestaw To!",       "Zestawy reczne",           "Polska", "zestawto.pl",                  "Recznie pakowane i dekorowane zestawy. Kosze wiklinowe, pudelka drewniane, kraft.", "WLASNA"),
                ("PREZENTtogo",      "Boxy z kosmetykami/zdrow.","Polska", "prezenttogo.pl",               "Boxy z naturalnymi kosmetykami i zdrowymi przekaskami. Starannie skomponowane upominki.", "WLASNA"),
                ("GiftBox",          "Kreator boxow",            "Polska", "giftbox.sklep.pl",             "Specjalny kreator — klient projektuje wlasny box, wybiera zawartosc, dekoracje, dedykacje.", "WLASNA"),
                ("Kreatywnylas",     "Zestawy personalizowane",  "Polska", "kreatywnylas.pl",              "Eleganckie zestawy z personalizacja. Darmowa dostawa od 80 zl. Szeroki asortyment.", "WLASNA"),
                ("MojaGwiazdka",     "Kosze / Zestawy swiatecz.","Polska", "mojagwiazdka.pl",              "15 lat doswiadczenia. Producent koszy premium. Realizuje zamowienia dla największych firm w Polsce.", "OBA"),
                ("Ekoloco",          "Premium boxy swiateczne",  "Polska", "ekoloco.pl",                   "Premium zestawy swiateczne. Naturalne konfiturze, reczna czekolada, aromatyczne herbaty. Takze hurt.", "WLASNA"),
            ],
        },

        # ── 3. ZESTAWY FIRMOWE B2B ─────────────────────────────────────────────
        {
            "name": "3. ZESTAWY PREZENTOWE DLA FIRM (B2B)",
            "color": "#1A4A2A",
            "intro": (
                "Najbardziej dochodowy segment. Firmy zamawiaja zestawy dla pracownikow, klientow "
                "i partnerow biznesowych — czesto z logo, personalizacja i hurtem. Szczyty: koniec roku "
                "(Swieta Bozego Narodzenia), Wielkanoc, Dzien Kobiet. Marze wyzsze niz B2C, "
                "ale wymaga dluzszego cyklu sprzedazy i ofertowania."
            ),
            "clients": [
                ("Manufaktura Podarunkow","Eko zestawy z logo",  "Polska", "manufakturapodarunkow.pl",     "Eleganckie zestawy z logo firmy. Wloskie wina + polskie produkty z rodzinnych manufaktur. Gwarancja dostawy.", "WLASNA"),
                ("Gift Factory",         "B2B kolekcje premium","Polska", "giftfactory.com.pl",            "6 kolekcji prezentow biznesowych: Basic, Made in Poland, Around the World, Merry Christmas, Easter, 4 Kids.", "WLASNA"),
                ("Gift Box Factory",     "Boxy firmowe duze wol.","Polska","giftboxfactory.pl",            "Ponad 50 000 boxow dla firm. Ceny od 49 PLN netto/szt. Elegancja, jakosc, personalizacja.", "WLASNA"),
                ("Have a Nice BOX",      "Zestawy biznesowe",    "Polska", "hnbx.pl",                      "Staly rabat -10% dla firm. Cennik hurtowy od 3 000 PLN netto. Gotowe zestawy robiace wrazenie.", "WLASNA"),
                ("OpenGift",             "Giftboxy firmowe",     "Polska", "opengift.pl",                  "Kompleksowa usluga: koncepcja, projekt, dostawa gotowych zestawow. B2B.", "WLASNA"),
                ("BiznesowePrezenty",    "Prezenty B2B",         "Polska", "biznesoweprezenty.pl",          "Prezenty dla klientow i partnerow biznesowych. Personalizacja i szeroki asortyment.", "WLASNA"),
                ("ePudelko",             "Zestawy dla kontrah.", "Polska", "epudelko.pl",                   "Eleganckie zestawy dla klientow, kontrahentow i pracownikow. Hurt dostepny.", "WLASNA"),
                ("GiftHome",             "Zestawy firmowe",      "Polska", "gifthome.pl",                   "Upominki i zestawy prezentowe dla firm na rozne okazje biznesowe.", "WLASNA"),
                ("Robimy Prezenty",      "Kosze firmowe",        "Polska", "robimyprezenty.pl",             "Ponad dekada doswiadczenia. Wyjatkowe kosze dla firm — najwyzsza jakosc pakowania.", "WLASNA"),
                ("Polski Podarek",       "Personalizowane B2B",  "Polska", "polskipodarek.pl",              "Personalizacja przez grawer LOGO, nadruki na obwolutach, wlasne etykiety. B2B i B2C.", "WLASNA"),
                ("PolskiPrezent.pl",     "Statuetki / Zestawy",  "Polska", "polskiprezent.pl",              "Personalizowane statuetki LED, skrzynki z grawerem, zestawy dla firm. Indywidualne projekty.", "WLASNA"),
                ("BAS Kreacja",          "Gift boxy / Welcome",  "Polska", "baskreacja.pl",                 "Gift boxy, welcome packi i spersonalizowane zestawy. Projektowanie i produkcja.", "WLASNA"),
                ("Giftboxy.pl",          "Giftboxy firmowe",     "Polska", "giftboxy.pl",                   "Firmowe giftboxy — prezenty biznesowe, welcome packi, beauty boxy.", "WLASNA"),
                ("Betlewski Hurt",       "Hurtownia galanterii", "Polska", "hurt.betlewski.com",            "Hurtownia galanterii i dodatkow — zestawy prezentowe w ofercie hurt B2B.", "WLASNA"),
                ("Domarex Hurt",         "Hurtownia tekstylna",  "Polska", "domarexhurt.pl",                "Hurtownia tekstyliow domowych i ogrodowych — zestawy prezentowe w segmencie B2B.", "WLASNA"),
            ],
        },

        # ── 4. BEAUTY BOXY I KOSMETYCZNE ───────────────────────────────────────
        {
            "name": "4. BEAUTY BOXY I ZESTAWY KOSMETYCZNE",
            "color": "#5E1A3C",
            "intro": (
                "Dynamicznie rozwijajacy sie segment. Boxy z kosmetykami sa popularne jako prezenty "
                "dla kobiet. Marki kosmetyczne sprzedaja zestawy sezonowo (Swieta, Walentynki, "
                "Dzien Matki). Mocna obecnosc na Allegro i platformach subskrypcyjnych. "
                "Boxy discovery i subskrypcyjne to osobna nisza."
            ),
            "clients": [
                ("ECOSPA",           "Naturalne kosmetyki",    "Polska",   "ecospa.pl",                    "Zestawy dla Niej, Niego, Nastolatki, Mamy. Naturalna pielegnacja w estetycznych kompozycjach.", "WLASNA"),
                ("Pure Beauty",      "Beauty boxy",            "Polska",   "purebeauty.pl",                "Gotowe boxy z kosmetykami dla kobiet. Estetyczna prezentacja, dobrane produkty.", "WLASNA"),
                ("Organique",        "Zestawy kosmetyczne",    "Polska",   "organique.pl",                 "Kolorowe i pachnace zestawy dla Niej i Niego. Takze B2B — personalizowane zestawy z logo marki.", "OBA"),
                ("BasicLab",         "Dermokosmetyki",         "Polska",   "basiclab.shop",                "Specjalistyczne dermokosmetyki. Zestawy prezentowe ukierunkowane na konkretne problemy skorne.", "WLASNA"),
                ("Notino",           "Parfumy / Beauty boxy",  "Polska",   "notino.pl",                    "Discovery beauty box — miesieczna subskrypcja z kosmetykami swiatowych marek. Duza skala.", "OBA"),
                ("Alkmie",           "Beauty boxy z logo",     "Polska",   "alkmie.com",                   "Eleganckie pudelka prezentowe beauty z mozliwoscia druku logo. B2B i B2C.", "WLASNA"),
                ("Minti Shop",       "Zestawy kosmetyczne",    "Polska",   "mintishop.pl",                 "Zestawy dla kobiet, mezczyzn i dzieci: twarz, cialo, wlosy, paznokcie, kapiel.", "OBA"),
                ("Floslek",          "Kosmetyki / Beauty box", "Polska",   "floslek.pl",                   "Polski producent kosmetykow. Beauty boxy i zestawy prezentowe wlasnej marki.", "WLASNA"),
            ],
        },

        # ── 5. ZESTAWY DLA DZIECI I BABY ───────────────────────────────────────
        {
            "name": "5. ZESTAWY DLA DZIECI — BABY SHOWER / CHRZEST / KOMUNIE",
            "color": "#2A4A5E",
            "intro": (
                "Segment okazjonalny z mocna sezonowosc (wiosna — komunia i chrzest, caly rok — baby shower). "
                "Produkty laczace praktycznosc z estetyka: tekstylia, zabawki, kosmetyki dla niemowlat, "
                "pamiatki. Personalizacja jest tu kluczowa — imie dziecka, data urodzenia. "
                "Emocjonalny charakter zakupow uzasadnia wyzsza cene."
            ),
            "clients": [
                ("Baby Box Polska",  "Boxy baby shower/chrzest","Polska", "babyboxpolska.pl",              "Gotowe zestawy na baby shower, narodziny, chrzest, komunia i urodziny. Estetyczne pudelka.", "WLASNA"),
                ("Bio-Pure",         "Zestawy eko dla dzieci", "Polska",  "bio-pure.pl",                   "Bezpieczne dla niemowlat produkty eko. Pudelka serduszka lub drewniane z logo Bio Pure.", "WLASNA"),
                ("Niebieski Stolik", "Pamiatki chrzestne",     "Polska",  "niebieskistolik.pl",            "Eleganckie pamiatki chrzestne i zestawy w pudelkach — rozaniec, aksamitna sakiewka, karta.", "WLASNA"),
                ("Bimbus",           "Baby shower / Chrzest",  "Polska",  "bimbus.com.pl",                 "Wspaniale prezenty na chrzest, baby shower, Dzien Dziecka, urodziny i komunia.", "WLASNA"),
                ("Planeta Dzieci",   "Zestawy na chrzest",     "Polska",  "planetadzieci.pl",              "Zestawy prezentowe na Chrzest Swiety — praktyczne, edukacyjne i sentymentalne podarunki.", "OBA"),
                ("LiLi Shop",        "Zestawy dla dzieci",     "Polska",  "shoplili.pl",                   "Zestawy prezentowe dla dziewczynek na baby shower i chrzest. Popularne wsrod przyszlych mam.", "WLASNA"),
                ("Prezenty na Chrzest","Pamiatki chrzestne",   "Polska",  "prezentynachrzest.com",         "Specjalizacja: prezenty na chrzest — dedykowane propozycje dla chlopcow i dziewczynek.", "WLASNA"),
            ],
        },

        # ── 6. ZESTAWY Z ALKOHOLEM ──────────────────────────────────────────────
        {
            "name": "6. ZESTAWY PREZENTOWE Z ALKOHOLEM",
            "color": "#4A1A1A",
            "intro": (
                "Zestawy z alkoholem to segment premium, szczegolnie popularny jako prezenty firmowe "
                "i dla mezczyzn. Skrzynki z whisky, winami, zestawy degustacyjne. "
                "Wymaga koncesji na sprzedaz alkoholu. Sezonowosc: Swieta, Dzien Ojca, rocznice. "
                "Marze wysokie, klienci wydaja wiecej na upominek z alkoholem."
            ),
            "clients": [
                ("Sklep z Whisky",   "Zestawy whisky / wino",  "Polska",  "sklepzwhisky.pl",               "Staranne kompozycje z winami z renomowanych winnic i whisky. Eleganckie pudelka i skrzynki.", "WLASNA"),
                ("AlkoholNaPrezent", "Ekskluzywne alkohole",   "Polska",  "alkoholnaprezent.com",           "Ekskluzywne alkohole w ozdobnych butelkach, zestawy dla firm. Oryginalne prezenty.", "WLASNA"),
                ("Galeria Alkoholi", "Zestawy z alkoholem",    "Polska",  "galeriaalkoholi.pl",             "Wyjatkowe zestawy z alkoholem w estetycznych skrzynkach lub pudełkach. Szeroka oferta.", "OBA"),
                ("SingleMalt",       "Whisky na prezent",      "Polska",  "singlemalt.pl",                  "Whisky, upominki i skrzynki na alkohol dla milosnikow single malt.", "WLASNA"),
                ("Wino-sklep",       "Kosze z winem",          "Polska",  "wino-sklep.pl",                  "Kosze prezentowe z winami, whisky, wódkami premium, likierami i przekaskami degustacyjnymi.", "WLASNA"),
                ("Wina i Alkohole",  "Zestawy wino / spirits", "Polska",  "winaialkohole.pl",               "Sklep internetowy z winami i alkoholami swiata. Zestawy degustacyjne i kosze z akcesoriami.", "WLASNA"),
                ("Aleeks Alkohole",  "Whisky / Wódka premium", "Polska",  "aleeksalkohole.pl",              "Zestawy whisky ze szklankami, wódki premium. Kuratowane opcje upominkowe.", "OBA"),
            ],
        },

        # ── 7. ALLEGRO — OFICJALNE SKLEPY MAREK ────────────────────────────────
        {
            "name": "7. ALLEGRO — OFICJALNE SKLEPY I STREFA MAREK",
            "color": "#4A3A00",
            "intro": (
                "Allegro pozostaje dominujacym marketplace w Polsce. Wiele firm sprzedaje zestawy "
                "prezentowe rownoczesnie przez wlasne strony i Allegro. Strefa Marek Allegro skupia "
                "oficjalnych producentow. Kategoria zestawow prezentowych osiaga wzrost sprzedazy "
                "o 217% w sezonie swiatecznym. Super Sprzedawca to kluczowy status."
            ),
            "clients": [
                ("Green Touch (Allegro)","Kosze ekskluzywne",   "Polska",  "allegro.pl/uzytkownik/green-touch","Oficjalny sklep w Strefie Marek Allegro. Ekskluzywne kosze z rzemielniczymi czekoladami, herbatami, miodami.", "OBA"),
                ("Wawel (Allegro)",   "Slodycze / Zestawy",     "Krakow",  "allegro.pl/uzytkownik/wawel_slodycze","Oficjalny sklep producenta słodyczy Wawel w Strefie Marek Allegro. Zestawy swiateczne i okolicznosciowe.", "OBA"),
                ("Krupiec (Allegro)", "Miody / Zestawy",        "Polska",  "allegro.pl/uzytkownik/miodykrupiec","Oficjalny sklep Krupiec w Strefie Marek Allegro. Zestawy prezentowe z miodami.", "OBA"),
                ("Bacowka (Allegro)", "Produkty gorskie",        "Polska",  "allegro.pl",                    "Bacowka Towary aktywna na Allegro z produktami gorskimi w opakowaniach prezentowych.", "OBA"),
                ("Minti Shop (Allegro)","Kosmetyki / Zestawy",  "Polska",  "allegro.pl",                    "Minti Shop sprzedaje zestawy prezentowe kosmetyczne rowniez przez Allegro.", "OBA"),
                ("Planeta Dzieci (All.)","Zestawy dla dzieci",  "Polska",  "allegro.pl",                    "Zestawy na chrzest i urodziny dostepne takze na Allegro. Duza widocznosc.", "OBA"),
                ("Fabryka Prezentow (A.)","Kosze swiateczne",   "Polska",  "allegro.pl",                    "Fabryka Prezentow obecna na Allegro z szerokim asortymentem koszy okolicznosciowych.", "OBA"),
            ],
        },

    ],
    "tips": [
        "Szczyty sprzedazy: Swieta Bozego Narodzenia (styczen-grudzien), Wielkanoc, Dzien Matki (maj), Dzien Ojca (czerwiec), Walentynki — zacznij przygotowania 3 miesiace wczesniej.",
        "Segment B2B (prezenty firmowe) generuje wyzsze marze — firmy wydaja wiecej i zamawiaja hurtem. Priorytet: kontakt z dzialami HR i marketingu.",
        "Personalizacja (logo firmy, grawer, dedykacja, wlasna etykieta) to kluczowy wyroznik — klienci placa premium za spersonalizowany zestaw.",
        "Obecnosc na Allegro zwiekasza sprzedaz o 200%+ w sezonie. Rozwaiz model: wlasny sklep + Allegro jednoczesnie (omnikanal).",
        "Nisze z wysoka marga: zestawy z alkoholem (whisky, wino premium), beauty boxy z naturalnymi kosmetykami, zestawy eko z certyfikatami.",
        "Boxy dla dzieci (baby shower, chrzest) — silna sezonowosc wiosenna. Personalizacja imienia dziecka i daty urodzenia uzasadnia cene premium.",
        "Ekoloco, Bacowka, Lubelski Stol pokazuja model: regionalne produkty jako unikalny wyroznik. Wspolpraca z lokalnymi producentami buduje autentycznosc.",
        "Subskrypcyjne beauty boxy (Notino Discovery Box) to powtarzalny przychod — rozwaiz model subskrypcji w swojej kategorii.",
        "Fotografia produktowa ma kluczowe znaczenie — zestawy prezentowe to produkt wizualny. Inwestycja w profesjonalne zdjecia zwraca sie natychmiast.",
        "Sprawdz Allegro kategoria zestawy prezentowe (251902) — analizuj recenzje i pytania kupujacych, to zrodlo wiedzy o potrzebach rynku.",
        "Certyfikaty (eko, BIO, Made in Poland, Slow Food) zwiekszaja zaufanie i uzasadniaja wyzsze ceny — sprawdz wymagania na wczesnym etapie.",
    ],
}

# ─── CHANNEL CONFIG ────────────────────────────────────────────────────────────

CHANNEL_COLORS = {
    "OBA":    colors.HexColor("#1A3C8E"),   # both channels — blue
    "WLASNA": colors.HexColor("#1a7a1a"),   # own website — green
    "ALLEGRO": colors.HexColor("#c07000"),  # Allegro only — orange
}
CHANNEL_BG = {
    "OBA":    colors.HexColor("#eaf0ff"),
    "WLASNA": colors.HexColor("#eaf5ea"),
    "ALLEGRO": colors.HexColor("#fff8e0"),
}

# ─── PDF BUILDER ──────────────────────────────────────────────────────────────

def build_pdf(output_path: str):
    doc = SimpleDocTemplate(
        output_path, pagesize=A4,
        rightMargin=1.8*cm, leftMargin=1.8*cm,
        topMargin=1.8*cm, bottomMargin=1.8*cm,
        title=MARKET_DATA["meta"]["title"],
    )
    styles = getSampleStyleSheet()
    W = A4[0] - 3.6*cm

    s_title = ParagraphStyle("T", parent=styles["Title"], fontSize=18,
                              textColor=colors.HexColor("#1A1A2E"), spaceAfter=4,
                              fontName="Helvetica-Bold")
    s_sub   = ParagraphStyle("S", parent=styles["Normal"], fontSize=9,
                              textColor=colors.HexColor("#555555"), spaceAfter=3)
    s_sec   = ParagraphStyle("SEC", parent=styles["Normal"], fontSize=10,
                              textColor=colors.white, fontName="Helvetica-Bold",
                              spaceAfter=0, spaceBefore=0)
    s_intro = ParagraphStyle("I", parent=styles["Normal"], fontSize=8,
                              textColor=colors.HexColor("#444444"), leading=12, spaceAfter=6)
    s_body  = ParagraphStyle("B", parent=styles["Normal"], fontSize=7.5,
                              textColor=colors.HexColor("#333333"), leading=11)
    s_link  = ParagraphStyle("L", parent=styles["Normal"], fontSize=7.5,
                              textColor=colors.HexColor("#0057B8"), leading=11)
    s_tip   = ParagraphStyle("TP", parent=styles["Normal"], fontSize=8,
                              textColor=colors.HexColor("#1A3C5E"), leading=13,
                              leftIndent=8, spaceAfter=4)
    s_foot  = ParagraphStyle("F", parent=styles["Normal"], fontSize=7,
                              textColor=colors.HexColor("#aaaaaa"), alignment=TA_CENTER)
    s_ch    = {ch: ParagraphStyle(f"CH_{ch}", parent=s_body,
                                   textColor=CHANNEL_COLORS[ch], alignment=TA_CENTER,
                                   fontName="Helvetica-Bold")
               for ch in CHANNEL_COLORS}

    story = []
    meta = MARKET_DATA["meta"]

    # ── Cover ──
    story.append(Spacer(1, .5*cm))
    story.append(Paragraph(meta["title"], s_title))
    story.append(Paragraph(meta["subtitle"], s_sub))
    story.append(Paragraph(f"Data: {meta['date']}", s_sub))
    story.append(HRFlowable(width=W, thickness=2, color=colors.HexColor("#1A1A2E"), spaceAfter=12))

    # ── Stats banner ──
    total  = sum(len(s["clients"]) for s in MARKET_DATA["segments"])
    oba    = sum(1 for s in MARKET_DATA["segments"] for c in s["clients"] if c[5]=="OBA")
    wlasna = sum(1 for s in MARKET_DATA["segments"] for c in s["clients"] if c[5]=="WLASNA")
    segs   = len(MARKET_DATA["segments"])

    banner = Table([[
        Paragraph(f"<b>{total}</b>\nFirm lacznie", ParagraphStyle("bn", parent=s_body, alignment=TA_CENTER, fontSize=12, leading=16)),
        Paragraph(f"<b>{segs}</b>\nSegmentow rynku", ParagraphStyle("bn", parent=s_body, alignment=TA_CENTER, fontSize=12, leading=16)),
        Paragraph(f"<b>{oba}</b>\nOba kanaly", ParagraphStyle("bn", parent=s_body, alignment=TA_CENTER, fontSize=12, leading=16, textColor=CHANNEL_COLORS["OBA"])),
        Paragraph(f"<b>{wlasna}</b>\nTylko wlasna strona", ParagraphStyle("bn", parent=s_body, alignment=TA_CENTER, fontSize=12, leading=16, textColor=CHANNEL_COLORS["WLASNA"])),
    ]], colWidths=[W/4]*4)
    banner.setStyle(TableStyle([
        ("BACKGROUND",  (0,0),(-1,-1), colors.HexColor("#f0f4ff")),
        ("BOX",         (0,0),(-1,-1), 1, colors.HexColor("#cccccc")),
        ("INNERGRID",   (0,0),(-1,-1), .5, colors.HexColor("#dddddd")),
        ("TOPPADDING",  (0,0),(-1,-1), 10),
        ("BOTTOMPADDING",(0,0),(-1,-1), 10),
        ("VALIGN",      (0,0),(-1,-1), "MIDDLE"),
    ]))
    story.append(banner)
    story.append(Spacer(1, .3*cm))

    # ── Legend ──
    legend = Table([[
        Paragraph("<b>LEGENDA KANALU SPRZEDAZY:</b>", s_body),
        Paragraph("<b>OBA</b> = wlasna strona + Allegro", ParagraphStyle("leg", parent=s_body, textColor=CHANNEL_COLORS["OBA"])),
        Paragraph("<b>WLASNA</b> = tylko wlasna strona", ParagraphStyle("leg", parent=s_body, textColor=CHANNEL_COLORS["WLASNA"])),
        Paragraph("<b>ALLEGRO</b> = glownie Allegro", ParagraphStyle("leg", parent=s_body, textColor=CHANNEL_COLORS["ALLEGRO"])),
    ]], colWidths=[W*0.25, W*0.25, W*0.25, W*0.25])
    legend.setStyle(TableStyle([
        ("BACKGROUND",  (0,0),(-1,-1), colors.HexColor("#f8f8f8")),
        ("BOX",         (0,0),(-1,-1), .5, colors.HexColor("#cccccc")),
        ("TOPPADDING",  (0,0),(-1,-1), 5),
        ("BOTTOMPADDING",(0,0),(-1,-1), 5),
        ("LEFTPADDING", (0,0),(-1,-1), 8),
    ]))
    story.append(legend)
    story.append(Spacer(1, .4*cm))

    # ── Column widths ──
    cw = [W*0.20, W*0.13, W*0.10, W*0.20, W*0.29, W*0.08]
    hdr_labels = ["Firma", "Kategoria", "Lokalizacja", "Strona / Allegro", "Opis oferty", "Kanal"]
    hdr = [Paragraph(f"<b>{h}</b>", s_body) for h in hdr_labels]

    for seg in MARKET_DATA["segments"]:
        seg_color = colors.HexColor(seg["color"])

        hdr_block = Table([[Paragraph(seg["name"], s_sec)]], colWidths=[W])
        hdr_block.setStyle(TableStyle([
            ("BACKGROUND", (0,0),(-1,-1), seg_color),
            ("TOPPADDING", (0,0),(-1,-1), 7),
            ("BOTTOMPADDING",(0,0),(-1,-1), 7),
            ("LEFTPADDING",(0,0),(-1,-1), 10),
        ]))
        story.append(KeepTogether([hdr_block]))
        story.append(Spacer(1, .15*cm))
        story.append(Paragraph(seg["intro"], s_intro))

        rows = [hdr]
        row_bgs = []
        for c in seg["clients"]:
            name, cat, loc, url, desc, channel = c
            if url and url != "-":
                url_cell = Paragraph(f'<link href="https://{url}" color="#0057B8">{url}</link>', s_link)
            else:
                url_cell = Paragraph("—", s_body)
            rows.append([
                Paragraph(f"<b>{name}</b>", s_body),
                Paragraph(cat, s_body),
                Paragraph(loc, s_body),
                url_cell,
                Paragraph(desc, s_body),
                Paragraph(channel, s_ch[channel]),
            ])
            row_bgs.append(CHANNEL_BG[channel])

        tbl = Table(rows, colWidths=cw, repeatRows=1)
        ts  = TableStyle([
            ("BACKGROUND",  (0,0),(-1,0), colors.HexColor("#e8e8e8")),
            ("FONTNAME",    (0,0),(-1,0), "Helvetica-Bold"),
            ("FONTSIZE",    (0,0),(-1,-1), 7.5),
            ("VALIGN",      (0,0),(-1,-1), "TOP"),
            ("TOPPADDING",  (0,0),(-1,-1), 4),
            ("BOTTOMPADDING",(0,0),(-1,-1), 4),
            ("LEFTPADDING", (0,0),(-1,-1), 4),
            ("RIGHTPADDING",(0,0),(-1,-1), 4),
            ("BOX",         (0,0),(-1,-1), .5, colors.HexColor("#cccccc")),
            ("INNERGRID",   (0,0),(-1,-1), .25, colors.HexColor("#dddddd")),
        ])
        for i, bg in enumerate(row_bgs, 1):
            ts.add("BACKGROUND", (0,i), (-1,i), bg)
        tbl.setStyle(ts)
        story.append(tbl)
        story.append(Spacer(1, .35*cm))

    # ── Strategy Tips ──
    story.append(HRFlowable(width=W, thickness=1.5, color=colors.HexColor("#1A1A2E"), spaceAfter=8))
    story.append(Paragraph("WNIOSKI I WSKAZOWKI STRATEGICZNE", ParagraphStyle("TH", parent=styles["Heading2"],
                fontSize=11, textColor=colors.HexColor("#1A1A2E"),
                fontName="Helvetica-Bold", spaceAfter=6)))
    for tip in MARKET_DATA["tips"]:
        story.append(Paragraph(f"->  {tip}", s_tip))

    story.append(Spacer(1, .8*cm))
    story.append(Paragraph(f"Wygenerowano automatycznie  |  {meta['date']}", s_foot))

    doc.build(story)
    print(f"PDF wygenerowany: {output_path}")
    return output_path

# ─── ENTRY ────────────────────────────────────────────────────────────────────

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--output", default=".tmp/rynek_zestawy_prezentowe.pdf")
    args = parser.parse_args()
    os.makedirs(os.path.dirname(args.output), exist_ok=True)
    build_pdf(args.output)
