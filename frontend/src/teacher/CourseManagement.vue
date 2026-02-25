<template>
<div class="bg-background-light dark:bg-background-dark text-text-light dark:text-text-dark transition-colors duration-200 min-h-screen flex flex-col">
<header class="bg-surface-light dark:bg-surface-dark border-b border-border-light dark:border-border-dark sticky top-0 z-10 shadow-sm">
<div class="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
<div class="flex justify-between items-center h-16">
<div class="flex items-center">
<div class="flex-shrink-0 flex items-center gap-2">
<div class="bg-primary rounded-lg p-1.5 flex items-center justify-center">
<span class="material-symbols-outlined text-white text-xl">school</span>
</div>
<span class="font-bold text-lg tracking-tight text-gray-900 dark:text-white">University Grade Portal</span>
</div>
</div>
<div class="flex items-center space-x-6">
<a class="text-primary font-medium border-b-2 border-primary px-1 py-5 text-sm" href="#">Overview</a>
<div class="relative">
<button class="flex text-sm border-2 border-transparent rounded-full focus:outline-none focus:border-gray-300 transition duration-150 ease-in-out">
<img alt="User Avatar" class="h-9 w-9 rounded-full object-cover border border-gray-200 dark:border-gray-600" src="https://lh3.googleusercontent.com/aida-public/AB6AXuA6ks6i0YSsJsdUh4f96EGndBnmP5pOe0jjp_Q9acQEQM11AzaPK7CCc7w-QiLzzN_qmRFO6MoO1BUx0mq50TWJai3AYppjYwm0WmzXNk9gCodOda6Fln53ift0i4aOWutD0QihvMIyWdrlVe9bpfd8iaTyMDGDlVQFeXYITSMNcEaBk_SRw4GQAq2XvI0W-vb8uGMcGqvaS4uYNMiJXtr4p83cjHH_n0uhwOn-HWItnMXbPU3_rAg0HM6wz3pruWbigJmGvuRaYg"/>
</button>
</div>
<button class="text-text-muted-light dark:text-text-muted-dark hover:text-primary dark:hover:text-primary transition-colors">
<span class="material-symbols-outlined text-2xl transform rotate-180">logout</span>
</button>
</div>
</div>
</div>
</header>
<main class="flex-grow max-w-7xl w-full mx-auto px-4 sm:px-6 lg:px-8 py-8">
<div class="md:flex md:items-center md:justify-between mb-8">
<div class="flex-1 min-w-0">
<h1 class="text-3xl font-bold leading-7 text-gray-900 dark:text-white sm:text-3xl sm:truncate">
                    Course Management
                </h1>
<p class="mt-2 text-sm text-text-muted-light dark:text-text-muted-dark">
                    Manage your assigned courses and student grades
                </p>
</div>
</div>
<div class="bg-surface-light dark:bg-surface-dark rounded-xl shadow-sm border border-border-light dark:border-border-dark p-4 mb-6 flex flex-col sm:flex-row justify-between items-center gap-4">
<div class="relative w-full sm:max-w-md">
<div class="absolute inset-y-0 left-0 pl-3 flex items-center pointer-events-none">
<span class="material-symbols-outlined text-gray-400">search</span>
</div>
<input class="block w-full pl-10 pr-3 py-2 border-none bg-gray-50 dark:bg-gray-800 rounded-lg text-gray-900 dark:text-white placeholder-gray-400 focus:outline-none focus:ring-2 focus:ring-primary sm:text-sm" id="search" name="search" placeholder="Search Course Code or Name..." type="text"/>
</div>
<div class="flex w-full sm:w-auto items-center gap-4">
<button class="inline-flex items-center justify-center px-4 py-2 border border-transparent text-sm font-medium rounded-lg shadow-sm text-white bg-primary hover:bg-primary-dark focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-primary transition-colors whitespace-nowrap">
<span class="material-symbols-outlined text-white text-lg mr-2">add</span>
                    Create Course
                </button>
