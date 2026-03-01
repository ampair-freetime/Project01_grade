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
    <main class="flex-1 flex flex-col h-full overflow-hidden relative">
      <div
        class="absolute top-0 left-0 w-full h-32  pointer-events-none"
      ></div>
      <div class="flex-1 overflow-y-auto p-8 lg:p-12">
        <div class="max-w-5xl mx-auto flex flex-col gap-8">
          <header
            class="flex flex-col md:flex-row md:items-end justify-between gap-6"
          >
            <div class="flex flex-col gap-2">
              <h2
                class="text-[#111811] dark:text-white text-3xl md:text-4xl font-bold tracking-tight"
              >
                Hello, Alex
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
                  class="w-full bg-transparent border-none text-[#111811] dark:text-white placeholder:text-[#637888]/70 focus:ring-0 focus:outline-none text-base h-full"
                  placeholder="Search courses..."
                />
              </label>
            </div>
          </header>
          <section class="flex flex-col gap-4">
            <div class="flex items-center justify-between mb-2">
              <h3
                class="text-lg font-semibold text-[#111811] dark:text-white flex items-center gap-2"
              >
                Current Enrolled Courses
                <span
                  class="bg-[#e0e7eb] dark:bg-[#253038] text-[#4e5b6b] dark:text-[#a0b8cf] text-xs px-2 py-0.5 rounded-full"
                  >5</span
                >
              </h3>
              <div
                class="flex items-center gap-2 text-sm text-[#4e5b6b] cursor-pointer hover:text-[#111811] dark:hover:text-white transition-colors"
              >
                <span class="material-symbols-outlined text-[18px]">sort</span>
                Sort by recent
              </div>
            </div>
            <div
              class="group bg-white dark:bg-[#1a232e] p-4 rounded-xl shadow-sm border border-transparent hover:border-primary/40 hover:shadow-md transition-all duration-200 cursor-pointer"
            >
              <div class="flex items-center justify-between gap-4">
                <div class="flex items-center gap-5 overflow-hidden">
                  <div
                    class="shrink-0 size-14 rounded-xl bg-gradient-to-br from-[#f0f4f8] to-[#e8f1f5] dark:from-[#253038] dark:to-[#1f2633] flex items-center justify-center text-[#111811] dark:text-white group-hover:scale-105 transition-transform"
                  >
                    <span class="material-symbols-outlined text-3xl"
                      >terminal</span
                    >
                  </div>
                  <div class="flex flex-col min-w-0">
                    <div class="flex items-center gap-2 mb-0.5">
                      <span
                        class="font-mono text-xs font-bold text-[#637888] dark:text-[#a0b8cf] bg-[#f0f4f8] dark:bg-[#253038] px-1.5 py-0.5 rounded"
                        >CS101</span
                      >
                    </div>
                    <h4
                      class="text-[#111811] dark:text-white text-lg font-semibold truncate group-hover:text-primary transition-colors"
                    >
                      Introduction to Computer Science
                    </h4>
                  </div>
                </div>
                <div
                  class="shrink-0 flex items-center justify-center size-10 rounded-full bg-[#f6f8fa] dark:bg-[#253038] text-[#111811] dark:text-white group-hover:bg-primary group-hover:text-white transition-colors"
                >
                  <span class="material-symbols-outlined">arrow_forward</span>
                </div>
              </div>
            </div>
            <div
              class="group bg-white dark:bg-[#1a232e] p-4 rounded-xl shadow-sm border border-transparent hover:border-primary/40 hover:shadow-md transition-all duration-200 cursor-pointer"
            >
              <div class="flex items-center justify-between gap-4">
                <div class="flex items-center gap-5 overflow-hidden">
                  <div
                    class="shrink-0 size-14 rounded-xl bg-gradient-to-br from-[#f0f4f8] to-[#e8f1f5] dark:from-[#253038] dark:to-[#1f2633] flex items-center justify-center text-[#111811] dark:text-white group-hover:scale-105 transition-transform"
                  >
                    <span class="material-symbols-outlined text-3xl"
                      >biotech</span
                    >
                  </div>
                  <div class="flex flex-col min-w-0">
                    <div class="flex items-center gap-2 mb-0.5">
                      <span
                        class="font-mono text-xs font-bold text-[#637888] dark:text-[#a0b8cf] bg-[#f0f4f8] dark:bg-[#253038] px-1.5 py-0.5 rounded"
                        >BIO101</span
                      >
                    </div>
                    <h4
                      class="text-[#111811] dark:text-white text-lg font-semibold truncate group-hover:text-primary transition-colors"
                    >
                      General Biology I
                    </h4>
                  </div>
                </div>
                <div
                  class="shrink-0 flex items-center justify-center size-10 rounded-full bg-[#f6f8fa] dark:bg-[#253038] text-[#111811] dark:text-white group-hover:bg-primary group-hover:text-white transition-colors"
                >
                  <span class="material-symbols-outlined">arrow_forward</span>
                </div>
              </div>
            </div>
            <div
              class="group bg-white dark:bg-[#1a232e] p-4 rounded-xl shadow-sm border border-transparent hover:border-primary/40 hover:shadow-md transition-all duration-200 cursor-pointer"
            >
              <div class="flex items-center justify-between gap-4">
                <div class="flex items-center gap-5 overflow-hidden">
                  <div
                    class="shrink-0 size-14 rounded-xl bg-gradient-to-br from-[#f0f4f8] to-[#e8f1f5] dark:from-[#253038] dark:to-[#1f2633] flex items-center justify-center text-[#111811] dark:text-white group-hover:scale-105 transition-transform"
                  >
                    <span class="material-symbols-outlined text-3xl"
                      >functions</span
                    >
                  </div>
                  <div class="flex flex-col min-w-0">
                    <div class="flex items-center gap-2 mb-0.5">
                      <span
                        class="font-mono text-xs font-bold text-[#637888] dark:text-[#a0b8cf] bg-[#f0f4f8] dark:bg-[#253038] px-1.5 py-0.5 rounded"
                        >MATH202</span
                      >
                    </div>
                    <h4
                      class="text-[#111811] dark:text-white text-lg font-semibold truncate group-hover:text-primary transition-colors"
                    >
                      Calculus II
                    </h4>
                  </div>
                </div>
                <div
                  class="shrink-0 flex items-center justify-center size-10 rounded-full bg-[#f6f8fa] dark:bg-[#253038] text-[#111811] dark:text-white group-hover:bg-primary group-hover:text-white transition-colors"
                >
                  <span class="material-symbols-outlined">arrow_forward</span>
                </div>
              </div>
            </div>
            <div
              class="group bg-white dark:bg-[#1a232e] p-4 rounded-xl shadow-sm border border-transparent hover:border-primary/40 hover:shadow-md transition-all duration-200 cursor-pointer"
            >
              <div class="flex items-center justify-between gap-4">
                <div class="flex items-center gap-5 overflow-hidden">
                  <div
                    class="shrink-0 size-14 rounded-xl bg-gradient-to-br from-[#f0f4f8] to-[#e8f1f5] dark:from-[#253038] dark:to-[#1f2633] flex items-center justify-center text-[#111811] dark:text-white group-hover:scale-105 transition-transform"
                  >
                    <span class="material-symbols-outlined text-3xl"
                      >auto_stories</span
                    >
                  </div>
                  <div class="flex flex-col min-w-0">
                    <div class="flex items-center gap-2 mb-0.5">
                      <span
                        class="font-mono text-xs font-bold text-[#637888] dark:text-[#a0b8cf] bg-[#f0f4f8] dark:bg-[#253038] px-1.5 py-0.5 rounded"
                        >ENG105</span
                      >
                    </div>
                    <h4
                      class="text-[#111811] dark:text-white text-lg font-semibold truncate group-hover:text-primary transition-colors"
                    >
                      Academic Writing
                    </h4>
                  </div>
                </div>
                <div
                  class="shrink-0 flex items-center justify-center size-10 rounded-full bg-[#f6f8fa] dark:bg-[#253038] text-[#111811] dark:text-white group-hover:bg-primary group-hover:text-white transition-colors"
                >
                  <span class="material-symbols-outlined">arrow_forward</span>
                </div>
              </div>
            </div>
            <div
              class="group bg-white dark:bg-[#1a232e] p-4 rounded-xl shadow-sm border border-transparent hover:border-primary/40 hover:shadow-md transition-all duration-200 cursor-pointer"
            >
              <div class="flex items-center justify-between gap-4">
                <div class="flex items-center gap-5 overflow-hidden">
                  <div
                    class="shrink-0 size-14 rounded-xl bg-gradient-to-br from-[#f0f4f8] to-[#e8f1f5] dark:from-[#253038] dark:to-[#1f2633] flex items-center justify-center text-[#111811] dark:text-white group-hover:scale-105 transition-transform"
                  >
                    <span class="material-symbols-outlined text-3xl"
                      >history_edu</span
                    >
                  </div>
                  <div class="flex flex-col min-w-0">
                    <div class="flex items-center gap-2 mb-0.5">
                      <span
                        class="font-mono text-xs font-bold text-[#637888] dark:text-[#a0b8cf] bg-[#f0f4f8] dark:bg-[#253038] px-1.5 py-0.5 rounded"
                        >HIST300</span
                      >
                    </div>
                    <h4
                      class="text-[#111811] dark:text-white text-lg font-semibold truncate group-hover:text-primary transition-colors"
                    >
                      World History
                    </h4>
                  </div>
                </div>
                <div
                  class="shrink-0 flex items-center justify-center size-10 rounded-full bg-[#f6f8fa] dark:bg-[#253038] text-[#111811] dark:text-white group-hover:bg-primary group-hover:text-white transition-colors"
                >
                  <span class="material-symbols-outlined">arrow_forward</span>
                </div>
              </div>
            </div>
          </section>
        </div>
      </div>
    </main>
    <div class="fixed bottom-6 right-6 z-50">
      <button
        @click="toggleTheme"
        class="p-3 rounded-full bg-surface-light dark:bg-surface-dark text-gray-500 dark:text-gray-400 hover:text-primary dark:hover:text-primary shadow-lg border border-border-light dark:border-border-dark transition-all duration-300 focus:outline-none"
        id="theme-toggle"
      >
        <span
          class="material-symbols-outlined text-2xl hidden dark:block"
          id="theme-icon-dark"
          >dark_mode</span
        >
        <span
          class="material-symbols-outlined text-2xl block dark:hidden"
          id="theme-icon-light"
          >light_mode</span
        >
      </button>
    </div>
  </div>
</template>

<script setup>
name: "Dashboard";
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

const toggleTheme = () => {
  const htmlElement = document.documentElement;
  if (htmlElement.classList.contains("dark")) {
    htmlElement.classList.remove("dark");
    localStorage.setItem("color-theme", "light");
  } else {
    htmlElement.classList.add("dark");
    localStorage.setItem("color-theme", "dark");
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
