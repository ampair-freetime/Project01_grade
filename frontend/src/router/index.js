import { createRouter, createWebHistory } from 'vue-router'

// auth
import Login from '../auth/Login.vue'
import Signin from '../auth/Signup.vue'

// student
import Dashboard from '../student/Dashboard.vue'
import CourseDetail from '../student/CourseDetail.vue'
import Score from '../student/Score.vue'

// teacher
import AssignmentManagement from '../teacher/AssignmentManagement.vue'
import CourseManagement from '../teacher/CourseManagement.vue'
import Grade from '../teacher/Grade.vue'

const routes = [
  // Auth
  { path: '/', redirect: '/login' },
  { path: '/login', component: Login },
  { path: '/signin', component: Signin },

  // Student
  { path: '/student/dashboard', component: Dashboard },
  { path: '/student/course/:id', component: CourseDetail },
  { path: '/student/score', component: Score },

  // Teacher
  { path: '/teacher/courses', component: CourseManagement },
  { path: '/teacher/assignments/:id', component: AssignmentManagement },
  { path: '/teacher/grade', component: Grade },
]

const router = createRouter({
  history: createWebHistory(),
  routes,
})

export default router
