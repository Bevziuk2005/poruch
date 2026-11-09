import { Presentation } from "file:///C:/Users/LENOVO/.cache/codex-runtimes/codex-primary-runtime/dependencies/node/node_modules/@oai/artifact-tool/dist/artifact_tool.mjs";
const p = await Presentation.load("C:/Users/LENOVO/OneDrive/Робочий стіл/Навчання/6 Створення ПЗ/ДЗ/дз1/Практика 1. Проєктна пропозиція.pptx");
const i = await p.inspect({kind:"slide,textbox,shape,image,layout", maxChars:20000});
console.log(i.ndjson);
console.log('slides', p.slides.items.length);
