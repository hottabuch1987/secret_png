<template>
  <header
    ref="headerRef"
    class="fixed top-0 left-0 w-full z-50 transition-all duration-300"
    :class="[scrolled ? 'bg-white shadow-md' : 'bg-transparent']"
  >
    <div class="container mx-auto px-4 lg:px-8">
      <div class="flex items-center justify-between h-16 lg:h-20">
        <!-- Левая часть: логотип и десктопное меню -->
        <div class="flex items-center gap-6">
          <!-- Логотип -->
          <NuxtLink to="/" class="flex items-center space-x-2">
            <img src="~/assets/img/logo.png" alt="Logo" class="w-8 h-8" />
            <span class="text-xl font-bold text-gray-800 hidden sm:block"></span>
          </NuxtLink>

          <!-- Десктопная навигация -->
          <nav class="hidden lg:flex items-center space-x-1">
            <NuxtLink
              to="/"
              class="px-3 py-2 text-gray-700 hover:text-blue-600 rounded-md text-sm font-medium transition"
              active-class="text-blue-600 bg-blue-50"
            >
              Главная
            </NuxtLink>
            <NuxtLink
              to="/stego/embed"
              class="flex items-center px-3 py-2 text-gray-700 hover:text-blue-600 rounded-md text-sm font-medium transition"
              active-class="text-blue-600 bg-blue-50"
            >
              <svg class="w-4 h-4 mr-1.5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 15v2m-6 4h12a2 2 0 002-2v-6a2 2 0 00-2-2H6a2 2 0 00-2 2v6a2 2 0 002 2zm10-10V7a4 4 0 00-8 0v4h8z" />
              </svg>
              Спрятать
            </NuxtLink>
            <NuxtLink
              to="/stego/extract"
              class="flex items-center px-3 py-2 text-gray-700 hover:text-blue-600 rounded-md text-sm font-medium transition"
              active-class="text-blue-600 bg-blue-50"
            >
              <svg class="w-4 h-4 mr-1.5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M8 11V7a4 4 0 118 0m-4 8v2m-6 4h12a2 2 0 002-2v-6a2 2 0 00-2-2H6a2 2 0 00-2 2v6a2 2 0 002 2z" />
              </svg>
              Извлечь
            </NuxtLink>
          </nav>
        </div>

        <!-- Правая часть -->
        <div class="flex items-center gap-2">
          <!-- Поиск -->
          <div class="hidden md:block relative">
            <input
              v-model="searchQuery"
              @keyup.enter="searchPng"
              type="text"
              placeholder="Поиск PNG..."
              class="w-64 pl-10 pr-4 py-2 rounded-full border border-gray-200 focus:outline-none focus:ring-2 focus:ring-blue-400 focus:border-transparent text-sm"
            />
            <svg class="w-5 h-5 text-gray-400 absolute left-3 top-2.5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M21 21l-6-6m2-5a7 7 0 11-14 0 7 7 0 0114 0z" />
            </svg>
          </div>

          <button
            @click="searchPngMobile"
            class="md:hidden p-2 text-gray-600 hover:text-blue-600 transition"
            aria-label="Поиск"
          >
            <svg class="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M21 21l-6-6m2-5a7 7 0 11-14 0 7 7 0 0114 0z" />
            </svg>
          </button>

          

          <!-- Профиль / Кнопки авторизации -->
          <template v-if="userStore.isAuthenticated">
            <div class="relative" ref="profileMenuRef">
              <button
                @click="toggleProfileMenu"
                class="flex items-center space-x-2 p-1 rounded-full hover:ring-2 hover:ring-blue-300 transition"
                aria-label="Меню профиля"
              >
                
                <span class="hidden lg:block text-sm font-medium text-gray-700">
                  {{ userStore.fullName || 'Пользователь' }}
                </span>
                <svg class="w-4 h-4 text-gray-500 hidden lg:block" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M19 9l-7 7-7-7" />
                </svg>
              </button>

              <!-- Выпадающее меню профиля -->
              <Transition
                enter-active-class="transition duration-200 ease-out"
                enter-from-class="transform scale-95 opacity-0"
                enter-to-class="transform scale-100 opacity-100"
                leave-active-class="transition duration-150 ease-in"
                leave-from-class="transform scale-100 opacity-100"
                leave-to-class="transform scale-95 opacity-0"
              >
                <div
                  v-if="isProfileMenuOpen"
                  class="absolute right-0 mt-2 w-48 bg-white rounded-lg shadow-lg py-1 border border-gray-100 z-50"
                >
                  <NuxtLink to="/user/account" class="block px-4 py-2 text-sm text-gray-700 hover:bg-gray-50" @click="closeProfileMenu">Профиль</NuxtLink>
                  <NuxtLink to="/user/edit" class="block px-4 py-2 text-sm text-gray-700 hover:bg-gray-50" @click="closeProfileMenu">Редактировать профиль</NuxtLink>
                  <NuxtLink to="/stego/embed" class="block px-4 py-2 text-sm text-gray-700 hover:bg-gray-50" @click="closeProfileMenu">Спрятать текст</NuxtLink>
                  <NuxtLink to="/stego/extract" class="block px-4 py-2 text-sm text-gray-700 hover:bg-gray-50" @click="closeProfileMenu">Извлечь текст</NuxtLink>
                  <button
                    @click="logout"
                    class="block w-full text-left px-4 py-2 text-sm text-red-600 hover:bg-gray-50"
                  >
                    Выйти
                  </button>
                </div>
              </Transition>
            </div>
          </template>

          <template v-else>
            <NuxtLink to="/user/login" class="hidden sm:inline-flex px-4 py-2 text-sm font-medium text-gray-700 hover:text-blue-600 transition">
              Войти
            </NuxtLink>
            <NuxtLink to="/user/signup" class="hidden sm:inline-flex px-4 py-2 text-sm font-medium text-white bg-blue-600 rounded-lg hover:bg-blue-700 transition">
              Регистрация
            </NuxtLink>
          </template>

          <!-- ЕДИНАЯ КНОПКА ДЛЯ МОБИЛЬНОГО МЕНЮ -->
          <button
            @click="toggleMobileMenu"
            class="lg:hidden p-2 text-gray-600 hover:text-blue-600 transition"
            aria-label="Меню"
            :aria-expanded="isMobileMenuOpen"
          >
            <svg v-if="!isMobileMenuOpen" class="w-6 h-6" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M4 6h16M4 12h16M4 18h16" />
            </svg>
            <svg v-else class="w-6 h-6" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M6 18L18 6M6 6l12 12" />
            </svg>
          </button>
        </div>
      </div>
    </div>

    <!-- Мобильное меню -->
    <Teleport to="body">
      <Transition
        enter-active-class="transition duration-300 ease-out"
        enter-from-class="transform -translate-x-full"
        enter-to-class="transform translate-x-0"
        leave-active-class="transition duration-300 ease-in"
        leave-from-class="transform translate-x-0"
        leave-to-class="transform -translate-x-full"
      >
        <div
          v-if="isMobileMenuOpen"
          class="fixed inset-0 z-50 lg:hidden"
          @click.self="closeMobileMenu"
        >
          <div class="absolute inset-0 bg-black/30 backdrop-blur-sm" @click="closeMobileMenu"></div>

          <nav class="absolute left-0 top-0 h-full w-64 bg-white shadow-xl p-6 overflow-y-auto">
           

            <ul class="space-y-2 mt-4">
              <li>
                <NuxtLink to="/" class="block py-2 px-3 text-gray-700 hover:bg-gray-50 rounded-md" @click="closeMobileMenu">
                  Главная
                </NuxtLink>
              </li>
              <li>
                <NuxtLink to="/stego/embed" class="flex items-center py-2 px-3 text-gray-700 hover:bg-gray-50 rounded-md" @click="closeMobileMenu">
                  <svg class="w-4 h-4 mr-2" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                    <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 15v2m-6 4h12a2 2 0 002-2v-6a2 2 0 00-2-2H6a2 2 0 00-2 2v6a2 2 0 002 2zm10-10V7a4 4 0 00-8 0v4h8z" />
                  </svg>
                  Спрятать текст
                </NuxtLink>
              </li>
              <li>
                <NuxtLink to="/stego/extract" class="flex items-center py-2 px-3 text-gray-700 hover:bg-gray-50 rounded-md" @click="closeMobileMenu">
                  <svg class="w-4 h-4 mr-2" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                    <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M8 11V7a4 4 0 118 0m-4 8v2m-6 4h12a2 2 0 002-2v-6a2 2 0 00-2-2H6a2 2 0 00-2 2v6a2 2 0 002 2z" />
                  </svg>
                  Извлечь текст
                </NuxtLink>
              </li>
            </ul>

            <div class="border-t border-gray-100 my-4"></div>

            <!-- ИНФОРМАЦИЯ О ПОЛЬЗОВАТЕЛЕ В МОБИЛЬНОМ МЕНЮ -->
            <template v-if="userStore.isAuthenticated">
              <div class="bg-gray-50 rounded-lg mb-4 overflow-hidden">
                <div class="flex items-center gap-3 p-3">
                  <div class="flex-shrink-0">
                    <img
                      :src="userStore.user.avatar || 'https://i.pravatar.cc/150?img=3'"
                      alt="Avatar"
                      class="w-12 h-12 rounded-full object-cover border-2 border-white shadow-sm"
                    />
                  </div>
                  <div class="flex-1 min-w-0">
                    <p class="text-sm font-medium text-gray-800 truncate">
                      {{ userStore.fullName || 'Пользователь' }}
                    </p>
                    <p class="text-xs text-gray-500 truncate">
                      {{ userStore.user.email }}
                    </p>
                  </div>
                </div>

                <div v-if="userStore.user.id" class="px-3 pb-3">
                  <UserGallery :user-id="userStore.user.id" />
                </div>
              </div>

              <NuxtLink
                to="/user/account"
                class="block w-full text-center py-2.5 px-4 mb-2 text-sm font-medium text-gray-700 border border-gray-300 rounded-lg hover:bg-gray-50 transition"
                @click="closeMobileMenu"
              >
                Мой профиль
              </NuxtLink>
              <button
                @click="logout"
                class="block w-full text-center py-2.5 px-4 text-sm font-medium text-white bg-red-600 rounded-lg hover:bg-red-700 transition"
              >
                Выйти
              </button>
            </template>

            <template v-else>
              <NuxtLink
                to="/user/login"
                class="block w-full text-center py-2.5 px-4 mb-2 text-sm font-medium text-gray-700 border border-gray-300 rounded-lg hover:bg-gray-50 transition"
                @click="closeMobileMenu"
              >
                Войти
              </NuxtLink>
              <NuxtLink
                to="/user/signup"
                class="block w-full text-center py-2.5 px-4 text-sm font-medium text-white bg-blue-600 rounded-lg hover:bg-blue-700 transition"
                @click="closeMobileMenu"
              >
                Регистрация
              </NuxtLink>
            </template>
          </nav>
        </div>
      </Transition>
    </Teleport>
  </header>
