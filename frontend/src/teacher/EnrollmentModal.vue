<template>
  <div
    class="fixed inset-0 bg-black bg-opacity-50 flex items-center justify-center z-50 p-4"
    @click.self="emit('close')"
  >
    <div
      class="modal-enter-active bg-white dark:bg-gray-800 w-full max-w-3xl max-h-[90vh] overflow-y-auto rounded-xl shadow-xl p-6 relative"
      role="dialog"
      aria-labelledby="enrollment-title"
    >
      <button
        @click="emit('close')"
        class="absolute top-3 right-3 text-2xl text-gray-500 hover:text-red-500"
        aria-label="Close"
      >
        ✕
      </button>

      <div class="flex flex-wrap items-start justify-between gap-3 mb-4 pr-8">
        <div>
          <h2 id="enrollment-title" class="text-2xl font-semibold">
            Course Enrollment
          </h2>
          <p class="text-sm text-gray-500 dark:text-gray-400">
            {{ course?.course_name }} · {{ course?.course_id }}
          </p>
        </div>
        <span
          v-if="course"
          class="text-xs font-semibold px-2.5 py-1 rounded-full"
          :class="
            course.join_open
              ? 'bg-green-100 text-green-700 dark:bg-green-900/40 dark:text-green-300'
              : 'bg-gray-100 text-gray-600 dark:bg-gray-700 dark:text-gray-300'
          "
        >
          {{ course.join_open ? "Enrollment open" : "Enrollment closed" }}
        </span>
      </div>

      <p v-if="notice" class="text-sm text-primary mb-3" role="status">
        {{ notice }}
      </p>
      <p v-if="error" class="text-sm text-red-600 mb-3" role="alert">
        {{ error }}
      </p>

      <div v-if="course" class="grid gap-4 sm:grid-cols-2 mb-6">
        <!-- join code -->
        <div class="rounded-lg border border-gray-200 dark:border-gray-700 p-4">
          <div class="flex items-center justify-between gap-3">
            <span class="font-mono text-2xl font-bold tracking-[0.3em]">{{
              course.join_code
            }}</span>
            <button
              @click="copyCode"
              class="btn-animate inline-flex items-center gap-1 px-3 py-2 rounded-md bg-primary hover:bg-primary-dark text-white text-sm"
            >
              <span class="material-symbols-outlined text-base"
                >content_copy</span
              >
              Copy
            </button>
          </div>
        </div>

        <!-- settings -->
        <div
          class="rounded-lg border border-gray-200 dark:border-gray-700 p-4 flex flex-col gap-4"
        >
          <div class="flex items-center justify-between gap-3">
            <div>
              <div class="text-sm font-semibold">Allow enrollment</div>
            </div>
            <button
              role="switch"
              :aria-checked="course.join_open"
              aria-label="Allow enrollment"
              :disabled="busy"
              @click="toggleOpen"
              class="relative inline-flex h-6 w-11 shrink-0 rounded-full transition-colors"
              :class="course.join_open ? 'bg-primary' : 'bg-gray-300 dark:bg-gray-600'"
            >
              <span
                class="absolute top-0.5 h-5 w-5 rounded-full bg-white shadow transition-transform"
                :class="course.join_open ? 'translate-x-5' : 'translate-x-0.5'"
              ></span>
            </button>
          </div>
          <div class="flex items-center justify-between gap-3">
            <div>
              <div class="text-sm font-semibold">Reset join code</div>
            </div>
            <button
              @click="confirmReset = !confirmReset"
              class="p-2 text-gray-500 hover:text-primary rounded-full"
              aria-label="Reset join code"
            >
              <span class="material-symbols-outlined">refresh</span>
            </button>
          </div>
          <div
            v-if="confirmReset"
            class="rounded-md bg-yellow-50 dark:bg-yellow-900/20 p-3 text-sm"
          >
            <p>The current code will stop working. Create a new code?</p>
            <div class="flex justify-end gap-2 mt-2">
              <button
                @click="confirmReset = false"
                class="px-3 py-1 rounded-md border border-gray-300 dark:border-gray-600"
              >
                Cancel
              </button>
              <button
                @click="regenerate"
                :disabled="busy"
                class="px-3 py-1 rounded-md bg-primary text-white"
              >
                Create New Code
              </button>
            </div>
          </div>
        </div>
      </div>

      <!-- roster -->
      <div class="flex flex-wrap items-center justify-between gap-3 mb-2">
        <h3 class="font-semibold">
          Enrolled Students
          <span
            class="ml-1 text-xs bg-gray-100 dark:bg-gray-700 px-2 py-0.5 rounded-full"
            >{{ students.length }}</span
          >
        </h3>
        <input
          v-model="search"
          placeholder="Search student name or ID..."
          aria-label="Search students"
          class="w-full sm:w-64 border border-gray-300 dark:border-gray-600 rounded-md dark:bg-gray-700 px-3 py-1.5 text-sm focus:outline-none focus:ring-2 focus:ring-primary"
        />
      </div>
      <div class="overflow-x-auto">
        <table class="w-full text-sm text-left">
          <thead class="text-xs uppercase text-gray-500 dark:text-gray-400">
            <tr>
              <th class="py-2 pr-3">Name</th>
              <th class="py-2 pr-3">ID</th>
              <th class="py-2 pr-3">Section</th>
              <th class="py-2 pr-3">Joined via</th>
              <th class="py-2"></th>
            </tr>
          </thead>
          <tbody class="divide-y divide-gray-100 dark:divide-gray-700">
            <tr v-for="stu in filteredStudents" :key="stu.student_id">
              <td class="py-2 pr-3">
                <div class="font-medium">
                  {{ fullName(stu) }}
                </div>
                <div class="text-xs text-gray-500 dark:text-gray-400">
                  {{ stu.email }}
                  <span v-if="!stu.signed_up" class="text-yellow-600">
                    · not signed up</span
                  >
                </div>
              </td>
              <td class="py-2 pr-3 font-mono">{{ stu.student_id }}</td>
              <td class="py-2 pr-3">{{ stu.section || "-" }}</td>
              <td class="py-2 pr-3">
                {{ stu.joined_via === "code" ? "Join code" : "CSV" }}
              </td>
              <td class="py-2 text-right">
                <button
                  @click="removeStudent(stu)"
                  class="p-1.5 text-gray-400 hover:text-red-600 rounded-full"
                  :aria-label="`Remove ${fullName(stu)}`"
                  title="Remove from course"
                >
                  <span class="material-symbols-outlined text-lg"
                    >person_remove</span
                  >
                </button>
              </td>
            </tr>
            <tr v-if="loaded && !filteredStudents.length">
              <td colspan="5" class="py-6 text-center text-gray-500">
                {{ students.length ? "No matching students." : "No students yet." }}
              </td>
            </tr>
          </tbody>
        </table>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, computed, onMounted } from "vue";

