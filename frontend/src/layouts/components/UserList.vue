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
          
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { useWebSocket } from '@/composables/useWebSocket'


const props = defineProps({
  onlineUsers: {
    type: Array,
    default: () => []
  }
})

const emit = defineEmits(['callStarted'])

const { initiateCall } = useWebSocket()


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


</script>