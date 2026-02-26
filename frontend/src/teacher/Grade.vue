<template>
<div class="bg-background-light dark:bg-background-dark font-sans text-text-main-light dark:text-text-main-dark min-h-screen transition-colors duration-200">
<header class="bg-white dark:bg-card-dark border-b border-border-light dark:border-border-dark sticky top-0 z-30">
<div class="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 h-16 flex items-center justify-between">
<div class="flex items-center space-x-8">
<a class="flex items-center space-x-2 group" href="#">
<div class="w-8 h-8 bg-sky-500 rounded-lg flex items-center justify-center text-white">
<span class="material-symbols-outlined text-xl">school</span>
</div>
<span class="text-lg font-bold text-gray-900 dark:text-white tracking-tight">UniGrade Portal</span>
</a>
</div>
<div class="flex items-center space-x-4">
<div class="h-8 w-8 rounded-full bg-gray-200 dark:bg-gray-700 overflow-hidden border border-gray-200 dark:border-gray-600 cursor-pointer">
<img alt="User Profile" class="w-full h-full object-cover" src="https://lh3.googleusercontent.com/aida-public/AB6AXuDiqKCaTOqZUXW9tQ-lDk427nmydxkPZ2VpXhXv32xrd3_IQZw_IB6zaegZWijTxnQvD36xUBsdl4aDV-4nzwzlPmf-IOIydZqP2QyV5IIIivuPRiC2M3Gu2Fq2cNvwTZVXWrNv6JHyVAnh-iCFAMiXUtheQCjKOUGn1z5xokQvF1sdXnTxHpyMKBdwdMwHk1w3_kBN4UlibfxxCOTqfHE00uzUtQfOoYVYNw30gWw8vub1V7zlJSwOyX9yQu4vwJ2wuhPAzXWaAw"/>
</div>
</div>
</div>
</header>
<main class="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-8 space-y-6">
<nav class="text-sm font-medium text-text-muted-light dark:text-text-muted-dark flex items-center space-x-2 flex-wrap">
<a class="hover:text-sky-500 transition-colors" href="#">Courses</a>
<span class="text-gray-300 dark:text-gray-600">/</span>
<a class="hover:text-sky-500 transition-colors" href="#">CS101 - Intro to Algorithms</a>
<span class="text-gray-300 dark:text-gray-600">/</span>
<span class="text-gray-900 dark:text-white font-semibold">Midterm Exam</span>
</nav>
<div class="flex flex-col lg:flex-row lg:items-end justify-between gap-4">
<div>
<div class="flex items-center gap-3 mb-1">
<h1 class="text-3xl font-bold text-gray-900 dark:text-white">Midterm Exam</h1>
<span class="px-2.5 py-0.5 rounded-full bg-sky-100 dark:bg-sky-900/30 text-sky-700 dark:text-sky-300 text-xs font-semibold border border-sky-200 dark:border-sky-800">Section A</span>
</div>
</div>
<div class="flex flex-wrap items-center gap-3">
<button class="inline-flex items-center px-4 py-2 bg-white dark:bg-slate-800 border border-gray-300 dark:border-slate-600 rounded-lg text-sm font-medium text-gray-700 dark:text-gray-200 hover:bg-gray-50 dark:hover:bg-slate-700 shadow-sm transition-colors">
<span class="material-symbols-outlined text-lg mr-2">upload_file</span>
                Import CSV
            </button>
<button class="inline-flex items-center px-4 py-2 bg-slate-900 dark:bg-slate-700 border border-transparent rounded-lg text-sm font-medium text-white hover:bg-slate-800 dark:hover:bg-slate-600 shadow-sm transition-colors">
<span class="material-symbols-outlined text-lg mr-2">publish</span>
                Publish Scores
            </button>
<button class="inline-flex items-center px-4 py-2 bg-sky-500 dark:bg-sky-600 border border-transparent rounded-lg text-sm font-medium text-white hover:opacity-90 shadow-sm transition-colors">
<span class="material-symbols-outlined text-lg mr-2">save</span>
                Save Changes
            </button>
