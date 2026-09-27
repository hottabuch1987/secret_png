<!-- pages/stego/embed.vue -->
<template>
  <div class="max-w-2xl mx-auto p-4">
    <div class="bg-white rounded-2xl shadow-xl overflow-hidden border border-gray-100 hover:shadow-2xl transition-shadow duration-300">
      <!-- Градиентная шапка -->
      <div class="h-32 bg-gradient-to-r from-blue-500 to-purple-600"></div>

      <div class="relative px-6 pb-6">
        <!-- Заголовок -->
        <div class="flex items-end -mt-12 mb-6">
          <div class="w-24 h-24 rounded-full border-4 border-white bg-white shadow-lg flex items-center justify-center">
            <svg class="w-12 h-12 text-blue-600" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 15v2m-6 4h12a2 2 0 002-2v-6a2 2 0 00-2-2H6a2 2 0 00-2 2v6a2 2 0 002 2zm10-10V7a4 4 0 00-8 0v4h8z" />
            </svg>
          </div>
          <div class="ml-6 flex-1">
            <h2 class="text-2xl font-bold text-gray-800">Спрятать текст</h2>
            <p class="text-gray-500 mt-1">Зашифруйте сообщение внутри PNG-картинки</p>
          </div>
        </div>

        <!-- Блок успеха -->
        <div v-if="successMessage" class="mb-4 rounded-md bg-green-50 p-4">
          <div class="flex">
            <div class="flex-shrink-0">
              <svg class="h-5 w-5 text-green-400" xmlns="http://www.w3.org/2000/svg" viewBox="0 0 20 20" fill="currentColor">
                <path fill-rule="evenodd" d="M10 18a8 8 0 100-16 8 8 0 000 16zm3.707-9.293a1 1 0 00-1.414-1.414L9 10.586 7.707 9.293a1 1 0 00-1.414 1.414l2 2a1 1 0 001.414 0l4-4z" clip-rule="evenodd" />
              </svg>
            </div>
            <div class="ml-3">
              <p class="text-sm font-medium text-green-800">{{ successMessage }}</p>
            </div>
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
            <label class="block text-sm font-medium text-gray-700 mb-2">Картинка-носитель (PNG)</label>
            <div 
              class="border-2 border-dashed rounded-lg p-4 text-center cursor-pointer transition"
              :class="preview ? 'border-blue-400 bg-blue-50' : 'border-gray-300 hover:border-blue-400 hover:bg-gray-50'"
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
                <p class="text-xs text-gray-400 mt-1">JPG не подойдёт — сжатие уничтожит данные</p>
              </div>
            </div>
          </div>

          <!-- Секретный текст -->
          <div>
            <label for="text" class="block text-sm font-medium text-gray-700 mb-2">Секретный текст</label>
            <textarea
              id="text"
              v-model="form.text"
              rows="4"
              placeholder="Введите сообщение, которое нужно спрятать..."
              class="w-full px-4 py-3 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-500 focus:border-blue-500 transition resize-none"
            ></textarea>
            <p class="text-xs text-gray-500 mt-1">{{ form.text.length }} символов</p>
          </div>

          <!-- Пароль -->
          <div>
            <label for="password" class="block text-sm font-medium text-gray-700 mb-2">Пароль</label>
            <div class="relative">
              <input
                id="password"
                v-model="form.password"
                :type="showPassword ? 'text' : 'password'"
                placeholder="Пароль для шифрования"
                class="w-full px-4 py-3 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-500 focus:border-blue-500 transition"
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
            <p class="text-xs text-gray-500 mt-1">Минимум 6 символов</p>
          </div>

          <!-- Кнопка -->
          <div class="flex justify-end space-x-3 pt-4 border-t border-gray-200">
            <button
              type="submit"
              :disabled="loading || !canSubmit"
              class="px-4 py-2 text-sm font-medium text-white bg-blue-600 rounded-lg hover:bg-blue-700 transition disabled:opacity-50 disabled:cursor-not-allowed flex items-center"
            >
              <svg v-if="loading" class="animate-spin -ml-1 mr-2 h-4 w-4 text-white" xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24">
                <circle class="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" stroke-width="4"></circle>
                <path class="opacity-75" fill="currentColor" d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4zm2 5.291A7.962 7.962 0 014 12H0c0 3.042 1.135 5.824 3 7.938l3-2.647z"></path>
              </svg>
              {{ loading ? 'Шифрование...' : 'Спрятать и скачать' }}
            </button>
          </div>
        </form>

        <!-- Подсказка -->
        <div class="mt-6 p-4 bg-blue-50 rounded-lg">
          <div class="flex items-start">
            <svg class="w-5 h-5 text-blue-500 mr-3 flex-shrink-0 mt-0.5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M13 16h-1v-4h-1m1-4h.01M21 12a9 9 0 11-18 0 9 9 0 0118 0z" />
            </svg>
            <div class="text-sm text-blue-800">
              <p class="font-medium">Как это работает</p>
              <p class="mt-1 text-blue-700">Текст шифруется и прячется в пикселях картинки. Внешне она не изменится. Получатель сможет извлечь текст, только если знает пароль.</p>
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

