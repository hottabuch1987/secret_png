<!-- pages/index.vue -->
<template>
  <div>
    <!-- Секция с баннерами (премиум карусель Swiper) -->
    <section v-if="banners.length" class="bg-gradient-to-b from-gray-50 to-white dark:from-gray-900 dark:to-gray-800 py-12">
      <div class="container mx-auto px-4">
        <!-- Заголовок с декоративными элементами -->
        <div class="relative text-center mb-10">
          <div class="absolute inset-0 flex items-center justify-center">
            <div class="w-32 h-px bg-gradient-to-r from-transparent via-blue-400 to-transparent"></div>
          </div>
          <div class="relative inline-flex items-center gap-4 px-6 bg-white dark:bg-gray-800 rounded-full py-2 shadow-sm">
            <span class="text-2xl">🎬</span>
            <h2 class="text-xl md:text-2xl font-light bg-gradient-to-r from-blue-600 to-purple-600 bg-clip-text text-transparent">
              Акции и новинки
            </h2>
            <span class="text-2xl">🍿</span>
          </div>
        </div>

        <!-- Индикатор загрузки -->
        <div v-if="bannersLoading" class="text-center py-20">
          <div class="relative inline-block">
            <div class="w-20 h-20 border-4 border-blue-100 dark:border-blue-900 border-t-blue-600 rounded-full animate-spin"></div>
            <div class="absolute inset-0 flex items-center justify-center">
              <div class="w-10 h-10 bg-gradient-to-br from-blue-500 to-purple-500 rounded-full animate-pulse"></div>
            </div>
            <div class="absolute inset-0 flex items-center justify-center">
              <span class="text-white text-sm font-bold">✨</span>
            </div>
          </div>
          <p class="text-gray-500 dark:text-gray-400 mt-6 font-light tracking-wide">Загружаем свежие предложения...</p>
        </div>

        <!-- Ошибка -->
        <div v-else-if="bannersError" class="text-center py-16">
          <div class="inline-block p-8 bg-gradient-to-br from-red-50 to-orange-50 dark:from-red-900/20 dark:to-orange-900/20 rounded-3xl">
            <span class="text-5xl mb-4 block">🎭</span>
            <p class="text-red-600 dark:text-red-400 font-medium mb-4">{{ bannersError }}</p>
            <button 
              @click="loadBanners" 
              class="px-8 py-3 bg-gradient-to-r from-red-500 to-orange-500 text-white rounded-full text-sm hover:from-red-600 hover:to-orange-600 transition-all shadow-lg hover:shadow-xl transform hover:scale-105"
            >
              Попробовать снова
            </button>
          </div>
        </div>

        <!-- Премиум карусель Swiper -->
        <Swiper
          v-else
          :modules="[SwiperAutoplay, SwiperPagination, SwiperEffectCreative]"
          :slides-per-view="1"
          :space-between="24"
          :loop="true"
          :speed="1200"
          :effect="'creative'"
          :creative-effect="{
            prev: {
              shadow: true,
              translate: ['-20%', 0, -1],
              scale: [0.9, 0.9, 1],
              opacity: [0.7, 0.7, 1],
            },
            next: {
              translate: ['100%', 0, 0],
              scale: [0.9, 0.9, 1],
              opacity: [0.7, 0.7, 1],
            },
          }"
          :autoplay="{ 
            delay: 4500, 
            disableOnInteraction: false,
            pauseOnMouseEnter: true,
            waitForTransition: true
          }"
          :pagination="{ 
            clickable: true,
            dynamicBullets: true,
            dynamicMainBullets: 5
          }"
          :breakpoints="{
            640: { slidesPerView: 1 },
            768: { 
              slidesPerView: 2,
              spaceBetween: 24
            },
            1024: { 
              slidesPerView: 3,
              spaceBetween: 30
            }
          }"
          class="px-2 md:px-4"
        >
          <SwiperSlide v-for="(banner, index) in banners" :key="banner.id">
            <component
              :is="banner.url ? 'a' : 'div'"
              :href="banner.url"
              :target="banner.url ? '_blank' : undefined"
              :rel="banner.url ? 'noopener noreferrer' : undefined"
              class="relative block w-full aspect-[4/3] md:aspect-[16/9] rounded-2xl overflow-hidden group cursor-pointer"
            >
              <div class="absolute inset-0 bg-gradient-to-br from-blue-600/20 to-purple-600/20 mix-blend-overlay z-10 opacity-0 group-hover:opacity-100 transition-opacity duration-700"></div>
              
              <div class="absolute inset-0">
                <img
                  :src="banner.image"
                  :alt="banner.title"
                  class="w-full h-full object-cover transition-all duration-1000 group-hover:scale-110 group-hover:rotate-1"
                  loading="lazy"
                />
              </div>
              
              <div class="absolute inset-0 bg-gradient-to-t from-black/90 via-black/40 to-transparent opacity-90 z-20"></div>
              <div class="absolute inset-0 bg-gradient-to-br from-blue-600/30 to-transparent opacity-0 group-hover:opacity-100 transition-opacity duration-700 z-20"></div>
              
              <div class="absolute top-4 left-4 z-30">
                <span class="inline-flex items-center justify-center w-10 h-10 bg-white/10 backdrop-blur-md rounded-2xl text-white text-sm font-light border border-white/20 shadow-xl">
                  #{{ String(index + 1).padStart(2, '0') }}
                </span>
              </div>
              
              <div v-if="index < 2" class="absolute top-4 right-4 z-30">
                <span class="inline-flex items-center gap-1 px-3 py-1.5 bg-gradient-to-r from-yellow-400 to-orange-500 text-white text-xs font-medium rounded-full shadow-lg">
                  <span class="w-1.5 h-1.5 bg-white rounded-full animate-pulse"></span>
                  НОВИНКА
                </span>
              </div>
              
              <div class="absolute inset-x-0 bottom-0 p-6 z-30 transform transition-all duration-700 group-hover:translate-y-[-8px]">
                <h3 class="text-white text-xl md:text-2xl font-light mb-2 tracking-wide transform transition-all duration-700 group-hover:translate-x-2 drop-shadow-lg">
                  {{ banner.title }}
                </h3>
                
                <p v-if="banner.description" class="text-white/80 text-sm mb-4 line-clamp-2 transform transition-all duration-700 delay-100 opacity-80 group-hover:opacity-100">
                  {{ banner.description }}
                </p>
                
                <div class="flex items-center gap-3 transform transition-all duration-700 delay-200">
                  <span class="text-xs text-white/60 flex items-center gap-2">
                    <span class="w-6 h-px bg-white/40 group-hover:w-12 transition-all duration-700"></span>
                    Подробнее
                  </span>
                  
                  <span class="inline-flex items-center justify-center w-6 h-6 rounded-full bg-white/10 backdrop-blur-sm opacity-0 group-hover:opacity-100 transition-all duration-500 transform translate-x-[-10px] group-hover:translate-x-0">
                    <svg class="w-3 h-3 text-white" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                      <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 5l7 7-7 7" />
                    </svg>
                  </span>
                </div>
              </div>

              <div class="absolute inset-0 opacity-0 group-hover:opacity-100 transition-opacity duration-1000 pointer-events-none z-40">
                <div class="absolute inset-0 bg-gradient-to-r from-transparent via-white/10 to-transparent transform -skew-x-12 animate-shimmer"></div>
              </div>

              <div class="absolute inset-0 border-2 border-transparent group-hover:border-white/20 rounded-2xl transition-all duration-500 z-50"></div>
            </component>
          </SwiperSlide>
        </Swiper>

        <!-- Нижняя панель -->
        <div class="flex flex-col sm:flex-row justify-between items-center gap-4 mt-10">
          <div class="flex items-center gap-3">
            <span class="w-12 h-px bg-gradient-to-r from-transparent to-blue-400"></span>
            <span class="text-xs text-gray-500 dark:text-gray-400 tracking-wider font-light">
              {{ banners.length }} АКТИВНЫХ ПРЕДЛОЖЕНИЙ
            </span>
            <span class="w-12 h-px bg-gradient-to-l from-transparent to-blue-400"></span>
          </div>

          <div class="flex items-center gap-4">
            <div class="flex items-center gap-2">
              <span class="w-2 h-2 bg-green-400 rounded-full animate-pulse"></span>
              <span class="text-xs text-gray-500 dark:text-gray-400">Обновляется ежедневно</span>
            </div>
            <span class="text-gray-300 dark:text-gray-600">|</span>
            <span class="text-xs text-gray-500 dark:text-gray-400">🔥 Горячие предложения</span>
          </div>
        </div>
      </div>
    </section>

    <!-- Секция с определением местоположения -->
    <section class="bg-white dark:bg-gray-900 py-12">
      <div class="container mx-auto px-4">
        <!-- Заголовок секции -->
        <div class="relative text-center mb-10">
          <div class="absolute inset-0 flex items-center justify-center">
            <div class="w-32 h-px bg-gradient-to-r from-transparent via-blue-400 to-transparent"></div>
          </div>
          
        </div>

        <!-- Компонент определения местоположения -->
        <LocationInfo />
      </div>
    </section>
  </div>
