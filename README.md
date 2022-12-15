# The Gospel Narrative

Tools for editing and typesetting a textual remix of Scripture telling the essential arc of the Gospel from Genesis 3 to Revelation 22.

## Quickstart

TBA

## Editing

WIP

## Typesetting

WIP

## Data

### Baseline KJV Text

The `data/` subdirectory contains the file `kjvdat.txt`, downloaded from [sacred-texts.com](https://www.sacred-texts.com/bib/osrc/index.htm).

This particular file contains the canonical books of the Bible from the "King James Version" (a.k.a. "Authorized Version") translation first published in 1611.  (As with nearly all "KJV" Bibles in circulation today, this text follows the last significant errata revision, published in 1769, updated with somewhat modernized word spellings.)

Alternate translations/languages can be used instead if their data is available in the `kjvdat.txt` format, described below.

### Data Format

The format of the file is as follows:

```
Book|Chapter|Verse| <verse text>~
```

`Chapter` is always present, even in books without explicit chapter boundaries (e.g., all of *Jude* is considered *Jude chapter 1*).

The book name abbreviations must be:

```
Gen - Genesis
Exo - Exodus
Lev - Leviticus
Num - Numbers
Deu - Deuteronomy
Jos - Joshua
Jdg - Judges
Rut - Ruth
Sa1 - I Samuel
Sa2 - II Samuel
Kg1 - I Kings
Kg2 - II Kings
Ch1 - I Chronicles
Ch2 - II Chronicles
Ezr - Ezra
Neh - Nehemiah
Est - Esther
Job - Job
Psa - Psalms
Pro - Proverbs
Ecc - Ecclesiastes
Sol - Song of Solomon
Isa - Isaiah
Jer - Jeremiah
Lam - Lamentaions
Eze - Ezekiel
Dan - Daniel
Hos - Hosea
Joe - Joel
Amo - Amos
Oba - Obadiah
Jon - Jonah
Mic - Micah
Nah - Nahum
Hab - Habbakkuk
Zep - Zephaniah
Hag - Haggai
Zac - Zechariah
Mal - Malachi
Mat - Matthew
Mar - Mark
Luk - Luke
Joh - John
Act - Acts
Rom - Romans
Co1 - I Corinthians
Co2 - II Corinthians
Gal - Galatians
Eph - Ephesians
Phi - Phillippians
Col - Colossians
Th1 - I Thessalonians
Th2 - II Thessalonians
Ti1 - I Timonthy
Ti2 - II Timothy
Tit - Titus
Plm - Philemon
Heb - Hebrews
Jam - James
Pe1 - I Peter
Pe2 - II Peter
Jo1 - I John
Jo2 - II John
Jo3 - III John
Jde - Jude
Rev - Revelation
```