</div>
</div>
<div class="bg-white dark:bg-card-dark rounded-xl border border-border-light dark:border-border-dark p-2 flex flex-col md:flex-row items-center justify-between gap-4 shadow-sm">
<div class="relative w-full md:w-96">
<span class="absolute inset-y-0 left-0 pl-3 flex items-center pointer-events-none">
<span class="material-symbols-outlined text-gray-400 dark:text-gray-500">search</span>
</span>
<input class="pl-10 pr-4 py-2 w-full bg-gray-50 dark:bg-slate-800/50 border border-gray-200 dark:border-slate-700 rounded-lg text-sm focus:ring-2 focus:ring-sky-500 focus:border-transparent dark:text-white dark:placeholder-gray-500" placeholder="Search by name or student ID..." type="text"/>
</div>
<div class="flex items-center gap-4 w-full md:w-auto justify-between md:justify-end overflow-x-auto pb-2 md:pb-0">
<div class="flex items-center gap-2 text-sm text-text-muted-light dark:text-text-muted-dark whitespace-nowrap">
<span class="uppercase text-xs font-bold tracking-wider mr-1 text-gray-400 dark:text-gray-500">Status:</span>
<button class="px-3 py-1.5 bg-slate-900 dark:bg-slate-100 text-white dark:text-slate-900 rounded-md font-medium text-xs">All Students</button>
<button class="px-3 py-1.5 text-gray-600 dark:text-gray-300 hover:bg-gray-100 dark:hover:bg-slate-800 rounded-md font-medium text-xs flex items-center gap-1 transition-colors">
                    Read Announcement 
                    <span class="bg-sky-100 dark:bg-sky-900 text-sky-700 dark:text-sky-300 px-1.5 py-0.5 rounded-full text-[10px]">12</span>
</button>
<button class="px-3 py-1.5 text-gray-600 dark:text-gray-300 hover:bg-gray-100 dark:hover:bg-slate-800 rounded-md font-medium text-xs flex items-center gap-1 transition-colors">
                    Unread 
                    <span class="bg-amber-100 dark:bg-amber-900 text-amber-700 dark:text-amber-300 px-1.5 py-0.5 rounded-full text-[10px]">4</span>
</button>
</div>
<div class="w-px h-6 bg-gray-200 dark:bg-gray-700 hidden md:block"></div>
<div class="flex items-center gap-2 text-sm whitespace-nowrap">
<span class="uppercase text-xs font-bold tracking-wider text-gray-400 dark:text-gray-500">Sort By:</span>
<button class="flex items-center gap-1 font-semibold text-gray-800 dark:text-white hover:text-sky-500 transition-colors">
                    ID
                    <span class="material-symbols-outlined text-sm">expand_more</span>
</button>
</div>
</div>
</div>
<div class="bg-white dark:bg-card-dark rounded-xl border border-border-light dark:border-border-dark shadow-sm overflow-hidden">
<div class="overflow-x-auto">
<table class="w-full text-left border-collapse">
<thead>
<tr class="border-b border-border-light dark:border-border-dark bg-gray-50/50 dark:bg-slate-800/50">
<th class="p-4 text-xs font-bold text-gray-500 dark:text-gray-400 uppercase tracking-wider pl-6">Student Info</th>
<th class="p-4 text-xs font-bold text-gray-500 dark:text-gray-400 uppercase tracking-wider w-32 text-center">Score (0-100)</th>
<th class="p-4 text-xs font-bold text-gray-500 dark:text-gray-400 uppercase tracking-wider text-center">Status</th>
<th class="p-4 text-xs font-bold text-gray-500 dark:text-gray-400 uppercase tracking-wider text-right pr-6">Last Updated</th>
<th class="p-4 text-xs font-bold text-gray-500 dark:text-gray-400 uppercase tracking-wider text-center w-16">Action</th>
</tr>
</thead>
<tbody class="divide-y divide-border-light dark:divide-border-dark">
<tr class="group hover:bg-gray-50 dark:hover:bg-slate-800/50 transition-colors">
<td class="p-4 pl-6">
<div class="flex items-center gap-3">
<div class="w-10 h-10 rounded-full overflow-hidden flex-shrink-0">
<img alt="Alice Johnson" class="w-full h-full object-cover" src="https://lh3.googleusercontent.com/aida-public/AB6AXuBkSaqLRo55aSxruOMViPHwv4KXrCEh-Jt4rRHt0pzsYYkq6PChv3pfMUyxSiCkxd2z0z0KRTtThtJX_QiepD7rSfF-oqCMtqoraUVKfMl_Q2qr8ooHr1DTbhKfoD5zSIQjukFXEShxlvU6EHk3FUhKhMxXdVgoOq8RHG3MHaxcdHo98M6JRhOfbVQzjy0oGXGOx3h6FRjg4ASkFah3R-BqKPGHv_My_GLm8rsCnirFjXf6kvCJ-pUG5JzfUo4gpgfVm87sVrEbOw"/>
</div>
<div>
<div class="font-semibold text-gray-900 dark:text-white">Alice Johnson</div>
<div class="text-xs text-text-muted-light dark:text-text-muted-dark">ID: 2023001</div>
</div>
</div>
</td>
<td class="p-4 text-center">
<div class="w-16 h-10 mx-auto border border-gray-200 dark:border-slate-600 rounded-lg flex items-center justify-center font-semibold text-gray-900 dark:text-white bg-white dark:bg-slate-900">
                            92
                        </div>