</template>

<script>
import { useUserStore } from '@/stores/user';
import axios from 'axios';

// Импортируем компоненты Swiper и стили
import { Swiper, SwiperSlide } from 'swiper/vue';
import 'swiper/css';
import 'swiper/css/autoplay';
import 'swiper/css/pagination';
import 'swiper/css/effect-creative';

// Импортируем модули Swiper
import { Autoplay, Pagination, EffectCreative } from 'swiper/modules';

// Импортируем компонент определения местоположения
import LocationInfo from '@/layouts/components/LocationInfo.vue';

export default {
  name: 'IndexPage',
  
  components: {
    Swiper,
    SwiperSlide,
    LocationInfo
  },

  data() {
    return {
      banners: [],
      bannersLoading: false,
      bannersError: null,
      SwiperAutoplay: Autoplay,
      SwiperPagination: Pagination,
      SwiperEffectCreative: EffectCreative
    };
  },

  mounted() {
    if (typeof window !== 'undefined') {
      this.loadBanners();
    }
  },

  methods: {
    async loadBanners() {
      this.bannersLoading = true;
      this.bannersError = null;
      
      try {
        const response = await axios.get('/');
        this.banners = response.data.results || response.data || [];
      } catch (err) {
        console.error('Ошибка загрузки баннеров:', err);
        this.bannersError = 'Не удалось загрузить баннеры';
      } finally {
        this.bannersLoading = false;
      }
    }
  }
};
</script>

