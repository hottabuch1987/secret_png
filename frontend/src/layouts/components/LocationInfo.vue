<!-- layouts/components/LocationInfo.vue -->
<template>
  <div class="location-info-wrapper">
    <!-- Загрузка -->
    <div v-if="loading" class="flex items-center justify-center py-8">
      <div class="relative inline-block">
        <div class="w-12 h-12 border-4 border-blue-100 border-t-blue-600 rounded-full animate-spin"></div>
        <div class="absolute inset-0 flex items-center justify-center">
          <span class="text-lg">📍</span>
        </div>
      </div>
      <p class="ml-3 text-gray-500 text-sm">Определение местоположения...</p>
    </div>

    <!-- Ошибка -->
    <div v-else-if="error" class="bg-red-50 dark:bg-red-900/20 rounded-xl p-4 border border-red-200 dark:border-red-800">
      <div class="flex items-center gap-3">
        <span class="text-2xl">⚠️</span>
        <div>
          <p class="text-sm font-medium text-red-700 dark:text-red-400">Ошибка определения местоположения</p>
          <p class="text-xs text-red-500 dark:text-red-300 mt-1">{{ error }}</p>
        </div>
      </div>
      <button 
        @click="detectLocation"
        class="mt-3 px-4 py-2 bg-red-600 text-white rounded-lg text-sm hover:bg-red-700 transition-colors"
      >
        Попробовать снова
      </button>
    </div>

    <!-- Данные о местоположении -->
    <div v-else-if="locationData" class="bg-white dark:bg-gray-800 rounded-2xl shadow-xl overflow-hidden border border-gray-100 dark:border-gray-700">
      <!-- Заголовок -->
      <div class="bg-gradient-to-r from-blue-500 to-purple-600 p-5">
        <div class="flex items-center justify-between">
          <div class="flex items-center gap-3">
            <div class="w-12 h-12 bg-white/20 backdrop-blur-sm rounded-full flex items-center justify-center">
              <span class="text-2xl">📍</span>
            </div>
            <div>
              <h3 class="text-white font-semibold text-lg">Ваше местоположение</h3>
              <p class="text-white/80 text-sm">Определено по IP адресу</p>
            </div>
          </div>
          <span class="px-3 py-1 bg-green-400/20 text-green-100 rounded-full text-xs font-medium">
            ✓ Успешно
          </span>
        </div>
      </div>

      <!-- Основная информация -->
      <div class="p-6">
        <div class="grid grid-cols-1 md:grid-cols-2 gap-4">
          <!-- Город -->
          <div class="bg-gray-50 dark:bg-gray-700/50 rounded-xl p-4">
            <div class="flex items-center gap-3">
              <div class="w-10 h-10 bg-blue-100 dark:bg-blue-900/30 rounded-full flex items-center justify-center">
                <svg class="w-5 h-5 text-blue-600 dark:text-blue-400" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M19 21V5a2 2 0 00-2-2H7a2 2 0 00-2 2v16m14 0h2m-2 0h-5m-9 0H3m2 0h5M9 7h1m-1 4h1m4-4h1m-1 4h1m-5 10v-5a1 1 0 011-1h2a1 1 0 011 1v5m-4 0h4" />
                </svg>
              </div>
              <div>
                <p class="text-xs text-gray-500 dark:text-gray-400">Город</p>
                <p class="text-sm font-semibold text-gray-800 dark:text-white">{{ locationData.city }}</p>
              </div>
            </div>
          </div>

          <!-- Регион -->
          <div class="bg-gray-50 dark:bg-gray-700/50 rounded-xl p-4">
            <div class="flex items-center gap-3">
              <div class="w-10 h-10 bg-purple-100 dark:bg-purple-900/30 rounded-full flex items-center justify-center">
                <svg class="w-5 h-5 text-purple-600 dark:text-purple-400" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M3.055 11H5a2 2 0 012 2v1a2 2 0 002 2 2 2 0 012 2v2.945M8 3.935V5.5A2.5 2.5 0 0010.5 8h.5a2 2 0 012 2 2 2 0 104 0 2 2 0 012-2h1.064M15 20.488V18a2 2 0 012-2h3.064M21 12a9 9 0 11-18 0 9 9 0 0118 0z" />
                </svg>
              </div>
              <div>
                <p class="text-xs text-gray-500 dark:text-gray-400">Регион</p>
                <p class="text-sm font-semibold text-gray-800 dark:text-white">{{ locationData.regionName }}</p>
              </div>
            </div>
          </div>

          <!-- Страна -->
          <div class="bg-gray-50 dark:bg-gray-700/50 rounded-xl p-4">
            <div class="flex items-center gap-3">
              <div class="w-10 h-10 bg-green-100 dark:bg-green-900/30 rounded-full flex items-center justify-center">
                <svg class="w-5 h-5 text-green-600 dark:text-green-400" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M3.055 11H5a2 2 0 012 2v1a2 2 0 002 2 2 2 0 012 2v2.945M8 3.935V5.5A2.5 2.5 0 0010.5 8h.5a2 2 0 012 2 2 2 0 104 0 2 2 0 012-2h1.064M15 20.488V18a2 2 0 012-2h3.064M21 12a9 9 0 11-18 0 9 9 0 0118 0z" />
                </svg>
              </div>
              <div>
                <p class="text-xs text-gray-500 dark:text-gray-400">Страна</p>
                <p class="text-sm font-semibold text-gray-800 dark:text-white">
                  {{ locationData.country }} ({{ locationData.countryCode }})
                </p>
              </div>
            </div>
          </div>

          <!-- Координаты -->
          <div class="bg-gray-50 dark:bg-gray-700/50 rounded-xl p-4">
            <div class="flex items-center gap-3">
              <div class="w-10 h-10 bg-yellow-100 dark:bg-yellow-900/30 rounded-full flex items-center justify-center">
                <svg class="w-5 h-5 text-yellow-600 dark:text-yellow-400" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M17.657 16.657L13.414 20.9a1.998 1.998 0 01-2.827 0l-4.244-4.243a8 8 0 1111.314 0z" />
                  <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M15 11a3 3 0 11-6 0 3 3 0 016 0z" />
                </svg>
              </div>
              <div>
                <p class="text-xs text-gray-500 dark:text-gray-400">Координаты</p>
                <p class="text-sm font-semibold text-gray-800 dark:text-white">
                  {{ locationData.lat }}, {{ locationData.lon }}
                </p>
              </div>
            </div>
          </div>
        </div>

        <!-- Дополнительная информация -->
        <div class="mt-4 space-y-2">
          <!-- IP адрес -->
          <div class="flex items-center justify-between py-2 border-b border-gray-100 dark:border-gray-700">
            <span class="text-sm text-gray-500 dark:text-gray-400">IP адрес</span>
            <span class="text-sm font-mono font-medium text-gray-800 dark:text-white">{{ locationData.query }}</span>
          </div>

          <!-- Почтовый индекс -->
          <div v-if="locationData.zip" class="flex items-center justify-between py-2 border-b border-gray-100 dark:border-gray-700">
            <span class="text-sm text-gray-500 dark:text-gray-400">Почтовый индекс</span>
            <span class="text-sm font-medium text-gray-800 dark:text-white">{{ locationData.zip }}</span>
          </div>

          <!-- Часовой пояс -->
          <div v-if="locationData.timezone" class="flex items-center justify-between py-2 border-b border-gray-100 dark:border-gray-700">
            <span class="text-sm text-gray-500 dark:text-gray-400">Часовой пояс</span>
            <span class="text-sm font-medium text-gray-800 dark:text-white">{{ locationData.timezone }}</span>
          </div>

          <!-- Провайдер -->
          <div v-if="locationData.isp" class="flex items-center justify-between py-2 border-b border-gray-100 dark:border-gray-700">
            <span class="text-sm text-gray-500 dark:text-gray-400">Провайдер</span>
            <span class="text-sm font-medium text-gray-800 dark:text-white">{{ locationData.isp }}</span>
          </div>

          <!-- Организация -->
          <div v-if="locationData.org" class="flex items-center justify-between py-2 border-b border-gray-100 dark:border-gray-700">
            <span class="text-sm text-gray-500 dark:text-gray-400">Организация</span>
            <span class="text-sm font-medium text-gray-800 dark:text-white">{{ locationData.org }}</span>
          </div>

          <!-- AS -->
          <div v-if="locationData.as" class="flex items-center justify-between py-2">
            <span class="text-sm text-gray-500 dark:text-gray-400">AS</span>
            <span class="text-sm font-medium text-gray-800 dark:text-white">{{ locationData.as }}</span>
          </div>
        </div>

        <!-- Кнопки -->
        <div class="mt-6 flex gap-3">
          <button 
            @click="detectLocation"
            class="flex-1 px-4 py-2.5 bg-blue-600 text-white rounded-lg text-sm font-medium hover:bg-blue-700 transition-colors"
          >
            🔄 Обновить
          </button>
          <button 
            @click="copyLocation"
            class="flex-1 px-4 py-2.5 bg-gray-100 dark:bg-gray-700 text-gray-700 dark:text-gray-300 rounded-lg text-sm font-medium hover:bg-gray-200 dark:hover:bg-gray-600 transition-colors"
          >
            📋 Копировать
          </button>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import axios from 'axios'