</div>
</div>
<div class="bg-surface-light dark:bg-surface-dark shadow-sm rounded-xl border border-border-light dark:border-border-dark overflow-hidden">
<div class="px-6 py-4 border-b border-border-light dark:border-border-dark flex justify-between items-center bg-gray-50/50 dark:bg-gray-800/30">
<span class="text-xs font-semibold text-text-muted-light dark:text-text-muted-dark uppercase tracking-wider">Course Info</span>
<div class="flex items-center gap-8">
<span class="text-xs font-semibold text-text-muted-light dark:text-text-muted-dark uppercase tracking-wider">Enrolled</span>
<span class="w-8"></span>
</div>
</div>
<ul class="divide-y divide-border-light dark:divide-border-dark">
<li class="hover:bg-gray-50 dark:hover:bg-gray-800/50 transition-colors duration-150">
<div class="px-6 py-5 flex items-center justify-between">
<a class="flex items-center flex-grow" href="#">
<div class="flex-shrink-0 h-12 w-12 rounded-xl bg-blue-100 dark:bg-blue-900/30 text-blue-600 dark:text-blue-400 flex items-center justify-center">
<span class="material-symbols-outlined">laptop_mac</span>
</div>
<div class="ml-4">
<div class="text-base font-bold text-gray-900 dark:text-white">CS101</div>
<div class="text-sm text-text-muted-light dark:text-text-muted-dark">Intro to Computer Science</div>
</div>
</a>
<div class="flex items-center gap-6">
<div class="flex flex-col items-end min-w-[80px]">
<div class="flex items-center text-gray-900 dark:text-white font-semibold">
<span class="material-symbols-outlined text-text-muted-light dark:text-text-muted-dark mr-1 text-lg">people</span>
                                    142
                                </div>
<div class="text-xs text-text-muted-light dark:text-text-muted-dark uppercase mt-0.5">Students</div>
</div>
<button class="p-2 text-gray-400 hover:text-red-600 hover:bg-red-50 dark:hover:bg-red-900/30 rounded-full transition-colors duration-200 group" title="Delete Course">
<span class="material-symbols-outlined text-xl group-hover:text-red-600">delete</span>
</button>
</div>
</div>
</li>
<li class="hover:bg-gray-50 dark:hover:bg-gray-800/50 transition-colors duration-150">
<div class="px-6 py-5 flex items-center justify-between">
<a class="flex items-center flex-grow" href="#">
<div class="flex-shrink-0 h-12 w-12 rounded-xl bg-sky-100 dark:bg-sky-900/30 text-sky-600 dark:text-sky-400 flex items-center justify-center">
<span class="material-symbols-outlined">science</span>
</div>
<div class="ml-4">
<div class="text-base font-bold text-gray-900 dark:text-white">BIO205</div>
<div class="text-sm text-text-muted-light dark:text-text-muted-dark">Molecular Biology</div>
</div>
</a>
<div class="flex items-center gap-6">
<div class="flex flex-col items-end min-w-[80px]">
<div class="flex items-center text-gray-900 dark:text-white font-semibold">
<span class="material-symbols-outlined text-text-muted-light dark:text-text-muted-dark mr-1 text-lg">people</span>
                                    45
                                </div>
<div class="text-xs text-text-muted-light dark:text-text-muted-dark uppercase mt-0.5">Students</div>
</div>
<button class="p-2 text-gray-400 hover:text-red-600 hover:bg-red-50 dark:hover:bg-red-900/30 rounded-full transition-colors duration-200 group" title="Delete Course">
<span class="material-symbols-outlined text-xl group-hover:text-red-600">delete</span>
</button>
</div>
</div>
</li>
<li class="hover:bg-gray-50 dark:hover:bg-gray-800/50 transition-colors duration-150">
<div class="px-6 py-5 flex items-center justify-between">
<a class="flex items-center flex-grow" href="#">
<div class="flex-shrink-0 h-12 w-12 rounded-xl bg-purple-100 dark:bg-purple-900/30 text-purple-600 dark:text-purple-400 flex items-center justify-center">
<span class="material-symbols-outlined">menu_book</span>
</div>
<div class="ml-4">
<div class="text-base font-bold text-gray-900 dark:text-white">ENG302</div>
<div class="text-sm text-text-muted-light dark:text-text-muted-dark">Creative Writing</div>
</div>
</a>
<div class="flex items-center gap-6">
<div class="flex flex-col items-end min-w-[80px]">
<div class="flex items-center text-gray-900 dark:text-white font-semibold">
<span class="material-symbols-outlined text-text-muted-light dark:text-text-muted-dark mr-1 text-lg">people</span>
                                    28
                                </div>