<style scoped>
/* Анимация для эффекта свечения */
@keyframes shimmer {
  0% {
    transform: translateX(-200%) skewX(-12deg);
  }
  100% {
    transform: translateX(200%) skewX(-12deg);
  }
}

.animate-shimmer {
  animation: shimmer 2s infinite;
}

/* Стили для пагинации Swiper */
:deep(.swiper-pagination) {
  bottom: -35px !important;
}

:deep(.swiper-pagination-bullet) {
  width: 6px;
  height: 6px;
  background: #cbd5e1;
  opacity: 0.3;
  transition: all 0.4s cubic-bezier(0.4, 0, 0.2, 1);
}

:deep(.swiper-pagination-bullet-active) {
  width: 24px;
  border-radius: 3px;
  background: linear-gradient(90deg, #3b82f6, #8b5cf6);
  opacity: 0.8;
}

:deep(.dark .swiper-pagination-bullet) {
  background: #4b5563;
}

:deep(.dark .swiper-pagination-bullet-active) {
  background: linear-gradient(90deg, #60a5fa, #a78bfa);
}

/* Стили для ограничения текста */
.line-clamp-2 {
  display: -webkit-box;
  -webkit-line-clamp: 2;
  -webkit-box-orient: vertical;
  overflow: hidden;
}

/* Эффект при наведении на слайдер */
:deep(.swiper) {
  padding: 8px 4px;
  margin: -8px -4px;
}

:deep(.swiper-slide) {
  transition: all 0.4s ease;
  filter: brightness(0.95);
}

:deep(.swiper-slide-active) {
  filter: brightness(1);
}

:deep(.swiper:hover .swiper-slide:not(:hover)) {
  filter: brightness(0.8) blur(0.5px);
  opacity: 0.8;
}

/* Адаптивные корректировки */
@media (max-width: 640px) {
  :deep(.swiper-pagination) {
    bottom: -25px !important;
  }
  
  .line-clamp-2 {
    -webkit-line-clamp: 1;
  }
}
</style>