</td>
<td class="p-4 text-center">
<span class="inline-flex items-center gap-1.5 px-2.5 py-1 rounded-full text-xs font-medium bg-sky-100 dark:bg-sky-900/30 text-sky-700 dark:text-sky-300">
<span class="w-1.5 h-1.5 rounded-full bg-sky-500"></span>
                            Read
                        </span>
</td>
<td class="p-4 text-right pr-6">
<div class="text-xs font-medium text-gray-900 dark:text-gray-200">Oct 24, 2023</div>
<div class="text-[10px] text-gray-500 dark:text-gray-400">10:42 AM</div>
</td>
<td class="p-4 text-center">
<button class="p-2 rounded-full hover:bg-red-50 text-gray-400 hover:text-red-500 dark:hover:bg-red-900/20 dark:hover:text-red-400 transition-colors" title="Delete record">
<span class="material-symbols-outlined text-[20px]">delete</span>
</button>
</td>
</tr>
<tr class="group hover:bg-gray-50 dark:hover:bg-slate-800/50 transition-colors">
<td class="p-4 pl-6">
<div class="flex items-center gap-3">
<div class="w-10 h-10 rounded-full bg-blue-100 dark:bg-blue-900 text-blue-600 dark:text-blue-300 flex items-center justify-center font-bold text-sm flex-shrink-0">
                                BS
                            </div>
<div>
<div class="font-semibold text-gray-900 dark:text-white">Bob Smith</div>
<div class="text-xs text-text-muted-light dark:text-text-muted-dark">ID: 2023002</div>
</div>
</div>
</td>
<td class="p-4 text-center">
<div class="w-16 h-10 mx-auto border border-gray-200 dark:border-slate-600 rounded-lg flex items-center justify-center font-semibold text-gray-900 dark:text-white bg-white dark:bg-slate-900">
                            85
                        </div>
</td>
<td class="p-4 text-center">
<span class="inline-flex items-center gap-1.5 px-2.5 py-1 rounded-full text-xs font-medium bg-amber-100 dark:bg-amber-900/30 text-amber-700 dark:text-amber-300">
<span class="w-1.5 h-1.5 rounded-full bg-amber-500"></span>
                            Unread
                        </span>
</td>
<td class="p-4 text-right pr-6">
<div class="text-xs font-medium text-gray-900 dark:text-gray-200">Oct 23, 2023</div>
<div class="text-[10px] text-gray-500 dark:text-gray-400">4:15 PM</div>
</td>
<td class="p-4 text-center">
<button class="p-2 rounded-full hover:bg-red-50 text-gray-400 hover:text-red-500 dark:hover:bg-red-900/20 dark:hover:text-red-400 transition-colors" title="Delete record">
<span class="material-symbols-outlined text-[20px]">delete</span>
</button>
</td>
</tr>
<tr class="bg-sky-50/50 dark:bg-sky-900/10 border-l-4 border-l-sky-500">
<td class="p-4 pl-6">
<div class="flex items-center gap-3">
<div class="w-10 h-10 rounded-full overflow-hidden flex-shrink-0 border-2 border-sky-100 dark:border-sky-800">
<img alt="Charlie Brown" class="w-full h-full object-contain bg-amber-50" src="https://lh3.googleusercontent.com/aida-public/AB6AXuBN0g-WHePpThTNMUhPAiYyolESpOvQwcvWsK86MgulRv8D3VHb3aOZJJV34TDq1T4OcXDsgb6hyBSaJgeedYQwQwGhlcX-dZLSF70FjunbM15RLBTgJk3IrodQswRdAM_26LPuhmB4M-ws_MQE4UJs0SAB2qtD755nqywNpp8Si9MBghBdT_dCxzvYrd4sml8IgvIY2OL0tul0_FlLUpiL_6M6-mrIyurLIqDHaFVTN6X8edP6SRuHWUQx5YPNnZJDocL6xbwJwA"/>
</div>
<div>
<div class="font-semibold text-gray-900 dark:text-white">Charlie Brown</div>
<div class="text-xs text-text-muted-light dark:text-text-muted-dark">ID: 2023003</div>
</div>
</div>
</td>
<td class="p-4 text-center">
<div class="relative w-20 mx-auto">
<div class="h-10 border-2 border-sky-500 rounded-lg flex items-center justify-between px-2 bg-white dark:bg-slate-900 shadow-sm ring-4 ring-sky-100 dark:ring-sky-900/20">
<span class="font-semibold text-gray-500 dark:text-gray-400">--</span>
<div class="flex flex-col -mr-1">
<span class="material-symbols-outlined text-[10px] text-gray-400 hover:text-sky-500 cursor-pointer leading-none">expand_less</span>
<span class="material-symbols-outlined text-[10px] text-gray-400 hover:text-sky-500 cursor-pointer leading-none">expand_more</span>
</div>
</div>
</div>
</td>
<td class="p-4 text-center">
<span class="inline-flex items-center px-2.5 py-1 rounded-full text-xs font-medium bg-slate-100 dark:bg-slate-700 text-slate-600 dark:text-slate-300">
                            Pending
                        </span>
