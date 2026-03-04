<template>
  <div
    class="bg-background-light dark:bg-background-dark text-text-light dark:text-text-dark transition-colors duration-200 min-h-screen flex flex-col"
  >
    <header
      class="bg-surface-light dark:bg-surface-dark border-b border-border-light dark:border-border-dark h-16 sticky top-0 z-10 shadow-sm"
    >
      <div
        class="max-w-7xl mx-auto px-4 h-full flex items-center justify-between relative"
        ref="dropdownRef"
      >
        <div class="flex items-center gap-2">
          <div class="flex items-center gap-3">
            <div
              class="bg-primary rounded-lg p-1.5 flex items-center justify-center text-white"
            >
              <span class="material-symbols-outlined text-white text-xl">
                school
              </span>
            </div>
            <h2 class="text-lg font-bold leading-tight tracking-[-0.015em]">
              University Grade Portal
            </h2>
          </div>
        </div>

        <div class="flex items-center gap-6">
          <div class="flex items-center gap-3">
            <button
              @click="toggleDropdown"
              class="flex items-center space-x-3 hover:bg-gray-100 dark:hover:bg-gray-700 px-3 py-2 rounded-lg transition"
            >
              <div class="hidden md:flex flex-col items-end mr-1">
                <span
                  class="text-sm font-semibold text-gray-900 dark:text-white"
                >
                  {{ teacherName }}
                </span>
              </div>
              <div class="relative">
                <img
                  alt="User profile picture"
                  class="h-10 w-10 rounded-full object-cover border-2 border-primary"
                  src="https://lh3.googleusercontent.com/aida-public/AB6AXuA6ks6i0YSsJsdUh4f96EGndBnmP5pOe0jjp_Q9acQEQM11AzaPK7CCc7w-QiLzzN_qmRFO6MoO1BUx0mq50TWJai3AYppjYwm0WmzXNk9gCodOda6Fln53ift0i4aOWutD0QihvMIyWdrlVe9bpfd8iaTyMDGDlVQFeXYITSMNcEaBk_SRw4GQAq2XvI0W-vb8uGMcGqvaS4uYNMiJXtr4p83cjHH_n0uhwOn-HWItnMXbPU3_rAg0HM6wz3pruWbigJmGvuRaYg"
                />
              </div>
            </button>

            <transition name="fade">
              <div
                v-if="isOpen"
                class="absolute right-4 top-full mt-2 bg-white dark:bg-gray-800 rounded-xl shadow-lg p-4 z-50 w-max min-w-[250px] max-w-[90vw]"
              >
                <div class="flex items-center space-x-3">
                  <img
                    class="h-12 w-12 rounded-full object-cover"
                    src="https://lh3.googleusercontent.com/aida-public/AB6AXuA6ks6i0YSsJsdUh4f96EGndBnmP5pOe0jjp_Q9acQEQM11AzaPK7CCc7w-QiLzzN_qmRFO6MoO1BUx0mq50TWJai3AYppjYwm0WmzXNk9gCodOda6Fln53ift0i4aOWutD0QihvMIyWdrlVe9bpfd8iaTyMDGDlVQFeXYITSMNcEaBk_SRw4GQAq2XvI0W-vb8uGMcGqvaS4uYNMiJXtr4p83cjHH_n0uhwOn-HWItnMXbPU3_rAg0HM6wz3pruWbigJmGvuRaYg"
                  />
                  <div>
                    <p
                      class="font-semibold text-gray-900 dark:text-white break-all"
                    >
                      Katarina Bluu
                    </p>
                    <p class="text-sm text-gray-500 break-all">
                      Email : katarina.bluu@cmu.ac.th
                    </p>
                  </div>
                </div>
              </div>
            </transition>

            <button
              @click="handleLogout"
              class="flex items-center justify-center size-10 rounded-full hover:bg-red-50 dark:hover:bg-red-900/20 text-[#637888] dark:text-[#a0b8cf] hover:text-red-600 dark:hover:text-red-400 transition-colors"
              title="Log Out"
            >
              <span class="material-symbols-outlined text-[20px]">
                logout
              </span>
            </button>
          </div>
        </div>
      </div>
    </header>
    <main class="flex-grow max-w-7xl w-full mx-auto px-4 sm:px-6 lg:px-8 py-8">
      <div class="md:flex md:items-center md:justify-between mb-8">
        <div class="flex-1 min-w-0">
          <h1
            class="text-3xl font-bold leading-7 text-gray-900 dark:text-white sm:text-3xl sm:truncate"
          >
            Course Management
          </h1>
        </div>
      </div>
      <div
        class="bg-surface-light dark:bg-surface-dark rounded-xl shadow-sm border border-border-light dark:border-border-dark p-4 mb-6 flex flex-col sm:flex-row justify-between items-center gap-4"
      >
        <div class="relative w-full sm:max-w-md">
          <div
            class="absolute inset-y-0 left-0 pl-3 flex items-center pointer-events-none"
          >
            <span class="material-symbols-outlined text-gray-400">search</span>
          </div>
          <input
            v-model="searchTerm"
            class="block w-full pl-10 pr-3 py-2 border-none bg-gray-50 dark:bg-gray-800 rounded-lg text-gray-900 dark:text-white placeholder-gray-400 focus:outline-none focus:ring-2 focus:ring-primary sm:text-sm"
            id="search"
            name="search"
            placeholder="Search Course Code or Name..."
            type="text"
          />
        </div>
        <div class="flex w-full sm:w-auto items-center gap-4">
          <button
            @click="createCourse"
            class="inline-flex items-center justify-center px-4 py-2 border border-transparent text-sm font-medium rounded-lg shadow-sm text-white bg-primary hover:bg-primary-dark focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-primary transition-colors whitespace-nowrap"
          >
            <span class="material-symbols-outlined text-white text-lg mr-2"
              >add</span
            >
            Create Course
          </button>
        </div>
        <div
          v-if="startCreate"
          class="fixed inset-0 bg-black bg-opacity-50 flex items-center justify-center z-50"
          @click.self="cancleCreate"
        >
          <div
            class="bg-white dark:bg-gray-800 w-[600px] rounded-xl shadow-xl p-6 relative"
          >
            <button
              @click="cancleCreate"
              class="absolute top-3 right-3 text-2xl text-gray-500 hover:text-red-500"
            >
              ✕
            </button>

            <h2 class="text-2xl font-semibold mb-4">Create New Course</h2>
            <div class="mb-4">
              <label class="block py-1">Course Name</label>
              <input
                v-model="courseName"
                type="text"
                class="w-full border border-gray-300 dark:border-gray-800 rounded-md dark:bg-gray-700 px-3 py-2 focus:outline-none focus:ring-green-200"
                placeholder="e.g., Intro to Computer Science"
              />
            </div>
            <div class="flex justify-end gap-3">
              <button
                @click="submit"
                class="px-6 py-3 rounded-md bg-primary hover:bg-primary-dark text-white text-base"
              >
                Create Course
              </button>
            </div>
          </div>
        </div>
      </div>
      <div
        class="bg-surface-light dark:bg-surface-dark shadow-sm rounded-xl border border-border-light dark:border-border-dark overflow-hidden"
      >
        <div
          class="px-8 py-4 border-b border-border-light dark:border-border-dark flex justify-between items-center bg-gray-50/50 dark:bg-gray-800/30"
        >
          <span
            class="text-xs font-semibold text-text-muted-light dark:text-text-muted-dark uppercase tracking-wider"
            >Course Info</span
          >
          <div class="flex items-center gap-6">
            <span
              class="text-xs font-semibold text-text-muted-light dark:text-text-muted-dark uppercase tracking-wider"
              >Enrolled</span
            >
            <span
              class="text-xs font-semibold text-text-muted-light dark:text-text-muted-dark uppercase tracking-wider"
              >Actions</span
            >
          </div>
        </div>
        <ul class="divide-y divide-border-light dark:divide-border-dark">
          <li
            v-for="course in filteredCourses"
            :key="course.course_id"
            class="hover:bg-gray-50 dark:hover:bg-gray-800/50 transition-colors duration-150"
          >
            <div class="px-6 py-5 flex items-center justify-between">
              <a @click="goToAssignment(course.course_id)" class="block">
                <div class="ml-4">
                  <!-- <div class="text-base font-bold">
                    {{ course.course_id }}
                  </div> -->
                  <div
                    class="text-l font-bold text-primary text-gray-900 dark:text-white uppercase tracking-wide"
                  >
                    {{ course.course_name }}
                  </div>
                </div>
              </a>
              <div class="flex items-center gap-6">
                <div class="flex flex-col items-end min-w-[80px]">
                  <div
                    class="flex items-center text-gray-900 dark:text-white font-semibold"
                  >
                    <span
                      class="material-symbols-outlined text-text-muted-light dark:text-text-muted-dark mr-1 text-lg"
                      >people</span
                    >
                    {{ course.student_count ?? 0 }}
                  </div>
                  <div
                    class="text-xs text-text-muted-light dark:text-text-muted-dark uppercase mt-0.5"
                  >
                    Students
                  </div>
                </div>
                <div class="flex items-end min-w-[50px]">
                  <button
                    @click="deleteCourse(course.course_id)"
                    class="p-2 text-gray-400 hover:text-red-600 hover:bg-red-50 dark:hover:bg-red-900/30 rounded-full transition-colors duration-200 group"
                    title="Delete Course"
                  >
                    <span
                      class="material-symbols-outlined text-xl group-hover:text-red-600"
                      >delete</span
                    >
                  </button>
                  <button
                    @click="archiveCourse(course.course_id)"
                    class="p-2 text-gray-400 hover:text-yellow-600 hover:bg-yellow-50 dark:hover:bg-yellow-900/30 rounded-full transition-colors duration-200 group"
                    title="Archive Course"
                  >
                    <span
                      class="material-symbols-outlined text-xl group-hover:text-yellow-600"
                      >archive</span
                    >
                  </button>
                </div>
              </div>
            </div>
          </li>
        </ul>
        <div
          class="px-6 py-4 border-t border-border-light dark:border-border-dark flex items-center justify-between"
        >
          <div class="text-sm text-text-muted-light dark:text-text-muted-dark">
            <span class="font-bold text-gray-900 dark:text-white"></span>
            <span class="font-bold text-gray-900 dark:text-white"></span>
          </div>
          <div class="flex space-x-2">
            <button
              class="p-2 border border-border-light dark:border-border-dark rounded-md text-gray-400 hover:text-gray-500 dark:hover:text-gray-300 bg-white dark:bg-surface-dark hover:bg-gray-50 dark:hover:bg-gray-700"
            >
              <span class="material-symbols-outlined text-sm"
                >chevron_left</span
              >
            </button>
            <button
              class="p-2 border border-border-light dark:border-border-dark rounded-md text-gray-400 hover:text-gray-500 dark:hover:text-gray-300 bg-white dark:bg-surface-dark hover:bg-gray-50 dark:hover:bg-gray-700"
            >
              <span class="material-symbols-outlined text-sm"
                >chevron_right</span
              >
            </button>
          </div>
        </div>
      </div>
    </main>

    <div class="fixed bottom-6 left-6 z-50">
      <button
        @click="openArchive"
        class="p-3 rounded-full bg-surface-light dark:bg-surface-dark text-gray-500 dark:text-gray-400 hover:text-yellow-600 dark:hover:text-yellow-400 shadow-lg border border-border-light dark:border-border-dark transition-all duration-300 focus:outline-none"
      >
        <span class="material-symbols-outlined text-2xl"> archive </span>
      </button>
    </div>
    <!-- Archive Modal -->
    <div
      v-if="showArchiveModal"
      class="fixed inset-0 bg-black bg-opacity-50 flex items-center justify-center z-50"
      @click.self="closeArchive"
    >
      <div
        class="bg-white dark:bg-gray-800 w-96 rounded-2xl shadow-xl p-6 relative"
      >
        <button
          @click="closeArchive"
          class="absolute top-3 right-3 text-gray-500 hover:text-red-500"
        >
          ✕
        </button>

        <h2 class="text-xl font-semibold mb-4">Archived Courses</h2>

        <ul class="space-y-2">
          <li
            class="rounded-xl hover:bg-gray-100 dark:hover:bg-gray-600/50 transition-colors duration-150"
          >
            <div class="px-4 py-2 flex items-center">
              <div
                class="flex-shrink-0 h-10 w-10 rounded-xl bg-purple-200 dark:bg-purple-600/50 text-purple-600 dark:text-purple-400 flex items-center justify-center"
              >
                <span class="material-symbols-outlined">rocket</span>
              </div>
              <div class="ml-4 grow items-center">
                <div class="text-sm font-bold text-gray-900 dark:text-white">
                  Astro101
                </div>
                <div
                  class="text-xs text-text-muted-light dark:text-text-muted-dark"
                >
                  Astronomy
                </div>
              </div>
              <div class="flex items-center gap-6">
                <div class="flex items-end min-w-[50px]">
                  <button
                    class="p-2 text-gray-400 hover:text-yellow-600 hover:bg-yellow-50 dark:hover:bg-yellow-900/30 rounded-full transition-colors duration-200 group"
                    title="Restore Course"
                  >
                    <span
                      class="material-symbols-outlined text-xl group-hover:text-yellow-600"
                      >restore</span
                    >
                  </button>
                  <button
                    class="p-2 text-gray-400 hover:text-red-600 hover:bg-red-50 dark:hover:bg-red-900/30 rounded-full transition-colors duration-200 group"
                    title="Delete Course"
                  >
                    <span
                      class="material-symbols-outlined text-xl group-hover:text-red-600"
                      >delete</span
                    >
                  </button>
                </div>
              </div>
            </div>
          </li>
          <li
            class="rounded-xl hover:bg-gray-100 dark:hover:bg-gray-600/50 transition-colors duration-150"
          >
            <div class="px-4 py-2 flex items-center">
              <div
                class="flex-shrink-0 h-10 w-10 rounded-xl bg-yellow-200 dark:bg-yellow-600/50 text-yellow-600 dark:text-yellow-400 flex items-center justify-center"
              >
                <span class="material-symbols-outlined">bolt</span>
              </div>
              <div class="ml-4 grow items-center">
                <div class="text-sm font-bold text-gray-900 dark:text-white">
                  EE101
                </div>
                <div
                  class="text-xs text-text-muted-light dark:text-text-muted-dark"
                >
                  Electric Engeneering
                </div>
              </div>
              <div class="flex items-center gap-6">
                <div class="flex items-end min-w-[50px]">
                  <button
                    class="p-2 text-gray-400 hover:text-yellow-600 hover:bg-yellow-50 dark:hover:bg-yellow-900/30 rounded-full transition-colors duration-200 group"
                    title="Restore Course"
                  >
                    <span
                      class="material-symbols-outlined text-xl group-hover:text-yellow-600"
                      >restore</span
                    >
                  </button>
                  <button
                    class="p-2 text-gray-400 hover:text-red-600 hover:bg-red-50 dark:hover:bg-red-900/30 rounded-full transition-colors duration-200 group"
                    title="Delete Course"
                  >
                    <span
                      class="material-symbols-outlined text-xl group-hover:text-red-600"
                      >delete</span
                    >
                  </button>
                </div>
              </div>
            </div>
          </li>
        </ul>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted, onBeforeUnmount, computed } from "vue";