const props = defineProps({ courseCode: { type: Number, required: true } });
// changed = จำนวนนักศึกษา/สถานะเปลี่ยน ให้หน้าหลักโหลดใหม่
const emit = defineEmits(["close", "changed"]);

const BASE_URL = "/api";
const course = ref(null);
const students = ref([]);
const loaded = ref(false);
const search = ref("");
const notice = ref("");
const error = ref("");
const busy = ref(false);
const confirmReset = ref(false);

const fullName = (s) =>
  [s.first_name, s.middle_name, s.last_name].filter(Boolean).join(" ");

const filteredStudents = computed(() => {
  const q = search.value.trim().toLowerCase();
  if (!q) return students.value;
  return students.value.filter((s) =>
    `${fullName(s)} ${s.student_id}`.toLowerCase().includes(q),
  );
});

const post = async (path) => {
  const response = await fetch(`${BASE_URL}/teacher/course/${props.courseCode}${path}`, {
    method: "POST",
    credentials: "include",
    headers: { "X-CSRF-Token": localStorage.getItem("csrf_token") || "" },
  });
  const data = await response.json().catch(() => null);
  if (!response.ok) throw new Error(data?.detail || "Request failed");
  return data;
};

// เรียกซ้อนกันไม่ได้ + โชว์ error จาก backend
const run = async (fn) => {
  error.value = "";
  notice.value = "";
  busy.value = true;
  try {
    await fn();
  } catch (e) {
    error.value = e.message;
  } finally {
    busy.value = false;
  }
};

const fetchRoster = async () => {
  const response = await fetch(
    `${BASE_URL}/teacher/course/${props.courseCode}/roster`,
    { credentials: "include" },
  );
  const data = await response.json().catch(() => null);
  if (!response.ok) {
    error.value = data?.detail || "Could not load roster";
    return;
  }
  course.value = data.course;
  students.value = data.students;
  loaded.value = true;
};

const copyCode = async () => {
  try {
    await navigator.clipboard.writeText(course.value.join_code);
    notice.value = "Join code copied.";
  } catch {
    notice.value = `Copy this code manually: ${course.value.join_code}`;
  }
};

const toggleOpen = () =>
  run(async () => {
    Object.assign(course.value, await post("/join_code/toggle"));
    emit("changed");
  });

const regenerate = () =>
  run(async () => {
    Object.assign(course.value, await post("/join_code/regenerate"));
    confirmReset.value = false;
    notice.value = "New code created. Existing enrollments are unchanged.";
    emit("changed");
  });

const removeStudent = (stu) => {
  if (!confirm(`Remove ${fullName(stu)} (${stu.student_id}) from this course?`)) return;
  run(async () => {
    await post(`/remove/${encodeURIComponent(stu.student_id)}`);
    students.value = students.value.filter((s) => s.student_id !== stu.student_id);
    emit("changed");
  });
};

onMounted(fetchRoster);
</script>
