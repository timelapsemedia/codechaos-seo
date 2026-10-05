# Erzeugt den JSON-LD-@graph der Startseite (index.html) neu, inkl. FAQPage aus den sichtbaren FAQ.
# Aufruf aus dem Repo-Root: python3 _build/schema_home.py
import re, json, html
p='index.html'; s=open(p,encoding='utf-8').read()
B='https://codechaos-official.de'
# --- FAQ from visible HTML ---
faq=[]
for q,a in re.findall(r'<details[^>]*>\s*<summary[^>]*>\s*(.*?)\s*<span[^>]*>\+</span>\s*</summary>\s*<div[^>]*>\s*<p>(.*?)</p>',s,re.S):
    clean=lambda t: re.sub(r'\s+',' ',html.unescape(re.sub(r'<[^>]+>','',t))).strip()
    faq.append({"@type":"Question","name":clean(q),"acceptedAnswer":{"@type":"Answer","text":clean(a)}})
assert len(faq)==15,len(faq)
same=["https://codechaos.bandcamp.com","https://soundcloud.com/codechaos","https://www.instagram.com/codechaos_official","https://www.tiktok.com/@codechaos_abstractsound","https://x.com/codechaos_music","https://www.threads.net/@codechaos_official","https://www.youtube.com/@codechaos_abstractsounddesign","https://www.discogs.com/artist/18204093-Code-Chaos","https://musicbrainz.org/artist/14d40d24-a91e-4600-a1b3-d14682d32e42","https://www.wikidata.org/wiki/Q141646843"]
asd={"@type":"Organization","@id":B+"/#label-asd","name":"Abstract Sound Design","url":"https://www.abstract-sound-design.de/","sameAs":["https://abstract-sound-design.bandcamp.com/","https://www.discogs.com/label/4052777-Abstract-Sound-Design","https://www.wikidata.org/wiki/Q141646831"],"foundingDate":"2021","founder":{"@id":B+"/#tim-borchert"}}
rt_tracks=["Cold Boot","Bitrot","Runtime Terror","Overdrive","Fork Bomb","Hyperthread","Ego Death","Core Dump","Night"]
graph=[
 {"@type":"WebSite","@id":B+"/#website","name":"Code Chaos","url":B+"/","inLanguage":["de","en"],"publisher":{"@id":B+"/#artist"},"hasPart":[{"@type":"WebPage","url":B+u,"name":n} for u,n in [("/psycore/","Was ist Psycore?"),("/hitech-psytrance/","Was ist Hitech Psytrance?"),("/darkpsy/","Was ist Darkpsy?"),("/crucible.html","Crucible Plugin"),("/mastering/","Psytrance Mastering"),("/en/mastering/","Psytrance Mastering (English)"),("/en/","Code Chaos (English)")]]},
 {"@type":"WebPage","@id":B+"/#webpage","url":B+"/","name":"Code Chaos · Psycore & Hitech Producer · Mastering ab 79 €",
  "description":"Offizielle Website von Code Chaos, Hitech Psytrance, Psycore und Darkpsy Producer aus Hamburg. Neue Single „Uhrwerk aus Blut“ am 30.10.2026, Diskografie, Genre Guide, Mastering und das Plugin Crucible.",
  "isPartOf":{"@id":B+"/#website"},"about":{"@id":B+"/#artist"},"mainEntity":{"@id":B+"/#artist"},
  "primaryImageOfPage":{"@type":"ImageObject","url":B+"/images/uhrwerk-aus-blut/og-uhrwerk-aus-blut.jpg","width":1200,"height":630},
  "speakable":{"@type":"SpeakableSpecification","cssSelector":["#single-info","#mastering","#was-ist-psycore","#was-ist-hitech","#was-ist-darkpsy","#bio-section"]},"significantLink":[B+"/mastering/",B+"/psycore/",B+"/hitech-psytrance/",B+"/darkpsy/",B+"/en/"],
  "inLanguage":"de","datePublished":"2024-01-01","dateModified":"2026-10-05"},
 {"@type":"MusicGroup","@id":B+"/#artist","name":"Code Chaos","alternateName":["Code-Chaos","CodeChaos"],
  "description":"Code Chaos ist ein Hitech Psytrance, Psycore und Darkpsy Producer aus Hamburg und das Studioprojekt von Tim Borchert. Eigene Bezeichnung des Sounds: New Psychedelic Death Art. Seit 2016 aktiv, über 24 Releases auf Labels wie Abstract Sound Design (2021 mitgegründet), TATEWARI Records (Mexiko) und Soma Ritual Records (Indien). Reines Studioprojekt ohne Liveshows oder DJ-Bookings.",
  "genre":["Hitech Psytrance","Psycore","Darkpsy","Dark Psytrance","Psytrance"],
  "foundingDate":"2016","foundingLocation":{"@type":"Place","name":"Hamburg","address":{"@type":"PostalAddress","addressLocality":"Hamburg","addressCountry":"DE"}},"slogan":"New Psychedelic Death Art",
  "url":B+"/","logo":B+"/images/brand/codechaos-logo-bone-480.webp","image":B+"/images/brand/portrait-press-1200.jpg",
  "sameAs":same,"member":{"@id":B+"/#tim-borchert"},
  "album":[{"@id":B+"/#runtime-terror"},{"@id":B+"/#uhrwerk-aus-blut-single"}],
  "track":{"@id":B+"/#uhrwerk-aus-blut"}},
 {"@type":"Person","@id":B+"/#tim-borchert","name":"Tim Borchert","alternateName":"Code Chaos","url":B+"/","image":B+"/images/brand/portrait-press-1200.jpg",
  "jobTitle":"Producer (Hitech Psytrance, Psycore, Darkpsy) und Mastering Engineer","nationality":{"@type":"Country","name":"Deutschland"},"homeLocation":{"@type":"Place","name":"Hamburg","address":{"@type":"PostalAddress","addressLocality":"Hamburg","addressCountry":"DE"}},
  "knowsAbout":["Psycore","Hitech Psytrance","Darkpsy","Dark Psytrance","Audio Mastering","Sounddesign","Audio-Plugin-Entwicklung"],
  "memberOf":{"@id":B+"/#artist"},"affiliation":{"@id":B+"/#label-asd"},"worksFor":{"@id":"https://polished.media/#org"},"sameAs":same},
 asd,
 {"@type":"MusicRecording","@id":B+"/#uhrwerk-aus-blut","name":"Uhrwerk aus Blut","byArtist":{"@id":B+"/#artist"},"datePublished":"2026-10-30",
  "genre":["Darkpsy","Hitech Psytrance","Gothic"],"inLanguage":"de","image":B+"/images/uhrwerk-aus-blut/cover-1600.jpg","url":B+"/#single",
  "description":"Ein Herz, das zu schnell schlägt. Ein Uhrwerk, das blutet. Neue Single von Code Chaos in fünf Szenen (Prolog, Die Uhr, Der Spiegel, Das Blut, Rückkehr), erscheint am 30.10.2026 auf Abstract Sound Design. Stimmen und Artwork mit KI erstellt.",
  "recordingOf":{"@type":"MusicComposition","name":"Uhrwerk aus Blut","composer":{"@id":B+"/#tim-borchert"}},
  "inAlbum":{"@id":B+"/#uhrwerk-aus-blut-single"},
  "potentialAction":{"@type":"ListenAction","name":"Pre-Save","target":"https://distrokid.com/hyperfollow/codechaos/uhrwerk-aus-blut-2"}},
 {"@type":"MusicAlbum","@id":B+"/#uhrwerk-aus-blut-single","name":"Uhrwerk aus Blut","albumReleaseType":"https://schema.org/SingleRelease","albumProductionType":"https://schema.org/StudioAlbum",
  "datePublished":"2026-10-30","byArtist":{"@id":B+"/#artist"},"recordLabel":{"@id":B+"/#label-asd"},"image":B+"/images/uhrwerk-aus-blut/cover-1600.jpg","numTracks":1,"track":{"@id":B+"/#uhrwerk-aus-blut"}},
 {"@type":"MusicAlbum","@id":B+"/#runtime-terror","name":"Runtime Terror","albumReleaseType":"https://schema.org/AlbumRelease","albumProductionType":"https://schema.org/StudioAlbum",
  "byArtist":{"@id":B+"/#artist"},"recordLabel":{"@id":B+"/#label-asd"},"genre":["Hitech Psytrance","Psycore","Darkpsy"],"datePublished":"2026-08-21","numTracks":9,
  "url":"https://codechaos.bandcamp.com/album/runtime-terror-lp","image":B+"/images/runtime-terror-cover.webp",
  "track":{"@type":"ItemList","numberOfItems":9,"itemListElement":[{"@type":"ListItem","position":i+1,"item":{"@type":"MusicRecording","name":t}} for i,t in enumerate(rt_tracks)]}},
 {"@type":"Organization","@id":"https://polished.media/#org","name":"Polished Media","url":"https://polished.media","email":"polished.media@gmx.de","founder":{"@id":B+"/#tim-borchert"}},
 {"@type":"Service","@id":B+"/#mastering","name":"Mastering für Psycore, Hitech Psytrance und Darkpsy","serviceType":"Audio Mastering",
  "description":"Genre-spezifisches Audio Mastering für Psycore, Hitech Psytrance und Darkpsy von einem aktiven Producer. Single (Stereo) 79 €, Stem Pro 129 €, EP bis 5 Tracks 349 €, Album bis 10 Tracks 629 €, inkl. 19 % MwSt., Audio-Audit und unbegrenzte Korrekturen.",
  "provider":{"@id":"https://polished.media/#org"},"areaServed":"Worldwide","availableLanguage":["de","en"],"url":B+"/mastering/",
  "offers":[{"@type":"Offer","name":n,"price":pr,"priceCurrency":"EUR","priceSpecification":{"@type":"PriceSpecification","price":pr,"priceCurrency":"EUR","valueAddedTaxIncluded":True}} for n,pr in [("Single: Stereo Mastering (1 Track)","79"),("Stem Pro: Stem Mastering (1 Track, bis 6 Stems)","129"),("EP Mastering (bis 5 Tracks)","349"),("Album Mastering (bis 10 Tracks)","629"),("Cover Art","99"),("Lyric Video","179"),("Promo Video (60 Sekunden)","299")]]},
 {"@type":["Product","SoftwareApplication"],"@id":B+"/crucible.html#product","name":"Crucible","url":B+"/crucible.html","brand":{"@type":"Brand","name":"Code Chaos Audio"},
  "applicationCategory":"MultimediaApplication","applicationSubCategory":"Audio Plugin","operatingSystem":"Windows 10+","softwareVersion":"1.0.0",
  "description":"3-Band Harmonic Saturation Plugin (VST3 + Standalone, Windows) von Code Chaos Audio: Low, Mid und High getrennt sättigen (Hard Clip, Wavefolder, Tube, Diode, Tape), Drive, Mix und Gain pro Band, bis zu 8x Oversampling.",
  "image":B+"/images/crucible-og.jpg",
  "offers":{"@type":"Offer","url":"https://timberwolf688.gumroad.com/l/crucible","price":"49.00","priceCurrency":"EUR","availability":"https://schema.org/InStock"}},
 {"@type":"FAQPage","@id":B+"/#faq","isPartOf":{"@id":B+"/#webpage"},"mainEntity":faq},
]
block='<script type="application/ld+json">\n'+json.dumps({"@context":"https://schema.org","@graph":graph},ensure_ascii=False,indent=1)+'\n</script>'
blocks=list(re.finditer(r'<script type="application/ld\+json">.*?</script>\n?',s,re.S))
print('removing',len(blocks))
first=blocks[0].start()
for m in reversed(blocks): s=s[:m.start()]+s[m.end():]
s=s[:first]+block+'\n'+s[first:]
open(p,'w',encoding='utf-8').write(s)
json.loads(block.split('\n',1)[1].rsplit('\n',1)[0])
print('faq',len(faq))