import { useUserStore } from '@/stores/user'

const userStore = useUserStore()
const loading = ref(false)
const error = ref(null)
const locationData = ref(null)

const detectLocation = async () => {
  loading.value = true
  error.value = null
  
  try {
    console.log('🌐 Определение местоположения по IP...')
    
    // Используем наш Django API вместо прямого запроса к ip-api.com
    const token = userStore.token
    const headers = token ? { 'Authorization': `Token ${token}` } : {}
    
    const response = await axios.get('/users/detect_location/', { headers })
    
    console.log('📍 Результат:', response.data)
    
    if (response.data && response.data.status === 'success') {
      // Преобразуем данные в формат, ожидаемый компонентом
      locationData.value = {
        ...response.data.data,
        query: response.data.data.ip,
        regionName: response.data.data.region,
        countryCode: response.data.data.country_code || response.data.data.countryCode
      }
    } else if (response.data && response.data.status === 'fallback') {
      // Используем данные по умолчанию
      locationData.value = {
        ...response.data.data,
        query: 'Не определен',
        regionName: response.data.data.region,
        countryCode: 'RU'
      }
    } else {
      error.value = response.data?.message || 'Не удалось определить местоположение'
    }
  } catch (err) {
    console.error('❌ Ошибка:', err)
    if (err.response?.data?.message) {
      error.value = err.response.data.message
    } else {
      error.value = 'Ошибка при определении местоположения'
    }
  } finally {
    loading.value = false
  }
}

const copyLocation = () => {
  if (!locationData.value) return
  
  const text = `
📍 Местоположение:
Город: ${locationData.value.city}
Регион: ${locationData.value.regionName || locationData.value.region}
Страна: ${locationData.value.country}
Координаты: ${locationData.value.lat}, ${locationData.value.lon}
IP: ${locationData.value.query || locationData.value.ip}
`.trim()
  
  navigator.clipboard.writeText(text).then(() => {
    alert('Информация скопирована в буфер обмена')
  }).catch(err => {
    console.error('Ошибка копирования:', err)
  })
}

onMounted(() => {
  detectLocation()
})
</script>

<style scoped>
.location-info-wrapper {
  width: 100%;
  max-width: 600px;
  margin: 0 auto;
}
</style>