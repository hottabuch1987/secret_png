<!-- pages/user/account.vue - ИСПРАВЛЕННАЯ ВЕРСИЯ -->
<template>
  <div v-if="isLoading" class="max-w-2xl mx-auto p-4">
    <div class="bg-white rounded-2xl shadow-xl overflow-hidden border border-gray-100 p-8">
      <div class="flex justify-center items-center h-64">
        <div class="text-center">
          <div class="animate-spin rounded-full h-12 w-12 border-b-2 border-blue-600 mx-auto"></div>
          <p class="mt-4 text-gray-500">Загрузка профиля...</p>
        </div>
      </div>
    </div>
  </div>

  <div v-else-if="!userStore.isAuthenticated" class="max-w-2xl mx-auto p-4">
    <div class="bg-white rounded-2xl shadow-xl overflow-hidden border border-gray-100 p-8">
      <div class="text-center">
        <svg class="w-16 h-16 text-gray-400 mx-auto mb-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
          <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 15v2m-6 4h12a2 2 0 002-2v-6a2 2 0 00-2-2H6a2 2 0 00-2 2v6a2 2 0 002 2zm10-10V7a4 4 0 00-8 0v4h8z" />
        </svg>
        <h3 class="text-lg font-semibold text-gray-800">Не авторизован</h3>
        <p class="text-gray-500 mt-2">Пожалуйста, войдите в систему</p>
        <NuxtLink to="/user/login" class="inline-block mt-4 px-6 py-2 bg-blue-600 text-white rounded-lg hover:bg-blue-700 transition">
          Войти
        </NuxtLink>
      </div>
    </div>
  </div>

  <div v-else class="max-w-2xl mx-auto p-4">
    <div class="bg-white rounded-2xl shadow-xl overflow-hidden border border-gray-100 hover:shadow-2xl transition-shadow duration-300">
      <!-- Градиентная шапка профиля -->
      <div class="h-32 bg-gradient-to-r from-blue-500 to-purple-600"></div>

      <!-- Аватар и основная информация -->
      <div class="relative px-6 pb-6">
        <!-- Аватар с инициалами или картинкой -->
        <div class="flex items-end -mt-12 mb-4">
          <div class="relative">
            <div class="w-24 h-24 rounded-full border-4 border-white bg-gray-200 shadow-lg flex items-center justify-center text-2xl font-bold text-gray-700 overflow-hidden">
              <img v-if="userStore.avatar" :src="userStore.avatar" alt="avatar" class="w-full h-full object-cover" />
              <span v-else>{{ userInitials }}</span>
            </div>
            
            <!-- Индикатор онлайн статуса -->
            <div class="absolute bottom-0 right-0 w-5 h-5 rounded-full border-2 border-white" 
                 :class="isOnline ? 'bg-green-500' : 'bg-gray-400'">
            </div>

            <!-- Кнопка редактирования аватара -->
            <button 
              @click="openGallery"
              class="absolute bottom-8 right-0 bg-white rounded-full p-1.5 shadow-md hover:shadow-lg transition border border-gray-200" 
              title="Редактировать аватар"
            >
              <svg class="w-4 h-4 text-gray-600" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M15.232 5.232l3.536 3.536m-2.036-5.036a2.5 2.5 0 113.536 3.536L6.5 21.036H3v-3.572L16.732 3.732z" />
              </svg>
            </button>
          </div>

          <div class="ml-6 flex-1">
            <div class="flex items-center justify-between">
              <div>
                <h2 class="text-2xl font-bold text-gray-800">{{ fullName || userStore.user.username }}</h2>
                <p class="text-gray-500 flex items-center mt-1">
                  <svg class="w-4 h-4 mr-1" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                    <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M16 7a4 4 0 11-8 0 4 4 0 018 0zM12 14a7 7 0 00-7 7h14a7 7 0 00-7-7z" />
                  </svg>
                  @{{ userStore.user.username }}
                </p>
              </div>
              
              <!-- Статус подключения к WebSocket -->
              <div class="flex items-center gap-2">
                <span class="text-xs px-2 py-1 rounded-full"
                      :class="isWsConnected ? 'bg-green-100 text-green-700' : 'bg-red-100 text-red-700'">
                  {{ isWsConnected ? '● Live' : '○ Offline' }}
                </span>
              </div>
            </div>
          </div>
        </div>

        <!-- Детали профиля в сетке -->
        <div class="grid grid-cols-1 md:grid-cols-2 gap-4 mt-6">
          <!-- Email -->
          <div class="flex items-center p-3 bg-gray-50 rounded-lg">
            <svg class="w-5 h-5 text-gray-500 mr-3" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M3 8l7.89 5.26a2 2 0 002.22 0L21 8M5 19h14a2 2 0 002-2V7a2 2 0 00-2-2H5a2 2 0 00-2 2v10a2 2 0 002 2z" />
            </svg>
            <div>
              <p class="text-xs text-gray-500">Email</p>
              <p class="text-sm font-medium text-gray-800">{{ userStore.user.email }}</p>
            </div>
          </div>

          <!-- Имя -->
          <div class="flex items-center p-3 bg-gray-50 rounded-lg">
            <svg class="w-5 h-5 text-gray-500 mr-3" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M16 7a4 4 0 11-8 0 4 4 0 018 0zM12 14a7 7 0 00-7 7h14a7 7 0 00-7-7z" />
            </svg>
            <div>
              <p class="text-xs text-gray-500">Имя</p>
              <p class="text-sm font-medium text-gray-800">{{ userStore.user.first_name || '—' }}</p>
            </div>
          </div>

          <!-- Фамилия -->
          <div class="flex items-center p-3 bg-gray-50 rounded-lg">
            <svg class="w-5 h-5 text-gray-500 mr-3" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M5.121 17.804A13.937 13.937 0 0112 16c2.5 0 4.847.655 6.879 1.804M15 10a3 3 0 11-6 0 3 3 0 016 0zm6 2a9 9 0 11-18 0 9 9 0 0118 0z" />
            </svg>
            <div>
              <p class="text-xs text-gray-500">Фамилия</p>
              <p class="text-sm font-medium text-gray-800">{{ userStore.user.last_name || '—' }}</p>
            </div>
          </div>

          <!-- Статус подтверждения email -->
          <div class="flex items-center p-3 bg-gray-50 rounded-lg col-span-2">
            <svg v-if="userStore.user.email_confirmed" class="w-5 h-5 text-green-500 mr-3" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 12l2 2 4-4m6 2a9 9 0 11-18 0 9 9 0 0118 0z" />
            </svg>
            <svg v-else class="w-5 h-5 text-yellow-500 mr-3" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 8v4m0 4h.01M21 12a9 9 0 11-18 0 9 9 0 0118 0z" />
            </svg>
            <div>
              <p class="text-xs text-gray-500">Статус email</p>
              <p class="text-sm font-medium" :class="userStore.user.email_confirmed ? 'text-green-700' : 'text-yellow-700'">
                {{ userStore.user.email_confirmed ? 'Подтвержден' : 'Не подтвержден' }}
              </p>
            </div>
          </div>
        </div>

        <!-- Кнопки действий -->
        <div class="flex justify-end space-x-3 mt-6">
          <NuxtLink
            to="/user/edit"
            class="px-4 py-2 text-sm font-medium text-gray-700 bg-gray-100 rounded-lg hover:bg-gray-200 transition flex items-center"
          >
            <svg class="w-4 h-4 mr-2" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M11 5H6a2 2 0 00-2 2v11a2 2 0 002 2h11a2 2 0 002-2v-5m-1.414-9.414a2 2 0 112.828 2.828L11.828 15H9v-2.828l8.586-8.586z" />
            </svg>
            Редактировать
          </NuxtLink>
          <button @click="logout" class="px-4 py-2 text-sm font-medium text-white bg-red-500 rounded-lg hover:bg-red-600 transition flex items-center">
            <svg class="w-4 h-4 mr-2" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M17 16l4-4m0 0l-4-4m4 4H7m6 4v1a3 3 0 01-3 3H6a3 3 0 01-3-3V7a3 3 0 013-3h4a3 3 0 013 3v1" />
            </svg>
            Выйти
          </button>
        </div>
      </div>

      <!-- Список онлайн пользователей с кнопками звонков -->
      <div class="px-6 pb-6 border-t border-gray-200 pt-6">
        <div class="flex items-center justify-between mb-4">
          <h3 class="text-lg font-semibold flex items-center">
            <span class="inline-block w-2 h-2 bg-green-500 rounded-full mr-2 animate-pulse"></span>
            Онлайн ({{ onlineUsersCount }})
          </h3>
          <div class="flex items-center gap-2">
            <button 
              @click="refreshOnlineUsers"
              class="text-sm text-blue-600 hover:text-blue-800 transition"
              :disabled="isRefreshing"
            >
              <svg class="w-4 h-4" :class="{ 'animate-spin': isRefreshing }" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M4 4v5h.582m15.356 2A8.001 8.001 0 004.582 9m0 0H9m11 11v-5h-.581m0 0a8.003 8.003 0 01-15.357-2m15.357 2H15" />
              </svg>
            </button>
          </div>
        </div>

        <div v-if="isLoadingOnline" class="text-center py-4">
          <div class="animate-spin rounded-full h-6 w-6 border-b-2 border-blue-600 mx-auto"></div>
        </div>
        <div v-else-if="onlineUsers.length === 0" class="text-gray-500 text-sm text-center py-4">
          <svg class="w-8 h-8 mx-auto text-gray-300 mb-2" fill="none" stroke="currentColor" viewBox="0 0 24 24">
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 4.354a4 4 0 110 5.292M15 21H3v-1a6 6 0 0112 0v1zm0 0h6v-1a6 6 0 00-9-5.197M13 7a4 4 0 11-8 0 4 4 0 018 0z" />
          </svg>
          Нет пользователей онлайн
        </div>
        <div v-else class="space-y-2 max-h-60 overflow-y-auto">
          <div 
            v-for="user in onlineUsers" 
            :key="user.id"
            class="flex items-center p-2 hover:bg-gray-50 rounded-lg transition group"
          >
            <div class="relative flex-shrink-0">
              <div class="w-10 h-10 rounded-full bg-gradient-to-br from-blue-400 to-purple-500 flex items-center justify-center text-white font-semibold text-sm shadow-md">
                <img 
                  v-if="user.avatar_url" 
                  :src="user.avatar_url" 
                  :alt="user.username"
                  class="w-full h-full rounded-full object-cover"
                  @error="handleImageError"
                />
                <span v-else>{{ getUserInitials(user) }}</span>
              </div>
              <span class="absolute bottom-0 right-0 w-3 h-3 bg-green-500 border-2 border-white rounded-full"></span>
            </div>
            
            <div class="ml-3 flex-1 min-w-0">
              <p class="text-sm font-medium text-gray-800 truncate">
                {{ user.full_name || user.username }}
              </p>
              <p class="text-xs text-gray-500 truncate">@{{ user.username }}</p>
            </div>
            
           
          </div>
        </div>
      </div>

      <!-- Галлерея фото -->
      <div v-if="userStore.user.id" class="px-6 pb-6 border-t border-gray-200 pt-6">
        <UserGallery :user-id="userStore.user.id" />
      </div>
    </div>
  </div>

  
