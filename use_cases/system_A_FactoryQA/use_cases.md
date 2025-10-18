# Factory QA — Use Cases

- Defect detection (surface/structural): identify scratches, dents, cracks; value: reduce escapes; signals: texture/edge anomalies
- Missing component detection: verify presence of screws, clips, labels; value: assembly completeness; signals: part confidence deficits
- Misalignment detection: detect off-axis placement; value: tolerance compliance; signals: pose deviation thresholds
- Wrong orientation detection: catch flipped or rotated parts; value: avoid downstream jams; signals: angle out-of-spec
- Color and finish verification: detect paint/coating variance; value: cosmetic QA; signals: calibrated color metrics
- Barcode/QR verification: read/validate codes; value: traceability; signals: OCR/decoding success
- Serial/OCR validation: read stamped text; value: genealogy; signals: OCR confidence + schema checks
- Dimensional compliance: approximate width/height from pose; value: tolerance checks; signals: projected distances
- Assembly verification: confirm subassemblies; value: process integrity; signals: multi-part pose agreement
- Packaging QA: seal/label placement correctness; value: shipping quality; signals: bounding pose regions
- Foreign object detection: detect unwanted items; value: safety; signals: out-of-catalog parts
- Rework triaging: route fails with overlays; value: reduce rework time; signals: defect type/region
- Line changeover validation: confirm new SKU parts; value: reduce misbuilds; signals: catalog ID match
