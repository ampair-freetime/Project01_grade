<template>
  <div
    class="bg-gray-50 dark:bg-background-dark text-text-light dark:text-text-dark transition-colors duration-200 min-h-screen flex flex-col"
  >
    <header
      class="bg-surface-light dark:bg-surface-dark border-b border-border-light dark:border-border-dark sticky h-16 top-0 z-10 shadow-sm"
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
                  {{ userProfile?.first_name }}
                </span>
              </div>
              <div class="relative">
                <img
                  alt="User profile picture"
                  class="h-10 w-10 rounded-full object-cover border-2 border-primary"
                  :src="randomAvatar"
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
                    :src="randomAvatar"
                  />
                  <div>
                    <p
                      class="font-semibold text-gray-900 dark:text-white break-all"
                    >
                      {{ userProfile?.first_name }} {{ userProfile?.middle }}
                      {{ userProfile?.last_name }}
                    </p>
                    <p class="text-sm text-gray-500 break-all">
                      Email : {{ userProfile?.email }}
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
    <main class="flex-1 flex flex-col h-full overflow-hidden relative">
      <div class="flex-1 overflow-y-auto p-8 lg:p-12">
        <div class="max-w-5xl mx-auto flex flex-col gap-8">
          <nav
            aria-label="Breadcrumb"
            class="mb-6 text-sm text-text-muted-light dark:text-text-muted-dark"
          >
            <button
            class="group inline-flex items-center gap-3 font-bold text-[#111811] dark:text-white hover:text-primary transition-colors"
            type="button"
            @click="router.push(`/teacher/courses`)"
          >
            <div
              class="flex size-9 items-center justify-center rounded-full bg-surface-light dark:bg-surface-dark border border-border-light dark:border-border-dark shadow-sm group-hover:border-primary group-hover:text-primary transition-colors"
            >
              <span class="material-symbols-outlined text-[20px]">
                arrow_back
              </span>
            </div>
            <span>Return</span>
          </button>

            <div class="flex flex-wrap items-center gap-2 mt-4">
              <button
                class="hover:text-primary font-medium"
                type="button"
                @click="router.push('/teacher/courses')"
              >
                Course Management
              </button>
              <span class="font-medium"> / </span>
              <span class="text-[#111811] dark:text-white font-medium">
                {{ courseTitle || `Course #${courseID}` }}
              </span>
            </div>
          </nav>
          <div
            class="flex flex-col md:flex-row md:items-center justify-between gap-4 mb-8"
          >
            <h1
              class="text-3xl font-bold text-gray-900 dark:text-white break-words"
            >
              {{ courseTitle || "Assignments" }}
            </h1>
            <div class="flex flex-col sm:flex-row gap-4 w-full md:w-auto">
              <div class="relative w-full md:w-64">
                <div
                  class="absolute inset-y-0 left-0 pl-3 flex items-center pointer-events-none"
                >
                  <span class="material-symbols-outlined text-gray-400"
                    >search</span
                  >
                </div>
                <input
                  v-model="searchTerm"
                  id="search"
                  name="search"
                  class="block w-full pl-10 pr-3 py-3 border border-border-light dark:border-border-dark rounded-md leading-5 bg-white dark:bg-surface-dark text-gray-900 dark:text-gray-100 placeholder-gray-500 focus:outline-none focus:ring-1 focus:ring-primary focus:border-primary sm:text-sm"
                  placeholder="Search assignments..."
                  type="text"
                />
              </div>
              <div>
                <button
                  @click="createAssignment"
                  class="inline-flex items-center justify-center px-4 py-2 border border-transparent text-sm font-medium rounded-md shadow-sm text-white bg-primary hover:bg-primary-dark focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-primary transition-colors whitespace-nowrap"
                >
                  <span class="material-symbols-outlined mr-2 text-lg"
                    >add</span
                  >
                  Create New Assignment
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

                  <h2 class="text-2xl font-semibold mb-4">
                    Create New Assignment
                  </h2>
                  <div class="mb-4">
                    <label class="block text-lg py-1">Assignment Title</label>
                    <input
                      v-model="assignmentTitle"
                      type="text"
                      class="w-full border border-gray-300 dark:border-gray-800 rounded-md dark:bg-gray-700 px-3 py-2 focus:outline-none focus:ring-green-200"
                      placeholder="e.g., HW01 - Python001"
                    />
                  </div>
                  <div class="mb-4">
                    <label class="block text-lg py-1">Score</label>
                    <input
                      v-model="score"
                      type="number"
                      class="w-full border border-gray-300 dark:border-gray-800 rounded-md dark:bg-gray-700 px-3 py-2 focus:outline-none focus:ring-green-200"
                      placeholder="e.g., 30"
                    />
                  </div>

                  <div class="flex justify-end gap-3">
                    <button
                      @click="submit"
                      class="px-6 py-3 rounded-md bg-green-600 hover:bg-green-800 text-white text-base"
                    >
                      Create Assignment
                    </button>
                  </div>
                </div>
              </div>
            </div>
          </div>
          <div class="flex flex-col space-y-4">
            <div
              v-if="assignments.length === 0"
              class="bg-white dark:bg-surface-dark border border-dashed border-border-light dark:border-border-dark rounded-xl px-6 py-10 text-center text-sm text-text-muted-light dark:text-text-muted-dark"
            >
              No assignments for this course yet.
            </div>

            <div
              v-for="assignment in filteredAssignment"
              :key="assignment.assign_id"
              class="bg-white dark:bg-surface-dark border border-border-light dark:border-border-dark rounded-xl px-6 py-5 shadow-sm hover:shadow-md transition-shadow"
            >
              <div class="flex items-center justify-between">
                <h3 class="text-lg font-semibold text-gray-900 dark:text-white">
                  {{ assignment.assign_name || assignment.quiz_name }}
                </h3>
                <div class="flex items-center gap-4">
                  <span
                    class="inline-flex items-center rounded-full bg-gray-100 dark:bg-gray-700 px-3 py-1 text-xs font-medium text-gray-700 dark:text-gray-200"
                  >
                    Full mark:
                    <span class="ml-1 font-semibold">
                      {{ assignment.full_mark ?? assignment.full_score ?? "-" }}
                    </span>
                  </span>
                  <button
                    class="text-sm font-medium text-primary hover:text-primary-dark border border-border-light dark:border-border-dark hover:border-primary bg-white dark:bg-surface-dark rounded-lg px-4 py-2 transition-colors shadow-sm"
                    @click="goToGrade(assignment.assign_id)"
                  >
                    View &amp; Edit Scores
                  </button>

                  <button
                    @click="archiveAssignment(assignment)"
                    class="p-2 text-gray-400 hover:text-yellow-600 hover:bg-yellow-50 dark:hover:bg-yellow-900/30 rounded-full transition-colors duration-200 group"
                    title="Archive Assignment"
                  >
                    <span class="material-symbols-outlined text-xl"
                      >archive</span
                    >
                  </button>
                  <button
                    @click="deleteAssign(assignment.assign_id)"
                    class="p-2 text-gray-400 hover:text-red-600 hover:bg-red-50 dark:hover:bg-red-500/10 rounded-full transition-colors duration-200 group"
                    title="Delete Assignment"
                  >
                    <span class="material-symbols-outlined text-xl"
                      >delete</span
                    >
                  </button>
                </div>
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
        id="archive-btn"
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

        <h2 class="text-xl font-semibold mb-4">Archived Assignment</h2>

        <ul v-if="archivedAssignments.length" class="space-y-2">
          <li
            v-for="assignment in archivedAssignments"
            :key="assignment.assign_id"
            class="rounded-xl hover:bg-gray-100 dark:hover:bg-gray-600/50 transition-colors duration-150"
          >
            <div class="px-4 py-2 flex items-center">
              <div class="grow items-center">
                <div class="text-sm font-bold text-gray-900 dark:text-white">
                  {{ assignment.assign_name || assignment.quiz_name }}
                </div>
              </div>
              <div class="flex items-center gap-6">
                <div class="flex items-end min-w-[50px]">
                  <button
                    class="p-2 text-gray-400 hover:text-yellow-600 hover:bg-yellow-50 dark:hover:bg-yellow-900/30 rounded-full transition-colors duration-200 group"
                    title="Restore Assignment"
                    @click="restoreArchivedAssignment(assignment)"
                  >
                    <span
                      class="material-symbols-outlined text-xl group-hover:text-yellow-600"
                      >restore</span
                    >
                  </button>
                  <button
                    class="p-2 text-gray-400 hover:text-red-600 hover:bg-red-50 dark:hover:bg-red-900/30 rounded-full transition-colors duration-200 group"
                    title="Delete Assignment"
                    @click="deleteArchivedAssignment(assignment.assign_id)"
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
          class="text-sm text-text-muted-light dark:text-text-muted-dark py-1"
        >
          No archived assignments.
        </p>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted, onBeforeUnmount, computed } from "vue";
