<template>
  <div
    class="bg-background-light dark:bg-background-dark text-[#111811] dark:text-[#f0f4f0] font-display min-h-screen flex flex-col overflow-x-hidden transition-colors duration-200"
  >
    <header
      class="sticky top-0 z-50 bg-surface-light dark:bg-surface-dark border-b border-border-light dark:border-border-dark px-4 md:px-10 py-3"
    >
      <div
        class="layout-content-container max-w-[1200px] mx-auto flex items-center justify-between whitespace-nowrap"
      >
        <div class="flex items-center gap-4 md:gap-8">
          <div class="flex items-center gap-3 text-[#111811] dark:text-white">
            <div class="size-8 text-primary">
              <svg
                class="w-full h-full"
                fill="none"
                viewBox="0 0 48 48"
                xmlns="http://www.w3.org/2000/svg"
              >
                <path
                  d="M13.8261 17.4264C16.7203 18.1174 20.2244 18.5217 24 18.5217C27.7756 18.5217 31.2797 18.1174 34.1739 17.4264C36.9144 16.7722 39.9967 15.2331 41.3563 14.1648L24.8486 40.6391C24.4571 41.267 23.5429 41.267 23.1514 40.6391L6.64374 14.1648C8.00331 15.2331 11.0856 16.7722 13.8261 17.4264Z"
                  fill="currentColor"
                ></path>
                <path
                  clip-rule="evenodd"
                  d="M39.998 12.236C39.9944 12.2537 39.9875 12.2845 39.9748 12.3294C39.9436 12.4399 39.8949 12.5741 39.8346 12.7175C39.8168 12.7597 39.7989 12.8007 39.7813 12.8398C38.5103 13.7113 35.9788 14.9393 33.7095 15.4811C30.9875 16.131 27.6413 16.5217 24 16.5217C20.3587 16.5217 17.0125 16.131 14.2905 15.4811C12.0012 14.9346 9.44505 13.6897 8.18538 12.8168C8.17384 12.7925 8.16216 12.767 8.15052 12.7408C8.09919 12.6249 8.05721 12.5114 8.02977 12.411C8.00356 12.3152 8.00039 12.2667 8.00004 12.2612C8.00004 12.261 8 12.2607 8.00004 12.2612C8.00004 12.2359 8.0104 11.9233 8.68485 11.3686C9.34546 10.8254 10.4222 10.2469 11.9291 9.72276C14.9242 8.68098 19.1919 8 24 8C28.8081 8 33.0758 8.68098 36.0709 9.72276C37.5778 10.2469 38.6545 10.8254 39.3151 11.3686C39.9006 11.8501 39.9857 12.1489 39.998 12.236ZM4.95178 15.2312L21.4543 41.6973C22.6288 43.5809 25.3712 43.5809 26.5457 41.6973L43.0534 15.223C43.0709 15.1948 43.0878 15.1662 43.104 15.1371L41.3563 14.1648C43.104 15.1371 43.1038 15.1374 43.104 15.1371L43.1051 15.135L43.1065 15.1325L43.1101 15.1261L43.1199 15.1082C43.1276 15.094 43.1377 15.0754 43.1497 15.0527C43.1738 15.0075 43.2062 14.9455 43.244 14.8701C43.319 14.7208 43.4196 14.511 43.5217 14.2683C43.6901 13.8679 44 13.0689 44 12.2609C44 10.5573 43.003 9.22254 41.8558 8.2791C40.6947 7.32427 39.1354 6.55361 37.385 5.94477C33.8654 4.72057 29.133 4 24 4C18.867 4 14.1346 4.72057 10.615 5.94478C8.86463 6.55361 7.30529 7.32428 6.14419 8.27911C4.99695 9.22255 3.99999 10.5573 3.99999 12.2609C3.99999 13.1275 4.29264 13.9078 4.49321 14.3607C4.60375 14.6102 4.71348 14.8196 4.79687 14.9689C4.83898 15.0444 4.87547 15.1065 4.9035 15.1529C4.91754 15.1762 4.92954 15.1957 4.93916 15.2111L4.94662 15.223L4.95178 15.2312ZM35.9868 18.996L24 38.22L12.0131 18.996C12.4661 19.1391 12.9179 19.2658 13.3617 19.3718C16.4281 20.1039 20.0901 20.5217 24 20.5217C27.9099 20.5217 31.5719 20.1039 34.6383 19.3718C35.082 19.2658 35.5339 19.1391 35.9868 18.996Z"
                  fill="currentColor"
                  fill-rule="evenodd"
                ></path>
              </svg>
            </div>
            <h2 class="text-lg font-bold leading-tight tracking-[-0.015em]">
              UniGrades
            </h2>
          </div>
          <nav class="hidden md:flex items-center gap-9">
            <a class="text-primary text-sm font-bold" href="#">Courses</a>
          </nav>
        </div>
        <div class="flex flex-1 justify-end gap-6 items-center">
          <label class="hidden sm:flex flex-col min-w-40 !h-10 max-w-64">
            <div
              class="flex w-full flex-1 items-stretch rounded-lg h-full border border-transparent focus-within:border-primary transition-colors"
            >
              <div
                class="text-[#638863] dark:text-[#8ba38b] flex bg-[#f0f4f8] dark:bg-[#1a232c] items-center justify-center pl-4 rounded-l-lg"
              >
                <span class="material-symbols-outlined text-[20px]"
                  >search</span
                >
              </div>
              <input
                class="form-input flex w-full min-w-0 flex-1 resize-none overflow-hidden rounded-lg text-[#111811] dark:text-white focus:outline-0 focus:ring-0 border-none bg-[#f0f4f8] dark:bg-[#1a232c] h-full placeholder:text-[#638863] px-4 rounded-l-none pl-2 text-sm font-normal"
                placeholder="Search assignment"
              />
            </div>
          </label>
          <div class="flex items-center gap-4">
            <div
              class="bg-center bg-no-repeat bg-cover rounded-full size-10 border-2 border-primary cursor-pointer hover:opacity-80 transition-opacity"
              data-alt="User profile picture showing a smiling student"
              style="
                background-image: url(&quot;https://lh3.googleusercontent.com/aida-public/AB6AXuB96ALsGJ226_L-iLmyNv9G9s5TWl6LqhYTURsbcOFNdzhfLdT6L9fYPWEDkqs4WN4blGQPigSfUUCEyiCb9rbPa_bZj8sU2IbEOZ5vITk9iHCSoJNC2A5Kj5yDF16t6rQReTOecAbav_TWJPGaDPr5WahJi8xmHe8vXzFEY7fwVw2agrrMHwobOgCDwSjCGQpMbNy3VKxtOLZ416ddQCulxxEBu2mJbSX780NEyKUR89mtuX_rAu4UhJyepC7EO0POMGtLEBZXDQ&quot;);
              "
            ></div>
            <form @submit.prevent="handleLogout">
              <button
              class="flex items-center justify-center text-[#638863] dark:text-[#8ba38b] hover:text-primary transition-colors">
              <span class="material-symbols-outlined text-[24px]">logout</span>
            </button>
          </form>
          </div>
        </div>
      </div>
    </header>
    <main
      class="flex-1 layout-container flex flex-col items-center py-5 md:py-8 px-4 md:px-10"
    >
      <div
        class="layout-content-container flex flex-col max-w-[1000px] w-full gap-8"
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
            <span>Return to Courses</span>
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
              <div class="flex flex-col gap-2">
                <div class="flex items-center gap-2">
                  <span
                    class="bg-primary/20 text-primary-content dark:text-primary px-2 py-0.5 rounded text-xs font-bold uppercase tracking-wider"
                    >Active</span
                  >
                  <span
                    class="text-[#638863] dark:text-[#8ba38b] text-sm font-medium"
                    >Fall 2023</span
                  >
                </div>
                <h1
                  class="text-[#111811] dark:text-white text-3xl md:text-4xl font-black leading-tight tracking-[-0.033em]"
                >
                  CS101: Intro to Algorithms
                </h1>
                <div
                  class="flex items-center gap-2 text-[#638863] dark:text-[#8ba38b] mt-1"
                >
                  <span class="material-symbols-outlined text-[20px]"
                    >school</span
                  >
                  <p class="text-base font-normal">
                    Instructor: Dr. Sarah Bennett
                  </p>
                </div>
              </div>
              <div class="flex gap-4 mt-4">
                <button
                  class="flex items-center justify-center gap-2 bg-[#f0f4f8] dark:bg-[#2a3440] hover:bg-[#e0e4e8] text-[#111811] dark:text-white font-semibold px-6 py-2.5 rounded-lg transition-colors"
                >
                  <span class="material-symbols-outlined text-[20px]"
                    >mail</span
                  >
                  <span>Contact</span>
                </button>
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
            <div class="text-sm text-[#638863] dark:text-[#8ba38b]">
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
                      class="p-4 text-xs font-bold text-[#638863] dark:text-[#8ba38b] uppercase tracking-wider"
                    >
                      Assessment
                    </th>
                    <th
                      class="p-4 text-xs font-bold text-[#638863] dark:text-[#8ba38b] uppercase tracking-wider w-24 text-center"
                    >
                      Weight
                    </th>
                    <th
                      class="p-4 text-xs font-bold text-[#638863] dark:text-[#8ba38b] uppercase tracking-wider w-28 text-center"
                    >
                      Status
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
                      <div class="text-xs text-[#638863] dark:text-[#8ba38b]">
                        Algorithm Implementation
                      </div>
                    </td>
                    <td class="p-4 text-center font-medium">40%</td>
                    <td class="p-4 text-center">
                      <span
                        class="inline-flex items-center justify-center gap-1.5 px-2.5 py-1 rounded-full text-xs font-bold bg-[#f0f9ff] text-[#0369a1] dark:bg-[#0c4a6e] dark:text-[#38bdf8] border border-[#e0f2fe] dark:border-[#075985]"
                      >
                        <span
                          class="w-1.5 h-1.5 rounded-full bg-[#0ea5e9] dark:bg-[#38bdf8]"
                        ></span>
                        Read
                      </span>
                    </td>
                  </tr>
                  <tr
                    class="hover:bg-[#fcfdfc] dark:hover:bg-[#1f2832] transition-colors group"
                  >
                    <td class="p-4">
                      <div class="font-bold text-[#111811] dark:text-white">
                        Midterm Exam
                      </div>
                      <div class="text-xs text-[#638863] dark:text-[#8ba38b]">
                        In-class written exam
                      </div>
                    </td>
                    <td class="p-4 text-center font-medium">30%</td>
                    <td class="p-4 text-center">
                      <span
                        class="inline-flex items-center justify-center gap-1.5 px-2.5 py-1 rounded-full text-xs font-bold bg-[#f0f9ff] text-[#0369a1] dark:bg-[#0c4a6e] dark:text-[#38bdf8] border border-[#e0f2fe] dark:border-[#075985]"
                      >
                        <span
                          class="w-1.5 h-1.5 rounded-full bg-[#0ea5e9] dark:bg-[#38bdf8]"
                        ></span>
                        Read
                      </span>
                    </td>
                  </tr>
                  <tr
                    class="hover:bg-[#fcfdfc] dark:hover:bg-[#1f2832] transition-colors group"
                  >
                    <td class="p-4">
                      <div class="font-bold text-[#111811] dark:text-white">
                        Assignment 1
                      </div>
                      <div class="text-xs text-[#638863] dark:text-[#8ba38b]">
                        Introduction to Sorting
                      </div>
                    </td>
                    <td class="p-4 text-center font-medium">10%</td>
                    <td class="p-4 text-center">
                      <span
                        class="inline-flex items-center justify-center gap-1.5 px-2.5 py-1 rounded-full text-xs font-bold bg-[#fffbeb] text-[#b45309] dark:bg-[#78350f] dark:text-[#fcd34d] border border-[#fef3c7] dark:border-[#92400e]"
                      >
                        <span
                          class="w-1.5 h-1.5 rounded-full bg-[#d97706] dark:bg-[#fbbf24]"
                        ></span>
                        Unread
                      </span>
                    </td>
                  </tr>
                  <tr
                    class="hover:bg-[#fcfdfc] dark:hover:bg-[#1f2832] transition-colors group"
                  >
                    <td class="p-4">
                      <div class="font-bold text-[#111811] dark:text-white">
                        Assignment 2
                      </div>
                      <div class="text-xs text-[#638863] dark:text-[#8ba38b]">
                        Graph Theory
                      </div>
                    </td>
                    <td class="p-4 text-center font-medium">10%</td>
                    <td class="p-4 text-center">
                      <span
                        class="inline-flex items-center justify-center gap-1.5 px-2.5 py-1 rounded-full text-xs font-bold bg-[#f0f9ff] text-[#0369a1] dark:bg-[#0c4a6e] dark:text-[#38bdf8] border border-[#e0f2fe] dark:border-[#075985]"
                      >
                        <span
                          class="w-1.5 h-1.5 rounded-full bg-[#0ea5e9] dark:bg-[#38bdf8]"
                        ></span>
                        Read
                      </span>
                    </td>
                  </tr>
                  <tr
                    class="hover:bg-[#fcfdfc] dark:hover:bg-[#1f2832] transition-colors group"
                  >
                    <td class="p-4">
                      <div class="font-bold text-[#111811] dark:text-white">
                        Quiz: Week 5
                      </div>
                      <div class="text-xs text-[#638863] dark:text-[#8ba38b]">
                        Dynamic Programming
                      </div>
                    </td>
                    <td class="p-4 text-center font-medium">5%</td>
                    <td class="p-4 text-center">
                      <span
                        class="inline-flex items-center justify-center gap-1.5 px-2.5 py-1 rounded-full text-xs font-bold bg-[#fffbeb] text-[#b45309] dark:bg-[#78350f] dark:text-[#fcd34d] border border-[#fef3c7] dark:border-[#92400e]"
                      >
                        <span
                          class="w-1.5 h-1.5 rounded-full bg-[#d97706] dark:bg-[#fbbf24]"
                        ></span>
                        Unread
                      </span>
                    </td>
                  </tr>
                  <tr
                    class="hover:bg-[#fcfdfc] dark:hover:bg-[#1f2832] transition-colors group"
                  >
                    <td class="p-4">
                      <div class="font-bold text-[#111811] dark:text-white">
                        Participation
                      </div>
                      <div class="text-xs text-[#638863] dark:text-[#8ba38b]">
                        Overall attendance
                      </div>
                    </td>
                    <td class="p-4 text-center font-medium">5%</td>
                    <td class="p-4 text-center">
                      <span
                        class="inline-flex items-center justify-center gap-1.5 px-2.5 py-1 rounded-full text-xs font-bold bg-[#f0f9ff] text-[#0369a1] dark:bg-[#0c4a6e] dark:text-[#38bdf8] border border-[#e0f2fe] dark:border-[#075985]"
                      >
                        <span
                          class="w-1.5 h-1.5 rounded-full bg-[#0ea5e9] dark:bg-[#38bdf8]"
                        ></span>
                        Read
                      </span>
                    </td>
                  </tr>
                </tbody>
              </table>
            </div>
          </div>
        </section>
      </div>
    </main>
  </div>
</template>

<script setup>
  import { useRouter } from 'vue-router';
  const router = useRouter();
  name: "CourseDetail"
  const handleLogout = async () => {
    try{
      const response = await fetch('http://localhost:56733/logout',{
        method: 'GET',
        credentials: 'include'
      });
      if (response.ok) {
        localStorage.removeItem('csrf_token');
        localStorage.removeItem('role');

        router.push('/login');
      }
    } catch (error){
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
