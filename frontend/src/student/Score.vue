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
                  >{{ userProfile?.first_name }}</span
                >
              </div>
              <div class="relative">
                <img
                  alt="User profile picture"
                  class="h-10 w-10 rounded-full object-cover border-2 border-primary"
                  :src="
                    userProfile?.avatar_url ||
                    'https://lh3.googleusercontent.com/aida-public/AB6AXuAfs56wd3ZKem_c5viO2sbQi6QqagsAHOE_1vjyHa7ZI8VHLknmGt20_hlaSVETqWYOsJL90qkBypXOjJp3RLSZRVCCQdcfaZh5kBgmGKpB2H1ljdV46tJTVLrSN0GurDyMvTs3Rbs4iUT-JQEizgeI8EIRbyNIvgzgmld5oKsHWGOuXctpZU9YajqdkAw1xoCp7REQvLbXOz8A9iuN2iz7maCHA50bOTOwjKS5ivvz9hojTaRSN6jd9o2cDN90A2qviBCKcL1ugg'
                  "
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
                      Student ID: {{ userProfile?.student_id }}
                    </p>
                    <p class="text-sm text-gray-500 break-all">
                      Email: {{ userProfile?.email }}
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
              <span class="material-symbols-outlined text-[20px]">logout</span>
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
            class="text-sm text-text-muted-light dark:text-text-muted-dark"
          >
            <button
              class="group inline-flex items-center gap-3 font-bold text-[#111811] dark:text-white hover:text-primary transition-colors"
              type="button"
              @click="router.push(`/student/dashboard`)"
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
            <div
              v-if="course_name || quiz_name"
              class="flex flex-wrap gap-2 mt-4"
            >
              <a
                class="hover:text-primary font-medium"
                href="#"
                @click.prevent="router.push('/student/dashboard')"
                >Courses</a
              >
              <template v-if="course_name">
                <span class="font-medium">/</span>
                <span class="text-[#111811] dark:text-white font-medium">{{
                  course_name
                }}</span>
              </template>
              <span class="font-medium">/</span>
              <span class="text-[#111811] dark:text-white font-medium">{{
                quiz_name
              }}</span>
            </div>
          </nav>
          <div
            class="flex flex-col md:flex-row md:items-center justify-between gap-4"
          >
            <div class="flex items-center gap-4">
              <h1 class="text-4xl font-bold text-gray-900 dark:text-white">
                {{ quiz_name }}
              </h1>
            </div>
          </div>
          <div
            v-if="loading"
            class="bg-card-light dark:bg-card-dark rounded-xl shadow-sm border border-border-light dark:border-blue-700 p-8 md:p-12 mb-8 text-center"
          >
            Loading...
          </div>
          <div
            v-else-if="errorMessage"
            class="bg-card-light dark:bg-card-dark rounded-xl shadow-sm border border-border-light dark:border-blue-700 p-8 md:p-12 mb-8 text-center text-red-600 dark:text-red-400"
          >
            {{ errorMessage }}
          </div>
          <div
            v-else
            class="bg-card-light dark:bg-card-dark rounded-xl shadow-sm border border-border-light dark:border-blue-700 p-8 md:p-12 mb-8 flex flex-col items-center justify-center text-center"
          >
            <div class="relative w-64 h-64 mb-6">
              <svg
                class="w-full h-full transform -rotate-90"
                viewBox="0 0 100 100"
              >
                <circle
                  class="text-gray-100 dark:text-blue-900"
                  cx="50"
                  cy="50"
                  fill="transparent"
                  r="40"
                  stroke="currentColor"
                  stroke-width="8"
                ></circle>
                <circle
                  class="text-primary"
                  cx="50"
                  cy="50"
                  fill="transparent"
                  r="40"
                  stroke="currentColor"
                  :stroke-dasharray="CIRCLE_CIRCUMFERENCE"
                  :stroke-dashoffset="progressDashoffset"
                  stroke-linecap="round"
                  stroke-width="8"
                ></circle>
              </svg>
              <div
                class="absolute inset-0 flex flex-col items-center justify-center"
              >
                <span
                  class="text-5xl font-bold text-gray-900 dark:text-white tracking-tight"
                  >{{ scoreText }}</span
                >
                <span
                  class="text-lg text-text-muted-light dark:text-text-muted-dark mt-1 font-medium"
                  >{{ percentText }}</span
                >
              </div>
            </div>
          </div>
          <div class="mb-8">
            <div class="flex items-center gap-2 mb-4">
              <span class="material-symbols-outlined text-primary"
                >analytics</span
              >
              <h3
                class="text-sm font-bold uppercase tracking-wider text-text-muted-light dark:text-text-muted-dark"
              >
                Class Performance Statistics
              </h3>
              <div
                class="ml-auto text-xs text-text-muted-light dark:text-text-muted-dark"
              >
                Total Participants:
                {{ scoreData?.total_students ?? 0 }} Students
              </div>
            </div>
            <div class="grid grid-cols-2 md:grid-cols-5 gap-4">
              <div
                class="bg-card-light dark:bg-card-dark p-5 rounded-xl border border-border-light dark:border-blue-700 shadow-sm text-center transition-transform hover:scale-105 duration-200"
              >
                <div
                  class="text-xs font-semibold text-text-muted-light dark:text-text-muted-dark uppercase tracking-wide mb-1"
                >
                  Mean
                </div>
                <div class="text-2xl font-bold text-gray-900 dark:text-white">
                  {{ scoreData?.mean ?? "-" }}
                </div>
              </div>
              <div
                class="bg-card-light dark:bg-card-dark p-5 rounded-xl border border-border-light dark:border-blue-700 shadow-sm text-center transition-transform hover:scale-105 duration-200"
              >
                <div
                  class="text-xs font-semibold text-text-muted-light dark:text-text-muted-dark uppercase tracking-wide mb-1"
                >
                  Median
                </div>
                <div class="text-2xl font-bold text-gray-900 dark:text-white">
                  {{ scoreData?.median ?? "-" }}
                </div>
              </div>
              <div
                class="bg-card-light dark:bg-card-dark p-5 rounded-xl border border-border-light dark:border-blue-700 shadow-sm text-center transition-transform hover:scale-105 duration-200 col-span-2 md:col-span-1"
              >
                <div
                  class="text-xs font-semibold text-text-muted-light dark:text-text-muted-dark uppercase tracking-wide mb-1"
                >
                  Std Dev
                </div>
                <div class="text-2xl font-bold text-gray-900 dark:text-white">
                  {{ scoreData?.std ?? "-" }}
                </div>
              </div>
              <div
                class="bg-card-light dark:bg-card-dark p-5 rounded-xl border border-border-light dark:border-blue-700 shadow-sm text-center transition-transform hover:scale-105 duration-200"
              >
                <div
                  class="text-xs font-semibold text-text-muted-light dark:text-text-muted-dark uppercase tracking-wide mb-1"
                >
                  Highest
                </div>
                <div
                  class="text-2xl font-bold text-blue-600 dark:text-blue-400"
                >
                  {{ scoreData?.highest ?? "-" }}
                </div>
              </div>
              <div
                class="bg-card-light dark:bg-card-dark p-5 rounded-xl border border-border-light dark:border-blue-700 shadow-sm text-center transition-transform hover:scale-105 duration-200"
              >
                <div
                  class="text-xs font-semibold text-text-muted-light dark:text-text-muted-dark uppercase tracking-wide mb-1"
                >
                  Lowest
                </div>
                <div class="text-2xl font-bold text-gray-900 dark:text-white">
                  {{ scoreData?.lowest ?? "-" }}
                </div>
              </div>
            </div>
          </div>
          <div
            class="bg-card-light dark:bg-card-dark rounded-xl shadow-sm border border-border-light dark:border-blue-700 p-8"
          >
            <h3
              class="text-sm font-bold uppercase tracking-wider text-text-muted-light dark:text-text-muted-dark mb-10"
            >
              Score Distribution
            </h3>
            <div class="relative w-full h-16">
              <div
                class="absolute left-0 -top-6 text-xs font-medium text-text-muted-light dark:text-text-muted-dark"
              >
                {{ scoreData?.lowest ?? 0 }} (Min)
              </div>
              <div
                class="absolute right-0 -top-6 text-xs font-medium text-text-muted-light dark:text-text-muted-dark"
              >
                {{ scoreData?.full_mark ?? 0 }} (Full Mark)
              </div>
              <div
                class="absolute -top-8 text-[10px] font-semibold text-text-muted-light dark:text-text-muted-dark transform -translate-x-1/2"
                :style="{ left: `${meanLeft}%` }"
              >
                Mean: {{ scoreData?.mean ?? 0 }}
              </div>
              <div
                class="absolute top-9 text-[10px] font-semibold text-text-muted-light dark:text-text-muted-dark transform -translate-x-1/2"
                :style="{ left: `${highestLeft}%` }"
              >
                High: {{ scoreData?.highest ?? 0 }}
              </div>
              <div
                class="absolute top-9 text-[10px] font-semibold text-text-muted-light dark:text-text-muted-dark transform -translate-x-1/2"
                :style="{ left: `${lowestLeft}%` }"
              >
                Low: {{ scoreData?.lowest ?? 0 }}
              </div>
              <div
                class="absolute top-0 w-full h-3 bg-gray-100 dark:bg-blue-900/50 rounded-full mt-2"
              ></div>
              <div
                class="absolute top-0 w-0.5 h-7 bg-gray-400 dark:bg-blue-500 transform -translate-x-1/2"
                :style="{ left: `${meanLeft}%` }"
              ></div>
              <div
                class="absolute top-0 w-0.5 h-7 bg-gray-400 dark:bg-blue-500 transform -translate-x-1/2"
                :style="{ left: `${highestLeft}%` }"
              ></div>
              <div
                class="absolute top-0 w-0.5 h-7 bg-gray-400 dark:bg-blue-500 transform -translate-x-1/2"
                :style="{ left: `${lowestLeft}%` }"
              ></div>
              <div
                class="absolute -top-7 transform -translate-x-1/2 flex flex-col items-center group cursor-pointer"
                :style="{ left: `${myLeft}%` }"
              >
                <div
                  class="bg-primary text-white text-xs font-bold px-2 py-1 rounded mb-0.5 shadow-md whitespace-nowrap"
                >
                  YOU: {{ scoreData?.my_score ?? 0 }}
                </div>
                <div class="w-1 h-8 bg-primary rounded-full"></div>
              </div>
            </div>
          </div>
        </div>
      </div>
    </main>
  </div>