</template>

<script setup>
import UserGallery from '@/layouts/components/UserGallery.vue'
import { computed, ref, onMounted, onUnmounted } from 'vue'
import { useRouter } from 'vue-router'
import { useUserStore } from '@/stores/user'
import { useToastStore } from '@/stores/toast'
import { useWebSocket } from '@/composables/useWebSocket'
import axios from 'axios'

const userStore = useUserStore()
const toastStore = useToastStore()
const router = useRouter()

// Состояние
const isLoading = ref(true)
const isLoadingOnline = ref(false)
const isRefreshing = ref(false)
const currentCallId = ref(null)
const currentReceiverId = ref(null)

// Используем WebSocket (один экземпляр для всего)
const { 
  isConnected: isWsConnected, 
  onlineUsers, 
  connect, 
  disconnect,
  getOnlineUsers: wsGetOnlineUsers,
  // Методы для видео-звонков из useWebSocket
  initiateCall,
  isCallActive,
  hasIncomingCall,
  incomingCall,
  callState
} = useWebSocket()

useHead({
  title: 'Мой профиль'
})

// Полное имя из first_name и last_name
const fullName = computed(() => {
  const first = userStore.user.first_name || ''
  const last = userStore.user.last_name || ''
  return first || last ? `${first} ${last}`.trim() : ''
})