</template>

<script setup>
import UserGallery from '@/layouts/components/UserGallery.vue'
import { ref, onMounted, onUnmounted, computed } from 'vue'
import { useRouter } from 'vue-router'
import { useUserStore } from '@/stores/user'
import { useToastStore } from '@/stores/toast'
import axios from 'axios'
import { onClickOutside } from '@vueuse/core'

const userStore = useUserStore()
const toastStore = useToastStore()
const router = useRouter()

// Состояния меню
const isMobileMenuOpen = ref(false)
const isProfileMenuOpen = ref(false)

// Для эффекта при скролле
const scrolled = ref(false)
const headerRef = ref(null)

// Референсы для клика вне
const profileMenuRef = ref(null)

// ===== ПОИСК PNG В ЯНДЕКСЕ =====
const searchQuery = ref('')

const searchPng = () => {
  const query = searchQuery.value?.trim()
  if (!query) return

  const url = `https://yandex.ru/images/search?text=${encodeURIComponent(query)}&itype=png`
  window.open(url, '_blank')
  searchQuery.value = ''
}

const searchPngMobile = () => {
  const query = prompt('Что искать в PNG?')
  if (!query) return

  const url = `https://yandex.ru/images/search?text=${encodeURIComponent(query)}&itype=png`
  window.open(url, '_blank')
}
// ================================

