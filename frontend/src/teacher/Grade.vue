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
              @click="router.go(-2)"
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
                      {{ userProfile?.first_name }} {{ userProfile?.middle_name }} {{ userProfile?.last_name }}
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
          <nav
            aria-label="Breadcrumb"
            class="flex flex-col gap-4 text-sm text-text-muted-light dark:text-text-muted-dark"
          >
            <!-- Return -->
            <button
              class="group inline-flex items-center mb-1 gap-3 font-bold text-[#111811] dark:text-white hover:text-primary transition-colors"
              type="button"
              @click="router.push(`/teacher/assignments/${courseId}`)"
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

            <!-- Navigaton -->
            <div class="animate-card delay-1 flex flex-wrap items-center gap-2">
              <button
                class="hover:text-primary font-medium"
                @click="router.go(-2)"
              >
                Course Management
              </button>

              <span class="font-medium">/</span>

              <button
                class="hover:text-primary font-medium"
                @click="router.go(-1)"
              >
                {{
                  courseTitle ||
                  (courseId ? `Course #${courseId}` : "Assignments")
                }}
              </button>

              <span class="font-medium">/</span>

              <span class="text-[#111811] dark:text-white font-medium">
                {{ assignment_title || "Assignment" }}
              </span>
            </div>
          </nav>
          <div
            class="animate-card delay-1 flex items-center justify-between flex-wrap gap-4"
          >
            <h1 class="text-4xl font-bold text-gray-900 dark:text-white">
              {{ assignment_title || "Assignment" }}
            </h1>
            <div class="animate-card delay-2 flex items-center gap-3">
              <label
                class="inline-flex items-center px-4 py-2 bg-white dark:bg-slate-800 border border-gray-300 dark:border-slate-600 rounded-lg text-sm font-medium text-gray-700 dark:text-gray-200 hover:bg-gray-50 dark:hover:bg-slate-700 shadow-sm transition-colors"
              >
                <span class="material-symbols-outlined text-lg mr-2"
                  >upload_file</span
                >
                Import CSV
                <input
                  type="file"
                  accept=".csv"
                  class="hidden"
                  @change="handleFileUpload"
                />
              </label>
              <button
                @click="publishScores"
                :disabled="isPublished"
                :class="[
                  'inline-flex items-center px-4 py-2 border border-transparent rounded-lg text-sm font-medium text-white shadow-sm transition-colors',
                  isPublished ? 'bg-black cursor-not-allowed opacity-80' : 'bg-sky-500 hover:opacity-70',
                ]"
              >
                <span class="material-symbols-outlined text-lg mr-2">
                  {{ isPublished ? "check_circle" : "publish" }}
                </span>
                {{ isPublished ? "Published" : "Publish Scores" }}
              </button>
            </div>
          </div>

          <!-- ผล import CSV: คนที่ยังไม่มีบัญชี / email ไม่ตรง จะยังไม่ได้คะแนน -->
          <div
            v-if="uploadResult"
            class="rounded-xl border p-4 text-sm"
            :class="
              uploadResult.unmatched.length
                ? 'border-yellow-300 bg-yellow-50 dark:bg-yellow-900/20 dark:border-yellow-700'
                : 'border-green-300 bg-green-50 dark:bg-green-900/20 dark:border-green-700'
            "
            role="status"
          >
            <div class="flex items-start justify-between gap-3">
              <p class="font-semibold">
                Imported {{ uploadResult.matched }} score(s).
                <span v-if="uploadResult.unmatched.length">
                  {{ uploadResult.unmatched.length }} row(s) skipped — these
                  students need to sign up (or fix the email), then import the
                  CSV again.
                </span>
              </p>
              <button
                @click="uploadResult = null"
                class="text-gray-500 hover:text-red-500"
                aria-label="Dismiss"
              >
                ✕
              </button>
            </div>
            <ul v-if="uploadResult.unmatched.length" class="mt-2 space-y-1">
              <li
                v-for="row in uploadResult.unmatched"
                :key="row.student_id"
                class="flex flex-wrap gap-x-3"
              >
                <span class="font-mono">{{ row.student_id }}</span>
                <span>{{ row.name }}</span>
                <span class="text-gray-500">{{ row.email }}</span>
                <span class="text-yellow-700 dark:text-yellow-400">{{
                  row.reason === "email_mismatch"
                    ? "email does not match account"
                    : "not signed up"
                }}</span>
              </li>
            </ul>
          </div>

          <div
            class="animate-card delay-3 px-4 py-6 bg-surface-light dark:bg-surface-dark rounded-xl border border-border-light dark:border-border-dark flex flex-col md:flex-row items-center justify-between gap-4 shadow-sm"
          >
            <div class="relative w-full md:w-96 min-w-0">
              <span
                class="absolute inset-y-0 left-0 pl-3 flex items-center pointer-events-none"
              >
                <span
                  class="material-symbols-outlined text-gray-400 dark:text-gray-500"
                  >search</span
                >
              </span>
              <input
                v-model="searchTerm"
                class="pl-10 pr-4 py-2 w-full bg-gray-50 dark:bg-slate-800/50 border border-gray-200 dark:border-slate-700 rounded-lg text-sm focus:ring-2 focus:ring-sky-500 focus:border-transparent dark:text-white dark:placeholder-gray-500"
                placeholder="Search by name or student ID..."
                type="text"
              />
            </div>
            <div
              class="flex items-center gap-4 w-full md:w-auto justify-between md:justify-end overflow-x-auto pb-2 md:pb-0 flex-shrink-0"
            >
              <div class="flex flex-wrap items-center gap-2 text-sm">
                <span
                  class="uppercase text-xs font-bold tracking-wider mr-1 text-gray-500 dark:text-gray-300"
                  >Status :</span
                >
                <div class="flex flex-nowrap items-center gap-2">
                  <button
                    @click="statusFilter = 'all'"
                    :class="[
                      'px-3 py-1.5 whitespace-nowrap rounded-md font-medium text-xs',
                      statusFilter === 'all'
                        ? 'bg-gray-300 text-black dark:bg-gray-400 dark:text-black'
                        : 'text-gray-600 dark:text-gray-300 hover:bg-gray-100 dark:hover:bg-slate-700',
                    ]"
                  >
                    All Students
                  </button>

                  <button
                    @click="statusFilter = 'Read'"
                    :class="[
                      'px-3 py-1.5 rounded-md font-medium text-xs flex items-center gap-1 transition-colors',
                      statusFilter === 'Read'
                        ? 'bg-gray-300 text-black dark:bg-gray-400 dark:text-black'
                        : 'text-gray-600 dark:text-gray-300 hover:bg-gray-100 dark:hover:bg-slate-700',
                    ]"
                  >
                    Read
                    <span
                      class="bg-sky-100 dark:bg-sky-800 text-sky-700 dark:text-sky-100 px-1.5 py-0.5 rounded-full text-[10px]"
                    >
                      {{ readCount }}
                    </span>
                  </button>

                  <button
                    @click="statusFilter = 'Unread'"
                    :class="[
                      'px-3 py-1.5 rounded-md font-medium text-xs flex items-center gap-1 transition-colors',
                      statusFilter === 'Unread'
                        ? 'bg-gray-300 text-black dark:bg-gray-400 dark:text-black'
                        : 'text-gray-600 dark:text-gray-300 hover:bg-gray-100 dark:hover:bg-slate-700',
                    ]"
                  >
                    Unread
                    <span
                      class="bg-amber-200 dark:bg-yellow-600 text-amber-900 dark:text-yellow-50 px-1.5 py-0.5 rounded-full text-[10px]"
                    >
                      {{ unreadCount }}
                    </span>
                  </button>
                </div>
              </div>

              <div
                class="animate-card delay-4 flex items-center gap-2 text-sm whitespace-nowrap"
              >
                <span
                  class="uppercase text-xs font-bold tracking-wider text-gray-400 dark:text-gray-300"
                  >Sort By:</span
                >
                <select
                  v-model="sortOption"
                  @change="sortPeople"
                  class="border border-gray-300 rounded-md pl-3 pr-8 py-1 text-sm dark:bg-gray-700 dark:border-gray-600"
                >
                  <option value="id_lowhigh">ID</option>

                  <option value="name_atoz">Name</option>
                </select>
              </div>
            </div>
          </div>
          <div
            class="animate-card delay-4 bg-surface-light dark:bg-surface-dark rounded-xl border border-border-light dark:border-border-dark shadow-sm overflow-hidden"
          >
            <div class="overflow-x-auto">
              <table class="w-full table-fixed text-left">
                <thead>
                  <tr
                    class="border-b border-border-light dark:border-border-dark bg-gray-50/50 dark:bg-slate-800/50"
                  >
                    <th
                      class="min-w-[120px] p-4 text-xs font-bold text-gray-500 text-center"
                    >
                      Student Info
                    </th>

                    <th
                      class="min-w-[120px] p-4 text-xs font-bold text-gray-500 text-center"
                    >
                      Score
                    </th>

                    <th
                      class="min-w-[120px] p-4 text-xs font-bold text-gray-500 text-center"
                    >
                      Status
                    </th>

                    <th
                      class="min-w-[120px] p-4 text-xs font-bold text-gray-500 text-center"
                    >
                      Actions
                    </th>
                  </tr>
                </thead>
                <tbody
                  class="divide-y divide-border-light dark:divide-border-dark"
                >
                  <tr
                    v-for="student in paginatedStudents"
                    :key="student.student_id"
                    class="group hover:bg-gray-50 dark:hover:bg-slate-800/50 transition-colors"
                  >
                    <td class="p-4 pl-6">
                      <div class="flex items-center gap-3">
                        <div class="relative flex-shrink-0">
                          <img
                            v-if="student.avatar_url"
                            :src="student.avatar_url"
                            alt="Student profile"
                            class="w-12 h-12 rounded-full object-cover border border-gray-200 dark:border-slate-600"
                          />
                          <div
                            v-else
                            :src="student.avatar_url"
                            class="w-12 h-12 rounded-full flex items-center justify-center font-bold text-sm"
                            :class="getAvatarColor(student)"
                          >
                            {{ getInitials(student) }}
                          </div>
                        </div>
                        <div>
                          <div
                            class="font-semibold text-sm text-gray-900 dark:text-white"
                          >
                            {{ student.stu_fname }} {{ student.stu_mname }}
                            {{ student.stu_lname }}
                          </div>
                          <div
                            class="text-xs text-text-muted-light dark:text-text-muted-dark"
                          >
                            ID: {{ student.student_id }}
                          </div>
                          <div
                            class="text-xs text-text-muted-light dark:text-text-muted-dark"
                          >
                            section : {{ student.section }}
                          </div>
                        </div>
                      </div>
                    </td>
                    <td class="p-4 text-center">
                      <div
                        class="w-16 h-10 mx-auto border border-gray-200 dark:border-slate-600 rounded-lg flex items-center justify-center font-semibold text-gray-900 dark:text-white bg-white dark:bg-slate-900"
                      >
                        {{ student.score }}
                      </div>
                    </td>
                    <td class="p-4 text-center">
                      <span
                        class="inline-flex items-center gap-1.5 px-2.5 py-1 rounded-full text-xs font-medium"
                        :class="
                          student.status === 'Unread'
                            ? 'bg-amber-100 dark:bg-yellow-900/50 text-amber-700 dark:text-yellow-300'
                            : 'bg-sky-100 dark:bg-sky-700/40 text-sky-700 dark:text-sky-200'
                        "
                      >
                        <span
                          class="w-1.5 h-1.5 rounded-full"
                          :class="
                            student.status === 'Unread'
                              ? 'bg-amber-500 dark:bg-yellow-400'
                              : 'bg-sky-500'
                          "
                        ></span>
                        {{ student.status }}
                      </span>
                    </td>
                    <td class="p-4 text-center">
                      <button
                        @click="deleteScore(student)"
                        class="p-2 rounded-full hover:bg-red-50 text-gray-400 hover:text-red-500 dark:hover:bg-red-900/20 dark:hover:text-red-400 transition-colors"
                        title="Delete record"
                      >
                        <span class="material-symbols-outlined text-[20px]"
                          >delete</span
                        >
                      </button>
                    </td>
                  </tr>
                </tbody>
              </table>
            </div>
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
                <!--first-->
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
  </div>