useHead({ title: 'Спрятать текст в картинку' })

// Форма
const form = ref({
  text: '',
  password: ''
})

// Реактивные переменные
const fileInput = ref(null)
const selectedFile = ref(null)  // ← храним файл реактивно
const preview = ref('')
const showPassword = ref(false)
const loading = ref(false)
const errors = ref([])
const successMessage = ref('')

// Проверка, можно ли отправить
const canSubmit = computed(() => {
  return (
    selectedFile.value !== null &&
    form.value.text.trim() !== '' &&
    form.value.password.length >= 6
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
  successMessage.value = ''

  // Проверка типа
  if (!file.type.startsWith('image/')) {
    errors.value.push('Выберите изображение')
    return
  }

  // JPG не подойдёт
  if (file.type === 'image/jpeg') {
    errors.value.push('JPG не подойдёт — используйте PNG')
    return
  }

  // Сохраняем файл реактивно
  selectedFile.value = file
  preview.value = URL.createObjectURL(file)
}

// Отправка формы
const submitForm = async () => {
  errors.value = []
  successMessage.value = ''
  loading.value = true

  // Валидация
  if (!selectedFile.value) {
    errors.value.push('Выберите картинку')
    loading.value = false
    return
  }

  if (!form.value.text.trim()) {
    errors.value.push('Введите секретный текст')
    loading.value = false
    return
  }

  if (form.value.password.length < 6) {
    errors.value.push('Пароль должен быть минимум 6 символов')
    loading.value = false
    return
  }

  try {
    const formData = new FormData()
    formData.append('image', selectedFile.value)
    formData.append('text', form.value.text)
    formData.append('password', form.value.password)

    // ВАЖНО: не указываем Content-Type вручную — браузер сам выставит boundary
    const response = await axios.post('/stego/embed/', formData, {
      responseType: 'blob'
    })

    // Скачиваем результат
    const blob = new Blob([response.data], { type: 'image/png' })
    const url = URL.createObjectURL(blob)
    const a = document.createElement('a')
    a.href = url
    a.download = 'stego.png'
    a.click()
    URL.revokeObjectURL(url)

    successMessage.value = 'Текст успешно спрятан! Картинка скачана.'
    toastStore.showToast(3000, 'Готово', 'bg-green-500/20')

    // Сброс формы
    form.value.text = ''
    form.value.password = ''
    selectedFile.value = null
    preview.value = ''
    if (fileInput.value) {
      fileInput.value.value = ''
    }
  } catch (error) {
    console.error('Embed error:', error)

    // Обработка ошибок
    if (error.response) {
      const status = error.response.status

      // Если ответ — Blob, читаем его как текст и парсим JSON
      let errorData = error.response.data
      if (errorData instanceof Blob) {
        try {
          const text = await errorData.text()
          errorData = JSON.parse(text)
        } catch (e) {
          errorData = { error: 'Неизвестная ошибка' }
        }
      }

      if (status === 401) {
        errors.value.push('Сессия истекла. Пожалуйста, войдите заново')
        userStore.removeToken()
      } else if (status === 400) {
        errors.value.push(errorData?.error || 'Неверные данные')
      } else if (status === 413) {
        errors.value.push('Файл слишком большой')
      } else if (status === 500) {
        errors.value.push(errorData?.error || 'Ошибка сервера. Попробуйте позже.')
      } else {
        errors.value.push(errorData?.error || 'Не удалось обработать запрос')
      }
    } else {
      errors.value.push('Сетевая ошибка. Проверьте подключение.')
    }

    toastStore.showToast(3000, errors.value[0], 'bg-red-500/20')
  } finally {
    loading.value = false
  }
}
</script>

<style scoped>
/* Дополнительные стили при необходимости */
</style>