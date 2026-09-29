<script setup>
import { computed, reactive, ref, watch } from 'vue'
import { enrollmentDemo as store, demoTerms, addDemoSection, joinDemoCourse, regenerateDemoCode } from './enrollmentState'

const demo = computed(() => store.sections.find(section => section.id === store.selectedId))
const props = defineProps({ role: { type: String, default: 'student' } })
const teacher = computed(() => props.role === 'teacher')
const code = ref('')
const search = ref('')
const studentSearch = ref('')
const stage = ref('input')
const error = ref('')
const notice = ref('')
const confirmReset = ref(false)
const enrollmentOpen = ref(true)
const joinDialog = ref(null)
const profileOpen = ref(false)
const courseDialog = ref(null)
const createDialog = ref(null)
const createMode = ref('course')
const formError = ref('')
const addingSemester = ref(false)
const semesterError = ref('')
const newSemester = reactive({ year: '', semester: '1' })
function openSemesterForm() {
  newSemester.year = form.termId.split('-')[0]
  newSemester.semester = '1'
  semesterError.value = ''
  addingSemester.value = true
}
function saveSemester() {
  const year = newSemester.year.trim()
  if (!/^[1-9][0-9]{3}$/.test(year)) {
    semesterError.value = 'Enter a 4-digit academic year, e.g. 2570.'
    return
  }
  const id = `${year}-${newSemester.semester}`
  if (!demoTerms.some(term => term.id === id)) {
    demoTerms.push({ id, label: `${newSemester.semester === 'summer' ? 'Summer' : newSemester.semester} / ${year}`, current: false })
  }
  form.termId = id
  semesterError.value = ''
  addingSemester.value = false
}
const form = reactive({ name: '', courseCode: '', section: '001', termId: '2569-1' })
const termFilter = ref('all')
const termLabel = id => demoTerms.find(term => term.id === id)?.label ?? id
const matchesSearch = section => `${section.name} ${section.courseCode}`.toLowerCase().includes(search.value.trim().toLowerCase())
const filteredCourses = computed(() => store.sections.filter(section => matchesSearch(section) && (termFilter.value === 'all' || section.termId === termFilter.value)))
const joinedCourses = computed(() => store.sections.filter(section => section.joined))
const visibleJoinedCourses = computed(() => joinedCourses.value.filter(matchesSearch))
const filteredStudents = computed(() => demo.value.students.filter(student => (student.name + ' ' + student.id).toLowerCase().includes(studentSearch.value.trim().toLowerCase())))
const showCourse = computed(() => filteredCourses.value.some(section => section.id === demo.value.id))
function selectSection(section) {
  studentSearch.value = ''
  if (store.selectedId === section.id) enrollmentOpen.value = !enrollmentOpen.value
  else { store.selectedId = section.id; enrollmentOpen.value = true }
  notice.value = ''
  confirmReset.value = false
}
function openCreate(section = null) {
  addingSemester.value = false
  semesterError.value = ''
  createMode.value = section ? 'section' : 'course'
  Object.assign(form, { name: section?.name ?? '', courseCode: section?.courseCode ?? '', section: '', termId: '2569-1' })
  formError.value = ''
  createDialog.value.showModal()
}
function createCourse() {
  if (addingSemester.value) return
  const values = { name: form.name.trim(), courseCode: form.courseCode.trim().toUpperCase(), section: form.section.trim(), termId: form.termId }
  if (!values.name || !values.courseCode || !values.section) { formError.value = 'Please complete all fields.'; return }
  const existing = store.sections.filter(section => section.courseCode === values.courseCode)
  if (createMode.value === 'course' && existing.length) { formError.value = 'This course code already exists. Use Add Section on the existing course.'; return }
  if (existing.some(section => section.termId === values.termId && section.section.toLowerCase() === values.section.toLowerCase())) {
    formError.value = 'This section already exists in the selected semester.'
    return
  }
  addDemoSection(values)
  search.value = ''
  termFilter.value = 'all'
  enrollmentOpen.value = true
  confirmReset.value = false
  notice.value = `${values.name} · Section ${values.section} created. The join code is ready to share.`
  createDialog.value.close()
}
watch(() => props.role, () => {
  joinDialog.value?.close()
  courseDialog.value?.close()
  createDialog.value?.close()
  stage.value = 'input'
  error.value = ''
  notice.value = ''
  search.value = ''
  profileOpen.value = false
  confirmReset.value = false
})
watch(code, () => { error.value = '' })
function openJoin() {
  code.value = ''
  error.value = ''
  stage.value = 'input'
  joinDialog.value.showModal()
}
function findCourse() {
  error.value = ''
  const match = store.sections.find(section => section.code === code.value.trim().toUpperCase())
  if (!match) {
    error.value = 'Invalid join code. Please check the code and try again.'
    return
  }
  store.selectedId = match.id
  if (match.joined) {
    error.value = 'You are already enrolled in this course.'
    return
  }
  if (!match.open) {
    error.value = 'Enrollment is closed. Please contact your teacher.'
    return
  }
  if (store.sections.some(section => section.joined && section.courseCode === match.courseCode && section.termId === match.termId && section.id !== match.id)) {
    error.value = 'You are enrolled in another section of this course this semester. Contact your teacher to transfer.'
    return
  }
  stage.value = 'review'
}
function enroll() {
  if (code.value.trim().toUpperCase() !== demo.value.code || !demo.value.open) {
    stage.value = 'input'
    findCourse()
    return
  }
  joinDemoCourse(demo.value)
  stage.value = 'success'
}
async function copyCode() {
  try {
    await navigator.clipboard.writeText(demo.value.code)
    notice.value = 'Join code copied.'
  } catch {
    notice.value = `Copy this code manually: ${demo.value.code}`
  }
}
function resetCode() {
  regenerateDemoCode(demo.value)
  confirmReset.value = false
  notice.value = 'New code created. Existing enrollments are unchanged.'
}
</script>

