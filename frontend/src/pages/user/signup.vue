<template>
  <main class="bg-white dark:bg-gray-900 min-h-screen flex items-center justify-center py-12 px-4 sm:px-6 lg:px-8">
    <div class="max-w-md w-full space-y-8">
      <!-- Заголовок -->
      <div>
        <h1 class="text-center text-4xl font-bold text-gray-900 dark:text-white">
          {{ showVerification ? 'Подтверждение email' : 'Регистрация' }}
        </h1>
        <p v-if="!showVerification" class="mt-2 text-center text-sm text-gray-600 dark:text-gray-400">
          Уже есть аккаунт?
          <NuxtLink to="/user/login" class="font-medium text-blue-600 hover:text-blue-500 dark:text-blue-400 dark:hover:text-blue-300 transition">
            Войдите
          </NuxtLink>
        </p>
        <p v-else class="mt-2 text-center text-sm text-gray-600 dark:text-gray-400">
          Код отправлен на <span class="font-medium text-gray-900 dark:text-white">{{ form.email }}</span>
        </p>
      </div>

      <!-- Блок ошибок -->
      <div v-if="errors.length > 0" class="rounded-md bg-red-50 dark:bg-red-900/20 p-4">
        <div class="flex">
          <div class="flex-shrink-0">
            <svg class="h-5 w-5 text-red-400 dark:text-red-300" xmlns="http://www.w3.org/2000/svg" viewBox="0 0 20 20" fill="currentColor" aria-hidden="true">
              <path fill-rule="evenodd" d="M10 18a8 8 0 100-16 8 8 0 000 16zM8.707 7.293a1 1 0 00-1.414 1.414L8.586 10l-1.293 1.293a1 1 0 101.414 1.414L10 11.414l1.293 1.293a1 1 0 001.414-1.414L11.414 10l1.293-1.293a1 1 0 00-1.414-1.414L10 8.586 8.707 7.293z" clip-rule="evenodd" />
            </svg>
          </div>
          <div class="ml-3">
            <h3 class="text-sm font-medium text-red-800 dark:text-red-200">Ошибка</h3>
            <div class="mt-2 text-sm text-red-700 dark:text-red-300">
              <ul class="list-disc list-inside space-y-1">
                <li v-for="(error, index) in errors" :key="index">{{ error }}</li>
              </ul>
            </div>
          </div>
        </div>
      </div>

      <!-- Форма регистрации -->
      <form v-if="!showVerification" class="mt-8 space-y-6" @submit.prevent="submitForm">
        <div class="space-y-4 rounded-md shadow-sm">
          <div>
            <label for="username" class="sr-only">Имя пользователя</label>
            <input
              id="username"
              v-model="form.username"
              type="text"
              autocomplete="username"
              required
              class="appearance-none relative block w-full px-3 py-3 border border-gray-300 dark:border-gray-600 placeholder-gray-500 dark:placeholder-gray-400 text-gray-900 dark:text-white rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-500 focus:border-blue-500 dark:focus:ring-blue-400 dark:focus:border-blue-400 focus:z-10 sm:text-sm bg-white dark:bg-gray-800"
              placeholder="Имя пользователя"
            />
          </div>
          <div>
            <label for="email" class="sr-only">Email</label>
            <input
              id="email"
              v-model="form.email"
              type="email"
              autocomplete="email"
              required
              class="appearance-none relative block w-full px-3 py-3 border border-gray-300 dark:border-gray-600 placeholder-gray-500 dark:placeholder-gray-400 text-gray-900 dark:text-white rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-500 focus:border-blue-500 dark:focus:ring-blue-400 dark:focus:border-blue-400 focus:z-10 sm:text-sm bg-white dark:bg-gray-800"
              placeholder="Email"
            />
          </div>
          <div>
            <label for="password" class="sr-only">Пароль</label>
            <input
              id="password"
              v-model="form.password"
              type="password"
              autocomplete="new-password"
              required
              class="appearance-none relative block w-full px-3 py-3 border border-gray-300 dark:border-gray-600 placeholder-gray-500 dark:placeholder-gray-400 text-gray-900 dark:text-white rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-500 focus:border-blue-500 dark:focus:ring-blue-400 dark:focus:border-blue-400 focus:z-10 sm:text-sm bg-white dark:bg-gray-800"
              placeholder="Пароль"
            />
          </div>
          <!-- ✅ Добавлено поле подтверждения пароля -->
          <div>
            <label for="re_password" class="sr-only">Подтверждение пароля</label>
            <input
              id="re_password"
              v-model="form.re_password"
              type="password"
              autocomplete="new-password"
              required
              class="appearance-none relative block w-full px-3 py-3 border border-gray-300 dark:border-gray-600 placeholder-gray-500 dark:placeholder-gray-400 text-gray-900 dark:text-white rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-500 focus:border-blue-500 dark:focus:ring-blue-400 dark:focus:border-blue-400 focus:z-10 sm:text-sm bg-white dark:bg-gray-800"
              placeholder="Подтверждение пароля"
            />
          </div>
        </div>

        <div>
          <button
            type="submit"
            :disabled="loading"
            class="group relative w-full flex justify-center py-3 px-4 border border-transparent text-sm font-medium rounded-lg text-white bg-blue-600 hover:bg-blue-700 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-blue-500 dark:focus:ring-offset-gray-900 disabled:opacity-50 disabled:cursor-not-allowed transition"
          >
            <span v-if="loading" class="absolute left-0 inset-y-0 flex items-center pl-3">
              <svg class="animate-spin h-5 w-5 text-white" xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24">
                <circle class="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" stroke-width="4"></circle>
                <path class="opacity-75" fill="currentColor" d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4zm2 5.291A7.962 7.962 0 014 12H0c0 3.042 1.135 5.824 3 7.938l3-2.647z"></path>
              </svg>
            </span>
            {{ loading ? 'Регистрация...' : 'Зарегистрироваться' }}
          </button>
        </div>
      </form>

      <!-- Форма подтверждения кода -->
      <div v-if="showVerification" class="mt-8 space-y-6">
        <!-- Иконка -->
        <div class="flex justify-center">
          <div class="w-16 h-16 bg-blue-100 dark:bg-blue-900 rounded-full flex items-center justify-center">
            <svg class="w-8 h-8 text-blue-600 dark:text-blue-300" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M3 8l7.89 5.26a2 2 0 002.22 0L21 8M5 19h14a2 2 0 002-2V7a2 2 0 00-2-2H5a2 2 0 00-2 2v10a2 2 0 002 2z" />
            </svg>
          </div>
        </div>

        <!-- Поля ввода кода -->
        <div>
          <label class="block text-sm font-medium text-gray-700 dark:text-gray-300 mb-3 text-center">
            Введите 6-значный код
          </label>
          <div class="flex justify-center space-x-2">
            <input
              v-for="(digit, index) in 6"
              :key="index"
              :ref="el => { if (el) codeInputs[index] = el }"
              v-model="codeDigits[index]"
              type="text"
              maxlength="1"
              @input="handleCodeInput(index, $event)"
              @keydown.backspace="handleCodeBackspace(index, $event)"
              @paste="handleCodePaste"
              class="w-12 h-14 text-center text-2xl font-bold border border-gray-300 dark:border-gray-600 rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-500 focus:border-blue-500 dark:focus:ring-blue-400 dark:focus:border-blue-400 bg-white dark:bg-gray-800 text-gray-900 dark:text-white"
            />
          </div>
        </div>

        <!-- Ошибка кода -->
        <div v-if="codeError" class="text-center text-sm text-red-600 dark:text-red-400">
          {{ codeError }}
        </div>

        <!-- Таймер повторной отправки -->
        <div class="text-center">
          <button
            v-if="canResend"
            @click="resendCode"
            :disabled="resendLoading"
            class="text-sm text-blue-600 hover:text-blue-500 dark:text-blue-400 dark:hover:text-blue-300 font-medium disabled:opacity-50"
          >
            {{ resendLoading ? 'Отправка...' : 'Отправить код повторно' }}
          </button>
          <p v-else class="text-sm text-gray-500 dark:text-gray-400">
            Отправить повторно через {{ resendTimer }} сек
          </p>
        </div>

        <!-- Кнопка подтверждения -->
        <div>
          <button
            @click="verifyCode"
            :disabled="verificationLoading || codeDigits.join('').length !== 6"
            class="group relative w-full flex justify-center py-3 px-4 border border-transparent text-sm font-medium rounded-lg text-white bg-blue-600 hover:bg-blue-700 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-blue-500 dark:focus:ring-offset-gray-900 disabled:opacity-50 disabled:cursor-not-allowed transition"
          >
            <span v-if="verificationLoading" class="absolute left-0 inset-y-0 flex items-center pl-3">
              <svg class="animate-spin h-5 w-5 text-white" xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24">
                <circle class="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" stroke-width="4"></circle>
                <path class="opacity-75" fill="currentColor" d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4zm2 5.291A7.962 7.962 0 014 12H0c0 3.042 1.135 5.824 3 7.938l3-2.647z"></path>
              </svg>
            </span>
            {{ verificationLoading ? 'Проверка...' : 'Подтвердить' }}
          </button>
        </div>

        <!-- Назад к регистрации -->
        <div class="text-center">
          <button
            @click="goBackToRegistration"
            class="text-sm text-gray-600 hover:text-gray-500 dark:text-gray-400 dark:hover:text-gray-300"
          >
            ← Назад к регистрации
          </button>
        </div>
      </div>

      <!-- Сообщение об успехе -->
      <div v-if="successMessage" class="rounded-md bg-green-50 dark:bg-green-900/20 p-4">
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
    </div>
  </main>
