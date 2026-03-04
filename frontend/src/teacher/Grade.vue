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
                      {{ userProfile?.first_name }} {{ userProfile?.last_name }}
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
    <main class="w-full">
      <div class="max-w-7xl mx-auto px-6 py-8 space-y-8">
        <nav
          aria-label="Breadcrumb"
          class="mb-6 text-sm text-text-muted-light dark:text-text-muted-dark"
        >
          <!-- Return -->
          <button
            class="group inline-flex items-center gap-3 font-bold text-[#111811] dark:text-white hover:text-primary transition-colors"
            type="button"
            @click="router.push(`/teacher/assignments/${assign_id}`)"
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

          <!-- Path -->
          <div class="flex flex-wrap items-center gap-2 mt-4">
            <a class="hover:text-primary font-medium" href="#">
              Course Management
            </a>

            <span class="font-medium">/</span>

            <a class="hover:text-primary font-medium" href="#">
              CS101 - Intro to Algorithms
            </a>

            <span class="font-medium">/</span>

            <span class="text-[#111811] dark:text-white font-medium">
              Midterm Exam
            </span>
          </div>
        </nav>
        <div
          class="flex flex-col lg:flex-row lg:items-end justify-between gap-4"
        >
          <div>
            <div class="flex items-center gap-3 mb-1">
              <h1 class="text-3xl font-bold text-gray-900 dark:text-white">
                Midterm Exam
              </h1>
              <span
                class="px-2.5 py-0.5 rounded-full bg-sky-50 dark:bg-sky-900/20 text-sky-700 dark:text-sky-300 text-xs font-semibold border border-sky-700 dark:border-sky-500"
                >Section A</span
              >
            </div>
          </div>
          <div class="flex flex-wrap items-center gap-3">
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
              class="inline-flex items-center px-4 py-2 bg-slate-900 dark:bg-slate-700 border border-transparent rounded-lg text-sm font-medium text-white hover:bg-slate-800 dark:hover:bg-slate-600 shadow-sm transition-colors"
            >
              <span class="material-symbols-outlined text-lg mr-2"
                >publish</span
              >
              Publish Scores
            </button>
            <button
              class="inline-flex items-center px-4 py-2 bg-sky-500 dark:bg-sky-600 border border-transparent rounded-lg text-sm font-medium text-white hover:opacity-90 shadow-sm transition-colors"
            >
              <span class="material-symbols-outlined text-lg mr-2">save</span>
              Save Changes
            </button>
          </div>
        </div>
        <div
          class="px-4 py-6 bg-surface-light dark:bg-surface-dark rounded-xl border border-border-light dark:border-border-dark p-2 flex flex-col md:flex-row items-center justify-between gap-4 shadow-sm"
        >
          <div class="relative w-full md:w-96">
            <span
              class="absolute inset-y-0 left-0 pl-3 flex items-center pointer-events-none"
            >
              <span
                class="material-symbols-outlined text-gray-400 dark:text-gray-500"
                >search</span
              >
            </span>
            <input
              class="pl-10 pr-4 py-2 w-full bg-gray-50 dark:bg-slate-800/50 border border-gray-200 dark:border-slate-700 rounded-lg text-sm focus:ring-2 focus:ring-sky-500 focus:border-transparent dark:text-white dark:placeholder-gray-500"
              placeholder="Search by name or student ID..."
              type="text"
            />
          </div>
          <div
            class="flex items-center gap-4 w-full md:w-auto justify-between md:justify-end overflow-x-auto pb-2 md:pb-0"
          >
            <div class="flex flex-wrap items-center gap-2 text-sm">
              <span
                class="uppercase text-xs font-bold tracking-wider mr-1 text-gray-500 dark:text-gray-300"
                >Status :</span
              >
              <button
                class="px-3 py-1.5 bg-surface-dark dark:bg-surface-light text-white dark:text-slate-900 rounded-md font-medium text-xs"
              >
                All Students
              </button>
              <button
                class="px-3 py-1.5 text-gray-600 dark:text-gray-300 hover:bg-gray-100 dark:hover:bg-slate-700 rounded-md font-medium text-xs flex items-center gap-1 transition-colors"
              >
                Read Announcement
                <span
                  class="bg-sky-100 dark:bg-sky-800 text-sky-700 dark:text-sky-100 px-1.5 py-0.5 rounded-full text-[10px]"
                  >12</span
                >
              </button>
              <button
                class="px-3 py-1.5 text-gray-600 dark:text-gray-300 hover:bg-gray-100 dark:hover:bg-slate-700 rounded-md font-medium text-xs flex items-center gap-1 transition-colors"
              >
                Unread
                <span
                  class="bg-amber-200 dark:bg-yellow-600 text-amber-900 dark:text-yellow-50 px-1.5 py-0.5 rounded-full text-[10px]"
                  >4</span
                >
              </button>
            </div>
            <div
              class="w-px h-6 bg-gray-200 dark:bg-gray-700 hidden md:block"
            ></div>
            <div class="flex items-center gap-2 text-sm whitespace-nowrap">
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

                <option value="section_lowhigh">section</option>
              </select>
            </div>
          </div>
        </div>
        <div
          class="bg-surface-light dark:bg-surface-dark rounded-xl border border-border-light dark:border-border-dark shadow-sm overflow-hidden"
        >
          <div class="overflow-x-auto">
            <table class="w-full table-fixed text-left">
              <thead>
                <tr
                  class="border-b border-border-light dark:border-border-dark bg-gray-50/50 dark:bg-slate-800/50"
                >
                  <th class="min-w-[120px] p-4 text-xs font-bold text-gray-500 text-center">
                    Student Info
                  </th>

                  <th class="min-w-[120px] p-4 text-xs font-bold text-gray-500 text-center">
                    Score
                  </th>

                  <th class="min-w-[120px] p-4 text-xs font-bold text-gray-500 text-center">
                    Status
                  </th>

                  <th class="min-w-[120px] p-4 text-xs font-bold text-gray-500 text-center">
                    Actions
                  </th>
                </tr>
              </thead>
              <tbody
                class="divide-y divide-border-light dark:divide-border-dark"
              >
                <tr
                  v-for="student in students"
                  :key="student.student_id"
                  class="group hover:bg-gray-50 dark:hover:bg-slate-800/50 transition-colors"
                >
                  <td class="p-4 pl-6">
                    <div class="flex items-center gap-3">
                      <div
                        class="w-10 h-10 rounded-full overflow-hidden flex-shrink-0"
                      >
                        <img
                          alt="Alice Johnson"
                          class="w-full h-full object-cover"
                          src="https://lh3.googleusercontent.com/aida-public/AB6AXuBkSaqLRo55aSxruOMViPHwv4KXrCEh-Jt4rRHt0pzsYYkq6PChv3pfMUyxSiCkxd2z0z0KRTtThtJX_QiepD7rSfF-oqCMtqoraUVKfMl_Q2qr8ooHr1DTbhKfoD5zSIQjukFXEShxlvU6EHk3FUhKhMxXdVgoOq8RHG3MHaxcdHo98M6JRhOfbVQzjy0oGXGOx3h6FRjg4ASkFah3R-BqKPGHv_My_GLm8rsCnirFjXf6kvCJ-pUG5JzfUo4gpgfVm87sVrEbOw"
                        />
                      </div>
                      <div>
                        <div
                          class="font-semibold text-gray-900 dark:text-white"
                        >
                          {{ student.student_name }}
                        </div>
                        <div
                          class="text-xs text-text-muted-light dark:text-text-muted-dark"
                        >
                          ID: {{ student.student_id }}
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
                      class="inline-flex items-center gap-1.5 px-2.5 py-1 rounded-full text-xs font-medium bg-sky-100 dark:bg-sky-700/40 text-sky-700 dark:text-sky-200"
                    >
                      <span class="w-1.5 h-1.5 rounded-full bg-sky-500"></span>
                      {{ student.status }}
                    </span>
                  </td>
                  <td class="p-4 text-center">
                    <button
                      class="p-2 rounded-full hover:bg-red-50 text-gray-400 hover:text-red-500 dark:hover:bg-red-900/20 dark:hover:text-red-400 transition-colors"
                      title="Delete record"
                    >
                      <span class="material-symbols-outlined text-[20px]"
                        >delete</span
                      >
                    </button>
                  </td>
                </tr>
                <tr
                  class="group hover:bg-gray-50 dark:hover:bg-slate-800/50 transition-colors"
                >
                  <td class="p-4 pl-6">
                    <div class="flex items-center gap-3">
                      <div
                        class="w-10 h-10 rounded-full bg-blue-100 dark:bg-blue-900 text-blue-600 dark:text-blue-300 flex items-center justify-center font-bold text-sm flex-shrink-0"
                      >
                        BS
                      </div>
                      <div>
                        <div
                          class="font-semibold text-gray-900 dark:text-white"
                        >
                          Bob Smith
                        </div>
                        <div
                          class="text-xs text-text-muted-light dark:text-text-muted-dark"
                        >
                          ID: 2023002
                        </div>
                      </div>
                    </div>
                  </td>
                  <td class="p-4 text-center">
                    <div
                      class="w-16 h-10 mx-auto border border-gray-200 dark:border-slate-600 rounded-lg flex items-center justify-center font-semibold text-gray-900 dark:text-white bg-white dark:bg-slate-900"
                    >
                      85
                    </div>
                  </td>
                  <td class="p-4 text-center">
                    <span
                      class="inline-flex items-center gap-1.5 px-2.5 py-1 rounded-full text-xs font-medium bg-amber-100 dark:bg-yellow-900/50 text-amber-700 dark:text-yellow-300"
                    >
                      <span
                        class="w-1.5 h-1.5 rounded-full bg-amber-500 dark:bg-yellow-400"
                      ></span>
                      Unread
                    </span>
                  </td>
                  <td class="p-4 text-center">
                    <button
                      class="p-2 rounded-full hover:bg-red-50 text-gray-400 hover:text-red-500 dark:hover:bg-red-900/20 dark:hover:text-red-400 transition-colors"
                      title="Delete record"
                    >
                      <span class="material-symbols-outlined text-[20px]"
                        >delete</span
                      >
                    </button>
                  </td>
                </tr>
                <tr
                  class="bg-sky-50/50 dark:bg-sky-900/10 border-l-4 border-l-sky-500"
                >
                  <td class="p-4 pl-6">
                    <div class="flex items-center gap-3">
                      <div
                        class="w-10 h-10 rounded-full overflow-hidden flex-shrink-0 border-2 border-sky-100 dark:border-sky-800"
                      >
                        <img
                          alt="Charlie Brown"
                          class="w-full h-full object-contain bg-amber-50"
                          src="https://lh3.googleusercontent.com/aida-public/AB6AXuBN0g-WHePpThTNMUhPAiYyolESpOvQwcvWsK86MgulRv8D3VHb3aOZJJV34TDq1T4OcXDsgb6hyBSaJgeedYQwQwGhlcX-dZLSF70FjunbM15RLBTgJk3IrodQswRdAM_26LPuhmB4M-ws_MQE4UJs0SAB2qtD755nqywNpp8Si9MBghBdT_dCxzvYrd4sml8IgvIY2OL0tul0_FlLUpiL_6M6-mrIyurLIqDHaFVTN6X8edP6SRuHWUQx5YPNnZJDocL6xbwJwA"
                        />
                      </div>
                      <div>
                        <div
                          class="font-semibold text-gray-900 dark:text-white"
                        >
                          Charlie Brown
                        </div>
                        <div
                          class="text-xs text-text-muted-light dark:text-text-muted-dark"
                        >
                          ID: 2023003
                        </div>
                      </div>
                    </div>
                  </td>
                  <td class="p-4 text-center">
                    <div class="relative w-20 mx-auto">
                      <div
                        class="w-16 h-10 mx-auto border border-gray-200 dark:border-slate-600 rounded-lg flex items-center justify-center font-semibold text-gray-900 dark:text-white bg-white dark:bg-slate-900"
                      >
                        75
                      </div>
                    </div>
                  </td>
                  <td class="p-4 text-center">
                    <span
                      class="inline-flex items-center gap-1.5 px-2.5 py-1 rounded-full text-xs font-medium bg-sky-100 dark:bg-sky-700/40 text-sky-700 dark:text-sky-200"
                    >
                      <span class="w-1.5 h-1.5 rounded-full bg-sky-500"></span>
                      Read
                    </span>
                  </td>
                  <td class="p-4 text-center">
                    <button
                      class="p-2 rounded-full hover:bg-red-50 text-gray-400 hover:text-red-500 dark:hover:bg-red-900/20 dark:hover:text-red-400 transition-colors"
                      title="Delete record"
                    >
                      <span class="material-symbols-outlined text-[20px]"
                        >delete</span
                      >
                    </button>
                  </td>
                </tr>
                <tr
                  class="group hover:bg-gray-50 dark:hover:bg-slate-800/50 transition-colors"
                >
                  <td class="p-4 pl-6">
                    <div class="flex items-center gap-3">
                      <div
                        class="w-10 h-10 rounded-full bg-pink-100 dark:bg-pink-900 text-pink-600 dark:text-pink-300 flex items-center justify-center font-bold text-sm flex-shrink-0"
                      >
                        DW
                      </div>
                      <div>
                        <div
                          class="font-semibold text-gray-900 dark:text-white"
                        >
                          Daisy Wong
                        </div>
                        <div
                          class="text-xs text-text-muted-light dark:text-text-muted-dark"
                        >
                          ID: 2023004
                        </div>
                      </div>
                    </div>
                  </td>
                  <td class="p-4 text-center">
                    <div
                      class="w-16 h-10 mx-auto border border-gray-200 dark:border-slate-600 rounded-lg flex items-center justify-center font-semibold text-gray-900 dark:text-white bg-white dark:bg-slate-900"
                    >
                      78
                    </div>
                  </td>
                  <td class="p-4 text-center">
                    <span
                      class="inline-flex items-center gap-1.5 px-2.5 py-1 rounded-full text-xs font-medium bg-sky-100 dark:bg-sky-700/40 text-sky-700 dark:text-sky-200"
                    >
                      <span class="w-1.5 h-1.5 rounded-full bg-sky-500"></span>
                      Read
                    </span>
                  </td>
                  <td class="p-4 text-center">
                    <button
                      class="p-2 rounded-full hover:bg-red-50 text-gray-400 hover:text-red-500 dark:hover:bg-red-900/20 dark:hover:text-red-400 transition-colors"
                      title="Delete record"
                    >
                      <span class="material-symbols-outlined text-[20px]"
                        >delete</span
                      >
                    </button>
                  </td>
                </tr>
                <tr
                  class="group hover:bg-gray-50 dark:hover:bg-slate-800/50 transition-colors"
                >
                  <td class="p-4 pl-6">
                    <div class="flex items-center gap-3">
                      <div
                        class="w-10 h-10 rounded-full overflow-hidden flex-shrink-0"
                      >
                        <img
                          alt="Evan Lee"
                          class="w-full h-full object-cover"
                          src="https://lh3.googleusercontent.com/aida-public/AB6AXuAOq5HIJrHhf31413-hbBg16dhLQOUngJZZhzPEXKub1u8NDLyzOpPeGQMUmYSlXk-4lPjAgrF1HhfEkYSXW8VvyL1ZjQJdBJmuSTAP27pFTTwzSD2a1M0CDqZUC54Mu8M9Y4OqxWhphFcgjoWwhUyBlnXYhEBnL0P4oNp84OIEzpB4e9sEDWos5bPJSrzNrpw__Jb3KaGwHYT1AQau6R2sbUKS0RxojV6vxXSOt-IA_xIOf9iLdzWyxWxcQMGNCE2_QIEavwcWRA"
                        />
                      </div>
                      <div>
                        <div
                          class="font-semibold text-gray-900 dark:text-white"
                        >
                          Evan Lee
                        </div>
                        <div
                          class="text-xs text-text-muted-light dark:text-text-muted-dark"
                        >
                          ID: 2023005
                        </div>
                      </div>
                    </div>
                  </td>
                  <td class="p-4 text-center">
                    <div class="relative w-20 mx-auto">
                      <div
                        class="w-16 h-10 mx-auto border border-gray-200 dark:border-slate-600 rounded-lg flex items-center justify-center font-semibold text-gray-900 dark:text-white bg-white dark:bg-slate-900"
                      >
                        74
                      </div>
                    </div>
                  </td>
                  <td class="p-4 text-center">
                    <span
                      class="inline-flex items-center gap-1.5 px-2.5 py-1 rounded-full text-xs font-medium bg-amber-100 dark:bg-yellow-900/50 text-amber-700 dark:text-yellow-300"
                    >
                      <span
                        class="w-1.5 h-1.5 rounded-full bg-amber-500"
                      ></span>
                      Unread
                    </span>
                  </td>
                  <td class="p-4 text-center">
                    <button
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
const sortKey = ref("");
const sortOption = ref("id_lowhigh");
const sortOpen = ref(false);

