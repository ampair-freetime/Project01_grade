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
      </div>
    </header>

    <!-- main -->
    <main
      class="flex-1 flex flex-col items-center justify-center p-4 sm:p-6 w-full"
    >
      <div class="layout-content-container flex flex-col w-full max-w-[480px]">
        <div
          class="bg-surface-light dark:bg-surface-dark rounded-2xl shadow-soft border border-border-color dark:border-[#0c4a6e] overflow-hidden relative"
        >
          <div
            class="absolute top-0 left-0 w-full h-1 bg-gradient-to-r from-primary/60 via-primary to-primary/60"
          ></div>
          <div class="pt-10 pb-6 px-8 text-center">
            <h1
              class="text-[#0f172a] dark:text-white tracking-tight text-[28px] sm:text-[32px] font-bold leading-tight mb-2"
            >
              Create Account
            </h1>
          </div>
          <form
            class="px-6 sm:px-8 pb-10 flex flex-col gap-5"
          >
            <div class="grid grid-cols-1 sm:grid-cols-2 gap-5">
              <div class="flex flex-col gap-1.5">
                <label
                  class="text-[#0f172a] dark:text-gray-200 text-sm font-semibold leading-normal ml-1"
                  >First Name</label
                >
                <div class="relative flex items-center group">
                  <div
                    class="absolute left-4 text-[#64748b] group-focus-within:text-primary transition-colors pointer-events-none flex items-center justify-center"
                  >
                    <span class="material-symbols-outlined">person</span>
                  </div>
                  <input
                    v-model="firstName"
                    class="form-input flex w-full min-w-0 flex-1 resize-none overflow-hidden rounded-lg text-text-main dark:text-white placeholder:text-[#64748b]/60 focus:outline-0 focus:ring-4 focus:ring-primary/10 border border-border-color dark:border-[#0c4a6e] bg-white dark:bg-[#0c4a6e] h-12 pl-11 pr-4 text-base font-normal leading-normal transition-all hover:border-primary/50 focus:border-primary"
                    placeholder="John"
                    type="text"
                  />
                </div>
              </div>
              <div class="flex flex-col gap-1.5">
                <label
                  class="text-[#0f172a] dark:text-gray-200 text-sm font-semibold leading-normal ml-1"
                  >Last Name</label
                >
                <div class="relative flex items-center group">
                  <div
                    class="absolute left-4 text-[#64748b] group-focus-within:text-primary transition-colors pointer-events-none flex items-center justify-center"
                  >
                    <span class="material-symbols-outlined">person</span>
                  </div>
                  <input
                    v-model="lastName"
                    class="form-input flex w-full min-w-0 flex-1 resize-none overflow-hidden rounded-lg text-text-main dark:text-white placeholder:text-[#64748b]/60 focus:outline-0 focus:ring-4 focus:ring-primary/10 border border-border-color dark:border-[#0c4a6e] bg-white dark:bg-[#0c4a6e] h-12 pl-11 pr-4 text-base font-normal leading-normal transition-all hover:border-primary/50 focus:border-primary"
                    placeholder="Doe"
                    type="text"
                  />
                </div>
              </div>
            </div>
            <div class="flex flex-col gap-1.5">
              <div class="flex justify-between items-center ml-1">
                <label
                  class="text-text-main dark:text-gray-200 text-sm font-semibold leading-normal"
                  >Middle Name</label
                >
                <span class="text-xs text-[#64748b] font-normal"
                  >(Optional)</span
                >
              </div>
              <div class="relative flex items-center group">
                <div
                  class="absolute left-4 text-[#64748b] group-focus-within:text-primary transition-colors pointer-events-none flex items-center justify-center"
                >
                  <span class="material-symbols-outlined">person</span>
                </div>
                <input
                  v-model="middleName"
                  class="form-input flex w-full min-w-0 flex-1 resize-none overflow-hidden rounded-lg text-text-main dark:text-white placeholder:text-[#64748b]/60 focus:outline-0 focus:ring-4 focus:ring-primary/10 border border-border-color dark:border-[#0c4a6e] bg-white dark:bg-[#0c4a6e] h-12 pl-11 pr-4 text-base font-normal leading-normal transition-all hover:border-primary/50 focus:border-primary"
                  placeholder="Quincy"
                  type="text"
                />
              </div>
            </div>
            <div class="flex flex-col gap-1.5">
              <label
                class="text-[#0f172a] dark:text-gray-200 text-sm font-semibold leading-normal ml-1"
                >Email</label
              >
              <div class="relative flex items-center group">
                <div
                  class="absolute left-4 text-[#64748b] group-focus-within:text-primary transition-colors pointer-events-none flex items-center justify-center"
                >
                  <span class="material-symbols-outlined">mail</span>
                </div>
                <input
                  v-model="email"
                  class="form-input flex w-full min-w-0 flex-1 resize-none overflow-hidden rounded-lg text-text-main dark:text-white placeholder:text-[#64748b]/60 focus:outline-0 focus:ring-4 focus:ring-primary/10 border border-border-color dark:border-[#0c4a6e] bg-white dark:bg-[#0c4a6e] h-12 pl-11 pr-4 text-base font-normal leading-normal transition-all hover:border-primary/50 focus:border-primary"
                  placeholder="example@cmu.ac.th"
                  type="email"
                />
              </div>
            </div>
            <div
              v-if="email.includes('_') && email.endsWith('@cmu.ac.th')"
              class="modal"
            >
              <div class="flex flex-col gap-1.5">
                <label
                  class="text-[#0f172a] dark:text-gray-200 text-sm font-semibold leading-normal ml-1"
                  >ID</label
                >
                <div class="relative flex items-center group">
                  <div
                    class="absolute left-4 text-[#64748b] group-focus-within:text-primary transition-colors pointer-events-none flex items-center justify-center"
                  >
                    <span class="material-symbols-outlined">badge</span>
                  </div>
                  <input
                    v-model="studentID"
                    required
                    class="form-input flex w-full min-w-0 flex-1 resize-none overflow-hidden rounded-lg text-text-main dark:text-white placeholder:text-[#64748b]/60 focus:outline-0 focus:ring-4 focus:ring-primary/10 border border-border-color dark:border-[#0c4a6e] bg-white dark:bg-[#0c4a6e] h-12 pl-11 pr-4 text-base font-normal leading-normal transition-all hover:border-primary/50 focus:border-primary"
                    placeholder="123456789"
                    type="text"
                  />
                </div>
              </div>
            </div>
            <div class="flex flex-col gap-1.5">
              <label
                class="text-text-main dark:text-gray-200 text-sm font-semibold leading-normal ml-1"
                >Password</label
              >
              <div class="relative flex items-center group">
                <div
                  class="absolute left-4 text-[#64748b] group-focus-within:text-primary transition-colors pointer-events-none flex items-center justify-center"
                >
                  <span class="material-symbols-outlined">lock</span>
                </div>
                <input
                  v-model="password"
                  class="form-input flex w-full min-w-0 flex-1 resize-none overflow-hidden rounded-lg text-text-main dark:text-white placeholder:text-[#64748b]/60 focus:outline-0 focus:ring-4 focus:ring-primary/10 border border-border-color dark:border-[#0c4a6e] bg-white dark:bg-[#0c4a6e] h-12 pl-11 pr-11 text-base font-normal leading-normal transition-all hover:border-primary/50 focus:border-primary"
                  placeholder="Create a strong password"
                  :type="showPassword ? 'text' : 'password'"
                />
                <button
                  aria-label="Toggle password visibility"
                  @click="togglePassword"
                  type="button"
                  class="absolute right-3 p-1.5 rounded-md flex items-center justify-center text-[#64748b] hover:bg-background-light dark:hover:bg-[#0c4a6e] hover:text-text-main dark:hover:text-white transition-colors cursor-pointer"
                >
                  <span class="material-symbols-outlined text-[20px]">
                    {{ showPassword ? "visibility_off" : "visibility" }}
                  </span>
                </button>
              </div>
            </div>
            <div class="flex flex-col gap-4 mt-2">
              <form @submit.prevent="handleSignup">
                <button
                  class="group relative w-full h-12 bg-primary hover:bg-primary-dark text-white text-base font-bold rounded-lg shadow-[0_2px_10px_rgba(56,189,248,0.2)] hover:shadow-glow hover:-translate-y-0.5 active:translate-y-0 transition-all duration-200 flex items-center justify-center gap-2 overflow-hidden"
                  type="submit"
                >
                  <span
                    class="absolute inset-0 bg-white/20 translate-y-full group-hover:translate-y-0 transition-transform duration-300 ease-out"
                  ></span>
                  <span
                    class="material-symbols-outlined relative z-10 group-hover:rotate-12 transition-transform duration-300"
                    >person_add</span
                  >
                  <span class="relative z-10">Sign Up</span>
                </button>
              </form>
              <div class="relative flex items-center justify-center w-full">
                <div class="absolute inset-0 flex items-center">
                  <div
                    class="w-full border-t border-border-color dark:border-[#0c4a6e]"
                  ></div>
                </div>
              </div>
            </div>
            <div class="text-center mt-2">
              <p class="text-sm text-[#64748b]">
                Already have an account?
                <router-link
                  to="/login"
                  class="font-bold text-sky-600 dark:text-sky-500 hover:text-sky-700 dark:hover:text-sky-400 transition-colors duration-200"
                >
                  Log in
                </router-link>
              </p>
            </div>
          </form>
        </div>
      </div>
    </main>
  </div>