import { useRouter } from "vue-router";

const router = useRouter();

const teacherName = ref("");
const courses = ref([]);
const searchTerm = ref("");
const courseName = ref("");
const startCreate = ref(false);
const dropdownRef = ref(null);
const isOpen = ref(false);
const showArchiveModal = ref(false);
const archivedCourses = ref([]);

const BASE_URL = "http://localhost:56733";

const fetchDashboard = async () => {
  try {
    const response = await fetch(`${BASE_URL}/teacher/dashboard_teacher`, {
      credentials: "include",
    });

    if (!response.ok) {
      router.push("/login");
      return;
    }

    const data = await response.json();
    teacherName.value = data.teacher_name;
    courses.value = data.courses;
  } catch (error) {
    console.error("Fetch dashboard error:", error);
  }
};

const filteredCourses = computed(() => {
  if (!searchTerm.value) return courses.value;

  return courses.value.filter(
    (c) =>
      c.course_name.toLowerCase().includes(searchTerm.value.toLowerCase()) ||
      String(c.course_id).includes(searchTerm.value),
  );
});

const toggleDropdown = () => {
  isOpen.value = !isOpen.value;
};

const handleClickOutside = (event) => {
  if (dropdownRef.value && !dropdownRef.value.contains(event.target)) {
    isOpen.value = false;
  }
};