// Инициалы для аватара (по умолчанию)
const userInitials = computed(() => {
  if (fullName.value) {
    const names = fullName.value.split(' ')
    return names.map(n => n[0]).join('').toUpperCase().slice(0, 2)
  }
  return userStore.user.username ? userStore.user.username[0].toUpperCase() : '?'
})

// Количество онлайн пользователей
const onlineUsersCount = computed(() => onlineUsers.value?.length || 0)

// Статус онлайн текущего пользователя
const isOnline = computed(() => {
  return onlineUsers.value?.some(user => user.id === userStore.user.id) || false
})



// Получить инициалы пользователя
const getUserInitials = (user) => {
  if (user.first_name && user.last_name) {
    return `${user.first_name[0]}${user.last_name[0]}`.toUpperCase()
  }
  if (user.first_name) {
    return user.first_name[0].toUpperCase()
  }
  return user.username ? user.username[0].toUpperCase() : '?'
}

// Обработка ошибки загрузки изображения
const handleImageError = (event) => {
  event.target.style.display = 'none'
}

// Открыть галлерею
const openGallery = () => {
  const galleryElement = document.querySelector('.border-t.border-gray-200.pt-6')
  if (galleryElement) {
    galleryElement.scrollIntoView({ behavior: 'smooth' })
  }
}

