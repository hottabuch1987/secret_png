<template>
  <div class="flex flex-col min-h-screen">
    <AppHeader />
    
    <main class="flex-grow mt-20 container mx-auto px-4">
      <Toast />
      <slot />
    </main>
    
    <AppFooter />
  </div>
</template>

<script setup>
import AppHeader from './components/AppHeader.vue';
import AppFooter from './components/AppFooter.vue';
import Toast from './components/Toast.vue';
</script>