</template>

<script setup>
name: "Score";
import { ref, onMounted, onBeforeUnmount, computed } from "vue";
import { useRouter, useRoute } from "vue-router";

const router = useRouter();
const route = useRoute();

const quizId = computed(() => Number(route.params.quiz_id));

const userProfile = ref(null);
const scoreData = ref(null);
const loading = ref(false);
const errorMessage = ref("");

const quiz_name = computed(() => {
  const q = route.query.quiz_name;
  if (q && typeof q === "string" && q.trim()) return q;
  return `Quiz ${quizId.value}`;
});
const course_name = computed(() => route.query.course_name || "");

const isOpen = ref(false);

const dropdownRef = ref(null);

const BASE_URL = "http://localhost:56733";

const CIRCLE_CIRCUMFERENCE = 251.2;

const clamp = (n, min, max) => Math.min(max, Math.max(min, n));

const percentValue = computed(() => {
  const p = Number(scoreData.value?.percent);
  return Number.isFinite(p) ? clamp(p, 0, 100) : 0;
});

const progressDashoffset = computed(() => {
  return CIRCLE_CIRCUMFERENCE * (1 - percentValue.value / 100);
});

const scoreText = computed(() => {
  const my = scoreData.value?.my_score;
  const full = scoreData.value?.full_mark;
  if (my === null || my === undefined || full === null || full === undefined) {
    return "-/-";
  }
  return `${my}/${full}`;
});

