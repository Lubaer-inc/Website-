/*
  Hier pflegst du die Inhalte der Website – ohne HTML anfassen zu müssen.

  WERKE
  - Bild in den Ordner images/werke/ legen (am besten JPG, ca. 2000 px lange Seite).
  - Einen Eintrag unten ergänzen, z. B.:
      { titel: "Ohne Titel", jahr: 2025, technik: "Öl auf Leinwand", masse: "120 × 90 cm",
        kategorie: "Malerei", bild: "images/werke/ohne-titel.jpg" },
  - Solange "bild" fehlt, wird eine farbige Platzhalterfläche angezeigt.

  AUSSTELLUNGEN
  - Neueste zuerst eintragen. "art" z. B. "Einzelausstellung" oder "Gruppenausstellung".
*/

const WERKE = [
  { titel: "Werk I",   jahr: 2026, technik: "Öl auf Leinwand",       masse: "120 × 90 cm", kategorie: "Malerei",      farbe: "#c9b79c" },
  { titel: "Werk II",  jahr: 2026, technik: "Acryl auf Leinwand",    masse: "80 × 80 cm",  kategorie: "Malerei",      farbe: "#8a9a8b" },
  { titel: "Werk III", jahr: 2025, technik: "Tusche auf Papier",     masse: "42 × 30 cm",  kategorie: "Zeichnung",    farbe: "#d8d4cc" },
  { titel: "Werk IV",  jahr: 2025, technik: "Mischtechnik",          masse: "150 × 110 cm",kategorie: "Malerei",      farbe: "#a0543f" },
  { titel: "Werk V",   jahr: 2024, technik: "Holz, Stahl, Licht",    masse: "Maße variabel", kategorie: "Installation", farbe: "#3f4a5a" },
  { titel: "Werk VI",  jahr: 2024, technik: "Graphit auf Papier",    masse: "70 × 50 cm",  kategorie: "Zeichnung",    farbe: "#b5b0a6" },
];

const AUSSTELLUNGEN = [
  { jahr: 2026, titel: "Titel der Ausstellung", ort: "Galerie, Stadt",    art: "Einzelausstellung" },
  { jahr: 2025, titel: "Titel der Ausstellung", ort: "Kunstverein, Stadt", art: "Gruppenausstellung" },
  { jahr: 2024, titel: "Titel der Ausstellung", ort: "Projektraum, Stadt", art: "Gruppenausstellung" },
];
