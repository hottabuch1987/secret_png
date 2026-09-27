export default defineNuxtConfig({
  compatibilityDate: '2024-04-03',
  devtools: { enabled: true },
  css: ['~/assets/css/main.css'],
  modules: ['@pinia/nuxt'],
  postcss: {
    plugins: {
      tailwindcss: {},
      autoprefixer: {},
    },
  },
  runtimeConfig: {
    public: {
      apiBase: process.env.API_BASE_URL || 'http://127.0.0.1:8000/api/v1',
      wsUrl: 'ws://127.0.0.1:8000'
    }
  },

  // 👇 Добавляем проксирование media-файлов на Django
  nitro: {
        routeRules: {
      '/media/**': {
        proxy: process.env.NODE_ENV === 'production'
          ? 'http://app:8000/media/**'
          : 'http://127.0.0.1:8000/media/**'
      }
    }
  }
})