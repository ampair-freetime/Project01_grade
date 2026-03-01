<template>
  <div
    class="bg-background-light dark:bg-background-dark text-text-main-light dark:text-text-main-dark transition-colors duration-200 min-h-screen flex flex-col"
  >
    <header
      class="bg-white dark:bg-[#1a232e] border-b border-[#e0e7eb] dark:border-[#2a363e] h-16 shrink-0 sticky top-0 z-50"
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
              <span class="material-symbols-outlined text-white text-xl"
                >school</span
              >
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
              <div class="hidden md:flex flex-col items-end mr-2">
                <span
                  class="text-sm font-semibold text-gray-900 dark:text-white"
                  >John Doe</span
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
                class="absolute right-4 top-full mt-2 w-64 bg-white dark:bg-gray-800 rounded-xl shadow-lg p-4 z-50"
              >
                <div class="flex items-center space-x-3">
                  <img
                    class="h-12 w-12 rounded-full object-cover"
                    src="https://lh3.googleusercontent.com/aida-public/AB6AXuAfs56wd3ZKem_c5viO2sbQi6QqagsAHOE_1vjyHa7ZI8VHLknmGt20_hlaSVETqWYOsJL90qkBypXOjJp3RLSZRVCCQdcfaZh5kBgmGKpB2H1ljdV46tJTVLrSN0GurDyMvTs3Rbs4iUT-JQEizgeI8EIRbyNIvgzgmld5oKsHWGOuXctpZU9YajqdkAw1xoCp7REQvLbXOz8A9iuN2iz7maCHA50bOTOwjKS5ivvz9hojTaRSN6jd9o2cDN90A2qviBCKcL1ugg"
                  />
                  <div>
                    <p class="font-semibold text-gray-900 dark:text-white">
                      Johnathan Doe
                    </p>
                    <p class="text-sm text-gray-500">Student ID: 65012345</p>
                  </div>
                </div>
              </div>
            </transition>
            <a
              class="flex items-center justify-center size-10 rounded-full hover:bg-red-50 dark:hover:bg-red-900/20 text-[#637888] dark:text-[#a0b8cf] hover:text-red-600 dark:hover:text-red-400 transition-colors"
              href="#"
              title="Log Out"
            >
              <span class="material-symbols-outlined text-[20px]">logout</span>
            </a>
          </div>
        </div>
      </div>
    </header>
    <main class="flex-grow w-full max-w-5xl mx-auto px-4 sm:px-6 lg:px-8 py-8">
      <nav
        aria-label="Breadcrumb"
        class="flex mb-6 text-sm text-text-muted-light dark:text-text-muted-dark"
      >
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
            <span>Return to CS101 - Intro to Algorithms</span>
          </a>
          <div class="flex flex-wrap gap-2 text-sm">
            <a
              class="text-[#638863] hover:text-primary dark:text-[#8ba38b] font-medium"
              href="#"
              >Courses</a
            >
            <span class="text-[#638863] dark:text-[#8ba38b] font-medium"
              >/</span
            >
            <a
              class="text-[#638863] hover:text-primary dark:text-[#8ba38b] font-medium"
              href="#"
              >CS101 - Intro to Algorithms</a
            >
            <span class="text-[#638863] dark:text-[#8ba38b] font-medium"
              >/</span
            >
            <span class="text-[#111811] dark:text-white font-medium"
              >Assignment 1</span
            >
          </div>
        </div>
      </nav>
      <div
        class="flex flex-col md:flex-row md:items-center justify-between mb-8 gap-4"
      >
        <div class="flex items-center gap-4">
          <h1 class="text-2xl font-bold text-gray-900 dark:text-white">
            Assignment 1
          </h1>
        </div>
      </div>
      <div
        class="bg-card-light dark:bg-card-dark rounded-xl shadow-sm border border-border-light dark:border-blue-700 p-8 md:p-12 mb-8 flex flex-col items-center justify-center text-center"
      >
        <div class="relative w-64 h-64 mb-6">
          <svg class="w-full h-full transform -rotate-90" viewBox="0 0 100 100">
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
              stroke-dasharray="251.2"
              stroke-dashoffset="50.24"
              stroke-linecap="round"
              stroke-width="8"
            ></circle>
          </svg>
          <div
            class="absolute inset-0 flex flex-col items-center justify-center"
          >
            <span
              class="text-5xl font-bold text-gray-900 dark:text-white tracking-tight"
              >24/30</span
            >
            <span
              class="text-lg text-text-muted-light dark:text-text-muted-dark mt-1 font-medium"
              >80%</span
            >
          </div>
        </div>
      </div>
      <div class="mb-8">
        <div class="flex items-center gap-2 mb-4">
          <span class="material-symbols-outlined text-primary">analytics</span>
          <h3
            class="text-sm font-bold uppercase tracking-wider text-text-muted-light dark:text-text-muted-dark"
          >
            Class Performance Statistics
          </h3>
          <div
            class="ml-auto text-xs text-text-muted-light dark:text-text-muted-dark"
          >
            Total Participants: 142 Students
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
              21.5
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
              22.0
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
              3.4
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
            <div class="text-2xl font-bold text-blue-600 dark:text-blue-400">
              29
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
              12
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
            12 (Min)
          </div>
          <div
            class="absolute right-0 -top-6 text-xs font-medium text-text-muted-light dark:text-text-muted-dark"
          >
            30 (Full Mark)
          </div>
          <div
            class="absolute -top-8 text-[10px] font-semibold text-text-muted-light dark:text-text-muted-dark transform -translate-x-1/2"
            style="left: 52%"
          >
            Mean: 21.5
          </div>
          <div
            class="absolute top-5 text-[10px] font-semibold text-text-muted-light dark:text-text-muted-dark transform -translate-x-1/2"
            style="left: 94%"
          >
            High: 29
          </div>
          <div
            class="absolute top-0 w-full h-3 bg-gray-100 dark:bg-blue-900/50 rounded-full mt-2"
          ></div>
          <div
            class="absolute top-0 w-0.5 h-7 bg-gray-400 dark:bg-blue-500 transform -translate-x-1/2"
            style="left: 52%"
          ></div>
          <div
            class="absolute -top-3 transform -translate-x-1/2 flex flex-col items-center group cursor-pointer"
            style="left: 66%"
          >
            <div
              class="bg-primary text-white text-xs font-bold px-2 py-1 rounded mb-1 shadow-md whitespace-nowrap"
            >
              YOU: 24
            </div>
            <div class="w-1 h-8 bg-primary rounded-full"></div>
          </div>
        </div>
      </div>
    </main>
  </div>
</template>

<script>
export default {
  name: "Score",
  data() {
    return {
      isOpen: false,
    };
  },

  methods: {
    toggleDropdown() {
      this.isOpen = !this.isOpen;
    },
    handleClickOutside(event) {
      if (!this.$refs.dropdownRef.contains(event.target)) {
        this.isOpen = false;
      }
    },
  },

  mounted() {
    document.addEventListener("click", this.handleClickOutside);
  },

  beforeUnmount() {
    document.removeEventListener("click", this.handleClickOutside);
  },
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
