export type SourceLink = {
  label: string;
  url: string;
  kind: "project" | "shared" | "doc";
};

const LIVE_WORKSPACE_URL = "https://example.com/live-workspace";
const SHARED_THREAD_SNAPSHOT_URL = "https://example.com/shared-thread-snapshot";

export const sources: SourceLink[] = [
  {
    label: "Live workspace",
    url: LIVE_WORKSPACE_URL,
    kind: "project",
  },
  {
    label: "Shared thread snapshot",
    url: SHARED_THREAD_SNAPSHOT_URL,
    kind: "shared",
  },
];

export const catherineMobiusPatchGuide = String.raw`
# Catherine Mobius Integration Patch Guide

If a build fails with \"Unterminated string constant\", it is usually caused by a
long Markdown/YAML blob embedded inside a normal string. Use \`String.raw\`...\`
(or move the blob into \`/public/*.md|*.yaml\` and fetch it) to preserve newlines,
quotes, and backticks without escaping every line.

## Recommended Patch

1. Replace the unsafe string literal with a \`String.raw\` template literal.
2. Keep long Markdown or YAML content in a separate asset for safer edits.
3. Store provenance URLs in a \`sources\` array so the UI can render both the
   live workspace and the frozen shared snapshot.

## Example

\`\`\`ts
export const guide = String.raw\`
# Patch
- Use String.raw
\`\`\`;
\`\`\`
`;
