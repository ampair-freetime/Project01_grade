<template>
<div class="bg-mint-soft dark:bg-background-dark text-[#111811] dark:text-white h-screen flex flex-col overflow-hidden">
<header class="bg-white dark:bg-[#1a232e] border-b border-[#e0e7eb] dark:border-[#2a363e] h-16 shrink-0 z-30">
<div class="max-w-7xl mx-auto px-4 h-full flex items-center justify-between">
<div class="flex items-center gap-2">
<div class="size-8 rounded-lg bg-primary/20 flex items-center justify-center text-primary">
<span class="material-symbols-outlined icon-filled">school</span>
</div>
<div class="flex flex-col">
<h1 class="text-[#111811] dark:text-white text-lg font-bold leading-tight">UniPortal</h1>
<p class="text-[#637888] dark:text-[#a0b8cf] text-xs font-normal">Student Dashboard</p>
</div>
</div>
<div class="flex items-center gap-6">
<nav class="hidden md:flex items-center gap-1">
<a class="flex items-center gap-2 px-3 py-2 rounded-lg bg-[#f0f4f8] dark:bg-[#253038] transition-colors group" href="#">
<span class="material-symbols-outlined text-[#111811] dark:text-white icon-filled text-[20px]">dashboard</span>
<p class="text-[#111811] dark:text-white text-sm font-medium">Overview</p>
</a>
</nav>
<div class="h-6 w-px bg-[#e0e7eb] dark:bg-[#2a363e] hidden md:block"></div>
<div class="flex items-center gap-3">
<div class="hidden sm:flex flex-col items-end">
<p class="text-sm font-medium text-[#111811] dark:text-white">Alex Student</p>
<p class="text-xs text-[#637888] dark:text-[#a0b8cf]">ID: 2024001</p>
</div>
<div class="relative rounded-full size-10 overflow-hidden shrink-0 border-2 border-primary/30 cursor-pointer hover:border-primary transition-colors">
<img alt="Portrait of student Alex smiling" class="w-full h-full object-cover" data-alt="Portrait of student Alex smiling" src="https://lh3.googleusercontent.com/aida-public/AB6AXuA2v_m2Fz1ch3NPLGzH9eMaoTV-93B4acKLrUPvM_rqxKrQYk5kbjKKMAfrFmtw5FGyzSD1KMH2a-VWjuWrPGK8ZlbPavlIIJuvuAzDbZMQGWe1jn0AQQ4ERw-WfWdu46hkD0G6xrSczReJZhozEyi8hZFyyQRv8-mgZ8VsbXRgnwsS2Iid9RIfNLhbVCqbfPuqjYUwPsIMmYxnNyuuFPckvZ7uBDRGVTE2avJ2C_oHiWeCQCTJ1XKfOkWyaIz7RJfgT2bZSBQJWg"/>
</div>
<a class="flex items-center justify-center size-10 rounded-full hover:bg-red-50 dark:hover:bg-red-900/20 text-[#637888] dark:text-[#a0b8cf] hover:text-red-600 dark:hover:text-red-400 transition-colors" href="#" title="Log Out">
<span class="material-symbols-outlined text-[20px]">logout</span>
</a>
</div>
</div>
</div>
</header>
<main class="flex-1 flex flex-col h-full overflow-hidden relative">
<div class="absolute top-0 left-0 w-full h-32 bg-gradient-to-b from-blue-50/40 to-transparent pointer-events-none"></div>
<div class="flex-1 overflow-y-auto p-8 lg:p-12">
<div class="max-w-5xl mx-auto flex flex-col gap-8">
<header class="flex flex-col md:flex-row md:items-end justify-between gap-6">
<div class="flex flex-col gap-2">
<h2 class="text-[#111811] dark:text-white text-3xl md:text-4xl font-bold tracking-tight">Hello, Alex</h2>
<p class="text-[#4e5b6b] dark:text-[#a0b8cf] text-base font-normal">Here are your courses for the Spring 2024 semester.</p>
</div>
<div class="w-full md:w-96">
<label class="flex w-full items-center h-12 rounded-lg bg-white dark:bg-[#1a232e] shadow-sm ring-1 ring-[#e0e7eb] dark:ring-[#2a363e] focus-within:ring-2 focus-within:ring-primary overflow-hidden transition-shadow">
<div class="flex items-center justify-center pl-4 pr-2 text-[#637888] dark:text-[#a0b8cf]">
<span class="material-symbols-outlined">search</span>
</div>
<input class="w-full bg-transparent border-none text-[#111811] dark:text-white placeholder:text-[#637888]/70 focus:ring-0 focus:outline-none text-base h-full" placeholder="Search courses..."/>
</label>
</div>
</header>
<section class="flex flex-col gap-4">
<div class="flex items-center justify-between mb-2">
<h3 class="text-lg font-semibold text-[#111811] dark:text-white flex items-center gap-2">
                            Current Enrolled Courses
                            <span class="bg-[#e0e7eb] dark:bg-[#253038] text-[#4e5b6b] dark:text-[#a0b8cf] text-xs px-2 py-0.5 rounded-full">5</span>
