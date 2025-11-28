# Schubert Lieder Corpus Analysis Summary

**Analyzed**: 94 lieder (100% success rate)
**Date**: 2025-11-28
**Purpose**: Extract compositional patterns for ML-based generation

## 🎹 Key Findings

### Key Preferences

Schubert's **favorite keys** (top 5):
1. **G major** - 10 songs (10.6%)
2. **A major** - 8 songs (8.5%)
3. **c minor** - 8 songs (8.5%)
4. **D major** - 7 songs (7.4%)
5. **a minor** - 7 songs (7.4%)

**Total unique keys used**: 21 keys

### Mode Distribution
- **Major**: 58 songs (61.7%)
- **Minor**: 36 songs (38.3%)

**Insight**: Schubert preferred major keys overall, but used minor keys significantly more than many of his contemporaries, especially in Winterreise (which is predominantly minor).

### Time Signatures

Most common meters:
1. **2/4** - 23 songs (24.5%) - Simple duple, often for folk-like or march-like songs
2. **3/4** - 20 songs (21.3%) - Waltz time, lyrical songs
3. **6/8** - 18 songs (19.1%) - Compound duple, flowing character
4. **2/2** - 15 songs (16.0%) - Alla breve, more serious character
5. **4/4** - 13 songs (13.8%) - Common time

**Insight**: Schubert favored simpler meters (2/4, 3/4) for accessibility and folk character.

## 📊 Statistical Summary

### Key Distribution Chart
```
G major   ████████████ 10
A major   ██████████ 8
c minor   ██████████ 8
D major   █████████ 7
a minor   █████████ 7
B♭ major  ████████ 6
b minor   ████████ 6
g minor   ███████ 5
C major   ███████ 5
E♭ major  ███████ 5
A♭ major  ███████ 5
```

### Mode Preference
```
Major ████████████████████████ 62%
Minor ███████████████ 38%
```

### Time Signature Distribution
```
2/4   ████████████████████████ 24%
3/4   ████████████████████ 21%
6/8   ███████████████████ 19%
2/2   ████████████████ 16%
4/4   ██████████████ 14%
Other ██ 6%
```

## 🎼 Compositional Insights

### Key Characteristics by Cycle

**Die schöne Müllerin (D795)** - 20 songs:
- Predominantly **major keys**
- Mix of simple meters (2/4, 6/8)
- Brighter, more pastoral character

**Winterreise (D911)** - 24 songs:
- More **minor keys**
- Wider variety of meters
- Darker, more introspective

**Schwanengesang (D957)** - 14 songs:
- Mix of major and minor
- Varied meters
- Diverse emotional range

### Typical Schubert Keys

**"Bright" keys** (major, sharp side):
- G major, A major, D major, E major

**"Dark" keys** (minor, flat side):
- c minor, a minor, b minor, g minor

**"Lyrical" keys** (major, flat side):
- B♭ major, E♭ major, A♭ major

## 🎯 Implications for Composition

### For ML Training

1. **Key Selection Model**:
   - Weight G major, A major, c minor, D major most heavily
   - 62% probability of major key
   - Consider emotional content when choosing key

2. **Meter Selection Model**:
   - Default to 2/4 or 3/4 (45% combined)
   - 6/8 for flowing, pastoral themes
   - 2/2 for serious, introspective songs

3. **Form Expectations**:
   - Typical length: 2-4 minutes
   - Strophic or through-composed
   - Piano introduction + multiple verses + postlude

## 📁 Data Files

- **Full analysis**: `corpus_analysis.json` (detailed data for all 94 songs)
- **Per-song data**: Available in JSON for:
  - Key and tonality
  - Harmonic progressions (first 50 chords)
  - Melodic intervals and range
  - Rhythmic patterns
  - Form structure

## 🔬 Next Steps for ML Preparation

1. **Deep Harmonic Analysis**:
   - Extract full chord progressions
   - Build Markov chain models
   - Identify cadential patterns

2. **Melodic Pattern Mining**:
   - N-gram analysis of melodic intervals
   - Phrase structure identification
   - Contour analysis

3. **Piano Texture Analysis**:
   - Identify accompaniment patterns
   - Extract left-hand/right-hand patterns
   - Categorize texture types (Alberti bass, broken chords, block chords, etc.)

4. **Text-Music Relationship**:
   - Analyze how stressed syllables map to strong beats
   - Study melismas (multiple notes per syllable)
   - Examine word-painting techniques

5. **Form Template Extraction**:
   - Identify intro/postlude patterns
   - Extract verse structures
   - Analyze key changes and modulations

## 💡 Composition Strategy

Based on this analysis, a new "Schubert" lied should:

1. **Choose key from top 5** (G major, A major, c minor, D major, a minor)
2. **Select appropriate meter** (2/4 for folk-like, 3/4 for lyrical, 6/8 for pastoral)
3. **Match key to mood**:
   - Happy/pastoral → G major, A major, D major
   - Melancholic → c minor, a minor, b minor
   - Lyrical/contemplative → B♭ major, E♭ major
4. **Follow typical form**:
   - Brief piano introduction (2-4 measures)
   - 2-4 verses with varied melody
   - Piano postlude echoing main theme
5. **Use characteristic patterns**:
   - Simple, singable melodies
   - Supportive piano accompaniment
   - Clear harmonic progressions
   - Text-sensitive phrasing

---

**Status**: Phase 1 Complete ✓
**Next**: Deep pattern analysis and ML data preparation