const percentText = computed(() => `${percentValue.value.toFixed(2)}%`);

const toLeftPercent = (value) => {
  const full = Number(scoreData.value?.full_mark);
  const v = Number(value);
  if (!Number.isFinite(full) || full <= 0 || !Number.isFinite(v)) return 0;
  return clamp((v / full) * 100, 0, 100);
};

const meanLeft = computed(() => toLeftPercent(scoreData.value?.mean));
const highestLeft = computed(() => toLeftPercent(scoreData.value?.highest));
const lowestLeft = computed(() => toLeftPercent(scoreData.value?.lowest));
const myLeft = computed(() => toLeftPercent(scoreData.value?.my_score));

const toggleDropdown = () => {
  isOpen.value = !isOpen.value;
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

const fetchStudentScore = async (quiz_id) => {
  try {
    loading.value = true;
    errorMessage.value = "";
    const response = await fetch(`${BASE_URL}/student/score/${quiz_id}`, {
      method: "GET",
      credentials: "include",
    });
    if (!response.ok) {
      if (response.status === 401) {
        router.push("/login");
        return;
      }
      if (response.status === 403 || response.status === 404) {
        errorMessage.value = "Score not found for this quiz.";
        return;
      }
      errorMessage.value = `Failed to fetch score (HTTP ${response.status})`;
      return;
    }

    const data = await response.json();
    scoreData.value = data;
  } catch (err) {
    console.error(err);
    errorMessage.value = "Network error while fetching score.";
  } finally {
    loading.value = false;
  }
};

const handleClickOutside = (event) => {
  if (dropdownRef.value && !dropdownRef.value.contains(event.target)) {
    isOpen.value = false;
  }
};

onMounted(() => {
  document.addEventListener("click", handleClickOutside);
  fetchUserProfile();
  if (Number.isFinite(quizId.value) && quizId.value > 0) {
    fetchStudentScore(quizId.value);
  } else {
    errorMessage.value = "Invalid quiz id.";
  }
});

onBeforeUnmount(() => {
  document.removeEventListener("click", handleClickOutside);
});

const handleLogout = async () => {
  try {
    const response = await fetch("http://localhost:56733/logout", {
      method: "GET",
      credentials: "include",
    });

    if (response.ok) {
      localStorage.removeItem("csrf_token");
      localStorage.removeItem("role");
      router.push("/login");
    }
  } catch (error) {
    console.error("Logout failed", error);
  }
};
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