// Закрытие профильного меню при клике вне
onClickOutside(profileMenuRef, () => {
  isProfileMenuOpen.value = false
})

// Обработка скролла
const handleScroll = () => {
  scrolled.value = window.scrollY > 20
}

// Функции управления меню
const toggleMobileMenu = () => {
  isMobileMenuOpen.value = !isMobileMenuOpen.value
  if (isMobileMenuOpen.value) {
    document.body.style.overflow = 'hidden'
  } else {
    document.body.style.overflow = ''
  }
}

const closeMobileMenu = () => {
  isMobileMenuOpen.value = false
  document.body.style.overflow = ''
}

const toggleProfileMenu = () => {
  isProfileMenuOpen.value = !isProfileMenuOpen.value
}

const closeProfileMenu = () => {
  isProfileMenuOpen.value = false
}

// Выход из системы
const logout = async () => {
  try {
    if (userStore.user.token) {
      await axios.post('/auth/token/logout/')
    }
  } catch (error) {
    console.error('Logout error:', error)
  } finally {
    userStore.removeToken()
    toastStore.showToast(5000, 'Вы вышли из системы!', 'bg-gray-300/10')
    closeProfileMenu()
    closeMobileMenu()
    router.push('/')
  }
}

// Инициализация
onMounted(() => {
  userStore.initStore()
  const token = userStore.user.token
  if (token) {
    axios.defaults.headers.common['Authorization'] = `Token ${token}`
  } else {
    delete axios.defaults.headers.common['Authorization']
  }

  window.addEventListener('scroll', handleScroll)
  handleScroll()
})

onUnmounted(() => {
  window.removeEventListener('scroll', handleScroll)
  document.body.style.overflow = ''
})
</script>

<style scoped>
/* Дополнительные стили при необходимости */
</style>