// Обновить список онлайн пользователей
const refreshOnlineUsers = async () => {
  isRefreshing.value = true
  try {
    if (isWsConnected.value) {
      wsGetOnlineUsers()
    } else {
      await fetchOnlineUsersFromAPI()
    }
  } finally {
    setTimeout(() => {
      isRefreshing.value = false
    }, 1000)
  }
}

// Получить онлайн пользователей через API
const fetchOnlineUsersFromAPI = async () => {
  isLoadingOnline.value = true
  try {
    const token = userStore.token
    console.log('🔍 Fetching online users with token:', token ? '✅ Present' : '❌ Missing')
    
    if (!token) {
      console.warn('⚠️ No token available for API request')
      return
    }
    
    const response = await axios.get('/users/online/', {
      headers: {
        'Authorization': `Token ${token}`
      }
    })
    
    console.log('📋 Online users from API:', response.data)
    
    if (response.data.online_users) {
      onlineUsers.value = response.data.online_users
    }
  } catch (error) {
    console.error('❌ Error fetching online users:', error)
    if (error.response?.status === 401) {
      console.warn('⚠️ Unauthorized - token may be invalid')
      userStore.removeToken()
      router.push('/user/login')
    }
    toastStore.showToast(5000, 'Ошибка загрузки списка онлайн пользователей', 'bg-red-500/20')
  } finally {
    isLoadingOnline.value = false
  }
}

// Выход из системы
const logout = async () => {
  try {
    await axios.post('/auth/token/logout/')
  } catch (error) {
    console.error('Logout error:', error)
  } finally {
    disconnect()
    userStore.removeToken()
    toastStore.showToast(5000, 'Вы вышли из системы успешно', 'bg-gray-300/10')
    router.push('/user/login')
  }
}