</template>

<script setup>
import { ref, onMounted, onBeforeUnmount, computed } from "vue";
import { useRouter, useRoute } from "vue-router";

defineOptions({
  name: "Grade",
});

const router = useRouter();
const route = useRoute();
const isOpen = ref(false);
const dropdownRef = ref(null);

const students = ref([]);
const searchTerm = ref("");
const sortOption = ref("id_lowhigh");
const sortOpen = ref(false);
const statusFilter = ref("all");
const isPublished = ref(false);
const uploadResult = ref(null);

const currentPage = ref(1);
const itemsPerPage = 5;

const quizID = computed(() => String(route.params.quiz_id));
const courseId = computed(() => Number(route.query.course_code));
const courseTitle = computed(() =>
  route.query.course_title ? String(route.query.course_title) : ""
);

const randomAvatar = ref("");
const userProfile = ref(null);
const assignment_title = ref("");
const csrfToken = localStorage.getItem("csrf_token");

const readCount = computed(
  () => students.value.filter((s) => s.status === "Read").length
);
const unreadCount = computed(
  () => students.value.filter((s) => s.status === "Unread").length
);
const BASE_URL = "/api";

const connectGoogle = () => {
  window.location.href = `${BASE_URL}/login_with_google`;
};

// ########################################### fetch ###################################################################################################################

