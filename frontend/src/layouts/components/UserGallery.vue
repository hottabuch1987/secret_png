<!-- layouts/components/UserGallery.vue -->
<template>
  <div v-if="userId" class="space-y-4">
    <div class="flex items-center justify-between">
      <h3 class="text-lg font-semibold text-gray-800">Мои фото</h3>
      <button
        @click="triggerFileInput"
        :disabled="uploading || photos.length >= 10"
        class="px-4 py-2 text-sm font-medium text-white bg-blue-600 rounded-lg hover:bg-blue-700 transition disabled:opacity-50 disabled:cursor-not-allowed"
      >
        <span v-if="uploading">Загрузка...</span>
        <span v-else>Загрузить фото</span>
      </button>
      <input
        ref="fileInput"
        type="file"
        accept="image/*"
        class="hidden"
        @change="handleFileUpload"
      />
    </div>

    <p class="text-sm text-gray-500">{{ photos.length }}/10 фото</p>

    <!-- Галерея -->
    <div v-if="photos.length > 0" class="grid grid-cols-2 sm:grid-cols-3 md:grid-cols-4 gap-4">
      <div
        v-for="photo in photos"
        :key="photo.id"
        class="relative group rounded-lg overflow-hidden shadow-md hover:shadow-xl transition-shadow"
      >
        <img
          :src="getPhotoUrl(photo)"
          :alt="'Фото пользователя'"
          class="w-full h-48 object-cover"
          @error="handleImageError"
        />
        
        <div
          v-if="photo.is_avatar"
          class="absolute top-2 left-2 bg-blue-500 text-white text-xs px-2 py-1 rounded-full"
        >
          Главное
        </div>

        <div class="absolute inset-0 bg-black/50 opacity-0 group-hover:opacity-100 transition-opacity flex items-center justify-center gap-2">
          <button
            v-if="!photo.is_avatar"
            @click="setAvatar(photo.id)"
            class="p-2 bg-white rounded-full hover:bg-gray-100 transition"
            title="Сделать главным"
          >
            <svg class="w-4 h-4 text-gray-700" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M5 13l4 4L19 7" />
            </svg>
          </button>
          <button
            @click="deletePhoto(photo.id)"
            class="p-2 bg-white rounded-full hover:bg-red-100 transition"
            title="Удалить"
          >
            <svg class="w-4 h-4 text-red-600" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M19 7l-.867 12.142A2 2 0 0116.138 21H7.862a2 2 0 01-1.995-1.858L5 7m5 4v6m4-6v6m1-10V4a1 1 0 00-1-1h-4a1 1 0 00-1 1v3M4 7h16" />
            </svg>
          </button>
        </div>
      </div>
    </div>

    <div v-else class="text-center py-12 bg-gray-50 rounded-lg">
      <svg class="w-16 h-16 text-gray-300 mx-auto mb-3" fill="none" stroke="currentColor" viewBox="0 0 24 24">
        <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M4 16l4.586-4.586a2 2 0 012.828 0L16 16m-2-2l1.586-1.586a2 2 0 012.828 0L20 14m-6-6h.01M6 20h12a2 2 0 002-2V6a2 2 0 00-2-2H6a2 2 0 00-2 2v12a2 2 0 002 2z" />
      </svg>
      <p class="text-gray-500">У вас пока нет фото</p>
      <p class="text-sm text-gray-400 mt-1">Загрузите свое первое фото</p>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import { useUserStore } from '@/stores/user'
import { useToastStore } from '@/stores/toast'
import axios from 'axios'

const props = defineProps({
  userId: {
    type: String,
    required: true
  }
})

const config = useRuntimeConfig()
const apiBase = config.public.apiBase

const userStore = useUserStore()
const toastStore = useToastStore()

const photos = ref([])
const uploading = ref(false)
const fileInput = ref(null)

// ✅ Получение URL фото
const getPhotoUrl = (photo) => {
  if (!photo) return '/default-avatar.png'
  
  if (photo.image_url) {
    return photo.image_url
  }
  
  if (photo.image) {
    if (photo.image.startsWith('http')) {
      return photo.image
    }
    return `${apiBase}${photo.image}`
  }
  
  return '/default-avatar.png'
}

// ✅ Обработка ошибки загрузки изображения
const handleImageError = (event) => {
  event.target.src = '/default-avatar.png'
}

// ✅ Создаем экземпляр axios с токеном
const getAuthAxios = () => {
  const token = userStore.user.token
  if (!token) {
    console.error('❌ Нет токена авторизации')
    return axios
  }
  
  return axios.create({
    headers: {
      'Authorization': `Token ${token}`,
      'Content-Type': 'application/json',
    }
  })
}

// Загрузка фото
const loadPhotos = async () => {
  try {
    const authAxios = getAuthAxios()
    const response = await authAxios.get(`${apiBase}/photos/`)
    
    if (Array.isArray(response.data)) {
      photos.value = response.data
    } else if (response.data && typeof response.data === 'object') {
      if (Array.isArray(response.data.results)) {
        photos.value = response.data.results
      } else {
        photos.value = [response.data]
      }
    } else {
      photos.value = []
    }
    
    const avatarPhoto = photos.value.find(p => p.is_avatar)
    if (avatarPhoto) {
      userStore.user.avatar = getPhotoUrl(avatarPhoto)
    }
    
    console.log('📸 Загружено фото:', photos.value.length)
  } catch (error) {
    console.error('Error loading photos:', error)
    toastStore.showToast(5000, 'Ошибка загрузки фото', 'bg-red-500/20')
    photos.value = []
  }
}

