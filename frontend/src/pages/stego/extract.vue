<!-- pages/stego/extract.vue -->
<template>
  <div class="max-w-2xl mx-auto p-4">
    <div class="bg-white rounded-2xl shadow-xl overflow-hidden border border-gray-100 hover:shadow-2xl transition-shadow duration-300">
      <!-- Градиентная шапка -->
      <div class="h-32 bg-gradient-to-r from-green-500 to-blue-600"></div>

      <div class="relative px-6 pb-6">
        <!-- Заголовок -->
        <div class="flex items-end -mt-12 mb-6">
          <div class="w-24 h-24 rounded-full border-4 border-white bg-white shadow-lg flex items-center justify-center">
            <svg class="w-12 h-12 text-green-600" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M8 11V7a4 4 0 118 0m-4 8v2m-6 4h12a2 2 0 002-2v-6a2 2 0 00-2-2H6a2 2 0 00-2 2v6a2 2 0 002 2z" />
            </svg>
          </div>
          <div class="ml-6 flex-1">
            <h2 class="text-2xl font-bold text-gray-800">Извлечь текст</h2>
            <p class="text-gray-500 mt-1">Достаньте скрытое сообщение из картинки</p>
          </div>
        </div>

        <!-- Блок ошибок -->
        <div v-if="errors.length > 0" class="mb-4 rounded-md bg-red-50 p-4">
          <div class="flex">
            <div class="flex-shrink-0">
              <svg class="h-5 w-5 text-red-400" xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24" fill="none" stroke="currentColor">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 8v4m0 4h.01M21 12a9 9 0 11-18 0 9 9 0 0118 0z" />
              </svg>
            </div>
            <div class="ml-3">
              <h3 class="text-sm font-medium text-red-800">Ошибка</h3>
              <div class="mt-2 text-sm text-red-700">
                <ul class="list-disc list-inside space-y-1">
                  <li v-for="(error, index) in errors" :key="index">{{ error }}</li>
                </ul>
              </div>
            </div>
          </div>
        </div>

        <!-- Форма -->
        <form @submit.prevent="submitForm" class="space-y-4">
          <!-- Загрузка картинки -->
          <div>
            <label class="block text-sm font-medium text-gray-700 mb-2">Картинка со скрытым текстом</label>
            <div 
              class="border-2 border-dashed rounded-lg p-4 text-center cursor-pointer transition"
              :class="preview ? 'border-green-400 bg-green-50' : 'border-gray-300 hover:border-green-400 hover:bg-gray-50'"
              @click="openFileDialog"
            >
              <input 
                ref="fileInput" 
                type="file" 
                accept="image/png,image/bmp,image/webp" 
                class="hidden" 
                @change="onFile"
              >
              <img v-if="preview" :src="preview" class="max-h-40 mx-auto rounded-lg shadow-md">
              <div v-else class="py-6">
                <svg class="w-12 h-12 text-gray-400 mx-auto mb-2" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M4 16l4.586-4.586a2 2 0 012.828 0L16 16m-2-2l1.586-1.586a2 2 0 012.828 0L20 14m-6-6h.01M6 20h12a2 2 0 002-2V6a2 2 0 00-2-2H6a2 2 0 00-2 2v12a2 2 0 002 2z" />
                </svg>
                <p class="text-sm text-gray-500">Нажмите, чтобы выбрать PNG</p>
              </div>
            </div>
          </div>

          <!-- Пароль -->
          <div>
            <label for="password" class="block text-sm font-medium text-gray-700 mb-2">Пароль</label>
            <div class="relative">
              <input
                id="password"
                v-model="form.password"
                :type="showPassword ? 'text' : 'password'"
                placeholder="Пароль для расшифровки текста"
                class="w-full px-4 py-3 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-green-500 focus:border-green-500 transition"
              >
              <button 
                type="button"
                @click="showPassword = !showPassword"
                class="absolute right-3 top-1/2 -translate-y-1/2 text-gray-400 hover:text-gray-600"
              >
                <svg v-if="showPassword" class="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M13.875 18.825A10.05 10.05 0 0112 19c-4.478 0-8.268-2.943-9.543-7a9.97 9.97 0 011.563-3.029m5.858.908a3 3 0 114.243 4.243M9.878 9.878l4.242 4.242M9.88 9.88l-3.29-3.29m7.532 7.532l3.29 3.29M3 3l3.59 3.59m0 0A9.953 9.953 0 0112 5c4.478 0 8.268 2.943 9.543 7a10.025 10.025 0 01-4.132 5.411m0 0L21 21" />
                </svg>
                <svg v-else class="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M15 12a3 3 0 11-6 0 3 3 0 016 0z" />
                  <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M2.458 12C3.732 7.943 7.523 5 12 5c4.478 0 8.268 2.943 9.542 7-1.274 4.057-5.064 7-9.542 7-4.477 0-8.268-2.943-9.542-7z" />
                </svg>
              </button>
            </div>
          </div>

          <!-- Кнопка -->
          <div class="flex justify-end space-x-3 pt-4 border-t border-gray-200">
            <button
              type="submit"
              :disabled="loading || !canSubmit"
              class="px-4 py-2 text-sm font-medium text-white bg-green-600 rounded-lg hover:bg-green-700 transition disabled:opacity-50 disabled:cursor-not-allowed flex items-center"
            >
              <svg v-if="loading" class="animate-spin -ml-1 mr-2 h-4 w-4 text-white" xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24">
                <circle class="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" stroke-width="4"></circle>
                <path class="opacity-75" fill="currentColor" d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4zm2 5.291A7.962 7.962 0 014 12H0c0 3.042 1.135 5.824 3 7.938l3-2.647z"></path>
              </svg>
              {{ loading ? 'Извлечение...' : 'Извлечь текст' }}
            </button>
          </div>
        </form>

        <!-- Результат -->
        <div v-if="result" class="mt-6 p-4 bg-gray-50 border border-gray-200 rounded-lg">
          <div class="flex items-center justify-between mb-2">
            <label class="text-sm font-medium text-gray-700">Извлечённый текст</label>
            <button 
              type="button"
              @click="copyText"
              class="text-sm text-blue-600 hover:text-blue-800 transition flex items-center"
            >
              <svg class="w-4 h-4 mr-1" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M8 16H6a2 2 0 01-2-2V6a2 2 0 012-2h8a2 2 0 012 2v2m-6 12h8a2 2 0 002-2v-8a2 2 0 00-2-2h-8a2 2 0 00-2 2v8a2 2 0 002 2z" />
              </svg>
              {{ copied ? 'Скопировано' : 'Копировать' }}
            </button>
          </div>
          <pre class="whitespace-pre-wrap text-sm text-gray-800 font-mono bg-white p-3 rounded border border-gray-200 max-h-60 overflow-y-auto">{{ result }}</pre>
        </div>

        <!-- Подсказка -->
        <div class="mt-6 p-4 bg-green-50 rounded-lg">
          <div class="flex items-start">
            <svg class="w-5 h-5 text-green-500 mr-3 flex-shrink-0 mt-0.5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M13 16h-1v-4h-1m1-4h.01M21 12a9 9 0 11-18 0 9 9 0 0118 0z" />
            </svg>
            <div class="text-sm text-green-800">
              <p class="font-medium">Важно</p>
              <p class="mt-1 text-green-700">Используйте ту же картинку, что скачали после шифрования. Если её пересжать или отправить через мессенджер — текст не извлечётся.</p>
            </div>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, computed } from 'vue'