const quizID = computed(() => Number(route.params.quiz_id));

const randomAvatar = ref("");
const userProfile = ref(null);

const BASE_URL = "http://localhost:56733";

const toggleDropdown = () => {
  isOpen.value = !isOpen.value;
};

const handleClickOutside = (event) => {
  if (dropdownRef.value && !dropdownRef.value.contains(event.target)) {
    isOpen.value = false;
  }
};

const fetchStudentScore = async () => {
  try {
    const response = await fetch(`${BASE_URL}/stu_score/${quizID}`, {
      method: "GET",
      credentials: "include",
    });
    if (!response.ok) {
      const text = await response.text().catch(() => "");
      console.error("Fetch student score failed:", response.status, text);
      throw new Error("Fetch failed");
    }

    const data = await response.json();
    const scoreList = Array.isArray(data?.score) ? data.score : [];

    students.value = scoreList.map((s) => ({
      student_id: s.stu_id,
      student_name: [s.stu_fname, s.stu_mname, s.stu_lname]
        .filter(Boolean)
        .join(" "),
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

const handleFileUpload = async (event) => {
  const file = event.target.files[0];
  if (!file) {
    return;
  }
  const formdata = new FormData();
  formdata.append("file", file);

  try {
    const token = localStorage.getItem("csrf_token");
    const response = await fetch(`http://localhost:56733/upload/${quizID}`, {
      method: "POST",
      headers: {
        Authorization: `Bearer ${token}`,
      },
      body: formdata,
    });
    if (!response.ok) {
      const errorData = await response.json();
      alert(errorData.detail || "Upload failed");
    }
    alert("CSV uploaded successfully");
    fetchStudentScore();
  } catch (err) {
    console.error(err);
  }
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

const sortPeople = () => {
  switch (sortOption.value) {
    case "id_lowhigh":
      students.value.sort(
        (a, b) => Number(a.student_id) - Number(b.student_id),
      );
      break;

    case "name_atoz":
      students.value.sort((a, b) =>
        a.student_name.localeCompare(b.student_name),
      );
      break;

    case "section_lowhigh":
      students.value.sort((a, b) => a.section.localeCompare(b.section));
      break;
  }
};

onMounted(() => {
  document.addEventListener("click", handleClickOutside);
  const seed = Math.random().toString(36).substring(7);
  randomAvatar.value = `https://robohash.org/${seed}.png`;
  fetchUserProfile();
  fetchStudentScore();
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