</td>
<td class="p-4 text-right pr-6">
<div class="flex items-center justify-end text-sky-600 text-xs font-medium animate-pulse">
<span class="material-symbols-outlined text-sm mr-1">edit</span>
                            Editing now...
                        </div>
</td>
<td class="p-4 text-center">
<button class="p-2 rounded-full hover:bg-red-50 text-gray-400 hover:text-red-500 dark:hover:bg-red-900/20 dark:hover:text-red-400 transition-colors" title="Delete record">
<span class="material-symbols-outlined text-[20px]">delete</span>
</button>
</td>
</tr>
<tr class="group hover:bg-gray-50 dark:hover:bg-slate-800/50 transition-colors">
<td class="p-4 pl-6">
<div class="flex items-center gap-3">
<div class="w-10 h-10 rounded-full bg-pink-100 dark:bg-pink-900 text-pink-600 dark:text-pink-300 flex items-center justify-center font-bold text-sm flex-shrink-0">
                                DW
                            </div>
<div>
<div class="font-semibold text-gray-900 dark:text-white">Daisy Wong</div>
<div class="text-xs text-text-muted-light dark:text-text-muted-dark">ID: 2023004</div>
</div>
</div>
</td>
<td class="p-4 text-center">
<div class="w-16 h-10 mx-auto border border-gray-200 dark:border-slate-600 rounded-lg flex items-center justify-center font-semibold text-gray-900 dark:text-white bg-white dark:bg-slate-900">
                            78
                        </div>
</td>
<td class="p-4 text-center">
<span class="inline-flex items-center gap-1.5 px-2.5 py-1 rounded-full text-xs font-medium bg-sky-100 dark:bg-sky-900/30 text-sky-700 dark:text-sky-300">
<span class="w-1.5 h-1.5 rounded-full bg-sky-500"></span>
                            Read
                        </span>
</td>
<td class="p-4 text-right pr-6">
<div class="text-xs font-medium text-gray-900 dark:text-gray-200">Oct 20, 2023</div>
<div class="text-[10px] text-gray-500 dark:text-gray-400">11:00 AM</div>
</td>
<td class="p-4 text-center">
<button class="p-2 rounded-full hover:bg-red-50 text-gray-400 hover:text-red-500 dark:hover:bg-red-900/20 dark:hover:text-red-400 transition-colors" title="Delete record">
<span class="material-symbols-outlined text-[20px]">delete</span>
</button>
</td>
</tr>
<tr class="group hover:bg-gray-50 dark:hover:bg-slate-800/50 transition-colors">
<td class="p-4 pl-6">
<div class="flex items-center gap-3">
<div class="w-10 h-10 rounded-full overflow-hidden flex-shrink-0">
<img alt="Evan Lee" class="w-full h-full object-cover" src="https://lh3.googleusercontent.com/aida-public/AB6AXuAOq5HIJrHhf31413-hbBg16dhLQOUngJZZhzPEXKub1u8NDLyzOpPeGQMUmYSlXk-4lPjAgrF1HhfEkYSXW8VvyL1ZjQJdBJmuSTAP27pFTTwzSD2a1M0CDqZUC54Mu8M9Y4OqxWhphFcgjoWwhUyBlnXYhEBnL0P4oNp84OIEzpB4e9sEDWos5bPJSrzNrpw__Jb3KaGwHYT1AQau6R2sbUKS0RxojV6vxXSOt-IA_xIOf9iLdzWyxWxcQMGNCE2_QIEavwcWRA"/>
</div>
<div>
<div class="font-semibold text-gray-900 dark:text-white">Evan Lee</div>
<div class="text-xs text-text-muted-light dark:text-text-muted-dark">ID: 2023005</div>
</div>
</div>
</td>
<td class="p-4 text-center">
<div class="w-16 h-10 mx-auto border border-gray-200 dark:border-slate-600 rounded-lg flex items-center justify-center font-semibold text-gray-400 dark:text-gray-500 bg-white dark:bg-slate-900">
                            --
                        </div>
