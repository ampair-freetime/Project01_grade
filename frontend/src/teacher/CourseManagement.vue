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
            <button
              class="bg-primary rounded-lg p-1.5 flex items-center justify-center text-white"
            >
              <span class="material-symbols-outlined text-white text-xl">
                school
              </span>
            </button>
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
                  {{ userProfile?.first_name }}
                </span>
              </div>
              <div class="relative">
                <img
                  alt="User profile picture"
                  class="h-10 w-10 rounded-full object-cover border-2 border-primary"
                  :src="userProfile?.avatar_url"
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
                    :src="userProfile?.avatar_url"
                  />

                  <div>
                    <p
                      class="font-semibold text-gray-900 dark:text-white break-all"
                    >
                      {{ userProfile?.first_name }}
                      {{ userProfile?.middle_name }}
                      {{ userProfile?.last_name }}
                    </p>
                    <p class="text-sm text-gray-500 break-all">
                      Email : {{ userProfile?.email }}
                    </p>
                    <button
                      v-if="!userProfile?.google_connected"
                      @click="connectGoogle"
                      class="mt-3 w-full flex items-center justify-center gap-2 bg-white dark:bg-gray-700 border border-gray-300 dark:border-gray-600 hover:bg-gray-100 dark:hover:bg-gray-600 text-sm font-medium px-3 py-2 rounded-lg transition"
                    >
                      <img
                        src="https://developers.google.com/identity/images/g-logo.png"
                        class="w-4 h-4"
                      />
                      Connect Google
                    </button>

                    <div
                      v-else
                      class="mt-3 text-green-600 dark:text-green-400 text-sm font-semibold flex items-center gap-2"
                    >
                      Google Connected Successfully 🎉
                    </div>
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
    <main class="flex-1 flex-row flex-col h-full overflow-hidden relative">
      <div class="flex-1 overflow-y-auto p-8 lg:p-12">
        <div class="max-w-5xl mx-auto flex flex-col gap-8">
          <h1
            class="text-3xl font-bold leading-7 text-gray-900 dark:text-white sm:text-3xl sm:truncate"
          >
            Course Management
          </h1>

          <div
            class="animate-card delay-1 bg-surface-light dark:bg-surface-dark rounded-xl shadow-sm border border-border-light dark:border-border-dark p-4 mb-6 flex flex-col sm:flex-row justify-between items-center gap-4"
          >
            <div class="relative w-full sm:max-w-md">
              <div
                class="absolute inset-y-0 left-0 pl-3 flex items-center pointer-events-none"
              >
                <span class="material-symbols-outlined text-gray-400"
                  >search</span
                >
              </div>
              <input
                v-model="searchTerm"
                class="block w-full pl-10 pr-3 py-2 border-none bg-gray-50 dark:bg-gray-800 rounded-lg text-gray-900 dark:text-white placeholder-gray-400 focus:outline-none focus:ring-2 focus:ring-primary sm:text-sm transition-all duration-200"
                id="search"
                name="search"
                placeholder="Search Course Code or Name..."
                type="text"
              />
            </div>
            <div class="flex w-full sm:w-auto items-center gap-4">
              <button
                @click="createCourse"
                class="btn-animate delay-2 inline-flex items-center justify-center px-4 py-2 border border-transparent text-sm font-medium rounded-lg shadow-sm text-white bg-primary hover:bg-primary-dark focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-primary transition-colors whitespace-nowrap"
              >
                <span class="material-symbols-outlined text-white text-lg mr-2"
                  >add</span
                >
                Create Course
              </button>
            </div>
          </div>
          <div
            class="animate-card delay-2 bg-surface-light dark:bg-surface-dark shadow-sm rounded-xl border border-border-light dark:border-border-dark overflow-hidden"
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
                v-for="(course, index) in paginatedCourses"
                :key="course.course_code"
                class="hover:bg-gray-50 dark:hover:bg-gray-800/50 transition-colors duration-150 animate-card"
                :class="`delay-${(index % 5) + 1}`"
              >
                <div
                  class="px-6 py-5 flex items-center justify-between cursor-pointer"
                  @click="goToAssignment(course.course_code)"
                >
                  <div class="flex-1 min-w-0">
                    <div
                      class="text-l font-bold dark:text-primary-light uppercase tracking-wide"
                    >
                      {{ course.course_name }}
                    </div>

                    <div
                      class="text-xs text-gray-500 dark:text-gray-400 tracking-wide"
                    >
                      Course ID: {{ course.course_code }}
                    </div>
                  </div>

                  <div class="flex items-center gap-6 shrink-0">
                    <div class="flex flex-col items-end min-w-[80px]">
                      <div
                        class="flex items-center text-gray-900 dark:text-white font-semibold"
                      >
                        <span
                          class="material-symbols-outlined text-text-muted-light dark:text-text-muted-dark mr-1 text-lg"
                          >people</span
                        >
                        {{ course.course_stu_number ?? 0 }}
                      </div>

                      <div
                        class="text-xs text-text-muted-light dark:text-text-muted-dark uppercase mt-0.5"
                      >
                        Students
                      </div>
                    </div>

                    <div class="flex items-end min-w-[50px]">
                      <button
                        @click.stop="archiveCourse(course.course_code)"
                        class="btn-animate delay-2 p-2 text-gray-400 hover:text-yellow-600 hover:bg-yellow-50 dark:hover:bg-yellow-900/30 rounded-full transition-colors duration-200 group"
                        title="Archive Course"
                      >
                        <span class="material-symbols-outlined text-xl"
                          >archive</span
                        >
                      </button>
                      <button
                        @click.stop="deleteCourse(course.course_code)"
                        class="btn-animate delay-2 p-2 text-gray-400 hover:text-red-600 hover:bg-red-50 dark:hover:bg-red-900/30 rounded-full transition-colors duration-200 group"
                        title="Delete Course"
                      >
                        <span class="material-symbols-outlined text-xl"
                          >delete</span
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
              <div
                class="text-sm text-text-muted-light dark:text-text-muted-dark"
              >
                <span class="font-bold text-gray-900 dark:text-white"></span>
                <span class="font-bold text-gray-900 dark:text-white"></span>
              </div>
              <div class="flex items-center space-x-1">
                <!-- first -->
                <button
                  @click="goToFirstPage"
                  :disabled="currentPage === 1"
                  class="btn-animate delay-2 p-2 border rounded-md disabled:opacity-40"
                >
                  <span class="material-symbols-outlined text-sm">
                    first_page
                  </span>
                </button>
                <!-- previous -->
                <button
                  @click="prevPage"
                  :disabled="currentPage === 1"
                  class="btn-animate delay-2 p-2 border rounded-md disabled:opacity-40"
                >
                  <span class="material-symbols-outlined text-sm">
                    chevron_left
                  </span>
                </button>

                <!-- page numbers -->
                <button
                  v-for="page in pages"
                  :key="page"
                  @click="page !== '...' && goToPage(page)"
                  class="btn-animate delay-2 px-3 py-1 border rounded-md text-sm"
                  :disabled="page === '...'"
                  :class="[
                    page === currentPage
                      ? 'bg-primary text-white'
                      : 'bg-white dark:bg-surface-dark',
                    page === '...' ? 'cursor-default opacity-60' : '',
                  ]"
                >
                  {{ page }}
                </button>

                <!-- next -->
                <button
                  @click="nextPage"
                  :disabled="currentPage === totalPages"
                  class="btn-animate delay-2 p-2 border rounded-md disabled:opacity-40"
                >
                  <span class="material-symbols-outlined text-sm">
                    chevron_right
                  </span>
                </button>

                <!-- last -->
                <button
                  @click="goToLastPage"
                  :disabled="currentPage === totalPages"
                  class="btn-animate delay-2 p-2 border rounded-md disabled:opacity-40"
                >
                  <span class="material-symbols-outlined text-sm">
                    last_page
                  </span>
                </button>
              </div>
            </div>
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

        <ul v-if="archivedCourses.length" class="space-y-2">
          <li
            v-for="course in archivedCourses"
            :key="course.course_code"
            class="rounded-xl hover:bg-gray-100 dark:hover:bg-gray-600/50 transition-colors duration-150"
          >
            <div class="px-4 py-2 flex items-center">
              <div
                class="flex-shrink-0 h-10 w-10 rounded-xl bg-purple-200 dark:bg-purple-600/50 text-purple-600 dark:text-purple-400 flex items-center justify-center"
              >
                <span class="material-symbols-outlined">archive</span>
              </div>
              <div class="ml-4 grow items-center">
                <div class="text-sm font-bold text-gray-900 dark:text-white">
                  {{ course.course_name }}
                </div>
                <div
                  class="text-xs text-text-muted-light dark:text-text-muted-dark"
                >
                  Course ID: {{ course.course_id }}
                </div>
              </div>
              <div class="flex items-center gap-6">
                <div class="flex items-end min-w-[50px]">
                  <button
                    @click="restoreCourse(course.course_code)"
                    class="btn-animate delay-2 p-2 text-gray-400 hover:text-yellow-600 hover:bg-yellow-50 dark:hover:bg-yellow-900/30 rounded-full transition-colors duration-200 group"
                    title="Restore Course"
                  >
                    <span
                      class="material-symbols-outlined text-xl group-hover:text-yellow-600"
                      >restore</span
                    >
                  </button>
                  <button
                    @click="deleteArchivedCourse(course.course_code)"
                    class="btn-animate delay-2 p-2 text-gray-400 hover:text-red-600 hover:bg-red-50 dark:hover:bg-red-900/30 rounded-full transition-colors duration-200 group"
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
        <p
          v-else
          class="text-sm text-text-muted-light dark:text-text-muted-dark py-4"
        >
          No archived courses.
        </p>
      </div>
    </div>
    <div
      v-if="startCreate"
      class="fixed inset-0 bg-black bg-opacity-50 flex items-center justify-center z-50 modal-enter-active"
      @click.self="cancleCreate"
    >
      <div
        class="animate-card delay-3 bg-white dark:bg-gray-800 w-[600px] rounded-xl shadow-xl p-6 relative"
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
        <div class="mb-4">
          <label class="block py-1">Course Code</label>
          <input
            v-model="courseID"
            type="text"
            class="w-full border border-gray-300 dark:border-gray-800 rounded-md dark:bg-gray-700 px-3 py-2 focus:outline-none focus:ring-green-200"
            placeholder="e.g., 204212"
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
const userProfile = ref(null);
const csrf_token = localStorage.getItem("csrf_token");
const randomAvatar = ref("");
const currentPage = ref(1);
const itemsPerPage = 5;
const courseID = ref("")

