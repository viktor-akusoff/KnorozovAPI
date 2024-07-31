<script setup>
import { RouterView } from 'vue-router'
import { useStore } from 'vuex'
import { computed } from 'vue'
import HeaderBar from './components/HeaderBar.vue'

const store = useStore()

const auth_user = computed(() => store.getters.USER)
</script>

<template>
  <HeaderBar v-if="auth_user" :login="auth_user?.login" />
  <RouterView :auth_user="auth_user" />
</template>

<style scoped></style>