const fetchTeacherGrade = async (quiz_id) => {
  try {
    const response = await fetch(`${BASE_URL}/teacher/stu_score/${quiz_id}`, {
      method: "GET",
      credentials: "include",
    });
    if (!response.ok) {
      const text = await response.text().catch(() => "");
      console.error("Fetch student score failed:", response.status, text);
      throw new Error("Fetch failed");
    }

    const data = await response.json();
    assignment_title.value = data?.assignment?.assign_name;
    isPublished.value = data?.assignment?.is_publish ?? false;

    const scoreList = Array.isArray(data?.score) ? data.score : [];

    students.value = scoreList.map((s) => ({
      score_id: s.score_id,
      student_id: s.stu_id,
      stu_fname: s.stu_fname,
      stu_mname: s.stu_mname,
      stu_lname: s.stu_lname,
      avatar_url: s.avatar_url,
      score: s.score,
      section: s.section,
      status: s.unread_flag ? "Unread" : "Read",
    }));

    sortPeople();
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

const avatarColorClasses = [
  "bg-sky-100 text-sky-700 dark:bg-sky-900 dark:text-sky-200",
  "bg-emerald-100 text-emerald-700 dark:bg-emerald-900 dark:text-emerald-200",
  "bg-violet-100 text-violet-700 dark:bg-violet-900 dark:text-violet-200",
  "bg-amber-100 text-amber-700 dark:bg-amber-900 dark:text-amber-200",
  "bg-rose-100 text-rose-700 dark:bg-rose-900 dark:text-rose-200",
];

const getInitials = (student) => {
  const parts = [student.stu_fname, student.stu_mname, student.stu_lname]
    .filter(Boolean)
    .join(" ")
    .trim()
    .split(/\s+/);

  if (!parts.length) return "?";
  if (parts.length === 1) return parts[0].charAt(0).toUpperCase();
  return (parts[0].charAt(0) + parts[parts.length - 1].charAt(0)).toUpperCase();
};

const getAvatarColor = (student) => {
  const idStr = String(student.student_id || "");
  let hash = 0;
  for (let i = 0; i < idStr.length; i++) {
    hash = (hash * 31 + idStr.charCodeAt(i)) >>> 0;
  }
  return avatarColorClasses[hash % avatarColorClasses.length];
};
// ########################################### pop-up ###################################################################################################################

const filteredStudents = computed(() => {
  const term = searchTerm.value.trim().toLowerCase();

  return students.value.filter((s) => {
    const name = `${s.stu_fname || ""} ${s.stu_lname || ""}`.toLowerCase();
    const id = String(s.student_id || "");

    const matchSearch = !term || name.includes(term) || id.includes(term);

    const matchStatus =
      statusFilter.value === "all" || s.status === statusFilter.value;

    return matchSearch && matchStatus;
  });
});

const toggleDropdown = () => {
  isOpen.value = !isOpen.value;
};

const handleClickOutside = (event) => {
  if (dropdownRef.value && !dropdownRef.value.contains(event.target)) {
    isOpen.value = false;
  }
};

// ########################################### grade ###################################################################################################################

const handleFileUpload = async (event) => {
  const file = event.target.files[0];
  // ให้เลือกไฟล์เดิมซ้ำได้ (import ใหม่หลังนักศึกษาสมัครแล้ว)
  event.target.value = "";

  console.log("File:", file);
  console.log("courseId:", courseId.value);
  console.log("quizID:", quizID.value);

  if (!file || !courseId.value || !quizID.value) {
    alert("Missing required data!");
    return;
  }
  console.log("Starting upload...");

  const formdata = new FormData();
  formdata.append("file", file);

  try {
    const csrfToken = localStorage.getItem("csrf_token") || "";
    const response = await fetch(
      `${BASE_URL}/teacher/upload/${courseId.value}/${quizID.value}`,
      {
        method: "POST",
        credentials: "include",
        headers: {
          "X-CSRF-Token": csrfToken,
        },
        body: formdata,
      }
    );

    if (!response.ok) {
      const errorData = await response.json().catch(() => null);
      alert(errorData?.detail || "Upload failed");
      return;
    }

    isPublished.value = false;
    uploadResult.value = await response.json();
    await fetchTeacherGrade(quizID.value);
  } catch (err) {
    console.error(err);
    alert("Upload failed");
  }
};

const deleteScore = async (student) => {
  if (!confirm(`You want to delete this score?`)) return;
  try {
    const response = await fetch(
      `${BASE_URL}/teacher/delete_score/${quizID.value}/${student.score_id}`,
      {
        method: "POST",
        credentials: "include",
        headers: {
          "X-CSRF-Token": csrfToken,
        },
      }
    );

    if (!response.ok) {
      throw new Error("Delete failed");
      return;
    }
    if (quizID.value) {
      await fetchTeacherGrade(quizID.value);
    }
  } catch (error) {
    console.error("Delete score failed:", error);
    alert("ลบคะแนนไม่สำเร็จ");
  }
};

const publishScores = async () => {
  if (!quizID.value) return;

  if (!confirm("Publish scores to students?")) return;

  try {
    const response = await fetch(
      `${BASE_URL}/teacher/publish/${quizID.value}`,
      {
        method: "POST",
        credentials: "include",
        headers: {
          "X-CSRF-Token": csrfToken,
        },
      }
    );

    const data = await response.json();

    if (!response.ok) {
      alert(data.detail || "Publish failed");
      return;
    }

    isPublished.value = true;
    alert("Scores published successfully");
  } catch (error) {
    console.error("Publish error:", error);
    alert("Publish failed");
  }
};

// ########################## method ####################################################################################################################################

const sortPeople = () => {
  switch (sortOption.value) {
    case "id_lowhigh":
      students.value.sort((a, b) =>
        String(a.student_id).localeCompare(String(b.student_id))
      );
      break;

    case "name_atoz":
      students.value.sort((a, b) => {
        const hasNameA = a.stu_fname ? 1 : 0;
        const hasNameB = b.stu_fname ? 1 : 0;
        if (hasNameB !== hasNameA) {
          return hasNameB - hasNameA;
        } // มีชื่อขึ้นก่อน

        const fnameCompare = (a.stu_fname || "").localeCompare(
          b.stu_fname || ""
        );
        if (fnameCompare !== 0) {
          return fnameCompare;
        }

        const mnameCompare = (a.stu_mname || "").localeCompare(
          b.stu_mname || ""
        );
        if (mnameCompare !== 0) {
          return mnameCompare;
        }

        return (a.stu_lname || "").localeCompare(b.stu_lname || "");
      });
      break;
  }
};

// ##############################################################################################################################################################
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

// ######################## page ###################################################################################################################################
const totalPages = computed(() => {
  return Math.ceil(filteredStudents.value.length / itemsPerPage);
});

const paginatedStudents = computed(() => {
  const start = (currentPage.value - 1) * itemsPerPage;
  const end = start + itemsPerPage;
  return filteredStudents.value.slice(start, end);
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

const goToCourse = () => {
  router.push(`/teacher/courses`);
};

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
  fetchUserProfile();
  if (quizID.value) {
    fetchTeacherGrade(quizID.value);
  }
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