const BASE_URL = "http://localhost:56733";
const connectGoogle = () => {
  window.location.href = `${BASE_URL}/login_with_google`;
};

// ################################ fetch ###########################################################################################################################

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

const fetchUserProfile = async () => {
  try {
    const response = await fetch(`${BASE_URL}/me`, {
      credentials: "include",
    });

    if (!response.ok) {
      router.push("/login");
      return;
    }

    const data = await response.json();
    userProfile.value = data;
  } catch (error) {
    console.error("Fetch profile error:", error);
  }
};

const fetchArchivedCourses = async () => {
  try {
    const response = await fetch(`${BASE_URL}/teacher/archive_teacher`, {
      credentials: "include",
    });
    if (response.ok) {
      const data = await response.json();
      archivedCourses.value = data.courses || [];
    } else {
      archivedCourses.value = [];
    }
  } catch (error) {
    console.error("Fetch archived courses error:", error);
    archivedCourses.value = [];
  }
};

// ######################## pop-up ###################################################################################################################################

const toggleDropdown = () => {
  isOpen.value = !isOpen.value;
};

const openArchive = async () => {
  await fetchArchivedCourses();
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

const handleClickOutside = (event) => {
  if (dropdownRef.value && !dropdownRef.value.contains(event.target)) {
    isOpen.value = false;
  }
};

// ######################## archive ###################################################################################################################################

//กู้คืนcourse
const restoreCourse = async (course_code) => {
  try {
    const response = await fetch(
      `${BASE_URL}/teacher/restore_to_dash/${course_code}`,
      {
        headers: { "X-CSRF-Token": csrf_token },
        method: "POST",
        credentials: "include",
      },
    );
    if (!response.ok) {
      const err = await response.json();
      alert(err.detail || "Restore failed");
    }
    archivedCourses.value = archivedCourses.value.filter(
      (c) => c.course_code !== course_code,
    );

    await fetchDashboard();
  } catch (error) {
    console.error("Restore error:", error);
  }
};

//ลบcourseที่อยู่ในกล่องarchive (ลบถาวร)
const deleteArchivedCourse = async (course_code) => {
  if (!confirm("Delete this archived course?")) return;
  try {
    const response = await fetch(
      `${BASE_URL}/teacher/delete_course/${course_code}`,
      {
        headers: { "X-CSRF-Token": csrf_token },
        method: "POST",
        credentials: "include",
      },
    );
    if (!response.ok) {
      const err = await response.json();
      alert(err.detail || "Delete failed");
    }
    archivedCourses.value = archivedCourses.value.filter(
      (c) => c.course_code !== course_code,
    );
  } catch (error) {
    console.error("Delete error:", error);
  }
};

// ######################## course ###################################################################################################################################

// กรองรายวิชาตามการค้นหา
const filteredCourses = computed(() => {
  if (!searchTerm.value) return courses.value;

  return courses.value.filter(
    (c) =>
      c.course_name.toLowerCase().includes(searchTerm.value.toLowerCase()) ||
      String(c.course_code).includes(searchTerm.value),
  );
});

// สร้างcourseใหม่
const submit = async () => {
  if (!courseName.value) return;

  try {
    const response = await fetch(`${BASE_URL}/teacher/create_course`, {
      method: "POST",
      credentials: "include",
      headers: {
        "Content-Type": "application/json",
        "X-CSRF-Token": csrf_token,
      },
      body: JSON.stringify({
        course_name: courseName.value,
        course_id: courseID.value
      }),
    });

    if (response.ok) {
      courseName.value = "";
      courseID.value = "";
      startCreate.value = false;
      await fetchDashboard();
    }
  } catch (error) {
    console.error("Create course error:", error);
  }
};

// จัดเก็บcourse
const archiveCourse = async (course_code) => {
  if (!confirm("Archive this course?")) return;

  const course = courses.value.find((c) => c.course_code === course_code);
  if (!course) return;

  try {
    const response = await fetch(`${BASE_URL}/teacher/archive/${course_code}`, {
      headers: { "X-CSRF-Token": csrf_token },
      method: "POST",
      credentials: "include",
    });

    if (!response.ok) {
      const err = await response.json();
      alert(err.detail || "Archive failed");
      return;
    }

    courses.value = courses.value.filter((c) => c.course_code !== course_code);
    archivedCourses.value.push(course);
    await fetchDashboard();
  } catch (error) {
    console.error("Archive error:", error);
  }
};

// ลบ course
const deleteCourse = async (id) => {
  if (!confirm("Delete this course?")) return;

  try {
    const response = await fetch(`${BASE_URL}/teacher/delete_course/${id}`, {
      headers: { "X-CSRF-Token": csrf_token },
      method: "POST",
      credentials: "include",
    });

    if (!response.ok) {
      const err = await response.json();
      alert(err.detail || "Delete failed");
      return;
    }

    courses.value = courses.value.filter((course) => course.course_code !== id);
  } catch (error) {
    console.error("Delete error:", error);
    alert("Something went wrong");
  }
};

//ไปที่หน้า Assignment
const goToAssignment = (course_code) => {
  router.push(`/teacher/assignments/${course_code}`);
};

// ###########################################################################################################################################################

const handleLogout = async () => {
  try {
    const response = await fetch(`${BASE_URL}/logout`, {
      method: "GET",
      credentials: "include",
    });

    if (!response.ok) {
      throw new Error();
    }

    localStorage.removeItem("csrf_token");
    localStorage.removeItem("role");
    router.push("/login");
  } catch (error) {
    console.error("Logout failed:", error);
  }
};

// ######################## page ###################################################################################################################################
const totalPages = computed(() => {
  return Math.ceil(filteredCourses.value.length / itemsPerPage);
});

const paginatedCourses = computed(() => {
  const start = (currentPage.value - 1) * itemsPerPage;
  const end = start + itemsPerPage;
  return filteredCourses.value.slice(start, end);
});

const pages = computed(() => {
  const total = totalPages.value;
  const current = currentPage.value;
  const maxButtons = 5;

  if (total <= maxButtons) {
    return Array.from({ length: total }, (_, i) => i + 1);
  }

  let start = current - Math.floor(maxButtons / 2);
  let end = current + Math.floor(maxButtons / 2);

  if (start < 1) {
    start = 1;
    end = maxButtons;
  }

  if (end > total) {
    end = total;
    start = total - maxButtons + 1;
  }

  const result = [];
  for (let i = start; i <= end; i++) {
    result.push(i);
  }

  return result;
});

const goToPage = (page) => {
  currentPage.value = page;
};

const nextPage = () => {
  if (currentPage.value < totalPages.value) {
    currentPage.value++;
  }
};

const prevPage = () => {
  if (currentPage.value > 1) {
    currentPage.value--;
  }
};

const goToFirstPage = () => {
  currentPage.value = 1;
};

const goToLastPage = () => {
  currentPage.value = totalPages.value;
};

onMounted(() => {
  document.addEventListener("click", handleClickOutside);
  fetchDashboard();
  fetchUserProfile();
  const params = new URLSearchParams(window.location.search);
  if (params.get("google") === "connect_success") {
    if (!sessionStorage.getItem("google_connected")) {
      sessionStorage.setItem("google_connected", "true");
      alert("🎉 Google connected successfully!");
      window.location.reload();
    }
    window.history.replaceState({}, document.title, window.location.pathname);
  }
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

@keyframes cardEnter {
  0% {
    opacity: 0;
    transform: translateY(25px) scale(0.97);
  }
  100% {
    opacity: 1;
    transform: translateY(0) scale(1);
  }
}

.animate-card {
  opacity: 0;
  transform: translateY(25px) scale(0.97);
  animation: cardEnter 0.5s cubic-bezier(0.16, 1, 0.3, 1) forwards;
  will-change: transform, opacity;
}

.delay-1 {
  animation-delay: 0.08s;
}

.delay-2 {
  animation-delay: 0.16s;
}

.delay-3 {
  animation-delay: 0.24s;
}

.delay-4 {
  animation-delay: 0.2s;
}

.delay-5 {
  animation-delay: 0.25s;
}

.btn-animate {
  transition: all 0.18s ease;
}

.btn-animate:hover {
  transform: translateY(-2px);
}

.btn-animate:active {
  transform: scale(0.95);
}

.modal-enter-active {
  animation: modalIn 0.25s ease;
}

@keyframes modalIn {
  0% {
    opacity: 0;
    transform: scale(0.9) translateY(15px);
  }
  100% {
    opacity: 1;
    transform: scale(1) translateY(0);
  }
}
</style>