// Триггер выбора файла
const triggerFileInput = () => {
  if (photos.value.length >= 10) {
    toastStore.showToast(5000, 'Максимальное количество фото - 10', 'bg-yellow-500/20')
    return
  }
  fileInput.value?.click()
}

// Загрузка файла
const handleFileUpload = async (event) => {
  const file = event.target.files[0]
  if (!file) return

  if (!file.type.startsWith('image/')) {
    toastStore.showToast(5000, 'Пожалуйста, выберите изображение', 'bg-yellow-500/20')
    return
  }

  if (file.size > 5 * 1024 * 1024) {
    toastStore.showToast(5000, 'Размер файла не должен превышать 5MB', 'bg-yellow-500/20')
    return
  }

  uploading.value = true

  const formData = new FormData()
  formData.append('image', file)

  try {
    const token = userStore.user.token
    const response = await axios.post(`${apiBase}/photos/`, formData, {
      headers: {
        'Content-Type': 'multipart/form-data',
        'Authorization': `Token ${token}`
      },
    })
    
    if (!Array.isArray(photos.value)) {
      photos.value = []
    }
    
    photos.value.unshift(response.data)
    toastStore.showToast(5000, 'Фото успешно загружено', 'bg-green-500/20')
    
    if (photos.value.length === 1) {
      await userStore.fetchUserInfo()
      userStore.user.avatar = getPhotoUrl(response.data)
    }
    
    console.log('✅ Фото загружено:', response.data)
  } catch (error) {
    console.error('Upload error:', error)
    toastStore.showToast(5000, 'Ошибка загрузки фото', 'bg-red-500/20')
  } finally {
    uploading.value = false
    if (fileInput.value) {
      fileInput.value.value = ''
    }
  }
}

// Установка аватара
const setAvatar = async (photoId) => {
  try {
    const token = userStore.user.token
    console.log('🔄 Установка аватара для фото:', photoId)
    
    await axios.post(`${apiBase}/photos/${photoId}/set_avatar/`, {}, {
      headers: {
        'Authorization': `Token ${token}`
      }
    })
    
    if (!Array.isArray(photos.value)) {
      photos.value = []
      return
    }
    
    photos.value = photos.value.map(photo => ({
      ...photo,
      is_avatar: photo.id === photoId
    }))
    
    const avatarPhoto = photos.value.find(p => p.is_avatar)
    if (avatarPhoto) {
      userStore.user.avatar = getPhotoUrl(avatarPhoto)
    }
    
    await userStore.fetchUserInfo()
    toastStore.showToast(5000, 'Главное фото обновлено', 'bg-green-500/20')
    console.log('✅ Аватар обновлен')
  } catch (error) {
    console.error('Set avatar error:', error)
    toastStore.showToast(5000, 'Ошибка установки главного фото', 'bg-red-500/20')
  }
}

// ✅ ИСПРАВЛЕНО: Удаление фото с явной передачей токена
const deletePhoto = async (photoId) => {
  if (!confirm('Вы уверены, что хотите удалить это фото?')) return

  const token = userStore.user.token
  
  if (!token) {
    toastStore.showToast(5000, 'Ошибка авторизации', 'bg-red-500/20')
    return
  }

  const url = `${apiBase}/photos/${photoId}/`
  console.log('🗑️ Удаление фото:', photoId)
  console.log('📡 URL запроса:', url)
  console.log('🔑 Токен:', token ? 'Есть' : 'Нет')

  try {
    const response = await axios.delete(url, {
      headers: {
        'Authorization': `Token ${token}`
      }
    })
    
    console.log('✅ Ответ сервера:', response.data)
    
    if (!Array.isArray(photos.value)) {
      photos.value = []
      return
    }
    
    // ✅ Удаляем фото из списка
    photos.value = photos.value.filter(photo => photo.id !== photoId)
    
    // ✅ Обновляем аватар если удалили главное фото
    const avatarPhoto = photos.value.find(p => p.is_avatar)
    if (avatarPhoto) {
      userStore.user.avatar = getPhotoUrl(avatarPhoto)
    } else {
      userStore.user.avatar = null
    }
    
    await userStore.fetchUserInfo()
    toastStore.showToast(5000, 'Фото успешно удалено', 'bg-green-500/20')
    console.log('✅ Фото удалено, осталось:', photos.value.length)
  } catch (error) {
    console.error('❌ Delete photo error:', error)
    console.error('❌ Статус ошибки:', error.response?.status)
    console.error('❌ Данные ошибки:', error.response?.data)
    
    if (error.response?.status === 401) {
      toastStore.showToast(5000, 'Сессия истекла, войдите заново', 'bg-red-500/20')
      userStore.removeToken()
    } else if (error.response?.status === 403) {
      toastStore.showToast(5000, 'Нет прав для удаления', 'bg-red-500/20')
    } else if (error.response?.status === 404) {
      toastStore.showToast(5000, 'Фото не найдено', 'bg-red-500/20')
    } else {
      toastStore.showToast(5000, 'Ошибка удаления фото', 'bg-red-500/20')
    }
  }
}

onMounted(() => {
  loadPhotos()
})
</script>