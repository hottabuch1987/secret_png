<!-- pages/user/account-edit.vue -->
<template>
  <div class="max-w-2xl mx-auto p-4">
    <div class="bg-white rounded-2xl shadow-xl overflow-hidden border border-gray-100">
      <!-- Заголовок -->
      <div class="px-6 py-4 border-b border-gray-200 bg-gray-50">
        <div class="flex items-center justify-between">
          <h2 class="text-xl font-bold text-gray-800">Редактирование профиля</h2>
          <NuxtLink
            to="/user/account"
            class="text-sm text-gray-500 hover:text-gray-700 transition flex items-center"
          >
            <svg class="w-4 h-4 mr-1" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M10 19l-7-7m0 0l7-7m-7 7h18" />
            </svg>
            Назад
          </NuxtLink>
        </div>
      </div>

      <!-- Форма -->
      <div class="p-6">
        <!-- Блок успеха -->
        <div v-if="successMessage" class="mb-4 rounded-md bg-green-50 dark:bg-green-900/20 p-4">
          <div class="flex">
            <div class="flex-shrink-0">
              <svg class="h-5 w-5 text-green-400" xmlns="http://www.w3.org/2000/svg" viewBox="0 0 20 20" fill="currentColor">
                <path fill-rule="evenodd" d="M10 18a8 8 0 100-16 8 8 0 000 16zm3.707-9.293a1 1 0 00-1.414-1.414L9 10.586 7.707 9.293a1 1 0 00-1.414 1.414l2 2a1 1 0 001.414 0l4-4z" clip-rule="evenodd" />
              </svg>
            </div>
            <div class="ml-3">
              <p class="text-sm font-medium text-green-800 dark:text-green-200">{{ successMessage }}</p>
            </div>
          </div>
        </div>

        <!-- Блок ошибок -->
        <div v-if="errors.length > 0" class="mb-4 rounded-md bg-red-50 dark:bg-red-900/20 p-4">
          <div class="flex">
            <div class="flex-shrink-0">
              <svg class="h-5 w-5 text-red-400" xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24" fill="none" stroke="currentColor">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 8v4m0 4h.01M21 12a9 9 0 11-18 0 9 9 0 0118 0z" />
              </svg>
            </div>
            <div class="ml-3">
              <h3 class="text-sm font-medium text-red-800">Ошибка при сохранении</h3>
              <div class="mt-2 text-sm text-red-700">
                <ul class="list-disc list-inside space-y-1">
                  <li v-for="(error, index) in errors" :key="index">{{ error }}</li>
                </ul>
              </div>
            </div>
          </div>
        </div>

        <form @submit.prevent="submitForm" class="space-y-6">
          <!-- Email (только для чтения) -->
          <div>
            <label for="email" class="block text-sm font-medium text-gray-700 dark:text-gray-300 mb-1">
              Email
            </label>
            <input
              id="email"
              :value="userStore.user.email"
              type="email"
              disabled
              class="w-full px-3 py-2 border border-gray-300 dark:border-gray-600 rounded-lg bg-gray-100 dark:bg-gray-700 text-gray-500 dark:text-gray-400 cursor-not-allowed"
            />
            <p class="mt-1 text-xs text-gray-500">Email нельзя изменить</p>
          </div>

          <!-- Username -->
          <div>
            <label for="username" class="block text-sm font-medium text-gray-700 dark:text-gray-300 mb-1">
              Имя пользователя *
            </label>
            <input
              id="username"
              v-model="form.username"
              type="text"
              required
              class="w-full px-3 py-2 border border-gray-300 dark:border-gray-600 rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-500 focus:border-blue-500 dark:focus:ring-blue-400 dark:focus:border-blue-400 bg-white dark:bg-gray-800 text-gray-900 dark:text-white"
              placeholder="Введите имя пользователя"
            />
          </div>

          <!-- Имя -->
          <div>
            <label for="first_name" class="block text-sm font-medium text-gray-700 dark:text-gray-300 mb-1">
              Имя
            </label>
            <input
              id="first_name"
              v-model="form.first_name"
              type="text"
              class="w-full px-3 py-2 border border-gray-300 dark:border-gray-600 rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-500 focus:border-blue-500 dark:focus:ring-blue-400 dark:focus:border-blue-400 bg-white dark:bg-gray-800 text-gray-900 dark:text-white"
              placeholder="Введите имя"
            />
          </div>

          <!-- Фамилия -->
          <div>
            <label for="last_name" class="block text-sm font-medium text-gray-700 dark:text-gray-300 mb-1">
              Фамилия
            </label>
            <input
              id="last_name"
              v-model="form.last_name"
              type="text"
              class="w-full px-3 py-2 border border-gray-300 dark:border-gray-600 rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-500 focus:border-blue-500 dark:focus:ring-blue-400 dark:focus:border-blue-400 bg-white dark:bg-gray-800 text-gray-900 dark:text-white"
              placeholder="Введите фамилию"
            />
          </div>

          <!-- Информация о подтверждении email -->
          <div class="p-4 bg-blue-50 dark:bg-blue-900/20 rounded-lg">
            <div class="flex items-center">
              <svg v-if="userStore.user.email_confirmed" class="w-5 h-5 text-green-500 mr-2" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 12l2 2 4-4m6 2a9 9 0 11-18 0 9 9 0 0118 0z" />
              </svg>
              <svg v-else class="w-5 h-5 text-yellow-500 mr-2" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 8v4m0 4h.01M21 12a9 9 0 11-18 0 9 9 0 0118 0z" />
              </svg>
              <span class="text-sm" :class="userStore.user.email_confirmed ? 'text-green-700 dark:text-green-300' : 'text-yellow-700 dark:text-yellow-300'">
                {{ userStore.user.email_confirmed ? 'Email подтвержден' : 'Email не подтвержден' }}
              </span>
            </div>
          </div>

          <!-- Кнопки действий -->
          <div class="flex justify-end space-x-3 pt-4 border-t border-gray-200">
            <NuxtLink
              to="/user/account"
              class="px-4 py-2 text-sm font-medium text-gray-700 bg-gray-100 rounded-lg hover:bg-gray-200 transition"
            >
              Отмена
            </NuxtLink>
            <button
              type="submit"
              :disabled="loading || !hasChanges"
              class="px-4 py-2 text-sm font-medium text-white bg-blue-600 rounded-lg hover:bg-blue-700 transition disabled:opacity-50 disabled:cursor-not-allowed flex items-center"
            >
              <svg v-if="loading" class="animate-spin -ml-1 mr-2 h-4 w-4 text-white" xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24">
                <circle class="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" stroke-width="4"></circle>
                <path class="opacity-75" fill="currentColor" d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4zm2 5.291A7.962 7.962 0 014 12H0c0 3.042 1.135 5.824 3 7.938l3-2.647z"></path>
              </svg>
              {{ loading ? 'Сохранение...' : 'Сохранить изменения' }}
            </button>
          </div>
        </form>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, computed, onMounted } from 'vue'