</template>

<script>
import axios from 'axios'
import { useToastStore } from '@/stores/toast'

export default {
  name: 'Signup',
  setup() {
    const toastStore = useToastStore()
    return { toastStore }
  },
  data() {
    return {
      form: {
        username: '',
        email: '',
        password: '',
        re_password: '', // ✅ Добавлено поле подтверждения
      },
      errors: [],
      loading: false,
      
      // Для подтверждения кода
      showVerification: false,
      codeDigits: ['', '', '', '', '', ''],
      codeInputs: [],
      codeError: '',
      verificationLoading: false,
      resendLoading: false,
      resendTimer: 60,
      canResend: false,
      resendTimerInterval: null,
      successMessage: '',
    }
  },
  mounted() {
    document.title = 'Регистрация | App'
  },
  beforeUnmount() {
    if (this.resendTimerInterval) {
      clearInterval(this.resendTimerInterval)
    }
  },
  methods: {
    async submitForm() {
      this.errors = []
      this.loading = true

      // Валидация
      if (!this.form.username) this.errors.push('Введите имя пользователя')
      if (!this.form.email) this.errors.push('Введите email')
      if (!this.form.password) this.errors.push('Введите пароль')
      if (!this.form.re_password) this.errors.push('Подтвердите пароль')
      if (this.form.password.length < 8) {
        this.errors.push('Пароль должен содержать минимум 8 символов')
      }
      if (this.form.password !== this.form.re_password) {
        this.errors.push('Пароли не совпадают')
      }

      if (this.errors.length > 0) {
        this.loading = false
        return
      }

      try {
        const response = await axios.post('http://127.0.0.1:8000/api/v1/auth/users/', this.form)
        
        if (response.status === 201) {
          this.showVerification = true
          this.errors = []
          this.codeError = ''
          this.startResendTimer()
          this.toastStore.showToast(5000, 'Код подтверждения отправлен на ваш email', 'bg-blue-100/40')
        }
      } catch (error) {
        console.error('Registration error:', error)
        if (error.response && error.response.data) {
          const data = error.response.data
          if (typeof data === 'object') {
            Object.keys(data).forEach(field => {
              const messages = data[field]
              if (Array.isArray(messages)) {
                this.errors.push(...messages)
              } else {
                this.errors.push(`${field}: ${messages}`)
              }
            })
          } else if (typeof data === 'string') {
            this.errors.push(data)
          } else {
            this.errors.push('Ошибка сервера. Проверьте введённые данные.')
          }
        } else if (error.request) {
          this.errors.push('Нет ответа от сервера. Проверьте соединение.')
        } else {
          this.errors.push('Ошибка при отправке запроса.')
        }
      } finally {
        this.loading = false
      }
    },

    handleCodeInput(index, event) {
      const value = event.target.value.replace(/\D/g, '')
      this.codeDigits[index] = value
      
      if (value && index < 5) {
        this.$nextTick(() => {
          this.codeInputs[index + 1]?.focus()
        })
      }
      
      this.codeError = ''
    },

    handleCodeBackspace(index, event) {
      if (!this.codeDigits[index] && index > 0) {
        this.codeInputs[index - 1]?.focus()
      }
    },

    handleCodePaste(event) {
      event.preventDefault()
      const pastedData = event.clipboardData.getData('text').replace(/\D/g, '').slice(0, 6)
      
      for (let i = 0; i < 6; i++) {
        this.codeDigits[i] = pastedData[i] || ''
      }
      
      const lastIndex = Math.min(pastedData.length, 5)
      this.codeInputs[lastIndex]?.focus()
      
      this.codeError = ''
    },

    async verifyCode() {
      const code = this.codeDigits.join('')
      if (code.length !== 6) return

      this.verificationLoading = true
      this.codeError = ''

      try {
        const response = await axios.post('http://127.0.0.1:8000/api/v1/auth/verify-code/', {
          email: this.form.email,
          code: code
        })

        if (response.status === 200) {
          this.successMessage = 'Email подтвержден! Сейчас вы будете перенаправлены на страницу входа...'
          this.toastStore.showToast(5000, 'Email подтвержден! Теперь вы можете войти.', 'bg-green-100/40')
          
          setTimeout(() => {
            this.$router.push('/user/login')
          }, 2000)
        }
      } catch (error) {
        if (error.response?.data) {
          const data = error.response.data
          this.codeError = data.detail || data.non_field_errors?.[0] || 'Неверный код подтверждения'
        } else {
          this.codeError = 'Ошибка проверки кода'
        }
        
        this.codeDigits = ['', '', '', '', '', '']
        this.$nextTick(() => {
          this.codeInputs[0]?.focus()
        })
      } finally {
        this.verificationLoading = false
      }
    },

    async resendCode() {
      this.resendLoading = true
      this.codeError = ''

      try {
        await axios.post('http://127.0.0.1:8000/api/v1/auth/resend-code/', {
          email: this.form.email
        })

        this.toastStore.showToast(3000, 'Новый код отправлен', 'bg-blue-100/40')
        this.startResendTimer()
        this.codeDigits = ['', '', '', '', '', '']
        this.$nextTick(() => {
          this.codeInputs[0]?.focus()
        })
      } catch (error) {
        if (error.response?.data) {
          const data = error.response.data
          this.codeError = data.detail || 'Ошибка отправки кода'
        } else {
          this.codeError = 'Ошибка отправки кода'
        }
      } finally {
        this.resendLoading = false
      }
    },

    startResendTimer() {
      this.canResend = false
      this.resendTimer = 60
      
      if (this.resendTimerInterval) {
        clearInterval(this.resendTimerInterval)
      }
      
      this.resendTimerInterval = setInterval(() => {
        this.resendTimer--
        if (this.resendTimer <= 0) {
          this.canResend = true
          clearInterval(this.resendTimerInterval)
        }
      }, 1000)
    },

    goBackToRegistration() {
      this.showVerification = false
      this.codeDigits = ['', '', '', '', '', '']
      this.codeError = ''
      this.successMessage = ''
      if (this.resendTimerInterval) {
        clearInterval(this.resendTimerInterval)
      }
    }
  }
}
</script>