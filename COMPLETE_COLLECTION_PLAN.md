# Complete Schubert Collection Plan

**Goal**: Acquire every available machine-readable Schubert score

**Current Status**: 96 scores (94 lieder + 2 others)
**Target**: 300-400 scores (realistic maximum based on availability)

## ✅ What We Have (96 scores)

### Lieder - 94 songs
- ✓ D795 - Die schöne Müllerin (20 songs) - COMPLETE
- ✓ D911 - Winterreise (24 songs) - COMPLETE
- ✓ D957 - Schwanengesang (14 songs) - COMPLETE
- ✓ D877 - 4 Gesänge aus Wilhelm Meister
- ✓ Various opus collections (36 songs)
- ✓ Famous songs: Erlkönig, Ave Maria, An die Musik, Gretchen am Spinnrade, Die Forelle

### Chamber Music - 1 work
- ✓ D667 - Piano Quintet "Trout"

### Piano - 1 work
- ✓ D899 - Four Impromptus Op. 90

## 🎯 Priority Additions (Essential Masterpieces)

### Symphonies (2 works) - HIGH PRIORITY
1. **D759 - Symphony No. 8 "Unfinished"** (1822)
   - Source: IMSLP
   - Format: MusicXML available
   - Difficulty: Manual download required

2. **D944 - Symphony No. 9 "Great C major"** (1825-1826)
   - Source: IMSLP
   - Format: MusicXML available
   - Difficulty: Manual download required

### Chamber Music (5-8 works) - HIGH PRIORITY
3. **D810 - String Quartet No. 14 "Death and the Maiden"** (1824)
   - Source: IMSLP, Kern Scores
   - One of Schubert's greatest chamber works

4. **D956 - String Quintet in C major** (1828)
   - Source: IMSLP
   - Considered his greatest chamber work

5. **D929 - Piano Trio No. 2 in E-flat major** (1827)
   - Source: IMSLP

6. **D887 - String Quartet No. 15 in G major** (1826)
   - Source: IMSLP

7. **D574 - String Quartet No. 13 "Rosamunde"** (1824)
   - Source: IMSLP

8. **D898 - String Trio in B-flat major** (1817)
   - Source: IMSLP

### Piano Works (10-15 works) - HIGH PRIORITY
9. **D960 - Piano Sonata No. 21 in B-flat major** (1828)
   - Source: MuseScore, IMSLP
   - His last and greatest piano sonata

10. **D958 - Piano Sonata No. 19 in C minor** (1828)
    - Source: MuseScore, IMSLP

11. **D959 - Piano Sonata No. 20 in A major** (1828)
    - Source: MuseScore, IMSLP

12. **D935 - Four Impromptus Op. 142** (1827)
    - Source: MuseScore, IMSLP
    - Companion to D899

13. **D780 - Six Moments Musicaux** (1823-1828)
    - Source: MuseScore, IMSLP

14. **D850 - Piano Sonata No. 17 in D major "Gasteiner"** (1825)
    - Source: MuseScore, IMSLP

15. **D845 - Piano Sonata No. 16 in A minor** (1825)
    - Source: MuseScore

16. **D784 - Piano Sonata No. 15 in C major "Reliquie"** (1825)
    - Source: MuseScore

17. **D894 - Fantasia in C major "Wanderer Fantasy"** (1822)
    - Source: MuseScore, IMSLP

18. **D899 - Allegretto in C minor** (1827)
    - Source: MuseScore

### More Lieder (50-100 additional songs) - MEDIUM PRIORITY
19. **Individual famous songs not yet in collection**:
    - D531 - Der Tod und das Mädchen
    - D296 - Rastlose Liebe
    - D539 - Der Wanderer
    - D160 - Heidenröslein
    - D263 - Der Fischer
    - Many more from MuseScore/IMSLP

## 🔍 Where to Find Them

### **IMSLP (Most Comprehensive)**
URL: https://imslp.org/wiki/Category:Schubert,_Franz

**How to download**:
1. Go to specific work page (search by D number or title)
2. Look for "MusicXML" or "MuseScore" files in the file list
3. Download and save to appropriate `scores/musicxml/[category]/` folder
4. Rename to: `D###_title.musicxml`

**Available**:
- Most symphonies (MusicXML)
- Major chamber works (MusicXML)
- Some piano sonatas (MusicXML)
- Many lieder (MusicXML)

### **MuseScore.com (Easy Downloads)**
URL: https://musescore.com

