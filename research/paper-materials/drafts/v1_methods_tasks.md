# Methods §2.3 — Experimental Paradigms (Draft v1)
**Paper:** Grid-Based Spatiotemporal Encoding of fNIRS Signals for GAD Classification Using a 3D Vision Transformer  
**Target:** IEEE Transactions on Neural Systems and Rehabilitation Engineering (TNSRE)  
**Word count (body prose):** ~355 words  
**Status:** Draft v1 — 2026-04-29  

---

## C. Experimental Paradigms

Four cognitive paradigms were administered to probe distinct dimensions of prefrontal executive function, each known to elicit task-related hemodynamic responses over the prefrontal cortex. Trial onsets were identified from the continuous fNIRS recording using event codes 3.0 and 4.0. For each paradigm, a fixed epoch was extracted relative to task onset, and the initial seconds were discarded to exclude the motor preparation and stimulus-instruction phase, yielding an effective trial window aligned to the active cognitive engagement period. Task design diagrams are shown in Fig. 3–6.

The **Go/No-Go (GNG)** task required participants to execute a speeded motor response to frequent "Go" stimuli while suppressing their prepotent response to infrequent "No-Go" stimuli, placing demands on inhibitory control and sustained attention [REF]. Epochs were extracted over a 0–35 s window relative to onset; the first 3 s were removed as the preparation interval, yielding an effective trial duration of 32 s (Fig. 3).

The **Stop-Signal (SS)** task probed reactive response inhibition by requiring participants to suppress an already-initiated motor response when an unpredictable stop signal appeared after a variable stop-signal delay [REF]. The stochastic delay structure imposes a greater cognitive demand on inhibitory control relative to the GNG paradigm. Epochs spanned 0–60 s from onset; the first 7 s were discarded, leaving an effective duration of 53 s (Fig. 4).

The **1-Back Working Memory (1backWM)** task required participants to judge whether each stimulus matched the one presented one trial previously, continuously engaging executive attention, stimulus updating, and short-term memory maintenance [REF]. Given the sustained nature of working memory engagement, epochs were extracted over a 0–90 s window with the first 5 s excluded, yielding an effective duration of 85 s — the longest among the four paradigms (Fig. 5).

The **Verbal Fluency (VF)** task required participants to generate words belonging to a designated semantic category within a fixed time period, engaging phonological access, semantic retrieval, and self-monitoring processes [REF]. Epochs spanned 0–60 s from onset; the first 7 s were discarded as preparation, yielding an effective duration of 53 s (Fig. 6).

---

### Epoch Summary Table

| Task | Raw Window (s) | Preparation Crop (s) | Effective Duration (s) | Event Codes |
|---|---|---|---|---|
| Go/No-Go (GNG) | 0–35 | 3 | **32** | 3.0 / 4.0 |
| Stop-Signal (SS) | 0–60 | 7 | **53** | 3.0 / 4.0 |
| 1-Back Working Memory (1backWM) | 0–90 | 5 | **85** | 3.0 / 4.0 |
| Verbal Fluency (VF) | 0–60 | 7 | **53** | 3.0 / 4.0 |

### Figure References for This Section

| Placeholder | File | Content |
|---|---|---|
| Fig. 3 | `GNG.tif` | Go/No-Go task paradigm diagram |
| Fig. 4 | `SS.tif` | Stop-Signal task paradigm diagram |
| Fig. 5 | `1backWM.tif` | 1-Back Working Memory paradigm diagram |
| Fig. 6 | `VF.tif` | Verbal Fluency paradigm diagram |

*Note: Fig. 3–6 numbering is a placeholder pending final figure ordering in the assembled manuscript.*

### Citation Placeholders

| Tag | Description |
|---|---|
| [REF] after GNG | Standard GNG citation — e.g., Aron & Poldrack 2006, or a task-validation reference used by dataset author |
| [REF] after SS | Standard Stop-Signal citation — e.g., Logan et al. 1984 / Verbruggen & Logan 2008 |
| [REF] after 1backWM | n-back / 1-back WM citation — e.g., Owen et al. 2005 or Jaeggi et al. 2010 |
| [REF] after VF | Verbal Fluency citation — e.g., Benton & Hamsher 1976, or Troyer et al. 1997 |
