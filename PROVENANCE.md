# Provenance

- `ui/buddy_voice_bridge_ui.jsx` comes from mounted carrier SHA-256 `a79e57bcc3627c0f61658f8b9a8d4eca9a82da211575f9b97a4daaee37ca6617`.
- It is a frontend contract that calls `POST /api/filter`; the backend was not present in the intake.
- `contracts/voice_touch_trace_contract.json` is cast from a direct user directive on 2026-08-31 and preserves immutable `(x,y,z,w)` trace samples across voice and future touch input.

The branch does not claim improved word-error rate, noise robustness, or deployed speech recognition. Those require a model, dataset, benchmark protocol, and results.
