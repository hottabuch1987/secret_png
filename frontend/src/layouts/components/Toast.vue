<script setup>
import { useToastStore } from '@/stores/toast'

const store = useToastStore()
</script>

<template>
    <div
        v-if="store.isVisible"
        class="transition ease-in-out delay-500 duration-500 px-6 py-6   absolute right-8 rounded-xl shadow-xl"
        :class="store.classes"
    >
        {{ store.message }}
    </div>
</template>