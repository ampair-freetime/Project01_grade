import { reactive } from 'vue'

// UI-only fixtures. No API or persistence; reload to restore the demo.
export const demoTerms = reactive([
  { id: '2569-1', label: '1 / 2569', current: true },
  { id: '2569-2', label: '2 / 2569', current: false },
  { id: '2570-1', label: '1 / 2570', current: false },
])
export const enrollmentDemo = reactive({
  selectedId: 'sample',
  sections: [{
    id: 'sample', name: 'Software Development', courseCode: 'CS212',
    section: '001', termId: '2569-1', code: 'K7MX2P', open: true, joined: false,
    students: [
      { id: '690510101', name: 'กมลชนก ใจดี', initials: 'กม' },
      { id: '690510108', name: 'ณัฐพล วัฒนกุล', initials: 'ณั' },
      { id: '690510115', name: 'พิมพ์ชนก สุขใจ', initials: 'พิ' },
    ],
  }],
})
function newCode() {
  const alphabet = 'ABCDEFGHJKLMNPQRSTUVWXYZ23456789'
  let code
  do {
    code = Array.from(crypto.getRandomValues(new Uint32Array(6)), value => alphabet[value % alphabet.length]).join('')
  } while (enrollmentDemo.sections.some(section => section.code === code))
  return code
}
export function addDemoSection(values) {
  const section = { ...values, id: crypto.randomUUID(), code: newCode(), open: true, joined: false, students: [] }
  enrollmentDemo.sections.push(section)
  enrollmentDemo.selectedId = section.id
}
export function joinDemoCourse(section) {
  if (section.joined || !section.open) return
  section.joined = true
  section.students.push({ id: '690510129', name: 'ธนกฤต แสงแก้ว', initials: 'ธน' })
}
export function regenerateDemoCode(section) { section.code = newCode() }
