import { Presentation } from "@oai/artifact-tool";
const p = await Presentation.load("C:/Users/LENOVO/OneDrive/Робочий стіл/Навчання/6 Створення ПЗ/ДЗ/дз1/Практика 1. Проєктна пропозиція.pptx");
const i = await p.inspect({kind:"slide,textbox,shape,image,layout", maxChars:20000});
console.log(i.ndjson);
console.log('slides', p.slides.items.length);