<div class="text-xs text-text-muted-light dark:text-text-muted-dark uppercase mt-0.5">Students</div>
</div>
<button class="p-2 text-gray-400 hover:text-red-600 hover:bg-red-50 dark:hover:bg-red-900/30 rounded-full transition-colors duration-200 group" title="Delete Course">
<span class="material-symbols-outlined text-xl group-hover:text-red-600">delete</span>
</button>
</div>
</div>
</li>
<li class="hover:bg-gray-50 dark:hover:bg-gray-800/50 transition-colors duration-150">
<div class="px-6 py-5 flex items-center justify-between">
<a class="flex items-center flex-grow" href="#">
<div class="flex-shrink-0 h-12 w-12 rounded-xl bg-orange-100 dark:bg-orange-900/30 text-orange-600 dark:text-orange-400 flex items-center justify-center">
<span class="material-symbols-outlined">history_edu</span>
</div>
<div class="ml-4">
<div class="text-base font-bold text-gray-900 dark:text-white">HIS201</div>
<div class="text-sm text-text-muted-light dark:text-text-muted-dark">World History</div>
</div>
</a>
<div class="flex items-center gap-6">
<div class="flex flex-col items-end min-w-[80px]">
<div class="flex items-center text-gray-900 dark:text-white font-semibold">
<span class="material-symbols-outlined text-text-muted-light dark:text-text-muted-dark mr-1 text-lg">people</span>
                                    89
                                </div>
<div class="text-xs text-text-muted-light dark:text-text-muted-dark uppercase mt-0.5">Students</div>
</div>
<button class="p-2 text-gray-400 hover:text-red-600 hover:bg-red-50 dark:hover:bg-red-900/30 rounded-full transition-colors duration-200 group" title="Delete Course">
<span class="material-symbols-outlined text-xl group-hover:text-red-600">delete</span>
</button>
</div>
</div>
</li>
</ul>
<div class="px-6 py-4 border-t border-border-light dark:border-border-dark flex items-center justify-between">
<div class="text-sm text-text-muted-light dark:text-text-muted-dark">
                    Showing <span class="font-bold text-gray-900 dark:text-white">1-4</span> of <span class="font-bold text-gray-900 dark:text-white">12</span> courses
                </div>
<div class="flex space-x-2">
<button class="p-2 border border-border-light dark:border-border-dark rounded-md text-gray-400 hover:text-gray-500 dark:hover:text-gray-300 bg-white dark:bg-surface-dark hover:bg-gray-50 dark:hover:bg-gray-700">
<span class="material-symbols-outlined text-sm">chevron_left</span>
</button>
<button class="px-3 py-1 border border-primary bg-primary text-white text-sm font-medium rounded-md">
                        1
                    </button>
<button class="px-3 py-1 border border-border-light dark:border-border-dark bg-white dark:bg-surface-dark text-gray-700 dark:text-gray-200 text-sm font-medium rounded-md hover:bg-gray-50 dark:hover:bg-gray-700">
                        2
                    </button>
<button class="px-3 py-1 border border-border-light dark:border-border-dark bg-white dark:bg-surface-dark text-gray-700 dark:text-gray-200 text-sm font-medium rounded-md hover:bg-gray-50 dark:hover:bg-gray-700">
                        3
                    </button>
<button class="p-2 border border-border-light dark:border-border-dark rounded-md text-gray-400 hover:text-gray-500 dark:hover:text-gray-300 bg-white dark:bg-surface-dark hover:bg-gray-50 dark:hover:bg-gray-700">
<span class="material-symbols-outlined text-sm">chevron_right</span>
</button>
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
<button class="p-3 rounded-full bg-surface-light dark:bg-surface-dark text-gray-500 dark:text-gray-400 hover:text-primary dark:hover:text-primary shadow-lg border border-border-light dark:border-border-dark transition-all duration-300 focus:outline-none" id="theme-toggle">
<span class="material-symbols-outlined text-2xl hidden dark:block" id="theme-icon-dark">dark_mode</span>
<span class="material-symbols-outlined text-2xl block dark:hidden" id="theme-icon-light">light_mode</span>
</button>
</div>
</div>
</template>

<script>
export default {
  name: "CourseManagement",

  mounted() {
    // Theme Toggle Logic
        const themeToggleBtn = document.getElementById('theme-toggle');
        const htmlElement = document.documentElement;
        // Check local storage or system preference on load
        if (localStorage.getItem('color-theme') === 'dark' || (!('color-theme' in localStorage) && window.matchMedia('(prefers-color-scheme: dark)').matches)) {
            htmlElement.classList.add('dark');
        } else {
            htmlElement.classList.remove('dark');
        }
        themeToggleBtn.addEventListener('click', function() {
            if (htmlElement.classList.contains('dark')) {
                htmlElement.classList.remove('dark');
                localStorage.setItem('color-theme', 'light');
            } else {
                htmlElement.classList.add('dark');
                localStorage.setItem('color-theme', 'dark');
            }
        });
  }
}
</script>