</template>

<script setup>
import { ref } from "vue";
import { useRouter } from "vue-router";


defineOptions({
  name: "SignIn",
});

const router = useRouter();
const firstName = ref("");
const lastName = ref("");
const middleName = ref("");

const email = ref("");

const studentID = ref(null);
const password = ref("");
const showPassword = ref(false);

const isModalOpen = ref(false);


const togglePassword = () => {
  showPassword.value = !showPassword.value;
};

const handleSignup = async () => {
  try {

    if (!firstName.value ||!lastName.value ||!email.value || !password.value) {
      alert("ใส่ให้ครบจ้า");
      return;
    }

    // ถ้าเป็น student email มี_
    if (email.value.includes("_") && email.value.endsWith("@cmu.ac.th")) {
      if (!studentID.value) {
        alert("ใส่ Student ID ด้วยจ้า");
        return;
      }
    }

    // ถ้าเป็น teacher email (มี .)
    if (email.value.includes(".") && email.value.endsWith("@cmu.ac.th")) {
      studentID.value = null;
    }

    const response = await fetch("http://localhost:56733/register", {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
      },
      body: JSON.stringify({
        first_name: firstName.value,
        last_name: lastName.value,
        middle_name: middleName.value,
        email: email.value,
        student_id: studentID.value,
        password: password.value,
      }),
    });
    if (!response.ok) {
      alert("not complete");
      const errorData = await response.json();
      throw new Error(errorData.detail || "SignUp failed");
    }

    router.push("/login");
  } catch (error) {
    alert(error.message);
  }
};
</script>