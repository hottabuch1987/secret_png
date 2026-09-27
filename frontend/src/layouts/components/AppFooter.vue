<template>
  <footer class="bg-white border-t border-gray-200 pt-12 pb-6 mt-auto">
    <div class="container mx-auto px-4">
      <!-- Блок рекламы с премиум каруселью -->
      <section v-if="advertisements.length > 0" class="mb-16">
        <!-- Заголовок с декоративными элементами -->
        <div class="relative text-center mb-10">
          <div class="absolute inset-0 flex items-center justify-center">
            <div class="w-24 h-px bg-gradient-to-r from-transparent via-blue-400 to-transparent"></div>
          </div>
          <h2 class="relative inline-flex items-center gap-3 px-6 bg-white text-2xl font-light">
            <span class="w-8 h-px bg-blue-400"></span>
            <span class="bg-gradient-to-r from-blue-600 to-purple-600 bg-clip-text text-transparent font-medium">
              Специальные предложения
            </span>
            <span class="w-8 h-px bg-blue-400"></span>
          </h2>
        </div>

        <!-- Индикатор загрузки -->
        <div v-if="advertisementsLoading" class="text-center py-16">
          <div class="relative inline-block">
            <div class="w-16 h-16 border-4 border-gray-200 border-t-blue-600 rounded-full animate-spin"></div>
            <div class="absolute inset-0 flex items-center justify-center">
              <span class="text-blue-600 text-xl">✨</span>
            </div>
          </div>
          <p class="text-gray-500 mt-4">Загружаем лучшие предложения...</p>
        </div>

        <!-- Ошибка -->
        <div v-else-if="advertisementsError" class="text-center py-16">
          <div class="inline-block p-6 bg-red-50 rounded-2xl">
            <span class="text-4xl mb-3 block">🎭</span>
            <p class="text-red-600 font-medium mb-3">{{ advertisementsError }}</p>
            <button 
              @click="fetchAdvertisements" 
              class="px-6 py-2 bg-red-600 text-white rounded-lg text-sm hover:bg-red-700 transition-colors shadow-md"
            >
              Попробовать снова
            </button>
          </div>
        </div>

        <!-- Премиум карусель Swiper без кнопок -->
        <Swiper
          v-else
          :modules="[SwiperAutoplay, SwiperPagination, SwiperEffectCreative]"
          :slides-per-view="1"
          :space-between="24"
          :loop="true"
          :speed="1000"
          :effect="'creative'"
          :creative-effect="{
            prev: {
              shadow: true,
              translate: ['-20%', 0, -1],
              scale: [0.9, 0.9, 1],
            },
            next: {
              translate: ['100%', 0, 0],
              scale: [0.9, 0.9, 1],
            },
          }"
          :autoplay="{ 
            delay: 5000, 
            disableOnInteraction: false,
            pauseOnMouseEnter: true 
          }"
          :pagination="{ 
            clickable: true,
            dynamicBullets: true,
            dynamicMainBullets: 5
          }"
          :breakpoints="{
            640: { slidesPerView: 1 },
            768: { slidesPerView: 2 },
            1024: { slidesPerView: 3 }
          }"
          class="px-4"
        >
          <SwiperSlide v-for="(ad, index) in advertisements" :key="ad.id">
            <a
              :href="ad.url"
              target="_blank"
              rel="noopener noreferrer"
              class="relative block w-full aspect-[3/4] rounded-3xl overflow-hidden group cursor-pointer"
            >
              <!-- Фоновое изображение с эффектом -->
              <div class="absolute inset-0 bg-gradient-to-br from-blue-500/20 to-purple-500/20 mix-blend-overlay z-10 opacity-0 group-hover:opacity-100 transition-opacity duration-700"></div>
              
              <img
                :src="ad.image"
                :alt="ad.title"
                class="w-full h-full object-cover transition-all duration-700 group-hover:scale-110"
                loading="lazy"
              />
              
              <!-- Многослойный градиент -->
              <div class="absolute inset-0 bg-gradient-to-t from-black/95 via-black/50 to-transparent opacity-90 z-20"></div>
              <div class="absolute inset-0 bg-gradient-to-br from-blue-600/20 to-transparent opacity-0 group-hover:opacity-100 transition-opacity duration-700 z-20"></div>
              
              <!-- Контент с элегантной анимацией -->
              <div class="absolute inset-x-0 bottom-0 p-6 z-30 transform transition-all duration-700 group-hover:translate-y-[-8px]">
                <!-- Премиум бейдж -->
                <div class="flex items-center gap-2 mb-3">
                  <span class="inline-flex items-center justify-center w-8 h-8 bg-white/10 backdrop-blur-sm rounded-2xl text-white text-xs font-light border border-white/20">
                    {{ String(index + 1).padStart(2, '0') }}
                  </span>
                  <span class="text-[10px] tracking-wider text-white/60 uppercase">
                    Эксклюзив
                  </span>
                </div>
                
                <!-- Заголовок с эффектом появления -->
                <h3 class="text-white text-xl font-light mb-2 tracking-wide transform transition-all duration-700 group-hover:translate-x-2">
                  {{ ad.title }}
                </h3>
                
                <!-- Описание с постепенным появлением -->
                <p v-if="ad.description" class="text-white/70 text-sm mb-4 line-clamp-2 transform transition-all duration-700 delay-100 opacity-80 group-hover:opacity-100">
                  {{ ad.description }}
                </p>
                
                <!-- Нижняя панель -->
                <div class="flex items-center justify-between pt-2 border-t border-white/10 transform transition-all duration-700 delay-200">
                  <span class="text-xs text-white/40 flex items-center gap-2">
                    <span class="w-4 h-px bg-white/40 group-hover:w-8 transition-all duration-700"></span>
                    Узнать больше
                  </span>
                  <span class="text-[10px] text-white/30 px-2 py-1 rounded-full border border-white/10">
                    Реклама
                  </span>
                </div>
              </div>

              <!-- Элегантный блеск при наведении -->
              <div class="absolute inset-0 opacity-0 group-hover:opacity-100 transition-opacity duration-1000 pointer-events-none z-40">
                <div class="absolute top-0 -inset-full w-full h-full transform -skew-x-12 bg-gradient-to-r from-transparent via-white/5 to-transparent group-hover:animate-shimmer"></div>
              </div>
            </a>
          </SwiperSlide>
        </Swiper>

        <!-- Минималистичный индикатор количества -->
        <div class="flex justify-center items-center gap-3 mt-8">
          <span class="w-12 h-px bg-gradient-to-r from-transparent to-gray-300"></span>
          <span class="text-xs text-gray-400 tracking-wider">
            {{ advertisements.length }} ПРЕДЛОЖЕНИЙ
          </span>
          <span class="w-12 h-px bg-gradient-to-l from-transparent to-gray-300"></span>
        </div>
      </section>

      <!-- Основная сетка футера -->
      <div class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-5 gap-8 mb-8">
        <!-- Колонка 1: Логотип и описание -->
        <div class="lg:col-span-1">
          <h2 class="text-xl font-light text-gray-800 mb-3 tracking-wide"> <span class="font-bold bg-gradient-to-r from-blue-600 to-purple-600 bg-clip-text text-transparent">СЕРВИС</span></h2>
          <p class="text-sm text-gray-500 font-light leading-relaxed">
            позволяет спрятать текст в картинку и переслать 
          </p>
        </div>

        

        <!-- Колонка 3: Ресурсы -->
        <div>
          <h3 class="text-xs font-semibold text-gray-400 uppercase tracking-wider mb-4">Ресурсы</h3>
          <ul class="space-y-3">
            <li><a href="/" class="text-gray-600 hover:text-blue-600 text-sm transition font-light">Документация</a></li>
            <li><a href="/" class="text-gray-600 hover:text-blue-600 text-sm transition font-light">Сообщество</a></li>
            <li><a href="/" class="text-gray-600 hover:text-blue-600 text-sm transition font-light">Поддержка</a></li>
          </ul>
        </div>

        <!-- Колонка 4: Компания -->
        <div>
          <h3 class="text-xs font-semibold text-gray-400 uppercase tracking-wider mb-4">Компания</h3>
          <ul class="space-y-3">
            <li><a href="/" class="text-gray-600 hover:text-blue-600 text-sm transition font-light">О нас</a></li>
            <li><a href="/" class="text-gray-600 hover:text-blue-600 text-sm transition font-light">Карьера</a></li>
            <li><a href="/" class="text-gray-600 hover:text-blue-600 text-sm transition font-light">Контакты</a></li>
          </ul>
        </div>

        <!-- Колонка 5: Правовая информация -->
        <div>
          <h3 class="text-xs font-semibold text-gray-400 uppercase tracking-wider mb-4">Правовая</h3>
          <ul class="space-y-3">
            <li><a href="/" class="text-gray-600 hover:text-blue-600 text-sm transition font-light">Конфиденциальность</a></li>
            <li><a href="/" class="text-gray-600 hover:text-blue-600 text-sm transition font-light">Условия использования</a></li>
            <li><a href="/" class="text-gray-600 hover:text-blue-600 text-sm transition font-light">Лицензии</a></li>
          </ul>
        </div>
      </div>

      <!-- Нижняя часть с копирайтом и соцсетями -->
      <div class="border-t border-gray-100 pt-6 flex flex-col sm:flex-row justify-between items-center">
        <p class="text-gray-400 text-xs font-light">
          &copy; {{ new Date().getFullYear() }}  Все права защищены.
        </p>
        <div class="flex space-x-6 mt-4 sm:mt-0">
          <!-- Иконки социальных сетей в минималистичном стиле -->
          <a href="/" aria-label="Twitter" class="text-gray-400 hover:text-blue-400 transition">
            <svg class="w-4 h-4" fill="currentColor" viewBox="0 0 24 24"><path d="M8.29 20.251c7.547 0 11.675-6.253 11.675-11.675 0-.178 0-.355-.012-.53A8.348 8.348 0 0022 5.92a8.19 8.19 0 01-2.357.646 4.118 4.118 0 001.804-2.27 8.224 8.224 0 01-2.605.996 4.107 4.107 0 00-6.993 3.743 11.65 11.65 0 01-8.457-4.287 4.106 4.106 0 001.27 5.477A4.072 4.072 0 012.8 9.713v.052a4.105 4.105 0 003.292 4.022 4.095 4.095 0 01-1.853.07 4.108 4.108 0 003.834 2.85A8.233 8.233 0 012 18.407a11.616 11.616 0 006.29 1.84"/></svg>
          </a>
          <a href="/" aria-label="GitHub" class="text-gray-400 hover:text-gray-900 transition">
            <svg class="w-4 h-4" fill="currentColor" viewBox="0 0 24 24"><path d="M12 2C6.477 2 2 6.484 2 12.017c0 4.425 2.865 8.18 6.839 9.504.5.092.682-.217.682-.483 0-.237-.008-.868-.013-1.703-2.782.605-3.369-1.343-3.369-1.343-.454-1.158-1.11-1.466-1.11-1.466-.908-.62.069-.608.069-.608 1.003.07 1.531 1.032 1.531 1.032.892 1.53 2.341 1.088 2.91.832.092-.647.35-1.088.636-1.338-2.22-.253-4.555-1.113-4.555-4.951 0-1.093.39-1.988 1.029-2.688-.103-.253-.446-1.272.098-2.65 0 0 .84-.27 2.75 1.026A9.564 9.564 0 0112 6.844c.85.004 1.705.115 2.504.337 1.909-1.296 2.747-1.027 2.747-1.027.546 1.379.202 2.398.1 2.651.64.7 1.028 1.595 1.028 2.688 0 3.848-2.339 4.695-4.566 4.943.359.309.678.92.678 1.855 0 1.338-.012 2.419-.012 2.747 0 .268.18.58.688.482A10.019 10.019 0 0022 12.017C22 6.484 17.522 2 12 2z"/></svg>
          </a>
        </div>
      </div>

      <!-- Финальная строка -->
      <p class="text-[10px] text-center text-gray-300 mt-6 font-light tracking-wider">
        СДЕЛАНО С ❤️ КОМАНДОЙ РАЗРАБОТЧИКОВ
      </p>
    </div>
  </footer>
