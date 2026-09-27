<!-- components/UserList.vue -->
<template>
  <div>
    <!-- Список онлайн пользователей с кнопкой звонка -->
    <div class="space-y-2 max-h-60 overflow-y-auto">
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
        
        <div class="ml-2 flex items-center gap-2">
          <span class="text-xs text-green-600 bg-green-50 px-2 py-1 rounded-full">
            Online
          </span>
          
          <!-- Кнопка видео-звонка -->
          <button
            @click="startVideoCall(user)"
            class="p-1.5 rounded-full hover:bg-blue-50 text-gray-400 hover:text-blue-600 transition group-hover:opacity-100 opacity-0"
            title="Видео-звонок"
          >
            <svg class="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M15 10l4.553-2.276A1 1 0 0121 8.618v6.764a1 1 0 01-1.447.894L15 14M5 18h8a2 2 0 002-2V8a2 2 0 00-2-2H5a2 2 0 00-2 2v8a2 2 0 002 2z" />
            </svg>
          </button>
          
          <!-- Кнопка аудио-звонка -->
          <button
            @click="startAudioCall(user)"
            class="p-1.5 rounded-full hover:bg-green-50 text-gray-400 hover:text-green-600 transition group-hover:opacity-100 opacity-0"
            title="Аудио-звонок"
          >
            <svg class="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M3 5a2 2 0 012-2h3.28a1 1 0 01.948.684l1.498 4.493a1 1 0 01-.502 1.21l-2.257 1.13a11.042 11.042 0 005.516 5.516l1.13-2.257a1 1 0 011.21-.502l4.493 1.498a1 1 0 01.684.949V19a2 2 0 01-2 2h-1C9.716 21 3 14.284 3 6V5z" />
            </svg>
          </button>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { useWebSocket } from '@/composables/useWebSocket'
import { useVideoCall } from '@/composables/useVideoCall'

const props = defineProps({
  onlineUsers: {
    type: Array,
    default: () => []
  }
})

const emit = defineEmits(['callStarted'])

const { initiateCall } = useWebSocket()
const { startCall } = useVideoCall()

const getUserInitials = (user) => {
  if (user.first_name && user.last_name) {
    return `${user.first_name[0]}${user.last_name[0]}`.toUpperCase()
  }
  if (user.first_name) {
    return user.first_name[0].toUpperCase()
  }
  return user.username ? user.username[0].toUpperCase() : '?'
}

const handleImageError = (event) => {
  event.target.style.display = 'none'
}

const startVideoCall = (user) => {
  console.log('📞 Starting video call with:', user.username)
  startCall(user.id, 'video')
  emit('callStarted', { user, type: 'video' })
}

const startAudioCall = (user) => {
  console.log('📞 Starting audio call with:', user.username)
  startCall(user.id, 'audio')
  emit('callStarted', { user, type: 'audio' })
}
</script>