<template>
  <div class="enroll-demo" :class="{ 'student-page': !teacher }">
    <!-- Same header structure and dimensions as CourseManagement and Dashboard. -->
    <header class="portal-header">
      <div class="header-inner">
        <div class="brand">
          <span class="brand-icon material-symbols-outlined" aria-hidden="true">school</span>
          <h2>University Grade Portal</h2>
        </div>
        <div class="header-actions">
          <div class="profile-wrap">
            <button class="profile-button" :aria-expanded="profileOpen" @click="profileOpen = !profileOpen">
              <strong>{{ teacher ? 'Orapan' : 'Thanakrit' }}</strong>
              <span class="avatar">{{ teacher ? 'OV' : 'TS' }}</span>
            </button>
            <div v-if="profileOpen" class="profile-dropdown">
              <strong>{{ teacher ? 'Orapan Wichai' : 'Thanakrit Saengkaew' }}</strong>
              <p>{{ teacher ? 'Teacher' : 'Student ID: 690510129' }}</p>
              <p>Demo profile</p>
            </div>
          </div>
          <button class="icon-button logout" aria-label="Log out of demo" @click="notice = 'This is a UI demo. No account is signed in.'">
            <span class="material-symbols-outlined" aria-hidden="true">logout</span>
          </button>
        </div>
      </div>
    </header>

    <main class="page-content">
      <div class="demo-bar">
        <span>Enrollment demo <span class="demo-caption">· Sample data only</span></span>
        <nav class="role-switch" aria-label="Demo view">
          <RouterLink to="/demo/enrollment/teacher" :class="{ selected: teacher }">Teacher</RouterLink>
          <RouterLink to="/demo/enrollment/student" :class="{ selected: !teacher }">Student</RouterLink>
        </nav>
      </div>
      <p v-if="notice" class="notice" role="status">{{ notice }}</p>

      <template v-if="teacher">
        <h1>Course Management</h1>
        <div class="toolbar panel">
          <label class="search-field teacher-search">
            <span class="material-symbols-outlined" aria-hidden="true">search</span>
            <input v-model="search" aria-label="Search courses" placeholder="Search Course Code or Name..." />
          </label>
          <div class="toolbar-actions"><select v-model="termFilter" class="term-filter" aria-label="Filter semester"><option value="all">All semesters</option><option v-for="term in demoTerms" :key="term.id" :value="term.id">Semester {{ term.label }}</option></select><button class="button primary" @click="openCreate()"><span class="material-symbols-outlined" aria-hidden="true">add</span>Create Course</button></div>
        </div>

        <section class="panel course-list" aria-label="Courses">
          <div class="list-heading"><span>Course Info</span><div><span>Enrolled</span><span>Actions</span></div></div>
          <div v-for="course in filteredCourses" :key="course.id" class="teacher-course-row">
            <div class="course-info">
              <h2>{{ course.name }}</h2>
              <p>Course ID: {{ course.courseCode }}</p>
              <p>Section: {{ course.section }} · Semester {{ termLabel(course.termId) }}</p>
            </div>
            <div class="course-actions">
              <div class="student-count"><strong><span class="material-symbols-outlined" aria-hidden="true">people</span>{{ course.students.length }}</strong><span>Students</span></div>
              <button class="icon-button" :aria-label="`Add Section to ${course.name}`" @click="openCreate(course)"><span class="material-symbols-outlined" aria-hidden="true">add</span></button>
              <button class="button secondary" :aria-expanded="enrollmentOpen && demo.id === course.id" aria-controls="enrollment-settings" @click="selectSection(course)">
                <span class="material-symbols-outlined" aria-hidden="true">group_add</span>Enrollment
              </button>
            </div>
          </div>
          <p v-if="!filteredCourses.length" class="empty-search">No courses found.</p>
        </section>

        <section v-if="enrollmentOpen && showCourse" id="enrollment-settings" class="panel enrollment-panel">
          <div class="panel-heading">
            <div><h2>Course Enrollment</h2><p>{{ demo.name }} · Section {{ demo.section }} · Semester {{ termLabel(demo.termId) }}</p></div>
            <span class="badge" :class="demo.open ? 'green' : 'neutral'">{{ demo.open ? 'Enrollment open' : 'Enrollment closed' }}</span>
          </div>
          <div class="enrollment-body">
            <div class="join-code-section">
              <label>Class join code</label>
              <p>Share this code with students to join your course.</p>
              <div class="code-box"><strong>{{ demo.code }}</strong><button class="button primary" @click="copyCode"><span class="material-symbols-outlined" aria-hidden="true">content_copy</span>Copy Code</button></div>
            </div>
            <div class="settings-section">
              <div class="setting-row"><div><strong>Allow enrollment</strong><p>Students with the code can join immediately.</p></div><button class="toggle" :class="{ on: demo.open }" role="switch" :aria-checked="demo.open" aria-label="Allow enrollment" @click="demo.open = !demo.open"><span></span></button></div>
              <div class="reset-row"><div><strong>Reset join code</strong><p>Existing students stay enrolled.</p></div><button class="icon-button" aria-label="Reset join code" @click="confirmReset = !confirmReset"><span class="material-symbols-outlined" aria-hidden="true">refresh</span></button></div>
              <div v-if="confirmReset" class="inline-confirm"><p>The current code will stop working. Create a new code?</p><div class="actions"><button class="button secondary" @click="confirmReset = false">Cancel</button><button class="button primary" @click="resetCode">Create New Code</button></div></div>
            </div>
          </div>
          <div class="roster-heading"><h3>Enrolled Students <span class="count-chip">{{ demo.students.length }}</span></h3><label class="search-field"><span class="material-symbols-outlined" aria-hidden="true">search</span><input v-model="studentSearch" aria-label="Search students" placeholder="Search student name or ID..." /></label></div>
          <div class="table-scroll"><table><thead><tr><th>Name</th><th>ID</th><th>Status</th></tr></thead><tbody><tr v-for="student in filteredStudents" :key="student.id"><td><div class="student-name"><span class="student-avatar">{{ student.initials }}</span><strong>{{ student.name }}</strong></div></td><td>{{ student.id }}</td><td><span class="badge green">Enrolled</span></td></tr><tr v-if="!filteredStudents.length"><td colspan="3" class="empty-search">No matching students.</td></tr></tbody></table></div>
          <div class="table-footer">Showing {{ filteredStudents.length }} of {{ demo.students.length }} students</div>
        </section>
      </template>

      <template v-else>
        <div class="student-heading"><h1>Hello, Thanakrit</h1><label class="search-field dashboard-search"><span class="material-symbols-outlined" aria-hidden="true">search</span><input v-model="search" aria-label="Search courses" placeholder="Search courses..." /></label></div>
        <section class="student-courses">
          <div class="section-heading"><h2>Current Enrolled Courses</h2><button class="button primary" @click="openJoin"><span class="material-symbols-outlined" aria-hidden="true">add</span>Join Course</button></div>
          <div v-if="!joinedCourses.length" class="empty-state panel">
            <span class="empty-icon material-symbols-outlined" aria-hidden="true">school</span>
            <h3>You haven't joined any courses yet</h3>
            <p>Enter the join code from your teacher to get started.</p>
            <button class="button primary" @click="openJoin"><span class="material-symbols-outlined" aria-hidden="true">add</span>Join Your First Course</button>
          </div>
          <button v-for="course in visibleJoinedCourses" :key="course.id" class="student-course-card" @click="store.selectedId = course.id; courseDialog.showModal()">
            <div><h3>{{ course.name }}</h3><p>{{ course.courseCode }} · Section {{ course.section }} · Semester {{ termLabel(course.termId) }}</p></div><span class="course-arrow material-symbols-outlined" aria-hidden="true">arrow_forward</span>
          </button>
          <p v-if="joinedCourses.length && !visibleJoinedCourses.length" class="empty-search">No courses found.</p>
        </section>
        <p class="demo-code-hint">Demo join code: <button @click="openJoin(); code = demo.code">{{ demo.code }}</button></p>
      </template>

      <dialog ref="createDialog" class="portal-dialog create-course-dialog" aria-labelledby="create-title" @click="($event.target === createDialog) && createDialog.close()">
        <div class="dialog-heading"><h2 id="create-title">{{ createMode === 'course' ? 'Create Course' : 'Add Section' }}</h2><button class="icon-button" aria-label="Close create course" @click="createDialog.close()"><span class="material-symbols-outlined" aria-hidden="true">close</span></button></div>
        <p class="dialog-description">{{ createMode === 'course' ? 'Create a course and set up its first class.' : 'Open a new class for your existing course.' }}</p>
        <form @submit.prevent="createCourse">
          <fieldset class="form-section">
            <legend><span class="material-symbols-outlined" aria-hidden="true">menu_book</span>Course Information</legend>
            <label class="field-label" for="course-name">Course Name</label>
            <input id="course-name" v-model="form.name" class="form-input" placeholder="e.g. Software Development" maxlength="120" required :readonly="createMode === 'section'" />
            <label class="field-label" for="course-code">Course Code</label>
            <input id="course-code" v-model="form.courseCode" class="form-input" placeholder="e.g. CS212" maxlength="30" required :readonly="createMode === 'section'" />
          </fieldset>
          <fieldset class="form-section class-information">
            <legend><span class="material-symbols-outlined" aria-hidden="true">groups</span>Class Information</legend>
            <div class="form-columns">
              <div><div class="semester-label"><label class="field-label" for="course-semester">Semester</label><button v-if="!addingSemester" type="button" class="add-semester-button" @click="openSemesterForm">+ Add Semester</button></div><select id="course-semester" v-model="form.termId" class="form-input" required><option v-for="term in demoTerms" :key="term.id" :value="term.id">{{ term.label }}{{ term.current ? ' (Current)' : '' }}</option></select></div>
              <div><label class="field-label" for="course-section">Section</label><input id="course-section" v-model="form.section" class="form-input" placeholder="e.g. 001" maxlength="20" required /></div>
            </div>
            <div v-if="addingSemester" class="semester-editor" @keydown.enter.prevent="saveSemester">
              <div class="form-columns">
                <div><label class="field-label" for="semester-year">Academic Year (B.E.)</label><input id="semester-year" v-model="newSemester.year" class="form-input" inputmode="numeric" maxlength="4" placeholder="e.g. 2570" :aria-invalid="Boolean(semesterError)" :aria-describedby="semesterError ? 'semester-error' : undefined" /></div>
                <div><label class="field-label" for="semester-number">Semester</label><select id="semester-number" v-model="newSemester.semester" class="form-input"><option value="1">1</option><option value="2">2</option><option value="summer">Summer</option></select></div>
              </div>
              <p v-if="semesterError" id="semester-error" class="error" role="alert">{{ semesterError }}</p>
              <div class="actions"><button type="button" class="button secondary" @click="addingSemester = false">Cancel</button><button type="button" class="button primary" @click="saveSemester">Add Semester</button></div>
            </div>
          </fieldset>
          <div class="form-info"><span class="material-symbols-outlined" aria-hidden="true">vpn_key</span><div><strong>A join code will be generated automatically.</strong><p>Students will join this section in the selected semester.</p></div></div>
          <p v-if="formError" class="error" role="alert">{{ formError }}</p>
          <div class="dialog-actions"><button type="button" class="button secondary" @click="createDialog.close()">Cancel</button><button class="button primary" type="submit" :disabled="addingSemester">{{ createMode === 'course' ? 'Create Course' : 'Create Section' }}</button></div>
        </form>
      </dialog>

      <dialog ref="joinDialog" class="portal-dialog" aria-labelledby="join-title" @click="($event.target === joinDialog) && joinDialog.close()">
        <div class="dialog-heading"><h2 id="join-title">{{ stage === 'success' ? 'Enrollment Successful' : stage === 'review' ? 'Confirm Course' : 'Join Course' }}</h2><button class="icon-button" aria-label="Close join course" @click="joinDialog.close()"><span class="material-symbols-outlined" aria-hidden="true">close</span></button></div>
        <form v-if="stage === 'input'" @submit.prevent="findCourse">
          <p class="dialog-description">Enter the 6-character code shared by your teacher.</p>
          <label class="field-label" for="join-code">Class Join Code</label>
          <input id="join-code" v-model="code" class="join-input" placeholder="e.g. K7MX2P" maxlength="6" autocomplete="off" autocapitalize="characters" spellcheck="false" required :aria-invalid="Boolean(error)" :aria-describedby="error ? 'join-error' : undefined" />
          <p v-if="error" id="join-error" class="error" role="alert">{{ error }}</p>
          <div class="dialog-actions"><button type="button" class="button secondary" @click="joinDialog.close()">Cancel</button><button class="button primary" type="submit">Find Course<span class="material-symbols-outlined" aria-hidden="true">arrow_forward</span></button></div>
        </form>
        <template v-else-if="stage === 'review'">
          <p class="dialog-description">Please check the course details before joining.</p>
          <div class="review-course"><h3>{{ demo.name }}</h3><p>Course ID: {{ demo.courseCode }}</p><dl><div><dt>Teacher</dt><dd>Orapan Wichai</dd></div><div><dt>Section</dt><dd>{{ demo.section }}</dd></div><div><dt>Semester</dt><dd>{{ termLabel(demo.termId) }}</dd></div></dl></div>
          <div class="dialog-actions"><button class="button secondary" @click="stage = 'input'">Back</button><button class="button primary" @click="enroll">Confirm Enrollment</button></div>
        </template>
        <template v-else>
          <div class="success-state" role="status"><span class="material-symbols-outlined" aria-hidden="true">check_circle</span><h3>You're enrolled!</h3><p>{{ demo.name }} is now in your courses.</p></div>
          <div class="dialog-actions"><button class="button primary" @click="joinDialog.close()">View My Courses</button></div>
        </template>
      </dialog>
      <dialog ref="courseDialog" class="portal-dialog" aria-labelledby="course-title" @click="($event.target === courseDialog) && courseDialog.close()">
        <div class="dialog-heading"><h2 id="course-title">{{ demo.name }}</h2><button class="icon-button" aria-label="Close course details" @click="courseDialog.close()"><span class="material-symbols-outlined" aria-hidden="true">close</span></button></div>
        <p class="dialog-description">{{ demo.courseCode }} · Section {{ demo.section }} · Semester {{ termLabel(demo.termId) }}</p><div class="review-course"><span class="badge green">Enrolled</span><p>No scores have been published yet.</p></div>
      </dialog>
    </main>
  </div>
</template>

<style scoped src="./enrollmentDemo.css"></style>
