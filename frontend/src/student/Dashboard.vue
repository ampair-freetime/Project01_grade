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
                  v-if="userProfile?.avatar_url"
                  alt="User profile picture"
                  class="h-10 w-10 rounded-full object-cover border-2 border-primary"
                  :src="userProfile.avatar_url"
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
                    v-if="userProfile?.avatar_url"
                    class="h-12 w-12 rounded-full object-cover":src="userProfile.avatar_url"/>
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
          <header
            class="animate-card flex flex-col md:flex-row md:items-end justify-between gap-6"
          >
            <div class="flex flex-col gap-2">
              <h2
                class="text-[#111811] dark:text-white text-3xl md:text-4xl font-bold tracking-tight"
              >
                Hello, {{ userProfile?.first_name }}
              </h2>
            </div>
            <div class="w-full md:w-96">
              <label
                class="flex w-full items-center h-12 rounded-lg bg-white dark:bg-[#1a232e] shadow-sm ring-1 ring-[#e0e7eb] dark:ring-[#2a363e] focus-within:ring-2 focus-within:ring-primary overflow-hidden transition-shadow"
              >
                <div
                  class="flex items-center justify-center pl-4 pr-2 text-[#637888] dark:text-[#a0b8cf]"
                >
                  <span class="material-symbols-outlined">search</span>
                </div>
                <input
                  v-model="searchTerm"
                  id="search"
                  name="search"
                  class="w-full bg-transparent border-none text-[#111811] dark:text-white placeholder:text-[#637888]/70 focus:ring-0 focus:outline-none text-base h-full"
                  placeholder="Search courses..."
                  type="text"
                />
              </label>
            </div>
          </header>
          <section class="animate-card delay-1 flex flex-col gap-4">
            <div class="flex items-center justify-between mb-2">
              <h3
                class="text-l text-primary dark:text-white flex items-center gap-2"
              >
                Current Enrolled Courses
              </h3>
            </div>
            <!-- Add courses -->
            <ul class="divide-y divide-border-light dark:divide-border-dark">
              <li
                v-for="(course, index) in filteredCourses"
                :key="course.course_code"
                class="hover:bg-gray-50 dark:hover:bg-gray-800/50 transition-colors duration-150"
              >
                <div
                  :class="[
                    'group bg-white dark:bg-[#1a232e] p-4 rounded-xl shadow-sm border border-transparent hover:border-primary/40 hover:shadow-md transition-all duration-200 cursor-pointer animate-card',
                    `delay-${(index % 5) + 1}`,
                  ]"
                  @click="goToAssignment(course.course_code)"
                >
                  <div class="flex items-center justify-between gap-4">
                    <div class="flex items-center gap-5 overflow-hidden">
                      <div class="flex flex-col min-w-0">
                        <!-- <div class="flex items-center gap-2 mb-0.5">
                          <span
                            class="font-mono text-xs font-bold text-[#637888] dark:text-[#a0b8cf] bg-[#f0f4f8] dark:bg-[#253038] px-1.5 py-0.5 rounded"
                            >{{ course.course_code }}</span
                          >
                        </div> -->
                        <h4
                          class="text-[#111811] dark:text-white text-lg font-semibold truncate group-hover:text-primary transition-colors"
                        >
                          {{ course.course_name }}
                        </h4>
                      </div>
                    </div>
                    <div
                      class="shrink-0 flex items-center justify-center size-10 rounded-full bg-[#f6f8fa] dark:bg-[#253038] text-[#111811] dark:text-white group-hover:bg-primary group-hover:text-white transition-colors"
                    >
                      <span class="material-symbols-outlined"
                        >arrow_forward</span
                      >
                    </div>
                  </div>
                </div>
              </li>
            </ul>
            <!-- end add courses -->
          </section>
        </div>
      </div>
    </main>
  </div>
</template>

<script setup>
name: "Dashboard";
import { ref, onMounted, onBeforeUnmount, computed } from "vue";
import { useRouter } from "vue-router";

const router = useRouter();

const isOpen = ref(false);

const dropdownRef = ref(null);

const userProfile = ref(null);
const courses = ref([]);
const searchTerm = ref("");

const BASE_URL = "/api";
const toggleDropdown = () => {
  isOpen.value = !isOpen.value;
};

const handleClickOutside = (event) => {
  if (dropdownRef.value && !dropdownRef.value.contains(event.target)) {
    isOpen.value = false;
  }
};

onMounted(() => {
  document.addEventListener("click", handleClickOutside);

  fetchDashboard();
  fetchUserProfile();

  const params = new URLSearchParams(window.location.search);

  if (params.get("google") === "connect_success") {
    if (!sessionStorage.getItem("google_alert_shown")) {
      alert("🎉 Google connected successfully!");
      sessionStorage.setItem("google_alert_shown", "true");
    }

    window.history.replaceState({}, document.title, window.location.pathname);
  }
});

onBeforeUnmount(() => {
  document.removeEventListener("click", handleClickOutside);
});
//########################################################################### fetch #################################
const fetchDashboard = async () => {
  try {
    const response = await fetch(`${BASE_URL}/student/dashboard_student`, {
      credentials: "include",
    });

    if (!response.ok) {
      router.push("/login");
      return;
    }

    const data = await response.json();
    courses.value = data.courses;
  } catch (error) {
    console.error("Fetch dashboard error:", error);
  }
};

const fetchUserProfile = async () => {
  try {
    const response = await fetch(`${BASE_URL}/me`, {
      credentials: "include",
      cache: "no-store"       
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

const connectGoogle = () => {
  window.location.href = "http://localhost:56733/login_with_google";
};

// ################################################################# course ########################################
const filteredCourses = computed(() => {
  if (!searchTerm.value) return courses.value;

  return courses.value.filter(
    (c) =>
      c.course_name.toLowerCase().includes(searchTerm.value.toLowerCase()) ||
      String(c.course_code).includes(searchTerm.value),
  );
});

const goToAssignment = (course_code) => {
  router.push(`/student/course/${course_code}`);
};
</script>

<style scoped>
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
    transform: translateY(20px) scale(0.97) ;
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
  animation-delay: 0.30s;
}
.delay-5 {
  animation-delay: 0.25s;
}
</style>
