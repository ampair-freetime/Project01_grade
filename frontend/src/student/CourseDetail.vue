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
              @click="router.go(-1)"
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
              class="btn-animate flex items-center space-x-3 hover:bg-gray-100 dark:hover:bg-gray-700 px-3 py-2 rounded-lg transition"
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
              class="btn-animate flex items-center justify-center size-10 rounded-full hover:bg-red-50 dark:hover:bg-red-900/20 text-[#637888] dark:text-[#a0b8cf] hover:text-red-600 dark:hover:text-red-400 transition-colors"
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
          </nav>

          <section class="@container">
            <div
              class="animate-card delay-1 flex flex-col md:flex-row gap-6 bg-surface-light dark:bg-surface-dark rounded-xl shadow-sm border border-border-light dark:border-border-dark overflow-hidden"
            >
              <div class="flex-1 p-6 md:p-8 flex flex-col justify-center gap-4">
                <h1
                  class="text-[#111811] dark:text-white text-3xl md:text-4xl font-black leading-tight tracking-[-0.033em]"
                >
                  {{ course?.course_name }}
                </h1>
                <div
                  class="flex items-center gap-2 text-primary dark:text-primary mt-1"
                >
                  <span class="material-symbols-outlined text-[20px]"
                    >school</span
                  >
                  <p class="text-base font-normal">
                    Instructor: {{ course?.teacher_name }}
                  </p>
                </div>
              </div>
            </div>
          </section>
          <section class="flex flex-col gap-4">
            <div class="animate-card delay-2 flex items-center justify-between">
              <div class="flex items-center gap-2">
                <span class="material-symbols-outlined text-primary">
                  assignment
                </span>

                <h3 class="text-lg font-bold text-[#111811] dark:text-white">
                  Assessments
                </h3>
              </div>

              <div class="text-sm dark:text-primary">
                Weighted Average:
                <span class="font-bold text-primary dark:text-primary">
                  {{ weightedAverage.toFixed(2) }}
                </span>
              </div>
            </div>
            <div
              class="animate-card delay-2 bg-surface-light dark:bg-surface-dark border border-border-light dark:border-border-dark rounded-xl overflow-hidden shadow-sm"
            >
              <div class="overflow-x-auto">
                <table class="w-full text-left border-collapse">
                  <thead>
                    <tr
                      class="bg-background-light dark:bg-[#1a232c] border-b border-border-light dark:border-border-dark"
                    >
                      <th
                        class="p-4 text-xs font-bold text-primary dark:text-primary uppercase tracking-wider"
                      >
                        Assessment
                      </th>
                      <th
                        class="p-4 text-xs font-bold text-primary dark:text-primary uppercase tracking-wider w-24 text-center"
                      >
                        Weight
                      </th>
                    </tr>
                  </thead>
                  <tbody
                    class="divide-y divide-border-light dark:divide-border-dark text-sm"
                  >
                    <tr
                      v-for="item in assessments"
                      :key="item.quiz_id"
                      class="hover:bg-[#fcfdfc] dark:hover:bg-[#1f2832] transition-all duration-200 hover:scale-[1.01] group cursor-pointer"
                      @click="
                        router.push({
                          path: `/student/score/${item.quiz_id}`,
                          query: {
                            quiz_name: item.quiz_name,
                            course_name: course?.course_name,
                          },
                        })
                      "
                    >
                      <td class="p-4">
                        <div class="font-bold text-[#111811] dark:text-white">
                          {{ item.quiz_name }}
                        </div>

                        <!-- คะแนน -->
                        <div
                          v-if="item.my_score !== null"
                          class="text-xs text-gray-500 mt-1"
                        >
                          Score: {{ item.my_score }} / {{ item.full_mark }} ({{
                            item.percent
                          }}%)
                        </div>
                      </td>

                      <td class="p-4 text-center font-medium">
                        {{ item.weight }}%
                      </td>
                    </tr>
                  </tbody>
                </table>
              </div>
            </div>
          </section>
        </div>
      </div>
    </main>
  </div>
</template>

<script setup>
name: "CourseDetail";
import { ref, onMounted, onBeforeUnmount } from "vue";
import { useRouter, useRoute } from "vue-router";

const router = useRouter();
const route = useRoute();
const userProfile = ref(null);
const course = ref(null);
const assessments = ref([]);
const weightedAverage = ref(0);

const courseId = route.params.course_id;

const isOpen = ref(false);

const dropdownRef = ref(null);

const BASE_URL = "http://localhost:56733";

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

const toggleDropdown = () => {
  isOpen.value = !isOpen.value;
};

const fetchCourseDetail = async (courseId) => {
  try {
    const response = await fetch(`${BASE_URL}/student/course/${courseId}`, {
      method: "GET",
      credentials: "include",
    });

    if (!response.ok) {
      if (response.status === 403) {
        alert("You are not enrolled in this course");
        router.push("/student/dashboard");
      }
      return;
    }

    const data = await response.json();
    //  backend: {
    //     "course_id": course.course_id,
    //     "course_name": course.course_name,
    //     "weighted_average": weighted_average,
    //     "assessments": assessment
    // }

    course.value = data;
    assessments.value = data.assessments;
    weightedAverage.value = data.weighted_average;
  } catch (error) {
    console.error("Fetch course detail error:", error);
  }
};

const handleClickOutside = (event) => {
  if (dropdownRef.value && !dropdownRef.value.contains(event.target)) {
    isOpen.value = false;
  }
};

onMounted(() => {
  document.addEventListener("click", handleClickOutside);
  fetchCourseDetail(courseId);
  fetchUserProfile();
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

<style scoped>
.fade-enter-active,
.fade-leave-active {
  transition: opacity 0.25s ease;
}

.fade-enter-from,
.fade-leave-to {
  opacity: 0;
}

.btn-animate {
  transition:
    transform 0.25s cubic-bezier(0.16, 1, 0.3, 1),
    box-shadow 0.25s cubic-bezier(0.16, 1, 0.3, 1),
    background-color 0.2s ease,
    color 0.2s ease;
  transform: translate3d(0, 0, 0);
  will-change: transform;
}

.btn-animate:hover {
  transform: translateY(-2px) scale(1.02);
  box-shadow: 0 8px 24px rgba(0, 0, 0, 0.15);
}

.btn-animate:active {
  transform: translateY(1px) scale(0.97);
  box-shadow: 0 3px 10px rgba(0, 0, 0, 0.12);
}

@keyframes cardEnter {
  0% {
    opacity: 0;
    transform: translateY(24px) scale(0.97);
  }
  100% {
    opacity: 1;
    transform: translateY(0) scale(1);
  }
}

.animate-card {
  animation: cardEnter 0.55s cubic-bezier(0.16, 1, 0.3, 1);
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

.link-animate {
  position: relative;
  transition:
    color 0.25s ease,
    transform 0.2s cubic-bezier(0.16, 1, 0.3, 1);
}

.link-animate:hover {
  transform: translateY(-1px);
}

.link-animate::after {
  content: "";
  position: absolute;
  left: 0;
  bottom: -3px;
  width: 0%;
  height: 2px;
  background: currentColor;
  transition: width 0.3s cubic-bezier(0.16, 1, 0.3, 1);
}

.link-animate:hover::after {
  width: 100%;
}
</style>