// Загрузка данных пользователя
const loadUserData = async () => {
  isLoading.value = true
  
  try {
    console.log('🔍 Loading user data...')
    console.log('🔍 Token from store:', userStore.token ? '✅ Present' : '❌ Missing')
    console.log('🔍 Is authenticated:', userStore.isAuthenticated)
    
    if (!userStore.token) {
      userStore.initStore()
    }
    
    if (!userStore.user.id && userStore.isAuthenticated) {
      await userStore.fetchUserInfo()
    }
    
    // Если пользователь авторизован, подключаем WebSocket и загружаем онлайн пользователей
    if (userStore.isAuthenticated && userStore.token) {
      console.log('🔌 Connecting WebSocket...')
      connect()
      
      // Небольшая задержка перед запросом онлайн пользователей
      setTimeout(async () => {
        await fetchOnlineUsersFromAPI()
      }, 500)
    } else {
      console.warn('⚠️ User not authenticated or no token')
    }
  } catch (error) {
    console.error('❌ Error loading user data:', error)
    toastStore.showToast(5000, 'Ошибка загрузки данных пользователя', 'bg-red-500/20')
    
    if (error.response?.status === 401) {
      userStore.removeToken()
      router.push('/user/login')
    }
  } finally {
    isLoading.value = false
  }
}

// Запуск видео-звонка
const startVideoCall = (user) => {
  console.log('📞 Starting video call with:', user.username)
  currentReceiverId.value = user.id
  
  const result = initiateCall(user.id, 'video')
  if (result) {
    toastStore.showToast(3000, `Видео-звонок пользователю ${user.username}...`, 'bg-blue-500/20')
  } else {
    toastStore.showToast(3000, 'Не удалось начать звонок', 'bg-red-500/20')
  }
}

// Запуск аудио-звонка
const startAudioCall = (user) => {
  console.log('📞 Starting audio call with:', user.username)
  currentReceiverId.value = user.id
  
  const result = initiateCall(user.id, 'audio')
  if (result) {
    toastStore.showToast(3000, `Аудио-звонок пользователю ${user.username}...`, 'bg-green-500/20')
  } else {
    toastStore.showToast(3000, 'Не удалось начать звонок', 'bg-red-500/20')
  }
}

// Обработка завершения звонка
const onCallEnded = () => {
  console.log('📞 Call ended')
  currentCallId.value = null
  currentReceiverId.value = null
  toastStore.showToast(3000, 'Звонок завершен', 'bg-gray-500/20')
}

// Жизненный цикл
onMounted(() => {
  console.log('🚀 Account page mounted')
  loadUserData()
})

onUnmounted(() => {
  console.log('🔌 Account page unmounting, disconnecting WebSocket')
  disconnect()
})
watch(hasIncomingCall, (newVal) => {
    console.log('🔄 hasIncomingCall changed:', newVal)
})

watch(incomingCall, (newVal) => {
    console.log('🔄 incomingCall changed:', newVal)
})

// Показывать ли видео-звонок
const showVideoCall = computed(() => {
    console.log('🔄 showVideoCall computed:', isCallActive.value, hasIncomingCall.value)
    return isCallActive.value || hasIncomingCall.value
})
</script>

<style scoped>
.animate-pulse {
  animation: pulse 2s cubic-bezier(0.4, 0, 0.6, 1) infinite;
}

@keyframes pulse {
  0%, 100% {
    opacity: 1;
  }
  50% {
    opacity: 0.5;
  }
}

.group:hover {
  background-color: #f9fafb;
}

/* Стили для скролла */
.max-h-60::-webkit-scrollbar {
  width: 6px;
}

.max-h-60::-webkit-scrollbar-track {
  background: #f1f1f1;
  border-radius: 10px;
}

.max-h-60::-webkit-scrollbar-thumb {
  background: #d1d5db;
  border-radius: 10px;
}

.max-h-60::-webkit-scrollbar-thumb:hover {
  background: #9ca3af;
}
</style>