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
            class="animate-card delay-1 text-sm text-text-muted-light dark:text-text-muted-dark"
          >
            <button
              class="group inline-flex items-center gap-3 font-bold text-[#111811] dark:text-white hover:text-primary transition-colors"
              type="button"
              @click="router.back()"
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
            <div class="animate-card delay-1 flex flex-wrap items-center gap-2 mt-4">
              <button
                class="hover:text-primary font-medium"
                type="button"
                @click="router.go(-2)"
              >
                Course Management
              </button>
              <span class="font-medium"> / </span>
              <button
                class="hover:text-primary font-medium"
                type="button"
                @click="router.go(-1)"
              >
                {{ course?.course_name }}
              </button>
              <span class="font-medium"> / </span>
              <span class="text-[#111811] dark:text-white font-medium">
                {{ quiz_name }}
              </span>
            </div>
          </nav>
          <div
            class="animate-card delay-1 flex flex-col md:flex-row md:items-center justify-between gap-4"
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
                class="text-sm text-gray-500 dark:text-gray-400 mt-1"
              >
                Rank {{ scoreData?.ranking ?? "-" }} / {{ scoreData?.total_students ?? "-" }}
              </span>
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
          <div class="animate-card delay-3 mb-8">
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
            <div class="grid grid-cols-2 md:grid-cols-6 gap-4">
              <div
                class="animate-card delay-1 bg-card-light dark:bg-card-dark p-5 rounded-xl border border-border-light dark:border-blue-700 shadow-sm text-center transition-transform hover:scale-105 duration-200"
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
                class="animate-card delay-1 bg-card-light dark:bg-card-dark p-5 rounded-xl border border-border-light dark:border-blue-700 shadow-sm text-center transition-transform hover:scale-105 duration-200"
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
                class="animate-card delay-1 bg-card-light dark:bg-card-dark p-5 rounded-xl border border-border-light dark:border-blue-700 shadow-sm text-center transition-transform hover:scale-105 duration-200"
              >
                <div
                  class="text-xs font-semibold text-text-muted-light dark:text-text-muted-dark uppercase tracking-wide mb-1"
                >
                  S.D.
                </div>
                <div class="text-2xl font-bold text-gray-900 dark:text-white">
                  {{ scoreData?.std ?? "-" }}
                </div>
              </div>
              <div
                class="animate-card delay-1 bg-card-light dark:bg-card-dark p-5 rounded-xl border border-border-light dark:border-blue-700 shadow-sm text-center transition-transform hover:scale-105 duration-200"
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
                class="animate-card delay-1 bg-card-light dark:bg-card-dark p-5 rounded-xl border border-border-light dark:border-blue-700 shadow-sm text-center transition-transform hover:scale-105 duration-200"
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
              <div
                class="animate-card delay-1 bg-card-light dark:bg-card-dark p-5 rounded-xl border border-border-light dark:border-blue-700 shadow-sm text-center transition-transform hover:scale-105 duration-200"
              >
                <div
                  class="text-xs font-semibold text-text-muted-light dark:text-text-muted-dark uppercase tracking-wide mb-1"
                >
                  Rank
                </div>
  <div class="text-2xl font-bold text-gray-900 dark:text-white">
    {{ scoreData?.ranking ?? "-" }}
  </div>
</div>
            </div>
          </div>
          <div
            class="animate-card delay-4 bg-card-light dark:bg-card-dark rounded-xl shadow-sm border border-border-light dark:border-blue-700 p-8"
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
                0 (Min)
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

const quizId = computed(() => String(route.params.quiz_id));

const userProfile = ref(null);
const scoreData = ref(null);
const animatedPercent = ref(0)
const animatedScore = ref(0)
const loading = ref(false);
const errorMessage = ref("");

const quiz_name = computed(() => {
  const q = route.query.quiz_name;
  if (q && typeof q === "string" && q.trim()) return q;
  return `Quiz ${quizId.value}`;
});

const course = computed(() => {
  const name = route.query.course_name
  if (name && typeof name === "string") {
    return { course_name: name }
  }
  return null
})

const isOpen = ref(false);

const dropdownRef = ref(null);

const BASE_URL = "http://localhost:56733";

const connectGoogle = () => {
  window.location.href = `${BASE_URL}/login_with_google`;
};

const CIRCLE_CIRCUMFERENCE = 251.2;

const clamp = (n, min, max) => Math.min(max, Math.max(min, n));

const animatePercent = (percentTarget, scoreTarget) => {
  animatedPercent.value = 0
  animatedScore.value = 0

  const percentInterval = setInterval(() => {
    if (animatedPercent.value >= percentTarget) {
      clearInterval(percentInterval)
    } else {
      animatedPercent.value += 1
    }
  }, 15)

  const scoreInterval = setInterval(() => {
    if (animatedScore.value >= scoreTarget) {
      clearInterval(scoreInterval)
    } else {
      animatedScore.value += 1
    }
  }, 25)
}

const percentValue = computed(() => {
  const p = Number(scoreData.value?.percent);
  return Number.isFinite(p) ? clamp(p, 0, 100) : 0;
});

const progressDashoffset = computed(() => {
  return CIRCLE_CIRCUMFERENCE * (1 - animatedPercent.value / 100);
});

const scoreText = computed(() => {
  const my = scoreData.value?.my_score;
  const full = scoreData.value?.full_mark;
  if (my === null || my === undefined || full === null || full === undefined) {
    return "-/-";
  }
  return `${animatedScore.value}/${full}`;
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
        errorMessage.value = "Score not found for this assignment.";
        return;
      }
      errorMessage.value = `Score not found for this assignment.`;
      return;
    }

    const data = await response.json();
    scoreData.value = data;
    animatePercent(
      data.percent ?? 0,
      data.my_score ?? 0
    )
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
  if (quizId.value && String(quizId.value).trim() !== "") {
    fetchStudentScore(quizId.value);
  } else {
    errorMessage.value = "Invalid quiz id.";
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

const animateScore = (target) => {
  const duration = 1200;
  const start = performance.now();

  const step = (timestamp) => {
    const progress = Math.min((timestamp - start) / duration, 1);
    animatedPercent.value = target * progress;

    if (progress < 1) {
      requestAnimationFrame(step);
    }
  };

  requestAnimationFrame(step);
};

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


@keyframes cardEnter {
  0% {
    opacity: 0;
    transform: translateY(20px) scale(0.97);
  }
  100% {
    opacity: 1;
    transform: translateY(0) scale(1);
  }
}

.animate-card {
  animation: cardEnter 0.55s cubic-bezier(0.16, 1, 0.3, 1) forwards;
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
  animation-delay: 0.20s;
}
.delay-5 {
  animation-delay: 0.25s;
}
</style>