import { useRouter, useRoute } from "vue-router";

defineOptions({
  name: "AssignmentManagement",
});

const router = useRouter();
const route = useRoute();

const showArchiveModal = ref(false);
const startCreate = ref(false);
const isOpen = ref(false);
const dropdownRef = ref(null);
const courseID = computed(() => Number(route.params.course_id));
const assignmentTitle = ref("");
const score = ref("");
const searchTerm = ref("");
const userProfile = ref(null);
const assignments = ref([]);
const courseTitle = ref("");
const csrf_token = localStorage.getItem("csrf_token");
const archivedAssignments = ref([]);
const randomAvatar = ref("");

const BASE_URL = "http://localhost:56733";

// ################################ fetch ###########################################################################################################################

const fetchAssignment = async (course_id) => {
  try {
    const response = await fetch(
      `${BASE_URL}/teacher/assignment/${course_id}`,
      {
        method: "GET",
        credentials: "include",
      }
    );

    if (!response.ok) {
      const text = await response.text().catch(() => "");
      console.error("Fetch assignment failed:", response.status, text);
      throw new Error("Fetch failed");
    }

    const data = await response.json();
    // backend:
    // {
    //   course: { course_id, course_name },
    //   assignment: [{ assign_id, assign_name, full_mark }, ...]
    // }

    if (Array.isArray(data.assignment)) {
      assignments.value = data.assignment;
    } else if (Array.isArray(data)) {
      assignments.value = data;
    } else {
      assignments.value = [];
    }
    courseTitle.value = data.course?.course_name || courseTitle.value;
  } catch (err) {
    console.error(err);
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
// ################################ pop-up ###########################################################################################################################
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

const createAssignment = () => {
  startCreate.value = true;
};

const cancleCreate = () => {
  startCreate.value = false;
};

// ################################ Assignment ###########################################################################################################################

// กรอง assignment ตามการค้นหา
const filteredAssignment = computed(() => {
  const term = searchTerm.value.trim().toLowerCase();
  if (!term) return assignments.value;

  return assignments.value.filter((a) => {
    const name = (a.assign_name || a.quiz_name || "").toLowerCase();
    return name.includes(term);
  });
});

const submit = async () => {
  try {
    if (!assignmentTitle.value || !assignmentTitle.value.trim()) {
      alert("Please enter assignment title");
      return;
    }
    if (!score.value) {
      alert("Please enter full mark");
      return;
    }

    const response = await fetch(`${BASE_URL}/teacher/create_assign`, {
      method: "POST",
      credentials: "include",
      headers: {
        "Content-Type": "application/json",
        "X-CSRF-Token": csrf_token,
      },
      body: JSON.stringify({
        quiz_name: assignmentTitle.value.trim(),
        full_mark: Number(score.value),
        course_id: courseID.value,
      }),
    });

    if (!response.ok) {
      throw new Error("Create assignment failed");
    }

    const data = await response.json();
    console.log("Created:", data);

    startCreate.value = false;

    assignmentTitle.value = "";
    score.value = "";

    if (courseID.value) {
      await fetchAssignment(courseID.value);
    }
  } catch (error) {
    console.error(error);
  }
};

const deleteAssign = async (assign_id) => {
  if (!confirm("Delete this Assignment?")) return;

  try {
    const response = await fetch(
      `${BASE_URL}/teacher/delete_assign/${assign_id}`,
      {
        method: "POST",
        headers: {
          "X-CSRF-Token": csrf_token,
        },
        credentials: "include",
      }
    );

    if (!response.ok) {
      throw new Error("Delete failed");
    }
    if (courseID.value) {
      await fetchAssignment(courseID.value);
    }
  } catch (err) {
    console.error("Delete failed", err);
  }
};

const archiveAssignment = async (assignment) => {
  if (!confirm("Archive this assignment?")) return;
  try {
    archivedAssignments.value.push(assignment);
    assignments.value = assignments.value.filter(
      (a) => a.assign_id !== assignment.assign_id
    );
  } catch (err) {
    console.error("Archive failed", err);
  }
};
// ################################ Archive ###########################################################################################################################

//คาดว่าจะลบ
const restoreArchivedAssignment = (assignment) => {
  archivedAssignments.value = archivedAssignments.value.filter(
    (a) => a.assign_id !== assignment.assign_id
  );
  assignments.value.push(assignment);
};

const deleteArchivedAssignment = async (assign_id) => {
  if (!confirm("Permanently delete this assignment?")) return;
  archivedAssignments.value = archivedAssignments.value.filter(
    (a) => a.assign_id !== assign_id
  );
};

// ###########################################################################################################################################################
const goToGrade = (quiz_id) => {
  router.push({
    path: `/teacher/grade/${quiz_id}`,
    query: {
      course_id: courseID.value,
      course_title: courseTitle.value,
    },
  });
};

const handleLogout = async () => {
  try {
    const response = await fetch(`${BASE_URL}/logout`, {
      method: "GET",
      credentials: "include",
    });

    if (!response.ok) {
      throw new Error("Logout request failed");
    }

    localStorage.removeItem("csrf_token");
    localStorage.removeItem("role");

    router.push("/login");
  } catch (error) {
    console.error("Logout failed:", error);
  }
};

onMounted(() => {
  document.addEventListener("click", handleClickOutside);
  if (courseID.value) {
    fetchAssignment(courseID.value);
  }
  const seed = Math.random().toString(36).substring(7);
  randomAvatar.value = `https://robohash.org/${seed}.png`;
  fetchUserProfile();
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