<template>
  <div
    class="bg-gray-50 dark:bg-background-dark text-text-light dark:text-text-dark transition-colors duration-200 min-h-screen flex flex-col"
  >
    <header
      class="bg-surface-light dark:bg-surface-dark border-b border-border-light dark:border-border-dark sticky top-0 z-10 shadow-sm"
    >
      <div class="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
        <div class="flex justify-between items-center h-16">
          <div class="flex items-center">
            <div class="flex-shrink-0 flex items-center gap-2">
              <div
                class="bg-primary rounded-lg p-1.5 flex items-center justify-center"
              >
                <span class="material-symbols-outlined text-white text-xl"
                  >school</span
                >
              </div>
              <span
                class="font-bold text-lg tracking-tight text-gray-900 dark:text-white"
                >University Grade Portal</span
              >
            </div>
          </div>
          <div class="flex items-center space-x-6">
            <a
              class="text-text-muted-light dark:text-text-muted-dark hover:text-primary dark:hover:text-primary font-medium px-1 py-5 text-sm transition-colors"
              href="#"
              >Overview</a
            >
            <div class="relative">
              <button
                class="flex text-sm border-2 border-transparent rounded-full focus:outline-none focus:border-gray-300 transition duration-150 ease-in-out"
              >
                <img
                  alt="User Avatar"
                  class="h-9 w-9 rounded-full object-cover border border-gray-200 dark:border-gray-600"
                  src="https://lh3.googleusercontent.com/aida-public/AB6AXuA6ks6i0YSsJsdUh4f96EGndBnmP5pOe0jjp_Q9acQEQM11AzaPK7CCc7w-QiLzzN_qmRFO6MoO1BUx0mq50TWJai3AYppjYwm0WmzXNk9gCodOda6Fln53ift0i4aOWutD0QihvMIyWdrlVe9bpfd8iaTyMDGDlVQFeXYITSMNcEaBk_SRw4GQAq2XvI0W-vb8uGMcGqvaS4uYNMiJXtr4p83cjHH_n0uhwOn-HWItnMXbPU3_rAg0HM6wz3pruWbigJmGvuRaYg"
                />
              </button>
            </div>
            <button
              class="text-text-muted-light dark:text-text-muted-dark hover:text-primary dark:hover:text-primary transition-colors"
            >
              <span
                class="material-symbols-outlined text-2xl transform rotate-180"
                >logout</span
              >
            </button>
          </div>
        </div>
      </div>
    </header>
    <main class="flex-grow max-w-7xl w-full mx-auto px-4 sm:px-6 lg:px-8 py-8">
      <div
        class="mb-6 flex items-center text-sm font-medium text-text-muted-light dark:text-text-muted-dark"
      >
        <a
          class="hover:text-primary dark:hover:text-primary transition-colors"
          href="#"
          >Courses</a
        >
        <span class="mx-2 text-gray-400">/</span>
        <span class="text-gray-900 dark:text-white"
          >CS101 - Intro to Algorithms</span
        >
      </div>
      <div
        class="flex flex-col md:flex-row md:items-center justify-between gap-4 mb-8"
      >
        <h1
          class="text-3xl font-bold text-gray-900 dark:text-white whitespace-nowrap"
        >
          CS101 - Intro to Computer Science
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
              class="block w-full pl-10 pr-3 py-2 border border-border-light dark:border-border-dark rounded-md leading-5 bg-white dark:bg-surface-dark text-gray-900 dark:text-gray-100 placeholder-gray-500 focus:outline-none focus:ring-1 focus:ring-primary focus:border-primary sm:text-sm"
              placeholder="Search assignments..."
              type="text"
            />
          </div>
          <button
            class="inline-flex items-center justify-center px-4 py-2 border border-transparent text-sm font-medium rounded-md shadow-sm text-white bg-primary hover:bg-primary-dark focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-primary transition-colors whitespace-nowrap"
          >
            <span class="material-symbols-outlined mr-2 text-lg">add</span>
            Create New Assignment
          </button>
        </div>
      </div>
      <div class="flex flex-col space-y-4">
        <div
          class="bg-white dark:bg-surface-dark border border-border-light dark:border-border-dark rounded-xl px-6 py-5 shadow-sm hover:shadow-md transition-shadow"
        >
          <div class="flex items-center justify-between">
            <h3 class="text-lg font-semibold text-gray-900 dark:text-white">
              Midterm Exam
            </h3>
            <div class="flex items-center gap-2">
                <!-- View&Edit botton -->
              <button class="text-sm font-medium text-primary hover:text-primary-dark border border-border-light dark:border-border-dark hover:border-primary bg-white dark:bg-surface-dark rounded-lg px-4 py-2 transition-colors shadow-sm">
                View &amp; Edit Scores
              </button>
                <!-- Archive botton -->
              <button class="flex items-center justify-center p-2 rounded-lg text-gray-500 hover:text-yellow-700 hover:bg-yellow-50 transition-colors"
                title="Delete Assignment" >
                <span class="material-symbols-outlined text-xl">archive</span>
              </button>
                <!-- Delete botton -->
              <button class="flex items-center justify-center p-2 rounded-lg text-gray-500 hover:text-red-700 hover:bg-red-50 transition-colors"
                title="Delete Assignment">
                <span class="material-symbols-outlined text-xl">delete</span>
              </button>

            </div>
          </div>
        </div>
        <div
          class="bg-white dark:bg-surface-dark border border-border-light dark:border-border-dark rounded-xl px-6 py-5 shadow-sm hover:shadow-md transition-shadow"
        >
          <div class="flex items-center justify-between">
            <h3 class="text-lg font-semibold text-gray-900 dark:text-white">
              Database Project Phase 1
            </h3>
            <div class="flex items-center gap-2">
                <!-- View&Edit botton -->
              <button class="text-sm font-medium text-primary hover:text-primary-dark border border-border-light dark:border-border-dark hover:border-primary bg-white dark:bg-surface-dark rounded-lg px-4 py-2 transition-colors shadow-sm">
                View &amp; Edit Scores
              </button>
                <!-- Archive botton -->
              <button class="flex items-center justify-center p-2 rounded-lg text-gray-500 hover:text-yellow-700 hover:bg-yellow-50 transition-colors"
                title="Delete Assignment" >
                <span class="material-symbols-outlined text-xl">archive</span>
              </button>
                <!-- Delete botton -->
              <button class="flex items-center justify-center p-2 rounded-lg text-gray-500 hover:text-red-700 hover:bg-red-50 transition-colors"
                title="Delete Assignment">
                <span class="material-symbols-outlined text-xl">delete</span>
              </button>

            </div>
          </div>
        </div>
        <div
          class="bg-white dark:bg-surface-dark border border-border-light dark:border-border-dark rounded-xl px-6 py-5 shadow-sm hover:shadow-md transition-shadow"
        >
          <div class="flex items-center justify-between">
            <h3 class="text-lg font-semibold text-gray-900 dark:text-white">
              SQL Practice Quiz
            </h3>
            <div class="flex items-center gap-2">
                <!-- View&Edit botton -->
              <button class="text-sm font-medium text-primary hover:text-primary-dark border border-border-light dark:border-border-dark hover:border-primary bg-white dark:bg-surface-dark rounded-lg px-4 py-2 transition-colors shadow-sm">
                View &amp; Edit Scores
              </button>
                <!-- Archive botton -->
              <button class="flex items-center justify-center p-2 rounded-lg text-gray-500 hover:text-yellow-700 hover:bg-yellow-50 transition-colors"
                title="Delete Assignment" >
                <span class="material-symbols-outlined text-xl">archive</span>
              </button>
                <!-- Delete botton -->
              <button class="flex items-center justify-center p-2 rounded-lg text-gray-500 hover:text-red-700 hover:bg-red-50 transition-colors"
                title="Delete Assignment">
                <span class="material-symbols-outlined text-xl">delete</span>
              </button>

            </div>
          </div>
        </div>
        <div
          class="bg-white dark:bg-surface-dark border border-border-light dark:border-border-dark rounded-xl px-6 py-5 shadow-sm hover:shadow-md transition-shadow"
        >
          <div class="flex items-center justify-between">
            <h3 class="text-lg font-semibold text-gray-900 dark:text-white">
              Normalization Exercise
            </h3>
            <div class="flex items-center gap-2">
                <!-- View&Edit botton -->
              <button class="text-sm font-medium text-primary hover:text-primary-dark border border-border-light dark:border-border-dark hover:border-primary bg-white dark:bg-surface-dark rounded-lg px-4 py-2 transition-colors shadow-sm">
                View &amp; Edit Scores
              </button>
                <!-- Archive botton -->
              <button class="flex items-center justify-center p-2 rounded-lg text-gray-500 hover:text-yellow-700 hover:bg-yellow-50 transition-colors"
                title="Delete Assignment" >
                <span class="material-symbols-outlined text-xl">archive</span>
              </button>
                <!-- Delete botton -->
              <button class="flex items-center justify-center p-2 rounded-lg text-gray-500 hover:text-red-700 hover:bg-red-50 transition-colors"
                title="Delete Assignment">
                <span class="material-symbols-outlined text-xl">delete</span>
              </button>

            </div>
          </div>
        </div>
      </div>
    </main>
    <footer class="mt-auto py-6">
      <div class="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 text-center">
        <p class="text-sm text-text-muted-light dark:text-text-muted-dark">
          © 2023 University Grade Portal. All rights reserved.
        </p>
      </div>
    </footer>
    <div class="fixed bottom-6 right-6 z-50">
      <button
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

<script>
export default {
  name: "AssignmentManagement",

  mounted() {
    const themeToggleBtn = document.getElementById("theme-toggle");
    const htmlElement = document.documentElement;
    if (
      localStorage.getItem("color-theme") === "dark" ||
      (!("color-theme" in localStorage) &&
        window.matchMedia("(prefers-color-scheme: dark)").matches)
    ) {
      htmlElement.classList.add("dark");
    } else {
      htmlElement.classList.remove("dark");
    }
    themeToggleBtn.addEventListener("click", function () {
      if (htmlElement.classList.contains("dark")) {
        htmlElement.classList.remove("dark");
        localStorage.setItem("color-theme", "light");
      } else {
        htmlElement.classList.add("dark");
        localStorage.setItem("color-theme", "dark");
      }
    });
  },
};
</script>
