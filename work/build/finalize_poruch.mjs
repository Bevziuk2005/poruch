import path from "node:path";
import { pathToFileURL } from "node:url";
const workspaceDir = "D:/Codex/2026-10-25/new-chat";
const SKILL_DIR = "C:/Users/LENOVO/.codex/plugins/cache/openai-primary-runtime/presentations/26.1024.11018/skills/presentations";
const candidatePath = path.join(workspaceDir,"work","build","poruch-draft.pptx");
const finalPath = path.join(workspaceDir,"work","build","poruch-final.pptx");
const { finalizePresentation } = await import(pathToFileURL(path.join(SKILL_DIR,"container_tools/artifact_tool_utils.mjs")).href);
const stagingDir = path.join(workspaceDir,"work",".codex-finalizer");
await (await import("node:fs/promises")).mkdir(stagingDir,{recursive:true});
await (await import("node:fs/promises")).mkdir(path.dirname(finalPath),{recursive:true});
const result = await finalizePresentation({
  explicitTotalSlideCount: 12,
  workspaceDir,
  candidatePath,
  finalPath,
  pythonExecutable: "C:/Users/LENOVO/.cache/codex-runtimes/codex-primary-runtime/dependencies/python/python.exe",
  integrityValidatorPath: path.join(SKILL_DIR,"container_tools/inspect_presentation_package_integrity.py"),
  layoutValidatorPath: path.join(SKILL_DIR,"container_tools/inspect_presentation_layout_geometry.py"),
  layoutArgs: ["--expected-slide-size-emu","12192000,6858000","--validate-heading-fit"],
  fontPolicy: { basis:"design", families:["Aptos"] },
  verifyArtifactToolImport: true,
  receiptPath: path.join(stagingDir,"poruch-validation.json"),
});
console.log(JSON.stringify(result,null,2));

