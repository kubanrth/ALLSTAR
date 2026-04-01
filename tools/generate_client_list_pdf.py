#!/usr/bin/env python3
"""
Tool: generate_client_list_pdf.py
Generates a PDF with potential clients for a photo/video content business.
Usage: python3 tools/generate_client_list_pdf.py --output .tmp/clients.pdf
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

CLIENT_DATA = {
    "meta": {
        "title": "Potential Clients – E-commerce Photo & Video Content",
        "subtitle": "Market Analysis: Rzeszow / Subcarpathia / Poland",
        "date": str(date.today()),
    },
    "segments": [

        # ── 1. LOCAL ──────────────────────────────────────────────────────────
        {
            "name": "RZESZOW & SUBCARPATHIA — Local Priority Clients",
            "color": "#1A3C5E",
            "intro": (
                "Local clients are the top priority at launch — short travel time, face-to-face meetings, "
                "and fast portfolio building. Rzeszow is the fastest-growing city in Poland with a vibrant "
                "e-commerce scene and hosts RZEcommerce, a dedicated regional e-commerce event."
            ),
            "clients": [
                ("INGLOT Cosmetics",          "Beauty / Cosmetics",         "Przemysl (near Rzeszow)", "inglotcosmetics.com",      "Global cosmetics producer — 950+ stores in 90 countries, HQ in Subcarpathia. Constant need for product shots, campaign & lookbook content.",                "HIGH"),
                ("Aruba Kosmetyka Profesjonalna","Beauty / Distribution",   "Rzeszow",                 "aruba.rzeszow.pl",         "Exclusive Polish distributor of Italian brand Karaja. Active online sales and social media — needs product photos and short-form video.",   "HIGH"),
                ("Cocolita.pl",               "Beauty / Online Drugstore",  "Rzeszow",                 "cocolita.pl",              "Rzeszow-based online beauty drugstore (SHOKO sp. z o.o.). Growing SKU catalogue requires ongoing professional product content.",              "HIGH"),
                ("Wispol",                    "Beauty / Online Drugstore",  "Rzeszow",                 "wispol.eu",                "24/7 online cosmetics store with a wide product catalogue — high demand for fresh, high-quality product imagery.",                          "HIGH"),
                ("Way to Beauty",             "Beauty / Retail + Online",   "Rzeszow",                 "waybeauty.pl",             "Stationery store + e-commerce drogeria. Product photography needed to grow the online channel.",                                          "MEDIUM"),
                ("Vanilla Hurtownia",         "Beauty / B2B Wholesale",     "Rzeszow",                 "vanilla.rzeszow.pl",       "20 years on the market. Supplies professional cosmetics and aesthetic medicine products — B2B catalogue and social content.",              "MEDIUM"),
                ("Prof-Kos",                  "Beauty / B2B Wholesale",     "Rzeszow",                 "profkos.pl",               "Since 2000, supplies beauty salons and aesthetic clinics across Poland. B2B catalogue content and e-shop imagery.",                        "MEDIUM"),
                ("KosmePro",                  "Beauty / B2B",               "Rzeszow",                 "kosmepro.pl",              "Specialist wholesaler for cosmetologists. Product imagery for online catalogue and social campaigns.",                                      "MEDIUM"),
                ("Dermie",                    "Beauty / Aesthetic Clinic",  "Rzeszow",                 "dermie.pl",                "Modern aesthetic cosmetology clinic. Needs clinic branding photography, treatment showcase video and social media content.",                "MEDIUM"),
                ("Taranko",                   "Fashion / Women's Clothing", "Rzeszow",                 "taranko.com.pl",           "Polish premium womenswear brand with gallery stores. Needs lookbooks, collection sessions and video campaigns.",                           "HIGH"),
                ("Pełna Szafa",               "Fashion / Pre-owned",        "Rzeszow",                 "-",                        "Top-rated clothing store in Rzeszow (4.5★ Google). Growing second-hand premium market demands attractive online content.",                  "MEDIUM"),
            ],
        },

        # ── 2. FASHION — WOMEN'S ──────────────────────────────────────────────
        {
            "name": "FASHION — Women's Clothing Brands",
            "color": "#2D5016",
            "intro": (
                "Women's fashion is one of the richest markets for content creation. Polish brands "
                "producing locally (#szyjemywpolsce) need regular lookbooks, collection sessions, "
                "campaign shoots and social media reels. Brands below are active online shops."
            ),
            "clients": [
                ("NAREE",          "Women's Fashion",          "Poland",   "naree.pl",           "152K Instagram followers, produces in Poland. Regular collection photoshoots and campaign videos.",                        "HIGH"),
                ("BLAAR",          "Women's Fashion (petite)", "Warsaw",   "blaar.pl",           "Brand for women under 164cm, 59K IG. Own production in Poland — lifestyle sessions and lookbooks.",                       "HIGH"),
                ("EMOI",           "Women's Fashion",          "Poland",   "emoi.pl",            "30+ year heritage, sizes 36-52, sews in Poland. E-commerce needs constant product and lifestyle content.",                "HIGH"),
                ("Makadamia",      "Women's Fashion",          "Poland",   "makadamia.pl",       "Elegant dresses and daily sets. Active online store needing seasonal campaign imagery.",                                  "HIGH"),
                ("Lillow",         "Women's Fashion",          "Poland",   "lillow.pl",          "Timeless Polish womenswear. Regular collection sessions and e-commerce product photography.",                             "HIGH"),
                ("TALYA",          "Women's Fashion",          "Poland",   "talya.pl",           "Sews exclusively in Poland. Steady market for product photography — dresses, shirts, trousers.",                         "HIGH"),
                ("MEISSIMO",       "Women's Fashion Premium",  "Poland",   "meissimo.com",       "Quality womenswear blending elegance and comfort. Premium imagery for website and campaigns.",                            "MEDIUM"),
                ("BIALCON",        "Women's Fashion",          "Poland",   "bialcon.pl",         "Founded 1992, elegant and clean cuts for women. Lookbooks, e-commerce photos and brand video.",                          "MEDIUM"),
                ("Hexeline",       "Women's Fashion Premium",  "Poland",   "hexeline.pl",        "Timeless elegance by designer Halina Zawadzka. High-end campaign photography and video.",                                "MEDIUM"),
                ("Bessoniana",     "Women's Fashion",          "Krakow",   "bessoniana.pl",      "Young Krakow brand with bold botanical prints — needs editorial and e-commerce shooting.",                               "MEDIUM"),
                ("ANSIN",          "Basics / Unisex",          "Poland",   "ansin.pl",           "Premium minimalist basics for men and women, European fabrics. Clean product and lifestyle imagery.",                    "MEDIUM"),
                ("Affair Warsaw",  "Women's / Unisex",         "Warsaw",   "affairwarsaw.com",   "Urban brand for everyday and evening. Product photos and social media video content.",                                   "MEDIUM"),
                ("Elementy",       "Slow Fashion",             "Poland",   "elementy.co",        "Transparent pricing, local production, Scandi aesthetics. Minimalist product sessions.",                                 "MEDIUM"),
            ],
        },

        # ── 3. FASHION — STREETWEAR ────────────────────────────────────────────
        {
            "name": "FASHION — Streetwear & Youth Brands",
            "color": "#3A1A5E",
            "intro": (
                "Streetwear and youth brands are high-volume content consumers — they run frequent drops, "
                "campaigns, and reels. Many of these Polish brands have strong social media followings and "
                "invest regularly in visual content."
            ),
            "clients": [
                ("Local Heroes",   "Streetwear",          "Poland",    "localheroesshop.com",  "One of Poland's most recognizable youth streetwear brands. Strong IG presence, regular campaigns and lookbooks.",          "HIGH"),
                ("Aloha From Deer","Streetwear / Art",    "Poland",    "alohafromdeer.com",    "Colorful pop-art inspired prints, viral social media. Creative, high-energy campaign shoots.",                             "HIGH"),
                ("MISBHV",         "Streetwear Premium",  "Warsaw",    "misbhv.com",           "World-class Polish streetwear worn by Rihanna and Kylie Jenner. Premium visual content is essential.",                    "HIGH"),
                ("Medicine",       "Fashion / Artistic",  "Poland",    "medicine-shop.com",    "LPP Group brand with unique graphics and limited art collections. Large content budget.",                                  "HIGH"),
                ("PLNY LALA",      "Women's Streetwear",  "Poland",    "plnylala.com",         "Feminine streetwear with distinctive prints. Very visual brand — lifestyle and campaign content.",                         "HIGH"),
                ("Pan Tu Nie Stał","Streetwear / Humor",  "Poland",    "pantuniestal.com",     "Cult PRL-aesthetic brand with humor — unconventional campaigns, high creative potential.",                                "MEDIUM"),
                ("PROSTO",         "Streetwear / Hip-hop","Poland",    "prosto.pl",            "Legend of Polish hip-hop streetwear. Regular collections need photography and video.",                                     "MEDIUM"),
                ("MMC Studio",     "Avant-garde Fashion", "Poland",    "mmcstudio.pl",         "Avant-garde design, fashion week favourite. Artistic shoots and video campaigns.",                                         "MEDIUM"),
                ("EL POLAKO",      "Streetwear",          "Lodz",      "elpolako.pl",          "Street style from Lodz, strong hip-hop scene. Lookbooks and campaign photography.",                                       "MEDIUM"),
                ("Proudly Presents","Lo-fi / Retro",      "Poland",    "proudlypresents.pl",   "Lo-fi and retro aesthetic — niche but growing brand needing consistent visual content.",                                  "LOW"),
            ],
        },

        # ── 4. FASHION PLATFORMS ────────────────────────────────────────────
        {
            "name": "FASHION — Multibrand Platforms & Marketplaces",
            "color": "#1A4A2A",
            "intro": (
                "Fashion platforms and multibrands run hundreds or thousands of SKUs and need constant "
                "product photography to stay competitive. They are also gateways to smaller brands "
                "listed on their platforms."
            ),
            "clients": [
                ("MODIVO",       "Fashion Multibrand",       "Poland",  "modivo.pl",         "300K+ products, 1700+ brands incl. Versace, DKNY, Tommy Hilfiger. One of Poland's largest fashion e-shops.",  "HIGH"),
                ("eButik.pl",    "Slow Fashion Platform",    "Poland",  "ebutik.pl",         "20+ years, connects slow fashion and local producers. Constant content demand.",                                "HIGH"),
                ("SzafaPolska",  "Polish Brands Platform",   "Poland",  "szafapolska.pl",    "Aggregator of Polish clothing brands (women, men, kids). Gateway to multiple brands at once.",                 "HIGH"),
                ("Domodi",       "Fashion Aggregator",       "Poland",  "domodi.pl",         "Large Polish fashion aggregator. Brands listed here need professional imagery to stand out.",                  "MEDIUM"),
                ("PolskieMarki", "Polish Brands Directory",  "Poland",  "polskiemarki.pl",   "Portal listing Polish brands — potential channel to reach multiple small brands needing content.",              "LOW"),
            ],
        },

        # ── 5. FOOTWEAR & BAGS ─────────────────────────────────────────────────
        {
            "name": "FOOTWEAR & BAGS — Polish Brands",
            "color": "#4A2800",
            "intro": (
                "Footwear and bags are high-photography-dependency categories. Clean product shots, "
                "lifestyle and detail photography are crucial for conversion in these segments. "
                "Poland has a strong tradition of leather goods manufacturing."
            ),
            "clients": [
                ("eobuwie.pl / modivo group","Footwear Platform", "Poland",  "eobuwie.com.pl",    "European leader in online footwear, 90K+ products, 700+ brands, 15 markets. Huge content pipeline.",          "HIGH"),
                ("Venezia",      "Footwear & Bags",     "Poland",  "venezia.pl",        "Since 1996. Classic meets modern — footwear and accessories. Seasonal campaigns and product photography.",         "HIGH"),
                ("Kazar",        "Premium Footwear",    "Poland",  "kazar.com",         "Premium Polish brand since 1990, 60+ stores. Original product and campaign photography.",                           "HIGH"),
                ("Gino Rossi",   "Footwear",            "Poland",  "gino-rossi.com",    "Polish-Italian brand since 1992, men's and women's. Catalogue and lifestyle photography.",                          "HIGH"),
                ("Wojas",        "Footwear",            "Poland",  "wojas.pl",          "Premium Polish footwear, some handmade. Product and lifestyle photography for online and print.",                   "HIGH"),
                ("Ryłko",        "Footwear",            "Poland",  "rylko.com",         "50+ year heritage brand. Classic Polish footwear — e-commerce product photography.",                                "MEDIUM"),
                ("Brilu",        "Bridal Footwear",     "Poland",  "brilu.pl",          "#1 Polish bridal shoes brand, 100% made in Poland. Elegant lifestyle and product sessions.",                        "MEDIUM"),
                ("Balagan Studio","Leather Goods",      "Warsaw",  "balagandstudio.com","Artisan leather bags and shoes, Warsaw/Tel Aviv aesthetic. Artistic product and editorial shoots.",                 "MEDIUM"),
                ("Neścior",      "Handmade Footwear",   "Poland",  "nescior.pl",        "Family business since 2001, handmade women's shoes in natural leather. Detail and lifestyle photography.",          "MEDIUM"),
                ("Skorzana.com", "Leather Bags Platform","Poland",  "skorzana.com",      "Largest platform for Polish leather bags brands. Gateway to multiple bag producers.",                              "LOW"),
            ],
        },

        # ── 6. BEAUTY — ESTABLISHED ────────────────────────────────────────────
        {
            "name": "BEAUTY — Established Polish Brands",
            "color": "#5E1A3C",
            "intro": (
                "Beauty is one of the best-paying niches for content creation. Product shots, lifestyle, "
                "video tutorials and social campaigns are daily needs. Large brands have dedicated content "
                "budgets and multi-SKU catalogues requiring ongoing photography."
            ),
            "clients": [
                ("Eveline Cosmetics",  "Cosmetics / Makeup",    "Poland",  "evelinecosmetics.pl",    "Polish brand in 70 countries, 6 continents. Large product catalogue — constant content demand.",                "HIGH"),
                ("Nacomi",             "Natural Cosmetics",     "Poland",  "nacomi.pl",              "Popular natural beauty brand, active e-commerce. Regular product shots and social campaigns.",                  "HIGH"),
                ("BasicLab",           "Dermocosmetics",        "Poland",  "basiclab.pl",            "Fast-growing science-based skincare brand with minimalist aesthetics. Visual quality is core to the brand.",    "HIGH"),
                ("Bielenda",           "Cosmetics / Professional","Poland", "bielenda.pl",            "Established brand with professional line for salons. Large content budget, ongoing photography.",               "HIGH"),
                ("Farmona",            "Natural Cosmetics",     "Poland",  "farmona.pl",             "Innovative dermocosemtics for body and hair. B2B and B2C content — laboratory and lifestyle.",                 "HIGH"),
                ("Apis Natural Cosmetics","Natural Cosmetics",  "Poland",  "apis.com.pl",            "35+ year tradition since 1988, Royal Jelly cult product. E-commerce and lifestyle photography.",               "HIGH"),
                ("Lirene",             "Skincare",              "Poland",  "lirene.pl",              "Brand under Dr Irena Eris group. Wide skincare range — product and campaign photography.",                      "HIGH"),
                ("Floslek",            "Dermocosmetics",        "Poland",  "floslek.pl",             "25+ years, sensitive skin focus. Clean, clinical photography for e-commerce.",                                  "MEDIUM"),
                ("Inglot",             "Makeup / Color",        "Przemysl","inglotcosmetics.com",     "900+ global locations, 2500+ products. Global-quality content needs, local HQ.",                               "MEDIUM"),
                ("Ziaja",              "Cosmetics / Pharmacy",  "Gdansk",  "ziaja.com",              "One of Poland's most recognizable pharmacy cosmetics brands. Very high SKU count.",                             "MEDIUM"),
            ],
        },

        # ── 7. BEAUTY — NATURAL & ECO ─────────────────────────────────────────
        {
            "name": "BEAUTY — Natural, Eco & Indie Brands",
            "color": "#1A4A1A",
            "intro": (
                "Natural and indie beauty brands often lack professional content despite having great "
                "products. This is a perfect entry point — smaller budgets but easier to win, and they "
                "become long-term clients as they scale."
            ),
            "clients": [
                ("YOPE",              "Natural Cosmetics / Home","Poland",  "yope.me",              "Recognizable animal-label packaging, sold in Poland and abroad. Product and lifestyle photography.",              "HIGH"),
                ("Organique",         "Organic Cosmetics",      "Wroclaw",  "organique.pl",         "25+ years, made near Wroclaw. Full product catalogue needs regular refreshing.",                                 "HIGH"),
                ("Mokosh",            "Natural Cosmetics",      "Poland",   "mokosh.pl",            "Premium natural cosmetics brand. Minimalist photography aligned with brand values.",                             "HIGH"),
                ("Resibo",            "Eco / Vegan Cosmetics",  "Poland",   "resibo.pl",            "96% natural ingredients, cruelty-free, vegan. Consistent eco-aesthetic content.",                               "HIGH"),
                ("Hagi Cosmetics",    "Handmade Natural",       "Poland",   "hagicosmetics.pl",     "Handmade cosmetics, Polish sourcing. Warm, authentic brand photography.",                                       "HIGH"),
                ("BognaSkin",         "Skincare / Minimalist",  "Poland",   "bognaskin.pl",         "Rising minimalist skincare brand with short ingredient lists. Clean, precise product photography.",              "HIGH"),
                ("Ukviat",            "Skincare / Adaptogens",  "Poland",   "ukviat.com",           "New brand with mushroom adaptogens and sea minerals. Building visual identity from scratch — ideal entry.",       "HIGH"),
                ("OnlyBio",           "Bio Cosmetics",          "Poland",   "onlybio.pl",           "Certified bio cosmetics, active brand collaborations (e.g. E.Wedel). Lifestyle and product content.",           "HIGH"),
                ("MIYA Cosmetics",    "Skincare",               "Poland",   "miyacosmetics.pl",     "Active brand constantly launching new products — ongoing content demand.",                                       "HIGH"),
                ("ZEW for Men",       "Men's Grooming",         "Poland",   "zewformen.com",        "Natural men's grooming brand inspired by Slavic nature. Masculine, outdoorsy photography.",                      "HIGH"),
                ("Orientana",         "Natural / Ayurveda",     "Poland",   "orientana.pl",         "100% natural, oriental aesthetic. Thematic product sessions with unique mood boards.",                           "MEDIUM"),
                ("Krayna",            "Vegan Cosmetics",        "Poland",   "krayna.pl",            "Eco, vegan brand based on local Polish plants. Authentic, natural content.",                                     "MEDIUM"),
                ("VIANEK / Sylveco",  "Natural Cosmetics",      "Poland",   "sylveco.pl",           "Colorful folk-inspired packaging, organic herbs from Podlasie. Lifestyle and product photography.",              "MEDIUM"),
                ("Clochee",           "Natural Skincare",       "Poland",   "clochee.com",          "Natural skincare range. Clean product photography for e-commerce.",                                              "MEDIUM"),
                ("beBio (Chodakowska)","Eco Cosmetics",         "Poland",   "bebio.pl",             "Ewa Chodakowska's eco cosmetics line. Celebrity brand — high content quality expected.",                         "MEDIUM"),
                ("Hairy Tale Cosmetics","Hair Care",            "Poland",   "hairytalecosmetics.pl","Hair care brand by a popular beauty blogger. Social media is key channel — video and photos.",                   "MEDIUM"),
                ("Make Me Bio",       "Certified Eco",          "Poland",   "makemebio.com",        "Certified organic cosmetics. E-commerce product photography.",                                                   "MEDIUM"),
                ("Bracia Mydlarze",   "Natural Soap / Handmade","Poland",   "braciamdlarze.pl",     "Artisan natural soaps, biodegradable. Handmade brand needs warm, craft-style photography.",                     "MEDIUM"),
                ("Food4face",         "Skincare",               "Poland",   "food4face.com",        "Active skincare brand with regular new product launches.",                                                       "MEDIUM"),
                ("OREKA",             "Eco / Minimalist",       "Poland",   "oreka.pl",             "Founded 2020, eco minimalist brand. Multifunctional products — lifestyle and product sessions.",                 "LOW"),
            ],
        },

        # ── 8. JEWELRY & ACCESSORIES ───────────────────────────────────────────
        {
            "name": "JEWELRY & ACCESSORIES — Polish Brands",
            "color": "#4A3500",
            "intro": (
                "Jewelry photography sells the product. Small handmade and independent designers especially "
                "need professional product and lifestyle photography — they often search for photographers "
                "directly in Instagram comments. Lower budgets but loyal, recurring clients."
            ),
            "clients": [
                ("Apart",          "Jewelry / Jubiler",      "Poland",   "apart.pl",          "Poland's #1 jewellery chain, founded 1977 in Poznan. Large content budget, seasonal campaigns.",          "HIGH"),
                ("W.KRUK",         "Jewelry / Heritage",     "Poland",   "wkruk.pl",          "Oldest Polish jewellery brand (since 1840). Premium campaign and product photography.",                    "HIGH"),
                ("Mokobelle",      "Handmade Jewelry",       "Poland",   "mokobelle.com",     "Popular online handmade jewelry brand. Constant product shoots and lifestyle content.",                    "HIGH"),
                ("Kazar Jewelry",  "Jewelry / Premium",      "Poland",   "kazar.com",         "Premium accessories alongside footwear — jewellery and accessories photography.",                          "HIGH"),
                ("Sadva",          "Amber Jewelry",          "Poland",   "sadva.pl",          "Modern amber jewelry brand — unique product photography showcasing 'Baltic gold'.",                        "HIGH"),
                ("Maar",           "Designer Jewelry",       "Poland",   "maar.pl",           "Bold colorful silver jewelry. Needs consistent, high-quality product sessions.",                           "HIGH"),
                ("LAU Jewelry",    "Artisan Jewelry",        "Poland",   "lau-jewelry.com",   "Handmade silver jewelry duo. Artistic lifestyle sessions.",                                                "MEDIUM"),
                ("Alicja&Maria",   "Trend Jewelry",          "Poland",   "alicjaimaria.pl",   "Instagram-trend jewelry brand. Social media content and product photography.",                             "MEDIUM"),
                ("Niesyzyfoweprace","Artisan / Personalized","Poland",   "niesyzyfoweprace.pl","Personalized handmade jewelry. Lifestyle and detail product sessions.",                                  "MEDIUM"),
                ("Jagg.",          "Vintage Jewelry",        "Poland",   "-",                 "Vintage and antique jewelry reworked as accessories. Unique, editorial-style photography.",               "LOW"),
                ("DecoBazaar",     "Handmade Marketplace",   "Poland",   "decobazaar.com",    "Marketplace of independent creators — entry point to many small jewelry makers.",                         "LOW"),
            ],
        },

        # ── 9. HOME DECOR ──────────────────────────────────────────────────────
        {
            "name": "HOME DECOR & INTERIOR — Polish E-commerce",
            "color": "#1A3A3A",
            "intro": (
                "Home decor is an inspiration-driven category. 80% of Polish consumers find home "
                "inspiration online. Lifestyle staging photography and detail product shots are "
                "critical for conversion. Poland is Europe's #2 furniture exporter."
            ),
            "clients": [
                ("Homla",          "Home Decor / Online",    "Poland",   "homla.com.pl",      "Polish home decor brand — ceramics, textiles, accessories. Large SKU catalogue needs regular content.",       "HIGH"),
                ("Fabryka Form",   "Home Decor / Design",    "Poland",   "fabrykaform.pl",    "Since 2005, thousands of products across kitchen, bedroom, bathroom, garden. High content volume.",           "HIGH"),
                ("Westwing",       "Premium Home Decor",     "Poland",   "westwing.pl",       "Premium furniture and decor online store. Inspiration-driven content — staging and lifestyle.",                "HIGH"),
                ("Homebook",       "Interior / Platform",    "Poland",   "homebook.pl",       "10-year interior design platform. Inspirational content is their core business model.",                        "MEDIUM"),
                ("VillaDecor",     "Luxury Home Decor",      "Poland",   "villadecor.pl",     "Luxury home accessories — modern, glamour, art deco. High-end product and interior photography.",             "MEDIUM"),
                ("Meble.pl",       "Furniture / E-commerce", "Poland",   "meble.pl",          "Large furniture e-shop. Catalogue and lifestyle photography for wide product range.",                          "MEDIUM"),
                ("Obracamy360",    "360° Product / Furniture","Poland",  "obracamy360.pl",    "Specialist in 360° and 3D furniture visuals — potential partner or direct client.",                            "LOW"),
            ],
        },

        # ── 10. SPORTS & OUTDOOR ───────────────────────────────────────────────
        {
            "name": "SPORTS & OUTDOOR — Polish Brands",
            "color": "#2A3A1A",
            "intro": (
                "Sports brands need dynamic photography and video — action shots, lifestyle, product detail. "
                "Polish brands in outdoor and fitness are growing fast and compete internationally. "
                "Content quality is often the deciding factor vs. international competitors."
            ),
            "clients": [
                ("4F",             "Sports Apparel",         "Poland",   "4f.com.pl",         "Poland's largest sports brand, Olympic team outfitter. Large content budget and diverse product range.",    "HIGH"),
                ("Nessi Sportswear","Women's Fitness Wear",  "Poland",   "nessi-sport.com",   "Designs and sews women's sportswear in Poland. Fitness lifestyle and product photography.",                 "HIGH"),
                ("ATTIQ",          "Running / Cycling",      "Poland",   "attiq.net",         "Performance gear tested by athletes. Action, lifestyle and product photography.",                            "HIGH"),
                ("PAJAK",          "Outdoor / Mountain",     "Poland",   "pajaksport.pl",     "Since 1983, premium outdoor gear. Adventure and lifestyle photography in mountain environments.",             "HIGH"),
                ("Marbo Sport",    "Gym Equipment",          "Poland",   "marbo-sport.pl",    "Manufacturer of home and commercial gym equipment. Product and lifestyle photography.",                       "MEDIUM"),
                ("Majesty",        "Winter Sports / Skis",   "Poland",   "majestyfreeride.com","Polish ski brand acclaimed internationally. Action, lifestyle and product photography.",                    "MEDIUM"),
                ("GOG Eyewear",    "Sports Eyewear",         "Poland",   "gogeyewear.com",    "Polish sports glasses and goggles for cycling, skiing, running. Product and action photography.",            "MEDIUM"),
                ("Sportano",       "Sports Multibrand",      "Poland",   "sportano.pl",       "Multi-brand sports online store. Product photography for wide assortment.",                                  "MEDIUM"),
            ],
        },

        # ── 11. KIDS & BABY ────────────────────────────────────────────────────
        {
            "name": "KIDS & BABY — Polish E-commerce",
            "color": "#5E3A1A",
            "intro": (
                "Baby and kids products are emotionally driven purchases. Professional photography "
                "that shows safety, quality and lifestyle is critical. Polish brands in this segment "
                "often produce locally and are competing with global giants like Cybex."
            ),
            "clients": [
                ("La Millou",      "Baby / Premium",         "Poland",   "lamillou.com",      "Premium Polish baby brand with gorgeous lifestyle content. Flagship e-commerce photography.",             "HIGH"),
                ("Kinderkraft",    "Baby Gear / Global",     "Poland",   "kinderkraft.com",   "Polish brand competing globally with strollers, car seats. High-quality product content required.",       "HIGH"),
                ("Lullalove",      "Baby Textiles",          "Poland",   "lullalove.pl",      "Popular Polish baby textile brand. Lifestyle and product photography for e-commerce.",                    "HIGH"),
                ("Babyboutik",     "Baby Multibrand",        "Poland",   "babyboutik.pl",     "450+ brands, curated baby products. Content partner for multiple brand shoots.",                          "HIGH"),
                ("ABC Bobasa",     "Baby Clothing / Polish", "Poland",   "abc-bobasa.pl",     "Polish baby clothing brands only — Pinokio, Eevi, Makoma. Product photography.",                         "MEDIUM"),
                ("Dobre Liski",    "Baby Lifestyle Store",   "Poland",   "dobreliski.pl",     "Carefully curated baby brands — Jellycat, BIBS, EZPZ. Lifestyle and product photography.",               "MEDIUM"),
                ("Baby and Mam",  "Baby / Mom",              "Poland",   "babyandmam.pl",     "Accessories, merino knitwear, Jellycat. Lifestyle photography for social media.",                         "MEDIUM"),
                ("Fartlandia",     "Baby Gear",              "Poland",   "fartlandia.pl",     "Strollers and baby gear — Cybex, Kinderkraft, Britax. Product photography catalogue.",                   "MEDIUM"),
            ],
        },

        # ── 12. FOOD & HEALTH ─────────────────────────────────────────────────
        {
            "name": "FOOD, HEALTH & SUPPLEMENTS — Polish E-commerce",
            "color": "#1A4A3A",
            "intro": (
                "Healthy food and supplements are fast-growing e-commerce categories in Poland. "
                "Brands need appetizing food photography, lifestyle content and video to compete "
                "online. Product imagery directly impacts conversion on these stores."
            ),
            "clients": [
                ("KruKam",          "Health Food / Producer",  "Poland",  "krukam.pl",           "Polish health food manufacturer and online store. Product photography for own SKUs.",                "HIGH"),
                ("NaturalnieZdrowe","Health Food / Online",    "Poland",  "naturalniezdrowe.pl",  "Eco food, supplements, diety specjalne — works mainly with Polish producers.",                     "HIGH"),
                ("MarketBio",       "Bio Food / Online",       "Poland",  "marketbio.pl",         "5000+ organic products, sports nutrition. Large product catalogue needs content.",                  "HIGH"),
                ("e-Superfood",     "Superfoods / Supplements","Poland",  "e-superfood.pl",       "Superfoods, adaptogens, keto, collagen. Product and lifestyle photography.",                        "HIGH"),
                ("Biogo",           "Eco / Gluten-free",       "Poland",  "biogo.pl",             "Organic, vegan, gluten-free, natural supplements. Product and lifestyle content.",                  "MEDIUM"),
                ("Organic Market",  "Organic Food / Delivery", "Poland",  "organic24.pl",         "Fresh organic produce + online. Lifestyle and product photography for digital channel.",            "MEDIUM"),
                ("DelikatesyZNatury","Eco Food / Zero Waste",  "Poland",  "delikatesyznatury.pl", "Eco food, cosmetics, zero waste lifestyle. Food and lifestyle photography.",                        "MEDIUM"),
                ("ZdrowieNaStole",  "Supplements / Eco",       "Poland",  "zdrowienastole.pl",    "Supplements and eco food. Product photography for online store.",                                   "MEDIUM"),
                ("eNaturalnie",     "Herbs / Tea / Eco",       "Poland",  "enaturalnie.pl",       "Herbs, teas, spices, organic oils — 90% certified organic. Food photography.",                     "LOW"),
            ],
        },

        # ── 13. PET CARE ──────────────────────────────────────────────────────
        {
            "name": "PET CARE — Polish E-commerce",
            "color": "#2A1A4A",
            "intro": (
                "Pet care is one of Poland's fastest-growing e-commerce segments. Polish brands are "
                "emerging in premium pet food. Professional product and lifestyle photography with "
                "animals creates strong emotional connection with buyers."
            ),
            "clients": [
                ("Dolina Noteci",   "Premium Pet Food / PL",  "Poland",  "dolinanoteci.pl",   "Leading Polish wet cat and dog food brand. Own brand product photography and campaigns.",               "HIGH"),
                ("Wiejska Zagroda", "Premium Pet Food / PL",  "Poland",  "wiejskazagroda.pl", "Polish mono-protein pet food brand. Product photography and lifestyle content.",                        "HIGH"),
                ("Paka Zwierzaka",  "Natural Pet Food / PL",  "Poland",  "pakazwierzaka.pl",  "Polish natural pet food brand growing fast. Brand and product content.",                                "HIGH"),
                ("Gussto",          "Wet Pet Food / PL",      "Poland",  "gussto.pl",         "Polish premium wet food for cats and dogs. Product photography.",                                        "HIGH"),
                ("Fera.pl",         "Pet Care / Multibrand",  "Poland",  "fera.pl",           "Founded 2014, multi-brand pet care store. Product photography for wide catalogue.",                     "MEDIUM"),
                ("ZooExpress",      "Pet Care / Online",      "Poland",  "zooexpress.pl",     "6000+ products, same-day shipping. Product imagery for e-commerce.",                                    "MEDIUM"),
                ("PsieDobre",       "Dog Care / Online",      "Poland",  "psiedobre.pl",      "Dog-focused online store emphasizing clean-ingredient food. Lifestyle photography.",                     "MEDIUM"),
                ("Apetete",         "Pet Care / Premium",     "Poland",  "apetete.pl",        "Premium and super-premium pet brands. Product photography for catalogues.",                              "MEDIUM"),
            ],
        },

        # ── 14. CRAFT BEER & BEVERAGES ─────────────────────────────────────────
        {
            "name": "CRAFT BEER & BEVERAGES — Polish E-commerce",
            "color": "#3A2A1A",
            "intro": (
                "Poland's craft beer revolution started in 2011 and hasn't stopped. Polish craft breweries "
                "are internationally recognised. Online beer shops need product photography and brand "
                "content to differentiate their selection. Breweries need brand imagery."
            ),
            "clients": [
                ("PINTA Brewery",        "Craft Beer / Producer",  "Poland",  "browarpinta.pl",       "Pioneer of Polish craft beer. Brand photography, product shots and video content.",           "HIGH"),
                ("Funky Fluid",          "Craft Beer / Producer",  "Poland",  "funkyfluid.pl",        "Internationally acclaimed craft brewery. Premium product and brand photography.",              "HIGH"),
                ("Browar Stu Mostów",    "Craft Beer / Producer",  "Wroclaw", "stustow.pl",           "Award-winning Wroclaw brewery. Campaign and product photography.",                            "HIGH"),
                ("OneMoreBeer",          "Craft Beer / Online",    "Poland",  "onemorebeer.pl",       "Largest selection of craft beers and meads online. Product photography for catalogue.",       "MEDIUM"),
                ("PiwaRzemieślnicze.pl", "Craft Beer / Online",    "Poland",  "piwarzemieslnicze.pl", "Polish craft beer marketplace. Product and lifestyle content.",                               "MEDIUM"),
                ("Piwoteka",             "Craft Beer / Online",    "Poland",  "sklep.piwoteka.pl",    "Pioneer craft beer online store since 2008. Brand and product photography.",                  "MEDIUM"),
                ("Alkoholeswiata24",     "Spirits / Online",       "Poland",  "alkoholeswiata24.pl",  "Online spirits shop — product photography for large alcohol catalogue.",                      "LOW"),
            ],
        },

    ],
    "tips": [
        "Start local in Rzeszow — lower acquisition cost, faster meetings, first portfolio references. INGLOT (Przemysl) alone can be a flagship case study.",
        "Beauty pays the most for product shots and video — prioritize when scaling. A standard beauty shoot earns 2-3x more than basic apparel.",
        "Offer a Starter Pack: 20 product photos + 1 Reel video — low decision threshold for new clients, easy upsell.",
        "Build portfolio in 3 key niches: beauty, fashion, home decor — biggest markets for content in Poland.",
        "Track the RZEcommerce event (Rzeszow) — perfect networking with local e-commerce decision makers.",
        "80% of Allegro sellers have no professional photography — massive untapped market. Target those with 4.5★+ ratings.",
        "Polish brands with #szyjemywpolsce hashtag on IG are ideal targets — they value local collaboration.",
        "Natural/eco beauty brands (Hagi, BognaSkin, Ukviat) are easier to win than corporates and become long-term clients.",
        "Pet food brands (Dolina Noteci, Wiejska Zagroda) are underserved in content quality — first mover advantage.",
        "Kids/baby lifestyle photography commands premium rates — emotional purchase category with high-trust brands.",
        "Craft breweries need brand photography for cans, events and social media — growing niche with high creative freedom.",
        "Don't cold-email. DM on Instagram or LinkedIn — find the brand's founder/marketing manager directly.",
    ],
}

# ─── PRIORITY CONFIG ──────────────────────────────────────────────────────────

PRIORITY_COLORS = {
    "HIGH":   colors.HexColor("#1a7a1a"),
    "MEDIUM": colors.HexColor("#b07d00"),
    "LOW":    colors.HexColor("#888888"),
}
PRIORITY_BG = {
    "HIGH":   colors.HexColor("#eaf5ea"),
    "MEDIUM": colors.HexColor("#fffaed"),
    "LOW":    colors.HexColor("#f5f5f5"),
}

# ─── PDF BUILDER ──────────────────────────────────────────────────────────────

def build_pdf(output_path: str):
    doc = SimpleDocTemplate(
        output_path, pagesize=A4,
        rightMargin=1.8*cm, leftMargin=1.8*cm,
        topMargin=1.8*cm, bottomMargin=1.8*cm,
        title=CLIENT_DATA["meta"]["title"],
    )
    styles = getSampleStyleSheet()
    W = A4[0] - 3.6*cm

    # ── Styles ──
    s_title = ParagraphStyle("T", parent=styles["Title"], fontSize=20,
                              textColor=colors.HexColor("#1A1A2E"), spaceAfter=4,
                              fontName="Helvetica-Bold")
    s_sub   = ParagraphStyle("S", parent=styles["Normal"], fontSize=10,
                              textColor=colors.HexColor("#555555"), spaceAfter=3)
    s_sec   = ParagraphStyle("SEC", parent=styles["Normal"], fontSize=11,
                              textColor=colors.white, fontName="Helvetica-Bold",
                              spaceAfter=0, spaceBefore=0)
    s_intro = ParagraphStyle("I", parent=styles["Normal"], fontSize=8.5,
                              textColor=colors.HexColor("#444444"), leading=13, spaceAfter=8)
    s_body  = ParagraphStyle("B", parent=styles["Normal"], fontSize=7.8,
                              textColor=colors.HexColor("#333333"), leading=12)
    s_link  = ParagraphStyle("L", parent=styles["Normal"], fontSize=7.8,
                              textColor=colors.HexColor("#0057B8"), leading=12)
    s_tip   = ParagraphStyle("TP", parent=styles["Normal"], fontSize=8.5,
                              textColor=colors.HexColor("#1A3C5E"), leading=14,
                              leftIndent=8, spaceAfter=4)
    s_foot  = ParagraphStyle("F", parent=styles["Normal"], fontSize=7,
                              textColor=colors.HexColor("#aaaaaa"), alignment=TA_CENTER)
    s_prio  = {p: ParagraphStyle(f"P_{p}", parent=s_body,
                                  textColor=PRIORITY_COLORS[p], alignment=TA_CENTER,
                                  fontName="Helvetica-Bold")
               for p in PRIORITY_COLORS}

    story = []
    meta = CLIENT_DATA["meta"]

    # ── Cover ──
    story.append(Spacer(1, .5*cm))
    story.append(Paragraph(meta["title"], s_title))
    story.append(Paragraph(meta["subtitle"], s_sub))
    story.append(Paragraph(f"Generated: {meta['date']}", s_sub))
    story.append(HRFlowable(width=W, thickness=2, color=colors.HexColor("#1A1A2E"), spaceAfter=12))

    # ── Stats banner ──
    total  = sum(len(s["clients"]) for s in CLIENT_DATA["segments"])
    high   = sum(1 for s in CLIENT_DATA["segments"] for c in s["clients"] if c[5]=="HIGH")
    medium = sum(1 for s in CLIENT_DATA["segments"] for c in s["clients"] if c[5]=="MEDIUM")
    segs   = len(CLIENT_DATA["segments"])

    banner = Table([[
        Paragraph(f"<b>{total}</b>\nTotal Clients", ParagraphStyle("bn", parent=s_body, alignment=TA_CENTER, fontSize=13, leading=16)),
        Paragraph(f"<b>{high}</b>\nHigh Priority", ParagraphStyle("bn", parent=s_body, alignment=TA_CENTER, fontSize=13, leading=16, textColor=PRIORITY_COLORS["HIGH"])),
        Paragraph(f"<b>{medium}</b>\nMedium Priority", ParagraphStyle("bn", parent=s_body, alignment=TA_CENTER, fontSize=13, leading=16, textColor=PRIORITY_COLORS["MEDIUM"])),
        Paragraph(f"<b>{segs}</b>\nMarket Segments", ParagraphStyle("bn", parent=s_body, alignment=TA_CENTER, fontSize=13, leading=16)),
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
    story.append(Spacer(1, .4*cm))

    # ── Column widths ──
    cw = [W*0.21, W*0.12, W*0.11, W*0.19, W*0.28, W*0.09]
    hdr = [Paragraph(f"<b>{h}</b>", s_body)
           for h in ["Company", "Category", "Location", "Website", "Why They Need You", "Priority"]]

    for seg in CLIENT_DATA["segments"]:
        seg_color = colors.HexColor(seg["color"])

        # Section header
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
            name, cat, loc, url, why, prio = c
            # Make URL a clickable link if not empty
            if url and url != "-":
                url_cell = Paragraph(f'<link href="https://{url}" color="#0057B8">{url}</link>', s_link)
            else:
                url_cell = Paragraph("—", s_body)
            rows.append([
                Paragraph(f"<b>{name}</b>", s_body),
                Paragraph(cat, s_body),
                Paragraph(loc, s_body),
                url_cell,
                Paragraph(why, s_body),
                Paragraph(prio, s_prio[prio]),
            ])
            row_bgs.append(PRIORITY_BG[prio])

        tbl = Table(rows, colWidths=cw, repeatRows=1)
        ts  = TableStyle([
            ("BACKGROUND",  (0,0),(-1,0), colors.HexColor("#e8e8e8")),
            ("FONTNAME",    (0,0),(-1,0), "Helvetica-Bold"),
            ("FONTSIZE",    (0,0),(-1,-1), 7.8),
            ("VALIGN",      (0,0),(-1,-1), "TOP"),
            ("TOPPADDING",  (0,0),(-1,-1), 5),
            ("BOTTOMPADDING",(0,0),(-1,-1), 5),
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
    story.append(Paragraph("STRATEGIC TIPS", ParagraphStyle("TH", parent=styles["Heading2"],
                fontSize=12, textColor=colors.HexColor("#1A1A2E"),
                fontName="Helvetica-Bold", spaceAfter=6)))
    for tip in CLIENT_DATA["tips"]:
        story.append(Paragraph(f"→  {tip}", s_tip))

    story.append(Spacer(1, .8*cm))
    story.append(Paragraph(f"Auto-generated · {meta['date']}", s_foot))

    doc.build(story)
    print(f"✅ PDF generated: {output_path}")
    return output_path

# ─── ENTRY ────────────────────────────────────────────────────────────────────

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--output", default=".tmp/potencjalni_klienci.pdf")
    args = parser.parse_args()
    os.makedirs(os.path.dirname(args.output), exist_ok=True)
    build_pdf(args.output)
