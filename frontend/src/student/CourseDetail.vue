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
                  >Giselle</span
                >
              </div>
              <div class="relative">
                <img
                  alt="User profile picture"
                  class="h-10 w-10 rounded-full object-cover border-2 border-primary"
                  src="https://lh3.googleusercontent.com/aida-public/AB6AXuAfs56wd3ZKem_c5viO2sbQi6QqagsAHOE_1vjyHa7ZI8VHLknmGt20_hlaSVETqWYOsJL90qkBypXOjJp3RLSZRVCCQdcfaZh5kBgmGKpB2H1ljdV46tJTVLrSN0GurDyMvTs3Rbs4iUT-JQEizgeI8EIRbyNIvgzgmld5oKsHWGOuXctpZU9YajqdkAw1xoCp7REQvLbXOz8A9iuN2iz7maCHA50bOTOwjKS5ivvz9hojTaRSN6jd9o2cDN90A2qviBCKcL1ugg"
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
                    src="https://lh3.googleusercontent.com/aida-public/AB6AXuAfs56wd3ZKem_c5viO2sbQi6QqagsAHOE_1vjyHa7ZI8VHLknmGt20_hlaSVETqWYOsJL90qkBypXOjJp3RLSZRVCCQdcfaZh5kBgmGKpB2H1ljdV46tJTVLrSN0GurDyMvTs3Rbs4iUT-JQEizgeI8EIRbyNIvgzgmld5oKsHWGOuXctpZU9YajqdkAw1xoCp7REQvLbXOz8A9iuN2iz7maCHA50bOTOwjKS5ivvz9hojTaRSN6jd9o2cDN90A2qviBCKcL1ugg"
                  />
                  <div>
                    <p
                      class="font-semibold text-gray-900 dark:text-white break-all"
                    >
                      Uchinaga Aeri
                    </p>
                    <p class="text-sm text-gray-500 break-all">
                      Student ID: 65012345
                    </p>
                    <p class="text-sm text-gray-500 break-all">
                      Email: Gigi_selle@cmu.ac.th
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
          <div class="flex flex-col gap-4">
            <a
              class="group flex w-fit items-center gap-3 text-sm font-bold text-[#111811] dark:text-white hover:text-primary transition-colors"
              href="#"
            >
              <div
                class="flex size-9 items-center justify-center rounded-full bg-surface-light dark:bg-surface-dark border border-border-light dark:border-border-dark shadow-sm group-hover:border-primary group-hover:text-primary transition-colors"
              >
                <span class="material-symbols-outlined text-[20px]"
                  >arrow_back</span
                >
              </div>
              <span>Return</span>
            </a>
            <div class="flex flex-wrap gap-2 text-sm">
              <a class="hover:text-primary font-medium" href="#"> Courses </a>
              <span class="font-medium"> / </span>
              <span class="text-[#111811] dark:text-white font-medium"
                >CS101 - Intro to Algorithms</span
              >
            </div>
          </div>
          <section class="@container">
            <div
              class="flex flex-col md:flex-row gap-6 bg-surface-light dark:bg-surface-dark rounded-xl shadow-sm border border-border-light dark:border-border-dark overflow-hidden"
            >
              <div class="flex-1 p-6 md:p-8 flex flex-col justify-center gap-4">
                <h1
                  class="text-[#111811] dark:text-white text-3xl md:text-4xl font-black leading-tight tracking-[-0.033em]"
                >
                  CS101: Intro to Algorithms
                </h1>
                <div
                  class="flex items-center gap-2 text-primary dark:text-primary mt-1"
                >
                  <span class="material-symbols-outlined text-[20px]"
                    >school</span
                  >
                  <p class="text-base font-normal">
                    Instructor: Katarina Bluu, PhD
                  </p>
                </div>
              </div>
            </div>
          </section>
          <section class="flex flex-col gap-4">
            <div class="flex items-center justify-between">
              <div class="flex items-center gap-2">
                <span class="material-symbols-outlined text-primary"
                  >assignment</span
                >
                <h3 class="text-lg font-bold text-[#111811] dark:text-white">
                  Assessments
                </h3>
              </div>
              <div class="text-sm dark:text-primary">
                Weighted Average:
                <span class="font-bold text-primary dark:text-primary"
                  >92.00</span
                >
              </div>
            </div>
            <div
              class="bg-surface-light dark:bg-surface-dark border border-border-light dark:border-border-dark rounded-xl overflow-hidden shadow-sm"
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
                      class="hover:bg-[#fcfdfc] dark:hover:bg-[#1f2832] transition-colors group"
                    >
                      <td class="p-4">
                        <div class="font-bold text-[#111811] dark:text-white">
                          Final Project
                        </div>
                      </td>
                      <td class="p-4 text-center font-medium">40%</td>
                    </tr>
                    <tr
                      class="hover:bg-[#fcfdfc] dark:hover:bg-[#1f2832] transition-colors group"
                    >
                      <td class="p-4">
                        <div class="font-bold text-[#111811] dark:text-white">
                          Midterm Exam
                        </div>
                      </td>
                      <td class="p-4 text-center font-medium">30%</td>
                    </tr>
                    <tr
                      class="hover:bg-[#fcfdfc] dark:hover:bg-[#1f2832] transition-colors group"
                    >
                      <td class="p-4">
                        <div class="font-bold text-[#111811] dark:text-white">
                          Assignment 1
                        </div>
                      </td>
                      <td class="p-4 text-center font-medium">10%</td>
                    </tr>
                    <tr
                      class="hover:bg-[#fcfdfc] dark:hover:bg-[#1f2832] transition-colors group"
                    >
                      <td class="p-4">
                        <div class="font-bold text-[#111811] dark:text-white">
                          Assignment 2
                        </div>
                      </td>
                      <td class="p-4 text-center font-medium">10%</td>
                    </tr>
                    <tr
                      class="hover:bg-[#fcfdfc] dark:hover:bg-[#1f2832] transition-colors group"
                    >
                      <td class="p-4">
                        <div class="font-bold text-[#111811] dark:text-white">
                          Quiz: Week 5
                        </div>
                      </td>
                      <td class="p-4 text-center font-medium">5%</td>
                    </tr>
                    <tr
                      class="hover:bg-[#fcfdfc] dark:hover:bg-[#1f2832] transition-colors group"
                    >
                      <td class="p-4">
                        <div class="font-bold text-[#111811] dark:text-white">
                          Participation
                        </div>
                      </td>
                      <td class="p-4 text-center font-medium">5%</td>
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
import { useRouter } from "vue-router";

const router = useRouter();

const isOpen = ref(false);

const dropdownRef = ref(null);

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
});

onBeforeUnmount(() => {
  document.removeEventListener("click", handleClickOutside);
});

const handleLogout = async () => {
  try {
    const response = await fetch(`${BASE_URL}/logout`, {
      method: "GET",
      credentials: "include",
    });

    if (response.ok) {
      localStorage.clear();
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
