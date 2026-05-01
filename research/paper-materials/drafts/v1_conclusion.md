# Section 6 — Conclusion (Draft v1)
**Paper:** Grid-Based Spatiotemporal Encoding of fNIRS Signals for GAD Classification Using a 3D Vision Transformer  
**Target:** IEEE Transactions on Neural Systems and Rehabilitation Engineering (TNSRE)  
**Word count (body prose):** ~210 words  
**Status:** Draft v1 updated — 2026-05-01 (future work expanded: motion correction reason filled; channel explainability added method-agnostic per 3-agent evaluation)

---

## VI. Conclusion

This paper presented a novel 1D→2D→3D encoding pipeline for fNIRS signals that
preserves the anatomical spatial arrangement of prefrontal optodes in a 5×7 grid,
enabling the construction of video-like clip tensors amenable to spatiotemporal
processing by a 3D Vision Transformer. Statistical analysis justified the selection of
total haemoglobin as the primary hemodynamic measure, with HbT achieving statistically
significant group discrimination at the most diagnostically responsive channel
(S7_D6: *p* = 0.026, Cohen's *d* = 0.64) while HbO and HbR did not. The Go/No-Go
paradigm was identified as the optimal cognitive task based on three convergent lines
of evidence — cross-strategy consistency, neuropsychological specificity to GAD
inhibitory deficits, and minimal task duration (32 s) — and was evaluated using
Configuration C (temporal clip *T* = 256, tubelet patch (16, 8, 8)), which captured
the full haemodynamic response function and outperformed shorter configurations on all
ablation metrics. Under 10-fold cross-validation, the GNG–HbT model achieved an
accuracy of 88.4%; under leave-one-subject-out cross-validation across all 48
participants, it achieved Acc = 71.4%, Sens = 95.3%, Spec = 59.4%, and κ = 0.459,
confirming cross-subject generalisation. These results demonstrate that topology-preserving
spatiotemporal encoding of fNIRS signals provides a viable, portable, and objective
approach to GAD screening that complements existing self-report instruments such as the
GAD-7 and STAI. Future work will prioritise wavelet-based motion correction combined with
Correlation-Based Signal Improvement (CBSI) preprocessing to mitigate the artefact-driven
false-positive GAD classifications observed in 13 of 32 HC participants under LOSO, thereby
improving cross-subject specificity in the aging cohort. Channel contribution analysis via
ViT attention map extraction is additionally planned to identify which prefrontal optodes
are most informative for HC vs. GAD discrimination and to guide targeted sensor reduction
for clinical deployment. An age-matched cohort replication remains a critical priority to
disentangle haemodynamic aging confounds from GAD-specific prefrontal dysregulation.

---

### Notes for Final Assembly

- No citation placeholders required in this section — the conclusion does not introduce new references.
- If the 10-fold 88.4% figure changes in the final results, it is the only number in this section that may need updating; all LOSO metrics are confirmed.
- TNSRE does not require a separate sub-heading for the Conclusion; the section number (VI) is sufficient.