const openArchive = () => {
  showArchiveModal.value = true;
};

const closeArchive = () => {
  showArchiveModal.value = false;
};

const createCourse = () => {
  startCreate.value = true;
};

const cancleCreate = () => {
  startCreate.value = false;
};

const submit = async () => {
  if (!courseName.value) return;

  try {
    const response = await fetch(`${BASE_URL}/teacher/create_course`, {
      method: "POST",
      credentials: "include",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({
        course_name: courseName.value,
      }),
    });

    if (response.ok) {
      courseName.value = "";
      startCreate.value = false;
      await fetchDashboard();
    }
  } catch (error) {
    console.error("Create course error:", error);
  }
};

const deleteCourse = async (id) => {
  if (!confirm("Delete this course?")) return;

  try {
    const response = await fetch(`${BASE_URL}/teacher/delete_course/${id}`, {
      method: "POST",
      credentials: "include",
    });

    if (response.ok) {
      await fetchDashboard();
    }
  } catch (error) {
    console.error("Delete error:", error);
  }
};

const goToAssignment = (course_id) => {
  router.push(`/assignment/${course_id}`);
};

const archiveCourse = async (id) => {
  try {
    const response = await fetch(`${BASE_URL}/teacher/archive_course/${id}`, {
      method: "POST",
      credentials: "include",
    });

    if (response.ok) {
      await fetchDashboard();
    }
  } catch (error) {
    console.error("Archive error:", error);
  }
};

const handleLogout = async () => {
  try {
    const response = await fetch(`${BASE_URL}/logout`, {
      method: "GET",
      credentials: "include",
    });

    if (!response.ok) throw new Error();

    localStorage.clear();
    router.push("/login");
  } catch (error) {
    console.error("Logout failed:", error);
  }
};

onMounted(() => {
  document.addEventListener("click", handleClickOutside);
  fetchDashboard();
});

onBeforeUnmount(() => {
  document.removeEventListener("click", handleClickOutside);
});
</script>

<style>
.fade-enter-active,
.fade-leave-active {
  transition: opacity 0.2s ease;
}
.fade-enter-from,
.fade-leave-to {
  opacity: 0;
}
</style>