import { useRouter } from 'vue-router'
import { useUserStore } from '@/stores/user'
import { useToastStore } from '@/stores/toast'
import axios from 'axios'

const userStore = useUserStore()
const toastStore = useToastStore()
const router = useRouter()

// Заголовок страницы
useHead({
  title: 'Редактирование профиля'
})

// Форма
const form = ref({
  username: '',
  first_name: '',
  last_name: ''
})

const loading = ref(false)
const errors = ref([])
const successMessage = ref('')

// Проверка, были ли изменения
const hasChanges = computed(() => {
  const user = userStore.user
  return (
    form.value.username !== user.username ||
    form.value.first_name !== (user.first_name || '') ||
    form.value.last_name !== (user.last_name || '')
  )
})

// Загрузка данных пользователя в форму
onMounted(async () => {
  // Проверяем авторизацию
  if (!userStore.isAuthenticated) {
    toastStore.showToast(5000, 'Пожалуйста, войдите в систему', 'bg-red-500/20')
    router.push('/user/login')
    return
  }

  // Если нет данных пользователя, загружаем их
  if (!userStore.user.id) {
    try {
      await userStore.fetchUserInfo()
    } catch (error) {
      console.error('Error loading user data:', error)
      toastStore.showToast(5000, 'Ошибка загрузки данных пользователя', 'bg-red-500/20')
      router.push('/user/login')
      return
    }
  }

  // Заполняем форму данными пользователя
  form.value = {
    username: userStore.user.username || '',
    first_name: userStore.user.first_name || '',
    last_name: userStore.user.last_name || ''
  }
})

// Отправка формы
const submitForm = async () => {
  errors.value = []
  successMessage.value = ''
  loading.value = true

  // Валидация
  if (!form.value.username || form.value.username.trim() === '') {
    errors.value.push('Имя пользователя обязательно')
    loading.value = false
    return
  }

  try {
    const userId = userStore.user.id
    const payload = {
      username: form.value.username.trim(),
      first_name: form.value.first_name.trim(),
      last_name: form.value.last_name.trim()
    }

    
    const response = await axios.patch(`/users/${userId}/`, payload)

    // Обновляем данные в сторе
    userStore.updateUserInfo({
      username: response.data.username,
      first_name: response.data.first_name || '',
      last_name: response.data.last_name || ''
    })

    // Показываем сообщение об успехе
    successMessage.value = 'Данные профиля успешно обновлены'
    

    // Через 2 секунды перенаправляем на страницу профиля
    setTimeout(() => {
      router.push('/user/account')
    }, 2000)

  } catch (error) {
    console.error('Update error:', error)
    
    // Обработка 401 (неавторизован)
    if (error.response && error.response.status === 401) {
      errors.value.push('Сессия истекла. Пожалуйста, войдите заново')
      userStore.removeToken()
      setTimeout(() => {
        router.push('/user/login')
      }, 1500)
    } else if (error.response && error.response.status === 400) {
      const data = error.response.data
      if (typeof data === 'object') {
        // Обработка ошибок валидации
        for (const [field, messages] of Object.entries(data)) {
          if (Array.isArray(messages)) {
            messages.forEach(msg => {
              errors.value.push(`${field}: ${msg}`)
            })
          } else {
            errors.value.push(`${field}: ${messages}`)
          }
        }
      } else if (typeof data === 'string') {
        errors.value.push(data)
      }
    } else if (error.response && error.response.status === 403) {
      errors.value.push('У вас нет прав на редактирование этого профиля')
    } else if (error.response && error.response.status === 404) {
      errors.value.push('Пользователь не найден')
    } else {
      errors.value.push('Ошибка сервера. Попробуйте позже.')
    }
  } finally {
    loading.value = false
  }
}
</script>

<style scoped>
/* Дополнительные стили при необходимости */
</style>