</template>

<script>
import axios from 'axios'
import { Swiper, SwiperSlide } from 'swiper/vue'
import 'swiper/css'
import 'swiper/css/autoplay'
import 'swiper/css/pagination'
import 'swiper/css/effect-creative'

import { Autoplay, Pagination, EffectCreative } from 'swiper/modules'

export default {
  name: 'AppFooter',

  components: {
    Swiper,
    SwiperSlide
  },

  data() {
    return {
      advertisements: [],
      advertisementsLoading: false,
      advertisementsError: null,
      SwiperAutoplay: Autoplay,
      SwiperPagination: Pagination,
      SwiperEffectCreative: EffectCreative
    }
  },

  mounted() {
    this.fetchAdvertisements()
  },

  methods: {
    async fetchAdvertisements() {
      this.advertisementsLoading = true
      this.advertisementsError = null

      try {
        const response = await axios.get('/')
        this.advertisements = response.data.results || response.data || []
      } catch (error) {
        console.error('Ошибка при загрузке рекламы:', error)
        this.advertisementsError = 'Не удалось загрузить рекламные предложения'
      } finally {
        this.advertisementsLoading = false
      }
    }
  }
}
</script>

<style scoped>
/* Элегантная пагинация */
:deep(.swiper-pagination) {
  bottom: -30px !important;
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

:deep(.swiper-pagination-bullet-active-main) {
  transform: scale(1);
}

/* Анимация блеска */
@keyframes shimmer {
  100% {
    transform: translateX(200%) skewX(-12deg);
  }
}

:deep(.group-hover\:animate-shimmer) {
  animation: shimmer 1.5s infinite;
}

/* Стили для ограничения текста */
.line-clamp-2 {
  display: -webkit-box;
  -webkit-line-clamp: 2;
  -webkit-box-orient: vertical;
  overflow: hidden;
}

/* Плавные переходы для слайдов */
:deep(.swiper-slide) {
  transition: all 0.4s ease;
}

/* Эффект при наведении на весь слайдер */
:deep(.swiper:hover .swiper-slide:not(:hover)) {
  opacity: 0.8;
  filter: blur(0.5px);
}
</style>