</td>
<td class="p-4 text-center">
<span class="inline-flex items-center gap-1.5 px-2.5 py-1 rounded-full text-xs font-medium bg-amber-100 dark:bg-amber-900/30 text-amber-700 dark:text-amber-300">
<span class="w-1.5 h-1.5 rounded-full bg-amber-500"></span>
                            Unread
                        </span>
</td>
<td class="p-4 text-right pr-6">
<div class="text-xs font-medium text-gray-400 dark:text-gray-500">--</div>
</td>
<td class="p-4 text-center">
<button class="p-2 rounded-full hover:bg-red-50 text-gray-400 hover:text-red-500 dark:hover:bg-red-900/20 dark:hover:text-red-400 transition-colors" title="Delete record">
<span class="material-symbols-outlined text-[20px]">delete</span>
</button>
</td>
</tr>
</tbody>
</table>
</div>
<div class="bg-gray-50 dark:bg-slate-800/50 border-t border-border-light dark:border-border-dark p-4 flex flex-col sm:flex-row items-center justify-between gap-4">
<div class="text-sm text-text-muted-light dark:text-text-muted-dark">
                Showing <span class="font-semibold text-gray-900 dark:text-white">1</span> to <span class="font-semibold text-gray-900 dark:text-white">5</span> of <span class="font-semibold text-gray-900 dark:text-white">34</span> students
            </div>
<nav class="flex items-center gap-1">
<button class="px-3 py-1 text-sm font-medium text-gray-500 dark:text-gray-400 bg-white dark:bg-slate-800 border border-gray-300 dark:border-slate-600 rounded-md hover:bg-gray-50 dark:hover:bg-slate-700 disabled:opacity-50">Previous</button>
<button class="w-8 h-8 flex items-center justify-center text-sm font-medium bg-sky-500 text-white rounded-md">1</button>
<button class="w-8 h-8 flex items-center justify-center text-sm font-medium text-gray-700 dark:text-gray-200 hover:bg-gray-100 dark:hover:bg-slate-700 rounded-md">2</button>
<button class="w-8 h-8 flex items-center justify-center text-sm font-medium text-gray-700 dark:text-gray-200 hover:bg-gray-100 dark:hover:bg-slate-700 rounded-md">3</button>
<span class="w-8 h-8 flex items-center justify-center text-sm text-gray-400 dark:text-gray-500">...</span>
<button class="w-8 h-8 flex items-center justify-center text-sm font-medium text-gray-700 dark:text-gray-200 hover:bg-gray-100 dark:hover:bg-slate-700 rounded-md">7</button>
<button class="px-3 py-1 text-sm font-medium text-gray-500 dark:text-gray-400 bg-white dark:bg-slate-800 border border-gray-300 dark:border-slate-600 rounded-md hover:bg-gray-50 dark:hover:bg-slate-700">Next</button>
</nav>
</div>
</div>
</main>
<button class="fixed bottom-6 right-6 w-12 h-12 bg-white dark:bg-slate-800 border border-gray-200 dark:border-slate-600 rounded-full shadow-lg flex items-center justify-center text-slate-700 dark:text-yellow-400 hover:scale-105 transition-transform z-50" id="theme-toggle">
<span class="material-symbols-outlined text-xl dark:hidden">dark_mode</span>
<span class="material-symbols-outlined text-xl hidden dark:block">light_mode</span>
</button>
</div>
</template>




<script>
export default {
  name: "Grade",
mounted() {
    const themeToggleBtn = document.getElementById('theme-toggle');
    const html = document.documentElement;
    // Check local storage or system preference
    if (localStorage.theme === 'dark' || (!('theme' in localStorage) && window.matchMedia('(prefers-color-scheme: dark)').matches)) {
        html.classList.add('dark');
    } else {
        html.classList.remove('dark');
    }
    themeToggleBtn.addEventListener('click', () => {
        html.classList.toggle('dark');
        if (html.classList.contains('dark')) {
            localStorage.theme = 'dark';
        } else {
            localStorage.theme = 'light';
        }
    });
}
}
</script>