</h3>
<div class="flex items-center gap-2 text-sm text-[#4e5b6b] cursor-pointer hover:text-[#111811] dark:hover:text-white transition-colors">
<span class="material-symbols-outlined text-[18px]">sort</span>
                            Sort by recent
                        </div>
</div>
<div class="group bg-white dark:bg-[#1a232e] p-4 rounded-xl shadow-sm border border-transparent hover:border-primary/40 hover:shadow-md transition-all duration-200 cursor-pointer">
<div class="flex items-center justify-between gap-4">
<div class="flex items-center gap-5 overflow-hidden">
<div class="shrink-0 size-14 rounded-xl bg-gradient-to-br from-[#f0f4f8] to-[#e8f1f5] dark:from-[#253038] dark:to-[#1f2633] flex items-center justify-center text-[#111811] dark:text-white group-hover:scale-105 transition-transform">
<span class="material-symbols-outlined text-3xl">terminal</span>
</div>
<div class="flex flex-col min-w-0">
<div class="flex items-center gap-2 mb-0.5">
<span class="font-mono text-xs font-bold text-[#637888] dark:text-[#a0b8cf] bg-[#f0f4f8] dark:bg-[#253038] px-1.5 py-0.5 rounded">CS101</span>
<span class="size-2 rounded-full bg-primary animate-pulse shadow-[0_0_8px_#30a0e8]"></span>
<span class="text-[10px] font-bold tracking-wider text-primary uppercase">New Grade</span>
</div>
<h4 class="text-[#111811] dark:text-white text-lg font-semibold truncate group-hover:text-primary transition-colors">Introduction to Computer Science</h4>
<p class="text-[#637888] dark:text-[#a0b8cf] text-sm">Spring 2024 • Prof. Alan Turing</p>
</div>
</div>
<div class="shrink-0 flex items-center justify-center size-10 rounded-full bg-[#f6f8fa] dark:bg-[#253038] text-[#111811] dark:text-white group-hover:bg-primary group-hover:text-white transition-colors">
<span class="material-symbols-outlined">arrow_forward</span>
</div>
</div>
</div>
<div class="group bg-white dark:bg-[#1a232e] p-4 rounded-xl shadow-sm border border-transparent hover:border-primary/40 hover:shadow-md transition-all duration-200 cursor-pointer">
<div class="flex items-center justify-between gap-4">
<div class="flex items-center gap-5 overflow-hidden">
<div class="shrink-0 size-14 rounded-xl bg-gradient-to-br from-[#f0f4f8] to-[#e8f1f5] dark:from-[#253038] dark:to-[#1f2633] flex items-center justify-center text-[#111811] dark:text-white group-hover:scale-105 transition-transform">
<span class="material-symbols-outlined text-3xl">biotech</span>
</div>
<div class="flex flex-col min-w-0">
<div class="flex items-center gap-2 mb-0.5">
<span class="font-mono text-xs font-bold text-[#637888] dark:text-[#a0b8cf] bg-[#f0f4f8] dark:bg-[#253038] px-1.5 py-0.5 rounded">BIO101</span>
</div>
<h4 class="text-[#111811] dark:text-white text-lg font-semibold truncate group-hover:text-primary transition-colors">General Biology I</h4>
<p class="text-[#637888] dark:text-[#a0b8cf] text-sm">Spring 2024 • Prof. Rosalind Franklin</p>
</div>
</div>
<div class="shrink-0 flex items-center justify-center size-10 rounded-full bg-[#f6f8fa] dark:bg-[#253038] text-[#111811] dark:text-white group-hover:bg-primary group-hover:text-white transition-colors">
<span class="material-symbols-outlined">arrow_forward</span>
</div>
</div>
</div>
<div class="group bg-white dark:bg-[#1a232e] p-4 rounded-xl shadow-sm border border-transparent hover:border-primary/40 hover:shadow-md transition-all duration-200 cursor-pointer">
<div class="flex items-center justify-between gap-4">
<div class="flex items-center gap-5 overflow-hidden">
<div class="shrink-0 size-14 rounded-xl bg-gradient-to-br from-[#f0f4f8] to-[#e8f1f5] dark:from-[#253038] dark:to-[#1f2633] flex items-center justify-center text-[#111811] dark:text-white group-hover:scale-105 transition-transform">
<span class="material-symbols-outlined text-3xl">functions</span>
</div>
<div class="flex flex-col min-w-0">
<div class="flex items-center gap-2 mb-0.5">
<span class="font-mono text-xs font-bold text-[#637888] dark:text-[#a0b8cf] bg-[#f0f4f8] dark:bg-[#253038] px-1.5 py-0.5 rounded">MATH202</span>
</div>
<h4 class="text-[#111811] dark:text-white text-lg font-semibold truncate group-hover:text-primary transition-colors">Calculus II</h4>
<p class="text-[#637888] dark:text-[#a0b8cf] text-sm">Spring 2024 • Prof. Katherine Johnson</p>
</div>
</div>
<div class="shrink-0 flex items-center justify-center size-10 rounded-full bg-[#f6f8fa] dark:bg-[#253038] text-[#111811] dark:text-white group-hover:bg-primary group-hover:text-white transition-colors">
<span class="material-symbols-outlined">arrow_forward</span>
</div>
</div>
</div>
<div class="group bg-white dark:bg-[#1a232e] p-4 rounded-xl shadow-sm border border-transparent hover:border-primary/40 hover:shadow-md transition-all duration-200 cursor-pointer">
<div class="flex items-center justify-between gap-4">
<div class="flex items-center gap-5 overflow-hidden">
<div class="shrink-0 size-14 rounded-xl bg-gradient-to-br from-[#f0f4f8] to-[#e8f1f5] dark:from-[#253038] dark:to-[#1f2633] flex items-center justify-center text-[#111811] dark:text-white group-hover:scale-105 transition-transform">
<span class="material-symbols-outlined text-3xl">auto_stories</span>
</div>
<div class="flex flex-col min-w-0">
<div class="flex items-center gap-2 mb-0.5">
<span class="font-mono text-xs font-bold text-[#637888] dark:text-[#a0b8cf] bg-[#f0f4f8] dark:bg-[#253038] px-1.5 py-0.5 rounded">ENG105</span>
<span class="size-2 rounded-full bg-primary animate-pulse shadow-[0_0_8px_#30a0e8]"></span>
<span class="text-[10px] font-bold tracking-wider text-primary uppercase">New Grade</span>
</div>
<h4 class="text-[#111811] dark:text-white text-lg font-semibold truncate group-hover:text-primary transition-colors">Academic Writing</h4>
<p class="text-[#637888] dark:text-[#a0b8cf] text-sm">Spring 2024 • Prof. Maya Angelou</p>
</div>
</div>
<div class="shrink-0 flex items-center justify-center size-10 rounded-full bg-[#f6f8fa] dark:bg-[#253038] text-[#111811] dark:text-white group-hover:bg-primary group-hover:text-white transition-colors">
<span class="material-symbols-outlined">arrow_forward</span>
</div>
</div>
</div>
<div class="group bg-white dark:bg-[#1a232e] p-4 rounded-xl shadow-sm border border-transparent hover:border-primary/40 hover:shadow-md transition-all duration-200 cursor-pointer">
<div class="flex items-center justify-between gap-4">
<div class="flex items-center gap-5 overflow-hidden">
<div class="shrink-0 size-14 rounded-xl bg-gradient-to-br from-[#f0f4f8] to-[#e8f1f5] dark:from-[#253038] dark:to-[#1f2633] flex items-center justify-center text-[#111811] dark:text-white group-hover:scale-105 transition-transform">
<span class="material-symbols-outlined text-3xl">history_edu</span>
</div>
<div class="flex flex-col min-w-0">
<div class="flex items-center gap-2 mb-0.5">
<span class="font-mono text-xs font-bold text-[#637888] dark:text-[#a0b8cf] bg-[#f0f4f8] dark:bg-[#253038] px-1.5 py-0.5 rounded">HIST300</span>
</div>
<h4 class="text-[#111811] dark:text-white text-lg font-semibold truncate group-hover:text-primary transition-colors">World History</h4>
<p class="text-[#637888] dark:text-[#a0b8cf] text-sm">Spring 2024 • Prof. Howard Zinn</p>
</div>
</div>
<div class="shrink-0 flex items-center justify-center size-10 rounded-full bg-[#f6f8fa] dark:bg-[#253038] text-[#111811] dark:text-white group-hover:bg-primary group-hover:text-white transition-colors">
<span class="material-symbols-outlined">arrow_forward</span>
</div>
</div>
</div>
</section>
</div>
</div>
</main>
</div>
</template>

<script>
export default {
  name: "Dashboard"
}
</script>