**How to download**:
1. Search: "Schubert D###" or title
2. Click on score
3. Click "Download" → Select "MusicXML"
4. Save to appropriate folder

**Available**:
- All major piano works
- Popular chamber music
- Many lieder
- Some symphonies

**Quality**: Community transcriptions, usually good quality

### **Kern Scores (Best for Analysis)**
URL: http://kern.humdrum.org/search?s=t&keyword=schubert

**Available**:
- Selected string quartets in Humdrum format (.krn)
- Some piano works
- Excellent for computational analysis

**How to download**:
1. Browse catalog
2. Download .krn files
3. Save to `scores/humdrum/[category]/`
4. Can convert to MusicXML with our tools

### **Other Potential Sources**
1. **CPDL (ChoralWiki)** - Sacred choral works
   - http://www.cpdl.org/

2. **Mutopia Project** - Some Schubert works
   - https://www.mutopiaproject.org/

3. **MusOpen** - Public domain recordings and scores
   - https://musopen.org/

## 📋 Systematic Download Process

### Phase 1: Essential Masterpieces (Priority 1-18 above)
**Estimated**: 25-30 works
**Time**: 2-4 hours manual work
**Result**: Core collection of absolute masterpieces

### Phase 2: Complete Categories
**Piano**: All 21 piano sonatas + character pieces
**Chamber**: All mature string quartets, trios, quintets
**Symphonies**: All 9 symphonies (if available)
**Estimated**: 50-75 additional works

### Phase 3: Extended Lieder Collection
**Goal**: Expand to 200+ songs
**Sources**: MuseScore, IMSLP individual songs
**Estimated**: 100-150 additional songs

### Phase 4: Rare & Lesser-Known Works
**Sacred music**: Masses, sacred songs
**Stage works**: Operatic excerpts if available
**Dances & occasional pieces**: If in MusicXML

## 🤖 Semi-Automated Approach

Since IMSLP and MuseScore don't have public APIs I can use, here's the workflow:

### For YOU to do (Manual):
1. Open IMSLP/MuseScore
2. Search for work
3. Download MusicXML file
4. Save to appropriate folder with naming: `D###_title.musicxml`

### For ME to do (Automated):
```bash
# After you download files to a temporary folder:
python tools/convert_formats.py temp_downloads/ scores/musicxml/ --format musicxml --batch
python tools/analyze_scores.py scores/musicxml/[category]/*.musicxml --validate
```

## 📊 Realistic Collection Estimates

### Conservative Estimate (With Manual Work)
- **Lieder**: 150-200 songs (from 600+ total)
- **Piano**: 30-40 works (from 200+ total)
- **Chamber**: 20-30 works (from 100+ total)
- **Symphonies**: 5-9 works (from 9 total)
- **Other**: 10-20 works
- **TOTAL**: **215-299 scores** (20-30% of Schubert's output)

### Optimistic Estimate (Maximum Available)
- **Lieder**: 250-300 songs
- **Piano**: 50-70 works
- **Chamber**: 30-40 works
- **Symphonies**: 9 works
- **Other**: 20-30 works
- **TOTAL**: **359-449 scores** (35-45% of Schubert's output)

### What's NOT Available (Yet)
- Most stage works (operas, singspiels) - only PDFs
- Many sacred works - only PDFs
- Fragmentary/early works - mostly unpublished
- Orchestral dances - limited availability
- Many songs - not yet digitized

## 🎯 Next Steps

### Immediate (Today):
1. Create detailed download checklist for priority works
2. Document manual download process
3. Set up folder structure for new categories

### Short-term (This Week):
1. Download priority symphonies (D759, D944)
2. Download major chamber works (D810, D956)
3. Download remaining piano masterpieces (D960, D935, D780)

### Medium-term (This Month):
1. Systematically download all available piano sonatas
2. Collect all string quartets
3. Expand lieder collection to 200+ songs

### Long-term (Ongoing):
1. Monitor IMSLP for new additions
2. Check MuseScore for community transcriptions
3. Contribute metadata for all collected works

## 💡 Community Contribution Idea

We could:
1. Document which works are still needed
2. Coordinate with digital score projects
3. Potentially help transcribe missing works
4. Contribute back to OpenScore/IMSLP

---

**Bottom Line**: We can realistically get **200-400 scores** (20-40% of Schubert's output) in machine-readable formats. The rest require either:
- Manual transcription from PDFs
- Access to scholarly editions
- Discovery in archives

Let's focus on what's achievable and build the best Schubert analysis collection possible!