import { useUserStore } from '@/stores/user'
import { useToastStore } from '@/stores/toast'
import axios from 'axios'

const userStore = useUserStore()
const toastStore = useToastStore()

useHead({ title: 'Извлечь текст из картинки' })

// Форма
const form = ref({
  password: ''
})

// Реактивные переменные
const fileInput = ref(null)
const selectedFile = ref(null)  // ← храним файл реактивно
const preview = ref('')
const showPassword = ref(false)
const loading = ref(false)
const errors = ref([])
const result = ref('')
const copied = ref(false)

// Проверка, можно ли отправить
const canSubmit = computed(() => {
  return (
    selectedFile.value !== null &&
    form.value.password !== ''
  )
})

// Открытие диалога выбора файла
const openFileDialog = () => {
  fileInput.value?.click()
}

// Обработка выбора файла
const onFile = (e) => {
  const file = e.target.files[0]
  if (!file) return

  errors.value = []
  result.value = ''

  if (!file.type.startsWith('image/')) {
    errors.value.push('Выберите изображение')
    return
  }

  // Сохраняем файл реактивно
  selectedFile.value = file
  preview.value = URL.createObjectURL(file)
}

// Отправка формы
const submitForm = async () => {
  errors.value = []
  result.value = ''
  loading.value = true

  // Валидация
  if (!selectedFile.value) {
    errors.value.push('Выберите картинку')
    loading.value = false
    return
  }

  if (!form.value.password) {
    errors.value.push('Введите пароль')
    loading.value = false
    return
  }

  try {
    const formData = new FormData()
    formData.append('image', selectedFile.value)
    formData.append('password', form.value.password)

    // ВАЖНО: не указываем Content-Type вручную — браузер сам выставит boundary
    const response = await axios.post('/stego/extract/', formData)

    result.value = response.data.text
    toastStore.showToast(3000, 'Текст извлечён', 'bg-green-500/20')
  } catch (error) {
    console.error('Extract error:', error)

    // Обработка ошибок
    if (error.response) {
      const status = error.response.status

      if (status === 401) {
        errors.value.push('Сессия истекла. Пожалуйста, войдите заново')
        userStore.removeToken()
      } else if (status === 400) {
        errors.value.push(error.response.data?.error || 'Не удалось извлечь текст. Проверьте пароль.')
      } else if (status === 404) {
        errors.value.push('В этой картинке нет скрытого текста')
      } else if (status === 500) {
        errors.value.push('Ошибка сервера. Попробуйте позже.')
      } else {
        errors.value.push('Не удалось обработать запрос')
      }
    } else {
      errors.value.push('Сетевая ошибка. Проверьте подключение.')
    }

    toastStore.showToast(3000, errors.value[0], 'bg-red-500/20')
  } finally {
    loading.value = false
  }
}

// Копирование текста
const copyText = async () => {
  try {
    await navigator.clipboard.writeText(result.value)
    copied.value = true
    setTimeout(() => { copied.value = false }, 2000)
  } catch (e) {
    toastStore.showToast(3000, 'Не удалось скопировать', 'bg-red-500/20')
  }
}
</script>

<style scoped>
/* Дополнительные стили при необходимости */
</style>